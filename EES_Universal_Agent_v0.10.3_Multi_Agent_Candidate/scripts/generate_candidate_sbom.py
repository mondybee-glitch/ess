#!/usr/bin/env python3
"""Emit a CycloneDX manifest-level SBOM candidate when full resolution is unavailable.

This report is explicitly PARTIAL until a package-manager lockfile and resolved
Python environment are available. Do not treat it as a release-grade transitive SBOM.
"""
from __future__ import annotations
import datetime, hashlib, json, re, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def parse_requirements(path:Path):
    items=[]
    if not path.exists(): return items
    for raw in path.read_text(encoding='utf-8').splitlines():
        line=raw.split('#',1)[0].strip()
        if not line or line.startswith(('-','--','git+','http:','https:','-e ')): continue
        m=re.match(r'^([A-Za-z0-9_.-]+)\s*(.*)$',line)
        if not m: continue
        name=re.sub(r'[-_.]+','-',m.group(1)).lower()
        items.append({'name':name,'constraint':m.group(2).strip() or 'unspecified'})
    return items
def main():
    manifest=json.loads((ROOT/'package-manifest.json').read_text(encoding='utf-8'))
    node=json.loads((ROOT/'operational-fixtures/playwright-ui-state/package.json').read_text(encoding='utf-8'))
    components=[]
    seen=set()
    for entry in parse_requirements(ROOT/'requirements-test.txt')+parse_requirements(ROOT/'requirements-gemini.txt'):
        ref='pkg:pypi/'+entry['name']
        if ref in seen: continue
        seen.add(ref)
        components.append({'type':'library','name':entry['name'],'purl':ref,'bom-ref':ref,'properties':[{'name':'ees:declaredVersionConstraint','value':entry['constraint']},{'name':'ees:resolutionStatus','value':'unresolved-transitive-dependency-graph'}]})
    for name,version in sorted(node.get('devDependencies',{}).items()):
        encoded=name.replace('@','%40',1) if name.startswith('@') else name
        purl=f'pkg:npm/{encoded}@{version}'
        components.append({'type':'library','name':name,'version':version,'purl':purl,'bom-ref':purl,'properties':[{'name':'ees:declaredVersionConstraint','value':version},{'name':'ees:resolutionStatus','value':'exact-direct-dependency-only'}]})
    root_ref=f"pkg:generic/ees-gemini@{manifest.get('version','0.0.0')}"
    payload={'bomFormat':'CycloneDX','specVersion':'1.6','version':1,'metadata':{'component':{'type':'application','name':'EES Gemini','version':manifest.get('version','0.0.0'),'bom-ref':root_ref,'properties':[{'name':'ees:releaseStatus','value':'candidate-not-production-approved'}]},'properties':[{'name':'ees:completeness','value':'PARTIAL'},{'name':'ees:reason','value':'Node package-lock.json is unavailable and Python dependencies are not resolved from a clean environment.'}]},'components':components,'dependencies':[{'ref':root_ref,'dependsOn':[c['bom-ref'] for c in components]}]}
    digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    payload['serialNumber']='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'ees-gemini-sbom:'+digest))
    out=ROOT/'reports/candidate-manifest-sbom.cdx.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    summary={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PARTIAL_NOT_RELEASE_GRADE','artifact':str(out.relative_to(ROOT)),'components':len(components),'python_manifest_entries':sum(c['purl'].startswith('pkg:pypi/') for c in components),'node_manifest_entries':sum(c['purl'].startswith('pkg:npm/') for c in components),'reason':'Transitive dependency graph and resolved Python environment are not available without package resolution.','claim_boundary':'Manifest-level BOM candidate only. Use CycloneDX from resolved clean environments and the npm lockfile for the release SBOM.'}
    (ROOT/'reports/candidate-manifest-sbom-report.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ('status','components','python_manifest_entries','node_manifest_entries','artifact')}))
if __name__=='__main__': main()
