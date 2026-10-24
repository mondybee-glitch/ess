#!/usr/bin/env python3
"""Run operational fixtures across Python and Node.js; Playwright is opt-in."""
import argparse, datetime, hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; FIX=ROOT/'operational-fixtures'
def sha(b): return hashlib.sha256(b).hexdigest()
def run(cmd,cwd,timeout):
 try:
  p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=timeout,shell=False,env={**os.environ,'CI':'1','PYTHONDONTWRITEBYTECODE':'1'})
  return {'status':'passed' if p.returncode==0 else 'failed','exit_code':p.returncode,'stdout':p.stdout[-10000:],'stderr':p.stderr[-10000:]}
 except subprocess.TimeoutExpired as e: return {'status':'timeout','exit_code':124,'stdout':str(e.stdout or '')[-10000:],'stderr':str(e.stderr or '')[-10000:]}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--timeout',type=int,default=45); ap.add_argument('--include-playwright',action='store_true'); ap.add_argument('--output',default='reports/multilang-fixtures-latest.json'); a=ap.parse_args()
 if not 1<=a.timeout<=300: print('timeout must be 1..300',file=sys.stderr); return 2
 records=[]
 for d in sorted(x for x in FIX.iterdir() if x.is_dir()):
  if (d/'subject.py').exists(): continue # Existing Python runner remains the authority for Python fixtures.
  if d.name=='playwright-ui-state' and not a.include_playwright: continue
  if d.name=='node-idempotency-boundary':
   if not shutil.which('node'): result={'status':'skipped','exit_code':None,'stdout':'','stderr':'node not installed'}
   else: result=run(['node','--test','subject.test.mjs'],d,a.timeout)
  elif d.name=='playwright-ui-state':
   if not shutil.which('npx'): result={'status':'skipped','exit_code':None,'stdout':'','stderr':'npx not installed'}
   elif not (d/'node_modules/@playwright/test').exists(): result={'status':'skipped','exit_code':None,'stdout':'','stderr':'Playwright dependency not installed; runner will not install dependencies'}
   else: result=run(['npx','playwright','test'],d,a.timeout)
  else: continue
  result.update({'fixture_id':d.name,'language':'TypeScript' if d.name=='playwright-ui-state' else 'JavaScript','artifact_hashes':{p.name:sha(p.read_bytes()) for p in sorted(d.iterdir()) if p.is_file()}}); records.append(result)
 report={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runner':'scripts/run_multilang_fixtures.py','claim_boundary':'Only listed fixture outcomes are covered; skipped means not tested. Existing Python fixtures run via scripts/run_operational_fixtures.py.','summary':{'total':len(records),'passed':sum(x['status']=='passed' for x in records),'failed':sum(x['status']=='failed' for x in records),'timed_out':sum(x['status']=='timeout' for x in records),'skipped':sum(x['status']=='skipped' for x in records)},'records':records}
 out=(ROOT/a.output).resolve(); out.relative_to(ROOT.resolve()); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(json.dumps(report['summary'])); return 1 if report['summary']['failed'] or report['summary']['timed_out'] else 0
if __name__=='__main__': raise SystemExit(main())
