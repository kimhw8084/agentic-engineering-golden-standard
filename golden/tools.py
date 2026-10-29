"""Offline tool-policy teaching example. Caller inputs are NOT authenticated.

No MCP connection, model, network or effects. Production must resolve trusted
registry/policy inputs itself and validate actual tool arguments at the adapter.
"""
from dataclasses import dataclass
from golden.change import canonical_hash


class ToolDenied(ValueError):
    pass


@dataclass(frozen=True)
class ToolPolicy:
    server_id: str
    tool_id: str
    definition_hash: str
    permitted_scopes: frozenset[str]
    classifications: frozenset[str]
    max_calls: int = 2

    def check(self, *, server_id: str, definition: dict, actor_scopes: frozenset[str],
              required_scope: str, classification: str, calls_used: int,
              remaining_ms: int, canceled: bool = False) -> None:
        if canceled:
            raise ToolDenied('canceled')
        if type(remaining_ms) is not int or remaining_ms <= 0:
            raise ToolDenied('deadline')
        if type(calls_used) is not int or calls_used < 0 or calls_used >= self.max_calls:
            raise ToolDenied('budget')
        if (not isinstance(definition, dict) or not isinstance(required_scope, str)
                or not isinstance(classification, str)):
            raise ToolDenied('input_contract')
        if server_id != self.server_id:
            raise ToolDenied('unapproved_server')
        try:
            definition_matches = canonical_hash(definition) == self.definition_hash
        except (TypeError, ValueError):
            definition_matches = False
        if definition.get('name') != self.tool_id or not definition_matches:
            raise ToolDenied('definition_drift')
        if required_scope not in self.permitted_scopes or required_scope not in actor_scopes:
            raise ToolDenied('scope_denied')
        if classification not in self.classifications:
            raise ToolDenied('classification_denied')
