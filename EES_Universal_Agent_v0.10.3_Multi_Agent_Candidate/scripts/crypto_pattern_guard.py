#!/usr/bin/env python3
"""Conservative source-pattern guardrail for common cryptography footguns.

This is a heuristic scanner: findings require review; a clean result is not a security certification.
"""
from __future__ import annotations
import argparse, pathlib, re, sys

RULES = [
    ("weak-hash", re.compile(r"\b(?:md5|sha1)\s*\(", re.I), "MD5/SHA-1 used as a security primitive; choose a purpose-built modern primitive"),
    ("ecb-mode", re.compile(r"\bAES\s*\.\s*MODE_ECB\b|\bMODE_ECB\b", re.I), "ECB mode is not suitable for general application encryption"),
    ("insecure-rng", re.compile(r"\bMath\.random\s*\(|\brandom\.random\s*\(", re.I), "non-cryptographic random source used in security-sensitive code"),
    ("raw-password-hash", re.compile(r"(?:password|passwd|pwd).{0,80}(?:sha256|sha1|md5)\s*\(", re.I), "passwords require a dedicated password hashing scheme such as Argon2id"),
    ("ordinary-secret-compare", re.compile(r"(?:token|mac|signature|secret).{0,60}==|==.{0,60}(?:token|mac|signature|secret)", re.I), "review secret-dependent equality; use constant-time comparison where appropriate"),
]
def scan(text: str):
    findings=[]
    for rule, pattern, message in RULES:
        for n,line in enumerate(text.splitlines(),1):
            if pattern.search(line) and not line.lstrip().startswith(("#", "//", "*")):
                findings.append({"rule":rule,"line":n,"message":message,"snippet":line.strip()[:180]})
    return findings
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    args=ap.parse_args()
    findings=[]
    for raw in args.paths:
        path=pathlib.Path(raw)
        files=[path] if path.is_file() else [x for x in path.rglob("*") if x.is_file() and x.suffix in {".py",".js",".mjs",".ts",".tsx",".jsx"}]
        for file in files:
            try:
                for item in scan(file.read_text(encoding="utf-8",errors="replace")):
                    item["file"]=str(file); findings.append(item)
            except OSError as exc:
                print(f"ERROR: {file}: {exc}",file=sys.stderr); return 2
    if args.json:
        import json; print(json.dumps({"scanner":"heuristic","findings":findings,"clean_is_not_certification":True},indent=2))
    else:
        for f in findings: print(f'{f["file"]}:{f["line"]}: {f["rule"]}: {f["message"]}')
        print(f"Findings: {len(findings)} (heuristic; review required)")
    return 1 if findings else 0
if __name__=="__main__": raise SystemExit(main())
