#!/usr/bin/env python3
"""Run deterministic fixture checks without pretending to run an AI agent.

The fixture-only mode validates the eval contract and inputs. It never marks
agent quality as passed. An agent runner may consume the same case later and
must attach direct artifacts before changing agent_status.
"""
from pathlib import Path
import argparse, json, datetime, sys

ROOT=Path(__file__).resolve().parents[1]

def load_cases(skill=None, case_id=None):
    paths=sorted((ROOT/'skills').glob('*/evals/evals.json')) if skill is None else [ROOT/'skills'/skill/'evals/evals.json']
    out=[]
    for p in paths:
        if not p.is_file(): raise FileNotFoundError(p)
        data=json.loads(p.read_text())
        for c in data.get('cases',[]):
            if case_id is None or c.get('id')==case_id: out.append((p.parent.parent.name,c))
    return out

def fixture_check(skill,c):
    required=['fixture','expected_output','automated_checks','human_review_rubric']
    missing=[k for k in required if not c.get(k)]
    fp=ROOT/c.get('fixture','')
    if not fp.is_file():
        missing.append('fixture-file')
    elif c.get('fixture_selector'):
        try:
            shared=json.loads(fp.read_text(encoding='utf-8'))
            matches=[x for x in shared.get('fixtures',[]) if x.get('fixture_id')==c.get('fixture_selector')]
            if len(matches)!=1:
                missing.append('fixture-selector-not-unique')
            else:
                selected=matches[0]
                if selected.get('skill_id') != skill: missing.append('fixture-skill-mismatch')
                if selected.get('expected_output') != c.get('expected_output'): missing.append('fixture-expected-output-mismatch')
                if selected.get('fixture_status') != 'defined-not-run' or selected.get('agent_status') != 'not-run': missing.append('fixture-claims-execution')
        except (OSError, json.JSONDecodeError, AttributeError):
            missing.append('fixture-json-invalid')
    return {'skill':skill,'case_id':c.get('id'),'fixture':c.get('fixture'),'fixture_selector':c.get('fixture_selector'),'fixture_status':'passed' if not missing else 'failed','missing':missing,'agent_status':'unverified','claim':'fixture contract only; no agent task executed'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--skill'); ap.add_argument('--case'); ap.add_argument('--output',default='reports/fixture-validation.json')
    ap.add_argument('--mode',choices=['fixture-only'],default='fixture-only')
    args=ap.parse_args()
    records=[fixture_check(s,c) for s,c in load_cases(args.skill,args.case)]
    if not records: print('No matching cases',file=sys.stderr); return 2
    report={'schema_version':1,'run_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':args.mode,'records':records,'summary':{'total':len(records),'fixture_passed':sum(r['fixture_status']=='passed' for r in records),'agent_results':'not run'}}
    out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(report['summary'],ensure_ascii=False))
    return 0 if report['summary']['fixture_passed']==report['summary']['total'] else 1
if __name__=='__main__': sys.exit(main())
