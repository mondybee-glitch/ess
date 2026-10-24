import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_grader_requires_complete_evidence_backed_criteria():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); run=td/'run.json'; grades=td/'grades.json'; out=td/'graded.json'
        run.write_text(json.dumps({'records':[{'skill':'demo','case_id':'d-1','success_criteria':['criterion A','criterion B']}]}))
        grades.write_text(json.dumps({'grader':'independent-reviewer','grades':[{'skill':'demo','case_id':'d-1','criteria':[
          {'criterion':'criterion A','verdict':'pass','evidence_ref':'artifact:a.txt','reason':'File confirms requirement'},
          {'criterion':'criterion B','verdict':'unknown','evidence_ref':'command:1','reason':'No conclusive evidence'}]}]}))
        p=subprocess.run([sys.executable,str(ROOT/'scripts/grade_agent_evals.py'),'--run',str(run),'--grades',str(grades),'--output',str(out)],text=True,capture_output=True,timeout=10)
        assert p.returncode==0,p.stdout+p.stderr
        data=json.loads(out.read_text())
        assert data['status']=='structurally_valid'
        assert data['summary']['criteria_pass']==1 and data['summary']['criteria_unknown']==1
        assert data['summary']['case_quality_passed']==0

def test_grader_rejects_missing_criterion():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); run=td/'run.json'; grades=td/'grades.json'; out=td/'graded.json'
        run.write_text(json.dumps({'records':[{'skill':'demo','case_id':'d-1','success_criteria':['criterion A','criterion B']}]}))
        grades.write_text(json.dumps({'grader':'reviewer','grades':[{'skill':'demo','case_id':'d-1','criteria':[{'criterion':'criterion A','verdict':'pass','evidence_ref':'x','reason':'supported'}]}]}))
        p=subprocess.run([sys.executable,str(ROOT/'scripts/grade_agent_evals.py'),'--run',str(run),'--grades',str(grades),'--output',str(out)],text=True,capture_output=True,timeout=10)
        assert p.returncode==1
        assert 'missing criterion grades' in out.read_text()
