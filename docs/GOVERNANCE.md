# Canonical rules and ownership

`AGENTS.md` governs the engineering work loop and authorization boundary. Skills and
commands apply that policy; they do not create permissions. Resolve conflicts by stopping
the affected action and reconciling with the owner; do not invent a second rule elsewhere.
Examples, labs and templates are explanatory, not additional normative sources.

| Canonical home | Owns | Accountable owner |
|---|---|---|
| `AGENTS.md` | Work loop, scope, response contract | Repository maintainer |
| `docs/DEFINITION_OF_DONE.md` | Release acceptance and evidence status | Delivery owner |
| `docs/ARCHITECTURE.md` | Boundaries and implemented capability inventory | Architecture owner |
| `docs/RUNTIME_CONTRACTS.md` | Target message fields, workflow states, retry/cancel semantics | Runtime owner |
| `docs/AGENT_PATTERNS.md` | Pattern choice and stopping limits | Architecture owner |
| `docs/CONTEXT_ENGINEERING.md` | Context authority, lifetime and assembly | Architecture/security owners |
| `docs/TOOL_TRUST.md` | Tool approval and model data exposure | Security/source owners |
| `docs/SECURITY_THREAT_MODEL.md`, `SECURITY.md` | Threat/control matrix; disclosure policy | Security owner |
| `docs/QUALITY_AND_EVALUATIONS.md` | Datasets, metrics, grading, failure taxonomy | Evaluation owner |
| `docs/PRODUCT_DELIVERY.md` | Employee acceptance and adoption stages | Product/sponsor |
| `docs/SKILL_PUBLICATION.md` | Skill packaging, rollout and rollback | Standard maintainer |
| `docs/IMPACT_AND_EXECUTIVE_RECOGNITION.md` | Business measurement method | Sponsor/delivery owner |
| `academy/README.md` | Mastery scoring, role-family readiness and assessment cadence; lectures/templates instantiate it | Human learning owner |
| `academy/V2_INTEGRITY_EXERCISE.md` | Release-specific lab instantiating the mastery rubric | Human learning owner |
| `docs/GLOSSARY.md` | Shared terminology | Standard maintainer |
| `docs/adr/` | Numbered architectural decisions | Decision author + independent reviewer |
| `CHANGELOG.md`, `docs/MIGRATION_V2.md` | Release history and migration | Release owner |
| `OFFLINE_START.md` | One-way Windows transfer, prerequisites and snapshot verification | Standard maintainer |
| `academy/assessment/README.md` | First synthetic assessment contract; canonical mastery rubric remains in academy README | Human learning owner |

The visual field guide in `docs/field-guide/` is explanatory and generated from `content.json`.
Its page-level sources point to canonical rules. It grants no permissions or new maturity.
The technical handbook in `docs/handbook/` is an explanatory teaching companion owned by
the human learning owner and maintainer. Its JSON source generates PDF, HTML and Markdown;
dated primary references support mechanisms/comparisons, not enterprise certification.

This is the documentation ownership map. Remaining `docs/` playbooks, blueprint, roadmap,
performance, brownfield and references pages are navigation/application guidance; their
owner is the maintainer, delegating to the specialist role above. `templates/` instantiate
canonical rules; `.opencode/` helpers link to them. `docs/V1_GAP_MATRIX.md` and
`docs/V2_VERIFICATION.md` are historical evidence owned by the change author. New
normative pages require a row here. Role names must be assigned to actual people before
a company pilot; the sole current repository owner is not an independent second approver.

`CODEOWNERS` routes review to the known repository owner; it does not enforce branch
protection, security expertise or reviewer independence. Configure required reviews/checks
on GitHub separately. An AI reviewer using the author's context is an assisted check.
Independent review requires a separately accountable reviewer who reproduces critical
checks against the exact commit; record identity, scope, findings and resolution in the PR.

Versioning uses SemVer: incompatible executable/reference-contract changes increment
major; compatible capabilities minor; fixes patch. `pyproject.toml` is the version source;
`golden.__version__` must match (verified). No tag/release until required human review.
ADRs use sequential `NNNN-title.md`, status Proposed until reviewed, supersession links
instead of rewriting history. The glossary defines maturity independently of version.
