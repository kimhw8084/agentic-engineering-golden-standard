---
name: project-audit
description: Audit an existing repository without rewriting it; inventory observed architecture, tests, risks, permissions and working features.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Project Audit

## Objective
Produce an evidence-based brownfield architecture and opportunity assessment **before** code changes.

## Method
1. Verify authorized project and clean/durable Git state. Inspect allowed config, entrypoints, services, test commands, and current OpenCode rules. Do not read unrelated private corpora or secrets.
2. Create a source-backed inventory: `working / partially working / broken / unverified / duplicates / missing`. Cite file path and line/commit where permitted.
3. Diagram dependencies, data boundaries, service identities, error flows, production-change gates and prior evaluations.
4. Run safe existing tests, recording exact command and result; never invent a passing result.
5. Identify first high-frequency workflow, available baseline, safety constraints, smallest verified improvement.
6. Produce `CURRENT_STATE`, concise diagram, ranked risks and one next task with measurable acceptance criteria. Do not rewrite without separate authorized implementation task.

### Stop conditions
Missing repo permission, test may hit production, uncertain command side effects, restricted corpus. Mark blockers.
