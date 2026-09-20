#!/usr/bin/env python3
"""Receipt invariants using explicitly synthetic tool transcripts, not live agents."""

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import research_library as library
import research_review as review


class ReviewReceiptTests(unittest.TestCase):
	def setUp(self):
		self.Temp = tempfile.TemporaryDirectory()
		self.Project = Path(self.Temp.name).resolve()
		(self.Project / "proof.md").write_text("Two terminal zeros leave the earlier term in a second difference.\n")
		(self.Project / "issue.json").write_text('{"finding":"terminal difference was incorrectly zero"}\n')
		self.Author = "00000000-0000-0000-0000-000000000001"
		self.Agent = "00000000-0000-0000-0000-000000000002"
		self.Spec = dict(author_ids=[self.Author], inputs=[dict(path="proof.md", role="proof"), dict(path="issue.json", role="correction")],
			claims=[dict(id="terminal", statement="The displayed terminal difference follows from the two zero conditions.", verification="analytic")])
		self.Packet = review.create_packet(self.Project, self.Spec)
		self.Spawn = dict(tool="multi_agent_v1__spawn_agent", arguments=dict(fork_context=False, message=self.Packet["prompt"]), result=dict(agent_id=self.Agent))

	def tearDown(self):
		self.Temp.cleanup()

	def report(self):
		return dict(packet_sha256=self.Packet["packet_sha256"], verdict="APPROVED", checked_paths=["proof.md", "issue.json"],
			claim_results=[dict(id="terminal", verdict="APPROVED", reason="Substitution of the two zero conditions leaves the earlier term.")],
			findings=[], limitations=["Synthetic transcript fixture; no subagent or Lean execution occurred."])

	def complete(self, Report=None):
		Dispatch = review.record_dispatch(self.Project, self.Project / self.Packet["packet"], self.Spawn)
		Completion = dict(status={self.Agent: dict(completed=json.dumps(Report or self.report()))}, timed_out=False)
		return Dispatch, Completion, review.receive_review(self.Project, Dispatch["bundle"], Completion)

	def test_bound_review_is_idempotent_and_does_not_claim_formal_proof(self):
		Dispatch, Completion, Result = self.complete()
		self.assertEqual(Result["verdict"], "APPROVED")
		self.assertEqual(Result["bindings"]["proof.md"], library.digest((self.Project / "proof.md").read_bytes()))
		self.assertEqual(Result["trust"], review.TRUST)
		self.assertEqual(Result["formalization"], "NOT_INFERRED_FROM_REVIEW_APPROVAL")
		self.assertEqual(review.receive_review(self.Project, Dispatch["bundle"], Completion), Result)

	def test_inherited_or_undocumented_context_rejected(self):
		for Value in [True, None, 0]:
			Spawn = copy.deepcopy(self.Spawn)
			Spawn["arguments"]["fork_context"] = Value
			with self.assertRaises(ValueError):
				review.record_dispatch(self.Project, self.Project / self.Packet["packet"], Spawn)

	def test_author_cannot_be_reviewer(self):
		self.Spawn["result"]["agent_id"] = self.Author
		with self.assertRaises(ValueError):
			review.record_dispatch(self.Project, self.Project / self.Packet["packet"], self.Spawn)

	def test_prompt_contamination_and_wrong_agent_rejected(self):
		self.Spawn["arguments"]["message"] += " The author says everything is correct."
		with self.assertRaises(ValueError):
			review.record_dispatch(self.Project, self.Project / self.Packet["packet"], self.Spawn)
		with self.assertRaises(ValueError):
			review.completion_report(dict(status={self.Author: dict(completed=json.dumps(self.report()))}), self.Agent)

	def test_boolean_pass_and_no_return_are_not_review(self):
		for Data in [dict(status={self.Agent: dict(completed='{"pass":true}')}), dict(status={self.Agent: "running"})]:
			with self.assertRaises(ValueError):
				Result = review.completion_report(Data, self.Agent)
				review.check_report(library.read_json(self.Project / self.Packet["packet"]), self.Packet["packet_sha256"], Result)

	def test_approval_requires_all_obligations_and_inputs(self):
		for Key, Value in [("claim_results", []), ("checked_paths", ["proof.md"]), ("findings", ["missing domain condition"])]:
			Report = self.report()
			Report[Key] = Value
			with self.assertRaises(ValueError):
				review.check_report(library.read_json(self.Project / self.Packet["packet"]), self.Packet["packet_sha256"], Report)

	def test_negative_review_is_preserved_and_not_approved(self):
		Report = self.report()
		Report["verdict"] = "CHANGES_REQUIRED"
		Report["claim_results"][0]["verdict"] = "CHANGES_REQUIRED"
		Report["findings"] = ["domain definition is absent"]
		_, _, Result = self.complete(Report)
		self.assertEqual(Result["verdict"], "CHANGES_REQUIRED")

	def test_changed_proof_or_issue_invalidates_review(self):
		Dispatch, _, _ = self.complete()
		for Name in ["proof.md", "issue.json"]:
			PathValue = self.Project / Name
			Raw = PathValue.read_bytes()
			PathValue.write_bytes(Raw + b"new version")
			with self.assertRaises(ValueError):
				review.verify_review_bundle(self.Project, Dispatch["bundle"])
			PathValue.write_bytes(Raw)

	def test_snapshot_and_transcript_tampering_invalidates_review(self):
		Dispatch, _, _ = self.complete()
		Targets = [self.Project / self.Packet["packet"], self.Project / Dispatch["bundle"] / "spawn.json",
			self.Project / Dispatch["bundle"] / "report.json", self.Project / Dispatch["bundle"] / "completion.json"]
		for PathValue in Targets:
			Raw = PathValue.read_bytes()
			PathValue.write_bytes(Raw + b" ")
			with self.assertRaises(ValueError):
				review.verify_review_bundle(self.Project, Dispatch["bundle"])
			PathValue.write_bytes(Raw)
		Snapshot = (self.Project / self.Packet["packet"]).parent / "inputs/proof.md"
		Snapshot.write_text("changed snapshot")
		with self.assertRaises(ValueError):
			review.verify_review_bundle(self.Project, Dispatch["bundle"])

	def test_readback_packet_excludes_informal_roles_and_intent(self):
		Spec = copy.deepcopy(self.Spec)
		Spec["kind"] = "formal-readback"
		Spec["claims"] = [dict(id="terminal", declaration="SL.terminal_difference")]
		with self.assertRaises(ValueError):
			review.create_packet(self.Project, Spec)
		Spec["inputs"] = [dict(path="proof.md", role="formal-statement")]
		Packet = review.create_packet(self.Project, Spec)
		self.assertIn("formal-readback", (self.Project / Packet["packet"]).read_text())
		Spec["claims"][0]["statement"] = "What the author wants to prove"
		with self.assertRaises(ValueError):
			review.create_packet(self.Project, Spec)

	def test_missing_inputs_and_external_path_rejected(self):
		for Name in ["absent.md", "../outside.md"]:
			Spec = copy.deepcopy(self.Spec)
			Spec["inputs"] = [dict(path=Name, role="proof")]
			with self.assertRaises((ValueError, OSError)):
				review.create_packet(self.Project, Spec)


if(__name__ == "__main__"):
	unittest.main()
