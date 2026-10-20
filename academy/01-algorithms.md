# Lecture 01 — Algorithms, complexity and engineering knowledge graphs

## Why this matters in your metrology project
Your architecture intelligence agent may need to answer: "Which source functions, validators and recipe parameters are affected by this change?" This is a graph reachability problem, not simply an LLM context-window problem. Your communication assistant also needs fast exact identifiers and selective search rather than scanning every message.

## Fundamentals
A set/map gives average O(1) lookup but does not guarantee adversarial worst-case O(1). A sorted array allows O(log n) lookup via binary search but costly updates O(n); a B-tree index supports large-scale disk-oriented read and write patterns. A directed graph G=(V,E) can represent module-to-module or recipe-to-validator dependencies. Breadth-first and depth-first search cost O(|V|+|E|) for adjacency-list representation; scanning an adjacency matrix is O(V²). Cycles are normal in software dependency graphs; use a visited set or the search can loop forever.

A topological sort exists only for a DAG. Code dependency graphs may have strongly connected components, requiring condensation into a DAG before layer ordering. The provenance of each edge matters: `static import` is observed; `dynamic runtime call` may be unknown until trace evidence arrives. Do not collapse those certainty levels.

**Example:** `recipe-A → ConfigLoader → Validator → Dispatcher → MESAdapter`. If Validator changes, traverse reverse dependency edges to identify consumers potentially affected. A reachable node is a *candidate* for impact, not proof of actual runtime execution (feature flags, plugin loads, exceptions).

## Complexity and performance
Suppose 100,000 documents, average 400 tokens. Naively searching all terms and documents approaches O(N × L) token comparisons per query. An inverted index maps term→posting list; retrieval cost depends on matched posting lengths plus ranking, often much less than N but sensitive to frequent terms. Use empirical p95 measurements rather than treating asymptotics as guaranteed runtime.

## Independent lab
Create a dependency map in plain Python **without AI writing your solution**:
1. Accept a dictionary of nodes to outgoing dependencies and a starting node.
2. Return all reachable nodes deterministically, handling cycles and missing nodes.
3. Return one explicit path for each reachable node, using BFS and parent pointers.
4. Track time complexity and memory. Add tests for no edges, duplicate edges, cycles, 10,000-node chain and disconnected graph.
5. Add an `edge_evidence` field with source file/revision; distinguish `observed` vs `assumed` links.

## Defense questions
Why BFS instead of DFS when users need shortest hop path? Why is graph reachability not causal proof? At what number of edges should you use a database? What test fails if the visited set is missing? Explain memory O(V+E) and the impact of edge revisions.

**Mastery gate:** Correct independent implementation, executed tests, Big-O reasoning, and precise limits of inference. Read MIT 6.006 in `docs/REFERENCES.md`.
