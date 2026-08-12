#!/usr/bin/env python3
"""Smoke test for the deterministic pipeline gate validator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "math-research-workflow" / "scripts" / "validate_pipeline.py"
GOOD = ROOT / "tests" / "fixtures" / "pipeline-good"
BAD = ROOT / "tests" / "fixtures" / "pipeline-bad"


def run(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--project", str(target)],
        capture_output=True,
        text=True,
    )


def main() -> int:
    good = run(GOOD)
    if good.returncode != 0:
        print(good.stdout)
        print(good.stderr)
        return 1

    bad = run(BAD)
    if bad.returncode == 0:
        print("bad fixture unexpectedly passed the gate")
        return 1

    print("pipeline gate smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
