# ADR-0001 — Preserve the teaching harness and make its boundaries testable

Status: Proposed; independent review pending. Date: 2026-10-28.

Context: v1 already contains substantial safety/mastery guidance and 24 passing tests.
The gap matrix identifies hash/state and exact-ID defects, and target/demo ambiguity.

Decision: preserve the dependency-free modules, original tests and OpenCode configuration.
Fix gates and installer path boundaries; keep caller-attested review explicitly synthetic.
Centralize definitions instead of adding a production engine. Add contracts and offline
examples in subsequent bounded commits. No new dependency, model, server or agent.

Alternatives: leave v1 unchanged (preserves misleading gates); replace it with a durable
platform (unjustified integration/operation cost and authorization requirements). Small
fixes cost an extra hash per gate but retain a comprehensible teaching implementation.

Failure model: caller can mutate all in-memory fields; no hostile-process protection,
durability, true independent identity or audit integrity. Filesystem symlink checks prevent
ordinary accidental redirection; no hostile concurrent filesystem actor guarantee.

Verification: negative tests for mutation before/after validation, atomic serialization,
false independence claims, identifier substrings, repeated install and symlink paths.
Rollback: revert these commits; no stored data migration. Revisit when an approved pilot
requires durable authenticated services. No production claim is accepted by this ADR.
