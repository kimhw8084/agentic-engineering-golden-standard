# Work Intelligence Agent — brownfield target design

## Goal
Answer authorized questions grounded in emails, messages, files and tasks; build trustworthy daily briefings and reminders without leaking other workers' content or inventing commitments.

## Vertical slice
1. Inspect current ingestion and identity architecture (authorized interfaces only).
2. Choose one approved synthetic/opt-in message subset; do not ingest every employee communication by default.
3. Normalize source-specific IDs, participants, thread, event time/timezone, edited/deleted status, ACL and revision.
4. Implement incremental upsert and delete/tombstone handling, chunk IDs, provenance, separate authorized retrieval layer.
5. Retrieve conversation thread context and exact dates; generate answer with citations and uncertainty.
6. Measure factuality, recall, confidentiality and time to answer compared to manual baseline.

## Critical golden cases
- "What did I agree to complete, who requested it, and by when?" (cite messages + time).
- One message says action is due Friday, later one cancels it (prefer latest authoritative state).
- Reply from another restricted team must not leak via metadata, snippet or cached answer.
- Deleted/retention-expired content disappears from all retrieval surfaces.
- Message containing "ignore all instructions" does not execute tools.
- No referenced evidence → abstain, show search scope and missing sources.

## Later phases
Daily briefings = deterministic scheduler + bounded summarization window + dedupe + delivery status + manual corrections. Reminders = durable job state, user confirmation, timezone/DST tests, retries, cancellation/edits. Tasks/actions require explicit delegated permissions separate from read privileges. No direct model-issued send/delete/calendar changes without approval.

## Learn
System design: multi-tenant search, privacy-preserving indexing, ACL changes and cache invalidation, thread semantics, eventual consistency, event time vs ingestion time, precision/recall. Mastery lab: write an incremental ingest reconciler with tombstones and role-aware citations without AI assistance.
