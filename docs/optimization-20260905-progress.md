# Optimization implementation progress

Updated: 2026-09-05. State: PATCH_VALIDATED_RELEASE_SYNC_PENDING.

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

1. Commit and push manage 1.8.1 patch and replay evidence to parent, then fork, using existing SSH authentication.
2. Fast-forward the canonical clone at C:/Users/HuangZY/.dsh/_math-research-upstream/rigorous-open-math-research. In C:/Users/HuangZY/.dsh/math-research-dsh, sync through scripts/sync-from-parent.py, validate package 1.15.1 and commit/push. Existing junction installation follows that checkout.
3. Upgrade Codex marketplace math-research and add manage-math-research-program@math-research; verify 1.8.1 installed helper hash and doctor, then record remote CI results.
4. Do not start expensive L1/L2 solver experiments as part of this release. Those remain the approved plan's next separately frozen measurement stage.

## Recovery boundaries

No Q9 worker or research solver has been dispatched. No BVE accepted graph or checkpoint-bound mathematical artifact has been changed. No reset credit is authorized. The last account snapshot was five-hour used 80%, weekly used 44%; shared usage is not task consumption. Resume this maintenance from this file and git diff, not by replaying old mathematical work.
