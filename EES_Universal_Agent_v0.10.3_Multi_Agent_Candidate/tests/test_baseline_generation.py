import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_source_of_truth_baseline_reports_actual_counts_and_hashes():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'baseline.json'
        p=subprocess.run([sys.executable,str(ROOT/'scripts/generate_baseline.py'),'--output',str(out)],cwd=ROOT,text=True,capture_output=True,timeout=10)
        assert p.returncode==0,p.stdout+p.stderr
        data=json.loads(out.read_text())
        assert data['status']=='consistent'
        assert data['counts']['skills_with_skill_md']==32
        assert data['counts']['capabilities']==74
        assert data['counts']['evaluation_contracts']==222
        assert data['counts']['success_criteria_missing']==0
        assert len(data['artifact_hashes'])>=100
        assert len(data['artifact_hashes']['capability-registry.json'])==64
