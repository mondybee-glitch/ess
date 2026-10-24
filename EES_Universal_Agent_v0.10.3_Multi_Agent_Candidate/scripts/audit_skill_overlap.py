#!/usr/bin/env python3
"""Create a human-review queue for skill-boundary overlaps; never auto-merges skills."""
import argparse, datetime, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# These are deliberately review candidates, not findings of duplication. Pair notes describe
# why a reviewer should compare task boundaries and distinguishable outputs.
CANDIDATES=[
 ("agent-workflow-specification","agent-workflow-orchestration","specification/acceptance criteria versus execution sequencing"),
 ("agent-workflow-orchestration","multi-agent-orchestration","single-workflow coordination versus explicitly multi-agent coordination"),
 ("backend-observability","observability-and-ai-evaluation","service telemetry versus evaluation observability"),
 ("observability-and-ai-evaluation","llm-evaluation-observability","broad AI evaluation observability versus LLM-specific evaluation traces/metrics"),
 ("frontend-development","web-artifacts-builder","general frontend implementation versus interactive artifact construction"),
 ("frontend-quality-and-cross-platform-ui","frontend-build-quality","cross-platform UI quality versus build/lint/typecheck quality"),
 ("ui-design-system-accessibility","accessible-component-behavior","system-level accessibility versus interaction/focus behavior of components"),
 ("ui-design-system-accessibility","react-component-library-engineering","system conventions/accessibility versus reusable React component package engineering"),
 ("api-design-contracts","api-integrations","contract design/versioning versus connecting to external APIs"),
 ("software-testing","backend-integration-testing","general test strategy versus backend service integration tests"),
 ("backend-production-readiness","devops-and-deployment","service release criteria versus deployment/operations implementation"),
 ("machine-learning-evaluation","llm-evaluation-observability","ML model evaluation versus LLM-specific evaluation instrumentation"),
]
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',default='reports/skill-overlap-candidates-v076.json'); a=ap.parse_args()
 reg=json.loads((ROOT/'capability-registry.json').read_text()); caps={x['id']:x for x in reg['capabilities']}; pairs=[]
 for left,right,note in CANDIDATES:
  if left not in caps or right not in caps: raise SystemExit(f'Unknown candidate pair: {left}, {right}')
  pairs.append({'skills':[left,right],'review_reason':note,'status':'review-candidate-not-proven-duplicate',
    'compare':['primary_scope','inputs','outputs','success_criteria','routing_signals','dependencies','pilot outcome'],
    'recommended_next_step':'Two domain reviewers compare at least 6 discriminating cases before merge/split/conflict decisions.'})
 out={'schema_version':1,'package_version':'0.7.6','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'scope':'Manual review queue derived from skill names and declared responsibilities; not a semantic duplicate detector.',
   'candidate_pair_count':len(pairs),'hard_conflicts_approved':sum(bool(c.get('conflicts_with')) for c in caps.values())//2,
   'hard_conflict_policy':reg.get('routing_ownership_policy',{}).get('conflicts_with_semantics'),
   'pairs':pairs,
   'limitation':'No candidate is automatically merged, split, or excluded. Overlapping tasks can legitimately require both specialists.'}
 p=Path(a.output); p=p if p.is_absolute() else ROOT/p; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'candidates':len(pairs),'hard_conflicts_approved':out['hard_conflicts_approved'],'output':str(p)}))
 return 0
if __name__=='__main__': raise SystemExit(main())
