# L1 three-arm regression status

Updated: 2026-09-08. State: T1_COMPLETE_T2_B_AUDITED_A_RUNNING.

User requested continuation. Preparation and one infrastructure-invalid attempt
are recorded. Completed solver runs: 4 (T1 C, A, B and T2 B). Scored/audited runs: 4.
All T1 blind audits PASS, 100/100, no load-bearing gap or repair.
A solver used 1277.998200 active seconds; its external audit used 432.192049.
T1 B launched at 2026-09-07T01:48:49Z. Inspect t1/b/run/state.json before dispatch.
Its first segment exited after 12.037755 seconds because the isolated refresh
token was already used. Only private same-account authentication was refreshed.
Session 01a0798d-cd6d-7b22-bbd2-bb4b4a1fdb43 resumed at 01:51:36Z with that time
still charged. No new attempt or config change was introduced.
B then exhausted quota during internal audit after 538.843714 cumulative active
seconds. The user requested continuation again; segment 03 resumed the same
session at 2026-09-07T07:03:44Z with 1261.156286 seconds left. Its existing private
access token remained valid. Candidate proof and research records are retained.
B returned normally and froze at 07:13:58Z after 1151.973121 active seconds.
It returned 244895 uncached input, 2307072 cached input and 38060 output tokens.
External B audit launched at 07:16:20Z. Mapping: r1/control/audit-t1-B.json.
Opaque root: /home/huangzy/codex-benchmark/blind-audits/63711bf5-ec61-453e-b47b-715ee6b7cbb8.
That audit returned normally at 07:22:22Z after 362.029277 seconds. All 17
checked claims pass. T1 comparison and cost limitations are in RESULTS.md and
comparison-t1.json. No T1 solver or auditor should be dispatched again.
The intended experiment remains old plugin A / new plugin B / blank Codex C,
with T1 order C,A,B and T2 order B,A,C. T2 is sealed and its B arm started at
2026-09-07T13:18:47Z with fresh same-account private authentication.
T2 B then hit the actual quota limit after 1172.987794 active seconds. The user
requested continuation on 2026-09-08 local time. Session
01a07c05-7813-7f23-89c6-f4aea5101e6a resumed at 2026-09-07T23:34:50Z with
627.012206 seconds remaining. The saved answer and candidate proof survived.
T2 B returned normally at 2026-09-07T23:44:32Z after 1754.826646 active seconds.
Its frozen candidate proves c=1/2, C=10^12 and t0=1024 according to the completed
external audit. Solver usage: 277157 uncached input, 2351360 cached input, 69407 output,
55 returned responses across the root and two children. No extra budget was used.
Its external audit started at 23:47:10Z; mapping is control/audit-t2-B.json,
opaque root /home/huangzy/codex-benchmark/blind-audits/0123470f-b6de-45a5-bd7e-fabe1d7af8e4.
The audit paused at 23:52:12Z after 302.375437 seconds because the coordinator's
quota snapshot exceeded five minutes, not because account quota was exhausted.
After a fresh positive snapshot, audit session
01a07e44-c25b-7913-977c-d2f3fb87dc2e resumed at 23:54:39Z with 597.624563
seconds remaining. The original candidate, task and audit allowance are unchanged.
That audit then exhausted actual quota at 2026-09-08T00:00:04Z after saving its
reports. The user requested continuation and reiterated using the available
quota. The original audit resumed at 04:54:42Z with 272.784132 seconds remaining
and returned normally at 04:55:25Z. Total active time: 670.340627 seconds.
External verdict: PASS 100/100, 15 checked claims, no load-bearing gap or repair.
Full B delivery: 2425.167273 active seconds, 415542 uncached input, 86552 output.
T2 A started at 2026-09-08T04:57:17Z after refreshing private same-account auth.
Root session: 01a07f60-ad98-7b10-b036-3be86f11c5dc. Inspect t2/a/run/state.json
before any dispatch; it has the original 1800-second solver allowance.
T2 A paused at 2026-09-08T05:14:19Z after 1022.394337 seconds because the live
account snapshot reached zero. The saved Fourier and kernel estimates remain
in its workspace, but answer.md had not yet been written. The next continuation
has 777.605663 seconds remaining, not a new 1800-second allowance.
The desktop now selects a different Pro account with one reported seven-day
Codex window. The preregistration amendment records this resource confound and
the runner's support for actual reported window durations. The old seal remains
in control/SEALED-before-quota-windows.json. No five-hour value is fabricated.
A resumed the same root session at 2026-09-08T07:33:37Z using the currently
selected desktop account. Its quota snapshot reports one seven-day window,
100% remaining. There is no reported five-hour value. The changed runner hash
and unchanged treatment gates are bound in evidence/quota-window-amendment.json.

## Current verified execution path

- Real checkout: /mnt/f/LaTeX/BVE research/_xsoc1_work. Ignore malformed desktop cwd.
- Current campaign: /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1.
- Isolated CLI: /home/huangzy/codex-benchmark-runtime/0.153.4/codex, plus its
  matching code-mode host. Both binaries and the bundled catalog are hash-bound.
  The PATH CLI 0.149.1 is not part of this experiment.
- A commit: 516037f14f340107da8448b6e42df17317d9fc63.
  B commit: 6d6d739645981a5a2970b5faa26adda49a724113.
  All arms use gpt-6-astra / max and the same basic tools and child limit.
- Existing WSL loopback proxy now works. No previously rejected bridge was run.
- All T1 and T2 arms passed filesystem and network isolation, expected skill metadata,
  actual functions.exec sandbox execution and synthetic same-session resume.
  These stub tests used no external model calls and no real auth credentials.
- control/SEALED.json binds the manifest, harness code and all twelve successful
  task/arm gates. T2 homes had zero solver sessions when their gates were sealed.
  The previous T1-only seal is retained in control/SEALED-before-t2.json.
- Four deterministic runner checks and all 81 repository checks passed.
- T2 A launch quota snapshot: 2026-09-08T04:57:16Z, five-hour remaining 81%, weekly
  remaining 97%. Historical snapshot only. The user has removed both reserve thresholds.
  Read live quota before dispatch; no reset redemption was authorized.

## A quota interruption and continuation

- Original session: 01a076cc-139f-76f1-aede-3af2443f3a4a.
- Segment 01 exited with code 1 after 451.422577 active seconds. CLI events
  explicitly report usage-limit exhaustion. The runner recorded INFRA_EXIT
  because the CLI exited before the next account snapshot reached zero.
- Segment 02 started at 2026-09-06T13:11:55Z with the same session ID and
  1348.577423 seconds remaining from the original 1800-second allowance.
  The research ledger, contract and candidate proof survived the interruption.
- This is an observed infrastructure recovery in old arm A, not a controlled
  test proving an advantage of the new plugin. No mathematical score is assigned
  before the returned candidate is frozen and independently audited.
- External A audit also hit actual quota after saving its PASS report, at
  391.086886 active seconds. On the user's 2026-09-07 continuation it resumed
  session 01a076e8-54ca-7531-b267-9c8372da88ed, returned normally after another
  41.105164 seconds, and was frozen. Scores, input/output hashes and actual
  model/effort were checked. All 15 claims pass; no repair was supplied.

## Exact next action

1. Read this file, git status and r1 control/SEALED.json. Do not prepare another
   campaign or reinstall the plugin. Inspect any run/state.json before dispatch.
2. Obtain a fresh account snapshot. Update r1 control/quota.json with captured_at
   (UTC ISO timestamp), limit_id=codex, and nonempty windows containing each
   actually returned window_duration_mins and remaining_percent. Preserve the
   plan and any spend block; do not assume primary means five hours. These are
   account-level data, not treatment costs. The user explicitly removed quota reserves. Launch with positive available
   quota; stop on actual exhaustion, stale snapshots or the fixed wall cap.
3. All T1 solvers/audits and T2 B solver/audit are complete. Do not repeat them.
   Inspect T2 A's t2/a/run/state.json. If it pauses or exits due to quota, use
   its original solver session and remaining allowance:

   python3 -X utf8 scripts/benchmark_runner.py --root /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1 --task t2 --arm A --resume
4. Refresh the quota file during execution. It expires after five minutes;
   actual exhaustion or creating run/STOP causes cancellation and checkpoint.
   The runner retains segment logs, root ID, observed child sessions and elapsed
   budget. An ordinary PAUSED state can use --resume with the same task/arm;
   --reconcile handles uncertain exits without creating another attempt.
5. T2 order is B,A,C, each followed by the same separately budgeted blind audit.
   Freeze and measure A's returned answer before its external blind audit, then C. Refresh each fresh
   arm's private same-account authentication before launch. Complete usage deduplication
   before aggregate cost comparisons. Missing returns or usage stay UNKNOWN.
6. Feature literature-to-tool reuse, controlled research interruption, L2 and
   model/effort ablations remain later work. They do not alter these offline arms.

## Preserved invalid attempt and earlier evidence

Initial Linux campaign: /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC.
Its C root was 01a07589-bd4d-7291-bb67-129338dbe34b, stopped after 62.290282 s.
Two calls failed because code_mode_host was disabled while the schema still
exposed functions.exec. A child dispatch was observed. This is INFRA_INVALID,
not a mathematical failure. Its invalid-attempt.json prevents continuation.
Known root cumulative usage is 33755 input (21888 cached) and 469 output.
A second file reuses the root header ID and has no returned usage; total child
cost is unknown. Do not sum inherited/fork records as separate fresh usage.

Windows preparation and failed probes remain under
F:/benchmark/L1-20260906-ASTRA-ABC. Restricted and explicit-deny probes could read
forbidden files, so no Windows solver was launched. A network timeout alone did
not certify isolation. Automatic approval rejected a bridge start with only
blocked by policy; no bridge receipt or process was created by that command.
The existing proxy later became reachable after the user changed environments.

Git contains only manifest/probe summaries and invalid-attempt observations.
Auth files, raw sessions and private runtime data remain outside the repository.
Current BVE mathematics, accepted graph and Q9 were not changed. This benchmark
branch does not change released plugins or require a DSH/runtime installation.
