---
name: performance-lab
description: Instrument and optimize end-to-end correctness, latency, retrieval quality, tool calls and cost.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Performance Lab

## Procedure
Create representative test corpus and workload; capture implementation revision and environment. Measure p50/p95 and max of end-to-end and per-stage latency; record model/tool calls, token usage/cost proxy, error/timeout counts, throughput under safe synthetic load. Change one variable per experiment, repeat runs and compare with original accuracy/security holdouts. Identify bottlenecks before concurrency, caching, reranking or model changes. Output a before/after table with uncertainty and any regressions. See `docs/PERFORMANCE_PLAYBOOK.md`.
