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

	def test_upstream_only_release_preserves_direct_and_transitive_review_obligations(self):
		Candidate = library.save_card(self.Root, dict(content="Existing upstream repair."), self.Bad["location"], self.Bad["sha256"])
		Direct = library.save_card(self.Root, dict(tool_id="direct-review", content="direct-review-cue", dependencies=[self.ref(Candidate)]))
		Indirect = library.save_card(self.Root, dict(tool_id="indirect-review", content="indirect-review-cue", dependencies=[self.ref(Direct)]))
		library.make_index(self.Root)
		self.Input.update(disposition="quarantine", targets=[self.ref(Candidate)])
		Corrections, _ = self.start()
		for Card in (Direct, Indirect):
			self.assertFalse(library.query_tools(self.Root, Card["tool_id"])["hits"])
		Revision = Corrections.propose_revision(self.Root, self.Input["issue_id"], self.ref(self.Bad), self.ref(Candidate), "author", "Review an existing upstream repair only.")
		Bundle = self.synthetic_review(Corrections, Revision)
		self.assertEqual(Corrections.release(self.Root, Revision["revision_id"], Bundle)["verdict"], "RELEASED")
		library.make_index(self.Root, ReadmePath="tools/README.md")
		for Card in (Direct, Indirect):
			self.assertFalse(library.query_tools(self.Root, Card["tool_id"])["hits"])
			History = library.query_tools(self.Root, Card["tool_id"], IncludeAffected=True)["hits"]
			Hit = next(Row for Row in History if Row["location"] == Card["location"])
			self.assertEqual(Hit["correction_state"]["status"], "needs_review")
			self.assertFalse(Hit["reuse_allowed"])
			self.assertNotIn(Card["tool_id"], (self.Root / "tools/README.md").read_text())
		DirectNew, DirectRevision = self.repair(Corrections, Direct, [self.ref(Candidate)], "Direct scope has now been repaired and reviewed.")
		DirectBundle = self.synthetic_review(Corrections, DirectRevision)
		self.assertEqual(Corrections.release(self.Root, DirectRevision["revision_id"], DirectBundle)["verdict"], "RELEASED")
		self.assertFalse(library.query_tools(self.Root, Indirect["tool_id"])["hits"])
		_, IndirectRevision = self.repair(Corrections, Indirect, [self.ref(DirectNew)], "Indirect scope now cites the reviewed direct version.")
		IndirectBundle = self.synthetic_review(Corrections, IndirectRevision)
		self.assertEqual(Corrections.release(self.Root, IndirectRevision["revision_id"], IndirectBundle)["verdict"], "RELEASED")

	def test_conflicting_dependency_versions_reject_new_and_legacy_revisions(self):
		Corrections, _ = self.start()
		First = library.save_card(self.Root, dict(content="upstream first version"), "tools/upstream.md")
		Second = library.save_card(self.Root, dict(content="upstream second version"), First["location"], First["sha256"])
		Current = max((First, Second), key=lambda Row: Row["sha256"])
		(self.Root / Current["location"]).write_bytes((self.Root / Current["version"]).read_bytes())
		Dependencies = [self.ref(First), dict(path="tools/./upstream.md", sha256=Second["sha256"])]
		with self.assertRaisesRegex(ValueError, "conflicting dependency versions"):
			Corrections.bind_dependencies(self.Root, Dependencies)
		# Construct an exact legacy store using the former permissive binder.
		# Reloading must reject it without rewriting its immutable records.
		def legacy_bind(Project, Refs, Capture=False):
			Bound = []
			for Ref in Refs:
				Exact = Corrections.exact_ref(Project, Ref)
				Corrections.version_bytes(Project, Exact, Capture)
				if(Exact not in Bound):
					Bound.append(Exact)
			return sorted(Bound, key=lambda Row: (Row["location"], Row["sha256"]))
		with mock.patch.object(Corrections, "bind_dependencies", side_effect=legacy_bind):
			_, Revision = self.repair(Corrections, Dependencies=Dependencies)
		Before = {PathValue: PathValue.read_bytes() for PathValue in Corrections.root(self.Root).rglob("*") if PathValue.is_file()}
		with self.assertRaisesRegex(ValueError, "conflicting dependency versions"):
			Corrections.review_requirements(self.Root, Revision["revision_id"])
		with self.assertRaisesRegex(ValueError, "conflicting dependency versions"):
			Corrections.release(self.Root, Revision["revision_id"], "old-review-bundle")
		self.assertEqual(library.query_tools(self.Root, "Corrected")["verdict"], "CORRECTIONS_INVALID")
		for PathValue, Raw in Before.items():
			self.assertEqual(PathValue.read_bytes(), Raw)

	def test_dependency_cannot_overwrite_repaired_card_review_binding(self):
		Corrections, _ = self.start()
		_, Revision = self.repair(Corrections, Dependencies=[self.ref(self.Bad)])
		with self.assertRaisesRegex(ValueError, "conflicting review input versions"):
			Corrections.review_requirements(self.Root, Revision["revision_id"])

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

	def test_removed_last_committed_request_and_event_cannot_shorten_history(self):
		Corrections, _ = self.start()
		SecondInput = dict(self.Input, issue_id="second-issue", targets=[self.ref(self.Good)])
		Second = Corrections.register_issue(self.Root, SecondInput)
		(self.Root / Second["path"]).unlink()
		sorted((Corrections.root(self.Root) / "events").glob("*.json"))[-1].unlink()
		Result = library.query_tools(self.Root, "Useful")
		self.assertEqual(Result["verdict"], "CORRECTIONS_INVALID")
		self.assertFalse(Result["hits"])
		with self.assertRaises(ValueError):
			Corrections.register_issue(self.Root, SecondInput)
		self.assertEqual(library.make_index(self.Root)["verdict"], "CORRECTIONS_INVALID")

	def test_conflicting_location_path_aliases_are_rejected_at_real_call_sites(self):
		Corrections, _ = self.start()
		Conflict = dict(self.ref(self.Good), path=self.Bad["location"])
		with self.assertRaisesRegex(ValueError, "location and path"):
			library.save_card(self.Root, dict(content="alias-bypass-cue", dependencies=[Conflict]))
		with self.assertRaisesRegex(ValueError, "location and path"):
			Corrections.register_issue(self.Root, dict(self.Input, issue_id="ambiguous", targets=[Conflict]))
		with self.assertRaisesRegex(ValueError, "location and path"):
			Corrections.propose_revision(self.Root, self.Input["issue_id"], self.ref(self.Bad), Conflict, "author", "ambiguous candidate")
		Agreeing = dict(self.ref(self.Bad), path="tools/../" + self.Bad["location"])
		Dependent = library.save_card(self.Root, dict(content="agreeing-alias-cue", dependencies=[Agreeing]))
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "agreeing-alias-cue")["hits"])
		self.assertEqual(Corrections.read_versions(self.Root)[Corrections.key(Dependent)]["dependencies"], [self.ref(self.Bad)])

	def test_archived_intake_retry_recovers_binding_catalog_and_marker_gaps(self):
		Corrections = self.corrections()
		for Boundary in ("binding", "catalog", "marker"):
			with self.subTest(boundary=Boundary):
				OldRaw = ("# Unindexed archived " + Boundary + "\n").encode()
				Archive = self.Root / (Boundary + "-old.md")
				Archive.write_bytes(OldRaw)
				Input = dict(self.Input, issue_id="gap-" + Boundary, targets=[dict(location=self.Bad["location"], sha256=library.digest(OldRaw), snapshot=Archive.name)])
				OriginalImmutable, OriginalAtomic = library.immutable_write, library.atomic_write
				def interrupt(PathValue, Raw):
					if(Boundary == "marker" and PathValue.name == "card-bindings-required.json"):
						raise OSError("injected before registry marker publication")
					OriginalImmutable(PathValue, Raw)
					if(Boundary == "binding" and PathValue.parent.name == "card-bindings"):
						raise OSError("injected after binding publication")
				def interrupt_catalog(PathValue, Raw):
					OriginalAtomic(PathValue, Raw)
					if(Boundary == "catalog" and PathValue.name == "catalog.json"):
						raise OSError("injected after catalog publication")
				with mock.patch.object(library, "immutable_write", side_effect=interrupt), mock.patch.object(library, "atomic_write", side_effect=interrupt_catalog):
					with self.assertRaises(OSError):
						Corrections.register_issue(self.Root, Input)
				Result = Corrections.register_issue(self.Root, Input)
				Store = Corrections.load_store(self.Root)
				self.assertIn(Result["request_id"], Store["requests"])
				self.assertEqual(Corrections.version_bytes(self.Root, Input["targets"][0]), OldRaw)

	def test_expected_head_rejects_a_valid_reordered_journal_with_same_membership(self):
		Corrections, First = self.start()
		Second = Corrections.register_issue(self.Root, dict(self.Input, issue_id="second", targets=[self.ref(self.Good)]))
		Folder = Corrections.root(self.Root) / "events"
		for PathValue in Folder.glob("*.json"):
			PathValue.unlink()
		Previous = None
		for Sequence, Result in enumerate((Second, First)):
			Event = dict(schema=Corrections.SCHEMA, previous=Previous, request=Result["request_id"])
			Raw = library.json_bytes(Event)
			Previous = library.digest(Raw)
			(Folder / f"{Sequence:08d}-{Previous}.json").write_bytes(Raw)
		with self.assertRaisesRegex(ValueError, "membership/head"):
			Corrections.load_store(self.Root)
		self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "CORRECTIONS_INVALID")

	def exit_writer(self, Project, Input, Boundary, ExitCode=92):
		InputPath = Project / "exit-input.json"
		InputPath.write_bytes(library.json_bytes(Input))
		Code = """import os,sys,json
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import research_library as library
import research_corrections as corrections
Boundary = sys.argv[4]
OriginalImmutable, OriginalAtomic = library.immutable_write, library.atomic_write
def stop():
\tos._exit(int(sys.argv[5]))
def immutable(PathValue, Raw):
\tOriginalImmutable(PathValue, Raw)
\tif((Boundary == 'registration-intent' and PathValue.name == 'card-binding-pending.json') or
\t\t(Boundary == 'binding' and PathValue.parent.name == 'card-bindings') or
\t\t(Boundary == 'marker' and PathValue.name == 'card-bindings-required.json') or
\t\t(Boundary == 'initial-anchor' and PathValue.name == 'corrections-journal.json') or
\t\t(Boundary == 'request' and PathValue.parent.name == 'requests') or
\t\t(Boundary == 'event' and PathValue.parent.name == 'events')):
\t\tstop()
def atomic(PathValue, Raw):
\tOriginalAtomic(PathValue, Raw)
\tif(Boundary == 'catalog' and PathValue.name == 'catalog.json'):
\t\tstop()
\tif(PathValue.name == 'corrections-journal.json'):
\t\tData = json.loads(Raw)
\t\tif((Boundary == 'journal-intent' and Data['pending'] is not None) or
\t\t\t(Boundary == 'head' and Data['pending'] is None)):
\t\t\tstop()
library.immutable_write, library.atomic_write = immutable, atomic
corrections.register_issue(sys.argv[2], library.read_json(Path(sys.argv[3])))
"""
		Run = subprocess.run([sys.executable, "-c", Code, str(SCRIPT_ROOT), str(Project), str(InputPath), Boundary, str(ExitCode)], capture_output=True, timeout=20, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
		self.assertEqual(Run.returncode, ExitCode, Run.stdout + Run.stderr)
		Lock = library.library_root(Project) / "writer.lock"
		LockRaw = Lock.read_bytes()
		with self.assertRaises(FileExistsError):
			self.corrections().register_issue(Project, Input)
		# run() joined this exact child. Preserve the exited owner's lock, not a
		# guessed stale lock belonging to a possibly live writer.
		Preserved = Lock.with_name("writer-exited-" + Boundary + ".lock")
		Lock.rename(Preserved)
		self.assertEqual(Preserved.read_bytes(), LockRaw)

	def test_real_exit_recovery_at_every_registration_publication_boundary(self):
		Corrections = self.corrections()
		for Existing in (False, True):
			for Boundary in ("registration-intent", "binding", "catalog", "marker"):
				with self.subTest(existing_registry=Existing, boundary=Boundary):
					Project = self.Root if Existing else self.Root / ("fresh-" + Boundary)
					(Project / "tools").mkdir(parents=True, exist_ok=True)
					(Project / "audit.txt").write_text("Archived old claim needs review.")
					OldRaw = ("# Old archived claim " + str(Existing) + Boundary + "\n").encode()
					(Project / "archived.md").write_bytes(OldRaw)
					LiveRaw = b"# Existing repaired candidate\n"
					(Project / "tools/archived-card.md").write_bytes(LiveRaw)
					Input = dict(self.Input, issue_id="exit-" + Boundary, targets=[dict(location="tools/archived-card.md", sha256=library.digest(OldRaw), snapshot="archived.md")])
					self.exit_writer(Project, Input, Boundary)
					with self.assertRaisesRegex(ValueError, "unfinished version registration"):
						Corrections.read_versions(Project)
					Folder = library.library_root(Project) / "card-bindings"
					Before = {PathValue: PathValue.read_bytes() for PathValue in Folder.glob("*.json") if PathValue.name != "catalog.json"}
					Result = Corrections.register_issue(Project, Input)
					Again = Corrections.register_issue(Project, Input)
					self.assertEqual(Result["request_id"], Again["request_id"])
					self.assertTrue(Again["reused"])
					for PathValue, Raw in Before.items():
						self.assertEqual(PathValue.read_bytes(), Raw)
					Store = Corrections.load_store(Project)
					self.assertEqual(sum(Event["request"] == Result["request_id"] for Event in Store["events"]), 1)
					self.assertEqual(Corrections.version_bytes(Project, Input["targets"][0]), OldRaw)
					self.assertEqual((Project / "tools/archived-card.md").read_bytes(), LiveRaw)
					self.assertFalse(library.query_tools(Project, "Existing repaired")["hits"])

	def test_real_exit_recovery_at_every_journal_publication_boundary(self):
		Corrections = self.corrections()
		for Count, Boundary in enumerate(("initial-anchor", "journal-intent", "request", "event", "head"), 1):
			with self.subTest(boundary=Boundary):
				Input = dict(self.Input, issue_id="journal-" + Boundary)
				self.exit_writer(self.Root, Input, Boundary)
				Result = library.query_tools(self.Root, "Useful")
				self.assertEqual(Result["verdict"], "RETRIEVAL_ONLY" if Boundary == "head" else "CORRECTIONS_INVALID")
				AnchorRaw = Corrections.journal_path(self.Root).read_bytes()
				if(Boundary in ("journal-intent", "request", "event")):
					with self.assertRaisesRegex(ValueError, "different input"):
						Corrections.register_issue(self.Root, dict(Input, summary="not the original request"))
					self.assertEqual(Corrections.journal_path(self.Root).read_bytes(), AnchorRaw)
				Retry = Corrections.register_issue(self.Root, Input)
				self.assertEqual(len(Corrections.load_store(self.Root)["events"]), Count)
				self.assertEqual(Corrections.register_issue(self.Root, Input)["request_id"], Retry["request_id"])
				self.assertFalse(library.query_tools(self.Root, "all-order")["hits"])

	def test_registration_recovery_rejects_corruption_without_adopting_it(self):
		Corrections = self.corrections()
		OldRaw = b"# Reserved archived bytes\n"
		(self.Root / "archived.md").write_bytes(OldRaw)
		Input = dict(self.Input, targets=[dict(location=self.Bad["location"], sha256=library.digest(OldRaw), snapshot="archived.md")])
		self.exit_writer(self.Root, Input, "binding")
		Folder, Catalog, Marker, Pending = Corrections.registry_paths(self.Root)
		IntentRaw = Pending.read_bytes()
		Intent = json.loads(IntentRaw)
		NodeRaw = library.json_bytes(Intent["node"])
		NodePath = Folder / (library.digest(NodeRaw) + ".json")
		Names = library.read_json(Catalog)["records"]
		OldRecord = Folder / (Names[0] + ".json")
		Snapshot = Corrections.version_path(self.Root, library.digest(OldRaw))
		Rogue = dict(Intent["node"], location="tools/unrequested.md")
		RogueRaw = library.json_bytes(Rogue)
		RoguePath = Folder / (library.digest(RogueRaw) + ".json")
		for Target, Damage in ((NodePath, b"{damaged"), (OldRecord, None), (Snapshot, b"different bytes"),
			(Catalog, library.json_bytes(dict(schema=Corrections.SCHEMA, records=[]))), (Marker, None),
			(RoguePath, RogueRaw), (Pending, None), (Pending, b"{damaged")):
			with self.subTest(target=Target.name, damage=Damage):
				Saved = Target.read_bytes() if Target.exists() else None
				if(Damage is None):
					Target.unlink()
				else:
					Target.write_bytes(Damage)
				ExpectedCatalog = Catalog.read_bytes()
				with self.assertRaises((OSError, ValueError)):
					Corrections.register_issue(self.Root, Input)
				self.assertEqual(Catalog.read_bytes(), ExpectedCatalog)
				self.assertEqual(Target.read_bytes() if Target.exists() else None, Damage)
				self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "CORRECTIONS_INVALID")
				if(Saved is None):
					Target.unlink()
				else:
					Target.write_bytes(Saved)
		Corrections.register_issue(self.Root, Input)
		self.assertFalse(Pending.exists())
		self.assertFalse(library.query_tools(self.Root, "all-order")["hits"])

	def test_registry_orphan_without_intent_is_not_silently_cataloged(self):
		Corrections = self.corrections()
		Folder, Catalog, _, Pending = Corrections.registry_paths(self.Root)
		Node = dict(Corrections.read_versions(self.Root)[Corrections.key(self.Bad)], location="tools/unrequested.md")
		Raw = library.json_bytes(Node)
		PathValue = Folder / (library.digest(Raw) + ".json")
		PathValue.write_bytes(Raw)
		Before = Catalog.read_bytes()
		self.assertFalse(Pending.exists())
		with library.writer_lock(library.library_root(self.Root)):
			with self.assertRaisesRegex(ValueError, "catalog"):
				Corrections.register_version(self.Root, self.Good["location"], (self.Root / self.Good["location"]).read_bytes())
		self.assertEqual(Catalog.read_bytes(), Before)
		self.assertEqual(PathValue.read_bytes(), Raw)
		self.assertEqual(library.make_index(self.Root)["verdict"], "CORRECTIONS_INVALID")

	def test_legacy_adoption_is_explicit_exact_idempotent_and_preserves_identities(self):
		Corrections, Issue = self.start()
		New, Revision = self.repair(Corrections)
		Store = Corrections.load_store(self.Root)
		Expected = Corrections.legacy_expectation(Store)
		Before = {PathValue: PathValue.read_bytes() for PathValue in Corrections.root(self.Root).rglob("*") if PathValue.is_file()}
		Corrections.journal_path(self.Root).unlink()  # Model a fully committed v1 journal.
		self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "CORRECTIONS_INVALID")
		self.assertEqual(library.make_index(self.Root)["verdict"], "CORRECTIONS_INVALID")
		with self.assertRaisesRegex(ValueError, "adoption"):
			Corrections.register_issue(self.Root, self.Input)
		for Wrong in ({}, dict(Expected, requests=Expected["requests"][:-1]), dict(Expected, head="0" * 64), dict(Expected, journal_sha256="0" * 64)):
			with self.subTest(expected=Wrong), self.assertRaises(ValueError):
				Corrections.adopt_legacy_journal(self.Root, Wrong)
			self.assertFalse(Corrections.journal_path(self.Root).exists())
		ExpectedPath = self.Root / "coordinator-validated-legacy.json"
		ExpectedPath.write_bytes(library.json_bytes(Expected))
		Run = subprocess.run([sys.executable, str(SCRIPT_ROOT / "research_corrections.py"), "adopt-legacy", "--project", str(self.Root), "--expected", str(ExpectedPath)], capture_output=True, text=True, timeout=20, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
		self.assertEqual(Run.returncode, 0, Run.stdout + Run.stderr)
		self.assertEqual(json.loads(Run.stdout)["verdict"], "ADOPTED")
		Corrections.adopt_legacy_journal(self.Root, Expected)
		AnchorPath = Corrections.journal_path(self.Root)
		AnchorRaw = AnchorPath.read_bytes()
		AnchorPath.write_bytes(library.json_bytes(dict(json.loads(AnchorRaw), head="0" * 64)))
		with self.assertRaisesRegex(ValueError, "immutable record conflict"):
			Corrections.adopt_legacy_journal(self.Root, Expected)
		self.assertNotEqual(AnchorPath.read_bytes(), AnchorRaw)
		AnchorPath.write_bytes(AnchorRaw)
		for PathValue, Raw in Before.items():
			self.assertEqual(PathValue.read_bytes(), Raw)
		self.assertEqual(Corrections.register_issue(self.Root, self.Input)["request_id"], Issue["request_id"])
		Again = Corrections.propose_revision(self.Root, self.Input["issue_id"], self.ref(self.Bad), self.ref(New), "00000000-0000-0000-0000-000000000001", "Restrict the claim to its actual hypotheses and recheck dependencies.")
		self.assertEqual(Again["revision_id"], Revision["revision_id"])
		self.assertTrue(Again["reused"])
		Corrections.register_issue(self.Root, dict(self.Input, issue_id="after-adoption"))
		self.assertEqual(len(Corrections.load_store(self.Root)["events"]), 3)
		self.assertFalse(library.query_tools(self.Root, "Corrected")["hits"])

	def test_validated_empty_legacy_store_needs_explicit_adoption_too(self):
		Corrections = self.corrections()
		with library.writer_lock(library.library_root(self.Root)):
			Corrections.initialize(self.Root)
		Expected = Corrections.legacy_expectation(Corrections.load_store(self.Root))
		self.assertEqual(Expected["requests"], [])
		self.assertIsNone(Expected["head"])
		Corrections.journal_path(self.Root).unlink()
		self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "CORRECTIONS_INVALID")
		with self.assertRaisesRegex(ValueError, "adoption"):
			Corrections.register_issue(self.Root, self.Input)
		Corrections.adopt_legacy_journal(self.Root, Expected)
		self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "RETRIEVAL_ONLY")

	def test_legacy_adoption_rejects_truncation_pending_requests_and_corrupt_evidence(self):
		Corrections, First = self.start()
		Second = Corrections.register_issue(self.Root, dict(self.Input, issue_id="legacy-second", targets=[self.ref(self.Good)]))
		Store = Corrections.load_store(self.Root)
		Expected = Corrections.legacy_expectation(Store)
		Corrections.journal_path(self.Root).unlink()
		RequestPath = self.Root / Second["path"]
		EventPath = sorted((Corrections.root(self.Root) / "events").glob("*.json"))[-1]
		EvidencePath = self.Root / Store["requests"][First["request_id"]]["payload"]["evidence"][0]["snapshot"]
		for Removed in ((RequestPath, EventPath), (EventPath,), (EvidencePath,)):
			with self.subTest(removed=[PathValue.name for PathValue in Removed]):
				Saved = {PathValue: PathValue.read_bytes() for PathValue in Removed}
				for PathValue in Removed:
					PathValue.unlink()
				with self.assertRaises((OSError, ValueError)):
					Corrections.adopt_legacy_journal(self.Root, Expected)
				self.assertFalse(Corrections.journal_path(self.Root).exists())
				for PathValue, Raw in Saved.items():
					PathValue.write_bytes(Raw)
		Corrections.adopt_legacy_journal(self.Root, Expected)
		self.assertEqual(len(Corrections.load_store(self.Root)["events"]), 2)

	def test_pending_journal_corruption_cannot_be_replayed_as_a_commit(self):
		Corrections = self.corrections()
		self.exit_writer(self.Root, self.Input, "event")
		Store = Corrections.load_store(self.Root, AllowPending=True)
		RequestHash = Store["pending"][0]
		RequestPath = Corrections.artifact(self.Root, "requests", RequestHash)
		EventPath = next((Corrections.root(self.Root) / "events").glob("*.json"))
		AnchorPath = Corrections.journal_path(self.Root)
		Original = {PathValue: PathValue.read_bytes() for PathValue in (RequestPath, EventPath, AnchorPath)}
		for Target in (RequestPath, EventPath, AnchorPath):
			with self.subTest(target=Target.name):
				Target.write_bytes(b"{damaged")
				with self.assertRaises(ValueError):
					Corrections.register_issue(self.Root, self.Input)
				self.assertEqual(Target.read_bytes(), b"{damaged")
				self.assertEqual(library.query_tools(self.Root, "Useful")["verdict"], "CORRECTIONS_INVALID")
				Target.write_bytes(Original[Target])
		Result = Corrections.register_issue(self.Root, self.Input)
		self.assertEqual(Result["request_id"], RequestHash)
		self.assertEqual(RequestPath.read_bytes(), Original[RequestPath])
		self.assertEqual(EventPath.read_bytes(), Original[EventPath])

	def test_payload_and_event_bytes_keep_the_legacy_v1_contract(self):
		Corrections, Issue = self.start()
		EvidenceHash = library.digest((self.Root / "audit.txt").read_bytes())
		LegacyPayload = dict(issue_id=self.Input["issue_id"], origin="external", reporter="auditor", summary="Invalid all-order generalization",
			disposition="retracted", targets=[self.ref(self.Bad)], evidence=[dict(path="audit.txt", sha256=EvidenceHash,
				snapshot="research/library/corrections/evidence/" + EvidenceHash + ".bin", locator="trace obstruction")],
			canonical_nodes=[dict(node_id="DENSITY", version="frozen-v1")], canonical_action="NEEDS_RECEIVER_REVIEW")
		LegacyRequest = dict(schema="research-corrections/v1", kind="issue", key="issue:" + self.Input["issue_id"], input_sha256=library.digest(library.json_bytes(self.Input)), payload=LegacyPayload)
		LegacyRaw = library.json_bytes(LegacyRequest)
		self.assertEqual((self.Root / Issue["path"]).read_bytes(), LegacyRaw)
		self.assertEqual(Issue["request_id"], library.digest(LegacyRaw))
		LegacyEvent = library.json_bytes(dict(schema="research-corrections/v1", previous=None, request=Issue["request_id"]))
		self.assertEqual(next((Corrections.root(self.Root) / "events").glob("*.json")).read_bytes(), LegacyEvent)
		New, Revision = self.repair(Corrections)
		LegacyInput = dict(issue=self.Input["issue_id"], old=self.ref(self.Bad), new=self.ref(New), author="00000000-0000-0000-0000-000000000001", rationale="Restrict the claim to its actual hypotheses and recheck dependencies.")
		InputHash = library.digest(library.json_bytes(LegacyInput))
		LegacyRevision = dict(schema="research-corrections/v1", kind="revision", key="revision:" + InputHash, input_sha256=InputHash,
			payload=dict(issue=Issue["request_id"], old=LegacyInput["old"], new=LegacyInput["new"], old_status="retracted", author=LegacyInput["author"], rationale=LegacyInput["rationale"]))
		self.assertEqual((self.Root / Revision["path"]).read_bytes(), library.json_bytes(LegacyRevision))

	def test_manual_opaque_repair_preserves_bytes_and_save_card_limitation(self):
		Corrections = self.corrections()
		Target = self.Root / "tools/manual-opaque.md"
		OldRaw = b'---\ntitle: Density: broken metadata\n---\n# manual-opaque-cue\n'
		Target.write_bytes(OldRaw)
		Old = dict(location="tools/manual-opaque.md", sha256=library.digest(OldRaw))
		Input = dict(self.Input, issue_id="manual-opaque", disposition="quarantine", targets=[Old])
		Corrections.register_issue(self.Root, Input)
		with self.assertRaises(ValueError):
			library.save_card(self.Root, dict(title="Explicit replacement", content="manual-repaired-cue"), Old["location"], Old["sha256"])
		self.assertEqual(Target.read_bytes(), OldRaw)
		NewRaw = b'---\n{"tool_id":"manual-opaque","title":"Explicit replacement","dependencies":[],"author_ids":["manual-author"]}\n---\n# manual-repaired-cue\nRestricted candidate; mathematical review remains required.\n'
		with library.writer_lock(library.library_root(self.Root)):
			self.assertEqual(library.digest(Target.read_bytes()), Old["sha256"])
			library.read_metadata(NewRaw)
			library.snapshot_card(self.Root, OldRaw)
			Corrections.register_version(self.Root, Old["location"], OldRaw)
			Corrections.register_version(self.Root, Old["location"], NewRaw)
			library.atomic_write(Target, NewRaw)
		New = dict(location=Old["location"], sha256=library.digest(NewRaw))
		library.make_index(self.Root)
		self.assertFalse(library.query_tools(self.Root, "manual-repaired-cue", IncludeUnreviewed=True)["hits"])
		Revision = Corrections.propose_revision(self.Root, "manual-opaque", Old, New, "manual-author", "Deliberately supplied complete metadata and corrected claim; inspect old opaque source.")
		Spec = Corrections.review_requirements(self.Root, Revision["revision_id"])
		self.assertEqual(Spec["metadata_warnings"][0]["version"], Old)
		self.assertIn("manual-author", Spec["author_ids"])
		self.assertEqual(Corrections.version_bytes(self.Root, Old), OldRaw)
		self.assertEqual(Corrections.version_bytes(self.Root, New), NewRaw)
		self.assertEqual(Target.read_bytes(), NewRaw)
		self.assertFalse(library.query_tools(self.Root, "manual-repaired-cue")["hits"])

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
