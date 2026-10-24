#!/usr/bin/env python3
"""Generate a source-of-truth package baseline from actual repository files.

This report counts files and checks metadata drift. It makes no claim about agent
quality or semantic correctness.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--output", default="reports/baseline-v076.json")
    ap.add_argument("--sync-readme-counts", action="store_true", help="rewrite stale evaluation totals in README files")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    manifest_path = root / "package-manifest.json"
    registry_path = root / "capability-registry.json"
    manifest = read_json(manifest_path)
    registry = read_json(registry_path)
    eval_files = sorted({(root / c.get("eval_spec", "")).resolve() for c in registry.get("capabilities", []) if isinstance(c, dict)})
    skill_dirs = sorted(p.parent.name for p in (root / "skills").rglob("SKILL.md"))
    cases_by_skill = {}
    cases = []
    missing_criteria = []
    empty_criteria = []
    for path in eval_files:
        data = read_json(path)
        skill = data.get("skill_id", path.stem)
        skill_cases = data.get("cases", [])
        cases_by_skill[skill] = len(skill_cases)
        for case in skill_cases:
            cases.append((skill, case))
            criteria = case.get("success_criteria") if isinstance(case, dict) else None
            if "success_criteria" not in case:
                missing_criteria.append({"skill": skill, "case_id": case.get("id")})
            elif not criteria:
                empty_criteria.append({"skill": skill, "case_id": case.get("id")})
    case_count = len(cases)
    cap_ids = sorted(c.get("id") for c in registry.get("capabilities", []) if isinstance(c, dict))
    central_fixture_path = root / "fixtures/engineering-v072.json"
    central_fixture_count = len(read_json(central_fixture_path).get("fixtures", [])) if central_fixture_path.is_file() else 0
    operational_count = len([p for p in (root / "operational-fixtures").iterdir() if p.is_dir() and (p / "fixture.json").is_file()]) if (root / "operational-fixtures").is_dir() else 0
    issues=[]
    if len(skill_dirs) != len(set(skill_dirs)): issues.append("duplicate skill directory names")
    if set(skill_dirs) != set(manifest.get("skills", [])): issues.append("package manifest skill list differs from SKILL.md files")
    canonical_ids = sorted({c.get("canonical_skill_id", c.get("id")) for c in registry.get("capabilities", []) if isinstance(c, dict)})
    if set(skill_dirs) != set(canonical_ids): issues.append("canonical skill folders differ from registry canonical_skill_id mapping")
    if manifest.get("eval_case_count") != case_count: issues.append(f"manifest says {manifest.get('eval_case_count')} eval cases; actual count is {case_count}")
    if missing_criteria: issues.append(f"{len(missing_criteria)} evaluation contracts lack success_criteria")
    if empty_criteria: issues.append(f"{len(empty_criteria)} evaluation contracts have empty success_criteria")
    readme_counts={}
    for filename in ("README.md", "README_AR.md"):
        p=root/filename
        if p.is_file():
            text=p.read_text(encoding="utf-8")
            if filename == "README.md":
                matches=re.findall(r"\|\s*Evaluation contracts\s*\|\s*(\d+)\s+contracts",text,re.I)
                counts=[int(x) for x in matches]
            else:
                counts=[int(x) for x in re.findall(r"(?<!\d)(\d+) عقد تقييم",text,re.I)]
            readme_counts[filename]=counts
            if counts and any(x != case_count for x in counts):
                issues.append(f"{filename} displays stale evaluation total(s): {counts}; expected {case_count}")
    if args.sync_readme_counts:
        for filename in ("README.md", "README_AR.md"):
            p=root/filename
            if not p.is_file(): continue
            text=p.read_text(encoding="utf-8")
            if filename == "README.md":
                text=re.sub(r"(\|\s*Evaluation contracts\s*\|\s*)\d+(\s+contracts)", rf"\g<1>{case_count}\g<2>", text, flags=re.I)
            else:
                text=re.sub(r"\b\d+ عقد تقييم\b", f"{case_count} عقد تقييم", text)
            p.write_text(text,encoding="utf-8")
        readme_counts={"README.md":[case_count],"README_AR.md":[case_count]}
        issues=[x for x in issues if not x.startswith(("README.md displays stale", "README_AR.md displays stale"))]
    hashed_files = sorted(set([str(p.relative_to(root)) for p in eval_files] +
        [str(p.relative_to(root)) for p in (root/"skills").rglob("SKILL.md")] +
        ["package-manifest.json", "capability-registry.json", "checks/catalog.json", "fixtures/engineering-v072.json"]))
    file_hashes = {rel: sha(root/rel) for rel in hashed_files if (root/rel).is_file()}
    report={
        "schema_version":1,
        "package_version":manifest.get("version"),
        "generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_hashes":{"package-manifest.json":sha(manifest_path),"capability-registry.json":sha(registry_path)},
        "artifact_hashes":file_hashes,
        "counts":{"skills_with_skill_md":len(skill_dirs),"capabilities":len(cap_ids),"evaluation_contracts":case_count,
          "eval_skills":len(cases_by_skill),"central_fixtures":central_fixture_count,"operational_fixture_projects":operational_count,
          "success_criteria_missing":len(missing_criteria),"success_criteria_empty":len(empty_criteria)},
        "cases_per_skill":dict(sorted(cases_by_skill.items())),
        "missing_criteria":missing_criteria,
        "empty_criteria":empty_criteria,
        "readme_displayed_counts":readme_counts,
        "issues":issues,
        "status":"consistent" if not issues else "drift_detected",
        "claim_boundary":"This is a static structural/count baseline. It does not establish AI-agent task quality, routing accuracy, security, or production readiness."
    }
    out=Path(args.output); out=out if out.is_absolute() else root/out
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"counts":report["counts"],"issues":report["issues"]},ensure_ascii=False))
    return 0 if report["status"]=="consistent" else 1

if __name__ == "__main__":
    raise SystemExit(main())
