#!/usr/bin/env python3
"""Mutation tests for the package validator. All edits occur in disposable copies."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VALIDATOR=ROOT/"scripts/validate.py"

def fresh():
    temp=Path(tempfile.mkdtemp(prefix="ees-validator-test-"))
    package=temp/"pkg"
    shutil.copytree(ROOT,package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
    return temp,package

def check(name, mutate=None, expect_fail=False, expect_text=None):
    temp,pkg=fresh()
    try:
        if mutate: mutate(pkg)
        result=subprocess.run([sys.executable,str(VALIDATOR),"--full","--root",str(pkg)],cwd=ROOT,text=True,capture_output=True)
        okay=(result.returncode!=0)==expect_fail
        if okay and expect_text: okay=expect_text in (result.stdout+result.stderr)
        print(("PASS" if okay else "FAIL")+": "+name)
        if not okay: print(result.stdout+result.stderr)
        return okay
    finally:
        shutil.rmtree(temp,ignore_errors=True)

def mutate_version(pkg):
    p=pkg/"package-manifest.json"; d=json.loads(p.read_text()); d["version"]="9.9.9"; p.write_text(json.dumps(d))
def unregistered_skill(pkg):
    p=pkg/"capability-registry.json"; d=json.loads(p.read_text()); d["capabilities"]=[x for x in d["capabilities"] if x["id"]!="graphic-design"]; p.write_text(json.dumps(d))
def unknown_dependency(pkg):
    p=pkg/"capability-registry.json"; d=json.loads(p.read_text()); d["capabilities"][0]["dependencies"].append("not-a-skill"); p.write_text(json.dumps(d))
def bad_runner_pin(pkg):
    p=pkg/"checks/catalog.json"; d=json.loads(p.read_text()); d["checks"][0]["runner_sha256"]="0"*64; p.write_text(json.dumps(d))
def bad_fixture_selector(pkg):
    p=pkg/"skills/api-design-contracts/evals/evals.json"; d=json.loads(p.read_text()); d["cases"][0]["fixture_selector"]="missing-fixture-id"; p.write_text(json.dumps(d))
def divergent_expected_output(pkg):
    p=pkg/"fixtures/engineering-v072.json"; d=json.loads(p.read_text()); d["fixtures"][0]["expected_output"]="forged expected output"; p.write_text(json.dumps(d))
def duplicate_check_id(pkg):
    p=pkg/"checks/catalog.json"; d=json.loads(p.read_text()); d["checks"][1]["check_id"]=d["checks"][0]["check_id"]; p.write_text(json.dumps(d))
def fixture_claims_agent_success(pkg):
    p=pkg/"fixtures/engineering-v072.json"; d=json.loads(p.read_text()); d["fixtures"][0]["agent_status"]="passed"; p.write_text(json.dumps(d))
def dependency_cycle(pkg):
    p=pkg/"capability-registry.json"; d=json.loads(p.read_text()); idx={x["id"]:x for x in d["capabilities"]}
    idx["graphic-design"]["dependencies"]=["technical-documentation"]
    idx["technical-documentation"]["dependencies"]=["graphic-design"]
    idx["graphic-design"]["must_run_after"]=[]; idx["technical-documentation"]["must_run_after"]=[]
    idx["graphic-design"]["must_run_before"]=[]; idx["technical-documentation"]["must_run_before"]=[]
    p.write_text(json.dumps(d))

def broken_link(pkg):
    p=pkg/"routing-matrix.md"; p.write_text(p.read_text()+"\n[broken link](missing-target.md)\n")
def code_fenced_link(pkg):
    p=pkg/"routing-matrix.md"; p.write_text(p.read_text()+"\n```markdown\n[example only](missing-target.md)\n```\n")

def main():
    tests=[
      ("pristine package passes",None,False,None),
      ("manifest version divergence is rejected",mutate_version,True,"manifest version"),
      ("unregistered skill is rejected",unregistered_skill,True,"registry/files capability mismatch"),
      ("unknown dependency is rejected",unknown_dependency,True,"references unknown capability"),
      ("runner hash mismatch is rejected",bad_runner_pin,True,"runner hash mismatch"),
      ("fixture selector must resolve uniquely",bad_fixture_selector,True,"fixture_selector must match exactly one"),
      ("fixture/evaluation expected-output divergence is rejected",divergent_expected_output,True,"expected_output diverges"),
      ("duplicate check ID is rejected",duplicate_check_id,True,"duplicate check_id"),
      ("fixture cannot claim agent execution",fixture_claims_agent_success,True,"fixture definitions contain execution claims"),
      ("dependency cycle is rejected",dependency_cycle,True,"ordering graph contains a cycle"),
      ("broken local Markdown link is rejected",broken_link,True,"broken local link"),
      ("example link inside code fence is ignored",code_fenced_link,False,None),
    ]
    passed=0
    for name,mut,fail,phrase in tests:
        if check(name,mut,fail,phrase): passed+=1
    print(f"{passed}/{len(tests)} validator mutation tests passed")
    return 0 if passed==len(tests) else 1
if __name__=="__main__": sys.exit(main())
