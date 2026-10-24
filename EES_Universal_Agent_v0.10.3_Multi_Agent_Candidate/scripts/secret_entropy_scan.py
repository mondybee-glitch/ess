#!/usr/bin/env python3
"""Conservative local secret scanner; reports paths/lines, never secret values.

Defense-in-depth heuristic only; it does not replace a maintained history scanner.
"""
from __future__ import annotations
import argparse, datetime, json, math, re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKIP_DIRS={'.git','.venv','venv','node_modules','__pycache__','.pytest_cache','.mypy_cache'}
SKIP_SUFFIXES={'.png','.jpg','.jpeg','.gif','.webp','.pdf','.zip','.gz','.sqlite','.db','.pyc','.woff','.woff2','.ttf','.otf','.mp4','.mov','.docx','.xlsx','.pptx'}
ASSIGN=re.compile(r"""(?ix)\b(?P<key>[A-Z0-9_\-]*(?:API[_-]?KEY|ACCESS[_-]?TOKEN|CLIENT[_-]?SECRET|PRIVATE[_-]?KEY|PASSWORD|PASSWD|SECRET|AUTH[_-]?TOKEN|CREDENTIAL)[A-Z0-9_\-]*)\b\s*(?:=|:)\s*['\"`]?\s*(?P<value>[A-Za-z0-9_./+\-=]{16,})""")
KNOWN=[
 ('aws-access-key',re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
 ('github-token',re.compile(r'\bgh[pousr]_[A-Za-z0-9_]{30,}\b')),
 ('gitlab-token',re.compile(r'\bglpat-[A-Za-z0-9_\-]{20,}\b')),
 ('google-api-key',re.compile(r'\bAIza[0-9A-Za-z_\-]{35}\b')),
 ('slack-token',re.compile(r'\bxox[baprs]-[0-9A-Za-z-]{20,}\b')),
 ('stripe-live-secret',re.compile(r'\bsk_live_[0-9A-Za-z]{16,}\b')),
 ('openai-style-secret',re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_\-]{24,}\b')),
 ('private-key-header',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
 ('credential-url',re.compile(r'://[^/\s:@]{1,64}:[^/\s@]{8,}@')),
]
def entropy(s:str)->float:
    if not s:return 0.0
    n=len(s)
    return -sum((count/n)*math.log2(count/n) for count in Counter(s).values())
def iter_files():
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts): continue
        if p.suffix.lower() in SKIP_SUFFIXES or p.stat().st_size > 2_000_000: continue
        try: data=p.read_bytes()
        except OSError: continue
        if b'\x00' in data[:4096]: continue
        try: text=data.decode('utf-8')
        except UnicodeDecodeError: continue
        yield p,text
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default='reports/secret-entropy-scan-latest.json'); a=ap.parse_args()
    findings=[]; scanned=0
    for path,content in iter_files():
        scanned+=1; rel=str(path.relative_to(ROOT))
        for lineno,line in enumerate(content.splitlines(),1):
            matched=False
            for kind,pat in KNOWN:
                if pat.search(line): findings.append({'path':rel,'line':lineno,'kind':kind,'confidence':'high'}); matched=True; break
            if matched: continue
            for m in ASSIGN.finditer(line):
                value=m.group('value').rstrip('.,;:')
                e=entropy(value)
                if len(value)>=20 and e>=3.5 and not re.fullmatch(r'[0-9a-fA-F]{32,}',value):
                    findings.append({'path':rel,'line':lineno,'kind':'sensitive-assignment-high-entropy','confidence':'review','length':len(value),'shannon_entropy_bits_per_char':round(e,3)}); matched=True; break
    unique={(x['path'],x['line'],x['kind']):x for x in findings}
    findings=sorted(unique.values(),key=lambda x:(x['path'],x['line'],x['kind']))
    report={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scanner':'scripts/secret_entropy_scan.py','files_scanned':scanned,'finding_count':len(findings),'status':'review_required' if findings else 'no_findings_by_heuristic','findings':findings,'limitations':['Heuristic detection can produce false positives and false negatives.','No candidate secret values are copied into this report.','Run a maintained repository-history scanner and independent security review before GA.']}
    out=(ROOT/a.output).resolve(); out.relative_to(ROOT.resolve()); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'files_scanned':scanned,'finding_count':len(findings),'status':report['status']}))
    print(f'Report: {out.relative_to(ROOT)}')
    return 1 if findings else 0
if __name__=='__main__': raise SystemExit(main())
