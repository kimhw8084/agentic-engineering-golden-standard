# Changelog

Versions describe the standard, not production maturity. No tag is implied.

## 2.0.0 — proposed, unreleased

- Fix hash/state atomicity, strict simulated-review inputs, ID substring boost and installer
  symlink redirection; preserve all 24 original tests.
- Separate simulated approval, one-shot retries and mutable diagnostics from identity,
  idempotency and audit integrity. Centralize target states and message/cancel contracts.
- Add ownership/glossary, CODEOWNERS routing and numbered proposed ADRs.
- Add eight-pattern selection, context contract, MCP/tool governance and offline poisoning
  traces/tests; no dependencies, models or agents added.
- Add 30 public domain-seed cases, recall/precision/abstention/p95 and provenance. Correct
  MRR denominator; protected holdout/model/human grading remain protocols only.
- Add employee/adoption gates, skill manifest, migration and unaided exercise/defense/recall.
- Breaking changes/rollback: `docs/MIGRATION_V2.md`; results: `docs/V2_VERIFICATION.md`.

## 1.0.0 — baseline a655268

Initial synthetic OpenCode template, academy, installer, seven fixtures and 24 tests.
No enterprise runtime or production certification.
