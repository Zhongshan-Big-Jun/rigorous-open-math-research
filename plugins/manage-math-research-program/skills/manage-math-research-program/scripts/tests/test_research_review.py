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

	def modern_spawn(self):
		return dict(tool="collaboration.spawn_agent", arguments=dict(task_name="fresh_review", fork_turns="none", message=self.Packet["prompt"]), result=dict(task_name="/root/fresh_review"))

	def modern_completion(self):
		return dict(message_type="FINAL_ANSWER", task_name="/root", sender="/root/fresh_review", payload=json.dumps(self.report()))

	def test_canonical_task_adapter_preserves_native_identity_and_requires_final(self):
		Spawn = self.modern_spawn()
		Dispatch = review.record_dispatch(self.Project, self.Project / self.Packet["packet"], Spawn)
		self.assertEqual(Dispatch["reviewer_id"], "/root/fresh_review")
		self.assertNotIn("/root/", Dispatch["bundle"])
		with self.assertRaises((ValueError, OSError)):
			review.verify_review_bundle(self.Project, Dispatch["bundle"])
		Result = review.receive_review(self.Project, Dispatch["bundle"], self.modern_completion())
		self.assertEqual(Result["verdict"], "APPROVED")
		self.assertEqual(Result["reviewer_id"], "/root/fresh_review")

	def test_canonical_task_adapter_rejects_inheritance_forged_ids_and_no_return(self):
		for Field, Value in [("fork_turns", None), ("fork_turns", "all"), ("fork_turns", "0"), ("fork_context", False)]:
			Spawn = self.modern_spawn()
			Spawn["arguments"][Field] = Value
			with self.assertRaises(ValueError):
				review.record_dispatch(self.Project, self.Project / self.Packet["packet"], Spawn)
		for Agent in (self.Agent, "/root/other_review", "/root/../fresh_review", "/root/fresh_review/"):
			Spawn = self.modern_spawn()
			Spawn["result"]["task_name"] = Agent
			with self.assertRaises(ValueError):
				review.record_dispatch(self.Project, self.Project / self.Packet["packet"], Spawn)
		Spawn = self.modern_spawn()
		Spawn["result"]["agent_id"] = self.Agent
		with self.assertRaises(ValueError):
			review.record_dispatch(self.Project, self.Project / self.Packet["packet"], Spawn)
		for Field, Value in [("message_type", "MESSAGE"), ("sender", "/root/other_review"), ("task_name", "/root/other_parent"), ("payload", None)]:
			Completion = self.modern_completion()
			Completion[Field] = Value
			with self.assertRaises(ValueError):
				review.completion_report(Completion, "/root/fresh_review")
		with self.assertRaises(ValueError):
			review.completion_report(dict(status={"/root/fresh_review": dict(completed=json.dumps(self.report()))}), "/root/fresh_review")

	def test_canonical_author_cannot_verify_self(self):
		Packet = review.create_packet(self.Project, dict(self.Spec, author_ids=["/root/fresh_review"]))
		Spawn = self.modern_spawn()
		Spawn["arguments"]["message"] = Packet["prompt"]
		with self.assertRaises(ValueError):
			review.record_dispatch(self.Project, self.Project / Packet["packet"], Spawn)

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

	def malformed_packet(self, Mutate):
		Original = self.Project / self.Packet["packet"]
		Packet = library.read_json(Original)
		Mutate(Packet)
		Raw = library.json_bytes(Packet)
		Target = Original.parent.parent / library.digest(Raw) / "packet.json"
		for Name, Row in Packet["inputs"].items():
			library.immutable_write(Target.parent / Row["snapshot"], (self.Project / Name).read_bytes())
		library.immutable_write(Target, Raw)
		return Target

	def test_consumption_revalidates_complete_packet_schema(self):
		Mutations = [lambda P: P.update(claims=[]),
			lambda P: P["claims"].append(dict(P["claims"][0], statement="A distinct obligation")),
			lambda P: P.pop("author_ids"), lambda P: P.update(kind="unsupported"),
			lambda P: P["claims"][0].update(verification="assumed"),
			lambda P: P.update(kind="formal-readback"),
			lambda P: P.update(kind="formal-readback", claims=[dict(id="x", declaration="T")])]
		for Mutate in Mutations:
			with self.subTest(mutation=Mutate):
				Target = self.malformed_packet(Mutate)
				with self.assertRaises(ValueError):
					review.check_packet(self.Project, Target)

	def test_changed_packet_cannot_rebind_original_spawn(self):
		self.complete()
		PathValue = self.Project / self.Packet["packet"]
		Packet = library.read_json(PathValue)
		Packet["claims"][0]["statement"] = "A different theorem"
		PathValue.write_bytes(library.json_bytes(Packet))
		with self.assertRaises(ValueError):
			review.record_dispatch(self.Project, PathValue, self.Spawn)

	def test_new_packet_requires_new_reviewer_identity(self):
		self.complete()
		Spec = copy.deepcopy(self.Spec)
		Spec["claims"][0]["statement"] = "A different theorem"
		Packet = review.create_packet(self.Project, Spec)
		Spawn = copy.deepcopy(self.Spawn)
		Spawn["arguments"]["message"] = Packet["prompt"]
		with self.assertRaises((ValueError, FileExistsError)):
			review.record_dispatch(self.Project, self.Project / Packet["packet"], Spawn)
		Spawn["result"]["agent_id"] = "00000000-0000-0000-0000-000000000003"
		self.assertEqual(review.record_dispatch(self.Project, self.Project / Packet["packet"], Spawn)["state"], "AWAITING_REVIEW")

	def test_duplicate_json_keys_rejected_at_every_depth(self):
		for Text in ['{"verdict":"CHANGES_REQUIRED","verdict":"APPROVED"}',
			'{"claim_results":[{"verdict":"INCOMPLETE","verdict":"APPROVED"}]}',
			'{"findings":["gap"],"findings":[]}']:
			with self.assertRaises(ValueError):
				review.completion_report(dict(status={self.Agent: dict(completed=Text)}), self.Agent)

	def test_deleted_identity_record_invalidates_receipt(self):
		Dispatch, _, _ = self.complete()
		(review.review_root(self.Project) / "identities" / (self.Agent + ".json")).unlink()
		with self.assertRaises((ValueError, OSError)):
			review.verify_review_bundle(self.Project, Dispatch["bundle"])


if(__name__ == "__main__"):
	unittest.main()
