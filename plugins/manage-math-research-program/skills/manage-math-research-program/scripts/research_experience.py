#!/usr/bin/env python3
"""Save research experience, compare routes and assemble an editable understanding page.

The author supplies mathematical explanations and tests. This helper binds and
assembles them; shared words do not establish a theorem or an accepted premise.
"""

from __future__ import annotations

import argparse
from contextlib import nullcontext
import json
import os
from pathlib import Path
import re

import research_library as library

OUTCOMES = ("success", "partial", "failed", "no_return", "unknown")
FAILURE_KINDS = ("counterexample", "method_limit", "missing_lemma", "numerical_resolution", "software_error", "infrastructure", "unknown")
COMPARISON_FIELDS = ("target", "admissible_class", "key_assumptions", "lost_information", "completed_steps", "failure_location", "complementary_lemma")
START = "<!-- research-understanding:v2:start -->"
END = "<!-- research-understanding:v2:end -->"
HASH_PREFIX = "<!-- research-understanding-sha256:"


def text_items(Value):
	if(Value is None):
		return []
	if(isinstance(Value, str)):
		return [Value] if Value.strip() else []
	if(not isinstance(Value, list) or any(not isinstance(Item, str) for Item in Value)):
		raise ValueError("expected text or a list of text")
	return Value


def record_experience(project, Data, ToolPath=None, ExpectedHash=None):
	Data = dict(Data)
	if(ToolPath is not None and library.inside(project, ToolPath).exists()):
		Front, Body, _ = library.read_metadata(library.inside(project, ToolPath).read_bytes())
		if(Front.get("kind") == "experience"):
			Previous = dict(Front.get("experience", dict()))
			Previous["content"] = Body
			Previous["title"] = Front.get("title", "Research experience")
			Previous["evidence_status"] = Front.get("evidence_status", "RESEARCH_NOTE")
			Data = dict(Previous, **Data)
	Outcome = str(Data.pop("outcome", "unknown")).lower()
	FailureKind = Data.pop("failure_kind", None)
	if(Outcome not in OUTCOMES or (FailureKind is not None and FailureKind not in FAILURE_KINDS)):
		raise ValueError("unknown outcome or failure_kind; describe details freely in mechanism")
	if(Outcome == "no_return"):
		if(FailureKind not in (None, "unknown", "infrastructure")):
			raise ValueError("no_return is not evidence for a mathematical failure")
		FailureKind = "infrastructure"
	elif(Outcome == "failed" and FailureKind is None):
		FailureKind = "unknown"
	Scope = Data.pop("scope", Data.get("conditions", "UNSPECIFIED"))
	Experience = dict(outcome=Outcome, failure_kind=FailureKind, scope=Scope,
		question=Data.pop("question", ""), conclusion=Data.pop("conclusion", ""),
		mechanism=Data.pop("mechanism", ""),
		transformations=text_items(Data.pop("transformations", [])),
		reconsider_when=text_items(Data.pop("reconsider_when", [])),
		not_applicable_to=text_items(Data.pop("not_applicable_to", [])))
	for Key in COMPARISON_FIELDS:
		Experience[Key] = text_items(Data.pop(Key, []))
	Content = Data.get("content", "")
	if(not Content and not Experience["question"] and not Experience["conclusion"]):
		raise ValueError("provide content, a question or a conclusion worth retaining")
	if(not Content):
		Sections = ["# " + str(Data.get("title", "Research experience"))]
		for Key in ("question", "conclusion", "scope", "mechanism", "transformations", "reconsider_when", "not_applicable_to"):
			Value = Experience[Key]
			if(Value):
				Sections.extend(["", "## " + Key.replace("_", " ").capitalize(), "",
					"\n".join("- " + Item for Item in text_items(Value))])
		Data["content"] = "\n".join(Sections)
	Data.update(kind="experience", experience=Experience, conditions=Scope)
	Data.setdefault("evidence_status", "RESEARCH_NOTE")
	if(ToolPath is None):
		RecordId = str(Data.get("tool_id") or "experience-" + library.digest(library.json_bytes(Data))[:20])
		if(not re.fullmatch(r"[A-Za-z0-9_.-]+", RecordId)):
			raise ValueError("use a file-safe tool_id or specify --tool")
		Data["tool_id"] = RecordId
		ToolPath = library.relative(project, library.library_root(project) / "experiences" / (RecordId + ".md"))
	return library.save_card(project, Data, ToolPath, ExpectedHash)


def read_route(project, PathValue, IncludeAffected=False, _Locked=False):
	if(not _Locked):
		with library.writer_lock(library.library_root(project)):
			return read_route(project, PathValue, IncludeAffected, True)
	Row = library.read_card(project, PathValue, IncludeAffected, _Locked=True)
	PathValue = library.inside(project, PathValue)
	Raw = PathValue.read_bytes()
	if(library.digest(Raw) != Row["sha256"]):
		raise ValueError("route changed during read")
	Front, Body, MetadataStatus = library.read_metadata(Raw)
	Experience = Row.get("experience", dict())
	for Key in ("question", "conclusion", "mechanism", "scope", "transformations", "reconsider_when", "not_applicable_to", *COMPARISON_FIELDS):
		text_items(Experience.get(Key))
	return dict(path=library.relative(project, PathValue), sha256=library.digest(Raw),
		tool_id=Row["tool_id"], title=Row["title"],
		metadata_status=MetadataStatus, evidence_status=Row.get("evidence_status", "UNKNOWN"),
		conditions=Row.get("conditions", "UNSPECIFIED"), experience=Experience,
		summary=Row["summary"],
		evidence=library.reference_states(project, Front.get("evidence", [])),
		resources=library.reference_states(project, Front.get("resources", [])),
		sources=library.reference_states(project, Front.get("sources", [])),
		lean=library.lean_reference_states(project, Front.get("lean", [])),
		correction_state=Row["correction_state"], reuse_allowed=Row["reuse_allowed"], field_provenance=Row["field_provenance"],
		trust=Row["trust"])


def hypothesis_view(project, Hypothesis):
	References = library.reference_states(project, Hypothesis.get("evidence", []))
	Allowed = all(Reference.get("reference_reuse_allowed") is not False and Reference.get("binding_state") not in ("STALE_OR_UNBOUND", "INVALID") for Reference in References)
	return dict(Hypothesis, evidence=References, reuse_allowed=Allowed,
		status="CANDIDATE_EXPLANATION" if Allowed else "HISTORY_ONLY_NOT_REUSE", validated=False,
		evidence_coverage="AUTHOR_REFERENCES_NOT_PROOF" if References else "NOT_SUPPLIED")


def compare_routes(project, Routes, Hypotheses=None, IncludeAffected=False, _Locked=False):
	if(not _Locked):
		with library.writer_lock(library.library_root(project)):
			return compare_routes(project, Routes, Hypotheses, IncludeAffected, True)
	Paths = list(dict.fromkeys(Routes))
	if(len(Paths) < 2):
		raise ValueError("compare at least two explicit routes")
	library.gated_rows(project, [])
	Records = [read_route(project, PathValue, IncludeAffected, True) for PathValue in Paths]
	Hypotheses = [] if Hypotheses is None else Hypotheses
	if(isinstance(Hypotheses, dict)):
		Hypotheses = [Hypotheses]
	if(not isinstance(Hypotheses, list)):
		raise ValueError("hypotheses must be an object or a list of objects")
	Candidates = []
	for Hypothesis in Hypotheses:
		if(not isinstance(Hypothesis, dict) or any(not isinstance(Hypothesis.get(Key), str) or not Hypothesis[Key].strip() for Key in ("explanation", "prediction", "test", "scope"))):
			raise ValueError("each supplied hypothesis needs an explanation, scope, prediction and test")
		Candidate = dict(Hypothesis, origin="AUTHOR_SUPPLIED", evidence=library.bind_references(project, Hypothesis.get("evidence", [])))
		Candidate = hypothesis_view(project, Candidate)
		if(not Candidate["reuse_allowed"] and not IncludeAffected):
			raise ValueError("REUSE_BLOCKED: candidate explanation cites changed or quarantined evidence; use explicit history inspection")
		Candidates.append(Candidate)
	Transforms = [set(text_items(Record["experience"].get("transformations", []))) for Record in Records]
	Shared = sorted(set.intersection(*Transforms))
	Comparison = dict(schema_version=2, kind="route_comparison", status="CANDIDATE_COMPARISON",
		routes=Records, shared_transformations=Shared, hypotheses=Candidates,
		interpretation="Shared labels are exact text matches, not inferred equivalence or mathematical evidence.",
		accepted_graph_modified=False)
	Comparison["dimensions"] = {Key: [dict(path=Record["path"], recorded=Record["experience"].get(Key, [])) for Record in Records] for Key in COMPARISON_FIELDS}
	Comparison["next_checks"] = [dict(path=Record["path"], reconsider_when=Record["experience"].get("reconsider_when", []), complementary_lemma=Record["experience"].get("complementary_lemma", [])) for Record in Records]
	Comparison["reuse_allowed"] = all(Record["reuse_allowed"] for Record in Records) and all(Candidate["reuse_allowed"] for Candidate in Candidates)
	if(not Comparison["reuse_allowed"]):
		Comparison["status"] = "HISTORY_ONLY_NOT_REUSE"
	Data = library.json_bytes(Comparison)
	PathValue = library.inside(project, library.library_root(project) / "comparisons" / (library.digest(Data) + ".json"))
	with nullcontext():
		for Record in Records:
			if(library.digest(library.inside(project, Record["path"]).read_bytes()) != Record["sha256"]):
				raise ValueError("route changed while comparing; read the current route")
		library.immutable_write(PathValue, Data)
	return dict(path=library.relative(project, PathValue), sha256=library.digest(Data), **Comparison)


def read_comparison(project, PathValue, _Locked=False):
	if(not _Locked):
		with library.writer_lock(library.library_root(project)):
			return read_comparison(project, PathValue, True)
	library.gated_rows(project, [])
	PathValue = library.inside(project, PathValue)
	Data = PathValue.read_bytes()
	Record = json.loads(Data)
	if(Record.get("kind") != "route_comparison" or library.digest(Data) != PathValue.stem):
		raise ValueError("comparison identity mismatch")
	Routes = []
	for Route in Record["routes"]:
		try:
			Current = library.read_card(project, Route["path"], True, _Locked=True)
			State = "CURRENT" if Current["sha256"] == Route["sha256"] else "STALE"
			Allowed = Current["reuse_allowed"] and State == "CURRENT"
		except OSError:
			State = "MISSING"
			Allowed = False
		Routes.append(dict(Route, binding_state=State, reuse_allowed=Allowed, correction_state=Current["correction_state"] if State != "MISSING" else dict(status="missing"), trust="RETRIEVAL_ONLY_REVALIDATE_APPLICATION" if Allowed else "HISTORY_ONLY_NOT_REUSE"))
	Candidates = [hypothesis_view(project, Hypothesis) for Hypothesis in Record["hypotheses"]]
	Allowed = all(Route["reuse_allowed"] for Route in Routes) and all(Candidate["reuse_allowed"] for Candidate in Candidates)
	return dict(Record, routes=Routes, hypotheses=Candidates, reuse_allowed=Allowed, status=Record["status"] if Allowed else "HISTORY_ONLY_NOT_REUSE", path=library.relative(project, PathValue), sha256=library.digest(Data))


def markdown_text(Value):
	return str(Value).replace("\r", "").replace("<!--", "&lt;!--")


def markdown_link(project, Output, Reference):
	if(not Reference.get("path")):
		return markdown_text(Reference.get("url", Reference.get("source_id", "unbound reference")))
	try:
		PathValue = library.inside(project, Reference["path"])
	except (ValueError, TypeError):
		return markdown_text(Reference["path"]) + " [INVALID_PATH]"
	Link = os.path.relpath(PathValue, Output.parent).replace("\\", "/")
	return "[" + markdown_text(Reference["path"]).replace("[", "\\[").replace("]", "\\]") + "](<" + Link.replace(">", "%3E") + ">)"


def replace_generated(Before, Payload):
	Text = Before.decode("utf-8")
	if(Text.count(START) != Text.count(END) or Text.count(START) > 1):
		raise ValueError("understanding page markers are malformed; human content was not changed")
	HashLine = HASH_PREFIX + library.digest(Payload.encode("utf-8")) + " -->\n"
	Block = START + "\n" + HashLine + Payload + END
	if(START not in Text):
		return (Text + ("\n\n" if Text else "") + Block + "\n").encode("utf-8")
	StartOffset, EndOffset = Text.index(START), Text.index(END)
	if(StartOffset > EndOffset):
		raise ValueError("understanding page markers are reversed")
	Old = Text[StartOffset + len(START) + 1:EndOffset]
	Match = re.match(re.escape(HASH_PREFIX) + r"([0-9a-f]{64}) -->\n", Old)
	if(not Match or library.digest(Old[Match.end():].encode("utf-8")) != Match[1]):
		raise ValueError("generated region has manual edits; move them outside the markers before refreshing, all bytes retained")
	return (Text[:StartOffset] + Block + Text[EndOffset + len(END):]).encode("utf-8")


def update_understanding(project, Routes=None, Comparisons=None, OutputPath=None):
	Existing = library.inside(project, "docs/PROJECT_UNDERSTANDING.md")
	Output = library.inside(project, OutputPath or (Existing if Existing.exists() else library.library_root(project).parent / "understanding.md"))
	Before = Output.read_bytes() if Output.exists() else None
	with library.writer_lock(library.library_root(project)):
		library.gated_rows(project, [])
	if(Output.suffix != ".md"):
		raise ValueError("the understanding page must be Markdown")
	if(Routes is None):
		Index = library.read_json(library.inside(project, "index/tools.json"))
		Routes = [Row["location"] for Row in Index["items"] if Row.get("kind") == "experience" and Row.get("pointer_state") == "CURRENT"]
	if(any(library.inside(project, PathValue) == Output for PathValue in Routes)):
		raise ValueError("the output page cannot also be an input card")
	Records, Reports, Issues = [], [], []
	for PathValue in dict.fromkeys(Routes):
		try:
			Records.append(read_route(project, PathValue))
		except (OSError, ValueError, TypeError, KeyError) as Error:
			Issues.append(library.issue(PathValue, Error))
	for PathValue in dict.fromkeys(Comparisons or []):
		try:
			Reports.append(read_comparison(project, PathValue))
		except (OSError, ValueError, TypeError, KeyError) as Error:
			Issues.append(library.issue(PathValue, Error))
	Lines = ["\n## Evidence and candidate explanations", "",
		"This section assembles recorded statements. It does not establish their mathematical validity.",
		"Write questions, intuition and decisions outside the generated markers.", ""]
	for Record in Records:
		Experience = Record["experience"]
		Lines.extend(["### " + markdown_text(Record["title"]), "",
			markdown_link(project, Output, Record), "",
			"- Reported evidence: " + markdown_text(Record["evidence_status"]),
			"- Outcome: " + markdown_text(Experience.get("outcome", "unknown")),
			"- Failure kind: " + markdown_text(Experience.get("failure_kind") or "not recorded"),
			"- Scope: " + markdown_text(Record["conditions"]),
			"- Recorded conclusion: " + markdown_text(Experience.get("conclusion") or Record["summary"])])
		for Key in ("mechanism", "transformations", "reconsider_when", "not_applicable_to"):
			for Value in text_items(Experience.get(Key)):
				Lines.append("- " + Key.replace("_", " ").capitalize() + ": " + markdown_text(Value))
		for Key in ("evidence", "resources", "sources"):
			for Reference in Record[Key]:
				Lines.append("- " + Key.capitalize() + ": " + markdown_link(project, Output, Reference) + " [" + Reference["binding_state"] + "]")
		Lines.append("")
	for Report in Reports:
		Lines.extend(["### Candidate route comparison", "", markdown_link(project, Output, Report), ""])
		for Route in Report["routes"]:
			Lines.append("- Input " + markdown_link(project, Output, Route) + ": " + Route["binding_state"])
		if(not Report["reuse_allowed"]):
			Lines.append("- Historical discussion only. Changed or quarantined inputs do not support reuse of these explanations.")
			continue
		for Hypothesis in Report["hypotheses"]:
			Lines.extend(["", "- Candidate explanation: " + markdown_text(Hypothesis["explanation"]),
				"- Scope: " + markdown_text(Hypothesis["scope"]),
				"- Testable prediction: " + markdown_text(Hypothesis["prediction"]),
				"- Proposed test: " + markdown_text(Hypothesis["test"])])
		Lines.append("")
	if(Issues):
		Lines.extend(["### Unavailable records", ""])
		Lines.extend("- " + markdown_text(Item["path"]) + ": " + markdown_text(Item["error"]) for Item in Issues)
	Payload = "\n".join(Lines).rstrip("\n") + "\n\n"
	with library.writer_lock(library.library_root(project)):
		library.gated_rows(project, [])
		if((Output.read_bytes() if Output.exists() else None) != Before):
			raise ValueError("understanding page changed concurrently; all human bytes retained")
		for Record in Records:
			if(library.digest(library.inside(project, Record["path"]).read_bytes()) != Record["sha256"]):
				raise ValueError("an input changed while assembling the page; retry")
			library.read_card(project, Record["path"], _Locked=True)
		for Report in Reports:
			Current = read_comparison(project, Report["path"], True)
			if(Current["reuse_allowed"] != Report["reuse_allowed"]):
				raise ValueError("comparison applicability changed while assembling; retry")
		After = replace_generated(Before or b"# Project understanding\n\n## Human notes\n\n", Payload)
		if(After != Before):
			library.atomic_write(Output, After, Before)
	return dict(path=library.relative(project, Output), sha256=library.digest(After),
		reused=Before == After, assembled_routes=len(Records), assembled_comparisons=len(Reports),
		issues=Issues, status="ASSEMBLED_RESEARCH_NOTES", accepted_graph_modified=False)


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Sub = Parser.add_subparsers(dest="command", required=True)
	Record = Sub.add_parser("record")
	Record.add_argument("--project", required=True)
	Record.add_argument("--input", required=True)
	Record.add_argument("--tool")
	Record.add_argument("--expected-sha256")
	Compare = Sub.add_parser("compare")
	Compare.add_argument("--project", required=True)
	Compare.add_argument("--route", action="append", required=True)
	Compare.add_argument("--hypothesis", help="JSON object or list: explanation, scope, prediction and test")
	Compare.add_argument("--include-affected", action="store_true", help="explicit history discussion only; never reuse")
	Understanding = Sub.add_parser("understanding")
	Understanding.add_argument("--project", required=True)
	Understanding.add_argument("--route", action="append")
	Understanding.add_argument("--comparison", action="append")
	Understanding.add_argument("--output")
	Args = Parser.parse_args()
	try:
		if(Args.command == "record"):
			Result = record_experience(Args.project, library.read_json(Path(Args.input)), Args.tool, Args.expected_sha256)
		elif(Args.command == "compare"):
			Hypotheses = library.read_json(Path(Args.hypothesis)) if Args.hypothesis else None
			Result = compare_routes(Args.project, Args.route, Hypotheses, Args.include_affected)
		else:
			Result = update_understanding(Args.project, Args.route, Args.comparison, Args.output)
		print(json.dumps(Result, ensure_ascii=False))
		return 0
	except (OSError, ValueError, TypeError, KeyError) as Error:
		print(json.dumps(dict(verdict="INVALID", error=str(Error)), ensure_ascii=False))
		return 1


if(__name__ == "__main__"):
	raise SystemExit(main())
