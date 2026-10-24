#!/usr/bin/env python3
"""Execute deterministic domain fixture projects and hash-bind their evidence.
This validates fixture implementations, not the AI agent or skill instructions.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIXTURES=ROOT/'operational-fixtures'
def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='reports/operational-fixtures-latest.json')
    ap.add_argument('--timeout',type=int,default=30)
    ap.add_argument('--fixture',action='append',default=[])
    args=ap.parse_args()
    if not 1 <= args.timeout <= 300: print('timeout must be in 1..300',file=sys.stderr); return 2
    dirs=sorted(p for p in FIXTURES.iterdir() if p.is_dir() and (not args.fixture or p.name in args.fixture) and (p/'subject.py').is_file())
    if args.fixture and {p.name for p in dirs} != set(args.fixture):
        missing=set(args.fixture)-{p.name for p in dirs}
        print('unknown Python fixture requested (use scripts/run_multilang_fixtures.py for JS/TS): '+', '.join(sorted(missing)),file=sys.stderr); return 2
    records=[]
    for d in dirs:
        manifest_path=d/'fixture.json'; subject=d/'subject.py'; tests=d/'test_fixture.py'
        record={'fixture_id':d.name,'status':'failed','exit_code':None,'duration_ms':None,'artifact_hashes':{},'scope':'fixture implementation only; does not prove agent/skill effectiveness'}
        missing=[p.name for p in (manifest_path,subject,tests) if not p.is_file()]
        if missing:
            record['error']='missing files: '+', '.join(missing); records.append(record); continue
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        record['title']=manifest.get('title',d.name)
        for p in (manifest_path,subject,tests): record['artifact_hashes'][p.name]=sha(p.read_bytes())
        env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONHASHSEED']='0'
        start=datetime.datetime.now(datetime.timezone.utc)
        import time; t=time.monotonic()
        try:
            proc=subprocess.run([sys.executable,'-m','unittest','discover','-s','.', '-p','test_fixture.py','-v'],cwd=d,env=env,text=True,capture_output=True,timeout=args.timeout)
            record['exit_code']=proc.returncode; record['stdout']=proc.stdout[-12000:]; record['stderr']=proc.stderr[-12000:]
            record['artifact_hashes']['stdout.txt']=sha(proc.stdout.encode())
            record['artifact_hashes']['stderr.txt']=sha(proc.stderr.encode())
            record['status']='passed' if proc.returncode==0 else 'failed'
        except subprocess.TimeoutExpired as exc:
            record['exit_code']=124; record['status']='timeout'; record['stdout']=(exc.stdout or '')[-12000:] if isinstance(exc.stdout,str) else ''; record['stderr']=(exc.stderr or '')[-12000:] if isinstance(exc.stderr,str) else ''; record['artifact_hashes']['stdout.txt']=sha(record['stdout'].encode()); record['artifact_hashes']['stderr.txt']=sha(record['stderr'].encode())
        record['duration_ms']=round((time.monotonic()-t)*1000,2)
        record['started_at']=start.isoformat()
        records.append(record)
    report={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runner':'scripts/run_operational_fixtures.py','claim_boundary':'A passing record means only that the deterministic fixture tests passed. It is not an agent-run skill evaluation.','summary':{'total':len(records),'passed':sum(r['status']=='passed' for r in records),'failed':sum(r['status']=='failed' for r in records),'timed_out':sum(r['status']=='timeout' for r in records),'agent_effectiveness':'not evaluated'},'records':records}
    out=Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report['summary'],ensure_ascii=False))
    return 0 if records and report['summary']['passed']==len(records) else 1
if __name__=='__main__': raise SystemExit(main())
