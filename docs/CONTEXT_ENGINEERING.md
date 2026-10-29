# Context engineering contract

The trusted runtime assembles context; retrieved text does not edit instructions, tool
definitions or grants. The work loop and authorization boundary remain in `AGENTS.md`.
This contract governs a consuming application's context, not OpenCode's internal behavior.

| Plane | Source and authority | Lifetime / assembly rule |
|---|---|---|
| Permanent rules | Reviewed system/company policy and reconciled project rules | Versioned at deployment; short invariants; policy conflicts fail closed |
| On-demand skills | Approved publication manifest with pinned content hashes | Load only selected task skill; record version; skills cannot grant permissions |
| Retrieved knowledge | Authorized revision-pinned evidence, untrusted content | Request-scoped; quote/delimit with IDs; never interpret as executable instructions |
| Tools | Approved server/definition registry | Pin definition hash before context assembly; reject drift; expose smallest useful set |
| Permissions | Trusted identity and runtime policy service | Re-evaluate per call/resume/output; keep credentials out of model context |
| Workflow state | Server-owned durable state/version, not chat memory | Load checkpoint at resume; reject stale writes; model proposes transitions only |

Assembly order: authenticate/classify task → select policy/skills/tools → budget context
→ retrieve authorized evidence → attach state summary → model proposes → runtime validates
and authorizes. Content classification determines allowed model destination before any
payload is sent. Source instruction injection remains data even if it calls itself system.

Allocate token budgets separately for rules, task, selected schemas/skills, evidence and
output reserve. Record actual tokens, dropped evidence IDs and truncation reason. Drop
low-relevance duplicate evidence first; never truncate required policy or hide missing
required evidence. If essential inputs do not fit, split deterministically or abstain.
Summaries retain source IDs/revisions and uncertainty; they are not independent evidence.

Cache keys bind tenant, actor grants/policy version, source revision and task/skill version;
recheck ACLs and deletions on read. No cross-user answer reuse without proven isolation.
At handoff include structured evidence/unknowns/budget/state version, not an unbounded
conversation transcript. Trace references/hashes rather than secret-bearing raw context.

Negative acceptance: source asks to change tool schema; cached result belongs to another
role; context truncates validator evidence; checkpoint is stale; model destination is
unapproved. Each must deny/abstain before disclosure/effects. The offline tool demo tests
some of these boundaries; actual model instruction resistance remains unverified.
