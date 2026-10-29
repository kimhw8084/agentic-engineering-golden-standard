# Choosing a workflow pattern

Start with deterministic lookup/retrieval; add model autonomy only for a demonstrated
gap. Measure paired correctness/task success, p50/p95, model/tool calls and cost on the
same frozen cases. Selection is per workflow, not a repository-wide mandate.
Numbers below are initial **example limits**, to be ratified against task SLOs; outer
deadline/cost/cancellation in TaskRequest always wins. No pattern grants permissions.

| Pattern | Select when | Tradeoff | Failure behavior and example stop | Anti-pattern |
|---|---|---|---|---|
| Simple retrieval | Exact known IDs or evidence lookup satisfies user | Lowest cost/variance; lexical misses paraphrases | One search, at most 3 refs; abstain on missing/stale evidence | Calling retrieval a reasoning agent or treating hits as proof |
| Single agent | One bounded goal needs dynamic choice among a few approved reads | Flexible but stochastic and sequential | Max 4 model steps, 3 tools, 15s; stop on denial/no progress | Universal assistant with every tool enabled |
| Sequential chaining | Fixed stages such as retrieve → summarize → validate | Easy attribution; serial latency and error propagation | Max 3 stages, each typed gate; stop at first invalid output | Repeating the same prompt hoping errors disappear |
| Routing | Stable task classes require different tools/policies | Less context/cost; misrouting can hide evidence | One classification plus one route; unknown class abstains; validate scope after route | Letting model-selected route authorize access |
| Parallel fan-out/fan-in | Independent read tasks or rubric dimensions | Lower critical-path latency; greater call/cost and correlated errors | Max 3 branches, one join deadline; cancel siblings on critical failure; mark partials | Parallel mutations or majority vote called factual truth |
| Orchestrator-workers | Work cannot be decomposed until evidence arrives | Adaptive breadth; expensive coordination and inconsistent context | Max 3 workers/1 delegation level/6 total calls; orchestrator validates evidence at join | Recursive swarms without measured benefit or global budget |
| Evaluator-optimizer | Explicit rubric and repairable output with trusted feedback | Quality may improve; judge bias/overfit and multiplied latency | Max 2 repairs, stop on repeated error or no rubric gain; human handles ambiguity | Model self-approval for consequential decisions |
| Durable workflow | Work spans crashes, scheduled jobs or human waits | Recovery/operability; storage, version migrations and reconciliation cost | Persist state before acknowledgment; max 3 read retries; deadline/cancel across resumes | In-memory loop marketed as durable/exactly once |

Use chaining for known steps and an agent for unknown next steps. Routing and parallelism
can be deterministic. Durable orchestration is an execution property and may wrap any
pattern; it need not add another model. Never trade away source ACLs for speed.

Record chosen pattern, simpler alternative, expected benefit, budget and failure model
in the charter/ADR. Promote complexity only when a controlled comparison exceeds an
agreed quality/latency/cost threshold, including coordinator overhead. On regression,
revert to the simpler route and retain failure traces. Current toy code is simple
retrieval plus a fixed in-memory state machine; the other patterns are guidance only.
