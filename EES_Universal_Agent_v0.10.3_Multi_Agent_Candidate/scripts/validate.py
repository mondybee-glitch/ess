#!/usr/bin/env python3
"""Single source-of-truth validator for Elite Engineering Suite v0.10.3.
Checks package structure/contracts only; it does not prove agent effectiveness.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.10.3"
REQUIRED_RUNTIME_FILES = [
    "SKILL.md", "README.md", "README_AR.md", "START_HERE_AR.md", "routing-matrix.md",
    "THIRD_PARTY_NOTICES.md", "references/anthropic-agent-skills-integration.md",
    "references/safety-policy.md", "capability-registry.json", "package-manifest.json",
    "checks/catalog.json", "scripts/task_runtime.py", "scripts/run_eval.py", "scripts/learning_governor.py", "scripts/sandbox_policy.py", "scripts/hierarchical_router_cache.py",
    "schemas/capability-registry.schema.json", "schemas/hierarchical-routing.schema.json", "hierarchical-routing.json", "schemas/task-state.schema.json",
    "schemas/execution-state.schema.json", "schemas/evidence-manifest.schema.json",
    "schemas/universal-skill-contract.schema.json", "templates/universal-skill-contract.example.json",
    "scripts/detect_capabilities.py", "docs/CROSS-AGENT-EVALUATION-v1.md", "docs/ADAPTIVE-RUNTIME-AND-EVIDENCE-GOVERNANCE-v0.10.0.md",
]

def load_json(path: Path):
    with path.open(encoding="utf-8") as f: return json.load(f)

def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: return None
    result = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result

def local_markdown_links(text: str):
    # Strip fenced code so example Markdown in code blocks is not treated as a real link.
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text)

def validate(root: Path):
    errors, warnings = [], []
    def err(msg): errors.append(msg)
    for name in REQUIRED_RUNTIME_FILES:
        if not (root / name).is_file(): err(f"required file missing: {name}")
    if errors: return errors, warnings, {}
    try:
        manifest = load_json(root / "package-manifest.json")
        registry = load_json(root / "capability-registry.json")
        catalog = load_json(root / "checks/catalog.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid JSON or unreadable package file: {exc}"], warnings, {}
    if manifest.get("name") != "elite-engineering-suite": err("manifest package name mismatch")
    if manifest.get("version") != VERSION: err(f"manifest version must be {VERSION}")
    if registry.get("package") != manifest.get("name"): err("registry/manifest package mismatch")
    if registry.get("version") != VERSION or registry.get("schema_version") != VERSION: err(f"registry versions must be {VERSION}")
    if catalog.get("version") != VERSION: err(f"checks catalog version must be {VERSION}")
    # Validate hierarchical routing both structurally and against the canonical registry.
    try:
        routing = load_json(root / "hierarchical-routing.json")
        routing_schema = load_json(root / "schemas/hierarchical-routing.schema.json")
        try:
            import jsonschema
            jsonschema.Draft202012Validator.check_schema(routing_schema)
            for problem in jsonschema.Draft202012Validator(routing_schema).iter_errors(routing):
                err("hierarchical routing schema violation at " + "/".join(map(str, problem.absolute_path)) + ": " + problem.message)
        except ImportError:
            if not isinstance(routing.get("stage1_routes"), list): err("hierarchical routing stage1_routes must be an array")
        route_ids = [r.get("id") for r in routing.get("stage1_routes", []) if isinstance(r, dict)]
        route_skills = [sid for r in routing.get("stage1_routes", []) if isinstance(r, dict) for sid in r.get("skills", [])]
        if len(route_ids) != len(set(route_ids)): err("hierarchical routing has duplicate route IDs")
        if len(route_skills) != len(set(route_skills)): err("hierarchical routing has duplicate skill assignments")
    except (OSError, json.JSONDecodeError, AttributeError, TypeError) as exc:
        routing = {}; route_skills = []; err(f"hierarchical routing config invalid: {exc}")

    caps = registry.get("capabilities")
    if not isinstance(caps, list) or not caps:
        err("registry capabilities must be a non-empty array"); caps=[]
    cap_ids = [c.get("id") for c in caps if isinstance(c, dict)]
    if len(cap_ids) != len(set(cap_ids)): err("duplicate capability id")
    cap_map = {c.get("id"): c for c in caps if isinstance(c, dict) and c.get("id")}
    # v0.7.6 ownership metadata and hard-conflict semantics.
    for sid, cap in cap_map.items():
        own = cap.get("ownership")
        if not isinstance(own, dict):
            err(f"{sid}: ownership metadata missing")
            continue
        if own.get("owner_skill") != sid: err(f"{sid}: ownership.owner_skill must equal capability ID")
        for ref in own.get("handoff_skill_ids", []) or []:
            if ref not in cap_map: err(f"{sid}: ownership references unknown handoff skill {ref}")
        for ref in cap.get("conflicts_with", []) or []:
            if ref in cap_map and sid not in (cap_map[ref].get("conflicts_with", []) or []):
                err(f"{sid}: conflicts_with must be reciprocal with {ref}")
    policy = registry.get("routing_ownership_policy")
    if not isinstance(policy, dict) or policy.get("conflicts_with_semantics") is None:
        err("routing_ownership_policy must define hard-conflict semantics")
    dirs = {p.parent.name for p in (root / "skills").rglob("SKILL.md")}
    manifest_skills = manifest.get("skills", [])
    if not isinstance(manifest_skills, list): err("manifest skills must be an array"); manifest_skills=[]
    if set(manifest_skills) != dirs:
        err(f"manifest/files skill mismatch: manifest-only={sorted(set(manifest_skills)-dirs)}, files-only={sorted(dirs-set(manifest_skills))}")
    if len(dirs) != 32: err(f"expected 32 canonical skill folders, found {len(dirs)}")
    if len(cap_map) != 74: err(f"expected 74 preserved capability IDs/aliases, found {len(cap_map)}")
    for sid, cap in cap_map.items():
        canonical_id = cap.get("canonical_skill_id")
        if not isinstance(canonical_id, str) or canonical_id not in dirs: err(f"{sid}: canonical_skill_id must map to an existing canonical skill folder")
    canonical_ids = {c.get("canonical_skill_id", c.get("id")) for c in cap_map.values()}
    if canonical_ids != dirs:
        err(f"registry/files canonical skill mismatch: registry-only={sorted(canonical_ids-dirs)}, files-only={sorted(dirs-canonical_ids)}")
    if set(route_skills) != set(cap_ids):
        err(f"hierarchical routing/registry mismatch: routing-only={sorted(set(route_skills)-set(cap_ids))}, unrouted={sorted(set(cap_ids)-set(route_skills))}")
    values=manifest.get("new_skills", [])
    if not isinstance(values,list): err("manifest new_skills must be an array")
    elif set(values)-dirs: err(f"manifest new_skills references missing canonical skills: {sorted(set(values)-dirs)}")
    source_values=manifest.get("source_modules", [])
    if not isinstance(source_values,list): err("manifest source_modules must be an array")
    elif set(source_values)-set(cap_ids): err(f"manifest source_modules references unknown capability aliases: {sorted(set(source_values)-set(cap_ids))}")
    if manifest.get("skill_count") != len(dirs): err(f"manifest skill_count {manifest.get('skill_count')} != actual {len(dirs)}")
    if manifest.get("capability_count") != len(cap_map): err(f"manifest capability_count {manifest.get('capability_count')} != registry {len(cap_map)}")
    if manifest.get("registry_skill_count") != len(cap_map): err("manifest registry_skill_count mismatch")
    if registry.get("source_module_count") != len(manifest.get("source_modules", [])): err("registry source_module_count does not match manifest source_modules")

    # Validate all active JSON Schema files syntactically; registry schema is also applied to the data.
    try:
        import jsonschema
        schema_engine = jsonschema.Draft202012Validator
    except ImportError:
        schema_engine = None
        warnings.append("jsonschema package unavailable; schema syntax receives only built-in checks")
    for schema_name in ("capability-registry.schema.json", "task-state.schema.json", "execution-state.schema.json", "evidence-manifest.schema.json"):
        sp=root/"schemas"/schema_name
        try:
            sd=load_json(sp)
            if sd.get("$schema") != "https://json-schema.org/draft/2020-12/schema": err(f"{schema_name} must declare JSON Schema Draft 2020-12")
            if schema_engine is not None: schema_engine.check_schema(sd)
        except (OSError,json.JSONDecodeError,Exception) as exc:
            # Avoid duplicate noise for missing schema paths already reported above.
            err(f"{schema_name} is not a valid JSON Schema: {exc}")
    # JSON Schema validation is supplementary; semantic checks below still run if jsonschema isn't installed.
    schema_path=root/"schemas/capability-registry.schema.json"
    try:
        schema=load_json(schema_path)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema": err("registry schema must use Draft 2020-12")
        try:
            import jsonschema
            jsonschema.Draft202012Validator.check_schema(schema)
            for problem in jsonschema.Draft202012Validator(schema).iter_errors(registry):
                err("registry schema violation at " + "/".join(map(str,problem.absolute_path)) + ": " + problem.message)
        except ImportError:
            warnings.append("jsonschema package unavailable; used built-in semantic checks")
    except (OSError, json.JSONDecodeError) as exc: err(f"registry schema cannot be read: {exc}")

    # Validate every specialist and require signal definitions to compile.
    required_cap_fields={"id","description","positive_signals","negative_signals","activation_threshold","risk_class","dependencies","skill_path"}
    order_edges={sid:set() for sid in cap_map}
    for sid, cap in cap_map.items():
        missing=required_cap_fields-set(cap)
        if missing: err(f"capability {sid} missing fields {sorted(missing)}")
        canonical_id = cap.get("canonical_skill_id", sid)
        expected=f"skills/{canonical_id}/SKILL.md"
        if cap.get("skill_path") != expected: err(f"capability {sid} skill_path should be {expected}")
        if canonical_id not in manifest_skills: err(f"capability {sid} canonical_skill_id is not in manifest skills: {canonical_id}")
        eval_spec=cap.get("eval_spec")
        if not isinstance(eval_spec,str) or not (root/eval_spec).is_file(): err(f"capability {sid} eval_spec missing or invalid: {eval_spec}")
        fixtures_dir=cap.get("fixtures_dir")
        fixture_source=cap.get("fixture_source")
        if fixtures_dir and not (root/fixtures_dir).is_dir(): err(f"capability {sid} fixtures_dir missing: {fixtures_dir}")
        if fixture_source and not (root/fixture_source).is_file(): err(f"capability {sid} fixture_source missing: {fixture_source}")
        if not fixtures_dir and not fixture_source: err(f"capability {sid} must declare fixtures_dir or fixture_source")
        skill_path=root/expected
        if not skill_path.is_file(): err(f"capability {sid} skill file missing")
        else:
            text=skill_path.read_text(encoding="utf-8")
            fm=parse_frontmatter(text)
            if not fm: err(f"{sid}: skill frontmatter missing")
            else:
                if fm.get("name") != canonical_id: err(f"{sid}: frontmatter name should match canonical skill {canonical_id}")
                if not fm.get("description") or len(fm["description"]) > 1024: err(f"{sid}: description missing or over 1024 chars")
            body=re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
            if len(body.split()) < 100: err(f"{sid}: specialist procedure is too short (<100 words)")
            if re.search(r"\b(TODO|TBD|coming soon|not yet written)\b", body, re.I): err(f"{sid}: unresolved placeholder content")
            if re.search(r"\bPhase\s+\d+\b", body, re.I): err(f"{sid}: unexplained deferred phase placeholder")
            for dest in local_markdown_links(text):
                if dest.startswith(("http://","https://","mailto:","#","data:")): continue
                target=(skill_path.parent/dest.split("#",1)[0]).resolve()
                try: target.relative_to(root.resolve())
                except ValueError: err(f"{sid}: local link escapes package: {dest}"); continue
                if not target.exists(): err(f"{sid}: broken local link: {dest}")
        if cap.get("risk_class") not in {"low","medium","high","critical"}: err(f"{sid}: invalid risk_class")
        th=cap.get("activation_threshold")
        if not isinstance(th,(int,float)) or isinstance(th,bool) or th < 0: err(f"{sid}: activation_threshold must be nonnegative numeric")
        for fld in ("positive_signals","negative_signals","dependencies","must_run_with","must_run_before","must_run_after","conflicts_with","pre_flight_checks"):
            val=cap.get(fld,[])
            if not isinstance(val,list): err(f"{sid}: {fld} must be an array"); continue
            if fld in {"dependencies","must_run_with","must_run_before","must_run_after","conflicts_with","pre_flight_checks"} and len(val)!=len(set(val)): err(f"{sid}: duplicate references in {fld}")
            if fld == "pre_flight_checks":
                catalog_ids={x.get("check_id") for x in catalog.get("checks",[]) if isinstance(x,dict)}
                for check_id in val:
                    if check_id not in catalog_ids: err(f"{sid}: unknown pre_flight_check {check_id}")
        for fld in ("positive_signals","negative_signals"):
            for signal in cap.get(fld,[]) if isinstance(cap.get(fld,[]),list) else []:
                pattern=signal if isinstance(signal,str) else signal.get("pattern","") if isinstance(signal,dict) else ""
                if not isinstance(pattern,str) or not pattern: err(f"{sid}: malformed {fld} entry"); continue
                try: re.compile(pattern,re.I)
                except re.error as exc: err(f"{sid}: invalid {fld} regex {pattern!r}: {exc}")
        ref_fields=("dependencies","must_run_with","must_run_before","must_run_after","conflicts_with")
        for fld in ref_fields:
            for ref in cap.get(fld,[]) if isinstance(cap.get(fld,[]),list) else []:
                if ref not in cap_map: err(f"{sid}.{fld} references unknown capability {ref}")
                if ref == sid: err(f"{sid}.{fld} cannot reference itself")
        # order edges are prerequisite -> dependent
        for dep in set(cap.get("dependencies",[])) | set(cap.get("must_run_after",[])):
            if dep in order_edges: order_edges[dep].add(sid)
        for before in cap.get("must_run_before",[]):
            if before in order_edges: order_edges[sid].add(before)
        conflicts=set(cap.get("conflicts_with",[]))
        if conflicts & (set(cap.get("dependencies",[])) | set(cap.get("must_run_with",[]))):
            err(f"{sid}: conflicts_with overlaps a required dependency/co-activation")
    indegree={x:0 for x in order_edges}
    for source, targets in order_edges.items():
        for target in targets: indegree[target]+=1
    ready=sorted(x for x,n in indegree.items() if n==0); seen=0
    while ready:
        node=ready.pop(0); seen+=1
        for target in sorted(order_edges[node]):
            indegree[target]-=1
            if indegree[target]==0: ready.append(target); ready.sort()
    if seen != len(order_edges): err("capability ordering graph contains a cycle: " + ", ".join(sorted(x for x,n in indegree.items() if n>0)))

    checks=catalog.get("checks",[])
    check_ids=[x.get("check_id") for x in checks if isinstance(x,dict)]
    if not checks: err("checks catalog is empty")
    if len(check_ids)!=len(set(check_ids)): err("duplicate check_id in checks catalog")
    for check in checks:
        if not isinstance(check,dict): err("malformed checks catalog entry"); continue
        if not check.get("check_id") or not check.get("runner") or not isinstance(check.get("argv",[]),list): err("check catalog entry missing check_id/runner/argv")
        runner=check.get("runner","")
        runner_path=root/runner if runner else None
        if runner_path and not runner_path.is_file(): err(f"check {check.get('check_id')} runner missing: {runner}")
        expected_hash=check.get("runner_sha256")
        if not isinstance(expected_hash,str) or not re.fullmatch(r"[a-f0-9]{64}",expected_hash): err(f"check {check.get('check_id')} runner_sha256 missing/invalid")
        elif runner_path and runner_path.is_file():
            import hashlib
            actual_hash=hashlib.sha256(runner_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash: err(f"check {check.get('check_id')} runner hash mismatch")
        if not isinstance(check.get("expected_exit_code",0),int): err(f"check {check.get('check_id')} expected_exit_code must be int")
        if not isinstance(check.get("timeout_seconds",120),int) or not 1 <= check.get("timeout_seconds",120) <= 300: err(f"check {check.get('check_id')} timeout_seconds must be in 1..300")
        if check.get("blocking") not in (True,False): err(f"check {check.get('check_id')} blocking must be boolean")

    # Validate central v0.7.6 fixture contract without claiming the agent ran it.
    fixture_path=root/"fixtures/engineering-v072.json"
    fixture_count=0
    if not fixture_path.is_file(): err("fixtures/engineering-v072.json missing")
    else:
        try:
            fixture=load_json(fixture_path); records=fixture.get("fixtures",[]); fixture_count=len(records)
            if fixture.get("version") != VERSION: err(f"central fixture version must be {VERSION}")
            ids=[x.get("fixture_id") for x in records]
            if len(ids)!=len(set(ids)): err("duplicate central fixture_id")
            if any(x.get("fixture_status")!="defined-not-run" or x.get("agent_status")!="not-run" for x in records): err("fixture definitions contain execution claims")
            if any(x.get("skill_id") not in cap_map for x in records): err("central fixture references unknown skill")
        except (OSError,json.JSONDecodeError,AttributeError) as exc: err(f"central fixtures invalid: {exc}")
    actual_eval=0
    eval_files = sorted((root/"evals"/"aliases").glob("*.json"))
    for eval_file in eval_files:
        try:
            ev=load_json(eval_file); cases=ev.get("cases",[]); actual_eval+=len(cases)
            cids=[x.get("id") for x in cases]
            if len(cids)!=len(set(cids)): err(f"{eval_file.relative_to(root)} duplicate case ID")
            for c in cases:
                for key in ("fixture","expected_output","automated_checks","human_review_rubric"):
                    if not c.get(key): err(f"{eval_file.relative_to(root)} case {c.get('id')} missing {key}")
                fpath=root/c.get("fixture","")
                if not fpath.is_file():
                    err(f"{eval_file.relative_to(root)} case {c.get('id')} fixture missing")
                elif c.get("fixture_selector"):
                    try:
                        shared=load_json(fpath)
                        matches=[x for x in shared.get("fixtures",[]) if x.get("fixture_id")==c.get("fixture_selector")]
                        if len(matches)!=1: err(f"{eval_file.relative_to(root)} case {c.get('id')} fixture_selector must match exactly one central fixture")
                        elif matches[0].get("skill_id") != (ev.get("skill_id") or eval_file.stem): err(f"{eval_file.relative_to(root)} case {c.get('id')} central fixture skill mismatch")
                        elif matches[0].get("expected_output") != c.get("expected_output"): err(f"{eval_file.relative_to(root)} case {c.get('id')} expected_output diverges from selected fixture")
                    except (OSError,json.JSONDecodeError,AttributeError) as exc:
                        err(f"{eval_file.relative_to(root)} case {c.get('id')} selected fixture cannot be read: {exc}")
        except (OSError,json.JSONDecodeError,AttributeError) as exc: err(f"cannot read {eval_file}: {exc}")
    if manifest.get("eval_case_count") != actual_eval: err(f"manifest eval_case_count {manifest.get('eval_case_count')} != actual {actual_eval}")
    if manifest.get("eval_status") is None: err("manifest eval_status missing")
    if manifest.get("backend_fixture_count") + manifest.get("source_fixture_count") != fixture_count:
        err(f"manifest central fixture breakdown does not match total {fixture_count}")
    if manifest.get("capability_registry") != "capability-registry.json": err("manifest capability_registry path mismatch")
    for doc in list(root.glob("*.md")) + list((root/"docs").glob("*.md")) + list((root/"references").glob("*.md")):
        if doc.name.endswith("v0.7.0.md"): continue
        text=doc.read_text(encoding="utf-8")
        for dest in local_markdown_links(text):
            if dest.startswith(("http://","https://","mailto:","#","data:")): continue
            target=(doc.parent/dest.split("#",1)[0]).resolve()
            try: target.relative_to(root.resolve())
            except ValueError: err(f"{doc.relative_to(root)}: local link escapes package: {dest}"); continue
            if not target.exists(): err(f"{doc.relative_to(root)}: broken local link: {dest}")
    return errors, warnings, {"version":VERSION,"skills":len(dirs),"capabilities":len(cap_map),"eval_contracts":actual_eval,"central_fixtures":fixture_count,"checks":len(checks),"operational_fixture_projects":len([p for p in (root/"operational-fixtures").iterdir() if p.is_dir() and (p/"fixture.json").is_file()]) if (root/"operational-fixtures").is_dir() else 0}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="also run extended schema and contract validation (current validator always checks required package contracts)")
    parser.add_argument("--root", default=str(ROOT), help="package root for mutation tests")
    args=parser.parse_args()
    root=Path(args.root).resolve()
    errors,warnings,summary=validate(root)
    for warning in warnings: print("WARNING:",warning)
    if errors:
        print("VALIDATION FAILED")
        for error in errors: print("ERROR:",error)
        return 1
    print(json.dumps({"status":"structurally_valid","behavioral_quality":"not established by structural validation","summary":summary,"warnings":warnings},indent=2))
    return 0
if __name__=="__main__": sys.exit(main())
