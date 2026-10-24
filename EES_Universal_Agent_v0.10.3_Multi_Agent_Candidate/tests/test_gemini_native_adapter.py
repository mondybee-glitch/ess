import importlib.util, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('gemini_native_adapter',ROOT/'scripts'/'gemini_native_agent_adapter.py')
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)
def test_workspace_path_rejects_parent_traversal(tmp_path):
 try: MOD.safe_path(tmp_path,'../escape')
 except ValueError: pass
 else: raise AssertionError('parent traversal accepted')
def test_command_runner_rejects_shell_syntax(tmp_path):
 try: MOD.run_command(tmp_path,'python -m pytest; echo unsafe')
 except ValueError: pass
 else: raise AssertionError('shell syntax accepted')
def test_adapter_missing_key_fails_with_protocol_json(tmp_path):
 env={k:v for k,v in os.environ.items() if k!='GEMINI_API_KEY'}
 proc=subprocess.run([sys.executable,str(ROOT/'scripts'/'gemini_native_agent_adapter.py')],input=json.dumps({'protocol':'ees-agent-eval/v1'}),text=True,capture_output=True,env=env,timeout=10)
 assert proc.returncode==2
 payload=json.loads(proc.stdout); assert payload['summary']=='Gemini adapter failed'; assert 'GEMINI_API_KEY is required' in payload['limitations'][0]
