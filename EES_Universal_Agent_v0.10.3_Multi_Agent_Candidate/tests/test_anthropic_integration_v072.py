#!/usr/bin/env python3
"""Regression checks for the selective Anthropic Agent Skills integration."""
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    manifest=json.loads((ROOT/'package-manifest.json').read_text(encoding='utf-8'))
    registry=json.loads((ROOT/'capability-registry.json').read_text(encoding='utf-8'))
    ids={c['id'] for c in registry['capabilities']}
    assert manifest['version']=='0.7.6'
    assert manifest['skill_count']==74 and len(manifest['skills'])==74
    assert ids==set(manifest['skills'])
    assert {'web-artifacts-builder','brand-guidelines'} <= ids
    assert 'multi-component' in (ROOT/'skills/web-artifacts-builder/SKILL.md').read_text(encoding='utf-8').lower()
    assert 'only when the user explicitly requests' in (ROOT/'skills/brand-guidelines/SKILL.md').read_text(encoding='utf-8').lower()
    creator=(ROOT/'skills/skill-creation-and-evaluation/SKILL.md').read_text(encoding='utf-8').lower()
    for term in ('positive examples','near-miss','progressive disclosure','baseline','unverified','failure category'):
        assert term in creator, f'skill-creator adaptation missing: {term}'
    mcp=(ROOT/'skills/mcp-server-engineering/SKILL.md').read_text(encoding='utf-8').lower()
    for term in ('input schema','authorization','pagination','timeout','client','untrusted'):
        assert term in mcp, f'MCP workflow missing: {term}'
    browser=(ROOT/'skills/browser-e2e-and-test-diagnostics/UPSTREAM-PATTERNS.md').read_text(encoding='utf-8').lower()
    for term in ('rendered-state reconnaissance','web-first assertions','redact','cleanup'):
        assert term in browser, f'web testing adaptation missing: {term}'
    design=(ROOT/'skills/ui-ux-design/DISTINCTIVE-DESIGN-REVIEW.md').read_text(encoding='utf-8').lower()
    for term in ('actual brief','generic','reduced-motion','rtl'):
        assert term in design, f'design adaptation missing: {term}'
    provenance=(ROOT/'references/anthropic-agent-skills-integration.md').read_text(encoding='utf-8').lower()
    notices=(ROOT/'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8').lower()
    for item in ('skill-creator','webapp-testing','frontend-design','mcp-builder'):
        assert item in provenance and item in notices, f'provenance missing upstream skill {item}'
    assert 'not copy' in provenance or 'no upstream' in provenance
    # Route actual prompts through the package CLI: a source note alone is insufficient.
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); repo=base/'repo'; repo.mkdir(); (repo/'README.md').write_text('test repository\n',encoding='utf-8')
        def route(request, name):
            out=base/name
            result=subprocess.run([sys.executable,str(ROOT/'scripts/task_runtime.py'),'route','--task-id',name,'--request',request,'--repo',str(repo),'--out-dir',str(out),'--acceptance','route decision is evidenced'],cwd=ROOT,text=True,capture_output=True,timeout=30)
            assert result.returncode==0,result.stdout+result.stderr
            return json.loads((out/'route-decision.json').read_text(encoding='utf-8'))['selected_skills']
        assert 'skill-creation-and-evaluation' in route('Create a skill and evaluate the skill with benchmark skill cases and a grading rubric','skill-positive')
        assert 'mcp-server-engineering' in route('Implement an MCP server using FastMCP with MCP tool schema and pagination tests','mcp-positive')
        assert 'mcp-server-engineering' not in route('Show me MCP client configuration only; do not implement a server','mcp-near-miss')
    for sid in ('skill-creation-and-evaluation','mcp-server-engineering'):
        spec=json.loads((ROOT/f'skills/{sid}/evals/evals.json').read_text(encoding='utf-8'))
        assert len(spec['cases'])==3
        assert all(c['status']=='defined-not-run' and c['agent_status']=='not-run' for c in spec['cases'])
        assert all((ROOT/c['fixture']).is_file() for c in spec['cases'])
        assert len({c['input']['request'] for c in spec['cases']})==3
    print('PASS: upstream patterns selectively adapted; provenance and six evaluation contracts checked; no agent effectiveness claimed')

if __name__=='__main__': main()
