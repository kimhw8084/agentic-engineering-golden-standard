# Lecture 04 — Information retrieval beyond "just add RAG"

## Why two retrieval modalities matter
A query for `JOB-1042` or `RECIPE-A7` usually requires exact ID search and revision filtering; an engineer asking "which configuration field controls sampled wafer count?" benefits from semantic search. A reliable system routes or fuses these types deliberately.

## Lexical ranking
BM25 models term frequency saturation and document-length normalization:

`BM25(q,d) = Σ_t IDF(t) * f(t,d)*(k1+1) / [ f(t,d)+k1*(1-b+b*|d|/avgdl) ]`

with typical tunable k1 and b. Very common words have little identifying power; rare field names often matter. BM25 is not semantic: paraphrased questions may miss terms. The toy `golden/retrieval.py` is a simple deterministic term-scoring baseline, **not** a BM25 implementation.

## Embeddings and ANN
An embedding encoder maps text to a numerical vector; cosine similarity compares direction, but top cosine score is not calibrated probability of factual correctness. HNSW approximates nearest neighbors through layered proximity graphs; tune search breadth for recall/latency/memory, benchmark exact search on sampled ground truth. BGE-M3-like models can support multi-lingual retrieval, but do not assume your internal endpoint's embedding settings or dimensions—measure them under approved access.

## Combining systems
Hybrid retrieval can use Reciprocal Rank Fusion `RRF(d) = Σ_i 1/(k + rank_i(d))` to combine lexical and semantic lists when their raw scores are not comparable. A reranker uses query/document pairs to refine a small candidate set but increases latency/cost. Evaluate whether reranking actually improves domain-specific queries.

## Scoring
- Recall@k: proportion of relevant documents found in top k (if multiple relevant docs, count them all).
- MRR: mean reciprocal rank of the first relevant hit. A first hit at rank 2 contributes 1/2.
- nDCG: discounted gain accounts for relevance grades and position, normalized by ideal DCG.
- Citation faithfulness: a sourced document must actually support the generated claim; high retrieval recall alone does not guarantee this.

## Independent lab
Extend the toy retriever to build an inverted index with token→document ID postings. Add explicit ID routing and revision/timestamp constraints. Make a 30-case frozen fixture containing questions with paraphrases, stale recipes, access exclusions and zero-evidence cases. Measure Recall@3, MRR@3, latencies; explain all misses. Optionally implement RRF over synthetic lexical/vector rankings without connecting real confidential content.

## Defense questions
When does a vector index lose to exact lookup? How do you update embeddings when a recipe is revised? What is the source of false citations? Why is nearest-neighbor similarity not factual confidence? How do you benchmark ANN recall fairly?

**Mastery gate:** independent evaluator, version-aware retrieval and demonstrated benchmark tradeoffs.
