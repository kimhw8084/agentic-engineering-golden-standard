"""Public development self-check; not independent labels or a protected evaluation."""
import argparse
import ast
from datetime import datetime, timezone
from hashlib import sha256
import json
from math import ceil
from pathlib import Path
import platform
import statistics
import subprocess
from time import perf_counter

from golden import investigation as pilot

ROOT = Path(__file__).resolve().parents[1]


def candidate(case, reader=pilot.read_snapshot):
    request = case['request']
    try:
        state, snapshot, root = pilot.authorize(request)
    except ValueError:
        return {'status': 'input_contract','nodes': [],'unresolved': []}
    if state != 'allowed': return {'status': state,'nodes': [],'unresolved': []}
    if case.get('fault') == 'unavailable':
        return {'status': 'unavailable','nodes': [],'unresolved': []}
    data = reader(snapshot)
    if case.get('fault') == 'tampered': data += b'\n# drift'
    try: return pilot.resolve(request,data,snapshot,root)
    except ValueError: return {'status': 'integrity_error','nodes': [],'unresolved': []}


def literal_search(case):
    """Baseline locator only: functions containing the exact parameter token.

    It does not claim an answer, dependency closure or negative-outcome semantics.
    Same authorization, corpus and revision pin as the candidate.
    """
    try: status, snapshot, _ = pilot.authorize(case['request'])
    except ValueError: return []
    if status != 'allowed' or case.get('fault'): return []
    data = pilot.read_snapshot(snapshot)
    text = data.decode('utf-8'); tree = ast.parse(text)
    return sorted(n.name for n in tree.body if isinstance(n,ast.FunctionDef)
                  and any(isinstance(v,ast.Constant) and v.value == case['request']['parameter']
                          for v in ast.walk(n)))


def citation_errors(result, expected_request=None):
    errors = []
    if result.get('nodes') and expected_request is not None and result.get('request') != expected_request:
        errors.append('wrong request/revision binding')
    for item in result.get('nodes',[]) + result.get('edges',[]) + result.get('unresolved',[]):
        ref = item.get('ref')
        if ref is None:
            if item.get('kind') != 'budget': errors.append('missing citation')
            continue
        snapshot = pilot.manifest()['snapshots'][result['request']['revision']]
        data = pilot.read_snapshot(snapshot)
        if (type(ref.get('line_start')) is not int or type(ref.get('line_end')) is not int
                or not 1 <= ref['line_start'] <= ref['line_end'] <= len(data.decode().splitlines())):
            errors.append('invalid line range'); continue
        excerpt = '\n'.join(data.decode().splitlines()[ref['line_start']-1:ref['line_end']])
        if (ref['path'] != snapshot['path'] or ref['source_sha256'] != sha256(data).hexdigest()
                or ref['revision'] != result['request']['revision'] or ref['excerpt'] != excerpt):
            errors.append(ref)
    return errors


def grade(case, result):
    expected=case['expected']; got=sorted(n['symbol'] for n in result['nodes'])
    unknown=sorted(u['kind'] for u in result['unresolved'])
    edges=sorted([e['from'],e['to']] for e in result.get('edges',[]))
    targets=sorted(u['target'] for u in result['unresolved'])
    errors=citation_errors(result,case['request'])
    return (result['status']==expected['status'] and got==expected['symbols']
            and unknown==expected['unknown_kinds'] and targets==expected['unknown_targets']
            and edges==expected['edges'] and not errors)


def evaluate(cases_path, repeats=5):
    if type(repeats) is not int or not 1 <= repeats <= 100: raise ValueError('repeats 1..100')
    raw = cases_path.read_bytes(); dataset = json.loads(raw); cases = dataset['cases']
    if not cases or len({c['id'] for c in cases}) != len(cases): raise ValueError('unique cases required')
    details, times, baseline_times, recalls, baseline_recalls = [], [], [], [], []
    positive_times, positive_baseline_times = [], []
    local_reads = 0
    def observe_read(snapshot):
        nonlocal local_reads
        local_reads += 1
        return pilot.read_snapshot(snapshot)
    for case in cases:
        for _ in range(repeats):
            start=perf_counter(); result=candidate(case,observe_read); duration=(perf_counter()-start)*1000;times.append(duration)
            start=perf_counter(); baseline=literal_search(case); base_duration=(perf_counter()-start)*1000;baseline_times.append(base_duration)
            if case['expected']['symbols']:
                positive_times.append(duration);positive_baseline_times.append(base_duration)
        expected=case['expected']; got=sorted(n['symbol'] for n in result['nodes'])
        errors=citation_errors(result,case['request']);passed=grade(case,result)
        needed=set(expected['symbols'])
        if needed:
            recalls.append(len(needed & set(got))/len(needed))
            baseline_recalls.append(len(needed & set(baseline))/len(needed))
        details.append({'id':case['id'],'slice':case['slice'],'passed':passed,
                        'status':result['status'],'symbols':got,'baseline_symbols':baseline,
                        'citation_binding_errors':len(errors)})
    def timing(xs):
        return {'p50_ms':round(statistics.median(xs),4),
                'p95_ms':round(sorted(xs)[ceil(len(xs)*.95)-1],4),'samples':len(xs)}
    def git(*args):
        try: return subprocess.check_output(['git',*args],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
        except (OSError,subprocess.CalledProcessError): return None
    files=['golden/investigation.py','golden/pilot_control.py','scripts/investigation_app.py',
           'scripts/evaluate_investigation.py','examples/manufacturing/manifest.json',
           'golden/tools.py','golden/change.py','examples/manufacturing/app.html']
    return {'scope':'Author-labeled PUBLIC SYNTHETIC DEVELOPMENT; no independent signoff or business win.',
            'cases':len(cases),'passed':sum(d['passed'] for d in details),'details':details,
            'dependency_locator_recall':{'candidate':statistics.mean(recalls),
                                       'literal_baseline':statistics.mean(baseline_recalls),
                                       'denominator_cases':len(recalls),
                                       'meaning':'Exact required function set in curated toy graph; not semantic accuracy.'},
            'latency':{'candidate':timing(times),'literal_baseline':timing(baseline_times),
                       'positive_candidate':timing(positive_times) if positive_times else None,
                       'positive_literal_baseline':timing(positive_baseline_times) if positive_baseline_times else None,
                       'method':'median / nearest-rank p95; local warm filesystem; full authorize/read/parse; no UI'},
            'model_calls':0,'external_calls':0,'billed_model_cost':0,
            'candidate_local_snapshot_read_attempts':local_reads,
            'read_count_scope':'Candidate lookup repeats only, excludes baseline/grader; no MCP connection.',
            'unmeasured':{'manual_active_minutes':None,'candidate_active_minutes':None,
                          'review_rework_minutes':None,'monthly_task_frequency':None,
                          'eligible_users':None,'monthly_capacity_hours':None,
                          'build_and_maintenance_cost':None,'independent_accuracy':None,
                          'protected_holdout':None,'employee_task_success':None,
                          'reason':'No authorized company corpus, curator, users, labor timing or approved endpoint.'},
            'provenance':{'commit':git('rev-parse','HEAD'),'dirty':bool(git('status','--porcelain')),
                          'timestamp_utc':datetime.now(timezone.utc).isoformat(),
                          'tool_definition_sha256':pilot.POLICY.definition_hash,
                          'python':platform.python_version(),'platform':platform.platform(),
                          'cases_sha256':sha256(raw).hexdigest(),'repeats':repeats,
                          'label_status':dataset['label_status'],
                          'implementation_sha256':{f:sha256((ROOT/f).read_bytes()).hexdigest() for f in files}}}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--cases',type=Path,default=ROOT/'examples/manufacturing/development_cases.json')
    parser.add_argument('--repeats',type=int,default=5)
    parser.add_argument('--output',type=Path,default=ROOT/'out/first-win/investigation-evaluation.json')
    args=parser.parse_args(); result=evaluate(args.cases,args.repeats)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['details','provenance']},indent=2))
    raise SystemExit(result['cases'] != result['passed'])
