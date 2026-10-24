import json, os, signal, subprocess, sys, threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'scripts'/'task_runtime.py'
def cli(*args):
 command=[sys.executable,str(RUNTIME),*map(str,args)]
 proc=subprocess.Popen(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                       start_new_session=(os.name=="posix"),close_fds=True,
                       env={**os.environ, "EES_REQUIRE_SIGNED_EVIDENCE": "0"})
 try:
  stdout,stderr=proc.communicate(timeout=30)
  return subprocess.CompletedProcess(command,proc.returncode,stdout,stderr)
 except subprocess.TimeoutExpired:
  if os.name=="posix":
   try: os.killpg(proc.pid,signal.SIGKILL)
   except ProcessLookupError: pass
  else: proc.kill()
  stdout,stderr=proc.communicate()
  return subprocess.CompletedProcess(command,124,stdout,(stderr or "")+"\nTimed out after 30s; process group terminated")
def init(out, task_id):
 p=cli('route','--task-id',task_id,'--request','read-only documentation audit','--out-dir',out,'--repo',ROOT,'--acceptance','validation result is evidenced')
 assert p.returncode==0,p.stdout+p.stderr
def test_full_lifecycle_event_ledger_and_release_gate(tmp_path):
 out=tmp_path/'task'; out.mkdir(); init(out,'e2e-001')
 for command in ('plan','start'):
  p=cli(command,'--out-dir',out); assert p.returncode==0,(command,p.stdout,p.stderr)
 p=cli('run-check','--out-dir',out,'--check-id','event-ledger-v072'); assert p.returncode==0,p.stdout+p.stderr
 p=cli('record-criterion','--out-dir',out,'--index','1','--status','pass','--evidence','out:runs/event-ledger-v072.stdout.txt','--note','E2E check passed'); assert p.returncode==0,p.stdout+p.stderr
 p=cli('verify','--out-dir',out); assert p.returncode==0,p.stdout+p.stderr
 state=json.loads((out/'task-state.json').read_text()); assert state['state']=='PASSED'
 events=state['events']; assert len(events)>=4; assert [e['revision'] for e in events]==list(range(1,len(events)+1))
 for i,event in enumerate(events): assert event['previous_hash']==('0'*64 if i==0 else events[i-1]['event_hash'])
 p=cli('release-decision','--out-dir',out); assert p.returncode==0,p.stdout+p.stderr
 assert json.loads((out/'release-decision.json').read_text())['decision']=='Go'
def test_invalid_transition_fails_closed_without_corrupting_ledger(tmp_path):
 out=tmp_path/'task'; out.mkdir(); init(out,'e2e-bad')
 before=json.loads((out/'task-state.json').read_text())
 p=cli('verify','--out-dir',out); assert p.returncode!=0,'verify must reject a task that has not started'
 after=json.loads((out/'task-state.json').read_text()); assert after['state']==before['state']; assert len(after['events'])==len(before['events'])
def test_concurrent_status_reads_are_consistent(tmp_path):
 out=tmp_path/'task'; out.mkdir(); init(out,'e2e-race')
 results=[]
 def read(): results.append(cli('status','--out-dir',out))
 threads=[threading.Thread(target=read) for _ in range(8)]
 [t.start() for t in threads]; [t.join() for t in threads]
 assert all(x.returncode==0 for x in results),[(x.stdout,x.stderr) for x in results]
 states=[json.loads(x.stdout).get('state') for x in results]; assert len(set(states))==1,states
