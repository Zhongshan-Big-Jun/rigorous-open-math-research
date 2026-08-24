#!/usr/bin/env python3
"""Smoke test for the workflow environment doctor (no live codex needed)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "math-research-workflow" / "scripts" / "doctor.py"

FULL_LIST = """name@marketplace          status              version                    path
math-research-workflow@math-research   installed, enabled  0.1.0+codex.20260813054312  C:\\tmp\\marketplaces\\math-research\\plugins\\math-research-workflow
manage-math-research-program@math-research   installed, enabled  0.1.0+codex.20260813054312  C:\\tmp\\marketplaces\\math-research\\plugins\\manage-math-research-program
rigorous-open-math-research@math-research   installed, enabled  0.1.0+codex.20260813054312  C:\\tmp\\marketplaces\\math-research\\plugins\\rigorous-open-math-research
lean-verify@personal   installed, enabled  0.1.0+codex.20260811140558  C:\\Users\\test\\plugins\\lean-verify
"""

MISSING_WORKFLOW_LIST = FULL_LIST.replace(
    "math-research-workflow@math-research   installed, enabled  0.1.0+codex.20260813054312  C:\\tmp\\marketplaces\\math-research\\plugins\\math-research-workflow\n",
    "",
)


def run(list_text: str, *extra: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        list_file = Path(tmp) / "plugin-list.txt"
        list_file.write_text(list_text, encoding="utf-8")
        env = os.environ.copy()
        env["CODEX_HOME"] = str(Path(tmp) / "codex-home")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--list-file", str(list_file), *extra],
            capture_output=True,
            text=True,
            env=env,
        )


def extract_json(stdout: str) -> dict:
    start = stdout.index("{")
    return json.loads(stdout[start:])


def main() -> int:
    ok = run(FULL_LIST)
    if ok.returncode != 0:
        print(ok.stdout)
        print(ok.stderr)
        return 1
    # config.toml may be absent (e.g. CI runner home): doctor then warns and
    # skips the enable-entry check, so only the plugin/skill health and the
    # absence of FAILs are hard requirements here.
    if "installed and enabled" not in ok.stdout or "0 problem(s)" not in ok.stdout:
        print("doctor did not report healthy state for the full listing")
        print(ok.stdout)
        return 1

    missing = run(MISSING_WORKFLOW_LIST, "--json")
    if missing.returncode == 0:
        print("doctor unexpectedly passed without the workflow plugin")
        print(missing.stdout)
        return 1
    payload = extract_json(missing.stdout)
    repairs = [c.get("repair", "") for c in payload["checks"]]
    if not any("codex plugin add math-research-workflow@math-research" in r for r in repairs):
        print("doctor did not suggest the repair command")
        print(missing.stdout)
        return 1

    print("doctor smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
