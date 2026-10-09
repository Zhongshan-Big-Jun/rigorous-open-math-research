#!/usr/bin/env python3
"""Capture source bytes, retrieve bounded passages, index tool cards and annotate them.

All records are retrieval aids, never accepted mathematical premises. This tool
does not search the network, extract PDFs or modify a Blueprint accepted graph.
Feed it actual browser retrievals or extracted text with the raw source attached.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from contextlib import contextmanager, nullcontext
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit

try:
	import yaml
except ImportError:
	yaml = None

START = "<!-- research-tool-pointers:v1:start -->"
END = "<!-- research-tool-pointers:v1:end -->"
NOTE_KINDS = ("retrieval_hint", "applicability", "correction", "failure", "observation")
POINTER_SCHEMA = "tool-pointers/v2"
METADATA_VIEW = "current-fields/v1"
CLAIM_FIELDS = ("title", "summary", "aliases", "tags", "kind", "conditions", "scope", "applicability", "evidence_status", "experience", "problem_ids", "objects", "parameter_scope", "tool_types", "missing_bridges", "relations", "sources", "evidence", "resources", "lean")
CONTEXT_SCRIPT_NAMES = ("research_context.py", "research_library.py", "research_experience.py", "research_corrections.py", "research_review.py")
CONTEXT_SCRIPT_DIR = Path(__file__).resolve().parent
CONTEXT_VERSION_PATH = CONTEXT_SCRIPT_DIR.parents[2] / ".codex-plugin/plugin.json"
# Bind one process epoch before a knowledge view can use any of these modules.
# Updating source in a warm interpreter requires a fresh Python process.
LOADED_CONTEXT_HASHES = {Name: hashlib.sha256((CONTEXT_SCRIPT_DIR / Name).read_bytes()).hexdigest() for Name in CONTEXT_SCRIPT_NAMES}
LOADED_CONTEXT_VERSION_BYTES = CONTEXT_VERSION_PATH.read_bytes()


def utc_now():
	return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def digest(Data):
	return hashlib.sha256(Data).hexdigest()


def file_digest(PathValue):
	Hash = hashlib.sha256()
	with Path(PathValue).open("rb") as Handle:
		for Block in iter(lambda: Handle.read(1024 * 1024), b""):
			Hash.update(Block)
	return Hash.hexdigest()


def context_code_identity():
	Current = {Name: file_digest(CONTEXT_SCRIPT_DIR / Name) for Name in CONTEXT_SCRIPT_NAMES}
	if(Current != LOADED_CONTEXT_HASHES or CONTEXT_VERSION_PATH.read_bytes() != LOADED_CONTEXT_VERSION_BYTES):
		raise ValueError("knowledge code changed since loading; start a new Python process")
	return dict(version=json.loads(LOADED_CONTEXT_VERSION_BYTES)["version"], script_hashes=dict(LOADED_CONTEXT_HASHES))


def json_bytes(Data):
	return (json.dumps(Data, ensure_ascii=False, sort_keys=True, indent="\t", allow_nan=False) + "\n").encode("utf-8")


def read_json(path):
	return json.loads(path.read_text(encoding="utf-8-sig"))


def inside(project, path):
	Root = Path(project).resolve()
	Target = (Root / path).resolve()
	Target.relative_to(Root)
	if(Target == Root):
		raise ValueError("a file or subdirectory inside the project is required")
	return Target


def library_root(project):
	ConfigPath = Path(project) / "blueprint-project.json"
	ResearchRoot = "research"
	if(ConfigPath.is_file()):
		ResearchRoot = read_json(ConfigPath).get("paths", dict()).get("research_root", ResearchRoot)
	return inside(project, Path(ResearchRoot) / "library")


def relative(project, path):
	return path.resolve().relative_to(Path(project).resolve()).as_posix()


def issue(path, Error):
	return dict(path=str(path), state="INVALID", error=str(Error))


def read_metadata(Raw):
	Text = Raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
	Header = re.match(r"\A---[ \t]*\n(.*?)^---[ \t]*(?:\n|\Z)(.*)\Z", Text, re.M | re.S)
	if(not Header):
		if(re.match(r"\A---[ \t]*(?:\n|$)", Text)):
			raise ValueError("opening header has no closing delimiter")
		return dict(), Text, "ABSENT"
	try:
		Front = json.loads(Header[1])
	except ValueError:
		if(yaml is None):
			raise ValueError("PyYAML is needed to read this legacy YAML header")
		try:
			Front = yaml.safe_load(Header[1])
		except yaml.YAMLError as Error:
			raise ValueError(str(Error)) from Error
	Front = dict() if Front is None else Front
	if(not isinstance(Front, dict)):
		raise ValueError("tool frontmatter must be a mapping")
	for Key in ("aliases", "applicability", "sources", "evidence", "resources", "lean", "dependencies", "depends_on", "relations"):
		if(Key in Front and not isinstance(Front[Key], list)):
			raise ValueError(f"{Key} must be a list")
	if("conditions" in Front and not isinstance(Front["conditions"], (str, list))):
		raise ValueError("conditions must be text or a list")
	if("experience" in Front and not isinstance(Front["experience"], dict)):
		raise ValueError("experience must be an object")
	if("_field_provenance" in Front and not isinstance(Front["_field_provenance"], dict)):
		raise ValueError("_field_provenance must be an object")
	if(any(not isinstance(Value, dict) for Value in Front.get("_field_provenance", {}).values())):
		raise ValueError("each field provenance binding must be an object")
	return Front, Header[2], "VALID"


def derived_status(Front):
	Statuses = {str(Row.get("status", "")) for Row in Front.get("applicability", []) if isinstance(Row, dict)}
	for Status, Lifecycle in (("active", "active"), ("conditional", "conditional"), ("retired", "archived")):
		if(Status in Statuses):
			return Lifecycle
	return "unclassified"


def snapshot_card(project, Raw):
	Path = inside(project, library_root(project) / "card-versions" / (digest(Raw) + ".md"))
	immutable_write(Path, Raw)
	return relative(project, Path)


def bind_references(project, References):
	if(not isinstance(References, list)):
		raise ValueError("references must be a list")
	Bound = []
	for Reference in References:
		Reference = dict(path=Reference) if isinstance(Reference, str) else dict(Reference)
		if(Reference.get("path")):
			Path = inside(project, Reference["path"])
			Hash = file_digest(Path)
			if(Reference.get("sha256", Hash) != Hash):
				raise ValueError(f"referenced bytes changed: {Reference['path']}")
			Reference.update(path=relative(project, Path), sha256=Hash)
		if(Reference.get("source_id")):
			Capture = capture_reference(project, Reference["source_id"])
			if(Reference.get("path") and inside(project, Reference["path"]) not in {inside(project, Member["path"]) for Member in Capture["capture_members"]}):
				raise ValueError("path and source_id do not describe the same captured source")
		elif(not Reference.get("path") and not Reference.get("url")):
			raise ValueError("a reference needs a local path, captured source_id or URL")
		Bound.append(Reference)
	return Bound


def capture_identity(Record):
	Keys = ("url", "version", "raw_sha256", "text_sha256")
	if(not isinstance(Record, dict) or any(not isinstance(Record.get(Key), str) or not Record[Key] for Key in Keys)):
		return None
	return tuple(Record[Key] for Key in Keys)


def capture_reference(project, SourceId):
	Record = read_source(project, SourceId, 1, 1)["metadata"]
	Folder = inside(project, library_root(project) / "sources" / SourceId)
	Members = [dict(path=relative(project, inside(project, Folder / Name)), sha256=file_digest(Folder / Name)) for Name in ("source.json", "raw.bin", "text.txt")]
	return dict(source_id=SourceId, captured_source=Record, capture_members=Members)


def capture_metadata_id(project, PathValue):
	return capture_member_id(project, PathValue) if Path(PathValue).name.casefold() == "source.json" else None


def capture_member_id(project, PathValue):
	PathValue = inside(project, PathValue)
	SourceRoot = inside(project, library_root(project) / "sources")
	if(PathValue.name.casefold() in ("source.json", "raw.bin", "text.txt") and PathValue.parent.parent == SourceRoot and re.fullmatch(r"[0-9a-f]{64}", PathValue.parent.name, re.I)):
		return PathValue.parent.name.casefold()
	return None


def capture_alias_rows(project, States):
	"""Read registered metadata snapshots, even if the old live capture is gone.

	Only the exact URL/version/raw/text tuple shares correction identity. Titles
	and reading annotations do not release its old exact-version obligations.
	"""
	Captured = [State for State in States if State.get("capture_members") and State["binding_state"] == "CURRENT"]
	if(not Captured):
		return []
	import research_corrections as corrections
	try:
		Store = corrections.load_store(project)
		SourceRoot = inside(project, library_root(project) / "sources")
		Rows = []
		for Node in Store["nodes"].values():
			PathValue = inside(project, Node["location"])
			if(PathValue.name.casefold() != "source.json" or PathValue.parent.parent != SourceRoot or not re.fullmatch(r"[0-9a-f]{64}", PathValue.parent.name)):
				continue
			Raw = corrections.version_bytes(project, Node)
			try:
				Recorded = json.loads(Raw.decode("utf-8-sig"))
			except (ValueError, UnicodeError):
				# A registered malformed input remains a historical issue; its
				# missing source identity cannot establish an equivalence.
				continue
			Identity = capture_identity(Recorded)
			for State in Captured:
				if(Identity is None or Identity != capture_identity(State["captured_source"])):
					continue
				Alias = dict(path=Node["location"], sha256=Node["sha256"], source_id=PathValue.parent.name,
					snapshot=relative(project, corrections.version_path(project, Node["sha256"])), basis="REGISTERED_EXACT_URL_VERSION_RAW_TEXT_NOT_MATHEMATICAL_EQUIVALENCE")
				State.setdefault("capture_aliases", []).append(Alias)
				Rows.append(dict(location=Alias["path"], sha256=Alias["sha256"], dependencies_known=False))
		return Rows
	except (OSError, ValueError, TypeError, KeyError, RuntimeError) as Error:
		raise ValueError("CORRECTIONS_INVALID: captured source alias identity: " + str(Error)) from Error


def reference_states(project, References):
	States = []
	for Reference in References:
		try:
			if(not isinstance(Reference, dict)):
				raise ValueError("reference is not an object")
			State = dict(Reference, binding_state="UNBOUND_REFERENCE")
			if(Reference.get("path")):
				PathValue = inside(project, Reference["path"])
				Location = relative(project, PathValue)
				if(Location != Reference["path"]):
					State["requested_path"] = Reference["path"]
				State["path"] = Location
				Hash = file_digest(PathValue)
				State["binding_state"] = "CURRENT" if Reference.get("sha256") == Hash else "STALE_OR_UNBOUND"
				CaptureId = capture_member_id(project, PathValue)
				if(State["binding_state"] == "CURRENT" and CaptureId and not Reference.get("source_id")):
					State.update(capture_reference(project, CaptureId))
			if(Reference.get("source_id")):
				Capture = capture_reference(project, Reference["source_id"])
				if(Reference.get("path") and PathValue not in {inside(project, Member["path"]) for Member in Capture["capture_members"]}):
					raise ValueError("path and source_id do not describe the same captured source")
				State.update(Capture)
				if(not Reference.get("path")):
					State["binding_state"] = "CURRENT"
		except (OSError, ValueError, TypeError, KeyError) as Error:
			State = dict(reference=Reference, binding_state="INVALID", error=str(Error))
		States.append(State)
	RefRows = []
	for State in States:
		if(State.get("path") and State["binding_state"] == "CURRENT"):
			try:
				Front = read_metadata(inside(project, State["path"]).read_bytes())[0] if Path(State["path"]).suffix == ".md" else {}
			except (ValueError, TypeError):
				Front = {}
			RefRows.append(dict(location=relative(project, inside(project, State["path"])), sha256=State["sha256"], tool_id=Front.get("tool_id", Front.get("slug")), dependencies_known=False))
		if(State.get("capture_members") and State["binding_state"] == "CURRENT"):
			RefRows.extend(dict(location=Member["path"], sha256=Member["sha256"], dependencies_known=False) for Member in State["capture_members"])
	RefRows.extend(capture_alias_rows(project, States))
	if(RefRows):
		Gated = gated_rows(project, RefRows)
		ByVersion = {(Row["location"], Row["sha256"]): Row for Row in Gated}
		for State in States:
			if(State.get("capture_members") and State["binding_state"] == "CURRENT"):
				Members = [dict(Member, reference_reuse_allowed=ByVersion[(Member["path"], Member["sha256"])]["reuse_allowed"], correction_state=ByVersion[(Member["path"], Member["sha256"])]["correction_state"]) for Member in State["capture_members"]]
				Aliases = [dict(Alias, reference_reuse_allowed=ByVersion[(Alias["path"], Alias["sha256"])]["reuse_allowed"], correction_state=ByVersion[(Alias["path"], Alias["sha256"])]["correction_state"]) for Alias in State.get("capture_aliases", [])]
				Allowed = all(Member["reference_reuse_allowed"] for Member in Members + Aliases)
				State.update(capture_members=Members, reference_reuse_allowed=Allowed,
					capture_aliases=Aliases, correction_alias_coverage="MATCHING_REGISTERED_CAPTURE_METADATA_VERSIONS",
					correction_state=dict(status="clear" if Allowed else "needs_review", reuse_allowed=Allowed, issues=sorted({IssueId for Member in Members + Aliases for IssueId in Member["correction_state"]["issues"]}), members=Members, aliases=Aliases),
					trust="BYTE_BINDING_ONLY_REVALIDATE_SOURCE" if Allowed else "HISTORY_ONLY_NOT_REUSE")
			elif((State.get("path"), State.get("sha256")) in ByVersion):
				Row = ByVersion[(State["path"], State["sha256"])]
				State.update(reference_reuse_allowed=Row["reuse_allowed"], correction_state=Row["correction_state"],
					trust="BYTE_BINDING_ONLY_REVALIDATE_SOURCE" if Row["reuse_allowed"] else "HISTORY_ONLY_NOT_REUSE")
	return States


def lean_reference_states(project, References):
	States = []
	for Reference in References:
		if(not isinstance(Reference, dict)):
			States.append(dict(reference=Reference, trust="INVALID_REFERENCE"))
			continue
		State = dict(Reference, trust="UNVERIFIED_DECLARATION_REFERENCE", machine_execution="UNKNOWN_NOT_RECHECKED", exact_root="UNKNOWN_NOT_RECHECKED", semantic_correspondence="UNKNOWN_NOT_RECHECKED",
			open_connections=Reference.get("open_connections", ["Model connections were not recorded."]), library_acceptance="NOT_ESTABLISHED", blueprint_acceptance="NOT_ESTABLISHED")
		for Key in ("source", "verification", "semantic_review"):
			if(Reference.get(Key)):
				State[Key] = reference_states(project, [Reference[Key]])[0]
		if(Reference.get("definitions")):
			State["definitions"] = reference_states(project, Reference["definitions"])
		if(isinstance(Reference.get("actual_type"), dict) and Reference["actual_type"].get("path")):
			State["actual_type"] = reference_states(project, [Reference["actual_type"]])[0]
		State["identity_fields_missing"] = [Key for Key in ("repository", "commit", "module", "declaration", "environment", "actual_type") if not Reference.get(Key)]
		States.append(State)
	return States


def save_card(project, Data, ToolPath=None, ExpectedHash=None):
	"""Save a small card. Changed existing bytes require the hash the caller read."""
	Data = dict(Data)
	Content = Data.pop("content", "")
	if(not isinstance(Content, str) or not Content.strip()):
		raise ValueError("a card needs nonempty content")
	for Key in ("sources", "evidence", "resources"):
		if(Key in Data):
			Data[Key] = bind_references(project, Data[Key])
	if("relations" in Data):
		from research_context import bind_relations
		Data["relations"] = bind_relations(project, Data["relations"])
	if("lean" in Data and (not isinstance(Data["lean"], list) or any(not isinstance(Item, dict) for Item in Data["lean"]))):
		raise ValueError("lean must be a list of declaration references")
	if("lean" in Data):
		Data["lean"] = [dict(Item) for Item in Data["lean"]]
		for Reference in Data["lean"]:
			for Key in ("source", "verification", "semantic_review"):
				if(Reference.get(Key)):
					Reference[Key] = bind_references(project, [Reference[Key]])[0]
			if(Reference.get("definitions")):
				Reference["definitions"] = bind_references(project, Reference["definitions"])
			if(isinstance(Reference.get("actual_type"), dict) and Reference["actual_type"].get("path")):
				Reference["actual_type"] = bind_references(project, [Reference["actual_type"]])[0]
	ToolId = str(Data.get("tool_id") or (Path(ToolPath).stem if ToolPath else "tool-" + digest(json_bytes([Data, Content]))[:20]))
	PathValue = ToolPath or "tools/" + ToolId + ".md"
	Target = inside(project, PathValue)
	if(Target.suffix != ".md" or Target.name.lower() == "readme.md"):
		raise ValueError("a card needs its own .md path")
	with writer_lock(library_root(project)):
		import research_corrections as corrections
		if("depends_on" in Data):
			Data["dependencies"] = corrections.card_dependencies(Data)
			Data.pop("depends_on")
		if("dependencies" in Data):
			Data["dependencies"] = corrections.bind_dependencies(project, Data["dependencies"], Capture=True)
		Old = Target.read_bytes() if Target.exists() else None
		if(Old is not None):
			Front, OldBody, _ = read_metadata(Old)
			ToolId = str(Front.get("tool_id") or Front.get("slug") or ToolId)
			if(Data.get("tool_id", ToolId) != ToolId):
				raise ValueError("keep the existing card identity; create a separate card for a different tool")
			Supplied = set(Data)
			Provenance = dict(Front.get("_field_provenance", {}))
			BodyHash = digest((Content.rstrip("\n") + "\n").encode("utf-8"))
			if(OldBody != Content.rstrip("\n") + "\n"):
				for Key in CLAIM_FIELDS:
					if(Key in Front and Key not in Supplied):
						Provenance.setdefault(Key, dict(origin="inherited_author_field", body_sha256=digest(OldBody.encode("utf-8")), source_sha256=digest(Old)))
			for Key in Supplied & set(CLAIM_FIELDS):
				if(OldBody != Content.rstrip("\n") + "\n" or Key in Provenance):
					Provenance[Key] = dict(origin="author_explicit", body_sha256=BodyHash)
			Data = dict(Front, **Data)
			if(Provenance):
				Data["_field_provenance"] = Provenance
			if("dependencies" in Data):
				Data.pop("depends_on", None)
		Data.update(tool_id=ToolId)
		Data.setdefault("evidence_status", "CANDIDATE")
		Raw = ("---\n" + json.dumps(Data, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n---\n" + Content.rstrip("\n") + "\n").encode("utf-8")
		read_metadata(Raw)
		if(Old != Raw and Old is not None and digest(Old) != ExpectedHash):
			raise ValueError("existing card differs; pass its current --expected-sha256")
		if(Old is None and ExpectedHash is not None):
			raise ValueError("expected an existing card but it is missing")
		if(Old is not None):
			snapshot_card(project, Old)
			corrections.register_version(project, relative(project, Target), Old, ToolId)
		Version = snapshot_card(project, Raw)
		corrections.register_version(project, relative(project, Target), Raw, ToolId)
		if(Old != Raw):
			atomic_write(Target, Raw, Old)
	return dict(tool_id=ToolId, location=relative(project, Target), sha256=digest(Raw),
		version=Version, reused=Old == Raw, trust="RETRIEVAL_ONLY_REVALIDATE_APPLICATION")


def immutable_write(path, Data):
	path.parent.mkdir(parents=True, exist_ok=True)
	if(path.exists()):
		if(path.read_bytes() != Data):
			raise ValueError(f"immutable record conflict: {path}")
		return
	Fd, TempPath = tempfile.mkstemp(prefix=".capture-", dir=path.parent)
	try:
		with os.fdopen(Fd, "wb") as Handle:
			Handle.write(Data)
			Handle.flush()
			os.fsync(Handle.fileno())
		try:
			os.link(TempPath, path)
		except FileExistsError:
			if(path.read_bytes() != Data):
				raise ValueError(f"immutable record conflict: {path}")
	finally:
		os.unlink(TempPath)


_UNSET = object()


def atomic_write(path, Data, ExpectedData=_UNSET):
	path.parent.mkdir(parents=True, exist_ok=True)
	Fd, TempPath = tempfile.mkstemp(prefix=".library-", dir=path.parent)
	try:
		with os.fdopen(Fd, "wb") as Handle:
			Handle.write(Data)
			Handle.flush()
			os.fsync(Handle.fileno())
		if(ExpectedData is not _UNSET and (path.read_bytes() if path.exists() else None) != ExpectedData):
			raise ValueError("concurrent file edit; original bytes retained: " + str(path))
		os.replace(TempPath, path)
	finally:
		if(os.path.exists(TempPath)):
			os.unlink(TempPath)


@contextmanager
def writer_lock(Root):
	Root.mkdir(parents=True, exist_ok=True)
	LockPath = Root / "writer.lock"
	with LockPath.open("x", encoding="utf-8") as Handle:
		Handle.write(f"pid={os.getpid()} time={utc_now()}\n")
	try:
		yield
	finally:
		LockPath.unlink()


def find_sources(project, query, limit=8, SearchContent=False):
	if(not query.strip() or not 1 <= limit <= 50):
		raise ValueError("query is required and limit must be in 1..50")
	Hits, Issues = [], []
	Terms = query.casefold().split()
	for path in sorted((library_root(project) / "sources").glob("*/source.json")):
		try:
			path = inside(project, path)
			Record = read_json(path)
			if(digest(json_bytes(Record)) != path.parent.name):
				raise ValueError("source metadata hash mismatch")
			SearchText = " ".join(Record[Key] for Key in ("url", "title", "version")).casefold()
			if(SearchContent):
				read_source(project, path.parent.name, 1, 1)
				SearchText += " " + (path.parent / "text.txt").read_text(encoding="utf-8").casefold()
		except (OSError, ValueError, KeyError, TypeError) as Error:
			Issues.append(issue(path, Error))
			continue
		Score = sum(Term in SearchText for Term in Terms)
		if(Score):
			Hits.append(dict(score=Score, source_id=path.parent.name,
				source=relative(project, path), **Record))
	Hits.sort(key=lambda Item: (-Item["score"], Item["source_id"]))
	return dict(verdict="RETRIEVAL_ONLY", hits=Hits[:limit], total_matches=len(Hits), issues=Issues)


def capture_source(project, InputPath, url, version, title, TextPath=None, method="provided-text", SourceKind="primary", Coverage=None, Locators=None):
	if(urlsplit(url).scheme not in ("http", "https") or not urlsplit(url).netloc):
		raise ValueError("a real HTTP(S) source locator is required")
	if(not version.strip() or not title.strip()):
		raise ValueError("source title and version are required")
	Raw = Path(InputPath).read_bytes()
	TextBytes = Path(TextPath or InputPath).read_bytes()
	if(max(len(Raw), len(TextBytes)) > 32 * 1024 * 1024):
		raise ValueError("source exceeds 32 MiB; provide a scoped extraction")
	Text = TextBytes.decode("utf-8")
	if(not Text.strip() or "\x00" in Text):
		raise ValueError("provide readable UTF-8 text; extract PDF/OCR text separately")
	Record = dict(schema_version=1, url=url, version=version, title=title,
		source_kind=SourceKind, extraction_method=method, raw_sha256=digest(Raw),
		text_sha256=digest(TextBytes), line_count=len(Text.splitlines()),
		trust="UNVERIFIED_SOURCE_CONTENT")
	if(Coverage is not None):
		Record["coverage"] = str(Coverage)
	if(Locators):
		Record["original_locators"] = list(Locators)
	SourceId = digest(json_bytes(Record))
	Folder = inside(project, library_root(project) / "sources" / SourceId)
	with writer_lock(library_root(project)):
		immutable_write(inside(project, Folder / "raw.bin"), Raw)
		immutable_write(inside(project, Folder / "text.txt"), TextBytes)
		immutable_write(inside(project, Folder / "source.json"), json_bytes(Record))
	return dict(source_id=SourceId, source=relative(project, Folder / "source.json"), **Record)


def read_source(project, SourceId, StartLine=1, MaxLines=80, StartOffset=None):
	if(not re.fullmatch(r"[0-9a-f]{64}", SourceId)):
		raise ValueError("invalid source content ID")
	Folder = inside(project, library_root(project) / "sources" / SourceId)
	Record = read_json(inside(project, Folder / "source.json"))
	if(digest(json_bytes(Record)) != SourceId):
		raise ValueError("source metadata hash mismatch")
	TextBytes = inside(project, Folder / "text.txt").read_bytes()
	if(digest(TextBytes) != Record["text_sha256"] or digest(inside(project, Folder / "raw.bin").read_bytes()) != Record["raw_sha256"]):
		raise ValueError("source bytes changed")
	if(StartLine < 1 or not 1 <= MaxLines <= 200):
		raise ValueError("start-line must be positive and max-lines must be in 1..200")
	Text = TextBytes.decode("utf-8")
	Lines = Text.splitlines(keepends=True)
	if(StartLine > len(Lines)):
		raise ValueError("start-line is beyond the source")
	Offset = sum(len(Line) for Line in Lines[:StartLine - 1]) if StartOffset is None else StartOffset
	if(not isinstance(Offset, int) or not 0 <= Offset < len(Text)):
		raise ValueError("start-offset is outside the extracted text")
	Passage = "".join(Text[Offset:].splitlines(keepends=True)[:MaxLines])[:12000]
	EndOffset = Offset + len(Passage)
	LineStarts, Position = [], 0
	for Line in Lines:
		LineStarts.append(Position)
		Position += len(Line)
	StartLine = bisect_right(LineStarts, Offset)
	EndLine = bisect_right(LineStarts, max(Offset, EndOffset - 1))
	return dict(source_id=SourceId, metadata=Record, start_line=StartLine,
		end_line=EndLine, start_offset=Offset, next_offset=EndOffset if EndOffset < len(Text) else None,
		passage_sha256=digest(Passage.encode("utf-8")), content=Passage,
		locator_note="Extraction line numbers; verify original page/theorem separately.")


def collect_notes(project, Issues=None):
	Root = library_root(project) / "annotations"
	Notes = []
	for path in sorted(Root.glob("*.json")):
		try:
			path = inside(project, path)
			Note = read_json(path)
			if(digest(json_bytes(Note)) != path.stem):
				raise ValueError("annotation content hash mismatch")
			if(any(not isinstance(Note.get(Key), str) for Key in ("tool_path", "tool_sha256", "kind", "content"))):
				raise ValueError("annotation has invalid fields")
			Notes.append(dict(Note, path=relative(project, path), sha256=digest(path.read_bytes())))
		except (OSError, ValueError, TypeError, KeyError) as Error:
			if(Issues is None):
				raise
			Issues.append(issue(path, Error))
	return Notes


def annotate(project, ToolPath, ExpectedHash=None, author="unspecified", kind="observation", locator="card", text="", SourceId=None):
	Tool = inside(project, ToolPath)
	CurrentHash = digest(Tool.read_bytes())
	ExpectedHash = CurrentHash if ExpectedHash is None else ExpectedHash
	if(CurrentHash != ExpectedHash):
		raise ValueError("tool changed since it was read; read the current card before annotating")
	if(not all(isinstance(Value, str) and Value.strip() for Value in (author, kind, locator, text))):
		raise ValueError("annotation needs author, kind, exact locator and content")
	if(SourceId):
		read_source(project, SourceId, 1, 1)
	Note = dict(schema_version=1, tool_path=relative(project, Tool), tool_sha256=CurrentHash,
		author=author, kind=kind, locator=locator, content=text, source_id=SourceId,
		status="CANDIDATE_ANNOTATION")
	NoteId = digest(json_bytes(Note))
	with writer_lock(library_root(project)):
		Raw = Tool.read_bytes()
		if(digest(Raw) != ExpectedHash):
			raise ValueError("tool changed during annotation")
		snapshot_card(project, Raw)
		immutable_write(inside(project, library_root(project) / "annotations" / (NoteId + ".json")), json_bytes(Note))
	return dict(annotation_id=NoteId, **Note)


def card_paths(project, Roots, ReadmePath=None, Issues=None):
	Paths = set()
	for ToolRoot in Roots:
		try:
			Root = inside(project, ToolRoot)
			if(not Root.is_dir()):
				raise ValueError("tool root is missing")
			for PathValue in Root.rglob("*.md"):
				try:
					Location = relative(project, inside(project, PathValue))
					if(PathValue.name.lower() != "readme.md" and Location != ReadmePath):
						Paths.add(Location)
				except (OSError, ValueError) as Error:
					if(Issues is not None):
						Issues.append(issue(PathValue, Error))
		except (OSError, ValueError) as Error:
			if(Issues is not None):
				Issues.append(issue(ToolRoot, Error))
	return Paths


def annotation_pointers(Notes, Row):
	return [dict(path=Note["path"], sha256=Note["sha256"], kind=Note["kind"],
		author=Note.get("author", "unspecified"), locator=Note.get("locator", "card"), source_id=Note.get("source_id"),
		tool_sha256=Note["tool_sha256"], state="CURRENT" if Note["tool_sha256"] == Row["sha256"] else "STALE")
		for Note in Notes if Note["tool_path"] == Row["location"]]


def card_tool_id(Front, Old, Location):
	# Current declarations outrank an optional cached/legacy pointer identity.
	return str(Front.get("tool_id") or Front.get("slug") or Old.get("tool_id") or Path(Location).stem)


def parse_card(project, Location, Raw, Old, Snapshot=True):
	MetadataError = None
	try:
		Front, Body, MetadataStatus = read_metadata(Raw)
	except (ValueError, TypeError) as Error:
		Front, Body, MetadataStatus = dict(), Raw.decode("utf-8", errors="replace"), "UNPARSEABLE"
		MetadataError = str(Error)
	ToolId = card_tool_id(Front, Old, Location)
	Headings = re.findall(r"^#\s+(.+)$", Body, re.M)
	BodyHash = digest(Body.encode("utf-8"))
	PreviousFront, PreviousBodyHash = {}, Old.get("body_sha256")
	if(Old.get("sha256") and Old["sha256"] != digest(Raw)):
		try:
			PreviousRaw = inside(project, library_root(project) / "card-versions" / (Old["sha256"] + ".md")).read_bytes()
			if(digest(PreviousRaw) != Old["sha256"]):
				raise ValueError("old metadata snapshot hash mismatch")
			PreviousFront, PreviousBody, _ = read_metadata(PreviousRaw)
			PreviousBodyHash = digest(PreviousBody.encode("utf-8"))
		except (OSError, ValueError, TypeError):
			PreviousBodyHash = None
	Provenance, Historical = {}, dict(Old.get("historical_metadata", {}))
	for Key in CLAIM_FIELDS:
		if(Key in Front):
			Binding = Front.get("_field_provenance", {}).get(Key, {})
			if(not Binding and Old.get("sha256") == digest(Raw)):
				Binding = Old.get("field_provenance", {}).get(Key, {})
			if(not isinstance(Binding, dict)):
				raise ValueError("invalid field provenance: " + Key)
			Unconfirmed = bool(Binding and Binding.get("body_sha256") != BodyHash)
			Retained = (PreviousBodyHash is not None and PreviousBodyHash != BodyHash and PreviousFront.get(Key) == Front[Key] and not Binding) or (Old.get("sha256") == digest(Raw) and Old.get("field_provenance", {}).get(Key, {}).get("state") == "INHERITED_NEEDS_REVALIDATION" and not Binding)
			State = "INHERITED_NEEDS_REVALIDATION" if Unconfirmed or Retained else "CURRENT_AUTHOR_FIELD"
			Provenance[Key] = dict(Binding, state=State, origin=Binding.get("origin", "author_explicit"), body_sha256=Binding.get("body_sha256", PreviousBodyHash if Retained else BodyHash))
			if(State != "CURRENT_AUTHOR_FIELD"):
				Historical[Key] = dict(value=Front[Key], **Provenance[Key])
			else:
				Historical.pop(Key, None)
		elif(Key in Old and Old[Key] not in ([], {}, "UNSPECIFIED", "UNKNOWN") and not (Old.get("metadata_view") == METADATA_VIEW and Key in ("title", "summary", "aliases", "kind"))):
			Historical.setdefault(Key, dict(value=Old[Key], origin="previous_index", source_sha256=Old.get("sha256"), state="INHERITED_NEEDS_REVALIDATION"))
	def current(Key, Default):
		return Front[Key] if Provenance.get(Key, {}).get("state") == "CURRENT_AUTHOR_FIELD" else Default
	Applicability = current("applicability", [])
	Lifecycle = derived_status(dict(applicability=Applicability)) if isinstance(Applicability, list) else "unclassified"
	if(Provenance.get("applicability", {}).get("state") != "CURRENT_AUTHOR_FIELD" and (Old.get("lifecycle") == "archived" or derived_status(Front) == "archived")):
		Lifecycle = "archived"
		Applicability = Front.get("applicability", Old.get("applicability", []))
		Provenance.setdefault("applicability", dict(state="INHERITED_NEEDS_REVALIDATION", origin="previous_index", source_sha256=Old.get("sha256")))
	Row = dict(Old)
	Row.update(tool_id=ToolId, location=Location, sha256=digest(Raw),
		metadata_status=MetadataStatus, metadata_error=MetadataError,
		title=str(current("title", Headings[0] if Headings else ToolId)),
		summary=str(current("summary", re.sub(r"\s+", " ", Body).strip()))[:500],
		aliases=current("aliases", []), kind=current("kind", "tool"),
		applicability=Applicability, lifecycle=Lifecycle,
		pointer_state="CURRENT", trust="RETRIEVAL_ONLY_REVALIDATE_APPLICATION")
	Defaults = dict(conditions="UNSPECIFIED", scope="UNSPECIFIED", sources=[], evidence=[], resources=[], lean=[], experience=dict(), evidence_status="UNKNOWN")
	Row["inherited_metadata"] = sorted(Historical)
	for Key, Default in Defaults.items():
		Row[Key] = Front.get(Key, Old.get(Key, Default))
	for Key in ("problem_ids", "objects", "parameter_scope", "tool_types", "missing_bridges", "relations", "tags"):
		Row[Key] = current(Key, [])
	Row["evidence_status"] = current("evidence_status", "UNKNOWN")
	Row["experience"] = current("experience", {})
	Row.update(metadata_view=METADATA_VIEW, body_sha256=BodyHash, field_provenance=Provenance, historical_metadata=Historical,
		dependencies_known=MetadataStatus != "UNPARSEABLE" and ("dependencies" in Front or "depends_on" in Front))
	Row["dependencies"] = Front.get("dependencies", Front.get("depends_on", []))
	json_bytes(Row)
	Row["version"] = snapshot_card(project, Raw) if Snapshot else relative(project, library_root(project) / "card-versions" / (digest(Raw) + ".md"))
	return Row


def make_index(project, ToolRoots=None, IndexPath="index/tools.json", ReadmePath=None, PreviousIndex=None, _Locked=False):
	import research_corrections as corrections
	Root = Path(project).resolve()
	Index = inside(Root, IndexPath)
	with (nullcontext() if _Locked else writer_lock(library_root(Root))):
		IndexBefore = Index.read_bytes() if Index.exists() else None
		if(PreviousIndex is not None and IndexBefore is not None):
			raise ValueError("--from-index requires a missing destination index; preserve an existing index before explicit recovery")
		MetadataBytes = inside(Root, PreviousIndex).read_bytes() if PreviousIndex is not None else IndexBefore
		Previous = json.loads(MetadataBytes.decode("utf-8-sig")) if MetadataBytes is not None else dict(schema_version=1, items=[])
		if(not isinstance(Previous, dict) or not isinstance(Previous.get("items"), list)):
			raise ValueError("tool index must be an object with an items array; preserve damaged bytes before rebuilding")
		RootValues = ToolRoots or Previous.get("tool_roots") or [Name for Name in ("tools", "knowledge/tools") if (Root / Name).is_dir()]
		Roots = list(dict.fromkeys(relative(Root, inside(Root, PathValue)) for PathValue in RootValues))
		ExperienceRoot = relative(Root, library_root(Root) / "experiences")
		if((Root / ExperienceRoot).is_dir() and ExperienceRoot not in Roots):
			Roots.append(ExperienceRoot)
		if(not Roots):
			raise ValueError("no card roots found; pass --tool-root")
		ReadmePath = ReadmePath if ReadmePath is not None else Previous.get("generated_readme")
		Readme = inside(Root, ReadmePath) if ReadmePath else None
		if(Readme == Index):
			raise ValueError("index and README must use different paths")
		ByPath = dict()
		for Item in Previous["items"] + Previous.get("blocked_items", []):
			if(not isinstance(Item, dict) or not isinstance(Item.get("location"), str) or Item["location"] in ByPath):
				raise ValueError("legacy index entries need distinct string locations; original index has not been changed")
			ByPath[Item["location"]] = Item
		Issues = []
		Notes = collect_notes(Root, Issues)
		# Validate the registry once for this locked refresh. Previously each
		# unchanged card re-read every registered version, making refresh O(N^2)
		# in filesystem reads. The final correction gate validates it again.
		KnownVersions, RegistryHealthy = {}, True
		if((library_root(Root) / "card-bindings-required.json").exists()):
			try:
				KnownVersions = corrections.read_versions(Root)
			except (OSError, ValueError, TypeError, KeyError, RuntimeError) as Error:
				RegistryHealthy = False
				Issues.append(issue("card-bindings", Error))
		Rows, Parsed, Reused = [], 0, 0
		Paths = card_paths(Root, Roots, relative(Root, Readme) if Readme else None, Issues)
		for Location in sorted(Paths):
			Old = ByPath.pop(Location, dict())
			try:
				Raw = inside(Root, Location).read_bytes()
				if(Previous.get("pointer_schema") == POINTER_SCHEMA and Old.get("metadata_view") == METADATA_VIEW and "scope" in Old and Old.get("sha256") == digest(Raw) and Old.get("metadata_status") != "UNPARSEABLE" and Old.get("tool_id") == card_tool_id(read_metadata(Raw)[0], Old, Location)):
					Row = dict(Old, pointer_state="CURRENT")
					Row["version"] = snapshot_card(Root, Raw)
					Reused += 1
				else:
					Row = parse_card(Root, Location, Raw, Old)
					Parsed += 1
				Row["annotations"] = annotation_pointers(Notes, Row)
				if(RegistryHealthy):
					VersionKey = (Location, digest(Raw))
					Node = KnownVersions.get(VersionKey)
					if(Node is None):
						Node = corrections.register_version(Root, Location, Raw, Row["tool_id"])
						KnownVersions[VersionKey] = Node
					Row["dependencies"] = Node["dependencies"]
				Row.pop("identity_error", None)
				Rows.append(Row)
			except (OSError, ValueError, TypeError) as Error:
				Issues.append(issue(Location, Error))
				Rows.append(dict(Old, location=Location, pointer_state="INVALID", metadata_status="UNPARSEABLE", metadata_error=str(Error)))
		Rows.extend(dict(Item, pointer_state="UNSCANNED") for Item in ByPath.values())
		ById = dict()
		for Row in Rows:
			if(Row.get("tool_id")):
				ById.setdefault(Row["tool_id"], []).append(Row)
		for ToolId, Duplicates in ById.items():
			if(len(Duplicates) > 1):
				for Row in Duplicates:
					Row["identity_error"] = f"duplicate tool ID: {ToolId}; use the exact path and resolve identity explicitly"
		Rows, CorrectionIssues = corrections.gate_rows(Root, Rows)
		Issues.extend(CorrectionIssues)
		Previous.update(items=[Row for Row in Rows if Row["reuse_allowed"]], blocked_items=[Row for Row in Rows if not Row["reuse_allowed"]], pointer_schema=POINTER_SCHEMA, tool_roots=Roots,
			generated_readme=relative(Root, Readme) if Readme else None, issues=Issues)
		ReadmeBytes, ReadmeBefore = None, None
		if(Readme):
			ReadmeBefore = Readme.read_bytes() if Readme.exists() else None
			Text = ReadmeBefore.decode("utf-8") if ReadmeBefore is not None else "# Mathematical tools\n"
			if(Text.count(START) != Text.count(END) or Text.count(START) > 1 or (START in Text and Text.index(START) > Text.index(END))):
				raise ValueError("malformed generated pointer markers")
			Table = [START, "", "## Generated retrieval pointers", "", "Cards and notes are retrieval leads. Check their scope and evidence before reuse.", "", "| Tool | Card | Annotations |", "| --- | --- | --- |"]
			for Row in Rows:
				if(Row.get("pointer_state") != "CURRENT" or not Row["reuse_allowed"]):
					continue
				Link = os.path.relpath(Root / Row["location"], Readme.parent).replace("\\", "/")
				Label = str(Row["tool_id"]).replace("|", "\\|").replace("\n", " ")
				Table.append(f"| {Label} | [card](<{Link}>) | {len(Row['annotations'])} |")
			Block = "\n".join(Table + ["", END])
			if(START in Text):
				Text = Text[:Text.index(START)] + Block + Text[Text.index(END) + len(END):]
			else:
				Text = Text + ("\n\n" if Text else "") + Block + "\n"
			ReadmeBytes = Text.encode("utf-8")
		for Row in Rows:
			if(Row.get("pointer_state") != "CURRENT"):
				continue
			try:
				if(digest(inside(Root, Row["location"]).read_bytes()) != Row["sha256"]):
					raise ValueError("card changed while building pointers; reindex this card")
			except (OSError, ValueError) as Error:
				Row["pointer_state"] = "STALE"
				Issues.append(issue(Row["location"], Error))
		if((Index.read_bytes() if Index.exists() else None) != IndexBefore):
			raise ValueError("index changed during refresh; retry against the current index")
		IndexChanged = IndexBefore is None or json.loads(IndexBefore.decode("utf-8-sig")) != Previous
		PreviousSnapshot = None
		if(IndexChanged and IndexBefore is not None):
			Snapshot = inside(Root, library_root(Root) / "index-history" / (digest(IndexBefore) + ".json"))
			immutable_write(Snapshot, IndexBefore)
			PreviousSnapshot = relative(Root, Snapshot)
		if(IndexChanged):
			Previous["updated_at"] = utc_now()
			atomic_write(Index, json_bytes(Previous))
		if(ReadmeBytes is not None):
			if((Readme.read_bytes() if Readme.exists() else None) != ReadmeBefore):
				raise ValueError("README changed while indexing; index is saved, retry the generated view")
			if(ReadmeBytes != ReadmeBefore):
				atomic_write(Readme, ReadmeBytes)
	return dict(index=relative(Root, Index), indexed=sum(Row.get("pointer_state") == "CURRENT" and Row["reuse_allowed"] for Row in Rows),
		blocked=sum(not Row["reuse_allowed"] for Row in Rows),
		verdict="CORRECTIONS_INVALID" if any(Item.get("state") == "CORRECTIONS_INVALID" for Item in Issues) else "INDEXED",
		needs_metadata_review=[Row["location"] for Row in Rows if Row.get("metadata_status") == "UNPARSEABLE" or Row.get("identity_error")],
		retained_unscanned=sum(Row.get("pointer_state") == "UNSCANNED" for Row in Rows),
		parsed=Parsed, reused=Reused, index_changed=IndexChanged, previous_index_snapshot=PreviousSnapshot, issues=Issues)


def query_tools(project, query, IndexPath="index/tools.json", limit=8, IncludeArchived=False, IncludeUnreviewed=False, IncludeStale=False, IncludeAffected=False, Context=None):
	with writer_lock(library_root(project)):
		return _query_tools(project, query, IndexPath, limit, IncludeArchived, IncludeUnreviewed, IncludeStale, IncludeAffected, Context)


def _query_tools(project, query, IndexPath, limit, IncludeArchived, IncludeUnreviewed, IncludeStale, IncludeAffected, Context=None):
	import research_corrections as corrections
	import research_context as context
	context.producer_identity()
	if(not query.strip() or not 1 <= limit <= 50):
		raise ValueError("query is required and limit must be in 1..50")
	Index = read_json(inside(project, IndexPath))
	if(Index.get("pointer_schema") not in ("tool-pointers/v1", POINTER_SCHEMA)):
		raise ValueError("build a current pointer index before querying")
	Issues = list(Index.get("issues", []))
	Rows, CorrectionIssues = corrections.gate_rows(project, Index["items"] + Index.get("blocked_items", []))
	Issues.extend(CorrectionIssues)
	if(any(Item.get("state") == "CORRECTIONS_INVALID" for Item in CorrectionIssues)):
		return dict(verdict="CORRECTIONS_INVALID", hits=[], issues=Issues, total_matches=0, changed_paths=[], blocked=len(Rows))
	Context = context.normalize_context(Context)
	Notes = collect_notes(project, Issues)
	Hits = []
	KnownPaths = set(Row["location"] for Row in Rows if Row.get("pointer_state") == "CURRENT")
	LivePaths = card_paths(project, Index["tool_roots"], Index.get("generated_readme"), Issues)
	Stale = LivePaths ^ KnownPaths
	Terms = query.casefold().split()
	for Row in Rows:
		if(Row.get("pointer_state") != "CURRENT"):
			continue
		if(not IncludeAffected and not Row["reuse_allowed"]):
			continue
		try:
			Raw = inside(project, Row["location"]).read_bytes()
			if(digest(Raw) != Row["sha256"]):
				raise ValueError("card changed since indexing")
		except (OSError, ValueError, KeyError) as Error:
			Stale.add(Row["location"])
			Issues.append(issue(Row["location"], Error))
			continue
		if(not IncludeArchived and Row.get("lifecycle") == "archived"):
			continue
		if(not IncludeUnreviewed and (Row.get("metadata_status") == "UNPARSEABLE" or Row.get("identity_error"))):
			continue
		ToolNotes = [dict(Note, state="CURRENT" if Note["tool_sha256"] == Row["sha256"] else "STALE")
			for Note in Notes if Note["tool_path"] == Row["location"]]
		Live = parse_card(project, Row["location"], Raw, Row, Snapshot=False)
		Live.update({Key: Row[Key] for Key in ("correction_state", "reuse_allowed", "dependencies_known")})
		Row = Live
		_, Body, _ = read_metadata(Raw) if Row["metadata_status"] != "UNPARSEABLE" else ({}, Raw.decode("utf-8", errors="replace"), "UNPARSEABLE")
		Score, Reasons = context.rank_candidate(query, Context, Row, Body, [Note for Note in ToolNotes if Note["state"] == "CURRENT"])
		OldText = json.dumps([Note for Note in ToolNotes if Note["state"] == "STALE"], ensure_ascii=False).casefold()
		if(not Score and IncludeStale and any(Term in OldText for Term in Terms)):
			Score = 1
		if(not Score):
			continue
		Lexical = any(Reason.get("basis") == "CURRENT_BYTES_OR_CURRENT_ANNOTATION" for Reason in Reasons)
		QueryMatch = any(Reason.get("query_terms") for Reason in Reasons)
		Hit = dict(score=Score, query_match=QueryMatch, lexical_match=Lexical, match_kind="QUERY_TEXT" if QueryMatch else "GOAL_TEXT" if Lexical else "CONTEXT_SUGGESTION", relevance_reasons=Reasons, applicability_check=context.condition_check(Context, Row), tool_id=Row["tool_id"], title=Row["title"], kind=Row.get("kind", "tool"),
			correction_state=Row["correction_state"], reuse_allowed=Row["reuse_allowed"], dependencies=Row.get("dependencies", []),
			dependencies_known=Row["dependencies_known"],
			metadata_status=Row.get("metadata_status", "UNKNOWN"), identity_error=Row.get("identity_error"),
			location=Row["location"], sha256=Row["sha256"], version=Row.get("version"), summary=Row["summary"],
			conditions=Row.get("conditions", "UNSPECIFIED"), scope=Row.get("scope", "UNSPECIFIED"),
			applicability=Row.get("applicability", []), lifecycle=Row.get("lifecycle"),
			evidence_status=Row.get("evidence_status", "UNKNOWN"), trust=Row["trust"] if Row["reuse_allowed"] else "HISTORY_ONLY_NOT_REUSE",
			inherited_metadata=Row.get("inherited_metadata", []), field_provenance=Row.get("field_provenance", {}), historical_metadata=Row.get("historical_metadata", {}),
			annotations=annotation_pointers(ToolNotes, Row),
			matched_historical_annotation=IncludeStale and any(Term in OldText for Term in Terms))
		for Key in ("sources", "evidence", "resources"):
			Hit[Key] = reference_states(project, Row.get(Key, []))
		Hit["lean"] = lean_reference_states(project, Row.get("lean", []))
		Hit["experience"] = Row.get("experience", dict())
		Hit.update({Key: Row.get(Key, []) for Key in ("problem_ids", "objects", "parameter_scope", "tool_types", "missing_bridges", "relations")})
		Hits.append(Hit)
	# Preserve direct current text matches before broad context-only suggestions,
	# regardless of the number of matching context fields or the caller's limit.
	Hits.sort(key=lambda Item: (not Item["query_match"], not Item["lexical_match"], -Item["score"], Item["tool_id"], Item["location"]))
	return dict(verdict="CORRECTIONS_INVALID" if any(Item.get("state") == "CORRECTIONS_INVALID" for Item in CorrectionIssues) else "STALE_INDEX" if Stale else "RETRIEVAL_ONLY", changed_paths=sorted(Stale),
		blocked=sum(not Row["reuse_allowed"] for Row in Rows),
		hits=Hits[:limit], total_matches=len(Hits), issues=Issues)


def gated_rows(project, Rows):
	import research_corrections as corrections
	Output, Issues = corrections.gate_rows(project, Rows)
	if(any(Item.get("state") == "CORRECTIONS_INVALID" for Item in Issues)):
		raise ValueError("CORRECTIONS_INVALID: " + json.dumps(Issues, ensure_ascii=False))
	return Output


def read_card(project, ToolPath, IncludeAffected=False, IndexPath="index/tools.json", StartLine=1, MaxLines=80, _Locked=False):
	"""Live, gated read. Cached hashes and cached correction labels authorize nothing."""
	with (nullcontext() if _Locked else writer_lock(library_root(project))):
		Location = relative(project, inside(project, ToolPath))
		Raw = inside(project, Location).read_bytes()
		IndexFile = inside(project, IndexPath)
		Rows = []
		if(IndexFile.exists()):
			Index = read_json(IndexFile)
			if(not isinstance(Index, dict) or not isinstance(Index.get("items"), list)):
				raise ValueError("invalid index; preserve it before explicit recovery")
			Rows = Index["items"] + Index.get("blocked_items", [])
		Old = next((Row for Row in Rows if Row.get("location") == Location), {})
		Row = parse_card(project, Location, Raw, Old, Snapshot=False)
		Row = gated_rows(project, [Row])[0]
		Duplicate = any(Item.get("tool_id") == Row["tool_id"] and Item.get("location") != Location for Item in Rows)
		if(Duplicate or Row["metadata_status"] == "UNPARSEABLE"):
			Row.update(reuse_allowed=False, correction_state=dict(status="identity_or_metadata_invalid", reuse_allowed=False, issues=[]))
		if(not Row["reuse_allowed"] and not IncludeAffected):
			raise ValueError("REUSE_BLOCKED: " + Location + "; use explicit history inspection")
		_, Body, _ = read_metadata(Raw) if Row["metadata_status"] != "UNPARSEABLE" else ({}, Raw.decode("utf-8", errors="replace"), "UNPARSEABLE")
		if(StartLine < 1 or not 1 <= MaxLines <= 200):
			raise ValueError("invalid bounded card read")
		Lines = Body.splitlines(keepends=True)
		Passage = "".join(Lines[StartLine - 1:StartLine - 1 + MaxLines])
		Row.update(path=Location, content=Passage, coverage=dict(start_line=StartLine, end_line=min(len(Lines), StartLine - 1 + MaxLines), complete_body=StartLine == 1 and len(Lines) <= MaxLines), trust="RETRIEVAL_ONLY_REVALIDATE_APPLICATION" if Row["reuse_allowed"] else "HISTORY_ONLY_NOT_REUSE")
		for Key in ("sources", "evidence", "resources"):
			Row[Key] = reference_states(project, Row.get(Key, []))
		Row["lean"] = lean_reference_states(project, Row.get("lean", []))
		return Row


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Sub = Parser.add_subparsers(dest="command", required=True)
	Capture = Sub.add_parser("capture-source")
	for name in ("project", "input", "url", "version", "title"):
		Capture.add_argument("--" + name, required=True)
	Capture.add_argument("--text-file")
	Capture.add_argument("--method", default="provided-text")
	Capture.add_argument("--source-kind", choices=("primary", "secondary"), default="primary")
	Capture.add_argument("--coverage", help="what was actually retrieved: full text, pages, abstract or excerpt")
	Capture.add_argument("--locator", action="append", help="original page, theorem or equation locator")
	Find = Sub.add_parser("find-source")
	Find.add_argument("--project", required=True)
	Find.add_argument("--query", required=True)
	Find.add_argument("--limit", type=int, default=8)
	Find.add_argument("--content", action="store_true", help="also search verified captured text bytes")
	Read = Sub.add_parser("read-source")
	Read.add_argument("--project", required=True)
	Read.add_argument("--source-id", required=True)
	Read.add_argument("--start-line", type=int, default=1)
	Read.add_argument("--max-lines", type=int, default=80)
	Read.add_argument("--start-offset", type=int)
	Note = Sub.add_parser("annotate")
	for name in ("project", "tool", "text-file"):
		Note.add_argument("--" + name, required=True)
	Note.add_argument("--expected-sha256")
	Note.add_argument("--author", default="unspecified")
	Note.add_argument("--kind", default="observation")
	Note.add_argument("--locator", default="card")
	Note.add_argument("--source-id")
	Card = Sub.add_parser("card", help="save JSON containing content and optional title, conditions and references")
	Card.add_argument("--project", required=True)
	Card.add_argument("--input", required=True)
	Card.add_argument("--tool")
	Card.add_argument("--expected-sha256")
	Index = Sub.add_parser("index")
	Index.add_argument("--project", required=True)
	Index.add_argument("--tool-root", action="append")
	Index.add_argument("--index", default="index/tools.json")
	Index.add_argument("--readme")
	Index.add_argument("--from-index", help="recover metadata from a preserved index after the destination index was lost")
	Query = Sub.add_parser("query")
	Query.add_argument("--project", required=True)
	Query.add_argument("--query", required=True)
	Query.add_argument("--index", default="index/tools.json")
	Query.add_argument("--limit", type=int, default=8)
	Query.add_argument("--include-archived", action="store_true")
	Query.add_argument("--include-unreviewed", action="store_true")
	Query.add_argument("--include-stale", action="store_true", help="also match historical annotations, marked STALE")
	Query.add_argument("--include-affected", action="store_true", help="inspect quarantined, retracted and needs-review versions; never authorizes reuse")
	Query.add_argument("--context", help="optional JSON: goal, problem_ids, objects, conditions, parameter_scope, tool_types")
	CardRead = Sub.add_parser("read", help="bounded current card read through the live correction gate")
	CardRead.add_argument("--project", required=True)
	CardRead.add_argument("--tool", required=True)
	CardRead.add_argument("--index", default="index/tools.json")
	CardRead.add_argument("--start-line", type=int, default=1)
	CardRead.add_argument("--max-lines", type=int, default=80)
	CardRead.add_argument("--include-affected", action="store_true")
	Package = Sub.add_parser("context", help="rebuild a bounded task knowledge view; no scheduling or canonical writes")
	Package.add_argument("--project", required=True)
	Package.add_argument("--query", required=True)
	Package.add_argument("--context")
	Package.add_argument("--index", default="index/tools.json")
	Package.add_argument("--limit", type=int, default=5)
	Package.add_argument("--depth", type=int, default=1)
	Package.add_argument("--max-chars", type=int, default=32000)
	Package.add_argument("--include-affected", action="store_true")
	Package.add_argument("--entry", action="append")
	Package.add_argument("--output", help="optional content-addressed JSON export inside the project")
	Package.add_argument("--recheck-lean", action="store_true", help="explicit selected-reference check via existing lean-verify")
	Package.add_argument("--lean-tools", help="trusted lean-verify scripts directory; never taken from a card")
	Args = Parser.parse_args()
	try:
		if(Args.command == "capture-source"):
			Result = capture_source(Args.project, Args.input, Args.url, Args.version, Args.title, Args.text_file, Args.method, Args.source_kind, Args.coverage, Args.locator)
		elif(Args.command == "find-source"):
			Result = find_sources(Args.project, Args.query, Args.limit, Args.content)
		elif(Args.command == "read-source"):
			Result = read_source(Args.project, Args.source_id, Args.start_line, Args.max_lines, Args.start_offset)
		elif(Args.command == "annotate"):
			Result = annotate(Args.project, Args.tool, Args.expected_sha256, Args.author, Args.kind, Args.locator,
				Path(Args.text_file).read_text(encoding="utf-8"), Args.source_id)
		elif(Args.command == "index"):
			Result = make_index(Args.project, Args.tool_root, Args.index, Args.readme, Args.from_index)
		elif(Args.command == "card"):
			Result = save_card(Args.project, read_json(Path(Args.input)), Args.tool, Args.expected_sha256)
		elif(Args.command == "read"):
			Result = read_card(Args.project, Args.tool, Args.include_affected, Args.index, Args.start_line, Args.max_lines)
		elif(Args.command == "context"):
			import research_context as context
			Result = context.knowledge_package(Args.project, Args.query, read_json(Path(Args.context)) if Args.context else None, Args.index, Args.limit, Args.depth, Args.max_chars, Args.include_affected, Args.entry, Args.recheck_lean, Args.lean_tools)
			if(Args.output):
				Result = context.export_package(Args.project, Result, Args.output)
		else:
			Result = query_tools(Args.project, Args.query, Args.index, Args.limit, Args.include_archived, Args.include_unreviewed, Args.include_stale, Args.include_affected, read_json(Path(Args.context)) if Args.context else None)
		print(json.dumps(Result, ensure_ascii=False))
		return 1 if Result.get("verdict") in ("STALE_INDEX", "CORRECTIONS_INVALID") else 0
	except (OSError, ValueError, TypeError, KeyError, RuntimeError) as Error:
		print(json.dumps(dict(verdict="INVALID", error=str(Error)), ensure_ascii=False))
		return 1


if(__name__ == "__main__"):
	raise SystemExit(main())
