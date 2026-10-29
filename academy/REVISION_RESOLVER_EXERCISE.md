# Unaided revision resolver and architecture defense

Status: **unassessed**. All code delivered in this change is AI-assisted; none proves the
learner independently wrote, debugged or operated it. Use the canonical 0–4 rubric in
[README.md](README.md), with an independently accountable human assessor. AI feedback is
formative. A lab alone cannot earn the rubric's production/leadership level 4.

Before reading the assisted implementation, start a separate blank workspace. The assessor
supplies new synthetic modules and a revision manifest after the implementation freezes.
Do not use AI-generated code, hints, existing resolver code or these visible fixtures as
the unseen assessment. Record time, permitted references and every hint. If the solution
was already read, the assessor changes the language/representation and failure constraints.

Timebox 60–90 minutes plus a 20-minute defense. Implement a revision-aware dependency
resolver with exact source/locator binding, iterative traversal, cycles, ambiguous targets,
missing edges, access denial and a bounded stopping condition. Include a cache only if the
assessor's workload requires it: key by immutable content, extractor version and authorization
scope, explain invalidation/revocation, and compare with no cache. Never silently use latest.
Return unknowns instead of fabricating runtime behavior. No external systems or company data.

The assessor privately creates unseen tests spanning joins/cycles, two changed snapshots,
missing source, shadowed symbol, runtime dispatch, altered bytes, new access scope, canceled
work and a large graph. Cases and labels stay outside the learner/public tuning material.
Require the learner to predict outcomes before execution. The examiner then introduces one
defect privately (for example an incorrect revision/cache key or premature visited marking).
The learner diagnoses it from a failing test and repairs it without hints. Do not publish
that variant until assessment is complete; revealed cases become development material.

Defense questions:

1. What does a static edge prove? Where do aliasing, branches, imported calls and dispatch break the inference?
2. Derive time/space complexity including source parsing, traversal, sorting and cache operations.
3. Why choose code search, this resolver or a bounded agent? What measurement changes the choice?
4. A canceled read returns after a stop/recovery epoch. Which result may be published, and why?
5. What do hashes fail to authenticate? Which authority owns the manifest, user grants and recovery?
6. How would you prove useful dependency recall without training on your evaluation labels?
7. What must change for 200 personnel, and which scaling feature would you defer until measurement?

Use [MASTERY_RECORD](../templates/MASTERY_RECORD.md) to record exact artifact hashes,
commands/results, failed unseen cases, reasoning, debugging behavior, assessor identity,
date, hints and authorized scope. For level 3, the human must observe unaided correct
implementation, unseen negative cases, defect repair and a coherent alternatives defense.
Record the actual canonical score and gaps; do not infer it from test count.

Retest at assessment date +2, +7 and +30 days: reconstruct traversal/invariants; debug a new
revision/cancellation variant; then implement a transfer case and defend design without AI.
These are due intervals, not completed assessments. If first assessed 2026-10-29, the dates
would be 2026-10-31, 2026-11-05 and 2026-11-28. Schedule from the actual assessment date.

## Interview-defense evidence record for this change

| Item | Defensible current statement |
|---|---|
| Decision | Deterministic AST traversal chosen for a bounded synthetic corpus; no model/vector database needed yet |
| Tradeoff | Better development locator coverage than literal search, with extra parsing/traversal; no measured human savings |
| Failure | Dynamic dispatch/missing external normalization remain unknown; interrupted reads require reconciliation |
| Concurrency | Durable admission and result fencing; separate-process stop, crash and cancel/publish race tests |
| Personal implementation | None independently observed in this session; delivered implementation is AI-assisted |
| Can demonstrate unaided | Unknown until the above human assessment is completed |
| Operational ownership/value | No real release, user adoption or company savings established |
| External reuse | Only public synthetic code/results; company-specific evidence requires explicit policy/source-owner approval |

An interview story may describe what was designed and tested with AI assistance. It must
not say the learner independently implemented it, shipped to 200 people, saved hours or
improved manufacturing yield without corresponding observed and approved evidence.
