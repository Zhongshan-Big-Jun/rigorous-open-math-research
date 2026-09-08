# Genuine service-event quota fallback

During A, the desktop usage tool repeatedly returned "Could not read current
usage limits. Try again later." The solver still received successful service
responses with current account-wide Codex limits. Private checks confirmed
that the desktop and isolated run account match and their access tokens were
valid. No account or credential was changed.

While investigating snapshot staleness, the coordinator read a returned
token_count event carrying rate_limits.limit_id=codex, a 10080-minute primary
window at 4 percent used, null secondary, and plan_type=pro. The original
event timestamp was 18.06 seconds old when the first fallback was written.
The first credential-free evidence is quota-fallback-first.json. Subsequent
state inspection showed that the runner had already paused at 950.671529
active seconds, QUOTA_SNAPSHOT_STALE, shortly before the fallback was written.
The coordinator's preliminary "not interrupted" commentary was corrected.
This was a monitoring interruption, not observed account quota exhaustion.
The remaining solver budget is 2649.328471 seconds on the same root UUID.

Subsequent fallback reads require the same desktop account, valid explicitly
reported windows and a service event at most 120 seconds old. captured_at is
the original event timestamp, never the time it was read again. An exhausted
window remains exhausted; null/invalid values and other-model buckets are
rejected. A newer existing snapshot is retained. If neither source supplies
a fresh observation, the sealed runner's existing staleness gate still stops
work. Every fallback records the source file, line and line hash.

This changes only the external monitoring feed and applies to all remaining
stages. The sealed solver/audit harness, model, task, treatments, time caps,
scores and same-session continuation rules remain bound to their original
hashes. The original preregistration and seal are retained. No additional
attempt or budget is created. The fallback helper is independently tested
for original timestamps, exhaustion, invalid windows and account mismatch.
