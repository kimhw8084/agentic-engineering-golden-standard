---
name: architecture-review
description: Review application or agent platform architecture with alternatives, operational tradeoffs and explicit trust boundaries.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Architecture Review

## Method
1. Restate quality attributes: correctness, latency, auditability, privacy, scope, team size and failure tolerance.
2. Present current architecture from code/evidence, then simplest viable incremental design.
3. Compare alternatives including no change. Evaluate coupling, consistency, concurrency, cache invalidation, rollback, deployment and costs.
4. Define typed contracts, state diagram, data boundaries, provenance and error/timeout behavior.
5. Write an ADR using `templates/ADR.md` and a decision table. Avoid microservices, swarms and vector DBs unless use case and measurements justify them.
6. Explain one concrete failure scenario and how the design detects/recovers.

### Deliverable
Updated architecture design, open risks, exact validation plan, reversible next step.
