# Golden Definition of Done

Each ticket must answer these questions and show exact evidence:

1. **Problem:** Who is affected? What measured baseline, if any, motivated work? Record unknown baseline honestly.
2. **Scope:** Existing behavior inspected? Identity/authorization and non-goals explicit?
3. **Design:** Smallest viable solution; alternate considered; error/rollback path; versioning and trust boundary.
4. **Implementation:** Small reviewable diff; no unauthorized production access; no surprise dependencies; backward compatibility assessed.
5. **Functional verification:** Unit/integration tests run and artifacts/results recorded. Nonexecuted checks are explicitly labeled unverified.
6. **Negative/security verification:** Missing/stale/malicious inputs, tenant/role access, retries, concurrency, invalid state, tampering and untrusted instruction handling (as relevant).
7. **Performance:** p50, p95 (with representative samples), request/tool count, baseline comparison, qualitative overhead where data insufficient.
8. **Observability:** Error reasons, auditable run/fixture/version IDs, logs without sensitive content, diagnostic runbook.
9. **Release:** Change owner, reviewers, environment approvals, rollout/rollback and monitoring plan. Sandbox passing does NOT authorize prod.
10. **Mastery:** Developer explains critical concepts unaided; independently completes an implementation/debugging exercise; logs gap and remediation.
11. **Business:** Before/after labor or quality measurements, method and uncertainty; never multiply fictional savings by employee headcount.
12. **Next step:** One prioritized small change with exit criterion.

For significant features attach a business hypothesis/measurement card and an independent
coding/debugging exercise plus architecture defense. Use the academy's canonical rubric;
schedule recall at days 2/7/30 and record actual results. Sanitized career evidence requires
explicit source-owner/confidentiality approval before external use. AI-assisted delivery
does not demonstrate human mastery. Employee products also satisfy the no-terminal journey
and staged gates in `docs/PRODUCT_DELIVERY.md`; skill changes follow `docs/SKILL_PUBLICATION.md`.

Status: `NOT STARTED`, `IN PROGRESS`, `BLOCKED`, `VERIFIED IN FIXTURES`, `VERIFIED IN STAGING`, `VERIFIED IN PRODUCTION`. Avoid ambiguous 'done'.
