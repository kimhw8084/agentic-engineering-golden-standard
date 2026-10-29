---
name: security-review
description: Threat-model AI application data, identity, tool privileges, injection, privacy and production change safety.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Security Review

## Procedure
Use `docs/TOOL_TRUST.md` for MCP enrollment, definition pinning and data-to-model policy.

Read `docs/SECURITY_THREAT_MODEL.md`. Identify assets, actors, trust boundaries, source and model context exposure, sensitive logs, service secrets, tenant/role scopes, retention and lifecycle, injection entry points. Reject any assumption that client-provided roles, prompts or retrieved documents establish authorization. Specify server-enforced controls. Attempt adversarial tests: restricted record metadata, retrieval cache, stale revisions, forged role, document-injected command, duplicate writes. Provide severity-ranked findings and block release if critical unresolved issues exist.
