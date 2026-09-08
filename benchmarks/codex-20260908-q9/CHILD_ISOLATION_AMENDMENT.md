# Delayed child isolation and the r2 replacement

This supersedes the r1 execution plan in ISOLATION_REPLACEMENT.md, preserving
that document and its seal. The r1 A run stopped after 274.3057983930048
seconds when its first child received the same forbidden remote skill
metadata. The child had made zero outer tool calls. The guard correctly
stopped work, but the earlier root-only gates did not cover this path.
Both initial A attempts are invalid, unscored, preserved, and must not resume.
No mathematical quality was used to select either replacement.

The r1 loss contains 10 unique returned responses: 35580 uncached input,
350208 cached input, and 6660 output tokens, including 1908 reasoning tokens.
See evidence/invalid-r1-A/. Add this separately to the initial infrastructure
loss; neither is valid A performance. Unreturned consumption is unknown.

A local Responses fixture using the same private account authentication for
plugin metadata synchronization reproduced the fault after a 35-second
delay before child creation. No model inference or quota query was made by
this fixture. The root input was clean, while the child received
deep-research-work and plugin-management. Adding explicit disabled entries
for remote SKILL.md paths removed those entries from both inputs under the
same delayed fixture. Authentication stays private and is not exported.

The new benchmark_child_probe.py now executes the actual child-spawn path
against a loopback Responses fixture, checks root and child model/effort and
assigned skill counts, and executes the filesystem/network checks from the
child. Account metadata synchronization remains enabled in this probe so
the earlier false-negative condition is not recreated. All model responses
are fixture data, and their zero usage is never counted as research usage.
The original functional same-session-resume gate remains in place.

All remote skill files are explicitly disabled in each new home, in addition
to the plugin-level switches and filesystem denial. Audits receive the same
disabled remote cache before configuration. The runtime can remove the
harness's cache canary, so that marker alone is excluded from plugin-byte
hashes. Assigned and unassigned real plugin files remain hash-bound. The
read-denial gate uses an existing remote skill file when available.

The valid replacement campaign is:

`/home/huangzy/codex-benchmark/Q9-20260908-ASTRA-ABC-r2`

All scored histories are fresh. The exact TASK.md, original A/B commits,
blank treatment, model, max effort, basic tools, A,C,B order, 3600-second
solver cap, 1200-second external-audit cap, and scoring remain fixed.
No original or r1 mathematical content is passed to r2 solvers. The r2 seal
also binds the delayed-child helper and requires its passing gate.
Quota monitoring stays disabled under the user's instruction.
