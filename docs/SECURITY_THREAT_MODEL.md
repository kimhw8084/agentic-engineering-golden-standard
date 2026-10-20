# Threat model and minimum production safeguards

## Assets
Employee communications, recipes, server code, production data, device configuration, access tokens, audit records, user identity and model/tool context.

## Trust boundaries

User → authenticated UI/API → policy decision → scoped adapter → datastore; authorized evidence → retrieval/model (untrusted **content**) → typed draft → trusted deterministic validator → independent review → approved change system. Never authorize commands based on natural language text supplied by source data.

## Threats and controls

| Threat | Required design control | Negative test |
|---|---|---|
| Cross-user disclosure | Trusted SSO, per-record/per-source ACL at query time and output cache | User A cannot retrieve user B's message by keyword or citation |
| Prompt injection in email/repo/log | Treat retrieved text as data; typed bounded tools; no content-to-execution | Fake "system instruction" in doc never triggers tool |
| Stale/different recipe revision | Immutable provenance and revision pinning | Old revision cannot be represented as current |
| Accidental manufacturing mutation | No prod write capabilities exposed to LLM; separated approval executor | Mock/unauthorized write denied regardless of prompt |
| Artifact tampering | Canonical hash bound to validation and approval | Edited value invalidates validation/review |
| Identity impersonation | Signed identity tokens validated at API gateway/service; never trust caller roles | Forged header rejected |
| Duplicate effects | Idempotency, transaction locks, dedupe and replay protection | Retry produces one approved effect |
| Secret leakage in traces | Structured logging, redaction, retention, restricted telemetry access | Logs contain no token or source payload |
| Unapproved dependencies | CI dependency review, pinned versions, approved registry | Unapproved package rejected |

The `golden` toy code demonstrates only the hash-gate and simulated role-filter concepts. It lacks real authentication, policy evaluation, persistence, audit integrity, encryption, tenancy, threat monitoring and operational approvals.

## Adoption checklist

Data owner approval → classification/retention → threat model → read-only service identity → least privilege → tool allowlist → validation/provenance → independent signoff → monitored bounded pilot → production acceptance and rollback ownership.
