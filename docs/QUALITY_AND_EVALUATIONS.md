# Evaluation engineering — ground truth over vibes

## Separate evaluation layers

1. **Deterministic contracts:** schemas, input types, authorization, validators, hash-bound review, state transitions; expected 100% on defined pass/fail fixtures.
2. **Retrieval:** document-level recall@k, MRR@k, rank shifts, fresh-source coverage, ACL leakage, query-level p50/p95 (representative workload required).
3. **Answer quality:** claim/citation correctness, hallucination rate, unknown acknowledgment, temporal accuracy, expert-reviewed answer rubric.
4. **Action correctness:** tool argument validity, tool scope, idempotency, recovery, human approval, refusal of disallowed actions.
5. **Business experiment:** randomized or matched crossover manual-vs-assisted, case complexity, rework, reviewer time, defects, time saved, adoption.

## Gold set composition

Start with 30–50 **approved or synthetic** domain questions per narrow workflow. Classify:
- 20% straightforward known-answer questions;
- 20% multi-source joins / conflicting versions;
- 20% ambiguous/incomplete evidence requiring abstention;
- 20% security, injection, access and unauthorized-tool tests;
- 20% latency, failure, staleness and long-context stress cases.

This is a starting distribution, not an industry mandate. Label each case with source snapshots, exact scope, expected source IDs, acceptable answer claims, forbidden claims, and reviewer signoff. Freeze a holdout set. Do not optimize prompts against the same holdout repeatedly.

## Reporting

Keep pass/fail by slice, not just one combined average. Record run ID, commit SHA, data/index revisions, model and parameters, tools, prompt/skill versions and authorization scope. Prefer pairwise repeated runs for stochastic models, with confidence intervals/uncertainty when sample size permits. Distinguish judge-model agreement from domain expert correctness.

## Performance

Measure wall-clock end-to-end and each component. Record number of LLM calls, prompt+completion tokens, retrieval candidates, rerank time, tool failures, and cost proxy. p95 over a handful of samples is unstable; increase sample size and give percentile method. Avoid premature speed optimization that lowers correctness or security.

## Provided toy benchmark

`python -m scripts.evaluate_fixture` runs seven deterministic, synthetic lexical search cases. It is NOT a test of internal LLM skill, embedding endpoint quality, real enterprise ACLs or hardware load. Replace only via approved offline fixtures first; production data must follow security policy.
