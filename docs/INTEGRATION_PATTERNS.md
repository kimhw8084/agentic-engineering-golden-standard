# Integration patterns for internal systems

## Trusted read-only adapter

Each adapter exposes a fixed typed operation such as `get_job(job_id, time_window, actor_context)` or `get_recipe_metadata(recipe_id, revision)`; it never lets the model supply arbitrary SQL or shell commands. Source owner controls service identity, rate limits, permission enforcement and approved fields. Treat empty results as ambiguous until source health/freshness checked.

## Provenance

Every result carries source URI/opaque ID, content revision, event timestamp, ingestion timestamp, permission scope, extraction version and hash if appropriate. Retain enough metadata to reproduce a test without exposing proprietary payloads.

## Incremental indexing

Use stable document IDs, semantic chunk IDs + content hashes, delete/tombstone propagation, ACL recheck at query time, transactional update metadata and replayable ingestion with dead-letter queues. Never rely on vector-store ACL tags alone for authorization.

## Structured facts vs documents

Use indexed SQL/timeseries exact queries for equipment/run IDs, timestamps, process values. Use lexical+semantic retrieval for SOPs and comments; rerank only with measured benefit. Link facts to source evidence; don't flatten run-time truth into a static knowledge vector.

## Compatibility

OpenCode can call MCP tools, but source services don't need MCP internally. Keep typed FastAPI/SDK interfaces as stable cores and add MCP adapters only when useful. Version tool schemas and test errors, slow sources, 429s and timeouts. Limit enabled tools to prevent context overload.
