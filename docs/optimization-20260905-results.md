# Codex optimization implementation, 2026-09-05

Implemented from baseline `516037f14f340107da8448b6e42df17317d9fc63` under the
[approved plan](codex-performance-optimization-plan-2026-09-05.md).
Release: workflow 1.15.0, rigorous 1.12.0, manage 1.8.0; Lean remains 1.6.0.

## Delivered behavior

| Area | Behavior | Entry |
| --- | --- | --- |
| Literature | Preserve actually retrieved raw/text bytes and source versions; find cached records; read bounded passages with exact continuation offsets | [Library runtime](../plugins/manage-math-research-program/skills/manage-math-research-program/references/library-runtime.md) |
| Annotatable tools | Candidate notes bind the exact card hash, author and source locator; generated pointers retain legacy metadata and human README content; stale/archived restrictions survive | Same runtime: `index`, `query`, `annotate` |
| Quota recovery | Verify the latest lineage, prepare or reuse the canonical receipt, detect successor drafts/concurrent state changes, reconcile workers before any action | [Recovery protocol](../plugins/math-research-workflow/skills/math-research-workflow/references/quota-interruption-recovery.md) |
| Context and cost | Resolve physical same-name skill copies without deleting them; update whiteboards on material decisions; align closure-first scheduling and verification tiers | Workflow `doctor.py --source-inventory --json` and updated skill references |
| Measurement | Preserve unknowns, normalize aliases, include output tokens as cost, enforce matching experimental identities, keep proof quality separate | [Performance observability](../plugins/math-research-workflow/skills/math-research-workflow/references/performance-observability.md) |

## Validation evidence

- Repository validator: 81 checks passed. Management skill manifest: 55 files.
- All 18 smoke scripts passed on Windows/Python 3.10 after updating the release
  assertion and inheriting `PYTHONUTF8=1` for subprocesses. Initial failures are
  disclosed here; they were not mathematical or recovery failures. Per-script
  exits and unscored local durations: [smoke results](validation-20260905/smoke-results.json).
- New fixtures cover 4 library tests, 3 recovery tests, 2 metric tests and
  1 source-inventory test. Linux/Windows CI coverage was added; local Windows
  results alone do not establish a Linux CI result.
- The first review attempt hit the account usage limit and returned no verdict.
  One replacement independent reviewer exercised isolated synthetic inputs and
  found P2 legacy applicability/retirement loss during reindexing. Its
  [before/after reproduction](validation-20260905/independent-finding.json)
  is retained. The fix preserves retirement and failure restrictions.
- The separate bounded repair review passed legacy preservation, documented
  source discovery/reading, and recovery races. Its
  [observed results](validation-20260905/independent-repair-review.json)
  include byte-exact two-version reads, `PENDING_DRAFT`, `STATE_CHANGED`,
  and zero dispatch. This review covers those runtime behaviors, not the
  correctness of any mathematical theorem or every possible filesystem failure.

## Limits and next measurement

No new solver benchmark, model comparison, mathematical proof audit or end-to-end
speedup measurement ran in this batch. Historical v1.7/v1.6 figures remain
historical; they do not measure these changes or the current model.
The next scored work is the plan's bounded matched experiment, with fresh quota,
frozen model/effort/input/harness/policy and independent quality assessment.

The library helper consumes actual web/browser retrievals or PDF extractions;
it does not fetch remote papers or certify extracted formulas. Candidate notes
never enter the accepted Blueprint graph automatically. A hard quota cutoff
cannot save work retrospectively; durable checkpoints and in-flight artifact
reconciliation preserve what reached disk. The index and generated README are
individually atomic, with documented retry recovery between their writes.

Main BVE research conclusions, Q9 workers and accepted graph were not modified.
Release/sync/install status is recorded in
[maintenance progress](optimization-20260905-progress.md).
