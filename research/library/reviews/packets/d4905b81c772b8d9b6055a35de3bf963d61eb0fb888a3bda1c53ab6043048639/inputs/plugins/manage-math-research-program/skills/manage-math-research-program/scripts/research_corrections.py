#!/usr/bin/env python3
"""Immutable audit issues, versioned dependency quarantine and reviewed releases.

This is a retrieval gate. It never edits an accepted Blueprint graph and never
authenticates a reviewer's identity from self-reported JSON fields.
"""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
import re

import research_library as library

SCHEMA = "research-corrections/v1"
TRUST = "COORDINATOR_ATTESTED_TOOL_TRANSCRIPT"
HASH = re.compile(r"[0-9a-f]{64}\Z")


def require(Condition, Message):
	if(not Condition):
		raise ValueError(Message)


def root(project):
	return library.inside(project, library.library_root(project) / "corrections")


def marker(project):
	return library.inside(project, library.library_root(project) / "corrections-required.json")


def artifact(project, Kind, ContentHash, Suffix=".json"):
	require(isinstance(ContentHash, str) and HASH.fullmatch(ContentHash), "invalid content hash")
	return library.inside(project, root(project) / Kind / (ContentHash + Suffix))


def exact_ref(project, Ref):
	require(isinstance(Ref, dict), "version reference must be an object")
	Location = Ref.get("location", Ref.get("path"))
	require(isinstance(Location, str) and Location, "version reference needs a path")
	Location = library.relative(project, library.inside(project, Location))
	ContentHash = Ref.get("sha256")
	require(isinstance(ContentHash, str) and HASH.fullmatch(ContentHash), "explicit version sha256 is required")
	return dict(location=Location, sha256=ContentHash)


def version_path(project, ContentHash):
	require(isinstance(ContentHash, str) and HASH.fullmatch(ContentHash), "invalid card version hash")
	return library.inside(project, library.library_root(project) / "card-versions" / (ContentHash + ".md"))


def version_bytes(project, Ref, Capture=False):
	Ref = exact_ref(project, Ref)
	Snapshot = version_path(project, Ref["sha256"])
	if(not Snapshot.exists() and Capture):
		Raw = library.inside(project, Ref["location"]).read_bytes()
		require(library.digest(Raw) == Ref["sha256"], "card version changed before binding")
		library.snapshot_card(project, Raw)
	Raw = Snapshot.read_bytes()
	require(library.digest(Raw) == Ref["sha256"], "card snapshot hash mismatch")
	return Raw


def capture_version(project, Ref):
	"""An explicit archived copy can supply old bytes without overwriting the live card."""
	Exact = exact_ref(project, Ref)
	if(Ref.get("snapshot")):
		Raw = library.inside(project, Ref["snapshot"]).read_bytes()
		require(library.digest(Raw) == Exact["sha256"], "archived card does not match the declared old version")
		library.snapshot_card(project, Raw)
	return Exact, version_bytes(project, Exact, Capture=True)


def bind_dependencies(project, Dependencies, Capture=False):
	require(isinstance(Dependencies, list), "dependencies must be a list of exact card versions")
	Bound = []
	for Ref in Dependencies:
		Ref = exact_ref(project, Ref)
		version_bytes(project, Ref, Capture)
		if(Ref not in Bound):
			Bound.append(Ref)
	return sorted(Bound, key=lambda Row: (Row["location"], Row["sha256"]))


def card_dependencies(Front):
	if("dependencies" in Front and "depends_on" in Front):
		require(Front["dependencies"] == Front["depends_on"], "dependencies and depends_on disagree; use one spelling")
	return Front.get("dependencies", Front.get("depends_on", []))


def register_version(project, Location, Raw, ToolId=None):
	"""Called under the existing library writer lock; never reinterprets a source URL as an edge."""
	Location = library.relative(project, library.inside(project, Location))
	MetadataError = None
	try:
		Front, _, _ = library.read_metadata(Raw)
	except (ValueError, TypeError) as Error:
		# Intake must be able to quarantine the exact broken source, without repairing it.
		Front, MetadataError = {}, str(Error)
	Folder = library.inside(project, library.library_root(project) / "card-bindings")
	Catalog = Folder / "catalog.json"
	Marker = library.inside(project, library.library_root(project) / "card-bindings-required.json")
	if(Marker.exists()):
		require(library.read_json(Marker) == dict(schema=SCHEMA), "invalid version registry marker")
		require(Catalog.is_file(), "version catalog is missing")
	Names = set()
	if(Catalog.exists()):
		CatalogData = library.read_json(Catalog)
		require(isinstance(CatalogData, dict) and CatalogData.get("schema") == SCHEMA and isinstance(CatalogData.get("records"), list), "invalid version catalog")
		Names = set(CatalogData["records"])
		require(all(isinstance(Name, str) and HASH.fullmatch(Name) for Name in Names), "invalid version catalog identity")
		for Name in Names:
			require((Folder / (Name + ".json")).is_file(), "version registry record is missing")
	Existing = {}
	for PathValue in Folder.glob("*.json"):
		if(PathValue.name == "catalog.json"):
			continue
		Prior = read_hashed(library.inside(project, PathValue))
		version_bytes(project, Prior)
		Existing[key(Prior)] = Prior
		Names.add(PathValue.stem)
	Prior = Existing.get((Location, library.digest(Raw)))
	if(Prior):
		# An indexed legacy identity can differ from its filename/frontmatter.
		ToolId = Prior["tool_id"]
	Node = dict(schema=SCHEMA, location=Location, sha256=library.digest(Raw),
		tool_id=str(ToolId or Front.get("tool_id") or Front.get("slug") or Path(Location).stem),
		dependencies=bind_dependencies(project, card_dependencies(Front), Capture=True))
	if(MetadataError is not None):
		Node.update(metadata_status="INVALID", metadata_error=MetadataError, dependencies_known=False)
	if(Prior and Prior.get("metadata_status") == "INVALID"):
		# A later parser/install or reindex cannot silently upgrade an opaque version.
		Node = Prior
	library.snapshot_card(project, Raw)
	for Ref in Node["dependencies"]:
		if(key(Ref) not in Existing):
			register_version(project, Ref["location"], version_bytes(project, Ref))
			Names.update(library.read_json(Catalog)["records"])
	ContentHash = library.digest(library.json_bytes(Node))
	PathValue = library.inside(project, Folder / (ContentHash + ".json"))
	library.immutable_write(PathValue, library.json_bytes(Node))
	Names.add(ContentHash)
	CatalogRaw = library.json_bytes(dict(schema=SCHEMA, records=sorted(Names)))
	if(not Catalog.exists() or Catalog.read_bytes() != CatalogRaw):
		library.atomic_write(Catalog, CatalogRaw)
	library.immutable_write(Marker, library.json_bytes(dict(schema=SCHEMA)))
	return Node


def read_hashed(PathValue):
	Raw = PathValue.read_bytes()
	require(library.digest(Raw) == PathValue.stem, "immutable record hash mismatch: " + str(PathValue))
	Data = json.loads(Raw)
	require(isinstance(Data, dict) and library.json_bytes(Data) == Raw, "noncanonical immutable record: " + str(PathValue))
	return Data


def read_versions(project):
	Nodes = {}
	Folder = library.inside(project, library.library_root(project) / "card-bindings")
	require(Folder.is_dir(), "version registry is missing")
	RegistryMarker = library.inside(project, library.library_root(project) / "card-bindings-required.json")
	require(library.read_json(RegistryMarker) == dict(schema=SCHEMA), "invalid version registry marker")
	Catalog = library.read_json(Folder / "catalog.json")
	require(isinstance(Catalog, dict) and Catalog.get("schema") == SCHEMA and isinstance(Catalog.get("records"), list), "invalid version catalog")
	Names = {PathValue.stem for PathValue in Folder.glob("*.json") if PathValue.name != "catalog.json"}
	require(len(Catalog["records"]) == len(Names) and set(Catalog["records"]) == Names, "version catalog is incomplete or has unfinished registrations")
	for PathValue in sorted(Folder.glob("*.json")):
		if(PathValue.name == "catalog.json"):
			continue
		Node = read_hashed(library.inside(project, PathValue))
		require(Node.get("schema") == SCHEMA and isinstance(Node.get("tool_id"), str) and Node["tool_id"], "invalid card binding")
		Ref = exact_ref(project, Node)
		Raw = version_bytes(project, Ref)
		if(Node.get("metadata_status") == "INVALID"):
			require(Node.get("dependencies_known") is False and Node.get("dependencies") == [] and isinstance(Node.get("metadata_error"), str) and Node["metadata_error"], "invalid opaque version record")
		else:
			Front, _, _ = library.read_metadata(Raw)
			require(Node.get("dependencies") == bind_dependencies(project, card_dependencies(Front)), "card dependency binding mismatch")
		Key = key(Ref)
		if(Key in Nodes):
			require(Nodes[Key] == Node, "conflicting version identity")
		Nodes[Key] = Node
	return Nodes


def key(Ref):
	return Ref["location"], Ref["sha256"]


def same_identity(Left, Right):
	return (Left["location"] == Right["location"] or Left["sha256"] == Right["sha256"]
		or bool(Left.get("tool_id") and Left.get("tool_id") == Right.get("tool_id")))


def initialize(project):
	Folder, Marker = root(project), marker(project)
	if(Marker.exists()):
		require(Folder.is_dir(), "correction store is missing; restore it, do not initialize a replacement")
		return
	if(Folder.exists()):
		# Only a provably empty interrupted initialization is recoverable here.
		require(not any(PathValue.is_file() for PathValue in Folder.rglob("*")), "correction marker is missing")
	for Name in ("requests", "events", "evidence"):
		(Folder / Name).mkdir(parents=True, exist_ok=True)
	library.immutable_write(Marker, library.json_bytes(dict(schema=SCHEMA, store=library.relative(project, Folder))))


def validate_request(project, Request, Nodes):
	require(Request.get("schema") == SCHEMA and Request.get("kind") in ("issue", "revision", "release"), "invalid correction request kind/schema")
	require(isinstance(Request.get("key"), str) and Request["key"] and isinstance(Request.get("input_sha256"), str) and HASH.fullmatch(Request["input_sha256"]), "invalid correction request identity")
	Payload = Request.get("payload")
	require(isinstance(Payload, dict), "invalid correction payload")
	Kind = Request["kind"]
	Refs = Payload.get("targets") if Kind == "issue" else [Payload.get("old"), Payload.get("new")] if Kind == "revision" else []
	require(isinstance(Refs, list) and (Refs or Kind == "release"), "missing correction targets")
	for Ref in Refs:
		Ref = exact_ref(project, Ref)
		require(key(Ref) in Nodes, "missing version binding for correction target")
	if(Kind == "issue"):
		require(Payload.get("disposition") in ("quarantine", "retracted"), "invalid issue disposition")
		require(isinstance(Payload.get("issue_id"), str) and Payload["issue_id"], "invalid issue ID")
		require(isinstance(Payload.get("evidence"), list) and Payload["evidence"], "issue evidence is required")
		for Evidence in Payload["evidence"]:
			Expected = artifact(project, "evidence", Evidence["sha256"], ".bin")
			require(Evidence["snapshot"] == library.relative(project, Expected) and library.digest(Expected.read_bytes()) == Evidence["sha256"], "issue evidence hash mismatch")
		require(isinstance(Payload.get("canonical_nodes"), list), "invalid canonical impact pointers")
	elif(Kind == "revision"):
		require(isinstance(Payload.get("issue"), str) and HASH.fullmatch(Payload["issue"]), "invalid revision issue binding")
		require(Payload["old"]["sha256"] != Payload["new"]["sha256"], "a repair needs a new card version")
		require(isinstance(Payload.get("author"), str) and Payload["author"], "revision author is required")
		require(Payload.get("old_status") in ("quarantine", "retracted", "needs_review"), "invalid historical repair status")
	else:
		require(isinstance(Payload.get("revision"), str) and HASH.fullmatch(Payload["revision"]), "invalid release revision binding")
		require(isinstance(Payload.get("bundle"), str) and isinstance(Payload.get("review"), dict), "invalid release receipt")


def load_store(project, AllowPending=False):
	Folder, Marker = root(project), marker(project)
	if(not Marker.exists() and not Folder.exists()):
		Registry = library.library_root(project) / "card-bindings"
		HasRegistry = Registry.exists() or (library.library_root(project) / "card-bindings-required.json").exists()
		return dict(requests={}, events=[], nodes=read_versions(project) if HasRegistry else {}, pending=[])
	require(Marker.is_file() and Folder.is_dir(), "missing correction marker/store; reuse is closed")
	require(library.read_json(Marker) == dict(schema=SCHEMA, store=library.relative(project, Folder)), "invalid correction marker")
	for Name in ("requests", "events", "evidence"):
		require((Folder / Name).is_dir(), "missing correction store directory: " + Name)
	Nodes = read_versions(project)
	Requests, Keys = {}, set()
	for PathValue in sorted((Folder / "requests").glob("*.json")):
		Request = read_hashed(library.inside(project, PathValue))
		validate_request(project, Request, Nodes)
		require(Request["key"] not in Keys, "conflicting idempotency key")
		Keys.add(Request["key"])
		Requests[PathValue.stem] = Request
	Events, Used, Previous = [], set(), None
	for PathValue in sorted((Folder / "events").glob("*.json")):
		Event = library.read_json(library.inside(project, PathValue))
		require(isinstance(Event, dict), "invalid correction event")
		EventHash = library.digest(library.json_bytes(Event))
		require(PathValue.name == f"{len(Events):08d}-{EventHash}.json" and PathValue.read_bytes() == library.json_bytes(Event), "event sequence/hash mismatch")
		require(Event.get("schema") == SCHEMA and Event.get("previous") == Previous and Event.get("request") in Requests, "broken correction event chain")
		require(Event["request"] not in Used, "duplicate committed correction")
		Used.add(Event["request"])
		Events.append(dict(Event, sha256=EventHash))
		Previous = EventHash
	Pending = sorted(set(Requests) - Used)
	require(AllowPending or not Pending, "unfinished correction transaction; retry its identical request")
	return dict(requests=Requests, events=Events, nodes=Nodes, pending=Pending)


def request_info(project, RequestHash):
	PathValue = artifact(project, "requests", RequestHash)
	return dict(path=library.relative(project, PathValue), sha256=RequestHash)


def append_request(project, Kind, OperationKey, Input, Build):
	"""Durable intent before commit; an interrupted intent closes all retrieval."""
	initialize(project)
	Store = load_store(project, AllowPending=True)
	InputHash = library.digest(library.json_bytes(Input))
	Matches = [(HashValue, Record) for HashValue, Record in Store["requests"].items() if Record["key"] == OperationKey]
	if(Matches):
		RequestHash, Request = Matches[0]
		require(Request["input_sha256"] == InputHash and Request["kind"] == Kind, "idempotency key reused with different input")
	else:
		require(not Store["pending"], "retry the unfinished correction request before starting another")
		Request = dict(schema=SCHEMA, kind=Kind, key=OperationKey, input_sha256=InputHash, payload=Build(Store))
		RequestHash = library.digest(library.json_bytes(Request))
		validate_request(project, Request, read_versions(project))
		library.immutable_write(artifact(project, "requests", RequestHash), library.json_bytes(Request))
	Committed = any(Event["request"] == RequestHash for Event in Store["events"])
	if(not Committed):
		require(not set(Store["pending"]) - {RequestHash}, "conflicting unfinished correction transaction")
		Event = dict(schema=SCHEMA, previous=Store["events"][-1]["sha256"] if Store["events"] else None, request=RequestHash)
		EventHash = library.digest(library.json_bytes(Event))
		PathValue = library.inside(project, root(project) / "events" / f"{len(Store['events']):08d}-{EventHash}.json")
		library.immutable_write(PathValue, library.json_bytes(Event))
	return dict(request_id=RequestHash, reused=bool(Matches), **request_info(project, RequestHash))


def issue_requests(Store):
	return {Event["request"]: Store["requests"][Event["request"]]["payload"] for Event in Store["events"] if Store["requests"][Event["request"]]["kind"] == "issue"}


def find_issue(Store, IssueId):
	Matches = [(HashValue, Payload) for HashValue, Payload in issue_requests(Store).items() if Payload["issue_id"] == IssueId or HashValue == IssueId]
	require(len(Matches) == 1, "issue ID must identify one committed issue")
	return Matches[0]


def revision_request(Store, RevisionId):
	require(RevisionId in Store["requests"] and Store["requests"][RevisionId]["kind"] == "revision", "unknown revision")
	require(any(Event["request"] == RevisionId for Event in Store["events"]), "revision is not committed")
	Revision = Store["requests"][RevisionId]["payload"]
	require(Revision["issue"] in issue_requests(Store), "revision has no committed issue")
	return Revision


def required_bindings(project, Store, RevisionId):
	Revision = revision_request(Store, RevisionId)
	IssueHash = Revision["issue"]
	Issue = Store["requests"][IssueHash]["payload"]
	Bindings = {request_info(project, HashValue)["path"]: HashValue for HashValue in (IssueHash, RevisionId)}
	for Ref in (Revision["old"], Revision["new"]):
		Bindings[library.relative(project, version_path(project, Ref["sha256"]))] = Ref["sha256"]
	Bindings[Revision["new"]["location"]] = Revision["new"]["sha256"]
	for Evidence in Issue["evidence"]:
		Bindings[Evidence["snapshot"]] = Evidence["sha256"]
	for Ref in Store["nodes"][key(Revision["new"])]["dependencies"]:
		Bindings[Ref["location"]] = Ref["sha256"]
	return Bindings


def known_authors(project, Store, RevisionId):
	Revision = revision_request(Store, RevisionId)
	Authors = {Revision["author"]}
	for Ref in (Revision["old"], Revision["new"]):
		if(Store["nodes"][key(Ref)].get("metadata_status") == "INVALID"):
			continue
		Front, _, _ = library.read_metadata(version_bytes(project, Ref))
		Extra = Front.get("author_ids", [])
		require(isinstance(Extra, list) and all(isinstance(Author, str) and Author for Author in Extra), "invalid card author_ids")
		Authors.update(Extra)
	for Request in Store["requests"].values():
		if(Request["kind"] == "revision" and Request["payload"]["new"]["location"] == Revision["new"]["location"]):
			Authors.add(Request["payload"]["author"])
	return sorted(Authors)


def repair_claim(RevisionId, Revision):
	return dict(id="correction:" + RevisionId, verification="analytic",
		statement="Independently check the repaired card " + Revision["new"]["location"] + " at sha256 " + Revision["new"]["sha256"] + ", its scope and dependencies, against the original issue " + Revision["issue"] + " and old version " + Revision["old"]["sha256"] + ". Determine whether this exact repair resolves that issue for this card; do not infer validity of other cards or complete formalization.")


def verify_bundle(project, BundlePath, Bindings, Claim, Authors):
	# Fixed sibling module only: no CLI callback, untrusted module path or boolean fallback.
	Review = importlib.import_module("research_review")
	try:
		Result = Review.verify_review_bundle(project, BundlePath)
	except Exception as Error:
		raise ValueError("review receipt verification failed: " + str(Error)) from Error
	require(isinstance(Result, dict) and Result.get("kind") == "mathematics" and Result.get("verdict") == "APPROVED" and Result.get("trust") == TRUST, "review is not a mathematics approval from the trusted coordinator receipt verifier")
	require(isinstance(Result.get("reviewer_id"), str) and Result["reviewer_id"] and isinstance(Result.get("packet_sha256"), str) and HASH.fullmatch(Result["packet_sha256"]), "incomplete review identity")
	Actual = Result.get("bindings")
	require(isinstance(Actual, dict) and all(Actual.get(PathValue) == HashValue for PathValue, HashValue in Bindings.items()), "review does not bind this issue, repair and exact card versions")
	for PathValue, HashValue in Bindings.items():
		require(library.digest(library.inside(project, PathValue).read_bytes()) == HashValue, "review input is no longer current: " + PathValue)
	require(Result["reviewer_id"] not in Authors, "an author cannot approve this repair")
	require(isinstance(Result.get("checked_paths"), list) and set(Bindings) <= set(Result["checked_paths"]), "review did not check the correction inputs")
	Dispatch = library.read_json(library.inside(project, Path(BundlePath) / "dispatch.json"))
	PacketRaw = library.inside(project, Dispatch["packet"]).read_bytes()
	require(library.digest(PacketRaw) == Result["packet_sha256"], "verified review packet changed")
	Packet = json.loads(PacketRaw)
	require(Claim in Packet["claims"], "packet substitutes a different obligation for the exact repair")
	require(set(Authors) <= set(Packet["author_ids"]), "packet omitted known repair authors")
	# The obligation ID is bound to this immutable repair, not a generic PASS claim.
	Claims = Result.get("claims")
	require(isinstance(Claims, list) and any(isinstance(Row, dict) and Row.get("id") == Claim["id"] and Row.get("verdict") == "APPROVED" for Row in Claims), "review report does not cover the exact repaired card")
	require(Result.get("bundle") == library.relative(project, library.inside(project, BundlePath)), "review bundle identity mismatch")
	return Result


def accepted_releases(project, Store):
	Released, Problems = {}, []
	Seen = dict(requests=Store["requests"], nodes=Store["nodes"], events=[], pending=[])
	Latest = {}
	for Event in Store["events"]:
		RequestHash = Event["request"]
		Request = Store["requests"][RequestHash]
		Payload = Request["payload"]
		if(Request["kind"] == "revision"):
			require(Payload["issue"] in issue_requests(Seen), "revision precedes its issue")
			Latest[(Payload["issue"], Payload["new"]["location"])] = RequestHash
		elif(Request["kind"] == "release"):
			Revision = revision_request(Seen, Payload["revision"])
			require(Latest.get((Revision["issue"], Revision["new"]["location"])) == Payload["revision"], "release refers to a superseded revision")
			try:
				Review = verify_bundle(project, Payload["bundle"], required_bindings(project, Seen, Payload["revision"]), repair_claim(Payload["revision"], Revision), known_authors(project, Seen, Payload["revision"]))
				require(Review == Payload["review"], "review receipt changed after release")
				Released[(Revision["issue"], key(Revision["new"]))] = Payload["revision"]
			except (ImportError, OSError, ValueError, TypeError, KeyError, RuntimeError) as Error:
				Problems.append(dict(release=RequestHash, status="REVIEW_NO_LONGER_VALID", error=str(Error)))
		Seen["events"].append(Event)
	Released = {Key: RevisionId for Key, RevisionId in Released.items() if Latest.get((Key[0], Key[1][0])) == RevisionId}
	return Released, Problems


def impact_states(project, Store):
	Released, Problems = accepted_releases(project, Store)
	States = {Key: dict(status="metadata_invalid" if Node.get("metadata_status") == "INVALID" else "clear", issues=[], reuse_allowed=Node.get("metadata_status") != "INVALID") for Key, Node in Store["nodes"].items()}
	Rank = dict(needs_review=1, quarantine=2, retracted=3)
	for IssueHash, Issue in issue_requests(Store).items():
		Blocked = {key(Ref): Issue["disposition"] for Ref in Issue["targets"]}
		for Event in Store["events"]:
			Request = Store["requests"][Event["request"]]
			if(Request["kind"] == "revision" and Request["payload"]["issue"] == IssueHash):
				Revision = Request["payload"]
				Blocked.setdefault(key(Revision["old"]), Revision["old_status"])
		# A pre-existing repair can itself have been quarantined pending review.
		# Retracted exact bytes remain withdrawn even if presented as the "new" card.
		Blocked = {Key: Status for Key, Status in Blocked.items() if Status == "retracted" or (IssueHash, Key) not in Released}
		for Ref in Issue["targets"]:
			require(key(Ref) in Store["nodes"], "issue target version is missing")
		Changed = True
		while(Changed):
			Changed = False
			for Key, Node in Store["nodes"].items():
				if((IssueHash, Key) in Released):
					continue
				Statuses = [Status for Other, Status in Blocked.items() if same_identity(Node, Store["nodes"][Other])]
				if(any(key(Ref) in Blocked for Ref in Node["dependencies"])):
					Statuses.append("needs_review")
				if(Statuses):
					Status = max(Statuses, key=Rank.get)
					if(Rank.get(Blocked.get(Key), 0) < Rank[Status]):
						Blocked[Key] = Status
						Changed = True
		for Key, Status in Blocked.items():
			State = States[Key]
			if(Rank.get(State["status"], 0) < Rank[Status]):
				State["status"] = Status
			State["reuse_allowed"] = False
			State["issues"].append(IssueHash)
	# A release never makes a still-blocked dependency usable, including later issues.
	Changed = True
	while(Changed):
		Changed = False
		for Key, Node in Store["nodes"].items():
			for Ref in Node["dependencies"]:
				if(key(Ref) not in States):
					raise ValueError("dependency version has no durable identity")
				Upstream = States[key(Ref)]
				if(not Upstream["reuse_allowed"] and States[Key]["reuse_allowed"]):
					States[Key] = dict(status="needs_review", issues=list(Upstream["issues"]), reuse_allowed=False)
					Changed = True
	return States, Problems


def gate_rows(project, Rows):
	"""Return a fresh projection, ignoring all cached correction status fields."""
	try:
		Store = load_store(project)
		States, Problems = impact_states(project, Store)
		Output = []
		for Row in Rows:
			VersionKey = Row.get("location"), Row.get("sha256")
			State = States.get(VersionKey)
			Node = Store["nodes"].get(VersionKey, {})
			if(State is None):
				Affected = [Value for Key, Value in States.items() if not Value["reuse_allowed"] and same_identity(Row, Store["nodes"][Key])]
				State = dict(status="needs_review", issues=sorted({IssueId for Value in Affected for IssueId in Value["issues"]}), reuse_allowed=False) if Affected else dict(status="clear", issues=[], reuse_allowed=True)
			Output.append(dict(Row, correction_state=State, reuse_allowed=State["reuse_allowed"], dependencies_known=Node.get("dependencies_known", Row.get("metadata_status") != "UNPARSEABLE")))
		return Output, Problems
	except (ImportError, OSError, ValueError, TypeError, KeyError, RuntimeError) as Error:
		State = dict(status="corrections_invalid", issues=[], reuse_allowed=False, error=str(Error))
		return [dict(Row, correction_state=State, reuse_allowed=False, dependencies_known=False) for Row in Rows], [dict(state="CORRECTIONS_INVALID", error=str(Error))]


def rebuild(project, Result):
	Result["pointers"] = library.make_index(project, _Locked=True)
	return Result


def register_issue(project, Data):
	Data = dict(Data)
	for Name in ("issue_id", "origin", "reporter", "summary"):
		require(isinstance(Data.get(Name), str) and Data[Name].strip(), "issue needs " + Name)
	require(Data["origin"] in ("internal", "external"), "origin must be internal or external")
	require(Data.get("disposition", "quarantine") in ("quarantine", "retracted"), "invalid issue disposition")
	def build(Store):
		Targets = []
		for Ref in Data.get("targets", []):
			Ref, Raw = capture_version(project, Ref)
			register_version(project, Ref["location"], Raw)
			Targets.append(Ref)
		require(Targets, "issue needs at least one exact target")
		EvidenceRows = []
		for Evidence in Data.get("evidence", []):
			require(isinstance(Evidence, dict) and isinstance(Evidence.get("locator"), str) and Evidence["locator"], "evidence needs a path and locator")
			PathValue = library.inside(project, Evidence["path"])
			Raw = PathValue.read_bytes()
			ContentHash = library.digest(Raw)
			require(Evidence.get("sha256", ContentHash) == ContentHash, "evidence changed before capture")
			Snapshot = artifact(project, "evidence", ContentHash, ".bin")
			library.immutable_write(Snapshot, Raw)
			EvidenceRows.append(dict(path=library.relative(project, PathValue), sha256=ContentHash, snapshot=library.relative(project, Snapshot), locator=Evidence["locator"]))
		require(EvidenceRows, "issue needs captured evidence")
		Canonical = Data.get("canonical_nodes", [])
		require(isinstance(Canonical, list) and all(isinstance(Node, dict) and Node.get("node_id") and Node.get("version") for Node in Canonical), "canonical pointers need node_id and version")
		return dict(issue_id=Data["issue_id"], origin=Data["origin"], reporter=Data["reporter"], summary=Data["summary"], disposition=Data.get("disposition", "quarantine"), targets=Targets, evidence=EvidenceRows, canonical_nodes=Canonical, canonical_action="NEEDS_RECEIVER_REVIEW")
	with library.writer_lock(library.library_root(project)):
		if(not (library.library_root(project) / "card-bindings/catalog.json").exists() and not marker(project).exists()):
			# Even a project containing only damaged legacy cards needs a registry.
			for Ref in Data.get("targets", []):
				Exact, Raw = capture_version(project, Ref)
				register_version(project, Exact["location"], Raw)
			library.make_index(project, _Locked=True)
		return rebuild(project, append_request(project, "issue", "issue:" + Data["issue_id"], Data, build))


def propose_revision(project, IssueId, Old, New, Author, Rationale):
	Input = dict(issue=IssueId, old=Old, new=New, author=Author, rationale=Rationale)
	def build(Store):
		IssueHash, _ = find_issue(Store, IssueId)
		OldRef, OldRaw = capture_version(project, Old)
		NewRef = exact_ref(project, New)
		require(OldRef["sha256"] != NewRef["sha256"], "a repair must have different bytes")
		require(OldRef["location"] == NewRef["location"], "repair in the existing card path; renames need separate migration")
		register_version(project, OldRef["location"], OldRaw)
		Store["nodes"] = read_versions(project)
		States, _ = impact_states(project, Store)
		require(key(OldRef) in States and IssueHash in States[key(OldRef)]["issues"], "old version is not affected by this issue")
		require(library.digest(library.inside(project, NewRef["location"]).read_bytes()) == NewRef["sha256"], "repair is not the current card version")
		register_version(project, NewRef["location"], version_bytes(project, NewRef, Capture=True))
		require(isinstance(Author, str) and Author.strip() and isinstance(Rationale, str) and Rationale.strip(), "repair author and rationale are required")
		return dict(issue=IssueHash, old=OldRef, new=NewRef, old_status=States[key(OldRef)]["status"], author=Author, rationale=Rationale)
	with library.writer_lock(library.library_root(project)):
		Result = append_request(project, "revision", "revision:" + library.digest(library.json_bytes(Input)), Input, build)
		Result["revision_id"] = Result["request_id"]
		return rebuild(project, Result)


def review_requirements(project, RevisionId):
	with library.writer_lock(library.library_root(project)):
		Store = load_store(project)
		Revision = revision_request(Store, RevisionId)
		Bindings = required_bindings(project, Store, RevisionId)
		return dict(kind="mathematics", revision_id=RevisionId, bindings=Bindings,
			inputs=[dict(path=PathValue, sha256=HashValue, role="correction-review-input") for PathValue, HashValue in sorted(Bindings.items())],
			targets=[Revision["new"]], author_ids=known_authors(project, Store, RevisionId), trust_boundary=TRUST,
			claims=[repair_claim(RevisionId, Revision)],
			metadata_warnings=[dict(version=Ref, warning="Opaque metadata: dependencies and author identities were not inferred. The coordinator must supply all known author IDs and the reviewer must examine original bytes.") for Ref in (Revision["old"], Revision["new"]) if Store["nodes"][key(Ref)].get("metadata_status") == "INVALID"])


def release(project, RevisionId, BundlePath):
	BundlePath = library.relative(project, library.inside(project, BundlePath))
	Input = dict(revision=RevisionId, bundle=BundlePath)
	def build(Store):
		Revision = revision_request(Store, RevisionId)
		require(Store["nodes"][key(Revision["new"])].get("metadata_status") != "INVALID", "an opaque repaired version cannot be released; correct its metadata first")
		Issue = Store["requests"][Revision["issue"]]["payload"]
		require(not (Issue["disposition"] == "retracted" and Revision["new"] in Issue["targets"]), "retracted exact bytes cannot be released as a repair")
		Revisions = [Event["request"] for Event in Store["events"] if Store["requests"][Event["request"]]["kind"] == "revision" and Store["requests"][Event["request"]]["payload"]["issue"] == Revision["issue"] and Store["requests"][Event["request"]]["payload"]["new"]["location"] == Revision["new"]["location"]]
		require(Revisions[-1] == RevisionId, "review of a superseded repair cannot release this card")
		Review = verify_bundle(project, BundlePath, required_bindings(project, Store, RevisionId), repair_claim(RevisionId, Revision), known_authors(project, Store, RevisionId))
		States, _ = impact_states(project, Store)
		for Ref in Store["nodes"][key(Revision["new"])]["dependencies"]:
			require(key(Ref) in States and States[key(Ref)]["reuse_allowed"], "repair still depends on an affected version")
		return dict(revision=RevisionId, bundle=BundlePath, review=Review)
	with library.writer_lock(library.library_root(project)):
		Result = append_request(project, "release", "release:" + library.digest(library.json_bytes(Input)), Input, build)
		Result = rebuild(project, Result)
		Store = load_store(project)
		Revision = revision_request(Store, RevisionId)
		States, _ = impact_states(project, Store)
		Result["reuse_allowed"] = States[key(Revision["new"])]["reuse_allowed"]
		Result["verdict"] = "RELEASED" if Result["reuse_allowed"] else "STILL_BLOCKED"
		return Result


def history(project, ToolPath=None):
	"""Explicit forensic view; old cards/notes are retained, never reuse recommendations."""
	with library.writer_lock(library.library_root(project)):
		Store = load_store(project)
		States, Problems = impact_states(project, Store)
		Location = library.relative(project, library.inside(project, ToolPath)) if ToolPath else None
		Notes = library.collect_notes(project)
		Versions = []
		for Key, Node in sorted(Store["nodes"].items()):
			if(Location and Node["location"] != Location):
				continue
			Versions.append(dict(Node, correction_state=States[Key], snapshot=library.relative(project, version_path(project, Node["sha256"])), annotations=[Note for Note in Notes if Note["tool_path"] == Node["location"] and Note["tool_sha256"] == Node["sha256"]]))
		return dict(verdict="HISTORY_ONLY_NOT_REUSE", versions=Versions, issues=issue_requests(Store), requests=Store["requests"], events=Store["events"], review_problems=Problems, canonical_action="NEEDS_RECEIVER_REVIEW", canonical_modified=False)


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Sub = Parser.add_subparsers(dest="command", required=True)
	for Name in ("issue", "revise", "review-inputs", "release", "history"):
		Command = Sub.add_parser(Name)
		Command.add_argument("--project", required=True)
		if(Name in ("issue", "revise")):
			Command.add_argument("--input", required=True)
		if(Name in ("review-inputs", "release")):
			Command.add_argument("--revision", required=True)
		if(Name == "release"):
			Command.add_argument("--bundle", required=True)
		if(Name == "history"):
			Command.add_argument("--tool")
	Args = Parser.parse_args()
	try:
		if(Args.command == "issue"):
			Result = register_issue(Args.project, library.read_json(Path(Args.input)))
		elif(Args.command == "revise"):
			Data = library.read_json(Path(Args.input))
			Result = propose_revision(Args.project, Data["issue"], Data["old"], Data["new"], Data["author"], Data["rationale"])
		elif(Args.command == "review-inputs"):
			Result = review_requirements(Args.project, Args.revision)
		elif(Args.command == "release"):
			Result = release(Args.project, Args.revision, Args.bundle)
		else:
			Result = history(Args.project, Args.tool)
		print(json.dumps(Result, ensure_ascii=False))
		return 1 if Result.get("verdict") == "STILL_BLOCKED" else 0
	except (ImportError, OSError, ValueError, TypeError, KeyError, RuntimeError) as Error:
		print(json.dumps(dict(verdict="INVALID", reuse_allowed=False, error=str(Error)), ensure_ascii=False))
		return 1


if(__name__ == "__main__"):
	raise SystemExit(main())
