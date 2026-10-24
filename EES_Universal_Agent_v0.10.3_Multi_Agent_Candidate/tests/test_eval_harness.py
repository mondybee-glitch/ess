import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/'scripts/run_eval.py'

def main():
    out=ROOT/'reports'/'test-harness-report.json'
    out.parent.mkdir(exist_ok=True)
    r=subprocess.run([sys.executable,str(RUNNER),'--output','reports/test-harness-report.json'],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==0, r.stdout+r.stderr
    data=json.loads(out.read_text())
    expected_total=sum(len(json.loads(p.read_text()).get('cases',[])) for p in (ROOT/'skills').glob('*/evals/evals.json'))
    assert data['summary']=={'total':expected_total,'fixture_passed':expected_total,'agent_results':'not run'}
    assert all(x['fixture_status']=='passed' for x in data['records'])
    assert all(x['agent_status']=='unverified' for x in data['records'])
    out.unlink()
    print(f'PASS: {expected_total} fixture checks pass without claiming agent success')

if __name__=='__main__': main()
