# Runtime reference contracts — version 2.0

Target specification for consuming applications, not implemented production APIs.
Reject unknown major versions/fields, invalid types, nonfinite numbers and naive times.
Identifiers are nonblank opaque strings; timestamps are RFC3339 UTC; hashes are SHA-256
over a declared canonical JSON encoding (sorted keys, compact separators, UTF-8, no NaN).
Do not equate canonical JSON hashes with source byte hashes; declare which is bound.
Use exact schema validation and domain validators at the trusted server boundary.

All messages carry `contract_version`, `message_id`, `run_id`, `created_at`, `tenant_id`.
Clients may propose values; server authenticates identity, authorizes scope and binds
correlation IDs. No natural-language field can authorize an action.

| Contract | Required fields beyond envelope | Enforced invariants |
|---|---|---|
| TaskRequest | actor_ref, purpose, task_type, target_scope, input_hash, idempotency_key, deadline_at, max_steps, max_tool_calls, max_cost | Trusted identity/policy supplies actor and tenant; finite positive budgets; scope subset of grants; deadline enforced outside model. |
| EvidenceRef | source, record_id, revision, content_hash, hash_kind, locator, event_at, retrieved_at, permission_scope, classification, extractor_version | Recheck ACL at fetch/output/cache; immutable revision; event vs retrieval times distinct; missing/stale source explicit. |
| ToolInvocation | invocation_id, parent_span_id, server_id, tool_id, definition_hash, input_hash, argument_ref, policy_decision_ref, timeout_ms, attempt, idempotency_key, classification | Exact approved definition; runtime authorization rechecked; bounded attempts/deadline; arguments schema-validated; redacted references in traces. |
| DraftArtifact | schema_version, generator_version, artifact_hash, hash_kind, evidence_refs, target_scope, environment, payload_ref | Exact schema and revision; local draft only until validated; no execution permission. |
| ValidationResult | artifact_hash, validator_version, environment, rule_results, passed, validated_at | Every required domain rule passes on same hash and target scope; missing validator blocks. |
| ApprovalDecision | decision_id, reviewer_ref, policy_version, decision, artifact_hash, validation_ref, target_scope, expires_at, signature_ref | Authenticated independent identity; allow/deny explicit; trusted signature verification, expiry/revocation/scope/hash rechecked at handoff. A boolean is insufficient. |
| RunTrace | trace_id, spans, implementation_commit, dataset_hash, model_ref, prompt_hash, skill_manifest_hash, policy_version, outcome, failure_category, metrics | Per-span start/duration/status; redact payloads, classify access/retention; missing metrics null with reason; trusted audit sink separately required. |
| Cancellation | request_id, actor_ref, reason_code, requested_at, expected_state_version | Authenticated actor may cancel own scope; compare-and-swap state version; acknowledgment records canceled / already_terminal / pending_remote_reconciliation. |

Metrics schema: correctness, retrieval recall/MRR/precision, citation grounding, latency_ms,
tool_calls, model_calls, input/output_tokens, cost_amount/currency/basis, leakage_count,
task_success. Each has a measurement scope; unavailable values are null with a reason,
never an inferred zero. Trace span status: ok/error/denied/canceled/timeout.

## Target lifecycle (not ChangeRun)

| From | Allowed next states / gate |
|---|---|
| requested | evidence_ready after authorized source retrieval; blocked on unavailable required source |
| evidence_ready | drafted with evidence bindings |
| drafted | validated only after deterministic schema/domain validation; rejected on invalid input |
| validated | review_pending with exact artifact/validator/scope bindings |
| review_pending | approved or rejected by authenticated decision; expired at deadline |
| approved | handed_off after signature/hash/scope/expiry/revocation recheck |
| any nonterminal | canceled before handoff; quarantined on integrity/policy incident; expired at deadline |
| blocked | requested only by explicit authorized resume with fresh budget/state version |

Terminal: handed_off, rejected, expired, canceled, quarantined. Handoff is not evidence
that a downstream company action executed. New attempts after terminal outcomes require
a new request/key. Draft editing invalidates approval and returns to drafted. Optimistic
state versions and atomic state+event persistence prevent conflicting transitions.
Ticket evidence statuses in Definition of Done are a different vocabulary.

## Retry, crash and cancellation protocol

Persist `(tenant, actor, operation, idempotency_key, input_hash)` atomically with result and
state version. Same key/hash replays stored outcome; differing hash conflicts. Key lifetime
must exceed retry/reconciliation windows. Timeout means unknown remote outcome; reconcile
by operation ID before retrying effects. Store state/event together or use a transactional
outbox; diagnostic tracing does not provide this guarantee. Reauthorize resumed requests.

Cancellation sets a durable flag and state version; workers check before every tool call,
after results and before handoff. A cancel/handoff race is decided by one atomic transition.
Already handed-off work returns already_terminal plus external reconciliation reference;
never promise rollback of a remote effect. Late results cannot restore canceled state.
Stop at the first of deadline, step/call/cost budget, cancellation or policy denial.
These full enterprise contracts are not executable here. The separate synthetic pilot
(`examples/manufacturing/README.md`) exercises a narrow local SQLite admission/cancel/stop
subset; it does not implement this envelope, employee identity, signatures, distributed
cancellation, remote effects or independent operational approval. `ChangeRun` is unchanged.
