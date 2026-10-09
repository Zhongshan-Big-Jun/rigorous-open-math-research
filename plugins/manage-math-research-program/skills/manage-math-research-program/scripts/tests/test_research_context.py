#!/usr/bin/env python3
"""Behavior contracts in a non-SL project with a different physical layout."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import research_context as context
import research_corrections as corrections
import research_experience as experience
import research_library as library


class ContextTests(unittest.TestCase):
	def setUp(self):
		self.Temp = tempfile.TemporaryDirectory()
		self.Root = Path(self.Temp.name)
		(self.Root / "blueprint-project.json").write_bytes(library.json_bytes(dict(paths=dict(research_root="evidence/stack"))))
		(self.Root / "docs").mkdir()
		(self.Root / "docs/PROJECT_UNDERSTANDING.md").write_bytes(b"# A person's mathematics\r\nKeep this intuition exactly.\r\n")
		(self.Root / "basis.md").write_text("A fixed-time estimate does not supply a time-uniform estimate.\n", encoding="utf-8")
		self.Index = "cache/pointers.json"
		self.First = library.save_card(self.Root, dict(tool_id="semigroup-local", title="局部半群估计", content="# 局部半群估计\nA finite-time bound under dissipativity.\n",
			aliases=["semigroup estimate", "C0 半群"], problem_ids=["P-S"], objects=dict(scalar_field="real", dimension="finite"), parameter_scope=dict(time="fixed"),
			conditions=["Dissipativity on the stated domain.", "Time is fixed; the constants may depend on time."], missing_bridges=["A uniform resolvent bound is still needed."], sources=[dict(path="basis.md", locator="line 1", read_coverage="line 1 only")]), "instruments/local.md")
		self.Second = library.save_card(self.Root, dict(tool_id="other", title="另一估计", content="A semigroup discussion in complex infinite dimension.\n", conditions=["Compact resolvent is required."], objects=dict(scalar_field="complex", dimension="infinite")), "instruments/other.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		# The unchanged correction writer still rebuilds its legacy default index.
		# Both views are gated live; the custom view is never a correction authority.
		library.make_index(self.Root, ["instruments"])

	def tearDown(self):
		self.Temp.cleanup()

	def query(self, Query, **Args):
		return library.query_tools(self.Root, Query, self.Index, **Args)

	def package(self, **Args):
		return context.knowledge_package(self.Root, "半群 semigroup", IndexPath=self.Index, **Args)

	def quarantine(self):
		return corrections.register_issue(self.Root, dict(issue_id="lost-uniformity", origin="internal", reporter="fixture-author", summary="An assumed uniform bound was not established.", targets=[dict(path=self.First["location"], sha256=self.First["sha256"])], evidence=[dict(path="basis.md", locator="line 1")]))

	def test_relevance_context_and_full_conditions_do_not_prove_application(self):
		Result = self.query("semigroup", Context=dict(problem_ids=["P-S"], objects=dict(scalar_field="complex", dimension="infinite"), parameter_scope=dict(time="uniform")))
		First = Result["hits"][0]
		self.assertEqual(First["tool_id"], "semigroup-local")
		self.assertEqual(len(First["conditions"]), 2)
		self.assertFalse(First["applicability_check"]["implication_checked"])
		self.assertTrue(all(not Item["proved"] for Item in First["applicability_check"]["condition_mentions"]))
		self.assertEqual({Item["state"] for Item in First["applicability_check"]["scope_axes"]}, {"DIFFERENT_RECORDED_SCOPE_CHECK_BRIDGE"})
		self.assertTrue(self.query("C0 半群")["hits"])

	def test_changed_plain_body_regenerates_old_derived_summary(self):
		PathValue = self.Root / "instruments/plain.md"
		PathValue.write_text("# A\nobsolete-unconditional-marker\n", encoding="utf-8")
		library.make_index(self.Root, ["instruments"], self.Index)
		PathValue.write_text("# B\nOnly a conditional compact-domain result.\n", encoding="utf-8")
		library.make_index(self.Root, ["instruments"], self.Index)
		self.assertFalse(self.query("obsolete-unconditional-marker")["hits"])
		self.assertIn("conditional", self.query("compact-domain")["hits"][0]["summary"])

	def test_saved_and_external_body_updates_do_not_reuse_stale_explicit_claims(self):
		Saved = library.save_card(self.Root, dict(tool_id="old-metadata", title="Old", summary="obsolete-summary-token", aliases=["obsolete-alias-token"], conditions=["obsolete-condition-token"], content="# Before\nOld body.\n"), "instruments/metadata.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		Changed = library.save_card(self.Root, dict(content="# After\nNew conditional result.\n"), Saved["location"], Saved["sha256"])
		library.make_index(self.Root, ["instruments"], self.Index)
		self.assertFalse(self.query("obsolete-summary-token obsolete-alias-token obsolete-condition-token")["hits"])
		Row = library.read_card(self.Root, Changed["location"], IndexPath=self.Index)
		self.assertEqual(Row["field_provenance"]["conditions"]["state"], "INHERITED_NEEDS_REVALIDATION")
		self.assertEqual(Row["historical_metadata"]["summary"]["value"], "obsolete-summary-token")
		self.assertIn("New conditional", Row["summary"])
		# A second refresh cannot silently promote retained fields back to current.
		library.make_index(self.Root, ["instruments"], self.Index)
		self.assertFalse(self.query("obsolete-alias-token")["hits"])
		External = library.save_card(self.Root, dict(tool_id="external", summary="external-stale-token", content="Original body.\n"), "instruments/external.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		PathValue = self.Root / External["location"]
		PathValue.write_bytes(PathValue.read_bytes().replace(b"Original body.", b"Changed body."))
		library.make_index(self.Root, ["instruments"], self.Index)
		self.assertFalse(self.query("external-stale-token")["hits"])

	def test_unknown_dependencies_are_not_an_empty_complete_graph(self):
		Hit = self.query("semigroup", limit=1)["hits"][0]
		self.assertEqual(Hit["dependencies"], [])
		self.assertFalse(Hit["dependencies_known"])
		Package = self.package(Limit=1)
		self.assertEqual(Package["materials"][0]["dependency_coverage"], "UNKNOWN_NOT_EMPTY_CLOSURE")

	def test_typed_links_do_not_create_proof_dependencies(self):
		Relation = dict(kind="method_analogy", target=dict(path=self.Second["location"], sha256=self.Second["sha256"], role="card"), basis=dict(path="basis.md", locator="line 1"))
		library.save_card(self.Root, dict(content="A related comparison of semigroups.\n", relations=[Relation]), self.First["location"], self.First["sha256"])
		library.make_index(self.Root, ["instruments"], self.Index)
		Package = self.package(Depth=1)
		Relations = [Item for Material in Package["materials"] for Item in Material["relations"]]
		self.assertEqual(Relations[0]["kind"], "method_analogy")
		self.assertFalse(Relations[0]["impact_eligible"])

	def test_read_compare_understanding_context_and_export_honor_live_quarantine(self):
		One = experience.record_experience(self.Root, dict(tool_id="route-a", conclusion="A conditional approach.", outcome="partial", target="A semigroup bound", lost_information=["Uniform time control."], complementary_lemma=["Uniform resolvent control."]))
		Two = experience.record_experience(self.Root, dict(tool_id="route-b", conclusion="Needs compactness.", outcome="failed", failure_kind="missing_lemma"))
		Report = experience.compare_routes(self.Root, [One["location"], Two["location"]])
		self.assertTrue(Report["reuse_allowed"])
		self.assertEqual(Report["dimensions"]["lost_information"][0]["recorded"], ["Uniform time control."])
		corrections.register_issue(self.Root, dict(issue_id="route-error", origin="internal", reporter="fixture-author", summary="Missing uniform control.", targets=[dict(path=One["location"], sha256=One["sha256"])], evidence=[dict(path="basis.md", locator="line 1")]))
		with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
			experience.compare_routes(self.Root, [One["location"], Two["location"]])
		History = experience.compare_routes(self.Root, [One["location"], Two["location"]], IncludeAffected=True)
		self.assertEqual(History["status"], "HISTORY_ONLY_NOT_REUSE")
		self.assertFalse(experience.read_comparison(self.Root, Report["path"])["reuse_allowed"])
		Page = experience.update_understanding(self.Root, [One["location"], Two["location"]], [Report["path"]])
		self.assertEqual(Page["path"], "docs/PROJECT_UNDERSTANDING.md")
		self.assertEqual(Page["assembled_routes"], 1)
		self.assertNotIn("A conditional approach.", (self.Root / Page["path"]).read_text(encoding="utf-8"))
		OldPackage = self.package()
		self.quarantine()
		with self.assertRaises(ValueError):
			context.export_package(self.Root, OldPackage, "exports")
		with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
			library.read_card(self.Root, self.First["location"], IndexPath=self.Index)
		self.assertFalse(library.read_card(self.Root, self.First["location"], True, self.Index)["reuse_allowed"])
		Package = self.package(IncludeAffected=True)
		self.assertNotIn(self.First["location"], [Item["path"] for Item in Package["materials"]])
		self.assertTrue(Package["historical"])

	def test_corrupt_authoritative_store_fails_closed_even_in_history_views(self):
		self.quarantine()
		Marker = library.library_root(self.Root) / "corrections-required.json"
		Marker.write_bytes(b"{truncated")
		self.assertFalse(self.query("semigroup", IncludeAffected=True)["hits"])
		for Action in (lambda: library.read_card(self.Root, self.First["location"], True, self.Index), lambda: self.package(IncludeAffected=True), lambda: experience.update_understanding(self.Root, [])):
			with self.assertRaisesRegex(ValueError, "CORRECTIONS_INVALID"):
				Action()

	def test_missing_lean_evidence_never_becomes_green_and_default_does_not_execute(self):
		Saved = library.save_card(self.Root, dict(content="A formal semigroup reference.\n", lean=[dict(declaration="Operator.partial_lemma", source=dict(path="basis.md"), open_connections=["The complex-domain equivalence remains open."])]), "instruments/lean.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		with mock.patch.object(context.subprocess, "run") as Run:
			Package = self.package()
			Run.assert_not_called()
		Ref = next(Item for Material in Package["materials"] for Item in Material["lean"])
		self.assertEqual(Ref["exact_root"], "UNKNOWN_NOT_RECHECKED")
		self.assertEqual(context.recheck_lean_reference(self.Root, Ref, None)["exact_root"], "UNKNOWN")
		self.assertEqual(Ref["source"]["binding_state"], "CURRENT")
		self.assertNotEqual(Ref["trust"], "VERIFIED")

	def test_byte_current_receipt_for_a_different_declaration_cannot_pass(self):
		Proof = self.Root / "manifest.json"
		Proof.write_bytes(b"{}")
		Ref = dict(declaration="Operator.target", verification=dict(path="manifest.json", sha256=library.digest(Proof.read_bytes())))
		Tools = self.Root / "trusted-tools"
		Tools.mkdir()
		(Tools / "lean_evidence.py").write_text("# Test double, not genuine Lean evidence\n", encoding="utf-8")
		Response = mock.Mock(returncode=0, stdout=json.dumps(dict(declaration="Operator.other", snapshot_current=True, exact_root_passed=True)))
		with mock.patch.object(context.subprocess, "run", return_value=Response):
			State = context.recheck_lean_reference(self.Root, Ref, Tools)
		self.assertFalse(State["identity_matches"])
		self.assertEqual(State["exact_root"], "NOT_ESTABLISHED")

	def test_exports_are_idempotent_bounded_and_do_not_execute_source_instructions(self):
		Package = self.package(MaxChars=4000)
		self.assertTrue(Package["follow_up"])
		self.assertTrue(all(Item["conditions"] for Item in Package["materials"]))
		First = context.export_package(self.Root, Package, "exports")
		Before = (self.Root / First["export"]).read_bytes()
		Again = context.export_package(self.Root, Package, "exports")
		self.assertEqual((self.Root / Again["export"]).read_bytes(), Before)
		self.assertEqual(self.package(MaxChars=4000)["view_sha256"], Package["view_sha256"])
		self.assertFalse(Package["canonical_modified"])
		self.assertFalse(Package["workflow_state_modified"])

	def test_understanding_preserves_human_edits_and_rejects_concurrent_write(self):
		Route = experience.record_experience(self.Root, dict(conclusion="The compactness bridge is missing.", outcome="partial"))
		PathValue = self.Root / "docs/PROJECT_UNDERSTANDING.md"
		Before = PathValue.read_bytes()
		Original = experience.read_route
		def race(*Args, **Keywords):
			Row = Original(*Args, **Keywords)
			PathValue.write_bytes(Before + b"A new human mathematical objection.\n")
			return Row
		with mock.patch.object(experience, "read_route", side_effect=race):
			with self.assertRaisesRegex(ValueError, "concurrently"):
				experience.update_understanding(self.Root, [Route["location"]])
		self.assertEqual(PathValue.read_bytes(), Before + b"A new human mathematical objection.\n")
		experience.update_understanding(self.Root, [Route["location"]])
		self.assertTrue(PathValue.read_bytes().startswith(Before))
		After = PathValue.read_bytes()
		self.assertTrue(experience.update_understanding(self.Root, [Route["location"]])["reused"])
		self.assertEqual(PathValue.read_bytes(), After)

	def test_corrupt_index_is_diagnosed_without_rewriting_it_or_versions(self):
		Index = self.Root / self.Index
		Before = {PathValue.name: PathValue.read_bytes() for PathValue in (library.library_root(self.Root) / "card-versions").iterdir()}
		Index.write_bytes(b"{interrupted")
		with self.assertRaises(ValueError):
			self.package()
		self.assertEqual(Index.read_bytes(), b"{interrupted")
		self.assertEqual(Before, {PathValue.name: PathValue.read_bytes() for PathValue in (library.library_root(self.Root) / "card-versions").iterdir()})

	def test_cooperative_lock_contention_is_explicit_and_does_not_change_inputs(self):
		Before = (self.Root / self.Index).read_bytes()
		with library.writer_lock(library.library_root(self.Root)):
			with self.assertRaises(FileExistsError):
				self.package()
		self.assertEqual((self.Root / self.Index).read_bytes(), Before)
		self.assertTrue(self.package()["materials"])

	def test_short_names_do_not_match_inside_unrelated_words(self):
		self.assertFalse(context.term_match("nd", "boundary and boundedness"))
		self.assertTrue(context.term_match("nd", "ND/G1".casefold()))
		self.assertTrue(context.term_match("riesz", "riesz替代系"))

	def test_explicit_replacement_can_be_found_from_history_without_releasing_it(self):
		self.quarantine()
		Replacement = library.save_card(self.Root, dict(tool_id="replacement-local", title="A correctly scoped replacement", content="A local estimate with its own hypotheses.\n", conditions=["Fixed time only."], relations=[dict(kind="replacement", target=dict(path=self.First["location"], sha256=self.First["sha256"], role="card"), basis=dict(path="basis.md", locator="line 1"))]), "instruments/replacement.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		Package = context.knowledge_package(self.Root, "semigroup-local", IndexPath=self.Index, Limit=1, Depth=1, IncludeAffected=True)
		self.assertEqual(Package["historical"][0]["path"], self.First["location"])
		self.assertIn(Replacement["location"], [Item["path"] for Item in Package["materials"]])
		self.assertFalse(library.read_card(self.Root, self.First["location"], True, self.Index)["reuse_allowed"])

	def test_quarantined_reference_remains_history_even_when_its_bytes_match(self):
		self.quarantine()
		Refs = library.reference_states(self.Root, [dict(path=self.First["location"], sha256=self.First["sha256"])])
		self.assertEqual(Refs[0]["binding_state"], "CURRENT")
		self.assertFalse(Refs[0]["reference_reuse_allowed"])
		self.assertEqual(Refs[0]["trust"], "HISTORY_ONLY_NOT_REUSE")

	def test_producer_change_prevents_export_without_rewriting_saved_knowledge(self):
		Package = self.package()
		Original = context.producer_identity
		with mock.patch.object(context, "producer_identity", side_effect=lambda: dict(Original(), version="changed")):
			with self.assertRaisesRegex(ValueError, "producer changed"):
				context.export_package(self.Root, Package, "exports")
		self.assertFalse((self.Root / "exports").exists())

	def test_body_edit_does_not_erase_retirement_or_reassert_old_experience(self):
		Retired = library.save_card(self.Root, dict(content="A retired historical method.\n", applicability=[dict(status="retired")]), "instruments/retired.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		library.save_card(self.Root, dict(content="A revised description of this method.\n"), Retired["location"], Retired["sha256"])
		library.make_index(self.Root, ["instruments"], self.Index)
		self.assertFalse(self.query("revised description")["hits"])
		self.assertEqual(self.query("revised description", IncludeArchived=True)["hits"][0]["lifecycle"], "archived")
		Route = experience.record_experience(self.Root, dict(tool_id="former-counterexample", conclusion="A recorded counterexample.", outcome="failed", failure_kind="counterexample"))
		library.save_card(self.Root, dict(content="# Revised route\nThe former explanation needs reconsideration.\n"), Route["location"], Route["sha256"])
		Current = experience.read_route(self.Root, Route["location"])
		self.assertEqual(Current["experience"], {})
		self.assertEqual(Current["evidence_status"], "UNKNOWN")

	def test_candidate_evidence_cannot_launder_a_quarantined_card(self):
		One = experience.record_experience(self.Root, dict(conclusion="A first scoped route.", outcome="partial"))
		Two = experience.record_experience(self.Root, dict(conclusion="A second scoped route.", outcome="partial"))
		Hypothesis = dict(explanation="A specific candidate explanation.", scope="Fixed-time estimates only.", prediction="A resolvent bridge suffices.", test="Check a time-uniform counterexample.", evidence=[dict(path=self.First["location"], locator="body")])
		Report = experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis)
		self.quarantine()
		Current = experience.read_comparison(self.Root, Report["path"])
		self.assertFalse(Current["reuse_allowed"])
		self.assertFalse(Current["hypotheses"][0]["reuse_allowed"])
		with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
			experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis)
		History = experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis, IncludeAffected=True)
		self.assertFalse(History["reuse_allowed"])
		Page = experience.update_understanding(self.Root, [One["location"], Two["location"]], [Report["path"]])
		self.assertNotIn(Hypothesis["explanation"], (self.Root / Page["path"]).read_text(encoding="utf-8"))

	def test_new_annotation_invalidates_export_without_a_new_index(self):
		Package = self.package()
		library.annotate(self.Root, self.First["location"], text="A newly recorded missing bridge.", author="reader")
		with self.assertRaisesRegex(ValueError, "annotations changed"):
			context.export_package(self.Root, Package, "exports")
		New = self.package()
		self.assertNotEqual(New["view_sha256"], Package["view_sha256"])
		self.assertTrue(New["annotation_basis"])

	def test_captured_source_bytes_and_coverage_are_part_of_export_identity(self):
		Captured = library.capture_source(self.Root, self.Root / "basis.md", "https://example.org/scoped-source", "revision-2", "Scoped estimate", Coverage="One supplied paragraph.", Locators=["Theorem 2"])
		library.save_card(self.Root, dict(content="A captured source for a semigroup estimate.\n", sources=[dict(source_id=Captured["source_id"], locator="Theorem 2", read_coverage="One paragraph only.")]), "instruments/captured.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		Package = context.knowledge_package(self.Root, "captured", IndexPath=self.Index, Limit=1)
		Ref = Package["materials"][0]["sources"][0]
		self.assertEqual(Ref["captured_source"]["version"], "revision-2")
		self.assertEqual(Ref["read_coverage"], "One paragraph only.")
		PathValue = library.library_root(self.Root) / "sources" / Captured["source_id"] / "text.txt"
		PathValue.write_text("Changed extraction.\n", encoding="utf-8")
		with self.assertRaisesRegex(ValueError, "inputs changed"):
			context.export_package(self.Root, Package, "exports")

	def test_bad_optional_provenance_isolated_without_hiding_healthy_cards(self):
		(self.Root / "instruments/bad.md").write_text('---\n{"_field_provenance":{"summary":"malformed"}}\n---\nsemigroup\n', encoding="utf-8")
		library.make_index(self.Root, ["instruments"], self.Index)
		Hits = self.query("semigroup")["hits"]
		self.assertTrue(Hits)
		self.assertNotIn("instruments/bad.md", [Hit["location"] for Hit in Hits])
		with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
			library.read_card(self.Root, "instruments/bad.md", IndexPath=self.Index)

	def test_inherited_conditions_cannot_supply_a_context_only_match(self):
		Saved = library.save_card(self.Root, dict(content="An old analytical estimate.\n", conditions=["uniform resolvent bound"]), "instruments/revised.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		library.save_card(self.Root, dict(content="An unrelated local algebraic identity.\n"), Saved["location"], Saved["sha256"])
		library.make_index(self.Root, ["instruments"], self.Index)
		Args = dict(Context=dict(conditions=["uniform resolvent bound"]))
		self.assertFalse(self.query("never-occurring-token", **Args)["hits"])
		Package = context.knowledge_package(self.Root, "never-occurring-token", IndexPath=self.Index, **Args)
		self.assertFalse(Package["materials"])
		Read = library.read_card(self.Root, Saved["location"], IndexPath=self.Index)
		self.assertEqual(Read["conditions"], ["uniform resolvent bound"])
		self.assertEqual(Read["field_provenance"]["conditions"]["state"], "INHERITED_NEEDS_REVALIDATION")

	def test_equivalent_reference_paths_and_legacy_comparison_keep_quarantine(self):
		One = experience.record_experience(self.Root, dict(conclusion="A healthy first route."))
		Two = experience.record_experience(self.Root, dict(conclusion="A healthy second route."))
		Report = experience.compare_routes(self.Root, [One["location"], Two["location"]], dict(explanation="A legacy candidate using rejected evidence.", scope="Recorded scope.", prediction="Recorded prediction.", test="Recorded test.", evidence=[dict(path=self.First["location"], locator="body")]))
		Legacy = {Key: Value for Key, Value in Report.items() if Key not in ("path", "sha256")}
		# A schema-2 legacy comparison may retain a caller's equivalent path spelling.
		Legacy["hypotheses"][0]["evidence"][0]["path"] = "./" + self.First["location"]
		Raw = library.json_bytes(Legacy)
		LegacyPath = library.library_root(self.Root) / "comparisons" / (library.digest(Raw) + ".json")
		library.immutable_write(LegacyPath, Raw)
		self.quarantine()
		for Location in ("./" + self.First["location"], "instruments/../" + self.First["location"], str(self.Root / self.First["location"])):
			Ref = library.reference_states(self.Root, [dict(path=Location, sha256=self.First["sha256"])])[0]
			self.assertEqual(Ref["path"], self.First["location"])
			self.assertFalse(Ref["reference_reuse_allowed"])
		Current = experience.read_comparison(self.Root, library.relative(self.Root, LegacyPath))
		self.assertFalse(Current["reuse_allowed"])
		Page = experience.update_understanding(self.Root, [One["location"], Two["location"]], [library.relative(self.Root, LegacyPath)])
		self.assertNotIn(Legacy["hypotheses"][0]["explanation"], (self.Root / Page["path"]).read_text(encoding="utf-8"))

	def test_relation_basis_or_noncard_target_quarantine_blocks_current_reuse(self):
		self.quarantine()
		for BlockedRole in ("basis", "target"):
			Target = self.Second if BlockedRole == "basis" else self.First
			Basis = self.First if BlockedRole == "basis" else self.Second
			Needle = "relation-" + BlockedRole + "-probe"
			Relation = dict(kind="mathematical_dependency", target=dict(path=Target["location"], sha256=Target["sha256"], role="source"), basis=dict(path=Basis["location"], sha256=Basis["sha256"], locator="body"))
			Dependencies = [dict(location=Target["location"], sha256=Target["sha256"])] if BlockedRole == "basis" else []
			Saved = library.save_card(self.Root, dict(content=Needle + "\n", relations=[Relation], dependencies=Dependencies), "instruments/" + Needle + ".md")
			library.make_index(self.Root, ["instruments"], self.Index)
			Package = context.knowledge_package(self.Root, Needle, IndexPath=self.Index, Limit=1)
			View = Package["materials"][0]["relations"][0]
			self.assertTrue(View["binding_current"])
			self.assertFalse(View[BlockedRole]["reference_reuse_allowed"])
			self.assertFalse(View["reuse_allowed"])
			self.assertFalse(View["impact_eligible"])
			Exported = context.export_package(self.Root, Package, "exports")
			self.assertFalse(Exported["materials"][0]["relations"][0]["reuse_allowed"])

	def test_broad_context_does_not_bury_a_lexically_relevant_material(self):
		Relevant = library.save_card(self.Root, dict(title="exact-route-keyword", content="An exact-route-keyword for a specific question.\n"), "instruments/relevant.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		Result = self.query("exact-route-keyword", Context=dict(problem_ids=["P-S"]))
		self.assertEqual(Result["hits"][0]["location"], Relevant["location"])
		ContextOnly = next(Hit for Hit in Result["hits"] if Hit["tool_id"] == "semigroup-local")
		self.assertTrue(ContextOnly["relevance_reasons"][0]["context_only"])

	def test_body_only_match_survives_many_context_suggestions_and_limit_one(self):
		Relevant = library.save_card(self.Root, dict(title="A specific lemma", content="The rarelemma statement is useful here.\n", conditions=["The parameter is fixed.", "The stated domain is required."]), "instruments/specific.md")
		Fields = dict(problem_ids=["P-model", "P-S"], objects=dict(scalar_field="real", dimension="finite"), conditions=["Dissipativity"], parameter_scope=dict(time="fixed"), tool_types=["estimate"])
		for Number in range(4):
			library.save_card(self.Root, dict(title="A broad catalogue", content="An algebraic side discussion.\n", **Fields), "instruments/side-" + str(Number) + ".md")
		library.make_index(self.Root, ["instruments"], self.Index)
		Result = self.query("rarelemma", Context=Fields)
		self.assertEqual(Result["hits"][0]["location"], Relevant["location"])
		self.assertTrue(Result["hits"][0]["lexical_match"])
		Suggestions = [Hit for Hit in Result["hits"] if Hit["match_kind"] == "CONTEXT_SUGGESTION"]
		self.assertGreater(len(Suggestions), 1)
		self.assertGreater(Suggestions[0]["score"], Result["hits"][0]["score"])
		self.assertEqual(self.query("rarelemma", Context=Fields, limit=1)["hits"][0]["location"], Relevant["location"])
		Package = context.knowledge_package(self.Root, "rarelemma", Context=Fields, IndexPath=self.Index, Limit=1)
		self.assertEqual(Package["reading_order"], [Relevant["location"]])
		self.assertEqual(Package["materials"][0]["conditions"], ["The parameter is fixed.", "The stated domain is required."])
		self.assertEqual(Package["materials"][0]["match_kind"], "QUERY_TEXT")
		GoalContext = dict(Fields, goal="algebraic")
		self.assertEqual(self.query("rarelemma", Context=GoalContext, limit=1)["hits"][0]["location"], Relevant["location"])
		self.assertEqual(context.knowledge_package(self.Root, "rarelemma", Context=GoalContext, IndexPath=self.Index, Limit=1)["reading_order"], [Relevant["location"]])
		# An absent lexical match can still supply explicitly labelled suggestions.
		OnlyContext = context.knowledge_package(self.Root, "absent-query-token", Context=Fields, IndexPath=self.Index, Limit=1)
		self.assertEqual(OnlyContext["materials"][0]["match_kind"], "CONTEXT_SUGGESTION")

	def test_real_warm_source_change_rejects_generation_and_export(self):
		Plugin = Path(context.__file__).resolve().parents[3]
		Clone = self.Root / "runtime-clone"
		shutil.copytree(Plugin, Clone, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
		Scripts = Clone / "skills/manage-math-research-program/scripts"
		Code = """
import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import research_context as context
project=Path(sys.argv[2])
args=dict(Query='semigroup',IndexPath='cache/pointers.json')
package=context.knowledge_package(project,**args)
source=Path(context.__file__)
loaded=package['producer']['script_hashes']['research_context.py']
source.write_text(source.read_text(encoding='utf-8').replace('return Score, Reasons','return 0, []'),encoding='utf-8')
result=dict(initial_materials=len(package['materials']),loaded_sha256=loaded,disk_sha256=context.library.file_digest(source))
for name,action in [('generate',lambda:context.knowledge_package(project,**args)),('export',lambda:context.export_package(project,package,'warm-exports'))]:
    try: action();result[name]='incorrectly allowed'
    except ValueError as error: result[name]=str(error)
print(json.dumps(result))
"""
		Options = dict(capture_output=True, text=True, encoding="utf-8", timeout=45, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
		Warm = subprocess.run([sys.executable, "-B", "-X", "utf8", "-c", Code, str(Scripts), str(self.Root)], **Options)
		self.assertEqual(Warm.returncode, 0, Warm.stderr)
		Result = json.loads(Warm.stdout)
		self.assertGreater(Result["initial_materials"], 0)
		self.assertNotEqual(Result["loaded_sha256"], Result["disk_sha256"])
		for Name in ("generate", "export"):
			self.assertIn("new Python process", Result[Name])
		self.assertFalse((self.Root / "warm-exports").exists())
		ColdCode = "import json,sys;sys.path.insert(0,sys.argv[1]);import research_context as c;p=c.knowledge_package(sys.argv[2],'semigroup',IndexPath='cache/pointers.json');print(json.dumps(dict(materials=len(p['materials']),sha256=p['producer']['script_hashes']['research_context.py'])))"
		Cold = subprocess.run([sys.executable, "-B", "-X", "utf8", "-c", ColdCode, str(Scripts), str(self.Root)], **Options)
		self.assertEqual(Cold.returncode, 0, Cold.stderr)
		Reloaded = json.loads(Cold.stdout)
		self.assertEqual(Reloaded["materials"], 0)
		self.assertEqual(Reloaded["sha256"], Result["disk_sha256"])

	def test_captured_source_members_gate_comparison_relations_and_export(self):
		One = experience.record_experience(self.Root, dict(conclusion="A healthy first method.", outcome="partial"))
		Two = experience.record_experience(self.Root, dict(conclusion="A healthy second method.", outcome="partial"))
		for Number, MemberName in enumerate(("source.json", "raw.bin", "text.txt")):
			with self.subTest(member=MemberName):
				Input = self.Root / ("capture-input-" + str(Number) + ".txt")
				Input.write_text("A distinct scoped estimate " + str(Number) + ".\n", encoding="utf-8")
				Captured = library.capture_source(self.Root, Input, "https://example.org/member-" + str(Number), "revision-1", "A scoped source", Coverage="One paragraph.")
				SourceRef = dict(source_id=Captured["source_id"], locator="paragraph 1", read_coverage="One supplied paragraph.")
				Folder = library.library_root(self.Root) / "sources" / Captured["source_id"]
				Original = {Name: (Folder / Name).read_bytes() for Name in ("source.json", "raw.bin", "text.txt")}
				Hypothesis = dict(explanation="A source-backed candidate " + str(Number), scope="Fixed time only.", prediction="The stated bridge suffices.", test="Check a uniform-time counterexample.", evidence=[SourceRef])
				OldComparison = experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis)
				Needle = "capture-probe-" + str(Number)
				Relation = dict(kind="mathematical_dependency", target=dict(path=self.Second["location"], sha256=self.Second["sha256"], role="card"), basis=SourceRef)
				Saved = library.save_card(self.Root, dict(content=Needle + "\n", conditions=["Fixed time only."], sources=[SourceRef], relations=[Relation], dependencies=[dict(location=self.Second["location"], sha256=self.Second["sha256"])]), "instruments/capture-" + str(Number) + ".md")
				library.make_index(self.Root, ["instruments"], self.Index)
				OldPackage = context.knowledge_package(self.Root, Needle, IndexPath=self.Index, Limit=1, Depth=0)
				self.assertTrue(OldPackage["materials"][0]["relations"][0]["impact_eligible"])
				OldExport = context.export_package(self.Root, OldPackage, "exports")
				ExportBytes = (self.Root / OldExport["export"]).read_bytes()
				Target = dict(path=library.relative(self.Root, Folder / MemberName), sha256=library.file_digest(Folder / MemberName))
				corrections.register_issue(self.Root, dict(issue_id="capture-member-" + str(Number), origin="internal", reporter="fixture-author", summary="The captured statement is not reusable.", targets=[Target], evidence=[dict(path="basis.md", locator="paragraph 1")]))
				State = library.reference_states(self.Root, [SourceRef])[0]
				self.assertEqual(State["binding_state"], "CURRENT")
				self.assertFalse(State["reference_reuse_allowed"])
				self.assertEqual(len(State["capture_members"]), 3)
				self.assertFalse(next(Member for Member in State["capture_members"] if Member["path"] == Target["path"])["reference_reuse_allowed"])
				with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
					experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis)
				self.assertFalse(experience.read_comparison(self.Root, OldComparison["path"])["reuse_allowed"])
				History = experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis, IncludeAffected=True)
				self.assertEqual(History["status"], "HISTORY_ONLY_NOT_REUSE")
				Page = experience.update_understanding(self.Root, [One["location"], Two["location"]], [OldComparison["path"]])
				self.assertNotIn(Hypothesis["explanation"], (self.Root / Page["path"]).read_text(encoding="utf-8"))
				with self.assertRaises(ValueError):
					context.export_package(self.Root, OldPackage, "exports")
				self.assertEqual((self.Root / OldExport["export"]).read_bytes(), ExportBytes)
				Current = context.knowledge_package(self.Root, Needle, IndexPath=self.Index, Limit=1, Depth=0)
				View = next(Material for Material in Current["materials"] if Material["path"] == Saved["location"])["relations"][0]
				self.assertFalse(View["reuse_allowed"])
				self.assertFalse(View["impact_eligible"])
				self.assertFalse(context.export_package(self.Root, Current, "exports")["materials"][0]["relations"][0]["reuse_allowed"])
				self.assertEqual(Original, {Name: (Folder / Name).read_bytes() for Name in Original})
				if(MemberName != "source.json"):
					Alias = library.capture_source(self.Root, Input, "https://example.org/alias-" + str(Number), "revision-2", "A different capture identity")
					self.assertNotEqual(Alias["source_id"], Captured["source_id"])
					self.assertFalse(library.reference_states(self.Root, [dict(source_id=Alias["source_id"])])[0]["reference_reuse_allowed"])

	def test_capture_title_alias_retains_registered_metadata_obligations(self):
		Input = self.Root / "title-alias-input.txt"
		Input.write_text("A captured local estimate with a missing uniform bridge.\n", encoding="utf-8")
		Original = library.capture_source(self.Root, Input, "https://example.org/exact-source", "revision-1", "Original title", Coverage="One paragraph.", Locators=["Theorem 2"])
		Alias = library.capture_source(self.Root, Input, Original["url"], Original["version"], "A new title", Coverage=Original["coverage"], Locators=Original["original_locators"])
		self.assertNotEqual(Original["source_id"], Alias["source_id"])
		self.assertEqual(Original["raw_sha256"], Alias["raw_sha256"])
		self.assertEqual(Original["text_sha256"], Alias["text_sha256"])
		Ref = dict(source_id=Alias["source_id"], locator="Theorem 2", read_coverage="One paragraph only.")
		One = experience.record_experience(self.Root, dict(conclusion="A local method.", outcome="partial"))
		Two = experience.record_experience(self.Root, dict(conclusion="A complementary method.", outcome="partial"))
		Hypothesis = dict(explanation="title-alias-candidate", scope="Fixed time only.", prediction="A uniform bridge suffices.", test="Check a uniform-time counterexample.", evidence=[Ref])
		Comparison = experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis)
		Relation = dict(kind="mathematical_dependency", target=dict(path=self.Second["location"], sha256=self.Second["sha256"], role="card"), basis=Ref)
		Saved = library.save_card(self.Root, dict(content="title-alias-needle\n", sources=[Ref], relations=[Relation], dependencies=[dict(location=self.Second["location"], sha256=self.Second["sha256"])]), "instruments/title-alias.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		OldPackage = context.knowledge_package(self.Root, "title-alias-needle", IndexPath=self.Index, Limit=1, Depth=0)
		OldExport = context.export_package(self.Root, OldPackage, "exports")
		OldBytes = (self.Root / OldExport["export"]).read_bytes()
		OriginalPath = self.Root / Original["source"]
		OriginalBytes = OriginalPath.read_bytes()
		corrections.register_issue(self.Root, dict(issue_id="captured-metadata-title-alias", origin="internal", reporter="fixture-author", summary="The source statement needs correction.", targets=[dict(path=Original["source"], sha256=library.digest(OriginalBytes))], evidence=[dict(path="basis.md", locator="line 1")]))
		AliasPath = self.Root / Alias["source"]
		PathRef = dict(path=Alias["source"].replace("/sources/", "/sources/./"), sha256=library.file_digest(AliasPath))
		for Reference in (Ref, PathRef):
			with self.subTest(reference=Reference):
				State = library.reference_states(self.Root, [Reference])[0]
				self.assertEqual(State["binding_state"], "CURRENT")
				self.assertFalse(State["reference_reuse_allowed"])
				self.assertEqual(State["captured_source"]["title"], "A new title")
				self.assertIn(Original["source"], [Row["path"] for Row in State["capture_aliases"]])
				with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
					experience.compare_routes(self.Root, [One["location"], Two["location"]], dict(Hypothesis, evidence=[Reference]))
		self.assertFalse(experience.read_comparison(self.Root, Comparison["path"])["reuse_allowed"])
		self.assertEqual(experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis, IncludeAffected=True)["status"], "HISTORY_ONLY_NOT_REUSE")
		Page = experience.update_understanding(self.Root, [One["location"], Two["location"]], [Comparison["path"]])
		self.assertNotIn(Hypothesis["explanation"], (self.Root / Page["path"]).read_text(encoding="utf-8"))
		with self.assertRaises(ValueError):
			context.export_package(self.Root, OldPackage, "exports")
		self.assertEqual((self.Root / OldExport["export"]).read_bytes(), OldBytes)
		Current = context.knowledge_package(self.Root, "title-alias-needle", IndexPath=self.Index, Limit=1, Depth=0)
		Material = next(Item for Item in Current["materials"] if Item["path"] == Saved["location"])
		self.assertFalse(Material["relations"][0]["reuse_allowed"])
		self.assertFalse(Material["relations"][0]["impact_eligible"])
		self.assertFalse(context.export_package(self.Root, Current, "exports")["materials"][0]["relations"][0]["reuse_allowed"])
		for Url, Version in (("https://example.org/different-source", Original["version"]), (Original["url"], "revision-2")):
			Separate = library.capture_source(self.Root, Input, Url, Version, "A separately versioned capture")
			self.assertTrue(library.reference_states(self.Root, [dict(source_id=Separate["source_id"])])[0]["reference_reuse_allowed"])
		self.assertEqual(OriginalPath.read_bytes(), OriginalBytes)
		# A missing old live capture cannot erase its registered version snapshot.
		OriginalPath.unlink()
		self.assertFalse(library.reference_states(self.Root, [Ref])[0]["reference_reuse_allowed"])
		AfterRemoval = context.knowledge_package(self.Root, "title-alias-needle", IndexPath=self.Index, Limit=1, Depth=0)
		self.assertFalse(context.export_package(self.Root, AfterRemoval, "exports")["materials"][0]["relations"][0]["reuse_allowed"])

	def test_dual_capture_selectors_gate_all_members_and_reject_disagreement(self):
		Input = self.Root / "dual-selector-input.txt"
		Input.write_text("A local capture used by two different selectors.\n", encoding="utf-8")
		Original = library.capture_source(self.Root, Input, "https://example.org/dual-source", "revision-1", "Original title")
		Alias = library.capture_source(self.Root, Input, Original["url"], Original["version"], "Another title")
		One = experience.record_experience(self.Root, dict(conclusion="A pointwise method.", outcome="partial"))
		Two = experience.record_experience(self.Root, dict(conclusion="A complementary method.", outcome="partial"))
		Probes = []
		for Capture in (Original, Alias):
			for Name in ("source.json", "raw.bin", "text.txt"):
				for UseSourceId in (True, False):
					Location = Capture["source"].replace("source.json", Name)
					Ref = dict(path="./" + Location, sha256=library.file_digest(self.Root / Location), locator="line 1")
					if(UseSourceId):
						Ref["source_id"] = Capture["source_id"]
					self.assertTrue(library.reference_states(self.Root, [Ref])[0]["reference_reuse_allowed"])
					Number = str(len(Probes))
					Hypothesis = dict(explanation="dual-selector-candidate-" + Number, scope="Fixed time only.", prediction="A bridge suffices.", test="Check a uniform-time counterexample.", evidence=[Ref])
					Comparison = experience.compare_routes(self.Root, [One["location"], Two["location"]], Hypothesis)
					Relation = dict(kind="mathematical_dependency", target=dict(path=self.Second["location"], sha256=self.Second["sha256"], role="card"), basis=Ref)
					Saved = library.save_card(self.Root, dict(content="dual-selector-needle-" + Number + "\n", sources=[Ref], relations=[Relation], dependencies=[dict(location=self.Second["location"], sha256=self.Second["sha256"])]), "instruments/dual-selector-" + Number + ".md")
					Probes.append(dict(reference=Ref, hypothesis=Hypothesis, comparison=Comparison, card=Saved))
		library.make_index(self.Root, ["instruments"], self.Index)
		for Number, Probe in enumerate(Probes):
			Package = context.knowledge_package(self.Root, "dual-selector-needle-" + str(Number), IndexPath=self.Index, Limit=1, Depth=0)
			Export = context.export_package(self.Root, Package, "exports")
			self.assertTrue(Export["materials"][0]["relations"][0]["impact_eligible"])
			Probe.update(package=Package, export=Export, export_bytes=(self.Root / Export["export"]).read_bytes())
		corrections.register_issue(self.Root, dict(issue_id="dual-selector-source-metadata", origin="internal", reporter="fixture-author", summary="The capture is not reusable.", targets=[dict(path=Original["source"], sha256=library.file_digest(self.Root / Original["source"]))], evidence=[dict(path="basis.md", locator="line 1")]))
		for Probe in Probes:
			with self.subTest(reference=Probe["reference"]):
				State = library.reference_states(self.Root, [Probe["reference"]])[0]
				self.assertEqual(State["binding_state"], "CURRENT")
				self.assertFalse(State["reference_reuse_allowed"])
				self.assertEqual(len(State["capture_members"]), 3)
				with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
					experience.compare_routes(self.Root, [One["location"], Two["location"]], Probe["hypothesis"])
				self.assertFalse(experience.read_comparison(self.Root, Probe["comparison"]["path"])["reuse_allowed"])
				Page = experience.update_understanding(self.Root, [One["location"], Two["location"]], [Probe["comparison"]["path"]])
				self.assertNotIn(Probe["hypothesis"]["explanation"], (self.Root / Page["path"]).read_text(encoding="utf-8"))
				with self.assertRaises(ValueError):
					context.export_package(self.Root, Probe["package"], "exports")
				self.assertEqual((self.Root / Probe["export"]["export"]).read_bytes(), Probe["export_bytes"])
				Current = context.knowledge_package(self.Root, "dual-selector-needle-" + str(Probes.index(Probe)), IndexPath=self.Index, Limit=1, Depth=0)
				View = context.export_package(self.Root, Current, "exports")["materials"][0]["relations"][0]
				self.assertFalse(View["reuse_allowed"])
				self.assertFalse(View["impact_eligible"])
		for PathValue in ("basis.md", Alias["source"].replace("source.json", "text.txt")):
			Mismatch = dict(path=PathValue, sha256=library.file_digest(self.Root / PathValue), source_id=Original["source_id"])
			with self.assertRaisesRegex(ValueError, "path and source_id"):
				library.bind_references(self.Root, [Mismatch])
			self.assertEqual(library.reference_states(self.Root, [Mismatch])[0]["binding_state"], "INVALID")
		WrongHash = dict(Probes[0]["reference"], sha256="0" * 64)
		self.assertEqual(library.reference_states(self.Root, [WrongHash])[0]["binding_state"], "STALE_OR_UNBOUND")

	def test_registered_capture_metadata_keeps_distinct_sources_and_dependencies(self):
		Input = self.Root / "registered-capture-input.txt"
		Input.write_text("The same extraction can come from distinct source versions.\n", encoding="utf-8")
		Original = library.capture_source(self.Root, Input, "https://example.org/registered-source", "revision-1", "Original title")
		Alias = library.capture_source(self.Root, Input, Original["url"], Original["version"], "Another title")
		Distinct = [library.capture_source(self.Root, Input, "https://example.org/independent-source", Original["version"], "Independent source"), library.capture_source(self.Root, Input, Original["url"], "revision-2", "Different version")]
		Genuine = library.save_card(self.Root, dict(tool_id="source", content="An unrelated tool with an explicit declared identity.\n"), "instruments/genuine-source-tool.md")
		corrections.register_issue(self.Root, dict(issue_id="registered-capture-metadata", origin="internal", reporter="fixture-author", summary="Only this captured metadata is affected.", targets=[dict(path=Original["source"], sha256=library.file_digest(self.Root / Original["source"]))], evidence=[dict(path="basis.md", locator="line 1")]))
		Catalog = library.library_root(self.Root) / "card-bindings/catalog.json"
		OldNames = library.read_json(Catalog)["records"]
		OldRecords = {Name: (Catalog.parent / (Name + ".json")).read_bytes() for Name in OldNames}
		for Number, Capture in enumerate(Distinct):
			Ref = dict(source_id=Capture["source_id"], locator="line 1")
			self.assertTrue(library.reference_states(self.Root, [Ref])[0]["reference_reuse_allowed"])
			Consumer = library.save_card(self.Root, dict(content="distinct-capture-consumer-" + str(Number) + "\n", sources=[Ref], dependencies=[dict(path=Capture["source"], sha256=library.file_digest(self.Root / Capture["source"]))]), "instruments/distinct-capture-" + str(Number) + ".md")
			self.assertTrue(library.reference_states(self.Root, [Ref])[0]["reference_reuse_allowed"])
			self.assertTrue(library.read_card(self.Root, Consumer["location"])["reuse_allowed"])
		AliasConsumer = library.save_card(self.Root, dict(content="A consumer of the same captured content under a new title.\n", dependencies=[dict(path=Alias["source"], sha256=library.file_digest(self.Root / Alias["source"]))]), "instruments/registered-title-alias.md")
		self.assertFalse(library.reference_states(self.Root, [dict(source_id=Alias["source_id"])])[0]["reference_reuse_allowed"])
		self.assertFalse(library.read_card(self.Root, AliasConsumer["location"], True)["reuse_allowed"])
		self.assertFalse(library.reference_states(self.Root, [dict(source_id=Original["source_id"])])[0]["reference_reuse_allowed"])
		self.assertTrue(library.read_card(self.Root, Genuine["location"])["reuse_allowed"])
		for Name, Raw in OldRecords.items():
			self.assertEqual((Catalog.parent / (Name + ".json")).read_bytes(), Raw)

	def test_cached_identity_projection_cannot_override_live_quarantine(self):
		self.quarantine()
		_, Body, _ = library.read_metadata((self.Root / self.First["location"]).read_bytes())
		NewPath = self.Root / "instruments/renamed.md"
		NewPath.write_bytes(b"---\n" + library.json_bytes(dict(tool_id=self.First["tool_id"], title="Changed title")) + b"---\n" + Body.encode("utf-8"))
		Location = library.relative(self.Root, NewPath)
		Index = library.read_json(self.Root / self.Index)
		CurrentRow = library.parse_card(self.Root, Location, NewPath.read_bytes(), {}, Snapshot=False)
		CachePath = self.Root / "cache/identity-shadow.json"
		for Extras in (dict(identity_tool_id=None), dict(identity_tool_id="another-identity", capture_identity=["forged", "metadata", "hash", "tuple"]), dict(tool_id="different-cached-tool"), dict(tool_id="different-cached-tool", identity_tool_id=None, capture_identity=None), dict(identity_tool_ids=["different-cached-tool"])):
			with self.subTest(cached_fields=Extras):
				Index["items"] = [dict(CurrentRow, **Extras)]
				Index["blocked_items"] = []
				CachePath.write_bytes(library.json_bytes(Index))
				Before = CachePath.read_bytes()
				with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
					library.read_card(self.Root, Location, IndexPath="cache/identity-shadow.json")
				History = library.read_card(self.Root, Location, True, "cache/identity-shadow.json")
				self.assertEqual(History["tool_id"], self.First["tool_id"])
				self.assertFalse(History["reuse_allowed"])
				self.assertNotIn("identity_tool_id", History)
				self.assertNotIn("capture_identity", History)
				Query = library.query_tools(self.Root, "finite-time", "cache/identity-shadow.json")
				self.assertFalse(Query["hits"])
				HistoryQuery = library.query_tools(self.Root, "finite-time", "cache/identity-shadow.json", IncludeAffected=True)
				self.assertTrue(HistoryQuery["hits"])
				self.assertTrue(all(not Hit["reuse_allowed"] and Hit["trust"] == "HISTORY_ONLY_NOT_REUSE" for Hit in HistoryQuery["hits"]))
				Package = context.knowledge_package(self.Root, "finite-time", IndexPath="cache/identity-shadow.json", IncludeAffected=True)
				self.assertFalse(Package["materials"])
				self.assertFalse(Package["reading_order"])
				Export = context.export_package(self.Root, Package, "exports")
				self.assertFalse(Export["materials"])
				self.assertTrue(Export["historical"])
				self.assertEqual(CachePath.read_bytes(), Before)
				# Explicit refresh must not preserve the same spoofed ID through
				# the byte-current incremental-index path or register it as truth.
				library.make_index(self.Root, ["instruments"], "cache/identity-shadow.json")
				Refreshed = library.read_json(CachePath)
				Indexed = next(Item for Item in Refreshed["items"] + Refreshed.get("blocked_items", []) if Item["location"] == Location)
				self.assertEqual(Indexed["tool_id"], self.First["tool_id"])
				self.assertFalse(Indexed["reuse_allowed"])
				self.assertFalse(library.query_tools(self.Root, "finite-time", "cache/identity-shadow.json")["hits"])

	def test_durable_legacy_identity_cannot_suppress_declared_source_obligations(self):
		self.quarantine()
		Location = "instruments/legacy-renamed.md"
		Raw = b"---\n" + library.json_bytes(dict(tool_id=self.First["tool_id"], title="A renamed statement")) + b"---\nA finite-time semigroup method.\n"
		(self.Root / Location).write_bytes(Raw)
		# The existing registration API allows legacy pointer IDs. This is the
		# persisted state that the old poisoned-index refresh actually produced.
		with library.writer_lock(library.library_root(self.Root)):
			Node = corrections.register_version(self.Root, Location, Raw, "different-legacy-pointer")
		self.assertEqual(Node["tool_id"], "different-legacy-pointer")
		Registry = library.library_root(self.Root) / "card-bindings"
		OriginalRecords = {PathValue: PathValue.read_bytes() for PathValue in Registry.glob("*.json") if PathValue.name != "catalog.json"}
		with self.assertRaisesRegex(ValueError, "REUSE_BLOCKED"):
			library.read_card(self.Root, Location, IndexPath="cache/missing.json")
		History = library.read_card(self.Root, Location, True, "cache/missing.json")
		self.assertEqual(History["tool_id"], self.First["tool_id"])
		self.assertFalse(History["reuse_allowed"])
		Ref = dict(path=Location, sha256=library.digest(Raw), locator="line 1")
		self.assertFalse(library.reference_states(self.Root, [Ref])[0]["reference_reuse_allowed"])
		Consumer = library.save_card(self.Root, dict(content="A consumer of this exact legacy version.\n", dependencies=[Ref]), "instruments/legacy-dependent.md")
		self.assertFalse(library.read_card(self.Root, Consumer["location"], True, "cache/missing.json")["reuse_allowed"])
		library.make_index(self.Root, ["instruments"], "cache/legacy-identity.json")
		self.assertFalse(library.query_tools(self.Root, "finite-time", "cache/legacy-identity.json")["hits"])
		Package = context.knowledge_package(self.Root, "finite-time", IndexPath="cache/legacy-identity.json", IncludeAffected=True)
		self.assertFalse(Package["materials"])
		self.assertFalse(Package["reading_order"])
		# An ambiguous duplicate ID is excluded from the query; exact-path
		# historical reading above remains available with reuse=false.
		self.assertFalse(context.export_package(self.Root, Package, "exports")["materials"])
		Store = corrections.load_store(self.Root)
		States, _ = corrections.impact_states(self.Root, Store)
		self.assertFalse(States[(Location, library.digest(Raw))]["reuse_allowed"])
		self.assertEqual(Store["nodes"][(Location, library.digest(Raw))]["tool_id"], "different-legacy-pointer")
		for PathValue, Before in OriginalRecords.items():
			self.assertEqual(PathValue.read_bytes(), Before)

	def test_first_source_issue_invalidates_export_without_catalog_or_cache_changes(self):
		Captured = library.capture_source(self.Root, self.Root / "basis.md", "https://example.org/first-correction", "edition-1", "A scoped source")
		Metadata = dict(path=Captured["source"], sha256=library.file_digest(self.Root / Captured["source"]))
		library.save_card(self.Root, dict(content="An unrelated registering consumer.\n", dependencies=[Metadata]), "instruments/registry-only.md")
		Reference = dict(source_id=Captured["source_id"], locator="line 1")
		Relation = dict(kind="mathematical_dependency", target=dict(path=self.Second["location"], sha256=self.Second["sha256"], role="card"), basis=Reference)
		Saved = library.save_card(self.Root, dict(content="first-correction-export-needle\n", sources=[Reference], relations=[Relation], dependencies=[dict(path=self.Second["location"], sha256=self.Second["sha256"])]), "instruments/export-first-issue.md")
		library.make_index(self.Root, ["instruments"], self.Index)
		Catalog = library.library_root(self.Root) / "card-bindings/catalog.json"
		Before = {PathValue: PathValue.read_bytes() for PathValue in (Catalog, self.Root / self.Index, self.Root / Saved["location"])}
		Package = context.knowledge_package(self.Root, "first-correction-export-needle", IndexPath=self.Index, Limit=1, Depth=0)
		Marker = library.relative(self.Root, library.library_root(self.Root) / "corrections-required.json")
		Journal = library.relative(self.Root, library.library_root(self.Root) / "corrections-journal.json")
		self.assertIsNone(Package["correction_basis"][Marker])
		self.assertIsNone(Package["correction_basis"][Journal])
		self.assertTrue(Package["materials"][0]["relations"][0]["impact_eligible"])
		Export = context.export_package(self.Root, Package, "exports")
		ExportBytes = (self.Root / Export["export"]).read_bytes()
		corrections.register_issue(self.Root, dict(issue_id="first-source-correction", origin="internal", reporter="fixture-author", summary="The captured basis is not reusable.", targets=[Metadata], evidence=[dict(path="basis.md", locator="line 1")]))
		for PathValue, Raw in Before.items():
			self.assertEqual(PathValue.read_bytes(), Raw)
		# The queried card remains clear: the issue is on its source, not on a
		# declared proof dependency. Export must check more than read_card reuse.
		self.assertTrue(library.read_card(self.Root, Saved["location"], IndexPath=self.Index)["reuse_allowed"])
		self.assertFalse(library.reference_states(self.Root, [Reference])[0]["reference_reuse_allowed"])
		with self.assertRaisesRegex(ValueError, "correction state changed"):
			context.export_package(self.Root, Package, "late-exports")
		self.assertFalse((self.Root / "late-exports").exists())
		self.assertEqual((self.Root / Export["export"]).read_bytes(), ExportBytes)
		Current = context.knowledge_package(self.Root, "first-correction-export-needle", IndexPath=self.Index, Limit=1, Depth=0)
		self.assertFalse(Current["materials"][0]["sources"][0]["reference_reuse_allowed"])
		self.assertFalse(Current["materials"][0]["relations"][0]["reuse_allowed"])
		self.assertFalse(Current["materials"][0]["relations"][0]["impact_eligible"])
		self.assertFalse(context.export_package(self.Root, Current, "exports")["materials"][0]["relations"][0]["impact_eligible"])
		# A caller cannot repair an old view by updating only its epoch/hash.
		Forged = dict(Package, correction_basis=Current["correction_basis"], inputs=Current["inputs"])
		Forged["view_sha256"] = library.digest(library.json_bytes({Key: Value for Key, Value in Forged.items() if Key != "view_sha256"}))
		with self.assertRaisesRegex(ValueError, "reference or relation state changed"):
			context.export_package(self.Root, Forged, "stale-reference-exports")



if(__name__ == "__main__"):
	unittest.main()
