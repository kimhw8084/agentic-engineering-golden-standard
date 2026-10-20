# Lecture 06 — Software testing, scientific experiments and agent evaluation

## Goals vs evidence
"It answers my questions" is an anecdote. "On a frozen set of 50 domain-expert-labeled cases, verified citation precision improved from A to B at fixed ACL requirements" is evidence (provided both numbers actually come from executed tests).

## Multiple oracles
Deterministic checks are appropriate for types, schemas, state transitions, ACL scope, file diffs and exact expected citations. Expert human graders handle ambiguous domain conclusions. LLM graders can scale evaluation but require calibration against human expert labels; judge agreement is not truth.

Separate **retrieval success** (found the right documents) from **answer success** (accurate claims supported by those documents) and **workflow success** (correct task completed safely). An answer with a citation may still be unsupported, and a schema-valid recipe may still violate an equipment-specific constraint.

## Experimental design
To compare manual vs AI-assisted engineering work, hold problem difficulty and participant skill as constant as feasible. A crossover design can assign some users manual-first and others assisted-first; record order/learning effects. Measure active human minutes, validation/rework, quality defects and maintenance burden. Report medians, distributions and exclusions. If sample sizes are small, present uncertainty rather than arbitrary precision.

## Statistical intuition
If outcomes are Bernoulli successes and observed success rate is p-hat over n independent cases, rough standard error is `sqrt(p*(1-p)/n)`. But repeated cases, correlated tasks, and nonrandom datasets violate independence. With 5 successes out of 5, you still have very weak evidence of near-perfect real-world reliability. For high-severity security gates, supplement statistical sampling with exhaustive invariant checks and adversarial analysis.

## Performance
p50 and p95 only mean something given representative traffic and a documented percentile method. Report model/tool calls, error rate, memory and compute alongside latency. Don't optimize to a benchmark that the model has already seen via repeated prompt tuning.

## Independent lab
Create five groups of synthetic cases: valid, invalid, stale evidence, unauthorized evidence and malicious instructions. Write Python unittest or pytest assertions for each. Introduce one bug intentionally, verify tests fail, fix it and rerun. Then design a randomized/manual-assisted measurement sheet with rework included.

## Defense questions
What is ground truth for a root-cause diagnosis? Can an LLM grade its own answers? Why is 100% of 10 toy cases not 100% accuracy? What happens if you change the held-out set based on failures? How would you quantify engineer-hour savings credibly?

**Mastery gate:** reproducible tests, falsification, metric interpretation and honest limitation reporting.
