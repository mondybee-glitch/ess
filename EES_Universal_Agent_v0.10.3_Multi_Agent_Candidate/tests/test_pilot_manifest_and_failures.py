import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_pilot_manifest_is_exactly_15_known_cases():
    from importlib.util import spec_from_file_location, module_from_spec
    spec=spec_from_file_location('ees_runner',ROOT/'scripts/run_agent_evals.py')
    mod=module_from_spec(spec); spec.loader.exec_module(mod)
    cases=mod.load_cases(None,None,None,'docs/archive/pre-v0.9.0/pilot-manifest-v076.json')
    assert len(cases)==15
    assert len({(s,c['id']) for s,c,_ in cases})==15
    assert len({s for s,_,_ in cases})==5
    assert all(c.get('success_criteria') for _,c,_ in cases)

def test_runner_rejects_invalid_json_stdout():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'invalid.json'
        cmd=[sys.executable,str(ROOT/'scripts/run_agent_evals.py'),'--command',f'{sys.executable} {ROOT / "tests/adapter_probe_invalid_output.py"}',
             '--skill','backend-development','--case','be-01','--timeout','10','--output',str(out)]
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=20)
        assert p.returncode==1, p.stdout+p.stderr
        report=json.loads(out.read_text())
        assert report['summary']['invalid_responses']==1
        assert report['summary']['quality_passed']==0
        assert report['records'][0]['quality_status']=='invalid_agent_response'

def test_runner_rejects_path_traversal_artifact_declaration():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'badpath.json'
        cmd=[sys.executable,str(ROOT/'scripts/run_agent_evals.py'),'--command',f'{sys.executable} {ROOT / "tests/adapter_probe_unsafe_path.py"}',
             '--skill','backend-development','--case','be-01','--timeout','10','--output',str(out)]
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=20)
        assert p.returncode==1, p.stdout+p.stderr
        report=json.loads(out.read_text())
        rec=report['records'][0]
        assert rec['quality_status']=='invalid_agent_response'
        assert rec['artifact_manifest'][0]['status']=='rejected_path_outside_workspace'
        assert report['summary']['quality_passed']==0
