# Agentic Engineering Golden Standard

**A GitHub-template-ready engineering operating system for OpenCode + an approved internal LLM.**

> **Status: v2.0 proposed teaching/reference template (L1).** Includes runnable baseline code and regression tests, not an enterprise-deployed agent. Uses synthetic inputs only. It does **not** implement company identity, production approvals, live APIs, a real embedding service, scheduling, or equipment actions. Human review and release tagging remain pending.

## Purpose

Every project should yield **(1) measured business value, (2) demonstrated software quality, and (3) independent engineering mastery**. Use this same standard for communication intelligence, manufacturing source-code intelligence, troubleshooting, artifact drafting, reporting and optimization. Do not merge those independent applications into one unsafe super-agent.

This repository improves the reusable workflow and the learner's transferable capability.
Its [roadmap](docs/ROADMAP.md) is separate from application playbooks. Select valuable work
with the [ROI decision protocol](docs/IMPACT_AND_EXECUTIVE_RECOGNITION.md), including limited
IT/support capacity, and maintain [current interview evidence](academy/README.md) as you work.

## In 10 minutes

For a one-way transfer to a Windows work PC, start with [OFFLINE_START.md](OFFLINE_START.md)
and the [visual field guide](docs/field-guide/field-guide.pdf). The guide is a generated
explanation of canonical rules; preflight is offline and needs approved Python 3.11+.

Requirements: **Python 3.11+**, Git. No external Python dependencies for the reference tests. OpenCode is optional for local exercises, required only for AI-assisted command/skill workflows.

```bash
python scripts/verify_standard.py
python -m unittest discover -s tests -v
python -m scripts.evaluate_fixture
python -m scripts.change_demo
python -m scripts.trace_demo
python -m scripts.skill_manifest
python scripts/offline_preflight.py
```

Then open this repository in OpenCode and use `/golden-audit`. No model or provider is configured by the template; your approved internal settings are preserved.

## Retrofit an existing project without replacing its code

```bash
python scripts/repo_audit.py /path/to/existing-project
python scripts/retrofit.py /path/to/existing-project            # dry run only
python scripts/retrofit.py /path/to/existing-project --apply    # copies only missing helpers and guidance
```

The installer **does not overwrite** existing paths, `AGENTS.md` or `opencode.json`; it includes missing support docs, templates and academy materials that the skills reference. For colliding documentation names, compare and reconcile manually. Manually compare `templates/AGENTS_BROWNFIELD.md` with your existing rules, and selectively add the project-specific instructions. Run the complete audit in your approved environment; the metadata-only `repo_audit.py` cannot assess code correctness.

## What's inside

| Location | Purpose |
|---|---|
| `AGENTS.md` | Concise governing workflow and safeguards |
| `.opencode/skills/` | On-demand repeatable engineering skills |
| `.opencode/commands/` | Natural-language slash-command workflows |
| `.opencode/agents/` | Read-only specialist subagents; model agnostic |
| `docs/` | Architecture, threat model, measurement, evaluation, adoption, career strategy |
| `templates/` | Charter, RFC, ADR, tests, impact and interview evidence formats |
| `academy/` | Concept-first engineering lectures, runnable labs, mastery rubric |
| `golden/` | Dependency-free toy retrieval and change-state logic |
| `examples/fixtures/` | Entirely synthetic evidence and evaluation cases |
| `tests/` | Negative, auth-filtering, hash-tamper, workflow, onboarding tests |
| `.github/` | PR/issue templates and CI verification |

## Architecture in one picture

```text
Your OpenCode + internal LLM (engineering control plane)
                 │ uses skills, commands, human reviews
                 ▼
       Git / CI / tested release of YOUR APP
                 │
                 ▼
  Application layer (FastAPI / other approved framework)
  ├─ trusted authentication + server-side per-source authorization
  ├─ task router + bounded agent context (reasoning only)
  ├─ typed read-only adapters / time-versioned evidence
  ├─ deterministic workflow, validators, trace and metrics
  └─ draft → review → company-controlled approval/execution
                 │
    NO direct privileged production write path from LLM
```

The included Python modules demonstrate pieces of this but **not** the entire production stack. See `docs/ARCHITECTURE.md`.

## First two brownfield playbooks

- `docs/playbooks/WORK_INTELLIGENCE.md`: permission-aware email/message search, cited answers, briefing, reminder correctness and scheduling.
- `docs/playbooks/MANUFACTURING_SYSTEM_INTELLIGENCE.md`: source/recipe architecture intelligence, code path reconstruction, revision-aware dependencies and change-impact investigation.

Do **not** initially replatform either project. Run `/golden-audit`, capture a baseline, add tests, then work one measurable vertical slice at a time.

## Career accelerator

`academy/` provides eight linked technical modules (algorithms, backend, distributed systems, retrieval, agent architecture, quality, security, staff-level leadership), independent code challenges, evaluation rubrics and interview-defense prompts. "AI wrote code" does not equal "I independently mastered it." A production feature, benchmark and unaided exercise each count separately.

## Release maturity levels

| Level | Evidence |
|---|---|
| L0 | Exploratory prompt, no reproducible results |
| L1 | Deterministic local tests and fixtures pass |
| L2 | Authorized real read-only integration, role checks, measured quality |
| L3 | Observability, negative tests, recovery, accountable operator and limited pilot |
| L4 | Approved production deployment, incident runbook, independent approvals and measured sustained impact |

This repository is **L1 reference scaffolding**, not L4. Do not claim corporate security validation based on fixture tests.

## Publishing to GitHub

1. Create a **private** empty repository in your approved personal/company GitHub organization (depending on intended use). Do not publish company-derived code or configurations externally.
2. From the extracted root, run `git init`, `git add .`, `git commit -m 'Initial golden engineering standard'`, `git branch -M main`, `git remote add origin <approved-url>`, `git push -u origin main`.
3. In GitHub repo settings, enable **Template repository** if available. Protect main, require the CI gate and code review. Keep GitHub Actions enabled only where company policy allows.
4. Choose the appropriate legal/license terms and data-handling policy with the repository owner before public distribution; no open-source license is granted by default.

## Clear boundaries

This is not: a replacement for company approvals; a production-ready employee-email ingestion pipeline; a real MCP integration; a training dataset made from proprietary data; a guaranteed big-tech hiring program; or a pre-validated SEMI-compliant manufacturing tool.

## See also

`docs/ROADMAP.md` • `docs/DEFINITION_OF_DONE.md` • `docs/SECURITY_THREAT_MODEL.md` • `docs/QUALITY_AND_EVALUATIONS.md` • `academy/README.md`.

Sources and OpenCode compatibility links are in `docs/REFERENCES.md`.

For v2 review start with [verified v1 gaps](docs/V1_GAP_MATRIX.md),
[rule ownership](docs/GOVERNANCE.md), [migration](docs/MIGRATION_V2.md),
[changelog](CHANGELOG.md) and [executed verification](docs/V2_VERIFICATION.md).
Pattern/context/tool contracts are indexed by governance. Employee acceptance and
adoption gates live in [product delivery](docs/PRODUCT_DELIVERY.md).
