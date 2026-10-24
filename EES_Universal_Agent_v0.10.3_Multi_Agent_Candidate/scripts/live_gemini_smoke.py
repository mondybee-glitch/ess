#!/usr/bin/env python3
"""Low-cost live Gemini API smoke test; never writes the API key or raw response.

Set GEMINI_API_KEY and optionally EES_GEMINI_MODEL. A PASS proves only that one
small JSON-generation request completed for that model/key at this point in time.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_MODEL='gemini-3.8-flash'
def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default='reports/live-gemini-smoke-latest.json')
    a=ap.parse_args()
    key=os.getenv('GEMINI_API_KEY')
    model=os.getenv('EES_GEMINI_MODEL',DEFAULT_MODEL).strip() or DEFAULT_MODEL
    report={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'blocked','model':model,'scope':'single low-token API connectivity/structured-response smoke test; not an agent-quality evaluation','response_text_logged':False}
    if not key:
        report['reason']='GEMINI_API_KEY is not configured; live verification was not run.'
        rc=2
    else:
        start=time.monotonic()
        try:
            from google import genai
            from google.genai import types
            client=genai.Client(api_key=key)
            nonce='ees-live-smoke-v1'
            response=client.models.generate_content(
                model=model,
                contents=f'Return exactly one JSON object with keys status and nonce. Set status to "ok" and nonce to "{nonce}". Do not include markdown or other text.',
                config=types.GenerateContentConfig(temperature=0,response_mime_type='application/json',max_output_tokens=64),
            )
            raw=(getattr(response,'text',None) or '').strip()
            data=json.loads(raw)
            if not isinstance(data,dict) or data.get('status')!='ok' or data.get('nonce')!=nonce:
                raise ValueError('structured response contract did not match')
            report['status']='passed'; report['duration_ms']=round((time.monotonic()-start)*1000,2)
            report['response_sha256']=hashlib.sha256(raw.encode()).hexdigest()
            usage=getattr(response,'usage_metadata',None)
            if usage is not None:
                for key_name,attr in [('prompt_tokens','prompt_token_count'),('candidate_tokens','candidates_token_count'),('total_tokens','total_token_count')]:
                    value=getattr(usage,attr,None)
                    if value is not None: report[key_name]=value
            rc=0
        except Exception as exc:
            report['status']='failed'; report['duration_ms']=round((time.monotonic()-start)*1000,2)
            report['error_type']=type(exc).__name__
            report['reason']='Request failed or response did not match the smoke-test contract; sensitive exception details are omitted.'
            rc=1
    out=(ROOT/a.output).resolve()
    try:
        out.relative_to(ROOT.resolve())
    except ValueError:
        print('output path must remain inside project root',file=sys.stderr); return 2
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','model','scope') if k in report},ensure_ascii=False))
    print(f'Report: {out.relative_to(ROOT)}')
    return rc
if __name__=='__main__': raise SystemExit(main())
