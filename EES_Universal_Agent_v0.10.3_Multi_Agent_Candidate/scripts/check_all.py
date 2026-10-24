#!/usr/bin/env python3
"""Reproducible standard-library release checks; does not claim agent quality."""
from __future__ import annotations
import json, subprocess, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def package_version() -> str:
    """Read the version from the canonical manifest; never hard-code it in reports."""
    manifest = json.loads((ROOT / "package-manifest.json").read_text(encoding="utf-8"))
    version = manifest.get("version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("package-manifest.json must define a non-empty string version")
    return version

def main() -> int:
    checks = [
        ("full_validation", [sys.executable, "scripts/validate.py", "--full"]),
        ("eval_contract_fixtures", [sys.executable, "scripts/run_eval.py", "--output", "reports/check-all-eval-fixtures.json"]),
        ("routing_audit", [sys.executable, "scripts/audit_routing.py", "--output", "reports/check-all-routing-audit.json"]),
        ("operational_fixtures", [sys.executable, "scripts/run_operational_fixtures.py", "--output", "reports/check-all-operational-fixtures.json"]),
    ]
    results=[]
    for name, cmd in checks:
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        results.append({"name":name,"command":" ".join(cmd),"exit_code":p.returncode,"status":"passed" if p.returncode==0 else "failed","stdout_tail":p.stdout[-4000:],"stderr_tail":p.stderr[-2000:]})
    try:
        import pytest  # noqa
        p=subprocess.run([sys.executable,"-m","pytest","-q","tests"],cwd=ROOT,text=True,capture_output=True)
        results.append({"name":"pytest_suite","command":"python -m pytest -q tests","exit_code":p.returncode,"status":"passed" if p.returncode==0 else "failed","stdout_tail":p.stdout[-4000:],"stderr_tail":p.stderr[-2000:]})
    except ImportError:
        results.append({"name":"pytest_suite","command":"python -m pytest -q tests","exit_code":None,"status":"skipped_dependency_missing","install":"python -m pip install -r requirements-test.txt","note":"Core checks above do not require pytest; unit tests are not claimed as run."})
    report={"schema_version":1,"created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"package_version":package_version(),"checks":results,"passed":sum(r["status"]=="passed" for r in results),"failed":sum(r["status"]=="failed" for r in results),"skipped":sum(r["status"].startswith("skipped") for r in results),"agent_quality_claim":"none; these are repository checks, not real-agent pilot results"}
    out=ROOT/"reports/check-all-latest.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:report[k] for k in ("passed","failed","skipped","agent_quality_claim")},indent=2))
    print(f"Report: {out.relative_to(ROOT)}")
    return 1 if report["failed"] else 0
if __name__=="__main__": raise SystemExit(main())
