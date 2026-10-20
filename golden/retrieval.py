"""Deterministic, access-filtered retrieval over synthetic records.

This is a teaching baseline, NOT an ACL implementation for a real employee data system.
Authn/authz must be enforced by trusted external infrastructure in production.
"""
from dataclasses import dataclass
from collections import Counter
from math import log
import re
from typing import Iterable

TOKENS = re.compile(r"[a-z0-9]+(?:[-_.][a-z0-9]+)*", flags=re.I)


def tokenize(text: str) -> list[str]:
    return TOKENS.findall(text.lower())


@dataclass(frozen=True)
class Evidence:
    record_id: str
    source: str
    revision: str
    text: str
    permitted_roles: frozenset[str]
    timestamp: str

    @classmethod
    def from_dict(cls, x: dict) -> 'Evidence':
        required = ('record_id', 'source', 'revision', 'text', 'permitted_roles', 'timestamp')
        if any(k not in x for k in required):
            raise ValueError('Evidence record missing required fields')
        if not x['record_id'] or not x['permitted_roles']:
            raise ValueError('Missing evidence ID or roles')
        return cls(x['record_id'], x['source'], x['revision'], x['text'],
                   frozenset(x['permitted_roles']), x['timestamp'])


@dataclass(frozen=True)
class Hit:
    record: Evidence
    score: float


class EvidenceIndex:
    def __init__(self, records: Iterable[Evidence]):
        self.records = tuple(records)
        identifiers = [r.record_id for r in self.records]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError('Duplicate evidence identifiers')

    def search(self, query: str, roles: frozenset[str], top_k: int = 3) -> list[Hit]:
        if top_k < 1 or top_k > 100:
            raise ValueError('top_k out of bounds')
        if not query.strip():
            return []
        # Defense in depth only: production must verify identity, map real ACLs,
        # and restrict data *before* search and in downstream cache/output.
        if not roles:
            return []
        visible = [r for r in self.records if r.permitted_roles & roles]
        words = tokenize(query)
        if not words:
            return []
        query_terms = Counter(words)
        postings = [Counter(tokenize(r.text + ' ' + r.record_id + ' ' + r.source)) for r in visible]
        N = len(visible)
        df = Counter(w for bag in postings for w in bag)
        hits = []
        for record, bag in zip(visible, postings):
            score = sum((1.0 + log(1 + N / (1 + df[w]))) * min(bag[w], 3) * min(qn, 2)
                        for w, qn in query_terms.items() if bag[w])
            # Exact identifiers are exceptionally important in manufacturing.
            if record.record_id.lower() in query.lower():
                score += 20
            if score > 0:
                hits.append(Hit(record, round(score, 5)))
        return sorted(hits, key=lambda x: (-x.score, x.record.record_id))[:top_k]
