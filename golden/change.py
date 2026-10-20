"""Offline reference state machine. No manufacturing execution interfaces."""
from dataclasses import dataclass, field
from hashlib import sha256
import json


class GateError(ValueError):
    pass


def canonical_hash(payload: dict) -> str:
    return sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=False).encode('utf-8')).hexdigest()


def validate_draft(payload: dict, allowed_systems: frozenset[str]) -> list[str]:
    """Illustrative checks; actual operational files need *existing domain validators*."""
    errors = []
    if not isinstance(payload, dict):
        return ['draft must be an object']
    if set(payload) != {'change_id', 'system', 'revision', 'parameter', 'value'}:
        errors.append('draft fields do not match exact schema')
    for key in ('change_id', 'system', 'revision', 'parameter'):
        if not isinstance(payload.get(key), str) or not payload.get(key, '').strip():
            errors.append(f'invalid or missing {key}')
    if not isinstance(payload.get('system'), str) or payload.get('system') not in allowed_systems:
        errors.append('unsupported system')
    # Strict integer, not bool (bool subclasses int).
    if type(payload.get('value')) is not int or not 0 <= payload['value'] <= 100:
        errors.append('value must be integer 0..100')
    return errors


@dataclass
class ChangeRun:
    """Approval here is merely a synthetic review event, NOT operational approval."""
    run_id: str
    status: str = 'created'
    draft: dict | None = None
    draft_hash: str | None = None
    validated_hash: str | None = None
    approval_hash: str | None = None
    events: list[dict] = field(default_factory=list)

    def _transition(self, wanted: str, permitted: tuple[str, ...]):
        if self.status not in permitted:
            raise GateError(f'Cannot transition from {self.status} to {wanted}')
        self.status = wanted
        self.events.append({'action': wanted, 'run_id': self.run_id})

    def evidence_ready(self):
        self._transition('evidence_ready', ('created',))

    def set_draft(self, payload: dict):
        self._transition('drafted', ('evidence_ready', 'drafted', 'validated'))
        # Copy prevents mutation of caller-owned dictionary after this point.
        self.draft = json.loads(json.dumps(payload))
        self.draft_hash = canonical_hash(self.draft)
        self.validated_hash = None
        self.approval_hash = None

    def validate(self, allowed_systems: frozenset[str]):
        if self.status != 'drafted' or self.draft is None:
            raise GateError('draft missing or not in drafted state')
        errors = validate_draft(self.draft, allowed_systems)
        if errors:
            self.events.append({'action': 'validation_failed', 'errors': errors})
            raise GateError('; '.join(errors))
        self.validated_hash = self.draft_hash
        self._transition('validated', ('drafted',))

    def review(self, reviewer_id: str, is_independent: bool):
        if not reviewer_id or not is_independent:
            raise GateError('independent reviewer required')
        if self.validated_hash != self.draft_hash:
            raise GateError('draft changed since validation')
        self._transition('reviewed', ('validated',))
        self.approval_hash = self.validated_hash
        self.events[-1]['reviewer'] = reviewer_id

    def export(self) -> dict:
        if self.status != 'reviewed':
            raise GateError('review required before export')
        if self.draft is None or canonical_hash(self.draft) != self.approval_hash:
            raise GateError('artifact changed after validation / review')
        self._transition('exported', ('reviewed',))
        return json.loads(json.dumps(self.draft))
