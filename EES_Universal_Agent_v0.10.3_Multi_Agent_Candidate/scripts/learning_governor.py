#!/usr/bin/env python3
"""Govern temporary agent instincts; promotion requires holdout + regression evidence."""
import argparse, json, hashlib, time, hmac, os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STORE=Path(__import__('os').environ.get('EES_INSTINCT_STORE', str(ROOT/'state'/'temporary-instincts.json')))

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x): return hashlib.sha256(x).hexdigest()
def report_signature(report, key):
    body={k:v for k,v in report.items() if k!='hmac_sha256'}
    return hmac.new(key.encode('utf-8'), canon(body), hashlib.sha256).hexdigest()
def verify_evaluation_report(report, target, baseline, holdout):
    key=os.environ.get('EES_LEARNING_REPORT_HMAC_KEY','')
    if len(key)<32: raise ValueError('EES_LEARNING_REPORT_HMAC_KEY must be set to a secret of at least 32 characters')
    required={'candidate_id','rule_sha256','dataset_id','runner_id','status','failed','holdout_passed','baseline_score','holdout_score','hmac_sha256'}
    if not isinstance(report,dict) or not required.issubset(report): raise ValueError('evaluation report missing required provenance fields')
    if report['candidate_id'] != target['id']: raise ValueError('evaluation report candidate_id mismatch')
    if report['rule_sha256'] != sha(target['rule'].encode('utf-8')): raise ValueError('evaluation report rule hash mismatch')
    if not isinstance(report['dataset_id'],str) or not report['dataset_id'] or not isinstance(report['runner_id'],str) or not report['runner_id']: raise ValueError('evaluation report provenance is invalid')
    if report['baseline_score'] != baseline or report['holdout_score'] != holdout: raise ValueError('evaluation report scores do not match requested scores')
    expected=report_signature(report,key)
    if not hmac.compare_digest(str(report.get('hmac_sha256','')), expected): raise ValueError('evaluation report signature invalid')
    if report['status']!='PASS' or report['failed']!=0 or report['holdout_passed'] is not True: raise ValueError('evaluation report did not pass regression and holdout gates')
    return True
def verify_ledger(d):
    previous='0'*64
    events=d.get('events')
    if not isinstance(events,list): raise ValueError('invalid event ledger')
    for seq,e in enumerate(events,1):
        if not isinstance(e,dict) or e.get('seq')!=seq or e.get('prev_hash')!=previous:
            raise ValueError(f'event ledger chain broken at sequence {seq}')
        body={k:v for k,v in e.items() if k!='hash'}
        expected=sha(canon(body))
        if e.get('hash')!=expected: raise ValueError(f'event ledger hash mismatch at sequence {seq}')
        previous=expected
    if not isinstance(d.get('instincts'),list): raise ValueError('invalid instincts store')
    return True

def load():
    if STORE.exists():
        d=json.loads(STORE.read_text())
        verify_ledger(d)
        if d.get('schema_version') != 1: raise ValueError('unsupported instinct store schema')
        return d
    return {'schema_version':1,'instincts':[],'events':[]}
def save(d):
    verify_ledger(d)
    STORE.parent.mkdir(parents=True,exist_ok=True); tmp=STORE.with_suffix('.tmp')
    tmp.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8'); tmp.replace(STORE)
def event(d,kind,payload):
    prev=d['events'][-1]['hash'] if d['events'] else '0'*64
    e={'seq':len(d['events'])+1,'at':int(time.time()),'kind':kind,'payload':payload,'prev_hash':prev}
    e['hash']=sha(canon(e)); d['events'].append(e)
def cmd(args):
    d=load()
    if args.action=='propose':
        if not args.name or not args.rule: raise SystemExit('--name and --rule required')
        if args.ttl_days < 1 or args.ttl_days > 90: raise SystemExit('--ttl-days must be between 1 and 90')
        if any(x['name']==args.name and x['status']=='ACTIVE' for x in d['instincts']): raise SystemExit('active instinct with this name exists')
        x={'id':sha(canon({'name':args.name,'rule':args.rule,'time':int(time.time())}) )[:16], 'name':args.name,'rule':args.rule,'status':'TEMPORARY','created_at':int(time.time()),'baseline_score':None,'holdout_score':None,'regression_passed':False,'expires_at':int(time.time())+args.ttl_days*86400}
        d['instincts'].append(x); event(d,'PROPOSED',{'id':x['id'],'name':x['name']}); save(d); print(json.dumps(x,indent=2)); return 0
    target=next((x for x in d['instincts'] if x['id']==args.id),None)
    if target is None: raise SystemExit('unknown instinct id')
    if args.action=='evaluate':
        if args.baseline is None or args.holdout is None or args.regression_report is None: raise SystemExit('evaluation requires --baseline, --holdout, --regression-report')
        if not (0.0 <= args.baseline <= 1.0 and 0.0 <= args.holdout <= 1.0): raise SystemExit('scores must be within [0, 1]')
        if not (0.0 <= args.max_regression <= 1.0): raise SystemExit('--max-regression must be within [0, 1]')
        report=Path(args.regression_report)
        if not report.is_file(): raise SystemExit('regression report file not found')
        try:
            regression=json.loads(report.read_text(encoding='utf-8'))
            verify_evaluation_report(regression,target,args.baseline,args.holdout)
        except Exception as e: raise SystemExit(f'invalid or untrusted regression report: {e}')
        passed=True
        target.update(baseline_score=args.baseline,holdout_score=args.holdout,regression_passed=passed,regression_report_sha256=sha(report.read_bytes()),evaluation_report=regression,evaluated_at=int(time.time()))
        event(d,'EVALUATED',{'id':target['id'],'baseline':args.baseline,'holdout':args.holdout,'regression_passed':passed}); save(d)
        print(json.dumps({'id':target['id'],'eligible':passed and args.holdout>=args.baseline-args.max_regression,'regression_passed':passed},indent=2)); return 0
    if args.action=='promote':
        # Promotion only after independent evaluation, score floor, no material regression, and unexpired candidate.
        if target['status']!='TEMPORARY': raise SystemExit('only TEMPORARY instincts can be promoted')
        if not (0.0 <= args.max_regression <= 1.0): raise SystemExit('--max-regression must be within [0, 1]')
        if target.get('expires_at',0)<int(time.time()): raise SystemExit('candidate expired; propose a new candidate')
        if target.get('holdout_score') is None or target.get('baseline_score') is None or not target.get('regression_passed'): raise SystemExit('blocked: missing passing holdout/regression evidence')
        try:
            verify_evaluation_report(target.get('evaluation_report',{}),target,target['baseline_score'],target['holdout_score'])
        except Exception as e: raise SystemExit(f'blocked: evaluation evidence revalidation failed: {e}')
        if target['holdout_score'] < target['baseline_score']-args.max_regression: raise SystemExit('blocked: holdout regression exceeds threshold')
        target['status']='ACTIVE'; target['promoted_at']=int(time.time()); event(d,'PROMOTED',{'id':target['id'],'max_regression':args.max_regression}); save(d); print('PROMOTED'); return 0
    if args.action=='rollback':
        target['status']='ROLLED_BACK'; target['rolled_back_at']=int(time.time()); target['rollback_reason']=args.reason; event(d,'ROLLED_BACK',{'id':target['id'],'reason':args.reason}); save(d); print('ROLLED_BACK'); return 0
    if args.action=='list': print(json.dumps(d,indent=2)); return 0
    return 2

def main():
 p=argparse.ArgumentParser(); p.add_argument('action',choices=['propose','evaluate','promote','rollback','list']); p.add_argument('--name'); p.add_argument('--rule'); p.add_argument('--ttl-days',type=int,default=14); p.add_argument('--id'); p.add_argument('--baseline',type=float); p.add_argument('--holdout',type=float); p.add_argument('--regression-report'); p.add_argument('--max-regression',type=float,default=0.02); p.add_argument('--reason',default='operator rollback'); a=p.parse_args(); return cmd(a)
if __name__=='__main__': raise SystemExit(main())
