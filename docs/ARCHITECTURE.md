# Reference architecture and architectural decisions

## Three independent layers

**Engineering harness:** OpenCode and approved internal LLM, on-demand skills, tests, Git change workflow, documentation, evaluation. It creates and reviews *software*, not authoritative corporate knowledge or approval decisions.

**Application runtime:** each project supplies authenticated APIs, request routing, scoped read-only system adapters, permitted evidence retrieval, narrow agent reasoning/tool-use budgets, typed outputs, state transitions, metrics, and user interface. Work Intelligence and Manufacturing Intelligence should remain separately deployable with different data classification and ownership.

**Privileged execution:** deployment, production modifications, recipe actions and manufacturing commands are performed only through pre-existing company-authorized identity and change controls, independent of the model and isolated from untrusted generated text. This repo implements no such executor.

## Data contracts (target specification, not implemented enterprise APIs)

- `TaskRequest`: actor identity from trusted identity provider, tenant, role, purpose, task type, target scope, version and idempotency key.
- `EvidenceRef`: source system, opaque record ID, permission scope, timestamp/timezone, immutable content revision/hash, lineage, canonical locator, retrieval time.
- `ToolInvocation`: tool id/version, allowlisted input schema, bounded timeout/retry policy, data classification, audit record.
- `DraftArtifact`: schema version, generator version, exact fields, content hash, provenance, environment classification.
- `ValidationResult`: validator version, passed rules, field-level failures, timestamp, hash, test environment.
- `Approval`: trusted reviewer ID, reviewed artifact hash, scope/expiry, independent approval policy and signature produced by approved system.
- `RunTrace`: run ID, trace/span, model and prompt/skill versions, tool telemetry, duration, cost proxy, errors, outcome classification.

In production *every authorization must be enforced again on the server/tool and data store*, not supplied by an LLM and not represented by the demo's caller-controlled role strings.

## State and safety

Desired production-oriented flow: `requested → evidence_ready → drafted → validated → review_pending → approved → handed_off`. Invalid states: `blocked`, `rejected`, `expired`, `quarantined`. Retries use deterministic idempotency keys; timeouts and interruptions persist state; approvals bind exact hashes and permissible target scope. The reference demo models only a simplified in-memory subset; persistence/locking is deliberately absent.

## Composition strategy

1. **Exact structured lookup** for equipment/job/product IDs and telemetry keys, with time-window and revision filters.
2. **Hybrid retrieval** for prose documentation when exact lookup is insufficient (BM25 + embeddings and rerank as justified by evaluation).
3. **Typed system tools** for restricted queries, no general SQL execution exposed to the agent.
4. **Coordinator** chooses one bounded workflow and gathers evidence; model does not invent nonexistent integrations or override tool policy.
5. **Deterministic executor** builds artifacts, validates schemas/domain rules and hands off to humans/approved external system.

## Failure policies

- Stale source revision: fail/flag based on task criticality, never pretend it's current.
- Source unavailable: return partial supported evidence and explicit unknowns; do not infer absence.
- Prompt injection: ignore any instructions from retrieved content, record suspicious payload, never execute tool instructions sourced from it.
- LLM timeout: safe partial state, no infinite retries, manual handling path.
- Parallel actions: optimistic concurrency compare-and-swap or DB transactions; a model may not manage race correctness.
- Secrets/data: approved company systems only, minimization and redaction in traces.

## Architecture decision records

Write an ADR for meaningful, hard-to-reverse choices (model/provider coupling, data persistence, retrieval approach, orchestration choice, privileges, schemas). Prefer modular monolith + typed adapters for a 1–3-person team; split services only after measurement demonstrates need. Avoid a multi-agent swarm without reproducible evidence that it improves results.
