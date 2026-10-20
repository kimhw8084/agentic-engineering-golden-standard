# Lecture 03 — Distributed systems, clocks and durable work

## Real problem
Your daily briefing service needs to ingest multiple upstream sources, retry when a message API fails, process edits/deletions and schedule user reminders correctly. Server changes and manufacturing events often arrive out of order.

## The three clocks
**Event time** (when an action happened), **processing time** (when your service handled it) and **ingestion time** (when your index stored it) are different. Sorting by ingestion time can misrepresent process chronology. Two systems' timestamps may differ because of clock skew, granularity, or timezone conversion. Tie-break events deterministically by IDs and record uncertainty when no total order is known.

## Delivery semantics
At-most-once risks loss, at-least-once risks duplication. "Exactly once" claims across separate systems are difficult and typically need deduplication plus transaction boundaries; aim for observable exactly-once *effects* with idempotency keys, unique constraints and a durable outbox. A retry budget with exponential backoff and jitter prevents all workers retrying at once.

A message consumer should track offset/checkpoint after durable processing, not before. When an index write succeeds but checkpoint fails, replay must be harmless. Source deletions also need replay/tombstones; otherwise deleted employee communications can remain in a vector index indefinitely.

## Failure reasoning
Model each stage as a state transition with at least: request received, scheduled, running, waiting external, completed, failed/retryable, dead-letter, canceled. Store last error category and safe idempotency token. Timeout does **not** prove a remote action failed—it may have completed before the response vanished. This is why blind retries of production commands are dangerous.

## Independent lab
Build a small durable job queue using SQLite with `jobs(id, idempotency_key UNIQUE, status, attempt_count, next_run_utc)`. Simulate 20 duplicate deliveries, worker crash after processing but before ACK, malformed payload and canceled reminder. Demonstrate one logical output, bounded attempts and manual recovery. Test a daylight-saving time boundary using timezone-aware datetimes.

## Defense questions
Why can retries double-execute an operation? What is an outbox? Which clock is correct for evaluating a production failure? How would you handle a canceled reminder already in-flight? What remains unsolved after adding a queue?

**Mastery gate:** executed crash/retry tests with documented failure model. Further reading: Google SRE workbook and Stanford CS144.
