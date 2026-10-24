#!/usr/bin/env python3
"""Audit capability-to-skill links, dependency references, and critical handoffs."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CRITICAL={'agent-skill-security-intake','ai-agents-rag-mcp','api-integrations','machine-learning-evaluation','mobile-desktop-development','multi-agent-orchestration','backend-integration-testing','backend-production-readiness','backend-reliability-recovery','database-engineering','async-jobs-messaging','backend-auth-authorization','backend-observability'}
REQUIRED_HANDOFFS={
 'agent-skill-security-intake':{'security-review'},
 'ai-agents-rag-mcp':{'security-review','software-testing'},
 'api-integrations':{'backend-development','security-review'},
 'machine-learning-evaluation':{'data-engineering-analytics'},
 'mobile-desktop-development':{'security-review','devops-and-deployment'},
 'backend-integration-testing':{'software-testing'},
 'backend-production-readiness':{'software-testing','security-review','backend-reliability-recovery'},
 'database-engineering':{'backend-reliability-recovery'},
 'async-jobs-messaging':{'backend-reliability-recovery','backend-observability'},
}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',default='reports/routing-audit.json'); a=ap.parse_args()
 reg=json.loads((ROOT/'capability-registry.json').read_text()); caps={x['id']:x for x in reg['capabilities']}; findings=[]
 for sid,c in caps.items():
  skill=ROOT/c.get('skill_path',''); evalp=ROOT/c.get('eval_spec','')
  if not skill.is_file(): findings.append({'severity':'error','skill':sid,'issue':'missing_skill_path','path':c.get('skill_path')})
  if not evalp.is_file(): findings.append({'severity':'error','skill':sid,'issue':'missing_eval_spec','path':c.get('eval_spec')})
  for field in ('dependencies','must_run_with','must_run_before','must_run_after','conflicts_with'):
   for ref in c.get(field,[]) or []:
    if ref not in caps: findings.append({'severity':'error','skill':sid,'issue':'unknown_reference','field':field,'reference':ref})
  if sid in CRITICAL and 'pre_flight_checks' not in c and not c.get('preflight_checks'):
   findings.append({'severity':'warning','skill':sid,'issue':'missing_explicit_preflight_checks'})
  missing=REQUIRED_HANDOFFS.get(sid,set())-set(c.get('must_run_with',[]) or [])
  for ref in sorted(missing): findings.append({'severity':'warning','skill':sid,'issue':'recommended_handoff_missing','reference':ref})
  fdir=c.get('fixtures_dir'); fsrc=c.get('fixture_source')
  if fdir and not (ROOT/fdir).is_dir(): findings.append({'severity':'error','skill':sid,'issue':'fixtures_dir_missing','path':fdir})
  if fsrc and not (ROOT/fsrc).is_file(): findings.append({'severity':'error','skill':sid,'issue':'fixture_source_missing','path':fsrc})
  if not fdir and not fsrc: findings.append({'severity':'error','skill':sid,'issue':'no_fixture_location'})
 out={'schema_version':1,'scope':'static routing and path audit; does not establish that routing produces correct task outcomes','capabilities':len(caps),'findings':findings,'summary':{'errors':sum(x['severity']=='error' for x in findings),'warnings':sum(x['severity']=='warning' for x in findings),'status':'passed' if not any(x['severity']=='error' for x in findings) else 'failed'}}
 path=Path(a.output).expanduser().resolve()
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out['summary']))
 return 0 if out['summary']['status']=='passed' else 1
if __name__=='__main__': raise SystemExit(main())
