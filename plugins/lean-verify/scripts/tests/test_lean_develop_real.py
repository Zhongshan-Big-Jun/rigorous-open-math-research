#!/usr/bin/env python3
"""Opt-in actual compiler integration for the same generic development entrance."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import subprocess
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lean_develop import TYPE_PRINT_OPTIONS, DevelopSession, make_parser, start_verification, verification_status, verify_targets
from lean_evidence import recheck_manifest
from lean_runtime import LeanRuntime, background_options, sha256_file, write_json
from verify_lean_project import verify_project

LEAN = os.environ.get("LEAN_VERIFY_REAL_LEAN")
LAKE = os.environ.get("LEAN_VERIFY_REAL_LAKE", "lake")


@unittest.skipUnless(LEAN, "set LEAN_VERIFY_REAL_LEAN for actual compiler integration")
class RealDevelopControls(unittest.TestCase):
	@classmethod
	def setUpClass(Class):
		Class.Temp = tempfile.TemporaryDirectory(prefix="develop-real-", dir=os.environ.get("LEAN_VERIFY_TEST_TMPDIR"))
		Class.Base = Path(Class.Temp.name).resolve()
		Class.Results = []
		Class.Counter = 0

	@classmethod
	def tearDownClass(Class):
		Output = os.environ.get("LEAN_DEVELOP_TEST_REPORT")
		if(Output):
			write_json(Output, {"scope": "generic actual Lean development fixture; no SL or full Mathlib build", "results": Class.Results})
		if(os.environ.get("LEAN_VERIFY_KEEP_TEST_ARTIFACTS")):
			Class.Temp._finalizer.detach()
		else:
			Class.Temp.cleanup()

	def project(self):
		type(self).Counter += 1
		Base = self.Base / str(self.Counter)
		Root = Base / "project"
		Root.mkdir(parents=True)
		(Root / "lean-toolchain").write_text("leanprover/lean4:v4.31.0\n", encoding="utf-8")
		Output = Base / "output"
		Runtime = LeanRuntime(Root, Output, LEAN, LAKE, True)
		self.assertIn("4.31.0", Runtime.environment()["lean_version"])
		return Root, Output, Runtime

	def arguments(self, Root, Output, Targets, Action="verify", Extra=()):
		return make_parser().parse_args(["--project", str(Root), "--output", str(Output), "--lean", LEAN, "--lake", LAKE, "--direct", "--timeout", "60", Action, "--targets", str(Targets), *Extra])

	def target_list(self, Root, Expected="∀ n : Nat, n + 0 = n", Declaration="Generic.result"):
		PathValue = Root / "targets.json"
		write_json(PathValue, {"targets": [{"id": "natural-addition", "file": "Main.lean", "declaration": Declaration, "expected_type": Expected}]})
		return PathValue

	def test_candidate_failure_revision_save_new_target_and_old_entry(self):
		Root, Output, Runtime = self.project()
		Candidate = Root.parent / "Candidate.lean"
		Candidate.write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := by\n  exact Nat.zero_add n\nend Generic\n", encoding="utf-8")
		Session = DevelopSession(Runtime, 60, "cli")
		try:
			Probe = Session.probe(["Nat.add_zero"], [])
			self.assertEqual(Probe["status"], "checked", Probe)
			self.assertIn("Nat", Probe["declarations"][0]["actual_type"])
			Bad = Session.trial("Main.lean", Candidate)
			# Nat.zero_add has a different syntactic expression but Lean may reduce both.
			if(Bad["status"] == "candidate_checked"):
				Candidate.write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := by\n  exact False.elim (by contradiction)\nend Generic\n", encoding="utf-8")
				Bad = Session.trial("Main.lean", Candidate)
			self.assertEqual(Bad["status"], "candidate_incomplete", Bad)
			with self.assertRaises(ValueError):
				Session.save(Bad["receipt"])
			Candidate.write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := by\n  exact Nat.add_zero n\nend Generic\n", encoding="utf-8")
			Good = Session.trial("Main.lean", Candidate)
			self.assertEqual(Good["status"], "candidate_checked", Good)
			Saved = Session.save(Good["receipt"])
			self.assertFalse(Saved["exact_root_passed"])
			self.assertEqual((Root / "Main.lean").read_bytes(), Candidate.read_bytes())
		finally:
			Session.close()
		Targets = self.target_list(Root)
		Result = verify_targets(self.arguments(Root, Output, Targets))
		self.assertTrue(Result["exact_root_passed"], Result)
		Manifest = Result["targets"][0]["manifest"]
		self.assertTrue(recheck_manifest(Manifest)["exact_root_passed"])
		# The existing entry still works, without this tool's orchestration.
		from verify_lean_project import make_parser as old_parser, verify_project
		Arguments = old_parser().parse_args(["--project", str(Root), "--output", str(Output / "old-entry"), "--lean", LEAN, "--lake", LAKE, "--direct", "--target-file", "Main.lean", "--declaration", "Generic.result", "--expected-type", "∀ n : Nat, n + 0 = n", "--strict-exit"])
		Old, _ = verify_project(Arguments)
		self.assertTrue(Old["exact_root_passed"], Old)
		write_json(Targets, {"targets": [{"id": "natural-addition", "file": "Main.lean", "declaration": "Generic.result", "expected_type": "∀ n : Nat, 0 + n = n"}]})
		Stale = recheck_manifest(Manifest)
		self.assertFalse(Stale["exact_root_passed"])
		self.assertTrue(any("contract_input:" in Reason for Reason in Stale["reasons"]))
		self.Results.append({"test": self.id(), "probe": Probe, "failed_trial": Bad, "revised_trial": Good, "save": Saved, "verification": Result, "contract_changed": Stale})

	def test_wrong_extra_hypotheses_missing_roots_and_transitive_assumptions(self):
		Root, Output, _ = self.project()
		Cases = [
			("theorem wrong (n : Nat) (h : n = 0) : n + 0 = n := Nat.add_zero n\n", "wrong", "∀ n : Nat, n + 0 = n"),
			("theorem leaf (n : Nat) : n + 0 = n := Nat.add_zero n\n", "missing_root", "∀ n : Nat, n + 0 = n"),
			("theorem unproved : False := by sorry\ndef hidden : False := unproved\ntheorem wrong (n : Nat) : n + 0 = n := False.elim hidden\n", "wrong", "∀ n : Nat, n + 0 = n"),
			("axiom extra : False\ndef hidden : False := extra\ntheorem wrong (n : Nat) : n + 0 = n := False.elim hidden\n", "wrong", "∀ n : Nat, n + 0 = n"),
			("def model : Prop := True\ntheorem wrong : model := True.intro\n", "wrong", "∀ n : Nat, n + 0 = n")]
		for Index, (Code, Declaration, Expected) in enumerate(Cases):
			with self.subTest(Index=Index):
				(Root / "Main.lean").write_text(Code, encoding="utf-8")
				Targets = self.target_list(Root, Expected, Declaration)
				Result = verify_targets(self.arguments(Root, Output / str(Index), Targets))
				self.assertFalse(Result["exact_root_passed"], Result)
				self.Results.append({"test": self.id(), "case": Index, "verification": Result})

	def test_actual_buffer_freshness_and_unavailable_compiler(self):
		Root, Output, Runtime = self.project()
		Candidate = Root.parent / "Candidate.lean"
		Candidate.write_text("theorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Session = DevelopSession(Runtime, 60, "cli")
		try:
			Trial = Session.trial("Main.lean", Candidate)
			self.assertEqual(Trial["status"], "candidate_checked", Trial)
			(Root / "Dependency.lean").write_text("def changed : Nat := 1\n", encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "source or configuration changed"):
				Session.save(Trial["receipt"])
		finally:
			Session.close()
		Missing = DevelopSession(LeanRuntime(Root, Output / "missing", str(Root / "missing-lean"), str(Root / "missing-lake"), True), 1, "cli")
		try:
			Trial = Missing.trial("Main.lean", Candidate)
			self.assertEqual(Trial["status"], "candidate_incomplete")
			self.assertFalse(Trial["exact_root_passed"])
		finally:
			Missing.close()
		self.Results.append({"test": self.id(), "unavailable": Trial})

	def test_real_workflow_resume_and_duplicate_dispatch(self):
		Root, Output, _ = self.project()
		(Root / "Main.lean").write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := Nat.add_zero n\nend Generic\n", encoding="utf-8")
		Targets = self.target_list(Root)
		Arguments = self.arguments(Root, Output, Targets, "start", ("--job-id", "generic-root", "--job-timeout", "120"))
		Started = start_verification(Arguments)
		Duplicate = start_verification(Arguments)
		self.assertTrue(Started["dispatched"])
		self.assertFalse(Duplicate["dispatched"])
		StatusArgs = make_parser().parse_args(["--project", str(Root), "--output", str(Output), "status", "--job-id", "generic-root"])
		Deadline = time.monotonic() + 150
		while(time.monotonic() < Deadline):
			Status = verification_status(StatusArgs)
			if(Status["state"] not in ("STARTING", "RUNNING")):
				break
			time.sleep(0.2)
		self.assertEqual(Status["state"], "SUCCEEDED", Status)
		self.assertTrue(Status["exact_root_passed"], Status)
		self.Results.append({"test": self.id(), "dispatch": Started, "duplicate": Duplicate, "resumed": Status})

	def test_actual_warm_entrance_and_target_extension(self):
		Root, Output, _ = self.project()
		(Root / "Pair/Left").mkdir(parents=True)
		(Root / "Pair/Right").mkdir(parents=True)
		(Root / "Pair/Left/One.lean").write_text("namespace Generic\ntheorem helper (n : Nat) : n + 0 = n := Nat.add_zero n\nend Generic\n", encoding="utf-8")
		(Root / "Pair/Right/Two.lean").write_text("namespace Generic\ntheorem second_helper (n : Nat) : n = n := rfl\nend Generic\n", encoding="utf-8")
		Candidate = Root.parent / "Candidate.lean"
		Code = "import Pair.Left.One\nimport Pair.Right.Two\nnamespace Generic\ntheorem result (n : Nat) : n + 0 = n := (helper n).trans (second_helper n)\nend Generic\n"
		Candidate.write_text(Code.replace("(helper n)", "(Nat.zero_add n)"), encoding="utf-8")
		Script = Path(__file__).resolve().parents[1] / "lean_develop.py"
		ErrorPath = Root.parent / "serve.stderr.log"
		Responses = []
		with ErrorPath.open("wb") as ErrorLog:
			Process = subprocess.Popen([sys.executable, str(Script), "--project", str(Root), "--output", str(Output), "--lean", LEAN, "--lake", LAKE, "--direct", "--timeout", "60", "serve", "--backend", "cli"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=ErrorLog, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="gbk"), **background_options())
			def request(Data):
				Process.stdin.write(json.dumps(Data) + "\n")
				Process.stdin.flush()
				Line = Process.stdout.readline()
				self.assertTrue(Line, ErrorPath.read_text(encoding="utf-8", errors="replace"))
				Response = json.loads(Line)
				Responses.append(Response)
				return Response
			try:
				Bad = request({"action": "trial", "file": "Main.lean", "candidate": str(Candidate)})
				self.assertEqual(Bad["status"], "candidate_incomplete", Bad)
				Candidate.write_text(Code, encoding="utf-8")
				Good = request({"action": "trial", "file": "Main.lean", "candidate": str(Candidate)})
				self.assertEqual(Good["status"], "candidate_checked", Good)
				Receipt = json.loads(Path(Good["receipt"]).read_text(encoding="utf-8"))
				self.assertTrue(any(Item.get("kind") == "development_import_cache" for Item in Receipt["preparation_commands"]))
				self.assertEqual(request({"action": "save", "receipt": Good["receipt"]})["status"], "saved")
				request({"action": "close"})
				self.assertEqual(Process.wait(timeout=10), 0)
			finally:
				if(Process.poll() is None):
					Process.kill()
					Process.wait(timeout=10)
				Process.stdin.close()
				Process.stdout.close()
		Targets = self.target_list(Root)
		First = verify_targets(self.arguments(Root, Output / "first-root", Targets))
		self.assertTrue(First["exact_root_passed"], First)
		Candidate.write_text(Code + "namespace Generic\ntheorem extended (n : Nat) : n + 0 + 0 = n := by\n  exact (result (n + 0)).trans (result n)\nend Generic\n", encoding="utf-8")
		Session = DevelopSession(LeanRuntime(Root, Output / "extension", LEAN, LAKE, True), 60, "cli")
		try:
			Extended = Session.trial("Main.lean", Candidate)
			self.assertEqual(Extended["status"], "candidate_checked", Extended)
			Session.save(Extended["receipt"])
		finally:
			Session.close()
		ListData = json.loads(Targets.read_text(encoding="utf-8"))
		ListData["targets"].append({"id": "addition-composition", "file": "Main.lean", "declaration": "Generic.extended", "expected_type": "∀ n : Nat, n + 0 + 0 = n"})
		write_json(Targets, ListData)
		Expanded = verify_targets(self.arguments(Root, Output / "two-roots", Targets))
		self.assertTrue(Expanded["exact_root_passed"], Expanded)
		self.assertEqual(len(Expanded["targets"]), 2)
		self.Results.append({"test": self.id(), "warm_responses": Responses, "first_root": First, "extension_trial": Extended, "expanded_targets": Expanded})

	def test_actual_save_rechecks_dependency_after_import_query(self):
		Root, Output, Runtime = self.project()
		Helper = Root / "Helper.lean"
		Helper.write_text("theorem helper (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
		Candidate = Root.parent / "Candidate.lean"
		Candidate.write_text("import Helper\ntheorem result (n : Nat) : n + 0 = n := helper n\n", encoding="utf-8")
		Session = DevelopSession(Runtime, 60, "cli")
		try:
			Trial = Session.trial("Main.lean", Candidate)
			self.assertEqual(Trial["status"], "candidate_checked", Trial)
			Receipt = json.loads(Path(Trial["receipt"]).read_bytes())
			RealImports = Session.import_identity
			Events = []
			def actual_import_query_then_edit(Text):
				Imports = RealImports(Text)
				self.assertEqual(Imports, Receipt["import_artifacts"])
				Helper.write_text("theorem helper (n : Nat) : n + 0 = n := by sorry\n", encoding="utf-8")
				Events.append({"event": "source changed after actual import query", "source_sha256": sha256_file(Helper), "imports_unchanged": Imports})
				return Imports
			with patch.object(Session, "import_identity", side_effect=actual_import_query_then_edit):
				with self.assertRaisesRegex(ValueError, "source or configuration changed during save") as Failure:
					Session.save(Trial["receipt"])
			self.assertFalse((Root / "Main.lean").exists())
			self.assertFalse(Path(Trial["receipt"]).with_name("save.json").exists())
			self.assertTrue(all(sha256_file(Item["path"]) == Item["sha256"] for Item in Receipt["import_artifacts"].values()))
			self.Results.append({"test": self.id(), "trial": Trial, "save_error": str(Failure.exception), "events": Events, "destination_created": False})
		finally:
			Session.close()

	def test_actual_batch_rechecks_share_one_input_version(self):
		for Timing in ("second_target", "after_terminal_rechecks"):
			with self.subTest(Timing=Timing):
				Root, Output, _ = self.project()
				First = Root / "First.lean"
				First.write_text("theorem first (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
				(Root / "Second.lean").write_text("theorem second (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
				Targets = Root / "targets.json"
				write_json(Targets, {"targets": [{"id": "first", "file": "First.lean", "declaration": "first", "expected_type": "∀ n : Nat, n + 0 = n"}, {"id": "second", "file": "Second.lean", "declaration": "second", "expected_type": "∀ n : Nat, n + 0 = n"}]})
				Calls = []
				def actual_verify_with_editor_edit(Arguments):
					Calls.append("verify")
					if(Timing == "second_target" and Calls.count("verify") == 2):
						First.write_text("theorem first : False := by sorry\n", encoding="utf-8")
					return verify_project(Arguments)
				def actual_recheck_with_editor_edit(PathValue):
					Calls.append("recheck")
					Check = recheck_manifest(PathValue)
					if(Timing == "after_terminal_rechecks" and Calls.count("recheck") == 2):
						First.write_text("theorem first : False := by sorry\n", encoding="utf-8")
					return Check
				with patch("lean_develop.verify_project", side_effect=actual_verify_with_editor_edit), patch("lean_develop.recheck_manifest", side_effect=actual_recheck_with_editor_edit):
					Result = verify_targets(self.arguments(Root, Output, Targets))
				self.assertEqual(Result["status"], "incomplete", Result)
				self.assertFalse(Result["exact_root_passed"])
				self.assertIn("sources", Result["batch"]["changed"])
				self.assertTrue(all(not Item["exact_root_passed"] for Item in Result["targets"]))
				Observed = [Item["evidence_check"]["exact_root_passed"] for Item in Result["targets"]]
				self.assertEqual(Observed, [False, True] if Timing == "second_target" else [True, True])
				Terminal = [recheck_manifest(Item["manifest"]) for Item in Result["targets"]]
				self.Results.append({"test": self.id(), "timing": Timing, "verification": Result, "actual_post_batch_rechecks": Terminal})

	def test_actual_nested_candidate_rejects_overlapping_output_save_and_batch(self):
		Root, Output, Runtime = self.project()
		(Root / "Src").mkdir()
		Helper = Root / "Src/Helper.lean"
		Helper.write_text("theorem helper (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
		Candidate = Root.parent / "Candidate.lean"
		Candidate.write_text("import Src.Helper\ntheorem result (n : Nat) : n + 0 = n := helper n\n", encoding="utf-8")
		Session = DevelopSession(Runtime, 60, "cli")
		try:
			Trial = Session.trial("Src/Main.lean", Candidate)
			self.assertEqual(Trial["status"], "candidate_checked", Trial)
			Helper.write_text("theorem helper : False := by sorry\n", encoding="utf-8")
			Runtime.LogDir = Root
			with self.assertRaisesRegex(ValueError, "outside the project") as Failure:
				Session.save(Trial["receipt"])
			self.assertFalse((Root / "Src/Main.lean").exists())
			self.assertFalse(Path(Trial["receipt"]).with_name("save.json").exists())
			Targets = Root / "targets.json"
			write_json(Targets, {"targets": [{"id": "nested", "file": "Src/Helper.lean", "declaration": "helper", "expected_type": "∀ n : Nat, n + 0 = n"}]})
			for BadOutput in (Root, Root.parent, Root / "generated", Root / "Src"):
				with self.subTest(Output=BadOutput), self.assertRaisesRegex(ValueError, "outside the project"):
					verify_targets(self.arguments(Root, BadOutput, Targets))
			self.Results.append({"test": self.id(), "actual_nested_trial": Trial, "save_rejected": str(Failure.exception), "destination_created": False, "overlapping_batch_outputs_rejected": [str(Root), str(Root.parent), str(Root / "generated"), str(Root / "Src")]})
		finally:
			Session.close()

	def run_tool_race_fixture(self, Mode):
		Root, _, _ = self.project()
		Base = Root.parent / ("tool-" + Mode)
		Fixture = Path(__file__).with_name("develop_tool_race_fixture.py")
		Log = Root.parent / ("tool-" + Mode + ".log")
		with Log.open("wb") as Stream:
			Process = subprocess.run([sys.executable, "-X", "utf8", str(Fixture), Mode, str(Base), LEAN, LAKE], stdout=Stream, stderr=subprocess.STDOUT, timeout=900, **background_options())
		self.assertEqual(Process.returncode, 0, Log.read_text(encoding="utf-8", errors="replace")[-8000:])
		Report = json.loads((Base / "REPORT.json").read_bytes())
		self.Results.append({"test": self.id(), "fixture_command": Process.args, "log": str(Log), "report": Report})

	def test_actual_verify_rejects_every_late_strict_tool_change(self):
		self.run_tool_race_fixture("verify")

	def test_actual_status_rejects_late_tool_and_binding_read_changes(self):
		self.run_tool_race_fixture("status")

	def test_actual_long_type_is_complete_in_probe_and_strict_extraction(self):
		Root, Output, Runtime = self.project()
		def balanced(Depth):
			if(Depth == 0):
				return "n + 0 = n", "Nat.add_zero n"
			Type, Proof = balanced(Depth - 1)
			return "(" + Type + ") ∧ (" + Type + ")", "And.intro (" + Proof + ") (" + Proof + ")"
		Type, Proof = balanced(9)
		(Root / "Main.lean").write_text("namespace Long\ntheorem result (n : Nat) : " + Type + " := " + Proof + "\nend Long\n", encoding="utf-8")
		Session = DevelopSession(Runtime, 90, "cli")
		try:
			Probe = Session.probe(["Long.result"], ["Main"])
			self.assertEqual(Probe["status"], "checked", Probe)
			Readable = Probe["declarations"][0]["actual_type"]
			self.assertNotIn("⋯", Readable)
			self.assertEqual(Readable.count("Eq"), 512)
			with patch("lean_develop.TYPE_PRINT_OPTIONS", TYPE_PRINT_OPTIONS.replace("10000000", "1")):
				Limited = Session.probe(["Long.result"], ["Main"])
			self.assertEqual(Limited["status"], "incomplete", Limited)
			self.assertFalse(Limited["exact_root_passed"])
		finally:
			Session.close()
		Targets = self.target_list(Root, "∀ n : Nat, " + Type, "Long.result")
		Result = verify_targets(self.arguments(Root, Output / "strict", Targets))
		self.assertTrue(Result["exact_root_passed"], Result)
		Manifest = json.loads(Path(Result["targets"][0]["manifest"]).read_bytes())
		Target = Manifest["target"]
		self.assertNotIn("⋯", Target["actual_type"])
		self.assertEqual(Target["actual_type"].count("Eq"), 512)
		for Tree in (Target["type_expression"], Target["expected_statement"]["type_expression"]):
			Stack, Count = [Tree], 0
			while(Stack):
				Node = Stack.pop()
				if(isinstance(Node, list)):
					Count += int(len(Node) == 2 and Node[0] == "const" and isinstance(Node[1], list) and Node[1][0] == "Eq")
					Stack.extend(Node)
			self.assertEqual(Count, 512)
		self.Results.append({"test": self.id(), "balanced_equality_leaves": 512, "full_probe": Probe, "limited_probe": Limited, "strict_verification": Result, "strict_actual_type": Target["actual_type"], "actual_and_expected_encoded_equality_count": 512})


if(__name__ == "__main__"):
	unittest.main()
