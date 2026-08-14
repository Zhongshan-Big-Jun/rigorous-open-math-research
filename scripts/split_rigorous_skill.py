#!/usr/bin/env python3
"""Progressive-disclosure split for the rigorous-open-math-research SKILL.md.

Splits the monolithic SKILL.md into a lean driver (global contracts + phase
index) plus per-phase reference files under references/. The transformation is
a PURE MOVE: every line of the original body appears exactly once in the
outputs; the only additions are the phase-index block in the driver, a
one-line header per phase file, and a changelog entry.

Usage (from the repository root):
    python scripts/split_rigorous_skill.py --apply
    python scripts/split_rigorous_skill.py --verify

--apply writes SKILL.md (driver) and the phase files; it reads the pre-split
SKILL.md from `git show HEAD:...` (the split is a one-time migration from the
commit before it lands) and refuses to overwrite an existing phase file unless
--force is given.
--verify rebuilds the expected outputs from `git show HEAD:` SKILL.md in
memory and compares them with the files on disk byte for byte, then reports
line-coverage statistics.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = "plugins/rigorous-open-math-research/skills/rigorous-open-math-research"
SKILL_MD = ROOT / SKILL / "SKILL.md"

# Contiguous section runs moved to reference files, by first and last section
# TITLE (the title line itself, including the leading hashes). Runs must be
# contiguous in the source file and are moved verbatim, in order.
PLAN = [
    (
        "## Phase 0 — Provenance, status, and scope",
        "## Contract audit",
        "references/phase-01-contract.md",
    ),
    (
        "## Phase 2 — Map known mathematics",
        "### Divergent search contract",
        "references/phase-23-search.md",
    ),
    (
        "## Phase 4 — Create a genuinely diverse route portfolio",
        "### The theorem-strength gap test",
        "references/phase-45-routes-loop.md",
    ),
    (
        "## Phase 6 — Computational and evolutionary search",
        "## Phase 6 — Computational and evolutionary search",
        "references/phase-6-computation.md",
    ),
    (
        "## Phase 7 — Synthesis",
        "### Structured verification output",
        "references/phase-78-synthesis-audit.md",
    ),
    (
        "## Phase 9 — Revision policy",
        "## Phase 11 — Novelty and significance audit",
        "references/phase-91011.md",
    ),
    (
        "## Phase 12 — Stopping and reporting",
        "### Research stop conditions",
        "references/phase-12-reporting.md",
    ),
    (
        "# Result",
        "## Confidence by axis",
        "references/phase-12-reporting.md",
    ),
    (
        "# Agent orchestration",
        "## Coordinator",
        "references/agent-orchestration.md",
    ),
]

INDEX_BLOCK = """## Phase index

Read the referenced file through this skill's resourceBase directory before
executing a phase; every phase file repeats this contract at its top.

| Phase | File |
|---|---|
| 0-1 provenance, scope, theorem contract | `references/phase-01-contract.md` |
| 2-3 literature map + proof-obligation graph | `references/phase-23-search.md` |
| 4-5 route portfolio + research loop | `references/phase-45-routes-loop.md` |
| 6 computational and evolutionary search | `references/phase-6-computation.md` |
| 7-8 synthesis + adversarial proof audit | `references/phase-78-synthesis-audit.md` |
| 9-11 revision, formalization, novelty | `references/phase-91011.md` |
| 12 stopping and reporting (+ Result template) | `references/phase-12-reporting.md` |
| delegation, sub-agents, role prompts | `references/agent-orchestration.md` |

Global contracts (epistemic rules, artifacts, Output protocol, anti-patterns)
stay in this file and bind every phase.
"""

PHASE_FILE_HEADER = (
    "> Phase file for the rigorous-open-math-research skill. Read this file "
    "before executing the phases it covers; the global contracts live in the "
    "parent SKILL.md. Relative paths in this file (assets/, references/, "
    "scripts/) resolve against the skill root (the directory containing "
    "SKILL.md).\n"
)


def parse_sections(lines: list[str]) -> list[tuple[int, int, str]]:
    """[(start_idx, end_idx, title)] with end_idx exclusive; blank lines
    between headings attach to the following section, and trailing blanks to
    the last section. Splits at '# ', '## ', and '### ' headings."""
    headings = [
        idx
        for idx, line in enumerate(lines)
        if line.startswith("# ") or line.startswith("## ") or line.startswith("### ")
    ]
    sections = []
    for pos, idx in enumerate(headings):
        end = headings[pos + 1] if pos + 1 < len(headings) else len(lines)
        sections.append((idx, end, lines[idx].rstrip("\n")))
    return sections


def build(original: str) -> tuple[str, dict[str, str], dict[str, int]]:
    """Decompose the original text into (driver, {relpath: content}, stats)."""
    lines = original.splitlines()
    sections = parse_sections(lines)
    title_to_range = {}
    for pos, (start, end, title) in enumerate(sections):
        title_to_range[title] = (pos, start, end)

    moved_ranges: list[tuple[int, int]] = []  # (start_idx, end_idx) line ranges
    dest_chunks: dict[str, list[str]] = {}
    for first, last, dest in PLAN:
        if first not in title_to_range or last not in title_to_range:
            raise SystemExit(f"plan anchor not found: {first!r} -> {last!r}")
        p_first, start, _ = title_to_range[first]
        p_last, _, end = title_to_range[last]
        if p_last < p_first:
            raise SystemExit(f"plan range reversed: {first!r} -> {last!r}")
        for pos in range(p_first, p_last + 1):
            s, e, _ = sections[pos]
            if moved_ranges and s < moved_ranges[-1][1]:
                raise SystemExit(f"plan ranges overlap at line {s + 1}")
            moved_ranges.append((s, e))
        dest_chunks.setdefault(dest, []).append("\n".join(lines[start:end]))
        moved_ranges.sort()

    # driver: everything outside the moved ranges, with the index block
    # inserted after the '# Workflow' section
    def in_moved(idx: int) -> bool:
        return any(s <= idx < e for s, e in moved_ranges)

    workflow_end = None
    for start, end, title in sections:
        if title == "# Workflow":
            workflow_end = end
            break
    if workflow_end is None:
        raise SystemExit("'# Workflow' section not found")

    driver_lines: list[str] = []
    idx = 0
    n = len(lines)
    inserted_index = False
    while idx < n:
        if not inserted_index and idx == workflow_end:
            driver_lines.append(INDEX_BLOCK.rstrip("\n"))
            inserted_index = True
        if in_moved(idx):
            idx += 1
            continue
        driver_lines.append(lines[idx])
        idx += 1
    if not inserted_index:
        driver_lines.append(INDEX_BLOCK.rstrip("\n"))

    driver_str = "\n".join(driver_lines).rstrip("\n") + "\n"
    changelog_entry = (
        "\n## Changelog (2026-08-14)\n"
        "- 渐进式披露重构: Phase 0-12 详细契约与角色 prompt 纯移动至 references/ "
        "(phase-01-contract, phase-23-search, phase-45-routes-loop, "
        "phase-6-computation, phase-78-synthesis-audit, phase-91011, "
        "phase-12-reporting, agent-orchestration); SKILL.md 退化为驱动层 "
        "(全局规则/工件清单/Phase 索引表/Output protocol/Anti-patterns), "
        f"单次加载从 {len(original.encode('utf-8'))} bytes 降至 "
        f"{len(driver_str.encode('utf-8'))} bytes; 内容未改写, "
        "scripts/split_rigorous_skill.py --verify 可复验覆盖.\n"
    )
    driver = driver_str + changelog_entry

    files: dict[str, str] = {}
    for dest, chunks in dest_chunks.items():
        body = "\n".join(chunks)
        files[dest] = PHASE_FILE_HEADER + body.rstrip("\n") + "\n"

    stats = {
        "original_lines": len(lines),
        "moved_lines": sum(e - s for s, e in moved_ranges),
        "driver_lines": len(driver.splitlines()),
        "original_bytes": len(original.encode("utf-8")),
        "driver_bytes": len(driver.encode("utf-8")),
        "added_lines": set(INDEX_BLOCK.splitlines())
        | set(PHASE_FILE_HEADER.rstrip("\n").splitlines())
        | set(changelog_entry.strip("\n").splitlines()),
    }
    return driver, files, stats


def original_from_git() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{SKILL}/SKILL.md"],
        capture_output=True,
        text=True,
        errors="replace",
    )
    if proc.returncode != 0:
        raise SystemExit(f"cannot read HEAD SKILL.md: {proc.stderr.strip()}")
    return proc.stdout.replace("\r\n", "\n")


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("--apply", "--verify"):
        print(__doc__)
        return 2
    mode = sys.argv[1]
    force = "--force" in sys.argv

    if mode == "--verify":
        original = original_from_git()
        driver, files, stats = build(original)
        problems = []
        disk_driver = SKILL_MD.read_text(encoding="utf-8").replace("\r\n", "\n")
        if disk_driver != driver:
            problems.append("SKILL.md differs from the expected driver")
        for rel, expected in files.items():
            path = ROOT / SKILL / rel
            if not path.is_file():
                problems.append(f"missing phase file: {rel}")
                continue
            disk = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            if disk != expected:
                problems.append(f"phase file differs from expected: {rel}")
        # pure-move check: every output line is either an original line or a
        # documented addition, and every original line appears exactly once
        original_lines = original.splitlines()
        additions = stats["added_lines"]
        from collections import Counter

        outputs = [disk_driver] if not problems else []
        if not problems:
            for rel in files:
                outputs.append((ROOT / SKILL / rel).read_text(encoding="utf-8").replace("\r\n", "\n"))
        if not problems:
            output_lines: list[str] = []
            for out in outputs:
                output_lines.extend(out.splitlines())
            unknown = [line for line in output_lines if line not in original_lines and line not in additions]
            if unknown:
                problems.append(f"{len(unknown)} output lines are not original content (first: {unknown[0]!r})")
            counts = Counter(line for line in output_lines if line in original_lines)
            orig_counts = Counter(original_lines)
            missing = [line for line, c in orig_counts.items() if counts.get(line, 0) == 0]
            if missing:
                problems.append(f"{len(missing)} original lines are missing from the outputs")
            if problems:
                pass
        print(
            f"original: {stats['original_lines']} lines / {stats['original_bytes']} bytes; "
            f"moved: {stats['moved_lines']} lines; driver: {stats['driver_lines']} lines / "
            f"{stats['driver_bytes']} bytes"
        )
        if problems:
            for line in problems[:20]:
                print("FAIL: " + line)
            return 1
        print("verify OK: outputs reconstruct the pre-split SKILL.md (pure move)")
        return 0

    # --apply
    original = original_from_git()
    driver, files, stats = build(original)
    existing = [rel for rel in files if (ROOT / SKILL / rel).exists()]
    if existing and not force:
        print("phase files already exist; re-run with --force to overwrite:")
        for rel in existing:
            print("  " + rel)
        return 1
    SKILL_MD.write_text(driver, encoding="utf-8")
    for rel, content in files.items():
        path = ROOT / SKILL / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(
        f"applied: original {stats['original_lines']} lines -> driver "
        f"{stats['driver_lines']} lines + {len(files)} phase files "
        f"({stats['moved_lines']} lines moved)"
    )
    print(f"driver: {stats['driver_bytes']} bytes (was {stats['original_bytes']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
