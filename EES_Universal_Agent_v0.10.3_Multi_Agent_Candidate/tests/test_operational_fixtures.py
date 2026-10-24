import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_operational_fixture_projects_execute_and_emit_hashes():
    proc=subprocess.run([sys.executable,'scripts/run_operational_fixtures.py','--output','reports/test-operational-fixtures.json'],cwd=ROOT,text=True,capture_output=True,timeout=90)
    assert proc.returncode==0,proc.stdout+proc.stderr
    report=json.loads((ROOT/'reports/test-operational-fixtures.json').read_text())
    expected = sum(1 for d in (ROOT/'operational-fixtures').iterdir() if d.is_dir() and (d/'subject.py').is_file())
    assert report['summary']=={'total':expected,'passed':expected,'failed':0,'timed_out':0,'agent_effectiveness':'not evaluated'}
    assert all(r['exit_code']==0 and len(r['artifact_hashes'])==5 for r in report['records'])
    (ROOT/'reports/test-operational-fixtures.json').unlink()
def test_routing_audit_is_explicit_about_warnings():
    proc=subprocess.run([sys.executable,'scripts/audit_routing.py','--output','reports/test-routing-audit.json'],cwd=ROOT,text=True,capture_output=True,timeout=30)
    assert proc.returncode==0,proc.stdout+proc.stderr
    report=json.loads((ROOT/'reports/test-routing-audit.json').read_text())
    assert report['capabilities']==74
    assert report['summary']['errors']==0
    assert report['summary']['warnings']==0
    assert report['summary']['status']=='passed'
    assert 'does not establish' in report['scope']
    (ROOT/'reports/test-routing-audit.json').unlink()
