# Fresh-context review packets

`scripts/research_review.py` makes evidence snapshots and checks review receipts.
The coordinator performs the actual subagent calls. The helper neither starts
an agent nor turns a report into a Lean proof.

## Prepare and dispatch

Supply only the files needed to check the named obligations. List all author
session identities. Each claim declares its actual checking method; `formal`
means the reviewer must inspect the supplied exact-target machine evidence,
not that this packet tool itself runs Lean.

```json
{
  "author_ids": ["author-session-id"],
  "kind": "mathematics",
  "inputs": [
    {"path": "proof/lemma.md", "role": "proof"},
    {"path": "tools/lemma.md", "role": "tool-card"},
    {"path": "research/library/corrections/issue.json", "role": "correction"}
  ],
  "claims": [
    {"id": "lemma", "statement": "Check the stated lemma and its scope in the card.", "verification": "analytic"}
  ]
}
```

```text
python REVIEW --project PROJECT prepare --input spec.json
```

The result contains a frozen packet and the exact reviewer prompt. Invoke
`multi_agent_v1__spawn_agent` with `fork_context:false` and this prompt as
`message`. Save the actual invocation and response in a JSON object with keys
`tool`, `arguments`, `result`; `tool` is `multi_agent_v1__spawn_agent`.

The current `collaboration.spawn_agent` adapter is also accepted. Save its
actual `task_name`, `fork_turns:"none"`, exact `message`, and returned canonical
`result.task_name`. The canonical task path remains the reviewer identity;
the storage directory uses a path-safe digest. Preserve the native fields
instead of inventing an old UUID or converting them to the legacy adapter.

```text
python REVIEW --project PROJECT dispatch --packet PACKET --spawn-transcript spawn.json
```

The returned `bundle` is the run identity. Retrying the same dispatch is
idempotent; it does not launch or reuse any agent. Do not fabricate an agent ID
or a successful tool response to make a packet complete.

## Receive and recheck

The reviewer returns one JSON object as specified in the emitted prompt. Save
the actual `wait_agent` result, including `status[agent_id].completed`, then:

For the current collaboration adapter, save the actual delivered message as
`message_type:"FINAL_ANSWER"`, `task_name` (recipient parent), `sender` (the
dispatched canonical task), and `payload` (complete original JSON report text).
`wait_agent` availability notifications and ordinary messages contain no final
review and cannot complete a bundle. Missing completion remains pending.

```text
python REVIEW --project PROJECT receive --bundle BUNDLE --completion-transcript completion.json
python REVIEW --project PROJECT verify --bundle BUNDLE
```

The receiver checks reviewer identity, exact prompt and explicit fresh context,
all claim results, checked paths, and hashes of current inputs and frozen bytes.
Changed proofs, issue records, snapshots or transcripts invalidate reuse. An
incomplete or negative review remains available but never becomes `APPROVED`.
Missing completion, an author's identity and a bare `pass:true` are rejected.
Every read repeats the packet schema checks: authors and unique obligations must
be present, modes and blind-readback roles must be supported, and the directory
must match the packet's content hash. One reviewer identity is bound immutably
to one packet and spawn transcript. A changed packet requires a fresh reviewer.
Ambiguous JSON with duplicate keys is rejected at every object depth, including
per-claim verdicts. Existing historical bundles without an identity record are
not retroactively promoted; retain them as history and dispatch a fresh review.

For blind formal readback use `kind:"formal-readback"`, input roles only
`formal-statement`, `definitions`, `environment`, and claims containing only
`id` and `declaration`. Strip informal intent from the supplied source extracts;
role labels cannot remove bias hidden in comments. A readback is not mathematical
approval and cannot release a correction. A separate fresh reviewer compares
the actual readback, formal evidence and intended theorem.

## Trust and recovery

The explicit trust boundary is `COORDINATOR_ATTESTED_TOOL_TRANSCRIPT`. Native
responses must be saved by the trusted coordinator outside the reviewer's write
scope. The helper detects inconsistent or stale records, not a malicious
coordinator fabricating a complete transcript. It provides no OS sandbox or
service-side cryptographic attestation. Context isolation and read-only file
scope must also be respected by the actual orchestration.

Packet inputs and receipts are immutable. Partial publication can be retried
with identical bytes; a different review needs a new dispatch identity. A
timeout, missing reviewer or unavailable Lean check leaves the relevant
obligation open. Preserve the packet and actual agent/job identity for resuming
collection; do not restart unknown external work automatically. Re-reviewing a
changed proof uses a new packet and a fresh stateless reviewer.
