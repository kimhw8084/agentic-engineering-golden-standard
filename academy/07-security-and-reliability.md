# Lecture 07 — Authentication, authorization, threat modeling and SRE

## Security begins at the trust boundary
Authentication proves who made the request (e.g., enterprise SSO). Authorization determines whether that identity can read a specific source record or perform a specific action. A model is not a trusted identity provider. Never accept "I am a manager" from a prompt or a caller-controlled role field as proof.

## Retrieval-specific threats
A user might query a restricted employee thread indirectly via summaries, autocomplete, search facets, citations or cache. The access check must apply to metadata and content before retrieval output and be revisited when source ACLs change. Shared vector indexes can work, but permission enforcement must not rely on prompt wording or convenience filters alone.

A malicious SOP/email/repo comment can contain instructions to leak secrets or call a tool. This is **indirect prompt injection**. The defense is architectural isolation: source text is data; tool schemas and authorized scope are not sourced from that data. Audit expected tool calls, gate permissions in code, and test malicious payloads as fixtures.

## Production boundary
An internal OpenCode session with broad source-code access must not inherit equipment/MES write credentials by default. Isolate production action executor in a separate identity and approval path; require exact artifact hash, target scope, independent reviewer, time window and change record. Add kill switches, dry-run, monitoring and rollback.

## SRE concepts
Define SLI (observed behavior), SLO (objective), and error budget (allowed miss rate over a defined interval). Example: "99.5% of authorized read-only queries return a properly sourced answer or explicit safe abstention within 10 seconds" is only useful if instrumented and approved. A model refusing to hallucinate can count as successful safe behavior, depending on the task definition.

## Independent lab
Threat-model the toy retrieval CLI: show why passing `roles=['manager']` directly is forgeable. Build a toy signed session or interface that rejects tampered identities (not a substitute for enterprise SSO). Add unauthorized document, citation metadata leakage and prompt-injection fixtures. Create an incident runbook for model outage, expired index and leaked token.

## Defense questions
Where does trusted identity come from? Can cached citations leak content? How does approval bind exact draft bytes? What must happen after a security incident? Why are "prompt says don't" controls insufficient?

**Mastery gate:** verified red-team negatives, threat boundaries and concrete reliability tradeoffs.
