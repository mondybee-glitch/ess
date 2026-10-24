import importlib.util, json, shutil, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('ees_provider_adapter',ROOT/'scripts/openai_compatible_agent_adapter.py')
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)
RSPEC=importlib.util.spec_from_file_location('ees_runner_for_schema',ROOT/'scripts/run_agent_evals.py')
RUNNER=importlib.util.module_from_spec(RSPEC); RSPEC.loader.exec_module(RUNNER)

class AdapterPathTests(unittest.TestCase):
    def test_workspace_relative_file_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'sub').mkdir()
            self.assertEqual(MOD.resolve_workspace_path(root,'sub/file.txt',writing=True),root/'sub'/'file.txt')

    def test_parent_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): MOD.resolve_workspace_path(Path(td),'../outside.txt',writing=True)

    def test_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): MOD.resolve_workspace_path(Path(td),'/etc/passwd')

    def test_fixture_and_skill_are_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'fixture').mkdir(); (root/'SKILL.md').write_text('locked')
            with self.assertRaises(ValueError): MOD.resolve_workspace_path(root,'fixture/new.txt',writing=True)
            with self.assertRaises(ValueError): MOD.resolve_workspace_path(root,'SKILL.md',writing=True)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside:
            root=Path(td); (root/'linked').symlink_to(Path(outside),target_is_directory=True)
            with self.assertRaises(ValueError): MOD.resolve_workspace_path(root,'linked/file.txt',writing=True)

    def test_response_contract_validation(self):
        good={"summary":"done","changed_files":[],"commands":[],"limitations":[],"evidence":[]}
        self.assertEqual(RUNNER.validate_response(good),[])
        bad={"summary":"done","changed_files":[4],"commands":[{"command":"pytest"}],"limitations":[],"evidence":[]}
        self.assertTrue(RUNNER.validate_response(bad))

    def test_missing_docker_blocks_sandbox_when_unavailable(self):
        if shutil.which('docker'):
            self.skipTest('Docker available; execution policy should be tested on the disposable sandbox host')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'fixture').mkdir(); (root/'SKILL.md').write_text('test')
            result=MOD.run_in_docker(root,'echo should-not-run',1)
            self.assertFalse(result['ok'])
            self.assertEqual(result['exit_code'],127)
            self.assertIn('Docker executable not found',result['stderr'])

class ProviderProtocolTests(unittest.TestCase):
    def test_provider_tool_call_writes_workspace_artifact_then_returns_schema(self):
        from contextlib import redirect_stdout
        from io import StringIO
        from unittest.mock import patch
        first={"choices":[{"message":{"role":"assistant","content":None,"tool_calls":[{"id":"call-1","type":"function","function":{"name":"write_file","arguments":json.dumps({"path":"result.txt","content":"pilot artifact\n"})}}]}}],"usage":{"prompt_tokens":100,"completion_tokens":20}}
        final={"choices":[{"message":{"role":"assistant","content":json.dumps({"summary":"created file","changed_files":[],"commands":[],"limitations":[],"evidence":[{"criterion":"creates artifact","artifact":"result.txt","detail":"file written"}]})}}],"usage":{"prompt_tokens":150,"completion_tokens":40}}
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'fixture').mkdir(); (root/'fixture'/'task.txt').write_text('task',encoding='utf-8'); (root/'SKILL.md').write_text('skill',encoding='utf-8')
            payload={"protocol":"ees-agent-eval/v1","skill_id":"test-skill","case_id":"test-01","task":"write result","success_criteria":["file exists"],"expected_output":"result file","human_review_rubric":[],"response_contract":{}}
            out=StringIO()
            with patch.dict('os.environ',{"EES_API_KEY":"unit-test-key","EES_MODEL":"unit-test-model","EES_API_BASE_URL":"https://mock.invalid/v1"},clear=False), patch('sys.stdin',StringIO(json.dumps(payload))), patch.object(MOD,'chat_completion',side_effect=[first,final]) as api, redirect_stdout(out):
                old=Path.cwd()
                try:
                    import os; os.chdir(root)
                    rc=MOD.main()
                finally: os.chdir(old)
            self.assertEqual(rc,0)
            response=json.loads(out.getvalue())
            self.assertEqual(response['changed_files'],['result.txt'])
            self.assertEqual(response['adapter_status'],'completed')
            self.assertEqual(response['usage']['provider_calls'],2)
            self.assertEqual((root/'result.txt').read_text(), 'pilot artifact\n')
            self.assertNotIn('unit-test-key', out.getvalue())
            self.assertNotIn('unit-test-key', json.dumps(response))

    def test_invalid_provider_final_json_does_not_pass(self):
        from contextlib import redirect_stdout
        from io import StringIO
        from unittest.mock import patch
        response={"choices":[{"message":{"role":"assistant","content":"{not json"}}],"usage":{"prompt_tokens":20,"completion_tokens":5}}
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'fixture').mkdir(); (root/'SKILL.md').write_text('skill')
            payload={"protocol":"ees-agent-eval/v1","skill_id":"test-skill","case_id":"test-02","task":"test","success_criteria":["test"],"response_contract":{}}
            out=StringIO()
            with patch.dict('os.environ',{"EES_API_KEY":"unit-test-key","EES_MODEL":"unit-test-model"},clear=False), patch('sys.stdin',StringIO(json.dumps(payload))), patch.object(MOD,'chat_completion',return_value=response), redirect_stdout(out):
                old=Path.cwd()
                try:
                    import os; os.chdir(root)
                    rc=MOD.main()
                finally: os.chdir(old)
            data=json.loads(out.getvalue())
            self.assertEqual(rc,1)
            self.assertEqual(data['adapter_status'],'invalid_final_json')
            self.assertEqual(data['changed_files'],[])


class DockerCommandConstructionTests(unittest.TestCase):
    def test_docker_policy_is_restrictive_and_does_not_pass_provider_key(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'fixture').mkdir(); (root/'fixture'/'input.txt').write_text('input'); (root/'SKILL.md').write_text('skill')
            completed=__import__('subprocess').CompletedProcess(args=['docker'],returncode=0,stdout='ok',stderr='')
            with patch.dict('os.environ',{'EES_API_KEY':'do-not-pass-to-container','EES_SANDBOX_IMAGE':'test-image:pilot'},clear=False), patch.object(MOD.shutil,'which',return_value='/usr/bin/docker'), patch.object(MOD.subprocess,'run',return_value=completed) as docker_run:
                result=MOD.run_in_docker(root,'python -c "print(1)"',10)
            self.assertTrue(result['ok'])
            args=docker_run.call_args.args[0]
            for flag in ('--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges:true','--pids-limit=128','--memory=2g','--memory-swap=2g','--cpus=2','--name'):
                self.assertIn(flag,args)
            joined=' '.join(args)
            self.assertNotIn('do-not-pass-to-container',joined)
            self.assertNotIn('EES_API_KEY',joined)
            self.assertIn('readonly',joined)


class DockerTimeoutCleanupTests(unittest.TestCase):
    def test_timeout_attempts_kill_and_remove_named_container(self):
        import subprocess
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'fixture').mkdir(); (root/'SKILL.md').write_text('skill')
            timed_out=subprocess.TimeoutExpired(cmd=['docker','run'],timeout=1,output=b'',stderr=b'')
            done=subprocess.CompletedProcess(args=['docker','kill'],returncode=0,stdout='killed',stderr='')
            removed=subprocess.CompletedProcess(args=['docker','rm'],returncode=0,stdout='removed',stderr='')
            with patch.object(MOD.shutil,'which',return_value='/usr/bin/docker'), patch.object(MOD.subprocess,'run',side_effect=[timed_out,done,removed]) as calls:
                result=MOD.run_in_docker(root,'sleep 10',1)
            self.assertFalse(result['ok'])
            self.assertEqual(result['exit_code'],124)
            self.assertIn('cleanup attempted',result['stderr'])
            self.assertGreaterEqual(calls.call_count,3)
            self.assertEqual(calls.call_args_list[1].args[0][1],'kill')
            self.assertIn('rm',calls.call_args_list[2].args[0])

if __name__=='__main__': unittest.main()
