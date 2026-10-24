#!/usr/bin/env python3
"""Runtime adversarial/regression tests. They test the local control layer, not agent effectiveness."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, shutil, signal, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT = ROOT / "scripts" / "task_runtime.py"

def run(*args, root=ROOT):
    rt = root / "scripts" / "task_runtime.py"
    command = [sys.executable, str(rt), *map(str, args)]
    # A timed-out CLI may have grandchildren inheriting stdout/stderr. Kill the
    # process group, not only its leader, so pytest cannot hang on open pipes.
    proc = subprocess.Popen(command, cwd=root, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=(os.name == "posix"),
                            close_fds=True, env={**os.environ, "EES_REQUIRE_SIGNED_EVIDENCE": "0"})
    try:
        stdout, stderr = proc.communicate(timeout=30)
        return subprocess.CompletedProcess(command, proc.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        else:
            proc.kill()
        stdout, stderr = proc.communicate()
        return subprocess.CompletedProcess(command, 124, stdout,
            (stderr or "") + "\nTimed out after 30s; process group terminated")

def init(out, repo, task_id="t-low", request="read-only documentation audit", acceptance="validation result is evidenced"):
    r=run("route","--task-id",task_id,"--request",request,"--repo",str(repo),"--out-dir",str(out),"--acceptance",acceptance)
    assert r.returncode==0, r.stdout+r.stderr
    assert run("plan","--out-dir",str(out)).returncode==0

def read_state(out): return json.loads((Path(out)/"task-state.json").read_text())
def write_file(path, content="evidence\n"):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content,encoding="utf-8"); return path

def test_exit_zero_and_acceptance_evidence():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"source.txt")
        init(out,repo)
        r=run("start","--out-dir",str(out)); assert r.returncode==0,r.stderr
        r=run("run-check","--out-dir",str(out),"--check-id","package-validate-v072"); assert r.returncode==0,r.stdout+r.stderr
        r=run("record-criterion","--out-dir",str(out),"--index","1","--status","pass","--evidence","out:runs/package-validate-v072.stdout.txt","--note","package validator completed"); assert r.returncode==0,r.stdout+r.stderr
        r=run("verify","--out-dir",str(out)); assert r.returncode==0,r.stderr
        assert read_state(out)["state"]=="PASSED"
        r=run("release-decision","--out-dir",str(out)); assert r.returncode==0,r.stdout+r.stderr
        assert json.loads((out/"release-decision.json").read_text())["decision"]=="Go"

def test_forged_execution_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        init(out,repo)
        assert run("start","--out-dir",str(out)).returncode==0
        r=run("record-action","--out-dir",str(out),"--action-id","package-validate-v072","--executed","--exit-code","0","--artifact","repo:a.txt")
        assert r.returncode!=0, "record-action must not accept user-authored execution status"
        assert read_state(out)["state"]=="RUNNING"
        assert read_state(out)["actions"]==[]

def test_no_artifact_never_passes():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        init(out,repo)
        assert run("start","--out-dir",str(out)).returncode==0
        assert run("record-action","--out-dir",str(out),"--action-id","package-validate-v072").returncode==0
        assert run("verify","--out-dir",str(out)).returncode==0
        assert read_state(out)["state"]=="UNVERIFIED"

def test_high_risk_requires_scoped_live_approval():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        init(out,repo,"t-prod-5","production database migration","migration dry-run evidence exists")
        assert read_state(out)["approval_required"] is True
        assert run("start","--out-dir",str(out)).returncode==0
        assert read_state(out)["state"]=="BLOCKED"
        # Expired approval must not be recorded.
        r=run("approve","--out-dir",str(out),"--approved-by","owner","--scope","t-prod-5 production database migration","--target",str(repo),"--objective","Authorize production database migration dry-run only","--review-record","change-884 approval review","--expires","2020-01-01")
        assert r.returncode!=0
        assert read_state(out)["approvals"]==[]
        # Approval scope must include this task ID and expiry must not be in the past.
        r=run("approve","--out-dir",str(out),"--approved-by","owner","--scope","t-prod-5: production database migration dry-run in isolated test database; no production writes","--target",str(repo),"--objective","Authorize production database migration dry-run in isolated test database","--review-record","change-884 approval review","--expires","2099-12-31")
        assert r.returncode==0,r.stdout+r.stderr
        assert read_state(out)["state"]=="ROUTED"
        assert run("plan","--out-dir",str(out)).returncode==0
        assert run("start","--out-dir",str(out)).returncode==0
        assert read_state(out)["state"]=="RUNNING"

def test_artifact_mutation_is_detected():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        init(out,repo)
        assert run("start","--out-dir",str(out)).returncode==0
        r=run("run-check","--out-dir",str(out),"--check-id","package-validate-v072"); assert r.returncode==0,r.stdout+r.stderr
        # Modify stdout after its hash is recorded; the verifier must fail closed.
        (out/"runs/package-validate-v072.stdout.txt").write_text("forged after execution\n",encoding="utf-8")
        r=run("record-criterion","--out-dir",str(out),"--index","1","--status","pass","--evidence","repo:a.txt"); assert r.returncode==0,r.stderr
        assert run("verify","--out-dir",str(out)).returncode==0
        assert read_state(out)["state"]=="FAILED"

def test_nonzero_runner_result_fails():
    # Use an isolated package clone with a purposely failing, explicitly pinned check.
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); package=base/"pkg"; shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
        runner=package/"scripts/fail_for_runtime_test.py"; runner.write_text("import sys\nprint('intentional failure')\nsys.exit(7)\n",encoding="utf-8")
        catalog_path=package/"checks/catalog.json"; catalog=json.loads(catalog_path.read_text())
        sha=hashlib.sha256(runner.read_bytes()).hexdigest()
        catalog["checks"].append({"check_id":"intentional-failure-test-only","purpose":"adversarial test","runner":"scripts/fail_for_runtime_test.py","runner_sha256":sha,"argv":[],"expected_exit_code":0,"timeout_seconds":10,"blocking":True,"risk_tier":"low"})
        catalog_path.write_text(json.dumps(catalog,indent=2)+"\n",encoding="utf-8")
        out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        r=run("route","--task-id","t-fail","--request","read-only documentation audit","--repo",repo,"--out-dir",out,"--acceptance","intentional runner failure is captured",root=package); assert r.returncode==0,r.stdout+r.stderr
        assert run("plan","--out-dir",out,root=package).returncode==0
        assert run("start","--out-dir",out,root=package).returncode==0
        r=run("run-check","--out-dir",out,"--check-id","intentional-failure-test-only",root=package); assert r.returncode==1,r.stdout+r.stderr
        assert read_state(out)["actions"][-1]["exit_code"]==7
        assert run("record-criterion","--out-dir",out,"--index","1","--status","pass","--evidence","repo:a.txt",root=package).returncode==0
        assert run("verify","--out-dir",out,root=package).returncode==0
        assert read_state(out)["state"]=="FAILED"

def test_runner_timeout_terminates_descendants():
    # Call the cloned runtime directly rather than recursively starting a second
    # CLI tree; this isolates the process-group timeout behavior being tested.
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); package=base/"pkg"; shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
        runner=package/"scripts/slow_runner_for_runtime_test.py"
        runner.write_text("import subprocess, sys\nsubprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\nprint('spawned child', flush=True)\n",encoding="utf-8")
        catalog_path=package/"checks/catalog.json"; catalog=json.loads(catalog_path.read_text())
        catalog["checks"].append({"check_id":"timeout-process-group-test-only","purpose":"adversarial timeout test","runner":"scripts/slow_runner_for_runtime_test.py","runner_sha256":hashlib.sha256(runner.read_bytes()).hexdigest(),"argv":[],"expected_exit_code":0,"timeout_seconds":1,"blocking":True,"risk_tier":"low"})
        catalog_path.write_text(json.dumps(catalog,indent=2)+"\n",encoding="utf-8")
        spec=importlib.util.spec_from_file_location("runtime_timeout_test", package/"scripts/task_runtime.py")
        runtime=importlib.util.module_from_spec(spec); spec.loader.exec_module(runtime)
        repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        out=base/"out"
        state={"state":"RUNNING","task_id":"t-timeout","package_version":runtime.VERSION,
               "repository":{"path":str(repo),"tree_hash_at_route":runtime.tree_digest(repo),"tree_hash_exclusion":None},
               "package_integrity":{"tree_hash_at_route":runtime.tree_digest(package),"tree_hash_exclusion":None},
               "budget":{"tool_calls":0,"max_tool_calls":40},"actions":[],"events":[]}
        started=__import__("time").monotonic()
        result=runtime.perform_run_check(argparse.Namespace(check_id="timeout-process-group-test-only"),state,out)
        elapsed=__import__("time").monotonic()-started
        assert result==1, f"expected a timed-out runner to fail closed, got {result}"
        assert elapsed < 15, f"timeout handling took too long: {elapsed:.1f}s"
        assert state["actions"][-1]["exit_code"]==124
        assert "Timed out after 1s" in (out/"runs/timeout-process-group-test-only.stderr.txt").read_text(encoding="utf-8")

def test_event_ledger_tampering_is_detected():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        init(out,repo)
        p=out/"task-state.json"; state=json.loads(p.read_text()); state["events"][0]["type"]="forged-event"; p.write_text(json.dumps(state,indent=2))
        r=run("status","--out-dir",str(out)); assert r.returncode!=0
        assert "hash mismatch" in r.stderr or "ledger" in r.stderr

def test_risk_classification_is_separate_and_conservative():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); write_file(repo/"a.txt")
        r=run("route","--task-id","t-security","--request","security testing of an external API","--repo",str(repo),"--out-dir",str(out),"--acceptance","authorized test findings are evidenced")
        assert r.returncode==0,r.stdout+r.stderr
        route=json.loads((out/"route-decision.json").read_text())
        assert route["task_risk"]=="high"
        out2=base/"out2"
        r=run("route","--task-id","t-drop","--request","drop production database","--repo",str(repo),"--out-dir",str(out2),"--acceptance","impact is assessed")
        assert r.returncode==0,r.stdout+r.stderr
        route=json.loads((out2/"route-decision.json").read_text())
        assert route["task_risk"]=="critical"

def main():
    tests=[test_exit_zero_and_acceptance_evidence,test_forged_execution_is_rejected,test_no_artifact_never_passes,
           test_high_risk_requires_scoped_live_approval,test_artifact_mutation_is_detected,test_nonzero_runner_result_fails]
    failed=[]
    for fn in tests:
        try: fn(); print("PASS",fn.__name__)
        except Exception as exc: failed.append((fn.__name__,str(exc))); print("FAIL",fn.__name__,exc)
    print(f"{len(tests)-len(failed)}/{len(tests)} runtime regression tests passed")
    if failed: sys.exit(1)
if __name__=="__main__": main()
