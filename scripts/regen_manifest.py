#!/usr/bin/env python3
"""Regenerate MANIFEST.sha256 for a skill bundle (deterministic, LF-normalized).

Usage:
    py -3 scripts/regen_manifest.py plugins/manage-math-research-program/skills/manage-math-research-program
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys


def is_transient(path: pathlib.Path) -> bool:
    return "__pycache__" in path.parts or path.suffix == ".pyc"


def sha256_norm(path: pathlib.Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", help="path to the skill bundle directory containing MANIFEST.sha256")
    args = parser.parse_args()

    bundle = pathlib.Path(args.bundle).resolve()
    files = [
        p
        for p in bundle.rglob("*")
        if p.is_file() and p.name != "MANIFEST.sha256" and not is_transient(p)
    ]
    entries = []
    for p in sorted(files, key=lambda path: path.relative_to(bundle).as_posix()):
        rel = "./" + p.relative_to(bundle).as_posix()
        entries.append(f"{sha256_norm(p)}  {rel}")
    manifest = bundle / "MANIFEST.sha256"
    manifest.write_text("\n".join(entries) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: regenerated {manifest} ({len(entries)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
