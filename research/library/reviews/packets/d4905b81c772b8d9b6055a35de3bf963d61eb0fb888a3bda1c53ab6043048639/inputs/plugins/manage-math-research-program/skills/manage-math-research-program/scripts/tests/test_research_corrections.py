#!/usr/bin/env python3
"""Author behavior checks, not an independent mathematical acceptance report."""

import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest import mock

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))
import research_library as library


class CorrectionTests(unittest.TestCase):
	def setUp(self):
		self.Temp = tempfile.TemporaryDirectory()
		self.Root = Path(self.Temp.name).resolve()
		self.Bad = library.save_card(self.Root, dict(tool_id="all-order", content="FALSE fixture: the span of x^(2n), n>=1, is dense in every Sobolev order on [0,1]."))
		self.Dep = library.save_card(self.Root, dict(tool_id="dependent", content="Dependent all-order application.", dependencies=[self.ref(self.Bad)]))
		self.Good = library.save_card(self.Root, dict(tool_id="experience", content="Useful experience: use endpoint traces to test proposed density claims."))
		(self.Root / "audit.txt").write_text("Counterexample fixture: every trial polynomial vanishes at zero; continuous trace excludes the constant 1 in H^1. This refutes this fixture's all-order claim, not every related density statement.", encoding="utf-8")
		library.make_index(self.Root, ReadmePath="tools/README.md")
		self.Input = dict(issue_id="audit-all-order", origin="external", reporter="auditor", summary="Invalid all-order generalization", disposition="retracted", targets=[self.ref(self.Bad)], evidence=[dict(path="audit.txt", locator="trace obstruction")], canonical_nodes=[dict(node_id="DENSITY", version="frozen-v1")])

	def tearDown(self):
		self.Temp.cleanup()

	def ref(self, Card):
		return dict(location=Card["location"], sha256=Card["sha256"])

	def corrections(self):
		try:
			return importlib.import_module("research_corrections")
		except ImportError:
			self.fail("missing executable corrections lifecycle: a correction annotation does not prevent reuse")

	def test_false_card_and_dependent_are_hidden_but_experience_survives(self):
		Corrections = self.corrections()
		Corrections.register_issue(self.Root, self.Input)
		self.assertFalse(library.query_tools(self.Root, "all-order")["hits"])
		self.assertEqual(library.query_tools(self.Root, "endpoint traces")["hits"][0]["location"], self.Good["location"])
		Index = library.read_json(self.Root / "index/tools.json")
		self.assertEqual([Row["location"] for Row in Index["items"]], [self.Good["location"]])
		States = {Row["location"]: Row["correction_state"]["status"] for Row in Index["blocked_items"]}
		self.assertEqual(States[self.Bad["location"]], "retracted")
		self.assertEqual(States[self.Dep["location"]], "needs_review")
		self.assertNotIn("all-order", (self.Root / "tools/README.md").read_text())
		View = library.query_tools(self.Root, "all-order", IncludeAffected=True)
		self.assertEqual(len(View["hits"]), 2)
		self.assertTrue(all(Hit["trust"] == "HISTORY_ONLY_NOT_REUSE" and not Hit["reuse_allowed"] for Hit in View["hits"]))

	def start(self):
		Corrections = self.corrections()
		Issue = Corrections.register_issue(self.Root, self.Input)
		return Corrections, Issue

	def repair(self, Corrections, Card=None, Dependencies=None, Text=None):
		Card = Card or self.Bad
		Data = dict(content=Text or "Corrected density claim: only the stated trace-compatible domain is proposed; all-order universality is withdrawn.")
		if(Dependencies is not None):
			Data["dependencies"] = Dependencies
		New = library.save_card(self.Root, Data, Card["location"], Card["sha256"])
		Revision = Corrections.propose_revision(self.Root, self.Input["issue_id"], self.ref(Card), self.ref(New), "00000000-0000-0000-0000-000000000001", "Restrict the claim to its actual hypotheses and recheck dependencies.")
		return New, Revision

	def synthetic_review(self, Corrections, Revision, Change=None, Kind="mathematics"):
		"""Explicit synthetic transport fixture; no independent agent is claimed."""
		import research_review as review
		Spec = Corrections.review_requirements(self.Root, Revision["revision_id"])
		Spec["kind"] = Kind
		if(Kind == "formal-readback"):
			Spec["claims"] = [dict(id=Spec["claims"][0]["id"], declaration="Fixture.repaired_statement")]
			for Input in Spec["inputs"]:
				Input["role"] = "formal-statement"
		if(Change):
			Change(Spec)
		Packet = review.create_packet(self.Root, Spec)
		Agent = str(uuid.uuid4())
		Spawn = dict(tool="multi_agent_v1__spawn_agent", arguments=dict(fork_context=False, message=Packet["prompt"]), result=dict(agent_id=Agent))
		Dispatch = review.record_dispatch(self.Root, self.Root / Packet["packet"], Spawn)
		Report = dict(packet_sha256=Packet["packet_sha256"], verdict="APPROVED", checked_paths=[Input["path"] for Input in Spec["inputs"]],
			claim_results=[dict(id=Claim["id"], verdict="APPROVED", reason="Synthetic fixture exercises receipt transport and exact bindings, not mathematical acceptance.") for Claim in Spec["claims"]],
			findings=[], limitations=["Synthetic tool transcript. No agent, OS sandbox, proof audit or Lean execution occurred."], readback="Synthetic statement readback.")
		Completion = dict(status={Agent: dict(completed=json.dumps(Report))}, timed_out=False)
		review.receive_review(self.Root, Dispatch["bundle"], Completion)
		return Dispatch["bundle"]

	def test_revision_preserves_old_card_and_notes_and_reindex_stays_blocked(self):
		Note = library.annotate(self.Root, self.Bad["location"], text="Old all-order approval is invalidated by the counterexample.", kind="review")
		NotePath = library.library_root(self.Root) / "annotations" / (Note["annotation_id"] + ".json")
		OldBytes, NoteBytes = (self.Root / self.Bad["version"]).read_bytes(), NotePath.read_bytes()
		Corrections, _ = self.start()
		New, Revision = self.repair(Corrections)
		library.make_index(self.Root)
		(self.Root / "index/tools.json").unlink()
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "Corrected")["hits"])
		self.assertFalse(library.query_tools(self.Root, "approval", IncludeArchived=True, IncludeUnreviewed=True, IncludeStale=True)["hits"])
		self.assertEqual((self.Root / self.Bad["version"]).read_bytes(), OldBytes)
		self.assertEqual(NotePath.read_bytes(), NoteBytes)
		View = Corrections.history(self.Root, self.Bad["location"])
		self.assertEqual(len(View["versions"]), 2)
		OldNotes = next(Row for Row in View["versions"] if Row["sha256"] == self.Bad["sha256"])["annotations"]
		self.assertEqual(OldNotes[0]["sha256"], Note["annotation_id"])
		self.assertTrue(all(not Row["correction_state"]["reuse_allowed"] for Row in View["versions"]))

	def test_release_requires_exact_receipt_then_dependent_needs_separate_repair(self):
		Corrections, _ = self.start()
		New, Revision = self.repair(Corrections)
		Bundle = self.synthetic_review(Corrections, Revision)
		self.assertEqual(Corrections.release(self.Root, Revision["revision_id"], Bundle)["verdict"], "RELEASED")
		self.assertEqual(library.query_tools(self.Root, "Corrected density")["hits"][0]["sha256"], New["sha256"])
		self.assertFalse(library.query_tools(self.Root, "Dependent")["hits"])
		Dependent, DepRevision = self.repair(Corrections, self.Dep, [self.ref(New)], "Repaired dependent application on the restricted domain.")
		self.assertFalse(library.query_tools(self.Root, "dependent")["hits"])
		DepBundle = self.synthetic_review(Corrections, DepRevision)
		self.assertEqual(Corrections.release(self.Root, DepRevision["revision_id"], DepBundle)["verdict"], "RELEASED")
		self.assertEqual(library.query_tools(self.Root, "dependent")["hits"][0]["sha256"], Dependent["sha256"])
		OldView = Corrections.history(self.Root, self.Bad["location"])
		self.assertEqual(next(Row for Row in OldView["versions"] if Row["sha256"] == self.Bad["sha256"])["correction_state"]["status"], "retracted")

	def test_boolean_receipt_missing_module_and_readback_never_release(self):
		Corrections, _ = self.start()
		_, Revision = self.repair(Corrections)
		(self.Root / "fake").mkdir()
		(self.Root / "fake/report.json").write_text('{"pass":true,"independent":true}')
		with self.assertRaises((OSError, ValueError)):
			Corrections.release(self.Root, Revision["revision_id"], "fake")
		Bundle = self.synthetic_review(Corrections, Revision)
		with mock.patch.object(Corrections.importlib, "import_module", side_effect=ImportError("review verifier not installed")):
			with self.assertRaises(ImportError):
				Corrections.release(self.Root, Revision["revision_id"], Bundle)
		Readback = self.synthetic_review(Corrections, Revision, Kind="formal-readback")
		with self.assertRaisesRegex(ValueError, "mathematics approval"):
			Corrections.release(self.Root, Revision["revision_id"], Readback)
		self.assertFalse(library.query_tools(self.Root, "Corrected")["hits"])

	def test_generic_review_and_missing_issue_or_revision_binding_rejected(self):
		Corrections, Issue = self.start()
		_, Revision = self.repair(Corrections)
		for PathValue in (Issue["path"], Revision["path"]):
			Bundle = self.synthetic_review(Corrections, Revision, lambda Spec: Spec.update(inputs=[Row for Row in Spec["inputs"] if Row["path"] != PathValue]))
			with self.assertRaisesRegex(ValueError, "does not bind"):
				Corrections.release(self.Root, Revision["revision_id"], Bundle)
		Bundle = self.synthetic_review(Corrections, Revision, lambda Spec: Spec["claims"][0].update(id="generic-prior-review"))
		with self.assertRaisesRegex(ValueError, "different obligation"):
			Corrections.release(self.Root, Revision["revision_id"], Bundle)
		Bundle = self.synthetic_review(Corrections, Revision, lambda Spec: Spec["claims"][0].update(statement="Only check that 1 equals 1."))
		with self.assertRaisesRegex(ValueError, "different obligation"):
			Corrections.release(self.Root, Revision["revision_id"], Bundle)

	def test_new_revision_and_new_issue_invalidate_old_approval(self):
		Corrections, _ = self.start()
		New, Revision = self.repair(Corrections)
		Bundle = self.synthetic_review(Corrections, Revision)
		Corrections.release(self.Root, Revision["revision_id"], Bundle)
		Next = library.save_card(self.Root, dict(content="A second repair after revisiting the scope."), New["location"], New["sha256"])
		NextRevision = Corrections.propose_revision(self.Root, self.Input["issue_id"], self.ref(self.Bad), self.ref(Next), "another-author", "Check a new scope.")
		self.assertFalse(library.query_tools(self.Root, "second repair")["hits"])
		with self.assertRaises(ValueError):
			Corrections.release(self.Root, NextRevision["revision_id"], Bundle)
		# Even returning to previously reviewed bytes after a new proposal cannot revive it.
		(self.Root / New["location"]).write_bytes((self.Root / New["version"]).read_bytes())
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "Corrected")["hits"])
		NewIssue = dict(self.Input, issue_id="new-audit", targets=[self.ref(New)])
		Corrections.register_issue(self.Root, NewIssue)
		self.assertFalse(library.query_tools(self.Root, "Corrected")["hits"])

	def test_edited_release_card_and_damaged_receipt_reclose_retrieval(self):
		Corrections, _ = self.start()
		New, Revision = self.repair(Corrections)
		Bundle = self.synthetic_review(Corrections, Revision)
		Corrections.release(self.Root, Revision["revision_id"], Bundle)
		(self.Root / Bundle / "completion.json").write_text('{"pass":true}')
		self.assertFalse(library.query_tools(self.Root, "Corrected")["hits"])
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "Corrected")["hits"])
		Changed = library.save_card(self.Root, dict(content="Changed after approval."), New["location"], New["sha256"])
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "Changed")["hits"])

	def test_transitive_versioned_dependencies_and_metadata_removal_remain_blocked(self):
		Leaf = library.save_card(self.Root, dict(tool_id="leaf", content="Leaf application.", dependencies=[self.ref(self.Dep)]))
		Corrections, _ = self.start()
		Changed = library.save_card(self.Root, dict(content="Erased dependency metadata.", dependencies=[]), self.Dep["location"], self.Dep["sha256"])
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "Erased Leaf")["hits"])
		Future = library.save_card(self.Root, dict(content="Future descendant.", dependencies=[self.ref(Changed)]))
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "Future")["hits"])
		self.assertEqual(next(Row for Row in Corrections.history(self.Root)["versions"] if Row["sha256"] == Leaf["sha256"])["correction_state"]["status"], "needs_review")

	def test_corrupt_issue_evidence_event_and_registry_fail_closed(self):
		Corrections, Issue = self.start()
		Store = Corrections.load_store(self.Root)
		Payload = Store["requests"][Issue["request_id"]]["payload"]
		Targets = [self.Root / Issue["path"], self.Root / Payload["evidence"][0]["snapshot"], next((Corrections.root(self.Root) / "events").glob("*.json")), library.library_root(self.Root) / "card-bindings/catalog.json"]
		for Target in Targets:
			with self.subTest(path=Target.name):
				Raw = Target.read_bytes()
				Target.write_bytes(b"{damaged")
				Result = library.query_tools(self.Root, "Useful")
				self.assertEqual(Result["verdict"], "CORRECTIONS_INVALID")
				self.assertFalse(Result["hits"])
				self.assertEqual(library.make_index(self.Root)["verdict"], "CORRECTIONS_INVALID")
				self.assertNotIn("[card]", (self.Root / "tools/README.md").read_text())
				Target.write_bytes(Raw)
				library.make_index(self.Root)

	def test_missing_store_or_version_record_cannot_be_rebuilt_as_clear(self):
		Corrections, _ = self.start()
		Folder = Corrections.root(self.Root)
		Backup = Folder.with_name("corrections-preserved")
		Folder.rename(Backup)
		self.assertEqual(library.make_index(self.Root)["verdict"], "CORRECTIONS_INVALID")
		self.assertFalse(library.query_tools(self.Root, "Useful")["hits"])
		Backup.rename(Folder)
		Record = next(PathValue for PathValue in (library.library_root(self.Root) / "card-bindings").glob("*.json") if PathValue.name != "catalog.json")
		Raw = Record.read_bytes()
		Record.unlink()
		self.assertEqual(library.make_index(self.Root)["verdict"], "CORRECTIONS_INVALID")
		Record.write_bytes(Raw)

	def test_idempotency_conflicts_and_canonical_are_unchanged(self):
		Canonical = self.Root / "blueprint/blueprint.json"
		Canonical.parent.mkdir()
		Raw = b'{"nodes":[{"id":"DENSITY","status":"reliable"}]}\n'
		Canonical.write_bytes(Raw)
		Corrections, First = self.start()
		Again = Corrections.register_issue(self.Root, self.Input)
		self.assertEqual(First["request_id"], Again["request_id"])
		self.assertTrue(Again["reused"])
		self.assertEqual(len(Corrections.load_store(self.Root)["events"]), 1)
		with self.assertRaisesRegex(ValueError, "different input"):
			Corrections.register_issue(self.Root, dict(self.Input, summary="changed report"))
		self.assertEqual(Canonical.read_bytes(), Raw)
		self.assertFalse(Corrections.history(self.Root)["canonical_modified"])

	def test_pending_intent_and_pointer_failure_retry_without_duplicate_issue(self):
		Corrections = self.corrections()
		Original = library.immutable_write
		def interrupt(PathValue, Raw):
			if(PathValue.parent.name == "events"):
				raise OSError("injected before commit")
			Original(PathValue, Raw)
		with mock.patch.object(library, "immutable_write", side_effect=interrupt):
			with self.assertRaises(OSError):
				Corrections.register_issue(self.Root, self.Input)
		self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "CORRECTIONS_INVALID")
		Retry = Corrections.register_issue(self.Root, self.Input)
		self.assertTrue(Retry["reused"])
		self.assertEqual(len(Corrections.load_store(self.Root)["events"]), 1)
		self.assertFalse(library.query_tools(self.Root, "all-order")["hits"])
		NewInput = dict(self.Input, issue_id="pointer-failure")
		OriginalAtomic = library.atomic_write
		def fail_pointer(PathValue, Raw):
			if(PathValue.name == "tools.json"):
				raise OSError("injected after durable issue")
			OriginalAtomic(PathValue, Raw)
		with mock.patch.object(library, "atomic_write", side_effect=fail_pointer):
			with self.assertRaises(OSError):
				Corrections.register_issue(self.Root, NewInput)
		self.assertFalse(library.query_tools(self.Root, "all-order")["hits"])
		Corrections.register_issue(self.Root, NewInput)
		self.assertEqual(len(Corrections.load_store(self.Root)["events"]), 2)

	def test_real_process_exit_and_writer_contention_are_recoverable(self):
		Corrections = self.corrections()
		InputPath = self.Root / "input.json"
		InputPath.write_bytes(library.json_bytes(self.Input))
		Code = """import os,sys
sys.path.insert(0, sys.argv[1])
import research_library as library
import research_corrections as corrections
Original = library.immutable_write
def interrupted(PathValue, Raw):
\tOriginal(PathValue, Raw)
\tif(PathValue.parent.name == 'requests'):
\t\tos._exit(91)
library.immutable_write = interrupted
corrections.register_issue(sys.argv[2], library.read_json(__import__('pathlib').Path(sys.argv[3])))
"""
		Run = subprocess.run([sys.executable, "-c", Code, str(SCRIPT_ROOT), str(self.Root), str(InputPath)], capture_output=True, timeout=20, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
		self.assertEqual(Run.returncode, 91, Run.stderr)
		Lock = library.library_root(self.Root) / "writer.lock"
		with self.assertRaises(FileExistsError):
			Corrections.register_issue(self.Root, self.Input)
		with self.assertRaises(FileExistsError):
			library.query_tools(self.Root, "all-order")
		# subprocess.run waited for the actual owner to exit; preserve its lock bytes.
		Lock.rename(Lock.with_name("writer-confirmed-exit-91.lock"))
		Corrections.register_issue(self.Root, self.Input)
		self.assertEqual(len(Corrections.load_store(self.Root)["events"]), 1)
		self.assertFalse(library.query_tools(self.Root, "all-order")["hits"])

	def test_cli_issue_query_history_and_review_inputs(self):
		Input = self.Root / "issue-input.json"
		Input.write_bytes(library.json_bytes(self.Input))
		Run = subprocess.run([sys.executable, str(SCRIPT_ROOT / "research_corrections.py"), "issue", "--project", str(self.Root), "--input", str(Input)], capture_output=True, text=True, timeout=20, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
		self.assertEqual(Run.returncode, 0, Run.stdout + Run.stderr)
		Run = subprocess.run([sys.executable, str(SCRIPT_ROOT / "research_library.py"), "query", "--project", str(self.Root), "--query", "all-order"], capture_output=True, text=True, timeout=20, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
		self.assertEqual(Run.returncode, 0, Run.stdout + Run.stderr)
		self.assertFalse(json.loads(Run.stdout)["hits"])

	def test_unindexed_legacy_cards_and_preexisting_revision_can_be_quarantined(self):
		Project = self.Root / "legacy-project"
		(Project / "tools").mkdir(parents=True)
		RawOld = b"# Unrestricted all-order claim\n"
		RawNew = b"---\nstatus: SUPERSEDED IN OPERATOR-DOMAIN INTERPRETATION\n---\n# Restricted current claim, still awaiting review\n"
		(Project / "old.md").write_bytes(RawOld)
		(Project / "tools/legacy.md").write_bytes(RawNew)
		(Project / "audit.txt").write_text("Audit addresses old.md; the current revision needs review.")
		Corrections = self.corrections()
		Input = dict(self.Input, targets=[dict(location="tools/legacy.md", sha256=library.digest(RawNew))], evidence=[dict(path="audit.txt", locator="finding"), dict(path="old.md", locator="audited bytes")])
		Corrections.register_issue(Project, Input)
		self.assertFalse(library.query_tools(Project, "Restricted")["hits"])
		self.assertEqual((Project / "tools/legacy.md").read_bytes(), RawNew)
		Evidence = next(iter(Corrections.history(Project)["issues"].values()))["evidence"]
		self.assertEqual((Project / Evidence[1]["snapshot"]).read_bytes(), RawOld)

	def test_depends_on_alias_and_exact_hash_are_required(self):
		Dependent = library.save_card(self.Root, dict(content="alias-descendant-cue", depends_on=[dict(path=self.Bad["location"], sha256=self.Bad["sha256"])]))
		self.start()
		self.assertFalse(library.query_tools(self.Root, "alias-descendant-cue")["hits"])
		with self.assertRaisesRegex(ValueError, "sha256"):
			library.save_card(self.Root, dict(content="Unversioned edge rejected.", dependencies=[dict(location=self.Bad["location"])]))

	def test_two_processes_cannot_overwrite_the_same_issue(self):
		InputPath = self.Root / "race.json"
		InputPath.write_bytes(library.json_bytes(self.Input))
		Command = [sys.executable, str(SCRIPT_ROOT / "research_corrections.py"), "issue", "--project", str(self.Root), "--input", str(InputPath)]
		Processes = [subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")) for _ in range(2)]
		Results = [Process.communicate(timeout=20) for Process in Processes]
		self.assertTrue(any(Process.returncode == 0 for Process in Processes), Results)
		self.assertTrue(all(Process.returncode in (0, 1) for Process in Processes), Results)
		Corrections = self.corrections()
		Corrections.register_issue(self.Root, self.Input)
		self.assertEqual(len(Corrections.load_store(self.Root)["events"]), 1)
		self.assertFalse(library.query_tools(self.Root, "all-order")["hits"])

	def test_release_is_idempotent_and_rejects_remaining_affected_dependency(self):
		Corrections, _ = self.start()
		_, Revision = self.repair(Corrections, self.Dep, Text="A rewritten dependent still relying on the old all-order card.")
		Bundle = self.synthetic_review(Corrections, Revision)
		with self.assertRaisesRegex(ValueError, "depends on an affected"):
			Corrections.release(self.Root, Revision["revision_id"], Bundle)
		_, RootRevision = self.repair(Corrections)
		RootBundle = self.synthetic_review(Corrections, RootRevision)
		First = Corrections.release(self.Root, RootRevision["revision_id"], RootBundle)
		Again = Corrections.release(self.Root, RootRevision["revision_id"], RootBundle)
		self.assertEqual(First["request_id"], Again["request_id"])
		self.assertTrue(Again["reused"])
		self.assertEqual(Again["verdict"], "RELEASED")

	def test_preexisting_repair_can_bind_archived_old_bytes_without_live_rewrite(self):
		OldBytes = (self.Root / self.Bad["location"]).read_bytes()
		Archive = self.Root / "audited-old.md"
		Archive.write_bytes(OldBytes)
		New = library.save_card(self.Root, dict(content="Previously corrected trace-restricted claim."), self.Bad["location"], self.Bad["sha256"])
		NewBytes = (self.Root / New["location"]).read_bytes()
		self.Input.update(disposition="quarantine", targets=[self.ref(New)])
		Corrections, _ = self.start()
		Old = dict(self.ref(self.Bad), snapshot="audited-old.md")
		Revision = Corrections.propose_revision(self.Root, self.Input["issue_id"], Old, self.ref(New), "author", "This repair predates issue intake; independently review the existing candidate.")
		self.assertFalse(library.query_tools(self.Root, "Previously")["hits"])
		Bundle = self.synthetic_review(Corrections, Revision)
		self.assertEqual(Corrections.release(self.Root, Revision["revision_id"], Bundle)["verdict"], "RELEASED")
		self.assertEqual((self.Root / New["location"]).read_bytes(), NewBytes)
		History = Corrections.history(self.Root, New["location"])
		self.assertFalse(next(Row for Row in History["versions"] if Row["sha256"] == self.Bad["sha256"])["correction_state"]["reuse_allowed"])
		self.assertEqual(Archive.read_bytes(), OldBytes)

	def test_retracted_exact_bytes_cannot_be_released_using_an_arbitrary_old_version(self):
		New = library.save_card(self.Root, dict(content="Still false updated all-order claim."), self.Bad["location"], self.Bad["sha256"])
		self.Input["targets"] = [self.ref(New)]
		Corrections, _ = self.start()
		Revision = Corrections.propose_revision(self.Root, self.Input["issue_id"], self.ref(self.Bad), self.ref(New), "author", "Review requested.")
		Bundle = self.synthetic_review(Corrections, Revision)
		with self.assertRaisesRegex(ValueError, "retracted exact bytes"):
			Corrections.release(self.Root, Revision["revision_id"], Bundle)

	def test_opaque_old_yaml_can_bind_current_repair_without_rewriting_live_bytes(self):
		OldRaw = b'---\ntitle: Density: all orders\nsource: Appendix: old\n---\n# Original body\nThe all-order claim needs review.\n'
		Old = dict(location=self.Bad["location"], sha256=library.digest(OldRaw))
		library.snapshot_card(self.Root, OldRaw)
		NewRaw = OldRaw.replace(b'title: Density: all orders', b'title: "Density: all orders"').replace(b'source: Appendix: old', b'source: "Appendix: old"')
		(self.Root / Old["location"]).write_bytes(NewRaw)
		New = dict(location=Old["location"], sha256=library.digest(NewRaw))
		library.make_index(self.Root)
		self.Input.update(disposition="quarantine", targets=[Old])
		Corrections, _ = self.start()
		Opaque = Corrections.load_store(self.Root)["nodes"][Corrections.key(Old)]
		self.assertEqual(Opaque["metadata_status"], "INVALID")
		self.assertFalse(Opaque["dependencies_known"])
		self.assertEqual(Opaque["dependencies"], [])
		self.assertFalse(library.query_tools(self.Root, "Original body")["hits"])
		self.assertEqual((self.Root / New["location"]).read_bytes(), NewRaw)
		Dependent = library.save_card(self.Root, dict(content="opaque-dependent-cue", dependencies=[Old]))
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "opaque-dependent-cue")["hits"])
		Revision = Corrections.propose_revision(self.Root, self.Input["issue_id"], Old, New, "author", "Review the exact current candidate against the opaque old source; quoting alone is not mathematical evidence.")
		Bundle = self.synthetic_review(Corrections, Revision)
		self.assertEqual(Corrections.release(self.Root, Revision["revision_id"], Bundle)["verdict"], "RELEASED")
		self.assertEqual((self.Root / New["location"]).read_bytes(), NewRaw)
		self.assertFalse(library.query_tools(self.Root, "opaque-dependent-cue")["hits"])
		Snapshot = Corrections.version_path(self.Root, Old["sha256"])
		self.assertEqual(Snapshot.read_bytes(), OldRaw)
		Snapshot.write_bytes(OldRaw + b"changed")
		self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "CORRECTIONS_INVALID")

	def test_first_issue_with_only_an_unparseable_card_can_initialize_and_stay_closed(self):
		Project = self.Root / "only-opaque"
		(Project / "tools").mkdir(parents=True)
		Raw = b'---\nstatus: SUPERSEDED: old interpretation\n---\n# old-density-cue\n'
		(Project / "tools/old.md").write_bytes(Raw)
		(Project / "audit.txt").write_text("Audit finding on this exact old card.")
		Input = dict(self.Input, disposition="quarantine", targets=[dict(location="tools/old.md", sha256=library.digest(Raw))])
		Corrections = self.corrections()
		Corrections.register_issue(Project, Input)
		self.assertFalse(library.query_tools(Project, "old-density-cue")["hits"])
		self.assertEqual((Project / "tools/old.md").read_bytes(), Raw)
		library.make_index(Project)
		self.assertFalse(library.query_tools(Project, "old-density-cue", IncludeUnreviewed=True)["hits"])
		View = library.query_tools(Project, "old-density-cue", IncludeAffected=True, IncludeUnreviewed=True)
		self.assertEqual(View["hits"][0]["trust"], "HISTORY_ONLY_NOT_REUSE")

	def test_opaque_registration_alone_does_not_allow_reuse_or_guess_edges(self):
		Corrections = self.corrections()
		PathValue = self.Root / "tools/opaque.md"
		Raw = b'---\ntitle: Opaque: old\ndependencies: unknown: broken\n---\n# opaque-only-cue\n'
		PathValue.write_bytes(Raw)
		with library.writer_lock(library.library_root(self.Root)):
			Corrections.register_version(self.Root, "tools/opaque.md", Raw)
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "opaque-only-cue", IncludeUnreviewed=True)["hits"])
		View = library.query_tools(self.Root, "opaque-only-cue", IncludeAffected=True, IncludeUnreviewed=True)
		self.assertEqual(View["hits"][0]["correction_state"]["status"], "metadata_invalid")
		self.assertEqual(View["hits"][0]["dependencies"], [])
		self.assertFalse(View["hits"][0]["dependencies_known"])


if(__name__ == "__main__"):
	unittest.main()
