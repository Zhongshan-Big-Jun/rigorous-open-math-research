#!/usr/bin/env python3
"""Inspect current verifier bookkeeping with simulated process results, without Lean."""

from contextlib import ExitStack, redirect_stdout
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch


def inspect_target(Module, Root, Case, TargetExists, ExitCode):
	Project = Root / Case
	Project.mkdir()
	Target = Project / "Target.lean"
	if(TargetExists):
		Target.write_text("theorem specimen : True := by trivial\n", encoding="utf-8")

	Calls = []

	def simulate_run(Command, Cwd, timeout=3600):
		Calls.append(Command)
		if("--version" in Command):
			return {"command": Command, "exit_code": 0, "stdout": "SIMULATED", "stderr": ""}
		return {
			"command": Command,
			"exit_code": ExitCode,
			"stdout": "",
			"stderr": "SIMULATED timeout" if ExitCode is None else "",
		}

	Arguments = ["verify_lean_project.py", "--project", str(Project), "--build", "--build-targets", "Target.lean"]
	with ExitStack() as Stack:
		Stack.enter_context(patch.object(sys, "argv", Arguments))
		Stack.enter_context(patch.object(Module.shutil, "which", side_effect=lambda Name: "/SIMULATED/" + Name))
		Stack.enter_context(patch.object(Module, "run", side_effect=simulate_run))
		Stack.enter_context(patch.object(Module.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout="", stderr="")))
		Stack.enter_context(redirect_stdout(io.StringIO()))
		ExitStatus = Module.main()

	Manifest = json.loads((Project / "run-manifest.json").read_text(encoding="utf-8"))
	return {
		"case": Case,
		"target_exists": TargetExists,
		"simulated_target_exit": ExitCode,
		"target_command_attempted": any("env" in Command for Command in Calls),
		"verifier_process_exit": ExitStatus,
		"aggregate_build_exit": Manifest["build"]["exit_code"],
		"machine_verification_passed": Manifest["machine_verification_passed"],
		"target_results": [{"exit_code": Result["exit_code"], "stderr": Result["stderr"]} for Result in Manifest["build"]["commands"]],
	}


def main():
	Repo = Path(__file__).resolve().parents[2]
	Script = Repo / "plugins/lean-verify/scripts/verify_lean_project.py"
	Spec = importlib.util.spec_from_file_location("inspected_verifier", Script)
	Module = importlib.util.module_from_spec(Spec)
	Spec.loader.exec_module(Module)
	with TemporaryDirectory(prefix="lean-verifier-research-") as Directory:
		Root = Path(Directory)
		Cases = [
			inspect_target(Module, Root, "missing_target", False, None),
			inspect_target(Module, Root, "timeout_target", True, None),
			inspect_target(Module, Root, "failed_target_control", True, 1),
			inspect_target(Module, Root, "successful_target_control", True, 0),
		]
		CommentFile = Root / "Comment.lean"
		CommentFile.write_text("/- A comment containing sorry. -/\ntheorem specimen : True := by trivial\n", encoding="utf-8")
		CommentHits = [{"line": Hit["line"], "kind": Hit["kind"]} for Hit in Module.scan_file(CommentFile, set())]
	Report = {
		"observed_at_utc": datetime.now(timezone.utc).isoformat(),
		"scope": "Verifier Python logic only. All process/version responses are simulated. No Lean proof was compiled or verified.",
		"source_path": str(Script.relative_to(Repo)),
		"source_sha256": hashlib.sha256(Script.read_bytes()).hexdigest(),
		"cases": Cases,
		"lean_block_comment_scan_hits": CommentHits,
	}
	Output = Path(__file__).with_name("verifier-probes.json")
	Output.write_text(json.dumps(Report, ensure_ascii=False, indent="\t") + "\n", encoding="utf-8")
	print(json.dumps(Report, ensure_ascii=False, indent="\t"))


if(__name__ == "__main__"):
	main()
