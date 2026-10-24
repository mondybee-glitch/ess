import json, os, pathlib, subprocess, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import agent_runtime
ROOT=pathlib.Path(__file__).resolve().parents[1]
class PackageTests(unittest.TestCase):
    def test_feedback_store_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            db=pathlib.Path(d)/'m.sqlite'
            cmd=[sys.executable,str(ROOT/'scripts/feedback_store.py'),'--db',str(db),'feedback','--task-id','t1','--skill-id','s1','--category','testing','--outcome','fail','--details','bad test']
            self.assertEqual(subprocess.run(cmd,capture_output=True,text=True).returncode,0)
            out=subprocess.run([sys.executable,str(ROOT/'scripts/feedback_store.py'),'--db',str(db),'list','--skill-id','s1'],capture_output=True,text=True)
            self.assertEqual(out.returncode,0); self.assertEqual(json.loads(out.stdout)[0]['task_id'],'t1')
    def test_runtime_blocks_without_credentials(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/agent_runtime.py')],input=json.dumps({'task_id':'t','request':'x'}),text=True,capture_output=True,env={**os.environ,'EES_API_KEY':'','EES_MODEL':''})
        self.assertEqual(p.returncode,2)
        self.assertEqual(json.loads(p.stdout)['status'],'blocked')

    def test_command_injection_payloads_are_rejected(self):
        payloads = [
            "python -c __import__('os').system('id')",
            "node -e console.log(123)",
            "python3 -c print(1)",
            "python -m pytest; id",
            "pytest && id",
            "sh -c id",
        ]
        for command in payloads:
            with self.subTest(command=command):
                self.assertFalse(agent_runtime.tool_run_command(command)["ok"])

    def test_write_rejects_traversal_and_control_plane(self):
        with tempfile.TemporaryDirectory() as d:
            old_root = agent_runtime.ROOT
            agent_runtime.ROOT = pathlib.Path(d).resolve()
            try:
                self.assertFalse(agent_runtime.tool_write_file("../escape.txt", "x")["ok"])
                self.assertFalse(agent_runtime.tool_write_file("scripts/new.py", "x")["ok"])
                self.assertFalse(agent_runtime.tool_write_file("integrations/adaptive-engineering-agent/new.py", "x")["ok"])
            finally:
                agent_runtime.ROOT = old_root

    def test_write_is_new_file_only_and_workspace_bound(self):
        with tempfile.TemporaryDirectory() as d:
            old_root = agent_runtime.ROOT
            agent_runtime.ROOT = pathlib.Path(d).resolve()
            try:
                result = agent_runtime.tool_write_file("outputs/result.txt", "safe")
                self.assertTrue(result["ok"])
                self.assertEqual((pathlib.Path(d)/"outputs/result.txt").read_text(), "safe")
                self.assertEqual(agent_runtime.tool_write_file("outputs/result.txt", "overwrite")["error"], "overwrite_not_allowed")
            finally:
                agent_runtime.ROOT = old_root

    def test_skill_has_frontmatter(self):
        text=(ROOT/'SKILL.md').read_text(); self.assertIn('name: adaptive-engineering-agent',text); self.assertIn('description:',text)
if __name__=='__main__': unittest.main()
