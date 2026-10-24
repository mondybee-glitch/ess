#!/usr/bin/env python3
"""Repository snapshot integrity regressions, isolated from runtime workflow tests."""
from __future__ import annotations
import json, os, signal, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RT = ROOT / "scripts" / "task_runtime.py"

def run(*args):
    command = [sys.executable, str(RT), *map(str, args)]
    proc = subprocess.Popen(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=(os.name == "posix"),
                            close_fds=True, env={**os.environ, "EES_REQUIRE_SIGNED_EVIDENCE": "0"})
    try:
        stdout, stderr = proc.communicate(timeout=30)
        return subprocess.CompletedProcess(command, proc.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        # Kill the entire process group so a runner cannot retain inherited pipes
        # and stall the whole pytest session after its direct parent times out.
        if os.name == "posix":
            try: os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError: pass
        else:
            proc.kill()
        stdout, stderr = proc.communicate()
        return subprocess.CompletedProcess(command, 124, stdout, (stderr or "") + "\nTimed out after 30s; process group terminated")

def write_file(path, content="evidence\n"):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path

def init(out, repo):
    result = run("route", "--task-id", "t-low", "--request", "read-only documentation audit",
                 "--repo", str(repo), "--out-dir", str(out), "--acceptance", "validation result is evidenced")
    assert result.returncode == 0, result.stdout + result.stderr
    result = run("plan", "--out-dir", str(out))
    assert result.returncode == 0, result.stdout + result.stderr

def read_state(out):
    return json.loads((Path(out) / "task-state.json").read_text(encoding="utf-8"))

def test_repo_changes_after_route_are_blocked():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); source=write_file(repo/"source.txt")
        init(out,repo)
        source.write_text("modified after route\n",encoding="utf-8")
        assert run("start","--out-dir",str(out)).returncode==0
        assert read_state(out)["state"]=="BLOCKED"

def test_repo_changes_after_start_prevent_check():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); source=write_file(repo/"source.txt")
        init(out,repo)
        assert run("start","--out-dir",str(out)).returncode==0
        source.write_text("changed after start\n",encoding="utf-8")
        result=run("run-check","--out-dir",str(out),"--check-id","package-validate-v072")
        assert result.returncode==2, result.stdout+result.stderr
        state=read_state(out)
        assert state["state"]=="BLOCKED"
        assert state["actions"]==[]

def test_repo_changes_before_verify_prevents_pass():
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp); out=base/"out"; repo=base/"repo"; repo.mkdir(); source=write_file(repo/"source.txt")
        init(out,repo)
        assert run("start","--out-dir",str(out)).returncode==0
        result=run("run-check","--out-dir",str(out),"--check-id","package-validate-v072")
        assert result.returncode==0, result.stdout+result.stderr
        result=run("record-criterion","--out-dir",str(out),"--index","1","--status","pass","--evidence","repo:source.txt")
        assert result.returncode==0, result.stdout+result.stderr
        source.write_text("changed before verify\n",encoding="utf-8")
        assert run("verify","--out-dir",str(out)).returncode==0
        assert read_state(out)["state"]=="FAILED"

def main():
    tests=[test_repo_changes_after_route_are_blocked, test_repo_changes_after_start_prevent_check,
           test_repo_changes_before_verify_prevents_pass]
    failed=[]
    for fn in tests:
        try:
            fn(); print("PASS",fn.__name__,flush=True)
        except Exception as exc:
            failed.append((fn.__name__,str(exc))); print("FAIL",fn.__name__,exc,flush=True)
    print(f"{len(tests)-len(failed)}/{len(tests)} repository-integrity tests passed",flush=True)
    if failed: sys.exit(1)

if __name__ == "__main__": main()
