#!/usr/bin/env python3
"""Validate independent criterion-level grading for an agent evaluation report.

Adjudication is a separate input artifact. The tool rejects missing graders,
missing evidence locators, invalid verdicts, and criterion counts that do not map
to the source case. It validates the grading record structure, not the grader's judgment.
"""
import argparse, datetime, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VALID={'pass','fail','unknown'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--run',required=True,help='Agent eval JSON report')
 ap.add_argument('--grades',required=True,help='Independent grading JSON file')
 ap.add_argument('--output',default='reports/agent-eval-grading.json')
 a=ap.parse_args()
 rp=Path(a.run); gp=Path(a.grades)
 if not rp.is_absolute(): rp=ROOT/rp
 if not gp.is_absolute(): gp=ROOT/gp
 try: run=json.loads(rp.read_text()); grades=json.loads(gp.read_text())
 except (OSError,json.JSONDecodeError) as e: print(f'Cannot read input: {e}',file=sys.stderr); return 2
 source={(r.get('skill'),r.get('case_id')):r for r in run.get('records',[])}
 grader=str(grades.get('grader','')).strip(); entries=grades.get('grades')
 errors=[]; normalized=[]
 if not grader: errors.append('grader identity is required')
 if not isinstance(entries,list): errors.append('grades must be an array'); entries=[]
 seen=set()
 for g in entries:
  key=(g.get('skill'),g.get('case_id')) if isinstance(g,dict) else (None,None)
  if key not in source: errors.append(f'unknown case {key}'); continue
  if key in seen: errors.append(f'duplicate grade {key}'); continue
  seen.add(key); source_case=source[key]
  criteria=g.get('criteria')
  if not isinstance(criteria,list) or not criteria: errors.append(f'{key}: criteria must be a non-empty array'); continue
  required=source_case.get('success_criteria')
  if isinstance(required,str): required=[required]
  if not isinstance(required,list): required=[]
  bycriterion={str(x.get('criterion')):x for x in criteria if isinstance(x,dict)}
  missing=[str(c) for c in required if str(c) not in bycriterion]
  if missing: errors.append(f'{key}: missing criterion grades: {missing}')
  for c in criteria:
   if not isinstance(c,dict): errors.append(f'{key}: criterion entry must be an object'); continue
   if c.get('verdict') not in VALID: errors.append(f'{key}: invalid verdict for {c.get("criterion")}'); continue
   if not str(c.get('evidence_ref','')).strip(): errors.append(f'{key}: evidence_ref required for {c.get("criterion")}')
   if not str(c.get('reason','')).strip(): errors.append(f'{key}: reason required for {c.get("criterion")}')
  normalized.append({'skill':key[0],'case_id':key[1],'criteria':criteria,'reviewer_notes':g.get('reviewer_notes','')})
 if not seen: errors.append('no valid case grades supplied')
 failed=sum(c.get('verdict')=='fail' for g in normalized for c in g['criteria'] if isinstance(c,dict))
 unknown=sum(c.get('verdict')=='unknown' for g in normalized for c in g['criteria'] if isinstance(c,dict))
 passed=sum(c.get('verdict')=='pass' for g in normalized for c in g['criteria'] if isinstance(c,dict))
 result={'schema_version':1,'run_report':str(rp),'run_report_sha256':sha(rp),'grade_input':str(gp),'grade_input_sha256':sha(gp),
  'graded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'grader':grader,'status':'structurally_valid' if not errors else 'invalid',
  'summary':{'cases_graded':len(normalized),'criteria_pass':passed,'criteria_fail':failed,'criteria_unknown':unknown,
   'case_quality_passed':sum(bool(g['criteria']) and all(c.get('verdict')=='pass' for c in g['criteria']) for g in normalized),
   'case_quality_failed':sum(any(c.get('verdict')=='fail' for c in g['criteria']) for g in normalized)},
  'grades':normalized,'errors':errors,
  'boundary':'Structural validity does not prove reviewer independence or correctness; audit the cited artifacts and grader.'}
 out=Path(a.output); out=out if out.is_absolute() else ROOT/out; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'status':result['status'],'errors':len(errors),'summary':result['summary']},ensure_ascii=False))
 return 0 if not errors else 1
if __name__=='__main__': sys.exit(main())
