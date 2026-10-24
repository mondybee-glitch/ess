#!/usr/bin/env python3
"""Deterministic test adapter; not an engineering agent."""
import json, pathlib, sys
payload=json.load(sys.stdin)
pathlib.Path('adapter-artifact.txt').write_text('synthetic test artifact for '+payload['case_id']+'\n',encoding='utf-8')
print(json.dumps({
  'summary':'Synthetic adapter response; does not perform the task.',
  'changed_files':['adapter-artifact.txt'],
  'commands':[{'command':'synthetic-noop','exit_code':0,'stdout':'synthetic only','stderr':''}],
  'limitations':['This is a test adapter and does not prove task correctness.'],
  'evidence':[{'criterion':str(payload.get('success_criteria')),'artifact':'adapter-artifact.txt','detail':'synthetic test evidence only'}]
}))
