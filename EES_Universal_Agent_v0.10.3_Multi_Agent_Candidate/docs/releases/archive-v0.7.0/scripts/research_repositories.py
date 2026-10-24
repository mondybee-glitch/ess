#!/usr/bin/env python3
import json, urllib.request, urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
repos=['magnus919/agent-skills','vercel/next.js','FlowiseAI/Flowise','refinedev/refine','payloadcms/payload','ColorlibHQ/AdminLTE','tailwindlabs/tailwindcss','shadcn-ui/ui','coreui/coreui-free-bootstrap-admin-template','ColorlibHQ/gentelella','immich-app/immich','tauri-apps/tauri','ClickHouse/ClickHouse','binhnguyennus/awesome-scalability','karanpratapsingh/system-design','donnemartin/system-design-primer','morluto/rea','Snailclimb/JavaGuide','krahets/hello-algo','Chalarangelo/30-seconds-of-code','freeCodeCamp/freeCodeCamp','github/spec-kit','tt-a1i/archify','DeusData/codebase-memory-mcp','cloudflare/security-audit-skill','router-for-me/CLIProxyAPI','n8n-io/n8n','D4Vinci/Scrapling','f/prompts.chat']
# Decisions are bounded by scope: only backend-relevant sources become extensions; UI/education sources remain reference-only.
backend={'magnus919/agent-skills':'extend existing skill','vercel/next.js':'reference-only','FlowiseAI/Flowise':'reference-only','ClickHouse/ClickHouse':'extend existing skill','github/spec-kit':'extend existing skill','DeusData/codebase-memory-mcp':'extend existing skill','cloudflare/security-audit-skill':'extend existing skill','n8n-io/n8n':'reference-only','D4Vinci/Scrapling':'reference-only','router-for-me/CLIProxyAPI':'deferred'}
rows=[]
for full in repos:
    url='https://api.github.com/repos/'+full
    req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'elite-engineering-suite-v0.7.0'})
    try:
        with urllib.request.urlopen(req,timeout=15) as res: x=json.load(res)
        lic=(x.get('license') or {}).get('spdx_id') if isinstance(x.get('license'),dict) else None
        decision=backend.get(full,'reference-only')
        rows.append({'repository':full,'url':'https://github.com/'+full,'default_branch':x.get('default_branch'),'archived':x.get('archived'),'license':lic or 'not-detected','pushed_at':x.get('pushed_at'),'updated_at':x.get('updated_at'),'last_checked':'2026-10-23','decision':decision,'principle':{'extend existing skill':'adapt a bounded operational principle without copying upstream text','reference-only':'use as comparative reference only; no dependency or copied assets','deferred':'do not integrate until a separate security and compatibility review'}[decision],'limitations':'Metadata, README/license and selected files only; this is not a full audit, quality proof, or legal opinion.'})
    except Exception as e:
        rows.append({'repository':full,'url':'https://github.com/'+full,'last_checked':'2026-10-23','decision':'deferred','error':str(e),'limitations':'Source could not be verified in this run; no integration claim.'})
(ROOT/'reports'/'repository-metadata-v070.json').write_text(json.dumps({'source':'GitHub REST repository metadata','checked_at':'2026-10-23','count':len(rows),'rows':rows},indent=2)+'\n')
lines=['# Repository batch v0.7.0 attribution and boundaries','', 'Checked through GitHub REST repository metadata. The API fields include default branch, archived status, timestamps, and detected license; a detected license is not legal advice and does not cover dependencies or assets. This is not a full repository audit. No upstream code or prose is copied.','', '| Repository | Decision | License | Archived | Last push | Principle / limits |','|---|---|---|---|---|---|']
for x in rows: lines.append(f"| [{x['repository']}]({x['url']}) | {x['decision']} | {x.get('license','unverified')} | {x.get('archived','unknown')} | {x.get('pushed_at','unknown')} | {x.get('principle','metadata unavailable')}; {x['limitations']} |")
(ROOT/'references'/'repository-batch-v070-attribution.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'count':len(rows),'verified':sum('error' not in x for x in rows),'errors':sum('error' in x for x in rows)},indent=2))
