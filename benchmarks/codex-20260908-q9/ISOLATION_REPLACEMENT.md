# Replacement after an observed isolation failure

The initial Q9 A attempt is excluded before scoring because account-level
remote plugin hydration added `deep-research-work` and `plugin-management`
skill metadata to both child agents. The root's initial input was clean.
No call to either extra plugin was found, but unassigned skill metadata in
child inputs violates the frozen treatment. `remote_plugin=false` alone
did not prevent this behavior. See evidence/remote-cache-input-scan.json.

The original attempt used 950.6715293199959 active seconds and stopped at
the former quota-snapshot gate. A later resume command was rejected by the
installed-plugin hash check before starting inference. No second segment
ran. The attempt is now permanently marked invalid and must not be resumed.
Its mathematical quality was not used to decide exclusion; it has no score.

Evidence and partial artifacts are preserved in evidence/invalid-initial-A/.
The 49 unique returned responses account for 189239 uncached input, 1612928
cached input, and 41533 output tokens, including 19456 reasoning tokens.
These are separate infrastructure-loss costs, not valid A performance.
Unknown in-flight consumption is not estimated.

The replacement campaign is:

`/home/huangzy/codex-benchmark/Q9-20260908-ASTRA-ABC-r1`

All three homes and solver histories are fresh. No original A mathematical
content is supplied to them. TASK.md, task-spec.json, original treatment
commits, model, reasoning effort, tool set, time caps, score rules, and A,C,B
order remain unchanged. Each solver has 3600 active seconds shared with its
children, followed by a separate 1200-second external audit. The original
PREREGISTRATION.md and seals are preserved; this document records the
infrastructure amendment, not a new mathematical selection.

All homes explicitly disable the three account-level remote bundles
`deep-research-work`, `openai-templates`, and `plugin-management`. An identical
already-hydrated copy is seeded before hashing to exercise this condition.
The entire remote-cache directory is denied to research tool processes.
Zero-inference gates verify that the extra skill metadata is absent, its
cache is unreadable, and the assigned research skills remain readable.
A live session check also stops any solver or audit whose root or children
receive the forbidden skill metadata. The replacement is sealed only after
all three filesystem and operational-tool gates pass.

USER_QUOTA_OVERRIDE.md remains effective: no quota queries, reserve, snapshot
gate, or reset redemption. Its original same-session continuation plan was
superseded only by the subsequently discovered isolation violation above.
