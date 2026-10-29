"""Bounded static inspection of TWO bundled synthetic Python snapshots.

No eval/import of inspected code, model, external adapter, general repository ingest,
or guarantee of runtime data flow. The trusted manifest maps parameters to roots.
"""
import ast
from collections import deque
from hashlib import sha256
import json
from pathlib import Path
import re

from golden.change import canonical_hash
from golden.tools import ToolPolicy

ROOT = Path(__file__).resolve().parents[1]
DEFINITION = {'name': 'read_synthetic_snapshot', 'version': '1',
              'description': 'Read a pinned bundled synthetic source snapshot only.',
              'input_schema': {'revision': 'manifest enum; no path or URL'}}
POLICY = ToolPolicy('bundled', DEFINITION['name'], canonical_hash(DEFINITION),
                    frozenset({'synthetic:read'}), frozenset({'synthetic'}), max_calls=1)
BUILTINS = frozenset({'int', 'type', 'ValueError'})


def manifest():
    return json.loads((ROOT/'examples/manufacturing/manifest.json').read_text(encoding='utf-8'))


def validate_request(request):
    if (not isinstance(request, dict) or set(request) != {'revision', 'parameter'}
            or not isinstance(request['revision'], str) or len(request['revision']) > 64
            or not isinstance(request['parameter'], str)
            or not re.fullmatch(r'[a-z_][a-z_0-9]{0,63}', request['parameter'])):
        raise ValueError('exact request schema: revision and parameter identifier required')


def authorize(request, grants=frozenset({'synthetic:read'})):
    validate_request(request)
    POLICY.check(server_id='bundled', definition=DEFINITION, actor_scopes=grants,
                 required_scope='synthetic:read', classification='synthetic',
                 calls_used=0, remaining_ms=1000)
    spec = manifest()
    entry = spec['parameters'].get(request['parameter'])
    if entry is not None and entry['scope'] not in grants:
        return 'denied', None, None
    if request['revision'] not in spec['snapshots']:
        return 'unavailable', None, None
    if entry is None:
        return 'abstained', None, None
    return 'allowed', spec['snapshots'][request['revision']], entry['root']


def read_snapshot(snapshot):
    # Path comes only from the bundled manifest, never user/model input.
    path = ROOT/snapshot['path']
    if path.is_symlink() or path.resolve().parent != (ROOT/'examples/manufacturing').resolve():
        raise ValueError('unapproved snapshot path')
    data = path.read_bytes()
    if sha256(data).hexdigest() != snapshot['sha256']:
        raise ValueError('snapshot hash mismatch')
    return data


def resolve(request, data, snapshot, root, max_nodes=64):
    """O(source AST + V + E) within bounded source and reachable graph; no cache.

    Enumerates syntactic local calls, including branches that may not run. Unknown
    calls stay unknown. It does not infer values, aliases or runtime reachability.
    """
    if len(data) > 100_000 or sha256(data).hexdigest() != snapshot['sha256']:
        raise ValueError('oversized or changed snapshot')
    text = data.decode('utf-8'); lines = text.splitlines()
    tree = ast.parse(text); functions = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name in functions:
                raise ValueError('ambiguous duplicate function definition')
            functions[node.name] = node
    if root not in functions:
        raise ValueError('manifest root missing')
    nodes, edges, unknowns = [], [], []
    queue, seen = deque([root]), set()
    def ref(node):
        return {'path': snapshot['path'], 'revision': request['revision'],
                'source_sha256': snapshot['sha256'], 'line_start': node.lineno,
                'line_end': node.end_lineno,
                'excerpt': '\n'.join(lines[node.lineno-1:node.end_lineno])}
    while queue:
        name = queue.popleft()
        if name in seen:
            continue
        if len(seen) >= max_nodes:
            unknowns.append({'kind': 'budget', 'target': name}); break
        seen.add(name); node = functions[name]
        if any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda))
               for child in node.body for n in ast.walk(child)):
            unknowns.append({'kind': 'unsupported_nested_scope', 'target': name, 'ref': ref(node)})
            continue
        nodes.append({'symbol': name, 'ref': ref(node)})
        for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
            target = call.func.id if isinstance(call.func, ast.Name) else ast.unparse(call.func)
            if isinstance(call.func, ast.Name) and target in functions:
                edges.append({'from': name, 'to': target, 'ref': ref(call), 'kind': 'static_call'})
                queue.append(target)
            elif not (isinstance(call.func, ast.Name) and target in BUILTINS):
                unknowns.append({'kind': 'missing_source' if isinstance(call.func, ast.Name)
                                 else 'dynamic_dispatch', 'target': target, 'ref': ref(call)})
    return {'status': 'partial' if unknowns else 'supported', 'request': request,
            'snapshot_sha256': snapshot['sha256'], 'nodes': nodes, 'edges': edges,
            'unresolved': unknowns, 'assumptions': [
                'Manifest parameter-to-root mapping is author-curated, not independently approved.',
                'Syntactic local calls overapproximate execution; no runtime behavior or values proven.',
                'Only one bundled Python module; aliases, imports and runtime dispatch unresolved.'],
            'model_calls': 0, 'external_calls': 0, 'classification': 'synthetic'}


def investigate(request, grants=frozenset({'synthetic:read'})):
    status, snapshot, root = authorize(request, grants)
    if status != 'allowed':
        return {'status': status, 'nodes': [], 'edges': [], 'unresolved': []}
    return resolve(request, read_snapshot(snapshot), snapshot, root)
