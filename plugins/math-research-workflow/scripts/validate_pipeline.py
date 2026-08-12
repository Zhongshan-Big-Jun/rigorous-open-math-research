#!/usr/bin/env python3
"""Deterministic gate checks for a math-research pipeline project.

This script validates the mechanical parts of the manage -> research -> verify
handoff without making any mathematical judgment. It does not replace the
solver, audit, or verifier agents; it only rejects states that can be decided
from files and hashes.

Checks:
  - task packets in agenda/task-packets/*.md have the required fields and do
    not leak unfilled template placeholders;
  - source-bundle hashes, task-packet hashes in run manifests, and lean-proof
    input hashes match the files they reference;
  - run manifests under runs/** and lean-proof/run-manifest.json parse;
  - completed manager runs carry a non-empty upstream status, and statuses
    outside the formalization gate are reported;
  - optionally, the git working tree is clean at a stage boundary.

Usage:
  python validate_pipeline.py --project ROOT [--check-git] [--allow-dirty]
      [--gate-status STATUS,STATUS...]

Exit code 0 when all hard checks pass, 1 otherwise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


PACKET_GLOB = "agenda/task-packets/*.md"
MANAGER_MANIFEST_GLOB = "runs/**/run-manifest.json"
LEAN_MANIFEST = "lean-proof/run-manifest.json"

PLACEHOLDER_VALUES = {"TASK-ID", "PROJECT-ID", "PROBLEM-ID", "RUN_ROOT"}
ALLOWED_TASK_TYPES = {"solve", "disprove", "construct", "formalize", "rigorously audit"}
DEFAULT_GATE_STATUSES = {"\u5df2\u8bc1", "CANDIDATE_COMPLETE_PROOF"}

REQUIRED_PACKET_HEADINGS = {
    "Source bundle",
    "Required run location",
    "Upstream invocation",
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

    def ok(self, message: str) -> None:
        self.checks += 1
        print(f"ok: {message}")

    def bad(self, message: str) -> None:
        self.checks += 1
        self.errors.append(message)
        print(f"FAIL: {message}")

    def warn(self, message: str) -> None:
        self.checks += 1
        self.warnings.append(message)
        print(f"warn: {message}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_json(path: Path, report: Report) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.bad(f"missing JSON file: {path}")
    except json.JSONDecodeError as exc:
        report.bad(f"invalid JSON in {path}: {exc}")
    except OSError as exc:
        report.bad(f"cannot read {path}: {exc}")
    return None


def strip_inline_code(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        return value[1:-1].strip()
    return value


def parse_packet(path: Path) -> tuple[dict[str, str], set[str], str]:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    headings: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            headings.add(stripped[3:].strip())
            continue
        match = re.match(r"-\s+\*\*([^*]+)\*\*\s*(.*)$", stripped)
        if match:
            key = match.group(1).rstrip(":").strip()
            fields[key] = match.group(2).strip()
    return fields, headings, text


def parse_source_bundle(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_table = stripped[3:].strip() == "Source bundle"
            continue
        if in_table and stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            rows.append(cells)
    return rows


def check_task_packet(path: Path, root: Path, report: Report) -> None:
    fields, headings, text = parse_packet(path)
    rel = path.relative_to(root)

    for key in ("Task ID", "Project ID", "Task type", "Task state"):
        if key not in fields:
            report.bad(f"{rel}: missing required field {key!r}")
            continue
        value = strip_inline_code(fields[key])
        if not value:
            report.bad(f"{rel}: {key} is empty")

    task_id = strip_inline_code(fields.get("Task ID", ""))
    project_id = strip_inline_code(fields.get("Project ID", ""))
    if task_id in PLACEHOLDER_VALUES:
        report.bad(f"{rel}: Task ID still contains placeholder {task_id!r}")
    if project_id in PLACEHOLDER_VALUES:
        report.bad(f"{rel}: Project ID still contains placeholder {project_id!r}")
    if task_id and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{7,}", task_id):
        report.warn(f"{rel}: Task ID {task_id!r} does not look like an ID")

    task_type = fields.get("Task type", "")
    if "|" in task_type:
        report.bad(f"{rel}: Task type still contains the template choices")
    elif task_type not in ALLOWED_TASK_TYPES:
        report.bad(f"{rel}: unknown Task type {task_type!r}")

    for heading in REQUIRED_PACKET_HEADINGS:
        if heading not in headings:
            report.bad(f"{rel}: missing required section {heading!r}")

    run_location = fields.get("Required run location", "")
    if run_location and strip_inline_code(run_location) in PLACEHOLDER_VALUES:
        report.bad(f"{rel}: Required run location still contains {run_location!r}")

    for row in parse_source_bundle(text):
        if not row or row[0] in {"Item", ""}:
            continue
        if len(row) < 4:
            continue
        source = row[2]
        expected = row[3]
        if not expected or not source:
            continue
        if re.match(r"^(https?|doi|arxiv)://|^10\.", source, re.IGNORECASE):
            continue
        check_referenced_hash(root, source, expected, report, f"{rel}: source bundle")


def check_referenced_hash(
    root: Path, rel_path: str, expected: str, report: Report, context: str
) -> None:
    target = root / rel_path
    if not target.is_file():
        report.bad(f"{context}: referenced file missing: {rel_path}")
        return
    actual = sha256_file(target)
    if actual != expected.strip().upper():
        report.bad(f"{context}: hash mismatch for {rel_path}: {actual} != {expected.strip().upper()}")


def check_manager_manifest(
    path: Path, root: Path, report: Report, gate_statuses: set[str]
) -> None:
    data = load_json(path, report)
    if not isinstance(data, dict):
        if data is not None:
            report.bad(f"{path.relative_to(root)}: run manifest is not a JSON object")
        return

    packet_path = data.get("task_packet_path")
    packet_hash = data.get("task_packet_sha256")
    if packet_path and packet_hash:
        check_referenced_hash(
            root, packet_path, str(packet_hash), report, f"{path.relative_to(root)}: task packet"
        )

    if data.get("completed_at") and not data.get("upstream_status_verbatim"):
        report.bad(
            f"{path.relative_to(root)}: completed_at is set but upstream_status_verbatim is empty"
        )

    status = data.get("upstream_status_verbatim")
    if status and gate_statuses and status not in gate_statuses:
        report.warn(
            f"{path.relative_to(root)}: status {status!r} is outside the formalization gate "
            f"{sorted(gate_statuses)}"
        )


def check_lean_manifest(path: Path, root: Path, report: Report) -> None:
    data = load_json(path, report)
    if not isinstance(data, dict):
        if data is not None:
            report.bad(f"{path.relative_to(root)}: lean manifest is not a JSON object")
        return
    input_hashes = data.get("input_hashes")
    if isinstance(input_hashes, dict):
        for rel_path, expected in input_hashes.items():
            check_referenced_hash(
                root, rel_path, str(expected), report, f"{path.relative_to(root)}: input hash"
            )
    else:
        report.warn(f"{path.relative_to(root)}: no input_hashes map to verify")


def check_git(root: Path, report: Report, allow_dirty: bool) -> None:
    proc = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        capture_output=True,
        text=True,
        errors="replace",
    )
    if proc.returncode != 0:
        report.warn(f"cannot run git status: {proc.stderr.strip()}")
        return
    if proc.stdout.strip():
        message = "working tree is dirty: run git status --porcelain"
        if allow_dirty:
            report.warn(message)
        else:
            report.bad(message)
    else:
        report.ok("git working tree is clean")


def iter_packet_files(root: Path) -> Iterable[Path]:
    return sorted(root.glob(PACKET_GLOB))


def iter_manager_manifests(root: Path) -> Iterable[Path]:
    return sorted(root.glob(MANAGER_MANIFEST_GLOB))


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic pipeline gate checks")
    parser.add_argument("--project", required=True, help="math project root directory")
    parser.add_argument("--check-git", action="store_true", help="require a clean git tree")
    parser.add_argument("--allow-dirty", action="store_true", help="warn instead of fail on dirty tree")
    parser.add_argument(
        "--gate-status",
        default=",".join(sorted(DEFAULT_GATE_STATUSES)),
        help="comma-separated statuses allowed into formalization (stage C)",
    )
    args = parser.parse_args()

    root = Path(args.project).resolve()
    if not root.is_dir():
        print(f"FAIL: project directory not found: {root}")
        return 2

    gate_statuses = {s.strip() for s in args.gate_status.split(",") if s.strip()}
    report = Report()

    packets = list(iter_packet_files(root))
    report.ok(f"found {len(packets)} task packet(s)")
    for packet in packets:
        check_task_packet(packet, root, report)

    manifests = list(iter_manager_manifests(root))
    report.ok(f"found {len(manifests)} manager run manifest(s)")
    for manifest in manifests:
        check_manager_manifest(manifest, root, report, gate_statuses)

    lean_manifest = root / LEAN_MANIFEST
    if lean_manifest.is_file():
        check_lean_manifest(lean_manifest, root, report)
    else:
        report.warn(f"no lean manifest at {LEAN_MANIFEST}")

    if args.check_git:
        check_git(root, report, args.allow_dirty)

    problem_count = len(report.errors)
    print(
        f"{problem_count} problem(s) found, {len(report.warnings)} warning(s), "
        f"{report.checks} check(s)."
    )
    return 1 if problem_count else 0


if __name__ == "__main__":
    sys.exit(main())
