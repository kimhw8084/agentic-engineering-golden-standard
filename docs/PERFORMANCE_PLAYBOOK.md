# Performance engineering playbook

**Optimize end-to-end verified outcomes, not raw tokens/second.**

Measure pipeline segments: identity→retrieval→rerank→LLM/tool calls→validation→UI. Start with three baselines: correctness on a frozen gold set; p50/p95 end-to-end on a representative request mix; per-run token and tool-call counts. Log data and model revisions.

Improvement order:
1. Correct false claims/authorization failures first.
2. Remove redundant tool calls and duplicated retrieved chunks.
3. Route exact IDs to deterministic queries instead of LLM planning.
4. Cache only authorization-invariant computation; permission-filter results per user and request.
5. Deduplicate embeddings by source content hash and revision; reindex changes only.
6. Introduce reranking, async fetching or parallel calls only after measuring tradeoffs.
7. Apply bounded timeouts, deadlines and capped retries (with jitter where appropriate).
8. Regression-test accuracy after every optimization.

For 200 potential users, estimate actual peak request arrival rates, not 200 simultaneous sessions by assumption. Load test synthetic data and approved isolated services only. Set SLOs only after baseline and stakeholder review.
