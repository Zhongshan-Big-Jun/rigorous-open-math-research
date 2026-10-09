#!/usr/bin/env python3
"""Portable development controls; synthetic feedback is not compiler evidence."""

from __future__ import annotations

import json
import io
import os
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lean_develop import DEVELOP_TOOLS, DevelopSession, declarations_in_file, development_layout, feedback_passed, load_targets, make_parser, project_file, search_sources, serve, start_verification, tool_hashes, verification_status, verify_targets, workflow_module
from lean_evidence import TOOL_NAMES
from verify_lean_project import derive_target
from lean_runtime import LeanRuntime, background_options, bound_input_changes, full_output, hash_bytes, hash_json, run, sha256_file, source_snapshot, write_json
from lean_feedback import ProtocolFailure


class DevelopControls(unittest.TestCase):
	def setUp(self):
		self.Temp = tempfile.TemporaryDirectory(prefix="develop-unit-", dir=os.environ.get("LEAN_VERIFY_TEST_TMPDIR"))
		self.Base = Path(self.Temp.name).resolve()
		self.Root = self.Base / "project"
		self.Root.mkdir()
		self.Output = self.Base / "output"
		self.Output.mkdir()
		self.Runtime = LeanRuntime(self.Root, self.Output, "missing-lean", "missing-lake", True)
		self.Runtime.Environment = {"sha256": "environment-fixture"}

	def tearDown(self):
		self.Temp.cleanup()

	def targets(self, Items):
		PathValue = self.Root / "targets.json"
		write_json(PathValue, {"targets": Items})
		return PathValue

	def test_empty_missing_duplicate_or_uncompared_targets_rejected(self):
		Target = {"id": "one", "file": "Main.lean", "declaration": "goal", "expected_type": "∀ n : Nat, n = n"}
		for Items in ([], [dict(Target, expected_type="")], [dict(Target, declaration="missing name")], [Target, Target]):
			with self.subTest(Items=Items), self.assertRaises(ValueError):
				load_targets(self.Root, self.targets(Items))
		with self.assertRaises(ValueError):
			load_targets(self.Root, self.targets([Target]), "absent")
		Targets, Digest = load_targets(self.Root, self.targets([Target]))
		self.assertEqual(Targets[0][1]["expected_type"], Target["expected_type"])
		self.assertEqual(Digest, sha256_file(self.Root / "targets.json"))

	def test_destination_cannot_escape_project_or_use_package_tree(self):
		for Name in ("../Escape.lean", ".lake/packages/pkg/Source.lean", ".git/Main.lean", ".lean-verify/Main.lean", "__pycache__/Main.lean", "notes.md"):
			with self.assertRaises(ValueError):
				project_file(self.Root, Name)

	def test_overlapping_outputs_rejected_before_trial_save_verify_start_or_status(self):
		Target = {"id": "one", "file": "Src/Main.lean", "declaration": "result", "expected_type": "∀ n : Nat, n = n"}
		Targets = self.targets([Target])
		for Output in (self.Root, self.Base, self.Root / "generated", self.Root / "Src"):
			with self.subTest(Output=Output):
				with self.assertRaisesRegex(ValueError, "outside the project"):
					development_layout(self.Root, Output)
				with self.assertRaisesRegex(ValueError, "outside the project"):
					DevelopSession(LeanRuntime(self.Root, Output, "missing", "missing", True))
				for Action in ("verify", "start", "status"):
					Extra = ["--job-id", "not-started"] if Action in ("start", "status") else []
					if(Action != "status"):
						Extra += ["--targets", str(Targets)]
					Arguments = make_parser().parse_args(["--project", str(self.Root), "--output", str(Output), Action, *Extra])
					with self.assertRaisesRegex(ValueError, "outside the project"):
						{"verify": verify_targets, "start": start_verification, "status": verification_status}[Action](Arguments)
		Session = DevelopSession(self.Runtime, Backend="cli")
		Receipt = self.receipt()
		self.Runtime.LogDir = self.Root
		try:
			with self.assertRaisesRegex(ValueError, "outside the project"):
				Session.save(Receipt)
			self.assertFalse((self.Root / "Main.lean").exists())
		finally:
			Session.close()

	def test_tool_epoch_covers_every_strict_verifier_tool(self):
		self.assertTrue(set(TOOL_NAMES).issubset(DEVELOP_TOOLS))
		self.assertEqual(set(DEVELOP_TOOLS), set(tool_hashes()))
		for ToolName in ("lake_build_guard.py", "run_manifest.schema.json"):
			with self.subTest(ToolName=ToolName):
				Current = dict(tool_hashes())
				Loaded = dict(Current)
				with patch("lean_develop.LOADED_TOOL_HASHES", Loaded), patch("lean_develop.tool_hashes", side_effect=lambda: dict(Current)):
					Session = DevelopSession(self.Runtime, Backend="cli")
					Current[ToolName] = hash_bytes(b"changed after process load")
					with self.assertRaisesRegex(ValueError, "new Python process"):
						Session.save("not-read-before-identity-check")
					Session.close()

	def test_truncated_or_absent_readable_type_cannot_be_derived(self):
		for ActualType in (None, "", "∀ n : Nat, ⋯"):
			with self.subTest(ActualType=ActualType), self.assertRaisesRegex(ValueError, "complete readable type"):
				derive_target({"actual_type": ActualType}, {}, {})

	def test_empty_candidate_rejected_and_native_gbk_json_output(self):
		Candidate = self.Output / "Empty.lean"
		Candidate.write_text("\n  \n", encoding="utf-8")
		Session = DevelopSession(self.Runtime, Backend="cli")
		try:
			with self.assertRaisesRegex(ValueError, "nonempty"):
				Session.trial("Main.lean", Candidate)
		finally:
			Session.close()
		(self.Root / "Main.lean").write_text("-- ℝ unicode fixture\ntheorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Script = Path(__file__).resolve().parents[1] / "lean_develop.py"
		Command = [sys.executable, str(Script), "--project", str(self.Root), "--output", str(self.Output), "--direct", "--lean", "missing-lean", "--lake", "missing-lake", "search", "--query", "unicode"]
		Result = subprocess.run(Command, capture_output=True, env=dict(os.environ, PYTHONIOENCODING="gbk"), timeout=45)
		self.assertEqual(Result.returncode, 0, Result.stderr.decode("ascii", errors="replace"))
		Data = json.loads(Result.stdout.decode("ascii"))
		self.assertIn("ℝ", Data["matches"][0]["text"])

	def test_lsp_stale_errors_and_unavailable_are_incomplete(self):
		for Data in ({"status": "stale"}, {"status": "unavailable"}, {"status": "timeout"}, {"status": "complete", "diagnostics": [{"severity": 1}]}, {"status": "passed", "diagnostics": [{"severity": "error"}]}):
			self.assertFalse(feedback_passed(Data))
		self.assertTrue(feedback_passed({"status": "complete", "diagnostics": [{"severity": 2}]}))

	def test_import_protocol_failure_retains_incomplete_candidate_receipt(self):
		Candidate = self.Output / "Candidate.lean"
		Candidate.write_text("theorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Session = DevelopSession(self.Runtime, Backend="cli")
		with patch.object(Session, "prepare_imports", return_value=[{"status": "passed", "exit_code": 0}]), patch.object(Session, "import_identity", side_effect=ProtocolFailure("module prefix unavailable")):
			Result = Session.trial("Main.lean", Candidate)
		self.assertEqual(Result["status"], "candidate_incomplete")
		self.assertFalse(Result["exact_root_passed"])
		self.assertIn("module prefix", Result["feedback"]["reason"])
		self.assertTrue(Path(Result["receipt"]).is_file())
		Session.close()

	def test_bound_prose_and_target_list_changes_invalidate(self):
		Source = self.Root / "contract.md"
		Source.write_text("for every natural number", encoding="utf-8")
		Contract = {"input_file_hashes": {str(Source): sha256_file(Source)}}
		self.assertEqual(bound_input_changes(self.Root, Contract), [])
		Source.write_text("for one natural number", encoding="utf-8")
		self.assertTrue(bound_input_changes(self.Root, Contract))
		Source.unlink()
		self.assertTrue(bound_input_changes(self.Root, Contract))
		with self.assertRaises(ValueError):
			bound_input_changes(self.Root, {"input_file_hashes": {"path": "not-a-hash"}})

	def test_namespace_locations_and_cross_project_mathlib_search(self):
		Local = self.Root / "Main.lean"
		Local.write_text("namespace Example\nsection\n/- theorem fake : False -/\nlemma shared_result (n : Nat) : n = n := rfl\nend\nend Example\n", encoding="utf-8")
		Package = self.Root / ".lake/packages/mathlib"
		(Package / "Mathlib").mkdir(parents=True)
		(Package / "Mathlib/Fixture.lean").write_text("lemma shared_result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		write_json(self.Root / "lake-manifest.json", {"packages": [{"name": "mathlib", "rev": "frozen-fixture"}]})
		Records = declarations_in_file(Local)
		self.assertEqual([Item["candidate_name"] for Item in Records], ["Example.shared_result"])
		self.assertEqual(Records[0]["declaration_line"], 4)
		for Engine in (None, __import__("shutil").which("rg")):
			with patch("lean_develop.shutil.which", return_value=Engine):
				Result = search_sources(self.Runtime, "shared_result", 10)
			self.assertEqual({Item["scope"] for Item in Result["matches"]}, {"project", "mathlib"})
			self.assertFalse(Result["exact_root_passed"])

	def receipt(self, Status="passed"):
		Candidate = self.Output / "Candidate.lean"
		Candidate.write_text("theorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Receipt = {"schema": "lean-development-trial/v1", "project_root": str(self.Root), "file": "Main.lean", "candidate": str(Candidate), "candidate_sha256": sha256_file(Candidate), "disk_sha256": None, "input_hashes": source_snapshot(self.Root), "environment_sha256": "environment-fixture", "import_artifacts": {}, "tool_hashes": tool_hashes(), "feedback": {"status": Status}, "search_paths": []}
		Receipt["receipt_sha256"] = hash_json(Receipt)
		ReceiptPath = self.Output / "trial.json"
		write_json(ReceiptPath, Receipt)
		return ReceiptPath

	def test_save_rejects_stale_buffer_destination_source_and_candidate(self):
		Session = DevelopSession(self.Runtime, Backend="cli")
		for Change in ("feedback", "destination", "source", "candidate"):
			with self.subTest(Change=Change):
				ReceiptPath = self.receipt("stale" if Change == "feedback" else "passed")
				if(Change == "destination"):
					(self.Root / "Main.lean").write_text("changed destination")
				elif(Change == "source"):
					(self.Root / "Dependency.lean").write_text("changed dependency")
				elif(Change == "candidate"):
					(self.Output / "Candidate.lean").write_text("changed candidate")
				with self.assertRaises(ValueError):
					Session.save(ReceiptPath)
				for Name in ("Main.lean", "Dependency.lean"):
					(self.Root / Name).unlink(missing_ok=True)
		Session.close()

	def test_completed_job_or_written_report_not_inferred_as_root(self):
		Target = {"id": "one", "file": "Main.lean", "declaration": "result", "expected_type": "∀ n : Nat, n = n"}
		Arguments = make_parser().parse_args(["--project", str(self.Root), "--output", str(self.Output), "verify", "--targets", str(self.targets([Target]))])
		Manifest = {"exact_root_passed": False, "machine": {"status": "passed"}, "root_closure": {"status": "target_mismatch"}, "semantic": {"status": "not_supplied"}}
		ManifestPath = self.Output / "negative.json"
		write_json(ManifestPath, Manifest)
		with patch("lean_develop.verify_project", return_value=(Manifest, ManifestPath)), patch("lean_develop.recheck_manifest", return_value={"exact_root_passed": False}):
			Result = verify_targets(Arguments)
		self.assertEqual(Result["status"], "incomplete")
		self.assertFalse(Result["exact_root_passed"])

	def test_target_list_hash_binds_the_bytes_actually_parsed(self):
		Targets = self.targets([{"id": "one", "file": "Main.lean", "declaration": "result", "expected_type": "∀ n : Nat, n = n"}])
		Raw = Targets.read_bytes()
		ReadBytes = Path.read_bytes
		def replace_after_read(PathValue):
			Result = ReadBytes(PathValue)
			if(PathValue == Targets):
				Targets.write_text('{"targets":[]}', encoding="utf-8")
			return Result
		with patch.object(Path, "read_bytes", replace_after_read):
			Loaded, Digest = load_targets(self.Root, Targets)
		self.assertEqual(len(Loaded), 1)
		self.assertEqual(Digest, hash_bytes(Raw))
		self.assertNotEqual(Digest, sha256_file(Targets))

	def test_save_rechecks_source_and_destination_after_import_query(self):
		Session = DevelopSession(self.Runtime, Backend="cli")
		try:
			for Changed in ("Dependency.lean", "Main.lean"):
				with self.subTest(Changed=Changed):
					Receipt = self.receipt()
					def change_during_import_query(Text):
						(self.Root / Changed).write_text("def changed : Nat := 1\n", encoding="utf-8")
						return {}
					with patch.object(self.Runtime, "environment", return_value={"sha256": "environment-fixture"}), patch.object(Session, "import_identity", side_effect=change_during_import_query):
						with self.assertRaisesRegex(ValueError, "changed during save"):
							Session.save(Receipt)
					if(Changed == "Dependency.lean"):
						self.assertFalse((self.Root / "Main.lean").exists())
					else:
						self.assertEqual((self.Root / Changed).read_text(encoding="utf-8"), "def changed : Nat := 1\n")
					(self.Root / Changed).unlink()
			Receipt = self.receipt()
			Calls = []
			def source_snapshot_then_destination_edit(*Args):
				Snapshot = source_snapshot(*Args)
				Calls.append(Snapshot)
				if(len(Calls) == 2):
					(self.Root / "Main.lean").write_text("def concurrent_destination : Nat := 2\n", encoding="utf-8")
				return Snapshot
			with patch.object(self.Runtime, "environment", return_value={"sha256": "environment-fixture"}), patch.object(Session, "import_identity", return_value={}), patch("lean_develop.source_snapshot", side_effect=source_snapshot_then_destination_edit):
				with self.assertRaisesRegex(ValueError, "destination changed during save"):
					Session.save(Receipt)
			self.assertEqual((self.Root / "Main.lean").read_text(encoding="utf-8"), "def concurrent_destination : Nat := 2\n")
		finally:
			Session.close()

	def positive_batch_fixture(self):
		(self.Root / "First.lean").write_text("theorem first (n : Nat) : n = n := rfl\n", encoding="utf-8")
		(self.Root / "Second.lean").write_text("theorem second (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Statement = self.Root / "statement.txt"
		Statement.write_text("original independently written statement", encoding="utf-8")
		Targets = self.targets([{ "id": "first", "file": "First.lean", "declaration": "first", "expected_type": "∀ n : Nat, n = n", "input_file_hashes": {"statement.txt": sha256_file(Statement)}}, {"id": "second", "file": "Second.lean", "declaration": "second", "expected_type": "∀ n : Nat, n = n"}])
		Arguments = make_parser().parse_args(["--project", str(self.Root), "--output", str(self.Output), "verify", "--targets", str(Targets)])
		def verify_fixture(Args):
			Contract = json.loads(Path(Args.contract).read_bytes())
			Manifest = {"exact_root_passed": True, "machine": {"status": "passed"}, "root_closure": {"exact_root_passed": True}, "semantic": {"status": "not_supplied"}, "evidence": {"contract": Contract}}
			PathValue = self.Output / (Contract["declaration"] + ".json")
			write_json(PathValue, Manifest)
			return Manifest, PathValue
		def recheck_fixture(PathValue):
			return {"exact_root_passed": True, "manifest_sha256": sha256_file(PathValue)}
		return Targets, Arguments, verify_fixture, recheck_fixture

	def test_batch_rechecks_have_common_source_list_and_bound_input_epoch(self):
		for Timing in ("second_target", "terminal_source", "terminal_list", "terminal_bound_input", "terminal_evidence", "terminal_guard", "terminal_schema"):
			with self.subTest(Timing=Timing):
				Targets, Arguments, Verify, Recheck = self.positive_batch_fixture()
				CurrentTools = tool_hashes()
				Calls = []
				def verify_with_edit(Args):
					Calls.append("verify")
					if(Timing == "second_target" and Calls.count("verify") == 2):
						(self.Root / "First.lean").write_text("theorem first : False := by sorry\n", encoding="utf-8")
					return Verify(Args)
				def recheck_with_edit(PathValue):
					Calls.append("recheck")
					Result = Recheck(PathValue)
					if(Calls.count("recheck") == 2):
						if(Timing == "terminal_source"):
							(self.Root / "First.lean").write_text("theorem first : False := by sorry\n", encoding="utf-8")
						elif(Timing == "terminal_list"):
							Targets.write_text('{"targets":[]}', encoding="utf-8")
						elif(Timing == "terminal_bound_input"):
							(self.Root / "statement.txt").write_text("changed independent statement", encoding="utf-8")
						elif(Timing == "terminal_evidence"):
							(self.Output / "first.json").write_text("{}", encoding="utf-8")
						elif(Timing in ("terminal_guard", "terminal_schema")):
							CurrentTools["lake_build_guard.py" if Timing == "terminal_guard" else "run_manifest.schema.json"] = hash_bytes(b"changed during terminal rechecks")
					return Result
				with patch("lean_develop.tool_hashes", side_effect=lambda: dict(CurrentTools)), patch("lean_develop.LeanRuntime.environment", return_value={"sha256": "portable-environment"}), patch("lean_develop.verify_project", side_effect=verify_with_edit), patch("lean_develop.recheck_manifest", side_effect=recheck_with_edit):
					Result = verify_targets(Arguments)
				self.assertEqual(Result["status"], "incomplete", Result)
				self.assertFalse(Result["batch"]["current"], Result)
				self.assertTrue(all(not Item["exact_root_passed"] for Item in Result["targets"]))
				self.assertTrue(all(Item["evidence_check"]["exact_root_passed"] for Item in Result["targets"]))

	def test_job_status_cannot_accept_inputs_changed_during_terminal_rechecks(self):
		Targets, Arguments, Verify, Recheck = self.positive_batch_fixture()
		with patch("lean_develop.LeanRuntime.environment", return_value={"sha256": "portable-environment"}), patch("lean_develop.verify_project", side_effect=Verify), patch("lean_develop.recheck_manifest", side_effect=Recheck):
			Summary = verify_targets(Arguments)
		self.assertTrue(Summary["exact_root_passed"], Summary)
		write_json(self.Root / "stdout.json", Summary)
		Command = [sys.executable, "lean_develop.py", "--project", str(self.Root), "--output", str(self.Output), "--lean", "lean", "--lake", "lake", "verify", "--targets", str(Targets)]
		Job = {"state": "SUCCEEDED", "recorded_inputs_match_current": True, "command": Command, "stdout": "stdout.json"}
		Workflow = workflow_module()
		Calls = []
		def recheck_then_edit(PathValue):
			Calls.append(PathValue)
			Result = Recheck(PathValue)
			if(len(Calls) == 2):
				(self.Root / "First.lean").write_text("theorem first : False := by sorry\n", encoding="utf-8")
			return Result
		with patch.object(Workflow, "job_status", return_value=Job), patch("lean_develop.workflow_module", return_value=Workflow), patch("lean_develop.LeanRuntime.environment", return_value={"sha256": "portable-environment"}), patch("lean_develop.recheck_manifest", side_effect=recheck_then_edit):
			Result = verification_status(make_parser().parse_args(["--project", str(self.Root), "--output", str(self.Output), "status", "--job-id", "batch"]))
		self.assertFalse(Result["exact_root_passed"], Result)
		self.assertFalse(Result["verification"]["batch_current"])

	def test_job_status_final_snapshot_follows_slow_binding_reads(self):
		Targets, Arguments, Verify, Recheck = self.positive_batch_fixture()
		with patch("lean_develop.LeanRuntime.environment", return_value={"sha256": "portable-environment"}), patch("lean_develop.verify_project", side_effect=Verify), patch("lean_develop.recheck_manifest", side_effect=Recheck):
			Summary = verify_targets(Arguments)
		Stdout = self.Root / "stdout.json"
		write_json(Stdout, Summary)
		Command = [sys.executable, "lean_develop.py", "--project", str(self.Root), "--output", str(self.Output), "--lean", "lean", "--lake", "lake", "verify", "--targets", str(Targets)]
		Job = {"state": "SUCCEEDED", "recorded_inputs_match_current": True, "command": Command, "stdout": "stdout.json"}
		Workflow = workflow_module()
		ReadBytes = Path.read_bytes
		def stdout_read_then_source_edit(PathValue):
			Raw = ReadBytes(PathValue)
			if(PathValue == Stdout):
				(self.Root / "First.lean").write_text("theorem first : False := by sorry\n", encoding="utf-8")
			return Raw
		with patch.object(Path, "read_bytes", stdout_read_then_source_edit), patch.object(Workflow, "job_status", return_value=Job), patch("lean_develop.workflow_module", return_value=Workflow), patch("lean_develop.LeanRuntime.environment", return_value={"sha256": "portable-environment"}), patch("lean_develop.recheck_manifest", side_effect=Recheck):
			Result = verification_status(make_parser().parse_args(["--project", str(self.Root), "--output", str(self.Output), "status", "--job-id", "batch"]))
		self.assertFalse(Result["exact_root_passed"], Result)
		self.assertFalse(Result["verification"]["batch_current"])

	def test_workflow_adapter_reuses_actual_local_job_interface(self):
		Workflow = workflow_module()
		self.assertTrue(callable(Workflow.start_job))
		self.assertTrue(callable(Workflow.job_status))
		self.assertTrue(callable(Workflow.atomic_write))

	def test_windows_background_flags_and_actual_child_has_no_console(self):
		self.assertEqual(background_options("nt"), {"creationflags": 0x08000000})
		self.assertEqual(background_options("posix"), {})
		Workflow = workflow_module()
		self.assertEqual(Workflow.hidden_child_options("nt"), {"creationflags": 0x08000000})
		self.assertEqual(Workflow.hidden_child_options("posix"), {})
		if(os.name == "nt"):
			Result = run([sys.executable, "-c", "import ctypes; print(ctypes.windll.kernel32.GetConsoleWindow())"], self.Root, log_dir=self.Output)
			self.assertEqual(Result["status"], "passed", Result)
			self.assertEqual(full_output(Result).strip(), "0")

	def test_warm_server_keeps_failed_requests_incomplete_and_continues(self):
		Session = DevelopSession(self.Runtime, Backend="cli")
		Output = io.StringIO()
		Requests = 'not JSON\n{"action":"unknown"}\n{"action":"restart"}\n{"action":"close"}\n'
		with patch("lean_develop.sys.stdin", io.StringIO(Requests)), patch("lean_develop.sys.stdout", Output):
			self.assertEqual(serve(Session), 0)
		Responses = [json.loads(Line) for Line in Output.getvalue().splitlines()]
		self.assertEqual([Item["status"] for Item in Responses], ["incomplete", "incomplete", "restarted", "closed"])
		self.assertTrue(all(Item["exact_root_passed"] is False for Item in Responses))
		Session.close()

	def test_loaded_python_identity_rejects_real_source_change_until_new_process(self):
		ToolSource = self.Output / "loaded-tool-fixture.py"
		ToolSource.write_text("VERSION = 1\n", encoding="utf-8")
		Loaded = {ToolSource.name: sha256_file(ToolSource)}
		with patch("lean_develop.LOADED_TOOL_HASHES", Loaded), patch("lean_develop.tool_hashes", side_effect=lambda: {ToolSource.name: sha256_file(ToolSource)}):
			Session = DevelopSession(self.Runtime, Backend="cli")
			ToolSource.write_text("VERSION = 2\n", encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "new Python process"):
				Session.trial("Main.lean", "not-read-before-identity-check")
			with self.assertRaisesRegex(ValueError, "new Python process"):
				DevelopSession(self.Runtime, Backend="cli")
			Output = io.StringIO()
			with patch("lean_develop.sys.stdin", io.StringIO('{"action":"restart"}\n')), patch("lean_develop.sys.stdout", Output):
				serve(Session)
			Result = json.loads(Output.getvalue())
			self.assertEqual(Result["status"], "incomplete")
			self.assertFalse(Result["exact_root_passed"])
			Session.close()


if(__name__ == "__main__"):
	unittest.main()
