# Q9 comparison recovery entry

State: COMPLETE. All three solver stages and three external audits returned
normally and are frozen. No stage remains to dispatch or resume.

- User request: select a harder repository problem and run old/new/blank comparison.
- Final report: [CONCLUSIONS.md](CONCLUSIONS.md).
- Machine comparison: [comparison.json](comparison.json).
- Repository overlap: [REPOSITORY_OVERLAP.md](REPOSITORY_OVERLAP.md).
- Active campaign, now closed: /home/huangzy/codex-benchmark/Q9-20260908-ASTRA-ABC-r2.
- Branch: codex/q9-astra-abc-20260908.
- Exact task: frozen TASK.md, Q9 in the remaining acute quadrature domain.
- Treatments: old A=516037f14f340107da8448b6e42df17317d9fc63,
  new B=6d6d739645981a5a2970b5faa26adda49a724113, blank C.
- Actual model/effort: gpt-6-astra / max for every scored root and child.
- Order: A,C,B, each solver followed by its separately budgeted blind audit.
- Fixed caps: solver and children 3600 seconds; external audit and children 1200.
- All six valid stages: one segment, exit 0, no stop reason or interruption.
- Quota queries, reserve gates and resets: disabled by user. Do not restore them.

## Completed results

A/B/C each received PASS 100/100, PROVED, root_closed=true, without substantive
gaps or auditor-supplied repair. B's final external audit checked 14 key claims
and independently reconstructed all 2565 exact certificate coefficients.
All three audit candidates are byte-identical to their original frozen answers.

| Stage | Root UUID | Active seconds | Recorded runner state |
| --- | --- | ---: | --- |
| A solver | 01a0812b-e1b4-7203-a59b-9dff0757e677 | 2477.650182 | RETURNED_UNAUDITED |
| A audit | 01a08155-6c5c-7501-add1-94840ddf1185 | 548.878768 | RETURNED_UNREVIEWED |
| B solver | 01a08188-1682-7611-9a7d-623663d5a538 | 2545.191219 | RETURNED_UNAUDITED |
| B audit | 01a081b2-68fc-7690-ba39-ba40f965211a | 625.152405 | RETURNED_UNREVIEWED |
| C solver | 01a0815e-b361-7b81-86f5-847de62d2841 | 1955.805844 | RETURNED_UNAUDITED |
| C audit | 01a0817f-8f44-7032-9bc0-a7b8d29658b4 | 527.603821 | RETURNED_UNREVIEWED |

The runner labels RETURNED_UNAUDITED and RETURNED_UNREVIEWED describe submission
states. The completed external verdicts are in evidence/q9-<arm>-audit/artifacts/audit.json;
they supersede any pending-verdict wording in earlier maintenance records.

Full delivery totals:

| Arm | Active seconds | Uncached input | Cached input | Output | Unique responses |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 3026.528950 | 369917 | 7725184 | 113459 | 122 |
| B | 3170.343624 | 365036 | 8044800 | 145770 | 138 |
| C | 2483.409666 | 468683 | 8024192 | 137792 | 215 |

B/A full-delivery ratios: uncached input 0.986805, time 1.047518, output 1.284781.
Blank C is fastest. These are one-task descriptive results, not a general speedup.

## Integrity and invalid attempts

Six-stage checks passed: 209 frozen-file hashes and 475 unique returned responses.
Original source files, blueprint.json and evidence_inventory.csv match the selection
hashes. See evidence/campaign-completion-checks.json and evidence/integrity-and-overhead.json.
Main-project mathematical integration has not been performed.

Both initial A attempts are invalid and preserved without mathematical scores:

- Original: /home/huangzy/codex-benchmark/Q9-20260908-ASTRA-ABC,
  950.671529 seconds, evidence/invalid-initial-A/.
- r1: /home/huangzy/codex-benchmark/Q9-20260908-ASTRA-ABC-r1,
  274.305798 seconds, evidence/invalid-r1-A/.

Do not resume, replace or reseal either invalid attempt, any completed r2 stage,
or the completed L1 campaign. CHILD_ISOLATION_AMENDMENT.md explains the r2 preflight
and live child metadata guard. SESSION_IDENTITY_NOTE.md explains inherited metadata
and the preserved corrected identity sidecars. No invalid-attempt content was given
to the valid solvers; invalid and valid returned response IDs are disjoint.

## Next scope

The requested harder comparison is finished. Literature-to-tool-library reuse and
controlled interruption recovery remain separate acceptance experiments. This
completion does not automatically dispatch L2 or another research wave. Use the
frozen reports as inputs to any subsequently requested optimization or integration.
