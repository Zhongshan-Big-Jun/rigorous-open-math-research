# Optimization implementation progress

Updated: 2026-09-09. State: FIRST_BATCH_RELEASED_AND_VERIFIED; L1_AND_Q9_COMPARISONS_COMPLETE.

## Contract

User approved the optimization plan and added actual source reading, agent-annotatable tool cards and pointer tables, and quota interruption recovery. Preserve independent mathematical audit and immutable checkpoint semantics. Baseline: 516037f14f340107da8448b6e42df17317d9fc63.

## Completed and verified

- Main release de540c0 published to parent and fork: workflow 1.15.0, rigorous 1.12.0, manage 1.8.0; Lean remains 1.6.0. Codex installed those versions and doctor passed. DSH 1.15.0 published through 87b4ce4.
- Parent validation and DSH CI passed. The old job-level secrets condition was repaired in bc4a03a; its validation and fork-sync CI passed.
- Manage 1.8.1 patch handles malformed or unterminated legacy metadata explicitly, supports BOM/CRLF/header-only cards, and corrects PDF extraction line numbers. Seven library tests pass, including retirement across 12 encoding/body combinations. The prior independent review passed 17 focused checks; the final BOM fix is covered by local regression and real replay.
- L0 real replay: 77 cards indexed, 14 flagged for metadata review, 3 legacy rows preserved. Sequence 26 uses 187 recovery files and retains 27 do-not-repeat IDs. Receipt reuse and tamper rejection pass. All 267 original files remain unchanged.
- Real arXiv PDF: 470532 raw bytes, 140497 extracted bytes, exact reconstruction through 29 bounded reads. Candidate notes are searchable. Extraction has 242 non-layout control characters; visual page inspection does not certify all formulas.
- Parent/DSH maintenance histories moved intact to AGENTS_HISTORY.md. Entry byte reductions are 92.67% and 90.06%, not measured solver savings.
- Full release suite previously passed: parent 81 checks + 18 smoke scripts + 4 plugin/4 skill validators; DSH 51 checks + 22 smoke scripts + bundle/sync checks. Affected patch checks are rerun before publication.
- Results and evidence: docs/optimization-20260905-results.md and docs/validation-20260905/.

## Next actions

The implementation batch is complete. The separately frozen L1 old/new/blank
regression completed on 2026-09-08: all six proofs passed external blind audit,
but the new plugin missed the observed solver cost targets. Blank Codex had
the lowest observed complete-delivery cost on both development tasks. Quota,
cache and account/plan differences prevent causal plugin-only attribution.
See the [L1 conclusion](../benchmarks/codex-20260906-l1/CONCLUSIONS.md) and
[current status](../benchmarks/codex-20260906-l1/STATUS.md).

The user then requested a harder repository problem. The Q9 frontier comparison
completed all three solver and external-audit stages on 2026-09-08 UTC. All three
proved Q9 and received PASS 100/100 with full root closure. New/old full-delivery
uncached input was 0.986805, time 1.047518, and output 1.284781. Blank Codex was
fastest. See [Q9 conclusions](../benchmarks/codex-20260908-q9/CONCLUSIONS.md),
[machine data](../benchmarks/codex-20260908-q9/comparison.json), and
[repository overlap](../benchmarks/codex-20260908-q9/REPOSITORY_OVERLAP.md).
All six valid stages returned in one uninterrupted segment on the same account.
Two earlier isolation-invalid attempts are preserved separately without scores.
This task does not establish a general speedup or replace the L1 results.

The next separate work is live literature-to-tool reuse and controlled in-flight
interruption acceptance, followed by scoped ablations before considering L2.
No L2 stage is automatically dispatched and no solver-speedup claim is made.
Resolve the actual loaded skill path before using helpers: the physical source
inventory still reports retained same-name direct/personal copies and does not
infer runtime selection from their existence.

## Publication and installation

- Parent and fork patch: 0af24619ccb57170d3d53f8477ee163cb5cc6604. Parent
  [validation](https://github.com/xsoc1/rigorous-open-math-research/actions/runs/33967089706)
  and [fork sync](https://github.com/xsoc1/rigorous-open-math-research/actions/runs/33967089709)
  passed. Existing SSH authentication avoided the HTTPS credential prompt.
- DSH package 1.15.1: 2b80ea4cb546f66eaf21eaf7129e86ff7d6013bd, inherited via
  the canonical parent clone and sync script. Its
  [CI passed](https://github.com/xsoc1/math-research-dsh/actions/runs/33967225740).
  Subsequent documentation-only parent commits may update the lock without
  changing the released runtime or package version.
- Codex marketplace math-research refreshed; manage 1.8.1 installed. The source,
  installed Codex helper and live DSH junction helper all have SHA256
  4b73ff5c0f3ff4c257bc5d9a1847276359854e7e5756450262c9fd268cffa7f8.
  [Doctor report](validation-20260905/installed-doctor.json): 0 failures. The
  JSON object is extracted from the doctor's existing mixed text/JSON stdout.

## Recovery boundaries

L1 and Q9 are complete and immutable. Do not resume their solver or audit sessions.
Q9 recovery and completion evidence is in benchmarks/codex-20260908-q9/STATUS.md.
The main project's nine source files, blueprint.json and evidence_inventory.csv
still match the selection hashes. Q9 proofs are benchmark artifacts awaiting any
separately scoped main-project integration. The user disabled quota queries,
reserve gates and quota-driven coordination; do not restore them or redeem resets.
Future acceptance work starts from these release records and frozen comparisons.
