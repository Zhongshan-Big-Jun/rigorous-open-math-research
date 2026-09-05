#!/usr/bin/env python3
"""No-model maintenance replay on isolated copies of real tool cards and checkpoints."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/manage-math-research-program/skills/manage-math-research-program/scripts"))
sys.path.insert(0, str(ROOT / "plugins/math-research-workflow/scripts"))
import research_library as library
import recovery_status as recovery


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	for name in ("project", "checkpoint-project", "run-root", "output"):
		Parser.add_argument("--" + name, required=True)
	Args = Parser.parse_args()
	Project = Path(Args.project).resolve()
	CheckpointProject = Path(Args.checkpoint_project).resolve()
	Output = Path(Args.output).resolve()
	if(Output.is_relative_to(Project) or Output.is_relative_to(CheckpointProject)):
		raise ValueError("replay output must be outside the original research roots")
	Output.mkdir(parents=True, exist_ok=False)
	OriginalHashes = dict()
	Timings = []
	def copy_artifact(Source, Target):
		if(Source.suffix not in (".json", ".md", ".lean")):
			raise ValueError(f"refusing to copy a project executable or undeclared artifact: {Source}")
		Data = Source.read_bytes()
		OriginalHashes[Source] = hashlib.sha256(Data).hexdigest()
		Target.parent.mkdir(parents=True, exist_ok=True)
		Target.write_bytes(Data)
	def timed(name, Operation):
		Start = time.perf_counter()
		Result = Operation()
		Timings.append(dict(operation=name, seconds=time.perf_counter() - Start))
		return Result
	LibraryProject = Output / "library-project"
	for path in sorted((Project / "tools").rglob("*.md")):
		copy_artifact(path, LibraryProject / path.relative_to(Project))
	for name in ("index/tools.json", "blueprint-project.json"):
		copy_artifact(Project / name, LibraryProject / name)
	Legacy = library.read_json(LibraryProject / "index/tools.json")
	IndexResult = timed("index_real_cards", lambda: library.make_index(LibraryProject, ["tools"], ReadmePath="tools/README.md"))
	Current = library.read_json(LibraryProject / "index/tools.json")
	ByPath = {Row["location"]: Row for Row in Current["items"]}
	for Old in Legacy["items"]:
		for Key, Value in Old.items():
			if(Key not in ("title", "summary", "aliases", "kind", "applicability", "lifecycle")):
				assert ByPath[Old["location"]][Key] == Value, (Old["location"], Key)
	Card = next(Row for Row in Current["items"] if Row["pointer_state"] == "CURRENT"
		and Row["lifecycle"] != "archived" and Row["metadata_status"] != "UNPARSEABLE")
	Note = library.annotate(LibraryProject, Card["location"], Card["sha256"], "maintenance-replay",
		"retrieval_hint", "isolated transport fixture", "replay-sentinel-20260905; no mathematical claim")
	Query = timed("query_real_cards_with_annotation", lambda: library.query_tools(LibraryProject, "replay-sentinel-20260905"))
	assert len(Query["hits"]) == 1
	assert Query["hits"][0]["sha256"] == Card["sha256"]
	CardPath = LibraryProject / Card["location"]
	CardPath.write_bytes(CardPath.read_bytes() + b"\n<!-- isolated replay edit -->\n")
	assert library.query_tools(LibraryProject, "replay-sentinel-20260905")["verdict"] == "STALE_INDEX"
	library.make_index(LibraryProject, ["tools"], ReadmePath="tools/README.md")
	assert not library.query_tools(LibraryProject, "replay-sentinel-20260905")["hits"]
	RunRoot = Path(Args.run_root)
	Run = library.inside(CheckpointProject, RunRoot)
	Paths = set()
	for path in Run.glob("interruption_checkpoint-*.json"):
		Checkpoint = library.read_json(path)
		Paths.add(path.relative_to(CheckpointProject))
		Paths.add(Path(Checkpoint["state"]["path"]))
		Paths.update(Path(Binding["path"]) for Binding in Checkpoint["bound_artifacts"])
	Paths.update(path.relative_to(CheckpointProject) for path in Run.glob("resume_receipt-*.json"))
	Paths.update(path.relative_to(CheckpointProject) for path in Run.glob("interruption_state-*.json"))
	RecoveryProject = Output / "recovery-project"
	for path in sorted(Paths):
		Source = library.inside(CheckpointProject, path)
		copy_artifact(Source, library.inside(RecoveryProject, path))
	Before = timed("inspect_real_latest_checkpoint", lambda: recovery.inspect_run(RecoveryProject, RunRoot))
	Prepared = timed("prepare_real_resume", lambda: recovery.prepare_resume(RecoveryProject, RunRoot))
	Receipt = RecoveryProject / Prepared["receipt"]
	ReceiptBytes = Receipt.read_bytes()
	Again = timed("retry_real_resume", lambda: recovery.prepare_resume(RecoveryProject, RunRoot))
	assert Again["verdict"] == "RESUME_RECEIPT_REUSED"
	assert Receipt.read_bytes() == ReceiptBytes
	assert not Prepared["dispatch_performed"] and not Again["dispatch_performed"]
	assert Before["result_status"] == Again["result_status"]
	assert Before["do_not_repeat_action_ids"] == Again["do_not_repeat_action_ids"]
	CheckpointPath = RecoveryProject / Before["checkpoint"]
	CheckpointPath.write_bytes(b"{}\n")
	try:
		recovery.inspect_run(RecoveryProject, RunRoot)
	except recovery.engine.CheckpointError:
		StaleBlocked = True
	else:
		raise AssertionError("tampered latest checkpoint was accepted")
	assert all(hashlib.sha256(path.read_bytes()).hexdigest() == Hash for path, Hash in OriginalHashes.items())
	Summary = dict(verdict="PASS", kind="L0_NO_MODEL_REAL_ARTIFACT_REPLAY", timings=Timings,
		runtime_sha256={Path(Module.__file__).name: library.digest(Path(Module.__file__).read_bytes())
			for Module in (library, recovery, recovery.engine)},
		replay_script_sha256=library.digest(Path(__file__).read_bytes()),
		library=IndexResult, annotation_id=Note["annotation_id"], legacy_rows_preserved=len(Legacy["items"]),
		checkpoint_id=Before["checkpoint_id"], checkpoint_sequence=Before["sequence"],
		copied_recovery_files=len(Paths), result_status=Before["result_status"],
		receipt_reused=True, stale_latest_blocked=StaleBlocked,
		do_not_repeat_ids_preserved=len(Before["do_not_repeat_action_ids"]),
		original_files_unchanged=len(OriginalHashes), dispatched_workers=0, model_calls=0,
		new_mathematical_claims=0, scoring="Local operation times only; no solver speedup inference.")
	library.atomic_write(Output / "results.json", library.json_bytes(Summary))
	print(json.dumps(Summary, ensure_ascii=False))


if(__name__ == "__main__"):
	main()
