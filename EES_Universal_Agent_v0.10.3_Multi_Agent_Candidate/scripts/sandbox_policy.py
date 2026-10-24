"""Risk-tiered, fail-closed sandbox policy planner for EES tasks."""
import argparse,json
from pathlib import Path

PROFILES={
 'low': {'network':'none','read_only_root':True,'read_only_workspace':False,'memory':'512m','cpus':'1','pids':64,'timeout_seconds':120,'capabilities':'drop-all','no_new_privileges':True,'tmpfs':'32m'},
 'medium': {'network':'none','read_only_root':True,'read_only_workspace':False,'memory':'1g','cpus':'2','pids':128,'timeout_seconds':300,'capabilities':'drop-all','no_new_privileges':True,'tmpfs':'64m'},
 'high': {'network':'none','read_only_root':True,'read_only_workspace':True,'memory':'2g','cpus':'2','pids':128,'timeout_seconds':180,'capabilities':'drop-all','no_new_privileges':True,'tmpfs':'64m'}
}
def policy(risk,network_requested=False,secret_access=False):
 if risk not in PROFILES: raise ValueError('unknown risk tier; refusing permissive defaults')
 p=dict(PROFILES[risk]); p['risk_tier']=risk
 if network_requested: p['blocked_reason']='network access is denied by default; explicit reviewed policy is required'
 if secret_access: p['blocked_reason']='secrets are not mounted into untrusted task sandboxes'
 p['allowed']=not network_requested and not secret_access
 return p
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--risk',choices=PROFILES,required=True); ap.add_argument('--network-requested',action='store_true'); ap.add_argument('--secret-access',action='store_true'); ap.add_argument('--output'); a=ap.parse_args(); d=policy(a.risk,a.network_requested,a.secret_access); s=json.dumps(d,indent=2); print(s)
 if a.output: Path(a.output).write_text(s+'\n')
 return 0 if d['allowed'] else 3
if __name__=='__main__': raise SystemExit(main())
