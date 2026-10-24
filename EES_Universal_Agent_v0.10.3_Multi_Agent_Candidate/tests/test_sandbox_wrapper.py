from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_sandbox_wrapper_declares_required_defense_in_depth_flags():
    script=(ROOT/'scripts'/'run_sandbox_task.sh').read_text()
    for flag in ('--user 10001:10001','--read-only','--network none','--cap-drop ALL','--security-opt no-new-privileges:true','--pids-limit','--memory','--cpus','--tmpfs /tmp','--mount','WORKSPACE_MODE=ro','WORKSPACE_MODE=rw','@sha256:'):
        assert flag in script, flag

def test_sandbox_build_uses_project_root_context():
    script=(ROOT/'scripts'/'build_pilot_sandbox.sh').read_text()
    assert '"$ROOT"' in script
    assert '"$ROOT/sandbox"' not in script
