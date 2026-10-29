# MCP and tool trust governance

No external MCP server is approved or configured by this repository. Default deny.
`opencode.json` is preserved. The offline `golden.tools` example is a deterministic
policy gate, not an MCP client, identity provider, sandbox or production security system.

An application registry entry must bind server ID, accountable owner, transport/endpoint,
approved artifact/commit and dependency digest, tool IDs, complete definition hashes
(including descriptions and schemas), classification, grants, expiry and incident contact.
Approved servers expose only narrowly typed operations; avoid general shell/SQL/URL tools.
Review transitive tool discovery; newly advertised tools never auto-enable.

At connection and every invocation compare against pinned definitions. Definition drift,
unknown server/tool, expired approval or unreachable policy service denies before model
exposure or execution. Tool descriptions are supply-chain inputs; review them for hidden
instructions and data exfiltration. Hashing detects change against a **trusted** baseline;
it does not prove a malicious baseline safe. Store approval separately from server output.

Runtime validates authenticated actor, tenant, purpose, scope, input/output schema,
classification, timeout and total budget. A model proposal or tool-returned instruction
does not grant authority. Enforce permissions again at the adapter/source; filter outputs
and caches. Production effects stay outside the reasoning tool set. Log redacted decision
IDs/reasons and reconcile unknown outcomes. Stop/disable the tool on poisoning suspicion;
quarantine affected traces and use the manual read-only path.

| Data class | Allowed data-to-model route |
|---|---|
| Synthetic/public | Explicitly approved endpoint for task; the offline demo sends nothing |
| Internal | Owner-approved internal model endpoint and retention policy |
| Restricted/proprietary/personal | Explicit purpose/source-owner approval, minimization, approved isolated endpoint; deny by default |
| Credentials/secrets | Never include in model context or tool telemetry; service resolves outside model |

Registry approval includes model destination and logging/retention, not just tool access.
Forbid downgrading classification because a tool summarizes content.

Required poisoning tests: altered description/schema/version, extra tool, lookalike server,
malicious source instruction requesting a write, mismatched classification, excess budget,
revoked grants, deadline/cancel and schema-invalid arguments. The runnable offline tests
cover deterministic gate decisions, not a live model's ability to resist prompt injection,
real identity, endpoint authenticity, remote schema validation or server compromise.
Run `python -m scripts.trace_demo` for safe successful/denied examples.
