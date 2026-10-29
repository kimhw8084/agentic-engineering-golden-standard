---
name: agent-workflow
description: Design minimal bounded tool-using agent workflows with typed states, retries and safe delegation.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Agent Workflow

## Procedure
Use `docs/AGENT_PATTERNS.md` for pattern selection, `docs/CONTEXT_ENGINEERING.md` for context assembly, and `docs/RUNTIME_CONTRACTS.md` for target lifecycle and cancellation. Tool approval lives in `docs/TOOL_TRUST.md`.

Define one objective and a machine-verifiable success criterion. Prefer deterministic preprocessing/router and one model coordinator; use specialized agents only if offline evals show benefit. Create allowed typed tools, budget of tool/model steps, deadlines, stale source checks, escalation, error/partial-outcome handling, isolated production action interface and audit events. Separate natural-language text from permissions. Test infinite loops, prompt injection, tool unavailability and deterministic refusal. Trace every consequential claim to source evidence.
