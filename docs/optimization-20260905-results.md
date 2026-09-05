# Codex optimization implementation, 2026-09-05

Implemented from baseline `516037f14f340107da8448b6e42df17317d9fc63` under the
[approved plan](codex-performance-optimization-plan-2026-09-05.md).
Release: workflow 1.15.0, rigorous 1.12.0, manage 1.8.1; Lean remains 1.6.0.

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
- New fixtures cover 7 library tests, 3 recovery tests, 2 metric tests and
  1 source-inventory test. Linux/Windows CI coverage was added; local Windows
  results alone do not establish a Linux CI result. Parent release validate CI
  subsequently passed on [GitHub Actions](https://github.com/xsoc1/rigorous-open-math-research/actions/runs/33952416286),
  as did [DSH CI](https://github.com/xsoc1/math-research-dsh/actions/runs/33952462186).
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

## Actual-artifact L0 follow-up

The no-model [replay driver](../scripts/replay_maintenance.py) copied 77 BVE
tool cards plus the existing README and index into a fresh external directory.
It retained all 3 legacy index rows and exercised current/stale candidate-note
retrieval. Fourteen existing headers need metadata review. These remain raw,
hash-bound pointers, excluded by default, without rewriting the source cards.
An independent follow-up found a missing-closing-delimiter case; after repair,
all [17 review checks passed](validation-20260905/manage-181-independent-review.json).
Final real-card replay exposed BOM compatibility in the legacy parser. The
repair accepts BOM, CRLF and closing delimiters at EOF, with retirement retained
across 12 encoding/body combinations in the seventh library regression test.

The same replay copied 187 bound checkpoint/lineage artifacts, preserving the
sequence-26 ID, `RIGOROUS_PARTIAL_RESULT` and 27 do-not-repeat action IDs. Receipt
retries reused identical bytes; tampering with the copied latest checkpoint was
rejected. All 267 original input files retained their hashes. There were zero
worker dispatches, model calls or new mathematical claims in this replay.
[Measured operations](validation-20260905/real-artifact-replay.json): card indexing
0.438 s, annotated query 0.096 s, latest-state inspection 6.680 s, preparation
19.515 s, retry 13.097 s. These single-run local operation times include full
lineage verification and do not measure solver speedup.

The [PDF transport replay](../scripts/replay_literature.py) used the actual
[arXiv v1 PDF](https://arxiv.org/pdf/1711.07032v1), retained 470532 raw bytes and
140497 extracted bytes, and reconstructed the text exactly through 29 bounded
reads. Candidate source notes were indexed and queried successfully. The
extraction contains 242 non-layout control characters; page 1 was rendered and
visually checked separately. Text transport is not formula-fidelity validation
or complete paper comprehension. Only metadata/hashes and
[replay results](validation-20260905/real-pdf-replay.json) are committed; the PDF
and its extracted content remain in the isolated local test directory.

The existing fork-sync workflow used `secrets` in a job-level condition, which
GitHub does not support. It now checks job environment values at step level,
following [GitHub context availability](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#context-availability).
The repaired [workflow passed](https://github.com/xsoc1/rigorous-open-math-research/actions/runs/33965542305).

## Instruction-context archive

Moved the complete old maintenance histories to same-directory
`AGENTS_HISTORY.md` files, retaining current rules and concise session pointers.
The parent entry changed from 46976 to 3444 UTF-8 bytes (-92.67%); the DSH entry
from 38947 to 3873 bytes (-90.06%). Historical text preservation was checked.
These are [static byte measurements](validation-20260905/agents-context.json)
at archival time, before subsequent concise release notes,
not measured token savings or end-to-end runtime improvements.

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
The final manage 1.8.1 parent CI and DSH 1.15.1 CI passed. Codex installation
and the active DSH junction match the released library helper hash. Retained
same-name skill copies are diagnosed explicitly; their runtime selection is
not inferred or silently changed.
