#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RIGOROUS = ROOT / "plugins" / "rigorous-open-math-research"
WORKFLOW = ROOT / "plugins" / "math-research-workflow"


def require(path: Path, markers: tuple[str, ...]) -> None:
	text = path.read_text(encoding="utf-8")
	missing = [marker for marker in markers if marker not in text]
	if missing:
		raise AssertionError(f"{path.relative_to(ROOT)} missing markers: {missing}")


def main() -> None:
	rigorous_skill = RIGOROUS / "skills" / "rigorous-open-math-research"
	workflow_skill = WORKFLOW / "skills" / "math-research-workflow"
	require(
		rigorous_skill / "references" / "closure-first-protocol.md",
		("OPEN_EXACT_GAP", "decision_delta", "Difficulty alone is not a spawn"),
	)
	require(
		rigorous_skill / "assets" / "closure-gate.template.md",
		("First open load-bearing claim", "Coordinator direct attempt", "Gate decision"),
	)
	require(
		rigorous_skill / "SKILL.md",
		("references/closure-first-protocol.md", "closure_gate.md"),
	)
	require(
		rigorous_skill / "assets" / "subtask-packet.template.md",
		("Decision to change", "decision_delta"),
	)
	require(
		workflow_skill / "SKILL.md",
		("Closure-first gate", "no-`decision_delta` returns"),
	)
	for plugin in (RIGOROUS, WORKFLOW):
		manifest = json.loads((plugin / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
		if manifest["version"] != "1.7.0":
			raise AssertionError(f"{manifest['name']} version is not 1.7.0")
	print("closure-first smoke passed")


if __name__ == "__main__":
	main()
