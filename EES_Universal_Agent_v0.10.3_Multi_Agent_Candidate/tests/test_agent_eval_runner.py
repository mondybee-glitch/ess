import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_runner_records_execution_without_claiming_quality():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'run.json'
        cmd=[sys.executable,str(ROOT/'scripts/run_agent_evals.py'),
             '--command',f'{sys.executable} {ROOT / "tests/fake_eval_adapter.py"}',
             '--skill','backend-development','--case','be-01','--timeout','20','--output',str(out)]
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=30)
        assert p.returncode==0, p.stdout+p.stderr
        data=json.loads(out.read_text())
        assert data['summary']['total']==1
        assert data['summary']['execution_completed']==1
        assert data['summary']['quality_passed']==0
        rec=data['records'][0]
        assert rec['execution_status']=='completed'
        assert rec['quality_status']=='awaiting_human_review'
        assert rec['agent_status']=='executed_unverified'
        assert rec['artifact_manifest'][0]['status']=='present'
        assert len(rec['artifact_manifest'][0]['sha256'])==64

def test_runner_timeout_is_not_pass():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'timeout.json'
        code='import time; time.sleep(3)'
        cmd=[sys.executable,str(ROOT/'scripts/run_agent_evals.py'),'--command',f'{sys.executable} -c "{code}"',
             '--skill','backend-development','--case','be-01','--timeout','1','--output',str(out)]
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=10)
        assert p.returncode==1, p.stdout+p.stderr
        data=json.loads(out.read_text())
        assert data['records'][0]['execution_status']=='timeout'
        assert data['summary']['quality_passed']==0
