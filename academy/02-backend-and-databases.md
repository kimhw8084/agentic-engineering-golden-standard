# Lecture 02 — Backend engineering, database transactions and schemas

## Target problem
An agent drafts a manufacturing operational file, validates it, gets reviewer signoff and emits a package. Concurrent retries and schema changes must not allow unvalidated or unreviewed outputs.

## From typed APIs to safe state
An endpoint should validate the shape of a request, enforce authentication from trusted identity infrastructure and attach scoped server-side authorization. An LLM prompt cannot authenticate a reviewer. In the reference `golden/change.py`, `is_independent=True` is caller-controlled and therefore **only a toy representation**. Production must obtain reviewer identity, independence policy and approval from authenticated company services.

A schema encodes syntax and types. Domain validators encode physical/operational constraints and may vary by equipment/product/revision. Passing a JSON schema is necessary but often insufficient for manufacturing correctness. Version every input and validator; store the content hash so approved bytes cannot silently change.

## Transactions and consistency
Imagine two simultaneous requests both attempting to approve revision 7. In-memory `if status == validated: status = approved` is a classic time-of-check-to-time-of-use race. With a database, use a transaction and compare-and-swap update such as `UPDATE requests SET status='reviewed' WHERE id=? AND status='validated' AND draft_hash=?`; require exactly one updated row. Persist an immutable audit event in the same transaction or use an outbox if a separate consumer needs delivery.

ACID vocabulary: Atomicity groups state changes, Consistency preserves constraints, Isolation bounds concurrent behavior, and Durability keeps committed changes after crash. Isolation levels differ: read-committed prevents dirty reads but may permit nonrepeatable reads; serializable has stronger guarantees and potentially lower throughput. Learn the exact database used by your company.

## Data design
Versioned entity tables might contain `source_system`, `external_id`, `revision`, `valid_from`, `ingested_at`, `content_hash`, `classification` and owner. Uniqueness for `(source_system, external_id, revision)` prevents one class of ingest duplicates. Logical deletion/tombstones must propagate into retrieval indices. Add indexes around actual query predicates—equipment ID + time window, for example—not every field indiscriminately.

## Independent lab
Implement a versioned change store using SQLite or a thread-safe fake. Two workers try the same transition; only one should succeed. Add crash/restart persistence, duplicate idempotency key and stale revision rejection. Write SQL migration and index justification. Run independent tests and explain the transaction boundary.

## Defense questions
How would you guarantee the approval is for exact bytes? Why are schema and domain validation different? How do you coordinate the DB commit with an external message? What race is prevented by compare-and-swap? How do you migrate old draft versions safely?

**Mastery gate:** personally implemented transaction, concurrent test and documented failure/rollback behavior. Further reading: CMU 15-445.
