# User-directed removal of quota monitoring

Current execution note: the same-session continuation plan below was
superseded before inference by an observed child-input isolation failure.
See ISOLATION_REPLACEMENT.md. The original A is invalid and must not resume;
the fresh r1 campaign inherits this no-quota-monitoring policy unchanged.
The paragraphs below preserve the policy amendment as originally recorded.

On 2026-09-08, after the monitoring pause, the user explicitly instructed:
"额度充足, 别管额度问题了".

The coordinator stops quota queries and disables the campaign's quota launch,
staleness and reported-percentage gates. A separate hash-bound policy records
this instruction; no fictional fresh snapshot or remaining percentage is
created. Actual provider errors still return normally through the runner,
and no reset credit is redeemed.

The shared solver cap remains 3600 active seconds and the separate external
audit cap remains 1200 seconds. A resumes root UUID
01a080e5-fe27-7231-b1e0-ad74e3d92501 after 950.671529 seconds already used,
with 2649.328471 seconds remaining. No new attempt is created. The new policy
applies to A continuation, C, B and all three external audits.

Archive the original seal and loaded runner before binding the new runner
and user policy. All task, treatment, prompt, config, tool gates, model,
runtime, ordering and score hashes stay fixed. The earlier monitoring
interruption remains part of A's observed execution history. It is not
account quota exhaustion or evidence of a plugin recovery advantage.

The former fallback helper and its tests remain historical infrastructure
artifacts. Neither the desktop usage endpoint nor the fallback is polled
after this override.
