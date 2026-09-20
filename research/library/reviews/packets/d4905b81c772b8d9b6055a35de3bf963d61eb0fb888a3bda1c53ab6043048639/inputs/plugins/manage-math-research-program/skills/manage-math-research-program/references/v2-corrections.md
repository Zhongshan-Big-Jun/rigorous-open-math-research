# Executable corrections and exact-version review

`scripts/research_corrections.py` manages issues, propagation, repair proposals
and reviewed retrieval releases. It shares the library's `writer_lock`,
`immutable_write`, `atomic_write` and card snapshots. It does not modify the
accepted Blueprint graph. `canonical_nodes` are explicit versioned pointers for
the receiver to examine; their state is `NEEDS_RECEIVER_REVIEW`, not a canonical
mutation or a declaration that a downstream theorem is false.

## Intake and explicit dependencies

First index existing Markdown cards, including cards without `tool_id`. An old
index's IDs and metadata are retained. Without any index, issue intake can scan
the ordinary `tools` and `knowledge/tools` roots. For custom roots, run `index`
with the desired roots first. All paths below are relative to the explicit
project; the configured research root is honored.

```text
python LIBRARY index --project PROJECT --tool-root tools --readme tools/README.md
python CORRECTIONS issue --project PROJECT --input issue.json
```

`LIBRARY` and `CORRECTIONS` stand for the corresponding script paths. `issue.json`
has this shape; replace the hash placeholders with actual SHA256 values:

```json
{
	"issue_id": "audit-density-20260920",
	"origin": "external",
	"reporter": "audit-source-or-session",
	"summary": "The all-order generalization has an endpoint obstruction.",
	"disposition": "quarantine",
	"targets": [{"location": "tools/density.md", "sha256": "CURRENT_CARD_SHA256"}],
	"evidence": [
		{"path": "reports/audit.md", "locator": "Finding F08"},
		{"path": "reports/archive/density-before.md", "locator": "Audited old card"}
	],
	"canonical_nodes": [{"node_id": "DENSITY", "version": "ACTUAL_NODE_VERSION"}]
}
```

`origin` is `internal` or `external`. `disposition` is `quarantine` (default) or
`retracted`. Evidence requires local bytes and a locator; its optional `sha256`
detects an intervening edit. The runtime copies evidence to immutable snapshots.
An issue is an attributed audit input, not independently authenticated proof.
Its safety action is immediate. `canonical_nodes` is optional.

Cards declare dependencies in their frontmatter:

```json
{
	"dependencies": [
		{"location": "tools/upstream.md", "sha256": "EXACT_UPSTREAM_CARD_SHA256"}
	]
}
```

`depends_on` is an alias for `dependencies`, and `path` is an alias for
`location`. Prefer one spelling. Conflicting simultaneous spellings are rejected.
Every dependency must bind an actual saved version. Markdown links, similar
wording, source URLs and arbitrary legacy `status` strings are not inferred as
mathematical dependencies or judgments. Search the original sources separately
to discover omissions, then record the explicit edges. There is no guarantee
of propagation over an undeclared dependency.

The runtime retains version identities and explicit edges when saving and
indexing. A direct issue blocks its card family; exact dependency edges propagate
`needs_review`. The downstream claim is not declared false. Editing a file,
removing a dependency from its new frontmatter, changing a title or ID at the
same path, deleting the derived index, or rebuilding it does not clear this
state. Card paths, known tool IDs and exact copied bytes retain the affected
identity. An unrelated healthy experience card remains retrievable.

## Default pointers and explicit history

Default query recomputes the gate from authoritative correction records. Index
`items` and the generated README contain only unsuppressed entries; affected rows
are retained under `blocked_items` with `reuse_allowed: false` and a
`correction_state`. This flag concerns the correction gate, not mathematical
certification. All ordinary hits still require applicability checks.

```text
python LIBRARY query --project PROJECT --query "density"
python LIBRARY query --project PROJECT --query "density" --include-affected --include-stale
python CORRECTIONS history --project PROJECT --tool tools/density.md
```

`--include-affected` is explicit inspection only. Its blocked hits have trust
`HISTORY_ONLY_NOT_REUSE`. Existing archived, unreviewed and stale switches do not
override the correction gate. `history` exposes immutable old/new snapshots,
annotations at their original hashes, issues, revisions, review problems and
canonical impact pointers. Corrupt history is reported as an error, never silently
treated as empty. Raw copies of an old index or README can be stale: consumers
must use the current query gate, particularly after an interrupted pointer write.

## Propose a new version

Use the existing `card --tool ... --expected-sha256 ...` command to save the
repair. This preserves old card bytes and leaves the correction gate closed.
Then register the exact old and new versions:

```json
{
	"issue": "audit-density-20260920",
	"old": {"location": "tools/density.md", "sha256": "OLD_CARD_SHA256"},
	"new": {"location": "tools/density.md", "sha256": "NEW_CARD_SHA256"},
	"author": "ACTUAL_AUTHOR_SESSION_ID",
	"rationale": "Describe the changed hypotheses and the correction to be checked."
}
```

```text
python CORRECTIONS revise --project PROJECT --input revision.json
python CORRECTIONS review-inputs --project PROJECT --revision REVISION_ID
```

The `old` and `new` hashes must differ and use the existing card path. Renames
need a separate, explicit migration. The new hash must match current bytes.
`review-inputs` returns a packet specification usable by `research_review`:
`kind`, `inputs`, `author_ids`, `claims`, plus exact bindings and targets.
Keep all known author sessions in the packet. Card metadata may supply additional
`author_ids`; previous repair authors at this path are included automatically.

For a card already repaired before intake, target its **current** hash with
`quarantine` and attach the old report and archived old bytes as evidence. In
`revision.json`, `old` may additionally contain
`"snapshot": "reports/archive/density-before.md"`. The archive must hash to the
declared old version; it is copied into the card-version store without touching
the live card. This permits reviewing the existing new version without an
artificial edit. Exact bytes explicitly marked `retracted` remain withdrawn;
they cannot be passed back as the repaired version.

Old cards with malformed YAML (for example an unquoted scalar containing `: `)
can be issue targets and old repair versions. They are recorded as **opaque**
versions with `metadata_status: INVALID`, the parser error,
`dependencies_known: false` and no inferred edges. The empty edge array means
unknown dependencies, not an assertion that no dependencies exist. Snapshot
hashes are still checked. The source is neither rewritten nor discarded.
An opaque exact version is blocked even before an issue is committed, and a
later parser installation or reindex cannot silently upgrade its immutable
record. Explicit dependencies from other cards to that version still propagate
`needs_review`; the unreadable card's outgoing edges require source investigation.

For already quoted/repaired live cards, snapshot the damaged old bytes first,
then target that old hash in the issue, or supply its archived `snapshot` path.
The current version at the same path stays blocked by the issue. Register the
old/new revision normally. Merely quoting YAML or rebuilding the index does not
release it. The **new** version must have parseable metadata before release.
`review-inputs.metadata_warnings` identifies opaque inputs; author IDs cannot be
recovered from their broken frontmatter, so the coordinator must supply all known
author IDs and the reviewer must inspect the preserved original bytes.

## Release requires the coordinator's review verifier

The runtime calls only the fixed sibling
`research_review.verify_review_bundle(project, BundlePath)`. It has no boolean
PASS input, custom verifier CLI flag or alternate fallback. Missing verifier,
damaged receipt, incomplete or negative review, and `formal-readback` all leave
the gate closed. Readback is not a mathematics approval.

```text
python CORRECTIONS release --project PROJECT --revision REVISION_ID --bundle REVIEW_BUNDLE_DIRECTORY
```

Release requires all of the following:

- `kind: mathematics`, `verdict: APPROVED`, and
  `trust: COORDINATOR_ATTESTED_TOOL_TRANSCRIPT` from the verifier.
- The exact issue artifact and repair artifact, old/new card snapshots, current
  repaired card, captured issue evidence, and declared new dependency files in
  both `bindings` and `checked_paths`, with matching current hashes.
- An approved report claim with ID `correction:REVISION_ID`, generated by
  `review-inputs`, and the unchanged generated obligation in the verified packet.
  A generic approval or a substituted trivial claim cannot cover a repair.
- A reviewer distinct from all known authors and a repair that remains the latest
  proposal for this issue and card. The verifier separately validates the saved
  `fork_context: false` spawn and matching completion provenance.
- No remaining affected version among the new card's declared dependencies.

Issue and repair artifacts are canonical JSON at
`RESEARCH_ROOT/library/corrections/requests/SHA256.json`; their filename hash is
also the exact file hash. `review-inputs` supplies their actual paths and hashes.
Do not invent a packet path or replace the fingerprint with a prose summary.

Each release affects one exact new version for one issue. It does not release
old bytes or dependent cards. Fix and review each affected downstream card with
new exact upstream bindings. New issues still block previously released cards.
Changing a review input, corrupting a receipt or superseding a repair invalidates
the release; query rechecks receipts. Restoring a previously reviewed file alone
does not undo a newer repair proposal.

The trust boundary is the **trusted coordinator's saved tool transcripts**.
Local hashes cannot cryptographically prove that a service ran an agent, that
all authors were honestly declared, or that operating-system isolation occurred.
The runtime does not claim those properties, proof correctness or complete
formalization. Synthetic receipt fixtures used by tests are labeled as such and
are not actual independent reviews.

## Durability, contention and recovery

An immutable request is the durable intent. A hash-linked, ordered immutable event
commits it. An uncommitted request closes retrieval until the identical operation
is retried. Issue IDs are idempotency keys: changing input under the same ID is
rejected. Repairs and releases use deterministic input fingerprints. A committed
operation can be retried to rebuild a pointer view after an index/README failure.

The version registry has a checked membership catalog, immutable records and a
required-store marker. Correction-store and evidence integrity are checked on
every gate evaluation. Damaged or missing required data yield
`CORRECTIONS_INVALID`, no ordinary query hits, and a rebuilt index/README without
active pointers. Reindexing does not discard bad records to manufacture a clean
state. Preserve damaged bytes and restore exact known-good data from backup.

Library readers use the same writer lock to avoid observing a partial operation.
Concurrent writers get explicit contention; retry after the owner finishes.
After a hard process exit, independently establish that the owner ended, preserve
the stale lock by renaming it, then retry the identical request. Never remove a
live writer's lock. Temporary publication files can remain after a hard exit;
they are not accepted events. This is cooperative filesystem recovery, not a
remote transactional service or protection against an administrator rolling back
the entire project and all its integrity markers together.

## Python entry points and checks

```text
register_issue(project, Data)
propose_revision(project, IssueId, Old, New, Author, Rationale)
review_requirements(project, RevisionId)
release(project, RevisionId, BundlePath)
history(project, ToolPath=None)
```

`library.query_tools(..., IncludeAffected=True)` exposes the explicit inspection
view. The new behavior tests use isolated temporary projects, including an
all-order monomial-density counterexample fixture, transitive dependencies,
retained experience, pre-existing repairs, receipt binding, stale reviews,
corruption, abrupt process exit, concurrent writers and idempotent retries.
These are implementation-author checks; final independent acceptance is separate.
