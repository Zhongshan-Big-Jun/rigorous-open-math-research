# L1 measured results

Development-task REGRESSION only. Updated 2026-09-07. T1 is complete: C, A and B
all passed the independent external audit at 100/100, with no load-bearing gap
or repair. B does not meet the observed T1 cost targets. T2 remains outstanding;
these interrupted development runs do not establish a causal plugin-only effect.

| T1 stage | Verdict | Score | Active seconds | Uncached input | Cached input | Output | Responses with usage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C blank solver | Frozen, independently accepted | - | 443.189 | 41354 | 86272 | 13231 | 7 |
| C independent blind audit | PASS, no load-bearing gap or repair | 100/100 | 393.085 | 32648 | 113408 | 12024 | 7 |
| C solver + external audit | Accepted | 100/100 | 836.274 | 74002 | 199680 | 25255 | 14 |
| A old solver, including internal audit | Frozen, independently accepted | - | 1277.998 | 123374 | 1425408 | 35714 | 29 |
| A independent blind audit | PASS, no load-bearing gap or repair | 100/100 | 432.192 | 62734 | 101120 | 12304 | 7 |
| A solver + external audit | Accepted | 100/100 | 1710.190 | 186108 | 1526528 | 48018 | 36 |
| B new solver, including internal audit | Frozen, independently accepted | - | 1151.973 | 244895 | 2307072 | 38060 | 41 |
| B independent blind audit | PASS, no load-bearing gap or repair | 100/100 | 362.029 | 30508 | 145920 | 9221 | 8 |
| B solver + external audit | Accepted | 100/100 | 1514.002 | 275403 | 2452992 | 47281 | 49 |

Full-delivery B/A ratios are 1.480 for uncached input and 0.885 for timed active
stages: B used 48.0% more uncached input and 11.5% less active time. Blank C has
the lowest observed cost at equal proof quality. Machine-readable totals, ratios
and unknown fields are in [comparison-t1.json](comparison-t1.json).

C proved the exact uniform polynomial root count and simplicity, with all
requested n=1, endpoint, midpoint and R=1 checks. The independent auditor
checked 17 claims and retained an additional exact algebra checker. The
checker supplements the submitted proof and is not the basis of uniform closure.

[Candidate](evidence/t1-c/answer.md), [audit](evidence/t1-c/audit/audit.json),
[solver usage](evidence/t1-c/usage-summary.json), and
[audit usage](evidence/t1-c/audit/usage-summary.json) bind this result.

Usage sums unique token_usage_record.response_id values across session files.
Cached input is included in provider input totals and subtracted once to obtain
uncached input. Reasoning output is included in output and is not added again.
These are returned usage records, not a conversion from account percentages.
Outer model calls, CLI command executions and complete nested tool calls are
different scopes; unknown aggregate active time and nested counts remain null.

The sum of timed solver and audit stages excludes the coordinator's intervening
setup work. Actual elapsed time from solver dispatch to audit return was about
1142.683 seconds; this first audit also required common harness preparation.
Keep setup/infrastructure costs separate in treatment comparisons. Earlier
INFRA_INVALID C and all its observed cost remain in the evidence directory.

The user explicitly removed quota reserves during C. C finished without hitting
its earlier loaded thresholds, so no interruption or extra wall allowance was
introduced. Later stages use the recorded no-reserve policy. This resource
amendment and the harness hash change must remain visible in comparisons.

A used one internal audit child. Its 29 returned responses include that child;
the interrupted in-flight response has no additional returned usage counter.
A naturally exhausted quota after 451.423 seconds, then completed the same
session using another 826.576 seconds. This does not establish a new-plugin
recovery benefit. See [continuation](evidence/t1-a/quota-continuation.json).

The solver exited normally. A local-file symlink blocked automatic freezing;
the stopped workspace was copied with that link materialized inside the frozen
copy after verifying the target and all before/after hashes. No solver rerun or
mathematical edit occurred. See [receipt](evidence/t1-a/freeze-reconciliation.json).
For external blindness, only A's leading status line reporting an earlier audit
PASS was removed from the auditor copy; all mathematical bytes remain unchanged.
The [binding](evidence/t1-a/blind-audit-binding.json) records both candidate hashes.

A's external audit checked 15 claims and retained a 16-identity exact algebra
checker. It exhausted quota after writing its report, then resumed the same
session for 41.105 seconds and returned normally. Its full 432.192 seconds and
all seven returned response records are counted. See [audit](evidence/t1-a/audit/audit.json)
and [audit continuation](evidence/t1-a/audit/quota-continuation.json).

At equal T1 proof quality, observed A/C solver ratios are 2.98 for uncached input
and 2.88 for active wall time. Full solver-plus-external-audit ratios are 2.51
for uncached input and 2.05 for active wall time. A includes two natural quota
continuations, so these raw observations do not isolate plugin overhead from
recovery overhead. One development task cannot establish a general performance
advantage; T2 is still required by the registered L1 comparison.

B returned after an authentication failure, a quota interruption and two
same-session continuations. Its internal audit resumed the original child task;
both root and child returned usage are included. B/A solver ratios are 1.985
for uncached input and 0.901 for active wall time. Neither meets the provisional
single-task targets of <=0.75 and <=0.80. B's continuation crossed about five
hours of quota waiting; keep all observed recovery and cache costs in these
ratios, without treating them as an isolated causal effect of plugin code.

B's auditor copy removes only the standalone leading workflow status and the
two-line footer disclosing the previous internal audit verdict. Mathematical
claims and verification limitations are unchanged. See [binding](evidence/t1-b/blind-audit-binding.json).

B's external auditor checked 17 claims and accepted the stronger root-location
bound as well as all requested cases. Its exact scratch commands are retained
verbatim because no separate checker file was written. See
[audit](evidence/t1-b/audit/audit.json) and
[commands](evidence/t1-b/audit/verification-commands.json).

Per-turn usage pinpoints a cache difference. A's root continuation first response
contained 54600 input tokens, 38784 cached. After B's five-hour interruption,
the first root response had 79780 input tokens with zero cached; its continuing
audit child's first response had 28377 with zero cached. Those costs remain in
the full totals. Grouping by actual thread and turn IDs also confirms that B's
audit continuation used the original child ID. See
[A turn usage](evidence/t1-a/usage-by-turn.json) and
[B turn usage](evidence/t1-b/usage-by-turn.json).

Elapsed dispatch-to-external-audit-return times were 1142.683 seconds for C,
46124.377 for A and 20012.582 for B. These include quota waits and coordinator
setup; the active-stage table above excludes those gaps. Do not confuse either
measure with summed root-plus-child active time, which remains unknown.

T2 B started at 2026-09-07T13:18:47Z after all six T2 preflight gates passed
without external model calls. Treatments, task and scoring remain unchanged.
The registered second task allows an honest exact partial result with a stated
first unresolved obligation. T2 has no scored result yet.
