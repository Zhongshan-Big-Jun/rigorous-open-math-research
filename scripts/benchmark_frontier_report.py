#!/usr/bin/env python3
"""Export frozen frontier benchmark evidence and compare actual outcomes."""

import argparse
from pathlib import Path
import shutil

import benchmark_codex as B
import benchmark_runner as R
import benchmark_usage as U


def copy_immutable(source, target):
	if(target.exists()):
		if(R.file_hash(source) != R.file_hash(target)):
			raise RuntimeError(f"refusing to overwrite different evidence: {target}")
		return
	target.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(source, target)


def frozen_checks(base):
	State = R.read_json(base / "run/state.json")
	if(State["status"] not in ["RETURNED_UNAUDITED", "BUDGET_EXHAUSTED", "RETURNED_UNREVIEWED"]):
		raise RuntimeError("stage must be frozen before export")
	Identity = R.process_identity(State.get("process_pid", 0))
	SameBoot = State.get("boot_id") == Path("/proc/sys/kernel/random/boot_id").read_text().strip()
	if(SameBoot and Identity and Identity[1] == State.get("process_start_ticks")):
		raise RuntimeError("owned stage process is still alive")
	Frozen = base / "run/frozen-work"
	Hashes = R.read_json(base / "run/frozen-hashes.json")
	for Name, Digest in Hashes.items():
		File = Frozen / Name
		if(not File.resolve().is_relative_to(Frozen.resolve()) and Name != "../last-message.txt"):
			raise RuntimeError("unexpected external frozen artifact")
		if(File.is_symlink() or R.file_hash(File) != Digest):
			raise RuntimeError("frozen artifact changed")
	return dict(verdict="PASS", files_verified=len(Hashes), owned_process_exited=True)


def export_stage(campaign, task, arm, phase, output):
	Manifest = R.read_json(campaign / "control/manifest.json")
	Mapping = None
	if(phase == "solver"):
		R.assert_sealed(campaign, task, arm)
		Base, Home, Work = B.arm_paths(campaign, task, arm)
	else:
		Mapping = R.read_json(campaign / f"control/audit-{task}-{arm}.json")
		Base, Home, Work = B.arm_paths(Path(Mapping["root"]), "candidate", "C")
	Checks = frozen_checks(Base)
	Frozen = Base / "run/frozen-work"
	if(R.file_hash(Frozen / "TASK.md") != Manifest["tasks"][task]["sha256"]):
		raise RuntimeError("wrong frozen task")
	if(Mapping and R.file_hash(Frozen / "CANDIDATE.md") != Mapping["candidate_sha256"]):
		raise RuntimeError("wrong blind candidate")
	Summary = U.measure(Base)
	if(Summary["models"] != [Manifest["model"]] or Summary["efforts"] != [Manifest["effort"]]):
		raise RuntimeError("observed identity is unknown or mismatched")
	if(any(Item["forbidden_skill_metadata"] for Item in R.session_inventory(Home))):
		raise RuntimeError("observed forbidden skill metadata; stage is not scoreable")
	Stage = output / "evidence" / f"{task}-{arm}-{phase}"
	Stage.mkdir(parents=True, exist_ok=True)
	for Name in ["state.json", "sessions.json", "frozen-hashes.json", "usage-summary.json", "usage-records.json", "last-message.txt"]:
		if((Base / "run" / Name).is_file()):
			copy_immutable(Base / "run" / Name, Stage / Name)
	for File in sorted(Frozen.rglob("*")):
		Relative = File.relative_to(Frozen)
		if(File.is_file() and not set(Relative.parts).intersection({"tmp", ".git", "__pycache__"}) and Relative.name != "PROMPT.md"):
			copy_immutable(File, Stage / "artifacts" / Relative)
	if(Mapping):
		copy_immutable(campaign / f"control/audit-{task}-{arm}.json", Stage / "input-binding.json")
	R.persist(Stage / "checks.json", dict(Checks, recorded_at=R.utc_now(), task_sha256=R.file_hash(Frozen / "TASK.md")))
	return dict(phase=phase, arm=arm, checks=Checks, usage=Summary)


def check_audit(data):
	Limits = dict(correctness=40, fidelity=20, strict_progress=15, calibration=10, evidence=10, reproducibility=5)
	if(set(data["scores"]) != set(Limits)):
		raise RuntimeError("unexpected score axes")
	for Key, Limit in Limits.items():
		Value = data["scores"][Key]
		if(type(Value) not in [int, float] or not 0 <= Value <= Limit):
			raise RuntimeError("score outside registered range")
	if(sum(data["scores"].values()) != data["total_score"]):
		raise RuntimeError("audit score does not sum")
	if(type(data["root_closed"]) is not bool):
		raise RuntimeError("missing explicit root closure")
	if(data["verdict"] == "PASS" and (not data["root_closed"] or data["load_bearing_gaps"] or data["target_status"] not in ["PROVED", "REFUTED"])):
		raise RuntimeError("PASS contradicts proof closure")


def compare(campaign, task, output):
	Manifest = R.read_json(campaign / "control/manifest.json")
	Arms, SeenResponses, Stages = {}, set(), []
	for Arm in Manifest["schedule"][task]:
		Collected = {}
		for Phase in ["solver", "audit"]:
			Result = export_stage(campaign, task, Arm, Phase, output)
			Collected[Phase] = Result["usage"]
			Stage = output / "evidence" / f"{task}-{Arm}-{Phase}"
			Records = R.read_json(Stage / "usage-records.json")["records"]
			if(SeenResponses.intersection(Records)):
				raise RuntimeError("a returned response appears in multiple stages")
			SeenResponses.update(Records)
			Stages.append(dict(arm=Arm, phase=Phase, checks=Result["checks"]))
		Verdict = R.read_json(output / "evidence" / f"{task}-{Arm}-audit/artifacts/audit.json")
		check_audit(Verdict)
		Full = {}
		for Key in ["uncached_input_tokens", "cached_input_tokens", "output_tokens", "responses_with_usage"]:
			Values = [Collected[Phase]["returned_usage"][Key] for Phase in ["solver", "audit"]]
			Full[Key] = sum(Values) if None not in Values else None
		Full["active_seconds"] = sum(Item["root_active_wall_seconds"] for Item in Collected.values())
		Arms[Arm] = dict(solver=Collected["solver"], external_audit=Collected["audit"], full_delivery=Full,
			verdict=Verdict["verdict"], target_status=Verdict["target_status"], root_closed=Verdict["root_closed"],
			score=Verdict["total_score"], scores=Verdict["scores"], proved_new_claims=Verdict["proved_new_claims"],
			load_bearing_gaps=Verdict["load_bearing_gaps"], first_proof_seconds=None)
	Comparisons = {}
	for Left, Right in [("B", "A"), ("B", "C"), ("A", "C")]:
		Ratios = {}
		for Scope in ["solver", "full_delivery"]:
			for Metric in ["uncached_input_tokens", "active_seconds"]:
				def metric_value(arm):
					Item = Arms[arm][Scope]
					if(Scope == "full_delivery"):
						return Item[Metric]
					return Item["root_active_wall_seconds"] if Metric == "active_seconds" else Item["returned_usage"][Metric]
				Numerator, Denominator = metric_value(Left), metric_value(Right)
				Ratios[f"{Scope}_{Metric}_ratio"] = Numerator / Denominator if Numerator is not None and Denominator else None
		Comparisons[f"{Left}/{Right}"] = Ratios
	Report = dict(schema_version=1, task=task, classification=Manifest["kind"], recorded_at=R.utc_now(),
		arms=Arms, comparisons=Comparisons, completed=True,
		limitations=["One repository task and one attempt per arm; descriptive only.",
			"Same-model audits are fallible; no formal verification or literature novelty claim.",
			"Costs include actual interruptions; unknown in-flight usage is not zero."])
	R.persist(output / "comparison.json", Report)
	R.persist(output / "evidence/campaign-completion-checks.json", dict(recorded_at=R.utc_now(),
		verdict="PASS", stages=Stages, unique_returned_responses=len(SeenResponses)))
	return Report


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("action", choices=["export", "compare"])
	Parser.add_argument("--campaign", required=True, type=Path)
	Parser.add_argument("--task", required=True)
	Parser.add_argument("--output", required=True, type=Path)
	Parser.add_argument("--arm", choices=["A", "B", "C"])
	Parser.add_argument("--phase", choices=["solver", "audit"])
	Args = Parser.parse_args()
	if(Args.action == "compare"):
		Result = compare(Args.campaign, Args.task, Args.output)
		print(R.json.dumps(dict(completed=Result["completed"], arms={Arm: dict(verdict=Data["verdict"], target_status=Data["target_status"], score=Data["score"], full_delivery=Data["full_delivery"]) for Arm, Data in Result["arms"].items()})))
	else:
		if(not Args.arm or not Args.phase):
			Parser.error("export requires --arm and --phase")
		print(R.json.dumps(export_stage(Args.campaign, Args.task, Args.arm, Args.phase, Args.output)))


if(__name__ == "__main__"):
	main()
