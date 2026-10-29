# ADR-0002 — Test policy decisions without a live model or MCP server

Status: Proposed; independent review pending. Date: 2026-10-28.

Context: seven public v1 retrieval cases cannot establish answer correctness, holdout
generalization or production trust. No live endpoint or company corpus is authorized.

Decision: add a small deterministic tool-definition/scope/classification budget gate and
runnable denied/successful policy traces; extend existing evaluator with labeled metric
denominators, p95, public domain slices and content-hash provenance. Keep production
contracts in documentation. Existing skills link to canonical pages; no new agent/framework.

Alternatives: documentation only (no executable poisoning regression); live model/MCP
platform (credentials, dependencies and integrations unnecessary for this contract change).
Definition hashes require trusted enrollment; caller policy fields are simulated. Tool
arguments and full runtime schemas still need real adapter validation. No claim of model
prompt-injection resistance or enterprise readiness follows from these tests.

Tradeoffs: additional report fields and corrected MRR denominator need migration notes;
repeated scans increase offline run time but measure no model variance. Fresh protected
holdouts cannot be public fixtures. Rollback by revert; no external state. Revisit at
approved endpoint integration and independent curator handoff. Verification: metric
counterexamples, bad dataset rejection, provenance changes and tool drift/denial tests.
