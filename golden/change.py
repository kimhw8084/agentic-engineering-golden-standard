"""Offline reference state machine. No manufacturing execution interfaces."""
from dataclasses import dataclass, field
from hashlib import sha256
import json


class GateError(ValueError):
    pass


def canonical_hash(payload: dict) -> str:
    return sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=False, allow_nan=False).encode('utf-8')).hexdigest()


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
    """Caller-attested simulation, not authenticated independent approval.

    Mutable fields/events, no persistence, concurrency control or audit integrity.
    Transitions are one-shot: repeated calls fail, rather than deduplicating retries.
    """
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
        # Prepare first: failed serialization must not change state or events.
        draft = json.loads(json.dumps(payload, allow_nan=False))
        draft_hash = canonical_hash(draft)
        self._transition('drafted', ('evidence_ready', 'drafted', 'validated'))
        self.draft = draft
        self.draft_hash = draft_hash
        self.validated_hash = None
        self.approval_hash = None

    def validate(self, allowed_systems: frozenset[str]):
        if self.status != 'drafted' or self.draft is None:
            raise GateError('draft missing or not in drafted state')
        self._check_draft_hash()
        errors = validate_draft(self.draft, allowed_systems)
        if errors:
            self.events.append({'action': 'validation_failed', 'errors': errors})
            raise GateError('; '.join(errors))
        self.validated_hash = self.draft_hash
        self._transition('validated', ('drafted',))

    def review(self, reviewer_id: str, is_independent: bool):
        """Record a caller assertion only; neither argument proves identity/independence."""
        if not isinstance(reviewer_id, str) or not reviewer_id.strip() or is_independent is not True:
            raise GateError('synthetic independent reviewer assertion required')
        self._check_draft_hash()
        if self.validated_hash != self.draft_hash:
            raise GateError('draft changed since validation')
        self._transition('reviewed', ('validated',))
        self.approval_hash = self.validated_hash
        self.events[-1]['reviewer'] = reviewer_id
        self.events[-1]['review_basis'] = 'unverified_caller_assertion'

    def _check_draft_hash(self):
        try:
            matches = self.draft is not None and canonical_hash(self.draft) == self.draft_hash
        except (TypeError, ValueError):
            matches = False
        if not matches:
            raise GateError('artifact changed since set_draft')

    def export(self) -> dict:
        if self.status != 'reviewed':
            raise GateError('review required before export')
        self._check_draft_hash()
        if self.draft is None or canonical_hash(self.draft) != self.approval_hash:
            raise GateError('artifact changed after validation / review')
        self._transition('exported', ('reviewed',))
        return json.loads(json.dumps(self.draft))
