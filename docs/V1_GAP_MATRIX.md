# Verified v1 gap matrix

Baseline: `a655268d6f4356f88dbcab0e6b278bf6a5d3f4af` (local and remote main matched).
Audit date: 2026-10-28. Clean working tree; 80 tracked/template files in metadata
inventory; Python >=3.11, no runtime dependencies, 11 skills, 7 commands, 3 optional
review/examiner agents. `opencode.json` contains permission settings and no model/provider.
Only this repository and synthetic fixtures were inspected. No company sources accessed.

| Priority / concern | Observed v1 evidence at baseline | Classification / v2 disposition |
|---|---|---|
| P0 reviewer independence | `golden/change.py:review` trusts caller boolean; `academy/02-backend-and-databases.md` already explains this; reviewer/auditor prompts say independent | Partial guidance, no identity enforcement. Label simulated review; role separation is no independent verification. Keep real identity/signoff outside demo. |
| P0 hash/state integrity | `set_draft` transitions before serialization; `validate` and `review` compare stored hashes without recomputing content; export alone rehashes | Executable defects. Make failed serialization atomic; reject content changes at each gate; regression tests. |
| P0 workflow states | `docs/ARCHITECTURE.md` calls blocked/rejected/expired/quarantined invalid; code has created/evidence_ready/drafted/validated/reviewed/exported | Terminology defect. Distinguish valid failure outcomes, demo states and target lifecycle. |
| P0 idempotency | `academy/03-distributed-systems.md` explains dedupe; architecture proposes keys; demo export is one-shot with no store | Existing guidance, missing runtime. Explicitly say retries fail, restart loses state; no exactly-once promise. |
| P0 audit integrity | `ChangeRun.events` is an editable list; threat model already says audit integrity absent | Existing caveat needs canonical home; no signed/append-only audit claim. |
| P0 retrieval algorithm | `academy/04-retrieval-science.md` correctly says not BM25; `EvidenceIndex.search` tokenizes every visible record per query, boosts substring IDs | Existing honest algorithm description; exact-ID substring is a defect. Token equality fix and adversarial regression. No inverted index/semantic/revision-routing claim. |
| P0 installer safety | `retrofit.py` skips existing paths but follows destination directory symlinks and dangling file symlinks | Executable no-overwrite boundary defect. Refuse symlink paths; test repeated apply and config preservation. No concurrent installer guarantee. |
| P0 governance | `templates/ADR.md` exists; versions in two Python metadata files; no changelog, numbered ADR, CODEOWNERS, glossary or rule ownership index | Missing governance. Add canonical map, glossary, ADRs, version consistency gate, changelog/migration. |
| P1 patterns/context | `academy/05-agents-and-context.md`, `agent-workflow` skill favor bounded single coordinator | Guidance exists; selection table for eight patterns and explicit context lifetime contract missing. Extend by reference. |
| P1 tool trust | Threat model and `INTEGRATION_PATTERNS.md` already require scoped tools, auth and injection tests; no MCP enabled | Missing approved-server/pinned-definition lifecycle and executable poisoning boundary example. Add deny-by-default synthetic gate; do not configure external tools. |
| P1 reference contracts | Architecture lists seven target types, no field-level lifecycle/cancellation semantics | Partial. Centralize versioned target contracts, cross-field invariants, cancellation and trace examples. Enterprise adapters remain absent. |
| P1 evaluation | Seven public retrieval cases; 24 unit tests; evaluation guidance already separates layers and calls for holdouts/repeated trials | Preserve regression. Add domain/adversarial fixtures, standard recall/MRR vs abstention metrics, p95 and provenance. Protected holdouts and model/human trials require a separate curator/approved endpoint. |
| P2 employee product | Playbooks describe vertical slices; no complete UI acceptance gate | Add minimum lovable employee journey and failure/recovery criteria. No employee application exists here. |
| P2 skill rollout | No-overwrite retrofit exists; skills have no publication manifest or release policy | Add content-hashed publication and canary/rollback instructions. Preserve skills/config and manual collision reconciliation. |
| P2 business/mastery | Academy, impact guide, mastery and experiment templates already substantial | Extend with spaced recall, evidence approval and staged sponsor/pilot/rollout gates; do not duplicate lectures. |

Baseline executed commands (all exit 0): structure verification (0 issues), unittest
discovery (24 tests, 0.017s), fixture evaluation (7/7, hit@3=1, MRR=1,
0 leaked cases; p50=0.0215ms, max=0.061ms). These timings are one tiny local sample,
not an SLO or speed comparison. Metadata inventory is not a code/security audit.

## Specification and bounded delivery

User: standard maintainer and engineers adopting Manufacturing System Intelligence.
Hypothesis: explicit tested boundaries reduce false readiness claims and integration rework;
operational minutes saved are unknown until a pilot. Authorization: synthetic local code,
tests, docs, branch and reviewable PR; no merge/deploy/company access.

Acceptance: preserve existing tests/config; fix reproduced P0 contracts; one source per
rule/type/state; dependency-free runnable negative examples and provenance; clearly label
target-only requirements; publish reviewable commits and exact results. Three increments:
P0 integrity, P1 contracts/evaluation, P2 delivery/release. Review may split these commits
into separate PRs. Non-goals: production identity, approval service, durable engine, live
LLM/MCP integration, employee UI or production readiness. Independent reviewer signoff
and human mastery are pending, not demonstrated by generated changes.

## Remaining external acceptance gates

Protected fresh holdout, domain expert labels, repeated approved-model trials, calibrated
human/AI grading, production auth/ACL/audit/persistence, no-terminal product, real pilot
benefit, independent review and unaided human exercise all remain unverified. Their
protocols are deliverables; they are not implemented enterprise capabilities.
