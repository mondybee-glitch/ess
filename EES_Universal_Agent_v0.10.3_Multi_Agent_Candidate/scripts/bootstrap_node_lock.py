#!/usr/bin/env python3
"""Generate and verify a genuine npm lockfile for the Playwright fixture.

Requires registry access. npm itself resolves transitive dependencies and integrity
metadata; this script deliberately refuses to fabricate a lockfile offline.
"""
from __future__ import annotations
import argparse, datetime, json, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "operational-fixtures" / "playwright-ui-state"
LOCK = FIXTURE / "package-lock.json"

def run(cmd: list[str], timeout: int) -> dict:
    try:
        p = subprocess.run(cmd, cwd=FIXTURE, text=True, capture_output=True, timeout=timeout, shell=False)
        return {"command": cmd, "exit_code": p.returncode, "status": "passed" if p.returncode == 0 else "failed", "stdout_tail": p.stdout[-3000:], "stderr_tail": p.stderr[-3000:]}
    except subprocess.TimeoutExpired as e:
        return {"command": cmd, "exit_code": 124, "status": "timeout", "stdout_tail": str(e.stdout or "")[-1000:], "stderr_tail": str(e.stderr or "")[-2000:]}

def validate_lock() -> tuple[bool, str]:
    if not LOCK.is_file(): return False, "npm did not create package-lock.json"
    try: lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except Exception as e: return False, f"lockfile is not valid JSON: {type(e).__name__}"
    if lock.get("lockfileVersion") != 3: return False, f"expected lockfileVersion 3; got {lock.get('lockfileVersion')!r}"
    package = json.loads((FIXTURE / "package.json").read_text(encoding="utf-8"))
    declared = package.get("devDependencies", {})
    locked_root = lock.get("packages", {}).get("", {}).get("devDependencies", {})
    if declared != locked_root: return False, "root devDependencies differ between package.json and package-lock.json"
    missing=[]
    for name, item in lock.get("packages", {}).items():
        if not name or not name.startswith("node_modules/"): continue
        if not item.get("resolved") or not item.get("integrity"):
            missing.append(name)
    if missing: return False, "lock entries missing resolved/integrity: " + ", ".join(missing[:12])
    return True, f"lockfile verified with {len(lock.get('packages', {}))-1} dependency package entries"

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeout', type=int, default=180, help='timeout per npm operation, seconds (default 180)')
    ap.add_argument('--verify-only', action='store_true', help='verify existing lockfile and run npm ci without regenerating it')
    a=ap.parse_args()
    if not 10 <= a.timeout <= 900: ap.error('--timeout must be between 10 and 900')
    npm=shutil.which('npm')
    report={"schema_version":1,"created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"fixture":"operational-fixtures/playwright-ui-state","steps":[],"status":"blocked","claim_boundary":"A real lock is generated only by npm with registry resolution; this script does not synthesize package integrity hashes."}
    if not npm:
        report['reason']='npm executable not found'
    else:
        if not a.verify_only:
            report['steps'].append(run([npm,'install','--package-lock-only','--ignore-scripts','--no-audit','--no-fund','--fetch-retries=2','--fetch-timeout=60000'],a.timeout))
        valid, message=validate_lock()
        report['lock_validation']={"status":"passed" if valid else "blocked","message":message}
        if valid:
            ci=run([npm,'ci','--ignore-scripts','--no-audit','--no-fund'],a.timeout)
            report['steps'].append(ci)
            report['status']='passed' if ci['status']=='passed' else ('blocked' if ci['status']=='timeout' else 'failed')
        else:
            report['reason']=message
            if not a.verify_only and LOCK.exists():
                try:
                    lock=json.loads(LOCK.read_text(encoding='utf-8'))
                    if lock.get('lockfileVersion') != 3 or lock.get('packages',{}).get('',{}).get('devDependencies') != json.loads((FIXTURE/'package.json').read_text())['devDependencies']:
                        LOCK.unlink()
                except Exception:
                    LOCK.unlink(missing_ok=True)
    out=ROOT/'reports/node-lock-bootstrap-latest.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({"status":report['status'], "reason":report.get('reason'), "lock_validation":report.get('lock_validation')}, ensure_ascii=False))
    print(f"Report: {out.relative_to(ROOT)}")
    return 0 if report['status']=='passed' else 1
if __name__=='__main__': raise SystemExit(main())
