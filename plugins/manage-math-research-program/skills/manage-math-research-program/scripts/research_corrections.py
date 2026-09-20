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
JOURNAL_SCHEMA = "research-corrections-journal/v1"
REGISTRATION_SCHEMA = "research-card-registration/v1"
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
	if("location" in Ref and "path" in Ref):
		require(all(isinstance(Ref[Name], str) and Ref[Name] for Name in ("location", "path")), "location and path must be nonempty paths")
		require(library.inside(project, Ref["location"]) == library.inside(project, Ref["path"]), "location and path disagree")
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
	Bound, Versions = [], {}
	for Ref in Dependencies:
		Ref = exact_ref(project, Ref)
		require(Ref["location"] not in Versions or Versions[Ref["location"]] == Ref["sha256"], "conflicting dependency versions at one location")
		Versions[Ref["location"]] = Ref["sha256"]
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
	recover_registration(project)
	Folder, Catalog, Marker, Pending = registry_paths(project)
	Existing = read_versions(project) if Folder.exists() or Marker.exists() else {}
	MetadataError = None
	try:
		Front, _, _ = library.read_metadata(Raw)
	except (ValueError, TypeError) as Error:
		# Intake must be able to quarantine the exact broken source, without repairing it.
		Front, MetadataError = {}, str(Error)
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
	if(Prior):
		require(Node == Prior, "conflicting version identity")
		return Prior
	library.snapshot_card(project, Raw)
	for Ref in Node["dependencies"]:
		if(key(Ref) not in Existing):
			register_version(project, Ref["location"], version_bytes(project, Ref))
	# Persist exact intent BEFORE publishing the binding. Recovery may complete
	# only this node against this exact prior catalog, never sweep in stray files.
	Intent = dict(schema=REGISTRATION_SCHEMA, node=Node,
		catalog_before=Catalog.read_bytes().decode("utf-8") if Catalog.exists() else None,
		marker_before=Marker.read_bytes().decode("utf-8") if Marker.exists() else None)
	library.immutable_write(Pending, library.json_bytes(Intent))
	recover_registration(project)
	return Node


def read_hashed(PathValue):
	Raw = PathValue.read_bytes()
	require(library.digest(Raw) == PathValue.stem, "immutable record hash mismatch: " + str(PathValue))
	Data = json.loads(Raw)
	require(isinstance(Data, dict) and library.json_bytes(Data) == Raw, "noncanonical immutable record: " + str(PathValue))
	return Data


def registry_paths(project):
	Base = library.library_root(project)
	Folder = library.inside(project, Base / "card-bindings")
	return Folder, library.inside(project, Folder / "catalog.json"), library.inside(project, Base / "card-bindings-required.json"), library.inside(project, Base / "card-binding-pending.json")


def catalog_names(Catalog):
	require(isinstance(Catalog, dict) and Catalog.get("schema") == SCHEMA and isinstance(Catalog.get("records"), list), "invalid version catalog")
	Names = Catalog["records"]
	require(all(isinstance(Name, str) and HASH.fullmatch(Name) for Name in Names) and len(set(Names)) == len(Names), "invalid version catalog identity")
	return set(Names)


def validate_version(project, Node):
	require(isinstance(Node, dict) and Node.get("schema") == SCHEMA and isinstance(Node.get("tool_id"), str) and Node["tool_id"], "invalid card binding")
	Ref = exact_ref(project, Node)
	require(Node["location"] == Ref["location"], "noncanonical card location")
	Raw = version_bytes(project, Ref)
	if(Node.get("metadata_status") == "INVALID"):
		require(Node.get("dependencies_known") is False and Node.get("dependencies") == [] and isinstance(Node.get("metadata_error"), str) and Node["metadata_error"], "invalid opaque version record")
	else:
		Front, _, _ = library.read_metadata(Raw)
		require(Node.get("dependencies") == bind_dependencies(project, card_dependencies(Front)), "card dependency binding mismatch")
	return Ref


def version_records(project, Names, Extra=None):
	Nodes = {}
	Folder, _, _, _ = registry_paths(project)
	Records = [read_hashed(library.inside(project, Folder / (Name + ".json"))) for Name in sorted(Names)]
	if(Extra is not None):
		Records.append(Extra)
	for Node in Records:
		Ref = validate_version(project, Node)
		Key = key(Ref)
		if(Key in Nodes):
			require(Nodes[Key] == Node, "conflicting version identity")
		Nodes[Key] = Node
	for Node in Nodes.values():
		require(all(key(Ref) in Nodes for Ref in Node["dependencies"]), "dependency version has no durable identity")
	return Nodes


def recover_registration(project):
	"""Under writer_lock: finish only a persisted exact-byte registration intent."""
	Folder, Catalog, Marker, Pending = registry_paths(project)
	if(not Pending.exists()):
		return
	IntentRaw = Pending.read_bytes()
	Intent = json.loads(IntentRaw)
	require(isinstance(Intent, dict) and library.json_bytes(Intent) == IntentRaw and Intent.get("schema") == REGISTRATION_SCHEMA, "invalid registration intent")
	Before, MarkerBefore = Intent["catalog_before"], Intent["marker_before"]
	require((Before is None and MarkerBefore is None) or (isinstance(Before, str) and isinstance(MarkerBefore, str) and json.loads(MarkerBefore) == dict(schema=SCHEMA)), "invalid registration baseline")
	Names = catalog_names(json.loads(Before)) if Before is not None else set()
	Node = Intent["node"]
	NodeRaw = library.json_bytes(Node)
	NodeHash = library.digest(NodeRaw)
	require(NodeHash not in Names, "registration intent is already in its baseline")
	After = library.json_bytes(dict(schema=SCHEMA, records=sorted(Names | {NodeHash})))
	CatalogRaw = Catalog.read_bytes() if Catalog.exists() else None
	require(CatalogRaw in (Before.encode("utf-8") if Before is not None else None, After), "version catalog differs from registration intent")
	MarkerRaw = Marker.read_bytes() if Marker.exists() else None
	ExpectedMarker = library.json_bytes(dict(schema=SCHEMA))
	require(MarkerRaw in (MarkerBefore.encode("utf-8") if MarkerBefore is not None else None, ExpectedMarker), "version marker differs from registration intent")
	Actual = {PathValue.stem for PathValue in Folder.glob("*.json") if PathValue.name != "catalog.json"}
	require(Actual in (Names, Names | {NodeHash}), "version membership differs from registration intent")
	NodePath = library.inside(project, Folder / (NodeHash + ".json"))
	if(NodePath.exists()):
		require(NodePath.read_bytes() == NodeRaw, "version binding differs from registration intent")
	# Validate all old records, the reserved new record and every exact snapshot
	# before any recovery write. Corruption is not an interrupted publication.
	version_records(project, Names, Node)
	library.immutable_write(NodePath, NodeRaw)
	if(CatalogRaw != After):
		library.atomic_write(Catalog, After)
	library.immutable_write(Marker, ExpectedMarker)
	Pending.unlink()


def read_versions(project):
	Folder, Catalog, Marker, Pending = registry_paths(project)
	require(not Pending.exists(), "unfinished version registration; retry the identical writer operation")
	require(Folder.is_dir(), "version registry is missing")
	require(library.read_json(Marker) == dict(schema=SCHEMA), "invalid version registry marker")
	Names = catalog_names(library.read_json(Catalog))
	Actual = {PathValue.stem for PathValue in Folder.glob("*.json") if PathValue.name != "catalog.json"}
	require(Names == Actual, "version catalog is incomplete or has unfinished registrations")
	return version_records(project, Names)


def key(Ref):
	return Ref["location"], Ref["sha256"]


def same_identity(Left, Right):
	return (Left["location"] == Right["location"] or Left["sha256"] == Right["sha256"]
		or bool(Left.get("tool_id") and Left.get("tool_id") == Right.get("tool_id")))


def journal_path(project):
	return library.inside(project, library.library_root(project) / "corrections-journal.json")


def journal_anchor(Store=None):
	Events = Store["events"] if Store is not None else []
	return dict(schema=JOURNAL_SCHEMA, requests=sorted(Event["request"] for Event in Events),
		event_count=len(Events), head=Events[-1]["sha256"] if Events else None, pending=None)


def initialize(project):
	Folder, Marker = root(project), marker(project)
	if(Marker.exists()):
		require(Folder.is_dir(), "correction store is missing; restore it, do not initialize a replacement")
		require(journal_path(project).is_file(), "missing journal anchor; explicit validated legacy adoption is required")
		return
	if(Folder.exists()):
		# Only a provably empty interrupted initialization is recoverable here.
		require(not any(PathValue.is_file() for PathValue in Folder.rglob("*")), "correction marker is missing")
	# An empty anchor is a known initialization intent, published before the
	# marker. Never infer an anchor from surviving requests or events.
	library.immutable_write(journal_path(project), library.json_bytes(journal_anchor()))
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


def read_journal_records(project, Nodes):
	"""Structural read only; callers MUST check an anchor or explicit legacy expectation."""
	Folder, Marker = root(project), marker(project)
	require(Marker.is_file() and Folder.is_dir(), "missing correction marker/store; reuse is closed")
	require(library.read_json(Marker) == dict(schema=SCHEMA, store=library.relative(project, Folder)), "invalid correction marker")
	for Name in ("requests", "events", "evidence"):
		require((Folder / Name).is_dir(), "missing correction store directory: " + Name)
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
		require(set(Event) == {"schema", "previous", "request"}, "invalid correction event fields")
		require(Event.get("schema") == SCHEMA and Event.get("previous") == Previous and Event.get("request") in Requests, "broken correction event chain")
		require(Event["request"] not in Used, "duplicate committed correction")
		Used.add(Event["request"])
		Events.append(dict(Event, sha256=EventHash))
		Previous = EventHash
	Pending = sorted(set(Requests) - Used)
	return dict(requests=Requests, events=Events, nodes=Nodes, pending=Pending)


def load_store(project, AllowPending=False):
	Folder, Marker, AnchorPath = root(project), marker(project), journal_path(project)
	if(not Marker.exists() and not Folder.exists() and not AnchorPath.exists()):
		Registry, _, RegistryMarker, Registration = registry_paths(project)
		HasRegistry = Registry.exists() or RegistryMarker.exists() or Registration.exists()
		return dict(requests={}, events=[], nodes=read_versions(project) if HasRegistry else {}, pending=[])
	require(AnchorPath.is_file(), "missing journal anchor; explicit validated legacy adoption is required")
	AnchorRaw = AnchorPath.read_bytes()
	Anchor = json.loads(AnchorRaw)
	require(isinstance(Anchor, dict) and library.json_bytes(Anchor) == AnchorRaw and set(Anchor) == {"schema", "requests", "event_count", "head", "pending"} and Anchor["schema"] == JOURNAL_SCHEMA, "invalid journal anchor")
	Names, Count, Head = Anchor["requests"], Anchor["event_count"], Anchor["head"]
	require(isinstance(Names, list) and all(isinstance(Name, str) and HASH.fullmatch(Name) for Name in Names) and Names == sorted(set(Names)), "invalid journal membership")
	require(type(Count) is int and Count == len(Names) and (Head is None if Count == 0 else isinstance(Head, str) and HASH.fullmatch(Head)), "invalid committed journal head")
	Store = read_journal_records(project, read_versions(project))
	Requests, Events = Store["requests"], Store["events"]
	require(set(Names) <= set(Requests) and len(Events) >= Count, "missing committed correction request/event")
	Committed = Events[:Count]
	require({Event["request"] for Event in Committed} == set(Names) and (Committed[-1]["sha256"] if Committed else None) == Head, "committed journal membership/head mismatch")
	Pending = Anchor["pending"]
	if(Pending is None):
		require(set(Requests) == set(Names) and len(Events) == Count, "unanchored correction request/event")
		Store["pending"] = []
	else:
		require(isinstance(Pending, dict), "invalid pending journal intent")
		validate_request(project, Pending, Store["nodes"])
		PendingHash = library.digest(library.json_bytes(Pending))
		require(PendingHash not in Names and all(Request["key"] != Pending["key"] for Name, Request in Requests.items() if Name != PendingHash), "conflicting pending correction identity")
		require(set(Requests) <= set(Names) | {PendingHash} and len(Events) <= Count + 1, "journal differs from pending intent")
		if(PendingHash in Requests):
			require(Requests[PendingHash] == Pending, "request differs from pending journal intent")
		if(len(Events) > Count):
			require(Events[-1]["request"] == PendingHash, "event differs from pending journal intent")
		require(AllowPending, "unfinished correction transaction; retry its identical request")
		Requests[PendingHash] = Pending
		Store["pending"] = [PendingHash]
	# A published event with a pending anchor is not yet a committed event.
	Store.update(events=Committed, journal=Anchor)
	return Store


def legacy_expectation(Store):
	"""Fingerprint a frozen, externally validated legacy journal, not evidence of completeness."""
	Requests = [Event["request"] for Event in Store["events"]]
	Events = [Event["sha256"] for Event in Store["events"]]
	return dict(requests=Requests, head=Events[-1] if Events else None,
		journal_sha256=library.digest(library.json_bytes(dict(requests=Requests, events=Events))))


def adopt_legacy_journal(project, Expected):
	"""Deliberate trust-boundary migration; never used by an ordinary read/write."""
	require(isinstance(Expected, dict) and set(Expected) == {"requests", "head", "journal_sha256"}, "supply the validated legacy request list, head and journal_sha256 explicitly")
	with library.writer_lock(library.library_root(project)):
		Store = read_journal_records(project, read_versions(project))
		require(not Store["pending"], "legacy journal has unfinished requests; recover with its original writer first")
		require(legacy_expectation(Store) == Expected, "legacy journal differs from supplied expected list/head/hash")
		# Check cross-request semantics and dependencies as well as exact bytes.
		impact_states(project, Store)
		Anchor = journal_anchor(Store)
		library.immutable_write(journal_path(project), library.json_bytes(Anchor))
		load_store(project)
		return dict(verdict="ADOPTED", **Expected, anchor=library.relative(project, journal_path(project)))


def request_info(project, RequestHash):
	PathValue = artifact(project, "requests", RequestHash)
	return dict(path=library.relative(project, PathValue), sha256=RequestHash)


def append_request(project, Kind, OperationKey, Input, Build):
	"""Durable intent before commit; an interrupted intent closes all retrieval."""
	recover_registration(project)
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
		library.atomic_write(journal_path(project), library.json_bytes(dict(Store["journal"], pending=Request)))
	Committed = any(Event["request"] == RequestHash for Event in Store["events"])
	if(not Committed):
		require(not set(Store["pending"]) - {RequestHash}, "conflicting unfinished correction transaction")
		library.immutable_write(artifact(project, "requests", RequestHash), library.json_bytes(Request))
		Event = dict(schema=SCHEMA, previous=Store["events"][-1]["sha256"] if Store["events"] else None, request=RequestHash)
		EventHash = library.digest(library.json_bytes(Event))
		PathValue = library.inside(project, root(project) / "events" / f"{len(Store['events']):08d}-{EventHash}.json")
		library.immutable_write(PathValue, library.json_bytes(Event))
		Store["events"].append(dict(Event, sha256=EventHash))
		library.atomic_write(journal_path(project), library.json_bytes(journal_anchor(Store)))
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
	Bindings = {}
	def bind(PathValue, HashValue):
		require(PathValue not in Bindings or Bindings[PathValue] == HashValue, "conflicting review input versions at one location")
		Bindings[PathValue] = HashValue
	for HashValue in (IssueHash, RevisionId):
		bind(request_info(project, HashValue)["path"], HashValue)
	for Ref in (Revision["old"], Revision["new"]):
		bind(library.relative(project, version_path(project, Ref["sha256"])), Ref["sha256"])
	bind(Revision["new"]["location"], Revision["new"]["sha256"])
	for Evidence in Issue["evidence"]:
		bind(Evidence["snapshot"], Evidence["sha256"])
	for Ref in bind_dependencies(project, Store["nodes"][key(Revision["new"])]["dependencies"]):
		bind(Ref["location"], Ref["sha256"])
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
		# Derive the full issue obligation before applying scoped releases. A
		# released upstream version must not erase its dependents' review duties.
		for Ref in Issue["targets"]:
			require(key(Ref) in Store["nodes"], "issue target version is missing")
		Changed = True
		while(Changed):
			Changed = False
			for Key, Node in Store["nodes"].items():
				Statuses = [Status for Other, Status in Blocked.items() if same_identity(Node, Store["nodes"][Other])]
				if(any(key(Ref) in Blocked for Ref in Node["dependencies"])):
					Statuses.append("needs_review")
				if(Statuses):
					Status = max(Statuses, key=Rank.get)
					if(Rank.get(Blocked.get(Key), 0) < Rank[Status]):
						Blocked[Key] = Status
						Changed = True
		for Key, Status in Blocked.items():
			RetractedTarget = Issue["disposition"] == "retracted" and Key in {key(Ref) for Ref in Issue["targets"]}
			if((IssueHash, Key) in Released and not RetractedTarget):
				continue
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
		recover_registration(project)
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
	for Name in ("issue", "revise", "review-inputs", "release", "history", "adopt-legacy"):
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
		if(Name == "adopt-legacy"):
			Command.add_argument("--expected", required=True)
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
		elif(Args.command == "adopt-legacy"):
			Result = adopt_legacy_journal(Args.project, library.read_json(Path(Args.expected)))
		else:
			Result = history(Args.project, Args.tool)
		print(json.dumps(Result, ensure_ascii=False))
		return 1 if Result.get("verdict") == "STILL_BLOCKED" else 0
	except (ImportError, OSError, ValueError, TypeError, KeyError, RuntimeError) as Error:
		print(json.dumps(dict(verdict="INVALID", reuse_allowed=False, error=str(Error)), ensure_ascii=False))
		return 1


if(__name__ == "__main__"):
	raise SystemExit(main())
