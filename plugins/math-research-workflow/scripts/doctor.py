#!/usr/bin/env python3
"""Environment preflight for the math-research-workflow pipeline.

Checks that the orchestrator runtime prerequisites exist in the current Codex
environment:

  - the workflow plugin itself is installed and enabled;
  - the dependency skills are available (as installed/enabled plugins, or as
    plain skills under $CODEX_HOME/skills);
  - the marketplace the plugin was installed from is registered (when a
    marketplace name is given);
  - config.toml still carries the enabled entry (when it can be located).

This script never modifies anything; it only reports and prints the exact
repair commands.  The desktop app has been observed to rewrite config.toml and
drop plugin-enable entries, so the workflow stage-A preflight should run this
before dispatch and re-add the plugin if a hard FAIL is reported.

Usage:
  python doctor.py [--plugin math-research-workflow]
                   [--marketplace math-research]
                   [--skills manage-math-research-program,rigorous-open-math-research,lean-verify]
                   [--list-file PLUGIN_LIST_TXT] [--json]

--list-file reads a saved `codex plugin list` transcript instead of invoking
codex (used by the smoke tests and for offline diagnosis).

Exit code 0 when all checks pass, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_PLUGIN = "math-research-workflow"
DEFAULT_MARKETPLACE = "math-research"
DEFAULT_SKILLS = (
    "manage-math-research-program",
    "rigorous-open-math-research",
    "lean-verify",
)


class Report:
    def __init__(self) -> None:
        self.entries: list[dict[str, Any]] = []
        self.checks = 0

    def ok(self, message: str) -> None:
        self.checks += 1
        self.entries.append({"status": "ok", "message": message})
        print(f"ok: {message}")

    def bad(self, message: str, repair: str = "") -> None:
        self.checks += 1
        item: dict[str, Any] = {"status": "FAIL", "message": message}
        if repair:
            item["repair"] = repair
        self.entries.append(item)
        print(f"FAIL: {message}")
        if repair:
            print(f"  repair: {repair}")

    def warn(self, message: str) -> None:
        self.checks += 1
        self.entries.append({"status": "warn", "message": message})
        print(f"warn: {message}")


def parse_plugin_list(text: str) -> dict[str, str]:
    """Map 'name@marketplace' to its status column from `codex plugin list`.

    Rows look like:
      math-research-workflow@math-research        installed, enabled  0.1.0+...  path
    The status is the second whitespace-delimited token.
    """
    result: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        tokens = re.split(r"\s{2,}", line)
        if not tokens:
            continue
        first = tokens[0].strip()
        if "@" not in first:
            continue
        status = tokens[1].strip() if len(tokens) > 1 else ""
        result[first] = status
    return result


def find_codex_home() -> Path:
    env = os.environ.get("CODEX_HOME")
    if env:
        return Path(env)
    return Path.home() / ".codex"


def run_codex(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["codex", *args], capture_output=True, text=True, errors="replace"
    )


def check_plugin(
    listing: dict[str, str], plugin: str, marketplace: str, report: Report
) -> None:
    key = f"{plugin}@{marketplace}"
    status = listing.get(key, "")
    if "installed" in status and "enabled" in status:
        report.ok(f"plugin {key} is installed and enabled ({status})")
        return
    if status:
        report.bad(
            f"plugin {key} is {status or 'present but not enabled'}; "
            "the workflow cannot dispatch without it",
            repair=f"codex plugin add {plugin}@{marketplace}",
        )
        return
    # Fallback: plugin may be enabled under another marketplace.
    for other_key, other_status in listing.items():
        if other_key.startswith(f"{plugin}@") and "installed" in other_status:
            report.warn(
                f"plugin {other_key} is {other_status}; re-add it under "
                f"marketplace {marketplace} to keep the pipeline preflight deterministic"
            )
            return
    report.bad(
        f"plugin {key} is not installed",
        repair=f"codex plugin add {plugin}@{marketplace}",
    )


def check_skills(
    listing: dict[str, str], skills: tuple[str, ...], home: Path, report: Report
) -> None:
    for skill in skills:
        found = False
        for key, status in listing.items():
            if key.startswith(f"{skill}@") and "installed" in status and "enabled" in status:
                report.ok(f"skill {skill} is available as plugin {key} ({status})")
                found = True
                break
        if found:
            continue
        if (home / "skills" / skill).is_dir():
            report.ok(f"skill {skill} is available as a plain skill under {home / 'skills'}")
            continue
        report.bad(
            f"skill {skill} is not installed and enabled, and no plain-skill "
            f"directory exists at {home / 'skills' / skill}",
            repair=f"codex plugin add {skill}@personal",
        )


def check_config(home: Path, plugin: str, marketplace: str, report: Report) -> None:
    config = home / "config.toml"
    if not config.is_file():
        report.warn(f"config.toml not found at {config}; skipping enable-entry check")
        return
    try:
        text = config.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        report.warn(f"cannot read {config}: {exc}")
        return
    section = f'[plugins."{plugin}@{marketplace}"]'
    if section not in text:
        report.bad(
            f"config.toml has no {section} section; the desktop app may have "
            "rewritten config.toml and dropped the enable entry",
            repair=f"codex plugin add {plugin}@{marketplace}",
        )
        return
    # The enabled line must appear within the section body (before the next [).
    rest = text.split(section, 1)[1]
    body = rest.split("\n[", 1)[0]
    if re.search(r"enabled\s*=\s*true", body):
        report.ok(f"config.toml enables {plugin}@{marketplace}")
    else:
        report.bad(
            f"config.toml section {section} exists but does not set enabled = true",
            repair=f"codex plugin add {plugin}@{marketplace}",
        )


def check_marketplace(
    marketplace: str, report: Report, listing_text: str = ""
) -> None:
    if not marketplace:
        return
    if listing_text:
        if marketplace in listing_text:
            report.ok(f"marketplace {marketplace} is registered")
            return
        report.bad(
            f"marketplace {marketplace} is not registered",
            repair=f"codex plugin marketplace add <owner>/<repo>",
        )
        return
    proc = run_codex(["plugin", "marketplace", "list"])
    if proc.returncode != 0:
        report.warn(f"cannot list marketplaces: {proc.stderr.strip() or proc.stdout.strip()}")
        return
    if marketplace in proc.stdout:
        report.ok(f"marketplace {marketplace} is registered")
    else:
        report.bad(
            f"marketplace {marketplace} is not registered",
            repair="codex plugin marketplace add <owner>/<repo>",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Math research workflow environment preflight")
    parser.add_argument("--plugin", default=DEFAULT_PLUGIN)
    parser.add_argument("--marketplace", default=DEFAULT_MARKETPLACE)
    parser.add_argument("--skills", default=",".join(DEFAULT_SKILLS))
    parser.add_argument("--list-file", help="read a saved `codex plugin list` transcript")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    args = parser.parse_args()

    report = Report()
    home = find_codex_home()

    if args.list_file:
        try:
            text = Path(args.list_file).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            report.bad(f"cannot read list file: {exc}")
            text = ""
        listing = parse_plugin_list(text)
    else:
        proc = run_codex(["plugin", "list"])
        if proc.returncode != 0:
            report.bad(
                "cannot run `codex plugin list`",
                repair="install the Codex CLI and ensure codex is on PATH",
            )
            listing = {}
        else:
            listing = parse_plugin_list(proc.stdout)

    check_plugin(listing, args.plugin, args.marketplace, report)
    check_skills(listing, tuple(s.strip() for s in args.skills.split(",") if s.strip()), home, report)
    check_config(home, args.plugin, args.marketplace, report)
    if not args.list_file:
        check_marketplace(args.marketplace, report)

    failures = [e for e in report.entries if e["status"] == "FAIL"]
    print(
        f"{len(failures)} problem(s) found, "
        f"{sum(1 for e in report.entries if e['status'] == 'warn')} warning(s), "
        f"{report.checks} check(s)."
    )
    if args.json:
        print(
            json.dumps(
                {
                    "checks": report.entries,
                    "failures": len(failures),
                    "codex_home": str(home),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())