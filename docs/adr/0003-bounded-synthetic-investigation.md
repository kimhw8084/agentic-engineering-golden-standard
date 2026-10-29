# ADR-0003 — Deterministic revision investigation before a model

Status: Proposed; independent review pending. Date: 2026-10-29.

Problem: the standard specifies revision-aware investigation, but has no end-to-end
implementation or stop executor. No company corpus, approved model endpoint, domain
curator or users are accessible in this session. Building enterprise integrations would
not produce valid evidence under that boundary.

Decision: add an isolated synthetic product slice over two bundled Python modules. A
curated hash-pinned manifest selects a root; AST parsing plus bounded graph traversal
returns exact excerpts/local call edges and unknowns without executing inspected code.
A standard-library loopback UI exercises the journey. SQLite transactions implement
local request deduplication, admission, cancel/result races, operator stop and recovery
fencing outside request/model content. A separate process controls the single capability.
The same trusted host reuses the existing tool policy, canonical hashing and evaluation
failure concepts; it does not retrofit the mutable ChangeRun toy into a security service.

Alternatives: A manual investigation remains the unmeasured real baseline. B literal search
is simpler but misses indirect toy dependencies; AST traversal is the selected B extension.
C a bounded model could help unstructured explanations/heterogeneous code, but has no
approved endpoint or measured incremental value here. Do not add it until paired evidence
shows benefit after human verification, rework, cost and operational burden.

Tradeoffs: narrow Python grammar, curated mapping and overapproximate static calls; no
runtime impact/value proof or protected labels. Local DB/key access bypasses the supervisor;
there is no SSO, remote-effect executor, signed audit or multi-host kill mechanism. Stop
cannot undo a read. Publication of old work is fenced even after recovery. For a shared
internal product reuse company identity/adapters/support, not this loopback prototype.

Review/rollback: two bounded PRs separate malformed-input fixes from this fixture. Revert
the fixture commit to remove the app; preserve any needed local evidence before operator
cleanup. No production migration or release is authorized. Existing configuration/skills
and tests are preserved. Acceptance evidence and remaining gates are recorded in
`docs/FIRST_WIN_READINESS.md`; normative controls remain in existing canonical documents.
