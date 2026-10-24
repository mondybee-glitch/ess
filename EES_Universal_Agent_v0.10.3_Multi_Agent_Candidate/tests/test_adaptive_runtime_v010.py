import hashlib, hmac, importlib.util, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_sandbox_policy_fail_closed():
 m=load('sandbox_policy','scripts/sandbox_policy.py')
 assert m.policy('high')['network']=='none'
 assert m.policy('high')['read_only_workspace'] is True
 assert m.policy('high',network_requested=True)['allowed'] is False
 assert m.policy('high',secret_access=True)['allowed'] is False

def test_router_cache_is_content_addressed_and_invalidatable(tmp_path,monkeypatch):
 m=load('router_cache','scripts/hierarchical_router_cache.py'); monkeypatch.setattr(m,'CACHE',tmp_path/'cache.json')
 a=m.select('Need frontend UI design and React component quality',ttl=30)
 b=m.select('Need frontend UI design and React component quality',ttl=30)
 assert a['cache']=='MISS' and b['cache']=='HIT' and a['route']['id']==b['route']['id']
 assert m.invalidate() is True
 assert m.select('Need frontend UI design and React component quality')['cache']=='MISS'

def test_router_cache_rejects_tampered_route(tmp_path,monkeypatch):
 m=load('router_cache_tamper','scripts/hierarchical_router_cache.py'); monkeypatch.setattr(m,'CACHE',tmp_path/'cache.json')
 first=m.select('frontend react'); data=json.loads(m.CACHE.read_text()); key=first['cache_key']
 data['entries'][key]['route']={'id':'attacker-route','name':'Unsafe route','skills':[]}
 m.CACHE.write_text(json.dumps(data))
 second=m.select('frontend react')
 assert second['cache']=='MISS' and second['route']['id']!='attacker-route'

def signed_report(iid,rule,baseline,holdout,key):
 report={'candidate_id':iid,'rule_sha256':hashlib.sha256(rule.encode()).hexdigest(),'dataset_id':'holdout-v1','runner_id':'trusted-ci-runner','status':'PASS','failed':0,'holdout_passed':True,'baseline_score':baseline,'holdout_score':holdout}
 report['hmac_sha256']=hmac.new(key.encode(),json.dumps(report,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode(),hashlib.sha256).hexdigest()
 return report

def test_learning_instinct_requires_signed_holdout_and_regression(tmp_path):
 store=tmp_path/'instincts.json'; key='test-only-secret-key-32-characters-minimum'; env=dict(os.environ,EES_INSTINCT_STORE=str(store),EES_LEARNING_REPORT_HMAC_KEY=key)
 def run(*args): return subprocess.run([sys.executable,str(ROOT/'scripts/learning_governor.py'),*args],capture_output=True,text=True,env=env)
 p=run('propose','--name','candidate-rule','--rule','Prefer reproducible checks'); assert p.returncode==0,p.stderr
 item=json.loads(p.stdout); iid=item['id']; rule=item['rule']
 assert run('promote','--id',iid).returncode!=0
 report=tmp_path/'regression.json'; report.write_text(json.dumps({'status':'PASS','failed':0,'holdout_passed':True}))
 unsigned=run('evaluate','--id',iid,'--baseline','0.90','--holdout','0.91','--regression-report',str(report))
 assert unsigned.returncode!=0
 report.write_text(json.dumps(signed_report(iid,rule,0.90,0.91,key)))
 ev=run('evaluate','--id',iid,'--baseline','0.90','--holdout','0.91','--regression-report',str(report)); assert ev.returncode==0,ev.stderr
 assert run('promote','--id',iid).returncode==0
 state=json.loads(store.read_text()); assert next(x for x in state['instincts'] if x['id']==iid)['status']=='ACTIVE'
 assert all(e['hash'] for e in state['events'])

def test_learning_governor_rejects_out_of_range_scores_and_tampered_ledger(tmp_path):
 store=tmp_path/'instincts.json'; key='test-only-secret-key-32-characters-minimum'; env=dict(os.environ,EES_INSTINCT_STORE=str(store),EES_LEARNING_REPORT_HMAC_KEY=key)
 def run(*args): return subprocess.run([sys.executable,str(ROOT/'scripts/learning_governor.py'),*args],capture_output=True,text=True,env=env)
 p=run('propose','--name','guarded-rule','--rule','Require independent holdout'); assert p.returncode==0,p.stderr
 iid=json.loads(p.stdout)['id']
 report=tmp_path/'regression.json'; report.write_text('{}')
 bad=run('evaluate','--id',iid,'--baseline','1.4','--holdout','0.9','--regression-report',str(report))
 assert bad.returncode!=0 and 'within [0, 1]' in bad.stderr
 data=json.loads(store.read_text()); data['events'][0]['payload']['name']='tampered'; store.write_text(json.dumps(data))
 listed=run('list'); assert listed.returncode!=0 and ('hash mismatch' in listed.stderr or 'chain broken' in listed.stderr)

def test_router_cache_does_not_persist_raw_task_text(tmp_path,monkeypatch):
 m=load('router_cache_privacy','scripts/hierarchical_router_cache.py'); monkeypatch.setattr(m,'CACHE',tmp_path/'cache.json')
 sentinel='PRIVATE_TASK_SENTINEL_7f23'; m.select('frontend react '+sentinel)
 persisted=(tmp_path/'cache.json').read_text(); assert sentinel not in persisted
