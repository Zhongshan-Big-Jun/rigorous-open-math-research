# Identity reporting for inherited session logs

The C solver used three children with inherited context. Each child's log
starts with its own session_meta, then includes the parent's session_meta
inside the copied history. The sealed runner's raw per-file inventory uses
the last metadata record, so its id/source fields display the parent again.

This does not change response accounting. benchmark_usage.py groups each
token_usage_record by its own thread_id and deduplicates by response_id.
Inherited parent responses are counted once. Model/effort and forbidden
skill checks scan every relevant input record, and root resumption uses the
actual thread.started event stored in run/state.json.

The reporting layer now additionally exports session-identities.json,
binding the first session_meta to the UUID in its rollout filename. It
retains the raw metadata ID sequence and log hash for inspection, and
checks that every thread with returned usage has an identified log.
Observed child counts use this table. Original logs and raw inventories
are preserved unchanged. A regression fixture covers parent metadata
following child metadata and rejects a mismatched filename.

This is a read-only measurement/reporting correction. It changes neither
the sealed execution harness nor any prompt, budget, result, or score.
