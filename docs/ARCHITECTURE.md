# Reference architecture and architectural decisions

## Three independent layers

**Engineering harness:** OpenCode and approved internal LLM, on-demand skills, tests, Git change workflow, documentation, evaluation. It creates and reviews *software*, not authoritative corporate knowledge or approval decisions.

**Application runtime:** each project supplies authenticated APIs, request routing, scoped read-only system adapters, permitted evidence retrieval, narrow agent reasoning/tool-use budgets, typed outputs, state transitions, metrics, and user interface. Work Intelligence and Manufacturing Intelligence should remain separately deployable with different data classification and ownership.

**Privileged execution:** deployment, production modifications, recipe actions and manufacturing commands are performed only through pre-existing company-authorized identity and change controls, independent of the model and isolated from untrusted generated text. This repo implements no such executor.

## Contracts and capability boundary

Versioned target contracts and lifecycle semantics live in [RUNTIME_CONTRACTS.md](RUNTIME_CONTRACTS.md).
Context assembly, pattern choice and tool policy are separate canonical specifications
listed in [GOVERNANCE.md](GOVERNANCE.md). These are requirements for consuming applications,
not implemented enterprise APIs.

Implemented here: full-scan synthetic lexical retrieval, simulated role filtering,
in-memory hash/state gates, offline evaluation and no-overwrite retrofit. The isolated
[synthetic investigation pilot](../examples/manufacturing/README.md) adds two pinned Python
snapshots, bounded AST traversal, a loopback browser journey and local SQLite supervision
(deduplication, admission, cancellation, stop/recovery and mutable event evidence).
These are synthetic demonstrations, with author-executed verification only. Absent from
enterprise runtime: authentication/source ACLs, distributed execution/recovery, protected
audit, model/embedding endpoints and authenticated independent operational approval.

## State and safety

`ChangeRun` implements only `created → evidence_ready → drafted → validated → reviewed → exported`.
Draft replacement from drafted/validated clears hashes; each gate rehashes current content.
`reviewed` means an unverified caller assertion, and `exported` means a local returned copy.
Repeated transitions fail; restart loses state. Mutable `events` are diagnostics, not an
integrity-protected audit log. The caller can mutate this Python object: it is no security
boundary. Target failure states and cancellation are defined in the runtime contract;
they are valid outcomes, not inherently invalid states.

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
