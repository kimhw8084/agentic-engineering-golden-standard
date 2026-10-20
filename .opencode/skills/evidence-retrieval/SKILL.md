---
name: evidence-retrieval
description: Build permission-scoped, version-aware retrieval across source code, messages, manuals and operational data.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Evidence Retrieval

## Procedure
1. Identify approved source owners, access controls, source-specific IDs, timestamps and retention/delete semantics.
2. Route exact identifiers and time-range facts to typed SQL/API lookups; documents to lexical/semantic search only where needed.
3. Preserve canonical IDs, source revision/hash, updated/deleted status, permitted scope and citation offsets.
4. Design incremental ingestion, dedupe, refresh, ACL recheck on every request, cache invalidation.
5. Evaluate recall/precision, citation provenance, stale-index failures and unauthorized disclosure.
6. Never infer operational truth solely from embeddings. Never ingest all employee communications or manufacturing recipes without approved need and access.
