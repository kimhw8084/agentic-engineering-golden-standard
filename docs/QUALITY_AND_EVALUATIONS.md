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

`python -m scripts.evaluate_fixture --cases examples/fixtures/domain_cases.json --repeats 20`
runs a 30-case public domain seed over the same six synthetic records: metrology IDs,
parameter/validator joins, unknowns, work commitments and adversarial ACL/content queries.
These cases illustrate slices, not representative enterprise scale or expert-labeled answers.
Revision conflicts, stale data, dynamic code paths, source outages and realistic long-context
stress still need new corpus/adapter coverage. Repeats measure deterministic timing only;
they do not increase the count of independent tasks or measure model variance.

## Metric definitions and provenance

The runner reports recall@k (all expected IDs), precision@k and MRR on answerable cases;
abstention accuracy uses empty-label cases separately. `hit_at_k` is retained for the v1 CLI
threshold and means hit-or-correct-abstention rate; it is not standard retrieval recall.
v1 MRR mixed abstentions into the denominator; v2 corrects that contract. Report denominators.
Unauthorized cases count queries returning any role-invisible ID; simulated roles do not
establish enterprise ACL security. p50 uses median, p95 nearest rank; query latency excludes
index construction. Timing is process-local; disclose warm/cold conditions and sample count.

Every result includes fixture and implementation SHA-256, standard/Python versions, k,
repeats, per-case ranks and per-slice passes. Record commit, dirty status, platform, command,
run timestamp and artifact hash with the report (see `docs/V2_VERIFICATION.md`). No model
is invoked: model/tool calls and billed model cost are zero; local compute cost unknown.
Answer correctness, citation grounding and employee task success are **null/unmeasured**.
For a real trial include prompt/skill/tool/policy hashes, model/parameters/seed (if supported),
endpoint class, failures, token usage and explicit price basis/date; do not infer cost from
tokens alone or record confidential prompts in public artifacts.

## Protected holdout and repeated-model protocol

1. A separately accountable curator generates fresh cases after the development corpus is
   frozen. Keep labels/cases outside this public repo and author/agent context, under approved
   access. Record custodian, split/version, manifest hash, freeze date and contamination audit.
2. Tune on development only; lock model/prompt/tools/skills before one holdout evaluation.
   Return aggregate slices and reviewed failures. Any failure revealed to authors becomes
   development data; replace with fresh cases for the next independent assessment.
3. Predeclare paired baseline/candidate trials, e.g. 5 model trials per case with fixed settings
   and randomized order. Record all errors/timeouts/cancels. Report per-case success frequency,
   dispersion and paired differences; bootstrap by case, not by treating repeats as new cases.
4. Protect high-severity ACL/unsafe-action gates regardless of aggregate score. Require domain
   review for unsupported diagnosis/impact claims. Public fixture passes remain L1.

This repository contains **no protected holdout or executed model trials**. Publishing a
file named holdout would not satisfy separation. Synthetic examples need expert calibration
before they can support a domain-accuracy claim.

## Calibrated grading

Before AI judging, two authorized humans independently grade a stratified calibration set
blind to candidate/version. Use 0=wrong/unsafe, 1=partly correct with material omissions,
2=correct with minor omissions, 3=fully correct/grounded; separately flag critical safety.
Score each answer claim against evidence revision; citation existence is not grounding.
Adjudicate disagreements and freeze anchors/rubric. Compare a pinned AI judge to adjudicated
labels using confusion matrix, agreement, critical false-pass rate and confidence intervals.
Set acceptable bounds before testing; judge outputs never approve operational artifacts.
Repeat calibration after judge/rubric/domain changes. No calibration has been executed here.

## Failure taxonomy

| Category | Example / required disposition |
|---|---|
| input_contract | Missing fields or version; reject before model |
| identity_scope | Forged identity/ACL leak; deny and block rollout |
| retrieval_miss | Relevant record absent/ranked low; diagnose indexing/query |
| stale_revision | Wrong source version; abstain or explicit historical answer |
| unsupported_claim | Evidence does not support claim; fail answer grader |
| citation_mismatch | Wrong locator/revision/claim binding; fail grounding |
| tool_trust | Drift, poisoning or unauthorized tool; deny/quarantine |
| validation_approval | Invalid domain value/hash/expiry; block handoff |
| budget_timeout | Deadline/call/cost exceeded; bounded partial/abstain |
| recovery_cancel | Replay conflict, late result, cancel race; reconcile deterministically |
| data_exposure | Payload/classification/telemetry leakage; incident handling |
| product_failure | Employee cannot complete/recover; fail workflow acceptance |

Record primary category, contributing causes, case/run/span/commit, expected/observed
behavior, severity, detection, owner and retest. `python -m scripts.trace_demo` emits offline
policy-decision spans with success, poisoning, write denial, classification and cancellation;
these are deliberately labeled partial examples, not production audit records.
