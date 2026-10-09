#!/usr/bin/env python3
"""Task knowledge views: lexical relevance, explicit scope and live correction gates.

No theorem implication, workflow scheduling or accepted-graph writes occur here.
All mathematical explanations and relations are supplied by authors, not inferred
from links. A knowledge view is not an independent review packet.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys

import research_library as library

CONTEXT_FIELDS = ("goal", "problem_ids", "objects", "conditions", "parameter_scope", "tool_types")
RELATION_KINDS = ("mathematical_dependency", "method_analogy", "implementation_call", "citation", "replacement")
LOADED_SOURCE_SHA256 = library.file_digest(Path(__file__))


def normalize_context(Context):
	Context = {} if Context is None else Context
	if(not isinstance(Context, dict) or set(Context) - set(CONTEXT_FIELDS)):
		raise ValueError("context accepts only optional goal, problem_ids, objects, conditions, parameter_scope and tool_types")
	for Key, Value in Context.items():
		if(not isinstance(Value, (str, list, dict)) or len(library.json_bytes(Value)) > 12000):
			raise ValueError("invalid or oversized context field: " + Key)
	return Context


def searchable(Value):
	return json.dumps(Value, ensure_ascii=False, sort_keys=True).casefold()


def term_match(Term, Text):
	if(re.fullmatch(r"[a-z][a-z0-9_]*", Term)):
		return re.search(r"(?<![a-z0-9_])" + re.escape(Term) + r"(?![a-z0-9_])", Text) is not None
	return Term in Text


def producer_identity():
	Identity = library.context_code_identity()
	if(Identity["script_hashes"]["research_context.py"] != LOADED_SOURCE_SHA256):
		raise ValueError("knowledge code changed since loading; start a new Python process")
	return dict(name="manage-math-research-program", python=sys.version.split()[0], code_epoch="FRESH_PROCESS_SOURCE_SNAPSHOT", **Identity)


def annotation_basis(project):
	return {library.relative(project, library.inside(project, PathValue)): library.file_digest(PathValue) for PathValue in sorted((library.library_root(project) / "annotations").glob("*.json"))}


def correction_basis(project):
	# Absence is part of the epoch: the first issue can create a journal without
	# changing an already registered catalog or the caller's cached index.
	Names = ("card-bindings/catalog.json", "card-bindings-required.json", "corrections-required.json", "corrections-journal.json")
	return {library.relative(project, library.inside(project, library.library_root(project) / Name)): library.file_digest(library.library_root(project) / Name) if (library.library_root(project) / Name).is_file() else None for Name in Names}


def reference_inputs(project, Reference, Inputs):
	if(Reference.get("binding_state") != "CURRENT"):
		return
	if(Reference.get("path") and Reference.get("sha256")):
		Inputs[Reference["path"]] = Reference["sha256"]
	if(Reference.get("source_id") and Reference.get("captured_source")):
		Folder = library.library_root(project) / "sources" / Reference["source_id"]
		for Name in ("source.json", "raw.bin", "text.txt"):
			PathValue = library.inside(project, Folder / Name)
			Inputs[library.relative(project, PathValue)] = library.file_digest(PathValue)
		for Alias in Reference.get("capture_aliases", []):
			Inputs[Alias["snapshot"]] = Alias["sha256"]


def rank_candidate(Query, Context, Row, Body, Notes):
	if(len(Query) > 2000):
		raise ValueError("query exceeds 2000 characters")
	Terms = list(dict.fromkeys((Query + " " + str(Context.get("goal", ""))).casefold().split()))[:64]
	QueryTerms = set(Query.casefold().split())
	Fields = dict(body=(Body.casefold(), 3), title=(searchable(Row.get("title", "")), 6), aliases=(searchable(Row.get("aliases", [])), 8),
		identity=(searchable(Row.get("tool_id", "")), 2), problem_ids=(searchable(Row.get("problem_ids", [])), 8),
		annotations=(searchable([Note.get("content", "") + " " + Note.get("kind", "") for Note in Notes]), 5))
	if(Row.get("field_provenance", {}).get("sources", {}).get("state") == "CURRENT_AUTHOR_FIELD"):
		Fields["source_locators"] = (searchable(Row.get("sources", [])), 2)
	for Key in ("conditions", "scope", "experience", "objects", "parameter_scope", "tool_types", "tags"):
		if(Row.get("field_provenance", {}).get(Key, {}).get("state") == "CURRENT_AUTHOR_FIELD"):
			Fields[Key] = (searchable(Row.get(Key)), 2)
	Reasons, Score = [], 0
	for Key, (Text, Weight) in Fields.items():
		Matched = [Term for Term in Terms if term_match(Term, Text)]
		if(Matched):
			Score += Weight * len(Matched)
			Reasons.append(dict(field=Key, terms=Matched, query_terms=[Term for Term in Matched if Term in QueryTerms], weight=Weight, basis="CURRENT_BYTES_OR_CURRENT_ANNOTATION"))
	HasLexicalMatch = Score > 0
	for Key in ("problem_ids", "objects", "conditions", "parameter_scope", "tool_types"):
		if(Row.get("field_provenance", {}).get(Key, {}).get("state") != "CURRENT_AUTHOR_FIELD"):
			continue
		Values = Context.get(Key, [])
		Recorded = Row.get(Key, [])
		if(isinstance(Values, dict)):
			Matched = [dict(axis=Axis, value=Value) for Axis, Value in Values.items() if isinstance(Recorded, dict) and Recorded.get(Axis) == Value]
		else:
			Values = Values if isinstance(Values, list) else [Values]
			Matched = [Value for Value in Values if Value and searchable(Value) in searchable(Recorded)]
		if(Matched):
			Weight = 36 if Key == "problem_ids" and HasLexicalMatch else 6
			Score += Weight * len(Matched)
			Reasons.append(dict(field=Key, context_mentions=Matched, weight=Weight, context_only=not HasLexicalMatch, basis="EXPLICIT_FIELD_TEXT_MATCH_NOT_IMPLICATION"))
	return Score, Reasons


def condition_check(Context, Row):
	Checks = []
	for Key in ("objects", "parameter_scope"):
		Required, Recorded = Context.get(Key), Row.get(Key)
		if(isinstance(Required, dict)):
			for Axis, Value in Required.items():
				Other = Recorded.get(Axis) if isinstance(Recorded, dict) else None
				State = "NOT_RECORDED" if Other is None else "TEXT_EQUAL_NOT_ENTAILMENT" if Value == Other else "DIFFERENT_RECORDED_SCOPE_CHECK_BRIDGE"
				Checks.append(dict(field=Key, axis=Axis, requested=Value, recorded=Other, state=State))
	Conditions = Row.get("conditions", "UNSPECIFIED")
	Required = Conditions if isinstance(Conditions, list) else [Conditions]
	return dict(status="HOST_MUST_CHECK_ORIGINAL_STATEMENT", conditions=Conditions,
		conditions_state=Row.get("field_provenance", {}).get("conditions", {}).get("state", "NOT_BOUND_TO_CURRENT_BODY"),
		condition_mentions=[dict(condition=Value, mentioned_in_context=searchable(Value) in searchable(Context.get("conditions", [])), proved=False) for Value in Required],
		scope_axes=Checks, missing_bridges=Row.get("missing_bridges", []), implication_checked=False)


def bind_relations(project, Relations):
	if(not isinstance(Relations, list)):
		raise ValueError("relations must be a list")
	Result = []
	for Relation in Relations:
		if(not isinstance(Relation, dict) or Relation.get("kind") not in RELATION_KINDS):
			raise ValueError("unknown typed relation")
		if(not isinstance(Relation.get("basis"), dict) or not Relation["basis"].get("locator")):
			raise ValueError("a relation requires an explicit source basis and locator")
		Target = library.bind_references(project, [Relation.get("target", {})])[0]
		Basis = library.bind_references(project, [Relation["basis"]])[0]
		Result.append(dict(Relation, target=Target, basis=Basis, origin="AUTHOR_SUPPLIED_RELATION"))
	return Result


def relation_views(project, Row, IndexPath):
	Views = []
	for Relation in Row.get("relations", []):
		try:
			if(not isinstance(Relation, dict) or Relation.get("kind") not in RELATION_KINDS):
				raise ValueError("unknown typed relation")
			Target = library.reference_states(project, [Relation["target"]])[0]
			Basis = library.reference_states(project, [Relation["basis"]])[0]
			Current = Target["binding_state"] == "CURRENT" and Basis["binding_state"] == "CURRENT" and bool(Basis.get("locator"))
			Reuse = Target.get("reference_reuse_allowed") is not False and Basis.get("reference_reuse_allowed") is not False
			if(Target.get("role") == "card" and Target.get("path")):
				Card = library.read_card(project, Target["path"], True, IndexPath, _Locked=True)
				Reuse = Reuse and Card["reuse_allowed"] and Card["sha256"] == Target.get("sha256")
				Target.update(reuse_allowed=Reuse, correction_state=Card["correction_state"])
			Declared = any(Ref.get("location", Ref.get("path")) == Target.get("path") and Ref.get("sha256") == Target.get("sha256") for Ref in Row.get("dependencies", []))
			Views.append(dict(Relation, target=Target, basis=Basis, binding_current=Current, reuse_allowed=Reuse and Current,
				impact_eligible=Current and Reuse and Declared and Relation["kind"] == "mathematical_dependency", trust="AUTHOR_SUPPLIED_NOT_AN_INFERRED_PROOF_EDGE"))
		except (OSError, ValueError, TypeError, KeyError) as Error:
			if("CORRECTIONS_INVALID" in str(Error)):
				raise
			Views.append(dict(relation=Relation, binding_current=False, reuse_allowed=False, error=str(Error)))
	return Views


def recheck_lean_reference(project, Reference, LeanTools):
	"""Call the existing verifier. Paths to executable tools come from the caller."""
	State = dict(Reference, machine_execution="UNKNOWN", exact_root="UNKNOWN", semantic_correspondence="UNKNOWN")
	try:
		if(not LeanTools):
			raise ValueError("no lean-verify tools directory was supplied")
		Tools = Path(LeanTools).resolve()
		Checker = Tools / "lean_evidence.py"
		if(not Checker.is_file()):
			raise ValueError("lean-verify recheck interface is unavailable")
		Verification = Reference.get("verification", {})
		Manifest = library.inside(project, Verification["path"])
		if(library.file_digest(Manifest) != Verification.get("sha256")):
			raise ValueError("saved verification reference changed or was never bound")
		Command = [sys.executable, "-X", "utf8", str(Checker), "--manifest", str(Manifest)]
		Process = subprocess.run(Command, capture_output=True, text=True, encoding="utf-8", timeout=240, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
		Result = json.loads(Process.stdout)
		Identity = bool(Reference.get("declaration")) and Result.get("declaration") == Reference["declaration"]
		if(Reference.get("semantic_sha256")):
			Identity = Identity and Result.get("semantic_sha256") == Reference["semantic_sha256"]
		Passed = Process.returncode == 0 and Result.get("snapshot_current") is True and Result.get("exact_root_passed") is True and Identity
		State.update(recheck=Result, checker=str(Checker), checker_sha256=library.digest(Checker.read_bytes()), identity_matches=Identity,
			machine_execution="SAVED_EXECUTION_RECHECKED" if Passed else "NOT_ESTABLISHED", exact_root="PASSED_CURRENT" if Passed else "NOT_ESTABLISHED",
			trust="EXACT_ROOT_ONLY_MODEL_CONNECTIONS_REMAIN_OPEN" if Passed else "UNVERIFIED_DECLARATION_REFERENCE")
		if(Passed and Reference.get("semantic_review")):
			Audit = library.inside(project, Reference["semantic_review"]["path"])
			if(library.digest(Audit.read_bytes()) != Reference["semantic_review"].get("sha256")):
				raise ValueError("semantic audit reference changed")
			# Reuse the verifier's public identity check; never invent semantic approval.
			Code = "import json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from verify_lean_project import semantic_review;m=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'));print(json.dumps(semantic_review(m['target'],sys.argv[3],Path(m['project_root']))))"
			Semantic = subprocess.run([sys.executable, "-X", "utf8", "-c", Code, str(Tools), str(Manifest), str(Audit)], capture_output=True, text=True, encoding="utf-8", timeout=240, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
			if(Semantic.returncode != 0):
				raise ValueError("existing semantic identity check did not complete")
			State["semantic_check"] = json.loads(Semantic.stdout)
			State["semantic_correspondence"] = "IDENTITY_RECHECKED_REVIEW_ATTESTATION" if State["semantic_check"].get("reused") is True else "NOT_ESTABLISHED"
		State["open_connections"] = Reference.get("open_connections", ["Model connections were not recorded."])
		State["library_acceptance"] = "NOT_ESTABLISHED"
		State["blueprint_acceptance"] = "NOT_ESTABLISHED"
	except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as Error:
		State.update(error=str(Error), trust="UNVERIFIED_DECLARATION_REFERENCE")
	return State


def knowledge_package(project, Query, Context=None, IndexPath="index/tools.json", Limit=5, Depth=1, MaxChars=32000, IncludeAffected=False, Entries=None, RecheckLean=False, LeanTools=None):
	Producer = producer_identity()
	Context = normalize_context(Context)
	if(not 0 <= Depth <= 3 or not 4000 <= MaxChars <= 250000):
		raise ValueError("depth must be 0..3 and max-chars 4000..250000")
	with library.writer_lock(library.library_root(project)):
		library.gated_rows(project, [])
		AnnotationBasis = annotation_basis(project)
		QueryResult = library._query_tools(project, Query, IndexPath, Limit, False, False, False, IncludeAffected, Context)
		if(QueryResult["verdict"] == "CORRECTIONS_INVALID"):
			raise ValueError("CORRECTIONS_INVALID")
		CorrectionBasis = correction_basis(project)
		Materials, History, FollowUp, Inputs, Seen = [], [], [], {}, set()
		Index = library.inside(project, IndexPath)
		Inputs[library.relative(project, Index)] = library.digest(Index.read_bytes())
		for Name in ("card-bindings/catalog.json", "card-bindings-required.json", "corrections-required.json", "corrections-journal.json"):
			PathValue = library.library_root(project) / Name
			if(PathValue.is_file()):
				Inputs[library.relative(project, PathValue)] = library.digest(PathValue.read_bytes())
		Queue = [(Hit["location"], 0, Hit) for Hit in QueryResult["hits"]]
		IndexRows = library.read_json(Index).get("items", [])
		Used = 0
		while(Queue):
			Location, Level, Hit = Queue.pop(0)
			if(Location in Seen):
				continue
			Seen.add(Location)
			try:
				Row = library.read_card(project, Location, True, IndexPath, _Locked=True)
			except (OSError, ValueError, TypeError, KeyError) as Error:
				if("CORRECTIONS_INVALID" in str(Error)):
					raise
				FollowUp.append(dict(path=Location, reason=str(Error)))
				continue
			Inputs[Location] = Row["sha256"]
			if(not Row["reuse_allowed"]):
				History.append(dict(path=Location, sha256=Row["sha256"], title=Row["title"], conditions=Row["conditions"], sources=Row["sources"], correction_state=Row["correction_state"], trust="HISTORY_ONLY_NOT_REUSE"))
				if(Level < Depth):
					for Candidate in IndexRows:
						if(library.file_digest(library.inside(project, Candidate["location"])) != Candidate.get("sha256")):
							continue
						if(Candidate.get("field_provenance", {}).get("relations", {}).get("state") != "CURRENT_AUTHOR_FIELD"):
							continue
						for Relation in Candidate.get("relations", []):
							Target = Relation.get("target", {})
							if(Relation.get("kind") == "replacement" and Target.get("path") == Location and Target.get("sha256") == Row["sha256"]):
								Basis = library.reference_states(project, [Relation.get("basis", {})])[0]
								if(Basis["binding_state"] == "CURRENT" and Basis.get("locator") and Basis.get("reference_reuse_allowed") is not False):
									Queue.append((Candidate["location"], Level + 1, dict(relevance_reasons=[dict(field="relations", basis="AUTHOR_EXPLICIT_REPLACEMENT_OF_HISTORY_NOT_A_RELEASE", historical_path=Location)])))
				continue
			Relations = relation_views(project, Row, IndexPath)
			Material = {Key: Row.get(Key) for Key in ("path", "sha256", "version", "title", "kind", "summary", "conditions", "scope", "objects", "parameter_scope", "problem_ids", "evidence_status", "experience", "sources", "evidence", "resources", "lean", "missing_bridges", "field_provenance", "historical_metadata", "dependencies", "dependencies_known", "correction_state", "reuse_allowed", "content", "coverage")}
			Material.update(match_kind=Hit.get("match_kind", "EXPLICIT_RELATION"), query_match=Hit.get("query_match", False), lexical_match=Hit.get("lexical_match", False), relevance_reasons=Hit.get("relevance_reasons", []), applicability_check=condition_check(Context, Row), relations=Relations,
				annotations=Hit.get("annotations", []),
				trust="RETRIEVAL_ONLY_REVALIDATE_APPLICATION", dependency_coverage="DECLARED_EDGES_ONLY" if Row["dependencies_known"] else "UNKNOWN_NOT_EMPTY_CLOSURE")
			Size = len(library.json_bytes(Material).decode("utf-8"))
			if(Used + Size > MaxChars):
				FollowUp.append(dict(path=Location, sha256=Row["sha256"], reason="SIZE_BOUND_WHOLE_MATERIAL_OMITTED_HYPOTHESES_NOT_TRUNCATED"))
				continue
			Used += Size
			Materials.append(Material)
			for Key in ("sources", "evidence", "resources"):
				for Ref in Row[Key]:
					reference_inputs(project, Ref, Inputs)
					if(Ref.get("binding_state") != "CURRENT" or Ref.get("reference_reuse_allowed") is False or not Ref.get("read_coverage")):
						FollowUp.append(dict(reference=Ref, reason="VERIFY_SOURCE_LOCATOR_AND_ACTUAL_READING_COVERAGE"))
			for Note in Hit.get("annotations", []):
				if(Note.get("state") == "CURRENT"):
					Inputs[Note["path"]] = Note["sha256"]
			for Relation in Relations:
				for Key in ("basis", "target"):
					Ref = Relation.get(Key, {})
					reference_inputs(project, Ref, Inputs)
				Target = Relation.get("target", {})
				if(Target.get("role") == "card" and Target.get("path")):
					if(Relation.get("reuse_allowed") and Level < Depth):
						Queue.append((Target["path"], Level + 1, {}))
					else:
						FollowUp.append(dict(reference=Target, relation_kind=Relation.get("kind"), reason="DEPTH_BOUND_OR_HISTORY_ONLY_OR_CHANGED_RELATION"))
			if(RecheckLean):
				Material["lean"] = [recheck_lean_reference(project, Ref, LeanTools) for Ref in Row["lean"]]
			for Ref in Row["lean"]:
				for Reference in [Ref.get(Key, {}) for Key in ("source", "verification", "semantic_review", "actual_type") if isinstance(Ref.get(Key), dict)] + Ref.get("definitions", []):
					reference_inputs(project, Reference, Inputs)
		EntryViews = []
		for Location in Entries or ["state/RESUME.md", "research_map.md"]:
			PathValue = library.inside(project, Location)
			if(PathValue.is_file()):
				Raw = PathValue.read_bytes()
				Inputs[library.relative(project, PathValue)] = library.digest(Raw)
				EntryViews.append(dict(path=library.relative(project, PathValue), sha256=library.digest(Raw), reading_hint="Read the current opening, then the named materials; history is not task state."))
		for Location, Hash in Inputs.items():
			if(library.file_digest(library.inside(project, Location)) != Hash):
				raise ValueError("input changed while assembling knowledge: " + Location)
		if(annotation_basis(project) != AnnotationBasis):
			raise ValueError("annotations changed while assembling knowledge; rebuild the view")
		if(correction_basis(project) != CorrectionBasis):
			raise ValueError("correction state changed while assembling knowledge; rebuild the view")
		if(producer_identity() != Producer):
			raise ValueError("knowledge producer changed while assembling; start a new Python process")
		Package = dict(schema="research-context/v1", producer=Producer, index_path=IndexPath, query=Query, context=Context, entries=EntryViews, materials=Materials, historical=History,
			reading_order=[Item["path"] for Item in sorted(Materials, key=lambda Item: Item["kind"] != "definition")], follow_up=FollowUp,
			coverage=dict(index_verdict=QueryResult["verdict"], changed_paths=QueryResult["changed_paths"], total_matches=QueryResult["total_matches"], selected=len(Materials), depth=Depth, max_material_chars=MaxChars, limitations=["Declared relations and indexed card roots only.", "Unknown dependencies are not an empty impact closure.", "Relevance and matching fields do not prove mathematical applicability."]),
			inputs=Inputs, annotation_basis=AnnotationBasis, correction_basis=CorrectionBasis, refresh_basis="Current card/source/entry bytes, annotation membership and live authoritative correction state including absence.",
			trust="REBUILDABLE_KNOWLEDGE_VIEW_NOT_PROOF_OR_BLIND_REVIEW", canonical_modified=False, workflow_state_modified=False)
		Package["view_sha256"] = library.digest(library.json_bytes(Package))
		return Package


def export_package(project, Package, Output):
	with library.writer_lock(library.library_root(project)):
		library.gated_rows(project, [])
		if(Package.get("producer") != producer_identity()):
			raise ValueError("knowledge producer changed; rebuild the view")
		if(Package.get("annotation_basis") != annotation_basis(project)):
			raise ValueError("annotations changed before export; rebuild the view")
		if(Package.get("correction_basis") != correction_basis(project)):
			raise ValueError("correction state changed before export; rebuild the view")
		if(Package.get("view_sha256") != library.digest(library.json_bytes({Key: Value for Key, Value in Package.items() if Key != "view_sha256"}))):
			raise ValueError("knowledge view identity mismatch")
		for Location, Hash in Package["inputs"].items():
			if(library.file_digest(library.inside(project, Location)) != Hash):
				raise ValueError("knowledge inputs changed before export: " + Location)
		for Item in Package["materials"]:
			Card = library.read_card(project, Item["path"], IndexPath=Package["index_path"], _Locked=True)
			if(Item.get("reuse_allowed") is not True or any(Item.get(Name, []) != Card[Name] for Name in ("sources", "evidence", "resources")) or Item.get("relations") != relation_views(project, Card, Package["index_path"])):
				raise ValueError("knowledge reference or relation state changed before export; rebuild the view: " + Item["path"])
		Target = library.inside(project, Path(Output) / (Package["view_sha256"] + ".json"))
		library.immutable_write(Target, library.json_bytes(Package))
		return dict(Package, export=library.relative(project, Target))
