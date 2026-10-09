#!/usr/bin/env python3
"""Real compiler race fixture in a disposable copy, never the frozen source."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import time
from unittest.mock import patch


Mode, BaseValue, Lean, Lake = sys.argv[1:]
Base = Path(BaseValue).resolve()
Scripts = Path(__file__).resolve().parents[1]
Replica = Base / "replica"
if(Replica.exists()):
	raise SystemExit("preserve existing race fixture")
for Component in ("lean-verify", "math-research-workflow"):
	shutil.copytree(Scripts.parents[1] / Component / "scripts", Replica / "plugins" / Component / "scripts", ignore=shutil.ignore_patterns("tests", "__pycache__", "*.pyc"))
sys.path.insert(0, str(Replica / "plugins/lean-verify/scripts"))
import lean_develop as develop
from lean_evidence import recheck_manifest
from lean_runtime import write_json


def project(Name):
	Root = Base / Name / "project"
	(Root / "Src").mkdir(parents=True)
	(Root / "lean-toolchain").write_text("leanprover/lean4:v4.31.0\n", encoding="utf-8")
	(Root / "Src/First.lean").write_text("theorem first (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
	(Root / "Src/Second.lean").write_text("theorem second (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
	Targets = Root / "targets.json"
	write_json(Targets, {"targets": [{"id": "first", "file": "Src/First.lean", "declaration": "first", "expected_type": "∀ n : Nat, n + 0 = n"}, {"id": "second", "file": "Src/Second.lean", "declaration": "second", "expected_type": "∀ n : Nat, n + 0 = n"}]})
	return Root, Root.parent / "output", Targets


def arguments(Root, Output, Action, Extra):
	return develop.make_parser().parse_args(["--project", str(Root), "--output", str(Output), "--lean", Lean, "--lake", Lake, "--direct", "--timeout", "90", Action, *Extra])


Results = []
if(Mode == "verify"):
	for ToolName in ("lake_build_guard.py", "run_manifest.schema.json"):
		Root, Output, Targets = project(ToolName.replace(".", "-"))
		Tool = Path(develop.__file__).parent / ToolName
		RawTool = Tool.read_bytes()
		Checks = []
		def actual_recheck_then_tool_edit(PathValue):
			Check = recheck_manifest(PathValue)
			Checks.append(Check)
			if(len(Checks) == 2):
				Tool.write_bytes(RawTool + b"\n")
			return Check
		try:
			with patch("lean_develop.recheck_manifest", side_effect=actual_recheck_then_tool_edit):
				Result = develop.verify_targets(arguments(Root, Output, "verify", ["--targets", str(Targets)]))
			assert len(Checks) == 2 and all(Check["exact_root_passed"] for Check in Checks), Checks
			assert not Result["exact_root_passed"] and "tool_hashes" in Result["batch"]["changed"], Result
			assert all(not Item["exact_root_passed"] for Item in Result["targets"]), Result
			Final = [recheck_manifest(Item["manifest"]) for Item in Result["targets"]]
			assert all(any("tool:" + ToolName == Reason for Reason in Item["reasons"]) for Item in Final), Final
			Results.append({"case": ToolName, "actual_checks_before_edit": Checks, "verification": Result, "actual_post_edit_checks": Final})
		finally:
			Tool.write_bytes(RawTool)
elif(Mode == "status"):
	Root, Output, Targets = project("status")
	Started = develop.start_verification(arguments(Root, Output, "start", ["--targets", str(Targets), "--job-id", "tool-status", "--job-timeout", "360"]))
	StatusArguments = arguments(Root, Output, "status", ["--job-id", "tool-status"])
	Deadline = time.monotonic() + 420
	while(time.monotonic() < Deadline):
		Baseline = develop.verification_status(StatusArguments)
		if(Baseline["state"] not in ("STARTING", "RUNNING")):
			break
		time.sleep(0.2)
	assert Baseline["state"] == "SUCCEEDED" and Baseline["exact_root_passed"], Baseline
	Rows = json.loads((Output / "development-result.json").read_bytes())["targets"]
	Results.append({"case": "actual successful durable job", "dispatch": Started, "status": Baseline})
	for ToolName in ("lake_build_guard.py", "run_manifest.schema.json"):
		Tool = Path(develop.__file__).parent / ToolName
		RawTool = Tool.read_bytes()
		Checks = []
		def actual_recheck_then_tool_edit(PathValue):
			Check = recheck_manifest(PathValue)
			Checks.append(Check)
			if(len(Checks) == 2):
				Tool.write_bytes(RawTool + b"\n")
			return Check
		try:
			with patch("lean_develop.recheck_manifest", side_effect=actual_recheck_then_tool_edit):
				Status = develop.verification_status(StatusArguments)
			assert len(Checks) == 2 and all(Check["exact_root_passed"] for Check in Checks), Checks
			assert not Status["exact_root_passed"] and not Status["verification"]["batch_current"], Status
			Final = [recheck_manifest(Item["manifest"]) for Item in Rows]
			assert all(any("tool:" + ToolName == Reason for Reason in Item["reasons"]) for Item in Final), Final
			Results.append({"case": "status late " + ToolName, "actual_checks_before_edit": Checks, "status": Status, "actual_post_edit_checks": Final})
		finally:
			Tool.write_bytes(RawTool)
	StdoutPath = Root / Baseline["stdout"]
	ReadBytes = Path.read_bytes
	for Changed in (Root / "Src/First.lean", Output / "development-result.json"):
		Raw = Changed.read_bytes()
		Events, Checks = [], []
		def actual_recheck_before_binding_edit(PathValue):
			Check = recheck_manifest(PathValue)
			Checks.append(Check)
			return Check
		def stdout_read_then_edit(PathValue):
			Result = ReadBytes(PathValue)
			if(PathValue == StdoutPath and len(Checks) == len(Rows) and not Events):
				Changed.write_bytes(b"theorem first : False := by sorry\n" if Changed.suffix == ".lean" else Raw + b"\n")
				Events.append({"edit_after_actual_stdout_read": str(Changed)})
			return Result
		try:
			with patch.object(Path, "read_bytes", stdout_read_then_edit), patch("lean_develop.recheck_manifest", side_effect=actual_recheck_before_binding_edit):
				Status = develop.verification_status(StatusArguments)
			assert Events and not Status["exact_root_passed"] and not Status["verification"]["batch_current"], Status
			assert all(Check["exact_root_passed"] for Check in Status["verification"]["checks"]), Status
			Results.append({"case": "late binding read " + str(Changed), "events": Events, "status": Status})
		finally:
			Changed.write_bytes(Raw)
else:
	raise ValueError("fixture mode must be verify or status")
write_json(Base / "REPORT.json", {"scope": "real compiler and durable job in disposable tool replica; original source never edited", "results": Results})
print(json.dumps({"mode": Mode, "cases": len(Results), "report": str(Base / "REPORT.json")}))
