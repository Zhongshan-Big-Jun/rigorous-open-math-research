# L1 three-arm regression status

Updated: 2026-09-08. State: L1_COMPLETE.

The user requested completion of this round. Both registered tasks, all three
arms per task, and all six external blind audits are complete and frozen.
Every submitted proof passed external audit at 100/100, with no load-bearing
gap or repair. Five solvers returned normally. T2 A exhausted its wall allowance
with a saved proof; its external audit passed without changing that process status.
All six external audit processes returned normally. No stage should be rerun.

## Final artifacts

- CONCLUSIONS.md: Chinese decision, cost table, limitations and separate next steps.
- RESULTS.md: detailed stage history and final measured totals.
- comparison-l1.json and comparison-t2.json: complete machine-readable comparison.
- evidence/campaign-completion-checks.json: all 12 stages rechecked; 285 unique
  returned responses, frozen hashes, actual model/effort, score consistency and
  owned-process exit checks.
- evidence/t1-{a,b,c} and evidence/t2-{a,b,c}: verbatim answers, audits and usage.

Blank C has the lowest observed full-delivery cost at equal audited proof
quality on both tasks. New B misses both registered solver cost targets:
B/A paired median uncached input 1.448519 (target <=0.75), active wall time
0.937393 (target <=0.80). This is a development-regression observation, not a
causal or general plugin verdict. Quota interruptions, cold caches, the B audit
snapshot pause, authentication recovery and a changed desktop account/plan are
retained confounds. Unknown costs and timing scopes remain unknown.

## Immutable execution and recovery references

- Real checkout: /mnt/f/LaTeX/BVE research/_xsoc1_work.
- Campaign: /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1.
- Runtime: /home/huangzy/codex-benchmark-runtime/0.153.4/codex with its matching
  code-mode host and pinned catalog. All actual stages used gpt-6-astra / max.
- A commit: 516037f14f340107da8448b6e42df17317d9fc63.
- B commit: 6d6d739645981a5a2970b5faa26adda49a724113.
- Final solver: t2/c, root 01a08008-2b94-7352-baf8-b6ba7ba9d481, normal return.
- Final audit: control/audit-t2-C.json, root
  /home/huangzy/codex-benchmark/blind-audits/1729c39b-2b92-4f03-a8fc-e440ca4f8338,
  session 01a0801c-b396-7923-8718-c04ca59d1f35, normal return at
  2026-09-08T08:32:37Z. This session has no unfinished audit work.
- The prior T1-only and pre-quota-window seals remain preserved. The current
  seal records the documented quota-window adapter; no task or treatment was retuned.
- The initial invalid Linux C attempt and failed Windows preflights remain
  recorded in evidence and prior commits. They are not scored mathematical runs.
- Auth and raw session data remain outside Git. No reset credit was redeemed.
  Current runtime quota data use actually reported windows; null is not a
  five-hour percentage, zero, or unlimited.

## Next authorized work boundary

The completed L1 campaign is closed. Separate live literature-to-tool reuse and
controlled in-flight interruption acceptances remain, as detailed in
CONCLUSIONS.md. They must not mutate these offline attempts. L2 and model/effort
ablations are later stages, not automatically dispatched by this round.

This benchmark branch does not change released plugin versions, reinstall DSH
or Codex plugins, or integrate mathematics into the main project. Ignore the
malformed desktop cwd; use the real checkout above for maintenance.
