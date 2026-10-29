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

The original hash/role toy classes lack real authentication, audit integrity, encryption,
tenancy, threat monitoring and operational approvals. The isolated synthetic investigation
adds a local policy gate and SQLite supervision only; it does not supply enterprise controls.

<a id="synthetic-investigation-risk-register"></a>

## Synthetic investigation risk register — 2026-10-29

Severity describes consequence **if misused for company work**, not a claim of production
exposure. All corporate owner roles below are **UNASSIGNED**; no real pilot is authorized.
The source for NIST function names is the [AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
(AI RMF 1.0, checked 2026-10-29; NIST notes a revision is in progress). This is a scoped
mapping to GOVERN, MAP, MEASURE and MANAGE, not certification or a full RMF assessment.

| ID / severity; threat and consequence | Data/system/trust boundary | Owner | Prevention and detection; status/evidence | Residual risk / deployment decision; NIST |
|---|---|---|---|---|
| R1 Critical: forged identity discloses restricted data | Employee → gateway → source grants | Security + source owner | Production SSO/ACL specified only. Synthetic server fixes grants, rejects role fields, host/origin forgery and missing browser capability; `test_investigation_http`, adversarial role-impersonation counterexample | Browser session capability is not employee auth; OS users can read local public specimens. Block shared/company deployment. GOVERN, MAP, MEASURE |
| R2 High: forged review or recomputed hashes authorizes wrong artifact | Draft/validator/reviewer → privileged executor | Runtime + independent reviewer | No executor added. ChangeRun hash gates detect ordinary mutation, but recomputing public fields bypasses them; `test_adversarial.test_recomputed_hashes_bypass_mutable_toy_not_security_boundary` | Authenticated independent approval, signatures, expiry/revocation are specification only. Block consequential handoff. GOVERN, MEASURE, MANAGE |
| R3 High: wrong revision or changed bytes supports incorrect impact claim | Manifest/source → resolver/result | Source owner | Explicit revision, source byte pin, exact excerpts, no latest/cache; `test_revision_changes_exact_source_and_dependency`, drift/duplicate tests | Manifest trusted via OS/review, not signed; static scope does not establish deployed revision. Block internal use until approved source chain. MAP, MEASURE, MANAGE |
| R4 High: retries/concurrency duplicate effects | Request → durable admission → adapter | Technical owner | Local owner/key/input uniqueness, atomic state/events, single claim/read budget; concurrent submission and duplicate-worker tests | Only local reads/results. No remote dedupe/outbox or distributed operation proof. Forbid external-effect tools. MEASURE, MANAGE |
| R5 High: stop/cancel race publishes unsafe late result | Operator capability → supervisor → worker/read/output | Operational support owner | Separate-process stop disables admissions/capability, cancels work, epochs fence output; crash, in-flight, deadline, race, recovery tests | Admitted OS read may finish; cannot undo disclosure/effects. Local mutable audit and OS bypass remain. Synthetic drill only. GOVERN, MEASURE, MANAGE |
| R6 High: poisoned/drifting tool or malformed scopes gains authority | Registry/tool definition → runtime gate | Security + tool owner | Trusted bundled definition hash at invocation; strict frozenset grants fixes reproduced substring bug; nested definition drift tests | Trusted registry enrollment and live MCP endpoint verification absent; no external servers approved. Deny external tools. GOVERN, MEASURE, MANAGE |
| R7 High: source/log/context exposure leaks company data | Source → UI/model/telemetry/export | Source + security owner | Two bundled synthetic sources only; no model/network egress; source displayed as text; HTTP capability/CSRF/CSP checks. Browser smoke observes loopback-only requests | No company classification/retention pipeline or SSO; operator key Windows ACL unverified. Do not substitute proprietary data. MAP, MEASURE, MANAGE |
| R8 High: missing/dynamic edge becomes a confident false conclusion | AST/curated roots → employee judgment | Domain + technical owner | Partial/unknown outcomes, missing-source/dynamic/nested-scope/cycle/budget tests; exact citations | Narrow syntactic call graph, not data flow or equipment behavior. Independently check mapping and representative language cases before a real investigation. MAP, MEASURE |
| R9 High: contaminated labels/partial hits create false readiness | Dev cases → evaluator → promotion | Evaluation owner | 32 public author-generated cases marked development; legacy partial-hit counterexample; locator denominators and null business/independent metrics | No protected holdout, independent labeling or calibrated graders. Block accuracy/generalization claims and promotion. GOVERN, MEASURE, MANAGE |
| R10 Medium: unowned service or fictional savings scales poor value | Demo → group rollout → organization | Sponsor + support owner | Named-role slots and promotion gates in readiness report; active time/rework/support measurement follows existing impact protocol | No users, sponsor, observed reuse, costs or real benefits. No automatic 200-person extrapolation. Remain at synthetic single-user proof. GOVERN, MAP, MANAGE |

## Adoption checklist

Data owner approval → classification/retention → threat model → read-only service identity → least privilege → tool allowlist → validation/provenance → independent signoff → monitored bounded pilot → production acceptance and rollback ownership.
