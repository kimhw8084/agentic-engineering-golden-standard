# Glossary

| Term | Meaning |
|---|---|
| Standard version | Version of template/contracts; v2 does not mean production maturity. |
| Fixture verified / L1 | Deterministic checks passed on named synthetic inputs. |
| Independent review | Separately accountable reviewer checks exact revision and evidence; a role prompt or caller boolean cannot establish it. |
| Simulated review | Local caller-attested event in `ChangeRun`; not authenticated approval. |
| Idempotency | Same scoped key and request hash returns the same logical outcome; conflicting payload rejected. Requires durable atomic enforcement for restart/concurrency. |
| Audit integrity | Detectable/controlled alteration with trusted access, retention and external anchoring; a mutable list or locally rewritable hash chain is insufficient. |
| Workflow state | Persisted runtime truth in a production implementation; demo state is in memory. Distinct from ticket/evidence status. |
| Lexical baseline | Full visible-corpus scan with capped term frequencies and ID boost; no BM25, embeddings, inverted index or freshness filter. |
| Grounding | Evidence supports the specific claim at the cited revision; a matching citation ID alone is insufficient. |
| Protected holdout | Fresh evaluator-controlled cases/labels excluded from author/model tuning context; public fixtures cannot be protected. |
| Task success | Predeclared end-to-end user outcome, including safety and quality; retrieval hit alone is not task success. |
| Minimum lovable workflow | Employee can finish a useful task and recover from failures through an accessible interface with understandable evidence. |
