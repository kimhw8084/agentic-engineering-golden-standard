# Manufacturing System Intelligence — brownfield target design

## Goal
Develop a Principal-engineer-quality architecture companion grounded in approved source code, recipe/config schemas, logs and domain descriptions, with explicit revision awareness and demonstrated correctness. Do not assume "all the source code in the prompt" equals understanding.

## Vertical slice
1. Locate bounded approved repository/revision and an example synthetic/approved recipe schema.
2. Parse module/dependency/API/call-site indices using proper language-aware tools where available; fall back to annotated code search, do not claim perfect static call graph.
3. Build typed relationships `code_symbol → config_field → validator → recipe_parameter → processing_step` with revision, evidence link and confidence type (static/dynamic/assumed).
4. Map a single "what happens if parameter X changes?" question to authoritative code locations and validators.
5. Retrieve relevant code/config evidence under permitted scope; answer with commit SHA, filename, line range, schema version and unknown runtime consequences.
6. Validate via human domain expert and executable fixture/simulation; no live production changes.

## Critical golden cases
- Compare parameter behavior across two code revisions; do not cite stale branch as current.
- Detect a parameter referenced by both default config and per-run override.
- Explain code execution path; identify dynamic dispatch, feature flags or external services which static code alone cannot resolve.
- Recipe value passes schema but violates a semantic constraint (must be caught by domain validator).
- Source unavailable must produce 'insufficient evidence', not invented root cause.
- "Create/modify a real production recipe" must route to separately approved workflow; this agent makes reviewable local drafts only.

## Learn
AST, symbol resolution, language-server tooling, dependency graphs, schema versioning, data lineage, event-driven architecture, distributed tracing, fault-tree reasoning. Mastery lab: independently implement a version-pinned dependency walker and test ambiguous symbol resolution, cycles and unseen runtime behavior.

## Metrics
Citation precision/recall by question type, exact revision accuracy, top-k source recall, expert-rated change-impact correctness, number of unsupported confident claims, latency and tokens. Report coverage limitations.
