#!/usr/bin/env python3
"""Evidence-bound local task runtime for Elite Engineering Suite v0.9.0.

The runtime never invokes arbitrary user-supplied shell text. `run-check` executes
only commands declared in checks/catalog.json, without a shell, with a timeout.
Approval records are self-attested local records; this tool does not authenticate
people or enforce operating-system-level permissions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.10.0"
REGISTRY_PATH = ROOT / "capability-registry.json"
CATALOG_PATH = ROOT / "checks" / "catalog.json"
ROUTING_PATH = ROOT / "hierarchical-routing.json"
try:
    REG = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    SKILLS = {c["id"]: c for c in REG["capabilities"]}
    CATALOG_DOC = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    CHECKS = {c["check_id"]: c for c in CATALOG_DOC["checks"]}
    ROUTING_DOC = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
    ROUTE_BY_SKILL = {sid: route["id"] for route in ROUTING_DOC["stage1_routes"] for sid in route["skills"]}
except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
    raise SystemExit(f"Invalid runtime configuration: {exc}")

STATES = {"PLANNED", "ROUTED", "GATED", "RUNNING", "YIELD_FOR_REROUTE", "VERIFYING",
          "PASSED", "FAILED", "BLOCKED", "PARTIAL", "UNVERIFIED", "RECOVERY_REQUIRED", "BUDGET_EXCEEDED"}
ALLOWED = {
    "PLANNED": {"ROUTED", "BLOCKED"}, "ROUTED": {"GATED", "BLOCKED"},
    "GATED": {"RUNNING", "BLOCKED"},
    "RUNNING": {"VERIFYING", "YIELD_FOR_REROUTE", "FAILED", "BLOCKED", "RECOVERY_REQUIRED", "BUDGET_EXCEEDED"},
    "YIELD_FOR_REROUTE": {"ROUTED", "BLOCKED"},
    "VERIFYING": {"PASSED", "PARTIAL", "FAILED", "BLOCKED", "UNVERIFIED", "RECOVERY_REQUIRED"},
    "FAILED": {"RECOVERY_REQUIRED", "BLOCKED"}, "RECOVERY_REQUIRED": {"PLANNED", "BLOCKED"},
    "BLOCKED": {"PLANNED", "BLOCKED"}, "PASSED": set(),
    "PARTIAL": {"RECOVERY_REQUIRED"}, "UNVERIFIED": {"PLANNED", "BLOCKED"},
    "BUDGET_EXCEEDED": {"BLOCKED", "RECOVERY_REQUIRED"},
}
GENESIS = "0" * 64


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def now() -> str:
    return utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def tree_digest(path: Path, exclude_rel: str | None = None) -> str | None:
    if not path.exists() or not path.is_dir():
        return None
    h = hashlib.sha256()
    volatile_dirs = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".venv", "venv", "node_modules"}
    for f in sorted(x for x in path.rglob("*") if x.is_file() and not any(part in volatile_dirs for part in x.parts) and x.suffix != ".pyc" and not x.name.endswith(".tmp")):
        rel = f.relative_to(path)
        if exclude_rel and (rel.as_posix() == exclude_rel or rel.as_posix().startswith(exclude_rel.rstrip("/") + "/")):
            continue
        h.update(rel.as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(bytes.fromhex(digest_file(f)))
    return h.hexdigest()


def atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try: os.unlink(tmp_name)
        except OSError: pass
        raise


def write_json(path: Path, value) -> None:
    atomic_write(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def outdir(args) -> Path:
    p = Path(args.out_dir).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p


def event_payload(event: dict) -> dict:
    return {k: v for k, v in event.items() if k != "event_hash"}


def verify_event_chain(events: list) -> None:
    prev = GENESIS
    if not isinstance(events, list):
        raise ValueError("event ledger must be an array")
    for i, item in enumerate(events, start=1):
        if not isinstance(item, dict) or item.get("revision") != i:
            raise ValueError(f"event ledger revision invalid at event {i}")
        if item.get("previous_hash") != prev:
            raise ValueError(f"event ledger chain broken at event {i}")
        expected = digest_bytes(canonical(event_payload(item)))
        if item.get("event_hash") != expected:
            raise ValueError(f"event ledger hash mismatch at event {i}")
        prev = expected


def event(state: dict, kind: str, **data) -> None:
    events = state.setdefault("events", [])
    prev = events[-1]["event_hash"] if events else GENESIS
    item = {"revision": len(events) + 1, "timestamp": now(), "type": kind, "previous_hash": prev, **data}
    item["event_hash"] = digest_bytes(canonical(item))
    events.append(item)


def save(state: dict, d: Path) -> None:
    verify_event_chain(state.get("events", []))
    write_json(d / "task-state.json", state)
    events = state["events"]
    write_json(d / "execution-state.json", {
        "schema_version": VERSION,
        "task_id": state["task_id"],
        "event_count": len(events),
        "head_hash": events[-1]["event_hash"] if events else GENESIS,
        "events": events,
        "tamper_evidence_note": "Hash chain detects accidental or partial edits; it is not a signed or externally anchored audit log.",
    })


def load_state(d: Path) -> dict:
    p = d / "task-state.json"
    if not p.is_file():
        raise ValueError(f"missing state: {p}")
    state = json.loads(p.read_text(encoding="utf-8"))
    if state.get("package_version") != VERSION:
        raise ValueError(f"state version mismatch: expected {VERSION}; found {state.get('package_version')}")
    verify_event_chain(state.get("events", []))
    ep = d / "execution-state.json"
    if not ep.is_file():
        raise ValueError("execution-state.json is missing; ledger pair is incomplete")
    execution = json.loads(ep.read_text(encoding="utf-8"))
    events = state.get("events", [])
    head = events[-1]["event_hash"] if events else GENESIS
    if execution.get("task_id") != state.get("task_id") or execution.get("event_count") != len(events) or execution.get("head_hash") != head or execution.get("events") != events:
        raise ValueError("task-state and execution-state ledger mismatch")
    return state


def transition(state: dict, to: str, reason: str = "") -> None:
    current = state.get("state")
    if to not in ALLOWED.get(current, set()):
        raise ValueError(f"invalid transition {current} -> {to}")
    state["state"] = to
    event(state, "state_change", from_state=current, to_state=to, reason=reason)


def _signal_pattern(signal):
    if isinstance(signal, str):
        return re.escape(signal), 1.0
    if isinstance(signal, dict):
        pattern = signal.get("pattern", "")
        weight = signal.get("weight", signal.get("penalty", 0))
        return str(pattern), float(weight)
    return "", 0.0


def _score(c: dict, text: str):
    positive, negative = [], []
    raw_pos = raw_neg = 0.0
    for item in c.get("positive_signals", []):
        pattern, weight = _signal_pattern(item)
        if pattern:
            try: matched = re.search(pattern, text, re.I) is not None
            except re.error: matched = pattern.lower() in text.lower()
            if matched:
                positive.append(pattern)
                raw_pos += abs(weight) if weight else 1.0
    for item in c.get("negative_signals", []):
        pattern, penalty = _signal_pattern(item)
        if pattern:
            try: matched = re.search(pattern, text, re.I) is not None
            except re.error: matched = pattern.lower() in text.lower()
            if matched:
                negative.append(pattern)
                raw_neg += abs(penalty) if penalty else 1.0
    score = raw_pos - raw_neg
    threshold = float(c.get("activation_threshold", 1.0))
    return score, threshold, positive, negative


def classify_task_risk(request: str) -> str:
    """Conservative task-level risk classifier, independent of skill relevance."""
    q = request.lower()
    critical = [r"\bdrop\s+(?:(?:the|all|production|prod)\s+)*(?:database|table)\b", r"\bdrop\s+table\b", r"\btruncate\s+table\b", r"\bdelete\s+all\b", r"\bwipe(?:\s+(?:the\s+)?(?:disk|database|production))?\b", r"\bdestroy\s+(?:all|production|prod|infrastructure)\b", r"\bterraform\s+destroy\b", r"\bproduction\s+data\s+deletion\b", r"\bdelete\s+production\s+(?:data|records|users|files)\b", r"\brotate\s+all\s+keys\b"]
    high = [r"\bproduction\b", r"\bprod\s+(?:database|environment|deploy|deployment)\b", r"\bdeploy(?:ment)?\b", r"\brelease\b", r"\bpublish\b", r"\bmigration\b", r"\bpenetration\s+test\b", r"\bsecurity\s+(?:test|testing|assessment|audit|scan)\b", r"\bpen.?test\b", r"\bexternal\s+(?:target|system|website|api)\b", r"\bpayment\b", r"\bbilling\b", r"\bpersonal\s+data\b", r"\bcredentials?\b", r"\bsecret\s+keys?\b", r"\bdelete\s+(?:records|users|files)\b", r"\baccess[- ]control change\b", r"\bidentity provider\b", r"\bdatabase restore\b"]
    if any(re.search(p, q) for p in critical): return "critical"
    if any(re.search(p, q) for p in high): return "high"
    if re.search(r"\b(read-only|read only|documentation|formatting|explain|summarize|typo)\b", q) and not re.search(r"\b(implement|modify|change|write|fix|refactor|code|test)\b", q):
        return "low"
    return "medium"


def route(request: str) -> dict:
    text = request.lower()
    scored = {}
    for sid, c in SKILLS.items():
        score, threshold, positive, negative = _score(c, text)
        scored[sid] = {"skill_id": sid, "score": round(score, 4), "threshold": threshold,
                       "matched": positive, "discounts": negative, "risk_class": c.get("risk_class", "medium"),
                       "selected": False, "activation_basis": "signal-score"}
    # Stage 1: rank route groups from their specialist signal scores. Stage 2: select
    # specialists only from activated groups. The routing manifest is validated at startup.
    route_scores = {}
    for route in ROUTING_DOC["stage1_routes"]:
        members = [scored[sid] for sid in route["skills"]]
        route_scores[route["id"]] = {"route_id": route["id"], "name": route["name"],
            "score": max((m["score"] for m in members), default=0.0),
            "matched_skills": [m["skill_id"] for m in members if m["matched"]]}
    active_routes = {rid for rid, r in route_scores.items() if r["matched_skills"]}
    selected = {sid for sid, x in scored.items() if sid in ROUTE_BY_SKILL and ROUTE_BY_SKILL[sid] in active_routes and x["score"] >= x["threshold"] and x["matched"]}
    if not selected:
        ranked = sorted((x for x in scored.values() if x["score"] > 0), key=lambda x: (-x["score"], x["skill_id"]))
        if not ranked:
            raise ValueError("no capability matched this request; add a clear domain term or extend the registry")
        best = ranked[0]
        selected.add(best["skill_id"])
        best["activation_basis"] = "best-positive-match-fallback-review-required"
        active_routes.add(ROUTE_BY_SKILL[best["skill_id"]])
    # Security floor: high/critical tasks cannot be routed without explicit security
    # review capabilities, even when first-stage semantic cues are incomplete.
    task_risk = classify_task_risk(request)
    security_floor = {"security-review", "defensive-appsec-assessment", "prompt-provenance-and-safety"}
    if task_risk in {"high", "critical"}:
        for sid in security_floor:
            if sid in SKILLS:
                selected.add(sid)
                active_routes.add(ROUTE_BY_SKILL[sid])
                scored[sid]["activation_basis"] = "mandatory-security-risk-floor"
    # Close dependencies and co-activation relationships transitively.
    queue = list(sorted(selected))
    while queue:
        sid = queue.pop(0)
        c = SKILLS[sid]
        refs = list(c.get("dependencies", [])) + list(c.get("must_run_with", []))
        for ref in refs:
            if ref not in SKILLS:
                raise ValueError(f"capability {sid} references unknown dependency {ref}")
            if ref not in selected:
                selected.add(ref); queue.append(ref)
    for sid in sorted(selected):
        conflicts = set(SKILLS[sid].get("conflicts_with", [])) & selected
        if conflicts:
            raise ValueError(f"selected capabilities conflict: {sid} conflicts with {sorted(conflicts)}")
    # Build edges prerequisite -> dependent. must_run_before only applies when both are selected.
    prerequisites = {sid: set(SKILLS[sid].get("dependencies", [])) & selected for sid in selected}
    for sid in selected:
        for after in SKILLS[sid].get("must_run_after", []):
            if after in selected: prerequisites[sid].add(after)
        for before in SKILLS[sid].get("must_run_before", []):
            if before in selected: prerequisites[before].add(sid)
    order, remaining = [], {k: set(v) for k, v in prerequisites.items()}
    while remaining:
        ready = sorted(k for k, v in remaining.items() if not v)
        if not ready:
            raise ValueError("dependency/order cycle among selected skills: " + ", ".join(sorted(remaining)))
        order.extend(ready)
        for k in ready: remaining.pop(k)
        for v in remaining.values(): v.difference_update(ready)
    for sid in selected: scored[sid]["selected"] = True
    return {
        "request": request,
        "algorithm": "two-stage-hierarchical-regex-signal-score-v2",
        "routing_release": ROUTING_DOC.get("release"),
        "stage1_routes": [route_scores[rid] for rid in sorted(active_routes)],
        "security_floor_applied": task_risk in {"high", "critical"},
        "selected_skills": order,
        "fallback_used": any(scored[s]["activation_basis"] != "signal-score" for s in selected),
        "confidence": None,
        "confidence_note": "Not statistically calibrated; no probability claim is made.",
        "task_risk": task_risk,
        "scores": sorted(scored.values(), key=lambda x: (-x["score"], x["skill_id"])),
        "dag": {sid: sorted(prerequisites[sid]) for sid in order},
    }


def check_catalog_entry(check_id: str) -> dict:
    if check_id not in CHECKS:
        raise ValueError(f"action/check {check_id!r} is not allowlisted in checks/catalog.json")
    check = CHECKS[check_id]
    runner = check.get("runner")
    if not isinstance(runner, str) or not runner:
        raise ValueError(f"allowlisted check {check_id!r} has no runner")
    runner_path = (ROOT / runner).resolve()
    try: runner_path.relative_to(ROOT.resolve())
    except ValueError: raise ValueError("check runner escapes package root")
    if not runner_path.is_file(): raise ValueError(f"check runner is missing: {runner}")
    expected_hash = check.get("runner_sha256")
    if not isinstance(expected_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", expected_hash):
        raise ValueError(f"check {check_id!r} has no valid runner_sha256 integrity pin")
    actual_hash = digest_file(runner_path)
    if actual_hash != expected_hash:
        raise ValueError(f"check runner integrity mismatch for {runner}; update and review the catalog pin")
    return check


def resolve_artifact(ref: str, state: dict, d: Path) -> tuple[Path, str]:
    if not isinstance(ref, str) or ":" not in ref:
        raise ValueError("artifact must use an explicit repo:relative/path or out:relative/path reference")
    namespace, rel = ref.split(":", 1)
    if namespace == "repo": base = Path(state["repository"]["path"]).resolve()
    elif namespace == "out": base = d.resolve()
    else: raise ValueError("artifact namespace must be repo: or out:")
    if not rel or Path(rel).is_absolute(): raise ValueError("artifact path must be relative")
    target = (base / rel).resolve()
    try: target.relative_to(base)
    except ValueError: raise ValueError("artifact path escapes its allowed base")
    if not target.is_file(): raise ValueError(f"artifact file does not exist: {ref}")
    return target, f"{namespace}:{target.relative_to(base).as_posix()}"


def artifact_record(ref: str, state: dict, d: Path) -> dict:
    path, normalized = resolve_artifact(ref, state, d)
    return {"artifact_ref": normalized, "artifact_sha256": digest_file(path), "artifact_bytes": path.stat().st_size}


def artifact_is_unchanged(entry: dict, state: dict, d: Path) -> tuple[bool, str]:
    try:
        path, _ = resolve_artifact(entry["artifact_ref"], state, d)
        current = digest_file(path)
        if current != entry.get("artifact_sha256"):
            return False, f"artifact hash changed: {entry['artifact_ref']}"
        return True, ""
    except (ValueError, OSError, KeyError) as exc:
        return False, str(exc)


def valid_approval(state: dict) -> tuple[bool, str]:
    required = state.get("approval_required", False)
    if not required: return True, "approval not required by task-risk policy"
    for approval in reversed(state.get("approvals", [])):
        try:
            if approval.get("task_id") != state.get("task_id"): continue
            scope = approval.get("scope", "")
            if state["task_id"] not in scope: continue
            if approval.get("target") != state.get("repository", {}).get("path"): continue
            if not approval.get("objective", "").strip() or not approval.get("review_record", "").strip(): continue
            request_tokens = set(re.findall(r"[a-z0-9]+", state.get("request", "").lower()))
            stop = {"task", "please", "make", "create", "implement", "update", "fix", "change", "test", "testing", "run", "verify", "check", "for", "the", "and", "with", "from", "into", "only", "audit", "review", "using", "current", "my", "project", "perform", "do", "a", "an", "of", "to", "in", "on", "at", "is", "are", "be", "it"}
            request_terms = {x for x in request_tokens if len(x) >= 4 and x not in stop}
            scope_terms = set(re.findall(r"[a-z0-9]+", scope.lower()))
            overlap = request_terms & scope_terms
            if request_terms and len(overlap) < min(2, len(request_terms)): continue
            expires = date.fromisoformat(approval.get("expires", ""))
            if expires < utc_now().date(): continue
            if not approval.get("approved_by", "").strip(): continue
            if not approval.get("approval_id"): continue
            return True, f"valid self-attested approval {approval['approval_id']}"
        except (ValueError, TypeError):
            continue
    return False, "missing, expired, malformed, or out-of-scope approval record"


def init(args) -> int:
    d = outdir(args)
    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir(): raise ValueError(f"repository path is not a directory: {repo}")
    if not args.acceptance: raise ValueError("at least one --acceptance criterion is required before routing")
    if len(args.acceptance) != len(set(args.acceptance)): raise ValueError("acceptance criteria must be unique")
    r = route(args.request)
    risk = r["task_risk"]
    try: excluded_output_dir = d.relative_to(repo).as_posix()
    except ValueError: excluded_output_dir = None
    try: package_output_exclusion = d.relative_to(ROOT).as_posix()
    except ValueError: package_output_exclusion = None
    state = {
        "task_id": args.task_id, "package": "elite-engineering-suite", "package_version": VERSION,
        "request": args.request, "state": "PLANNED",
        "repository": {"path": str(repo), "tree_hash_at_route": tree_digest(repo, excluded_output_dir), "tree_hash_exclusion": excluded_output_dir, "branch": None, "commit": None},
        "package_integrity": {"root": str(ROOT.resolve()), "tree_hash_at_route": tree_digest(ROOT, package_output_exclusion), "tree_hash_exclusion": package_output_exclusion},
        "acceptance_criteria": args.acceptance,
        "criterion_results": [{"index": i + 1, "criterion": criterion, "status": "pending", "evidence_ref": None, "evidence_sha256": None, "note": None} for i, criterion in enumerate(args.acceptance)],
        "selected_skills": r["selected_skills"], "route": r, "dag": r["dag"],
        "task_risk": risk, "approval_required": risk in {"high", "critical"},
        "budget": {"tool_calls": 0, "max_tool_calls": 40, "retries": 0, "reroutes": 0, "max_reroutes": 2, "files": 0, "max_files": 80},
        "approvals": [], "actions": [], "side_effects": [], "evidence": [], "failures": [], "reroutes": [],
        "rollback_recovery": {"plan": None, "tested": False},
        "next_safe_action": "review routed skills and plan; obtain task-scoped approval if required",
        "safe_to_resume": True, "events": [],
    }
    event(state, "created", request=args.request, repo_tree_hash=state["repository"]["tree_hash_at_route"])
    state["state"] = "ROUTED"
    event(state, "routed", selected=r["selected_skills"], task_risk=risk, approval_required=state["approval_required"])
    save(state, d)
    write_json(d / "route-decision.json", r)
    print(json.dumps({"state": state["state"], "selected_skills": r["selected_skills"], "task_risk": risk,
                      "approval_required": state["approval_required"], "fallback_used": r["fallback_used"],
                      "routing_algorithm": r["algorithm"], "routing_release": r["routing_release"],
                      "stage1_routes": [x["route_id"] for x in r.get("stage1_routes", [])],
                      "security_floor_applied": r.get("security_floor_applied", False)}, indent=2))
    return 0


def perform_approve(args, state: dict, d: Path) -> None:
    if state.get("state") not in {"ROUTED", "GATED", "BLOCKED"}:
        raise ValueError("approval can only be recorded before execution while task is ROUTED, GATED, or BLOCKED")
    if not state.get("approval_required"):
        raise ValueError("approval is not required by the current task-risk classification")
    approved_by = args.approved_by.strip()
    scope = args.scope.strip()
    target = str(Path(args.target).expanduser().resolve())
    objective = args.objective.strip()
    review_record = args.review_record.strip()
    if not approved_by: raise ValueError("--approved-by must be non-empty")
    if state["task_id"] not in scope: raise ValueError("--scope must explicitly include the task ID")
    if target != state["repository"]["path"]: raise ValueError("--target must exactly match the task repository path")
    if not objective: raise ValueError("--objective must be non-empty")
    if not review_record: raise ValueError("--review-record must identify the review/approval record")
    try: exp = date.fromisoformat(args.expires)
    except ValueError as exc: raise ValueError("--expires must be YYYY-MM-DD") from exc
    if exp < utc_now().date(): raise ValueError("approval expiry date is in the past")
    stamp = now()
    aid = digest_bytes(f"{state['task_id']}|{approved_by}|{scope}|{target}|{objective}|{review_record}|{exp.isoformat()}|{stamp}".encode())[:20]
    rec = {"approval_id": aid, "task_id": state["task_id"], "approved_by": approved_by, "scope": scope,
           "target": target, "objective": objective, "review_record": review_record,
           "expires": exp.isoformat(), "recorded_at": stamp, "authentication": "self-attested; identity not externally verified"}
    state.setdefault("approvals", []).append(rec)
    event(state, "approval_recorded", approval_id=aid, approved_by=approved_by, scope=scope, target=target,
          objective=objective, review_record=review_record, expires=exp.isoformat())
    if state["state"] == "BLOCKED":
        transition(state, "PLANNED", "new approval recorded; reroute/plan required")
        transition(state, "ROUTED", "resume planning after approval")
        state["next_safe_action"] = "review plan and run plan command"


def perform_record_action(args, state: dict, d: Path) -> None:
    """Record a manual/planned action. This can never count as execution evidence."""
    if state["state"] != "RUNNING": raise ValueError("record-action requires RUNNING")
    check = check_catalog_entry(args.action_id)
    if args.idempotency_key and any(x.get("idempotency_key") == args.idempotency_key for x in state["actions"]):
        raise ValueError("duplicate idempotency key")
    state["budget"]["tool_calls"] += 1
    if state["budget"]["tool_calls"] > state["budget"]["max_tool_calls"]:
        transition(state, "BUDGET_EXCEEDED", "tool-call budget exceeded")
        event(state, "budget_exceeded", budget="tool_calls")
        return
    act = {"action_id": args.action_id, "check_id": check["check_id"], "mode": "manual-action-not-evidence",
           "timestamp": now(), "idempotency_key": args.idempotency_key,
           "note": "Manual/planned record only; cannot establish that a check ran or passed."}
    state["actions"].append(act)
    event(state, "manual_action_recorded", action=act)


def perform_run_check(args, state: dict, d: Path) -> int:
    if state["state"] != "RUNNING": raise ValueError("run-check requires RUNNING")
    repo = Path(state["repository"]["path"])
    current_repo_hash = tree_digest(repo, state["repository"].get("tree_hash_exclusion"))
    expected_repo_hash = state["repository"].get("tree_hash_at_route")
    if current_repo_hash != expected_repo_hash:
        transition(state, "BLOCKED", "repository tree changed after routing; check was not executed")
        event(state, "repository_integrity_failure", expected=expected_repo_hash, actual=current_repo_hash, check_id=args.check_id)
        print(json.dumps({"result": "blocked", "reason": "repository tree changed after routing; check was not executed"}, indent=2))
        return 2
    package_hash = tree_digest(ROOT, state.get("package_integrity", {}).get("tree_hash_exclusion"))
    if package_hash != state.get("package_integrity", {}).get("tree_hash_at_route"):
        transition(state, "BLOCKED", "runtime package integrity changed after routing; check was not executed")
        event(state, "package_integrity_failure", expected=state.get("package_integrity", {}).get("tree_hash_at_route"), actual=package_hash, check_id=args.check_id)
        print(json.dumps({"result":"blocked","reason":"runtime package tree changed; check was not executed"},indent=2))
        return 2
    if state["budget"]["tool_calls"] >= state["budget"]["max_tool_calls"]:
        transition(state, "BUDGET_EXCEEDED", "tool-call budget would be exceeded; check not executed")
        event(state, "budget_exceeded", budget="tool_calls", action=args.check_id, executed=False)
        print(json.dumps({"result":"blocked","reason":"tool-call budget exceeded; command was not executed"},indent=2))
        return 2
    check = check_catalog_entry(args.check_id)
    extra = check.get("argv", [])
    if not isinstance(extra, list) or any(not isinstance(x, str) for x in extra):
        raise ValueError("allowlisted check argv must be a list of strings")
    runner = (ROOT / check["runner"]).resolve()
    timeout = min(max(int(check.get("timeout_seconds", 120)), 1), 300)
    run_dir = d / "runs"; run_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", args.check_id)
    stdout_path = run_dir / f"{safe_name}.stdout.txt"
    stderr_path = run_dir / f"{safe_name}.stderr.txt"
    argv_tail = [x.replace("@OUT_DIR@", str(d.resolve())) for x in extra]
    run_argv = [sys.executable, str(runner), *argv_tail]
    started = now()
    # Start a separate process group so timeout handling can stop the runner and
    # its descendants. Killing only the direct child can leave inherited pipes open.
    proc = subprocess.Popen(
        run_argv, cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=False, start_new_session=(os.name == "posix"), close_fds=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        code = proc.returncode
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        else:
            proc.kill()
        stdout, stderr = proc.communicate()
        code = 124
        stderr = (stderr or "") + f"\nTimed out after {timeout}s; runner process group terminated where supported"
    atomic_write(stdout_path, stdout)
    atomic_write(stderr_path, stderr)
    expected = int(check.get("expected_exit_code", 0))
    art = {"artifact_ref": f"out:runs/{stdout_path.name}", "artifact_sha256": digest_file(stdout_path), "artifact_bytes": stdout_path.stat().st_size}
    act = {"action_id": args.check_id, "check_id": args.check_id, "mode": "executed", "command_argv": run_argv,
           "command_sha256": digest_bytes(canonical(run_argv)), "runner_sha256": check["runner_sha256"],
           "expected_exit_code": expected, "exit_code": code, **art,
           "stderr_ref": f"out:runs/{stderr_path.name}", "stderr_sha256": digest_file(stderr_path),
           "started_at": started, "finished_at": now(), "timeout_seconds": timeout,
           "python_version": sys.version.split()[0], "platform": platform.platform(),
           "result": "pass" if code == expected else "fail"}
    state["budget"]["tool_calls"] += 1
    if state["budget"]["tool_calls"] > state["budget"]["max_tool_calls"]:
        transition(state, "BUDGET_EXCEEDED", "tool-call budget exceeded")
    else:
        state["actions"].append(act)
        event(state, "catalogued_check_executed", check_id=args.check_id, exit_code=code, expected_exit_code=expected,
              command_sha256=act["command_sha256"], runner_sha256=act["runner_sha256"], artifact_ref=act["artifact_ref"],
              artifact_sha256=act["artifact_sha256"], stderr_ref=act["stderr_ref"], stderr_sha256=act["stderr_sha256"])
    print(json.dumps({"check_id": args.check_id, "expected_exit_code": expected, "actual_exit_code": code,
                      "result": act["result"], "stdout_artifact": act["artifact_ref"], "stderr_artifact": act["stderr_ref"]}, indent=2))
    return 0 if code == expected else 1


def perform_criterion(args, state: dict, d: Path) -> None:
    if state["state"] != "RUNNING": raise ValueError("record-criterion requires RUNNING")
    if args.index < 1 or args.index > len(state.get("criterion_results", [])):
        raise ValueError("criterion index is outside the acceptance-criteria list")
    record = state["criterion_results"][args.index - 1]
    art = artifact_record(args.evidence, state, d)
    record.update({"status": args.status, "evidence_ref": art["artifact_ref"], "evidence_sha256": art["artifact_sha256"], "note": args.note})
    event(state, "acceptance_criterion_recorded", index=args.index, status=args.status, criterion=record["criterion"],
          evidence_ref=record["evidence_ref"], evidence_sha256=record["evidence_sha256"])


def verify_task(state: dict, d: Path) -> tuple[str, list[str]]:
    problems = []
    actions = state.get("actions", [])
    verified_actions = []
    hard_failure = False
    for i, act in enumerate(actions, 1):
        if act.get("mode") != "executed":
            continue
        if act.get("exit_code") != act.get("expected_exit_code", 0):
            problems.append(f"action {i} ({act.get('action_id')}) exit code {act.get('exit_code')} != expected {act.get('expected_exit_code', 0)}")
            hard_failure = True
            continue
        unchanged, msg = artifact_is_unchanged(act, state, d)
        if not unchanged:
            problems.append(f"action {i} artifact invalid: {msg}")
            hard_failure = True
        else: verified_actions.append(act)
        if act.get("stderr_ref"):
            unchanged, msg = artifact_is_unchanged({"artifact_ref": act["stderr_ref"], "artifact_sha256": act.get("stderr_sha256")}, state, d)
            if not unchanged:
                problems.append(f"action {i} stderr artifact invalid: {msg}")
                hard_failure = True
    if not actions: problems.append("no action evidence")
    elif not verified_actions: problems.append("no successfully executed, artifact-backed action")
    criteria = state.get("criterion_results", [])
    if not criteria: problems.append("no acceptance criteria recorded")
    for c in criteria:
        if c.get("status") == "pending": problems.append(f"acceptance criterion {c.get('index')} remains pending")
        elif c.get("status") != "pass": problems.append(f"acceptance criterion {c.get('index')} did not pass")
        else:
            unchanged, msg = artifact_is_unchanged({"artifact_ref": c.get("evidence_ref"), "artifact_sha256": c.get("evidence_sha256")}, state, d)
            if not unchanged: problems.append(f"acceptance criterion {c.get('index')} evidence invalid: {msg}")
    if any(c.get("status") == "fail" for c in criteria): return "FAILED", problems
    if hard_failure: return "FAILED", problems
    if not problems: return "PASSED", []
    return "UNVERIFIED", problems



def signed_attestation_check(args, state: dict, repo_hash: str) -> tuple[bool, dict, str]:
    """Fail-closed verification of a signed evidence manifest bound to this task and tree."""
    signed_path = getattr(args, "signed_evidence", None)
    public_path = getattr(args, "public_key", None)
    required = getattr(args, "required_check", []) or []
    if not signed_path or not public_path or not required:
        return False, {}, "signed evidence, public key, and at least one required check are mandatory"
    signed_path = Path(signed_path).expanduser().resolve()
    public_path = Path(public_path).expanduser().resolve()
    if not signed_path.is_file() or not public_path.is_file():
        return False, {}, "signed evidence or public key file is missing"
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "contract_verifier.py"),
             "verify-policy", "--signed", str(signed_path), "--public-key", str(public_path),
             *sum((["--required-check", check] for check in required), [])],
            cwd=str(ROOT), capture_output=True, text=True, timeout=15, check=False,
        )
        policy = json.loads(proc.stdout) if proc.stdout.strip() else {}
        if proc.returncode != 0 or policy.get("decision") != "PASS":
            return False, policy, "signed evidence policy did not PASS"
        envelope = json.loads(signed_path.read_text(encoding="utf-8"))
        manifest = envelope.get("payload", {})
        if manifest.get("run_id") != state.get("task_id"):
            return False, policy, "signed evidence run_id does not match task_id"
        if manifest.get("package_version") != VERSION:
            return False, policy, "signed evidence package_version does not match runtime version"
        if manifest.get("subject", {}).get("sha256") != repo_hash:
            return False, policy, "signed evidence subject hash does not match verified repository tree"
        attestation = {
            "status": "PASS", "run_id": manifest["run_id"], "package_version": manifest["package_version"],
            "subject_sha256": manifest["subject"]["sha256"], "required_checks": sorted(set(required)),
            "signed_manifest_path": str(signed_path), "signed_manifest_sha256": digest_file(signed_path),
            "public_key_path": str(public_path), "public_key_sha256": digest_file(public_path),
            "policy_version": policy.get("policy_version", 1), "verified_at": now(),
        }
        return True, attestation, ""
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        return False, {}, f"signed evidence verification error: {exc}"


def revalidate_saved_attestation(state: dict, repo_hash: str) -> tuple[bool, str]:
    att = state.get("contract_attestation")
    if not isinstance(att, dict) or att.get("status") != "PASS":
        return False, "missing independently verified signed evidence attestation"
    try:
        signed_path = Path(att["signed_manifest_path"])
        public_path = Path(att["public_key_path"])
        if not signed_path.is_file() or not public_path.is_file():
            return False, "signed evidence or public key is no longer available"
        if digest_file(signed_path) != att.get("signed_manifest_sha256"):
            return False, "signed evidence file changed after verification"
        if digest_file(public_path) != att.get("public_key_sha256"):
            return False, "verification public key changed after verification"
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "contract_verifier.py"),
             "verify-policy", "--signed", str(signed_path), "--public-key", str(public_path),
             *sum((["--required-check", check] for check in att.get("required_checks", [])), [])],
            cwd=str(ROOT), capture_output=True, text=True, timeout=15, check=False,
        )
        policy = json.loads(proc.stdout) if proc.stdout.strip() else {}
        if proc.returncode != 0 or policy.get("decision") != "PASS":
            return False, "saved signed evidence policy no longer passes"
        manifest = json.loads(signed_path.read_text(encoding="utf-8")).get("payload", {})
        if manifest.get("run_id") != state.get("task_id"):
            return False, "saved attestation task id mismatch"
        if manifest.get("package_version") != VERSION:
            return False, "saved attestation package version mismatch"
        if manifest.get("subject", {}).get("sha256") != repo_hash:
            return False, "saved attestation does not match current repository tree"
        return True, ""
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        return False, f"saved attestation revalidation error: {exc}"


def cmd(args) -> int:
    d = outdir(args)
    state = load_state(d)
    if args.command == "plan":
        if not state.get("acceptance_criteria"): raise ValueError("cannot plan without acceptance criteria")
        transition(state, "GATED", "plan recorded; acceptance criteria locked")
        state["next_safe_action"] = "obtain task-scoped approval if required, then start"
    elif args.command == "approve":
        perform_approve(args, state, d)
    elif args.command == "start":
        repo = Path(state["repository"]["path"])
        current_tree = tree_digest(repo, state["repository"].get("tree_hash_exclusion"))
        current_package_tree = tree_digest(ROOT, state.get("package_integrity", {}).get("tree_hash_exclusion"))
        if current_tree != state["repository"].get("tree_hash_at_route"):
            transition(state, "BLOCKED", "repository tree changed after routing; reroute and review before execution")
            state["repository"]["tree_hash_at_start"] = current_tree
            state["next_safe_action"] = "review repository changes and create a fresh route/task state"
        elif current_package_tree != state.get("package_integrity", {}).get("tree_hash_at_route"):
            transition(state, "BLOCKED", "runtime package changed after routing; review package integrity before execution")
            state["package_integrity"]["tree_hash_at_start"] = current_package_tree
            state["next_safe_action"] = "restore or revalidate the package and create a fresh task state"
        else:
            ok, why = valid_approval(state)
            if not ok:
                transition(state, "BLOCKED", why)
                state["next_safe_action"] = "record a valid task-scoped approval, then plan and start again"
            else:
                state["repository"]["tree_hash_at_start"] = current_tree
                transition(state, "RUNNING", "start gate passed: " + why)
                state["next_safe_action"] = "execute allowlisted checks and record evidence for each acceptance criterion"
    elif args.command == "record-action":
        perform_record_action(args, state, d)
    elif args.command == "run-check":
        rc = perform_run_check(args, state, d)
        save(state, d)
        return rc
    elif args.command == "record-criterion":
        perform_criterion(args, state, d)
    elif args.command == "verify":
        transition(state, "VERIFYING", "verification requested")
        result, problems = verify_task(state, d)
        repo = Path(state["repository"]["path"])
        verified_repo_hash = tree_digest(repo, state["repository"].get("tree_hash_exclusion"))
        state["repository"]["tree_hash_at_verify"] = verified_repo_hash
        if verified_repo_hash != state["repository"].get("tree_hash_at_route"):
            result = "FAILED"
            problems.append("repository tree changed since routing; evidence is not valid for the reviewed snapshot")
        strict_contract = os.environ.get("EES_REQUIRE_SIGNED_EVIDENCE", "1").strip().lower() not in {"0", "false", "no", "off"}
        if result == "PASSED" and strict_contract:
            att_ok, attestation, att_problem = signed_attestation_check(args, state, verified_repo_hash or "")
            if not att_ok:
                result = "BLOCKED"
                problems.append("contract attestation gate: " + att_problem)
                state.pop("contract_attestation", None)
            else:
                state["contract_attestation"] = attestation
                event(state, "contract_attestation_verified", run_id=attestation["run_id"],
                      subject_sha256=attestation["subject_sha256"],
                      signed_manifest_sha256=attestation["signed_manifest_sha256"],
                      required_checks=attestation["required_checks"])
        if result != "PASSED": state["failures"].extend(x for x in problems if x not in state["failures"])
        transition(state, result, "; ".join(problems) if problems else "all recorded acceptance criteria and artifact-backed checks verified")
        state["safe_to_resume"] = result != "PASSED"
        state["next_safe_action"] = "release-decision" if result == "PASSED" else "resolve evidence gaps or recover; do not claim success"
    elif args.command == "recover":
        if state["state"] not in {"FAILED", "BLOCKED", "PARTIAL", "UNVERIFIED", "RECOVERY_REQUIRED", "BUDGET_EXCEEDED"}:
            raise ValueError("recover requires unresolved state")
        transition(state, "RECOVERY_REQUIRED", "recovery plan recorded")
        state["rollback_recovery"] = {"plan": args.plan, "tested": False, "recorded_at": now()}
        state["next_safe_action"] = "test recovery plan in an isolated safe environment"
    elif args.command == "resume":
        if state["state"] not in {"RECOVERY_REQUIRED", "UNVERIFIED", "BLOCKED"}:
            raise ValueError("resume requires recovery, unverified, or blocked state")
        if not args.change_record.strip(): raise ValueError("resume requires a non-empty change record")
        transition(state, "PLANNED", "resume change record accepted")
        event(state, "change_record", value=args.change_record)
        transition(state, "ROUTED", "existing route retained for reviewed recovery")
        state["safe_to_resume"] = True
        state["next_safe_action"] = "review plan and run plan command"
    else:
        raise ValueError("unknown command")
    save(state, d)
    print(json.dumps({"state": state["state"], "next_safe_action": state.get("next_safe_action"),
                      "event_count": len(state["events"])}, indent=2))
    return 0


def release(args) -> int:
    d = outdir(args); state = load_state(d); reasons = []; blocked = False
    if state.get("state") != "PASSED": reasons.append(f"task state is {state.get('state')}, not PASSED")
    risk_ok, risk_why = valid_approval(state)
    if not risk_ok: reasons.append(risk_why); blocked = True
    result, detail = verify_task(state, d)
    if result != "PASSED": reasons.append("evidence re-validation failed: " + "; ".join(detail))
    strict_contract = os.environ.get("EES_REQUIRE_SIGNED_EVIDENCE", "1").strip().lower() not in {"0", "false", "no", "off"}
    if strict_contract:
        current_repo_hash = tree_digest(Path(state["repository"]["path"]), state["repository"].get("tree_hash_exclusion"))
        att_ok, att_problem = revalidate_saved_attestation(state, current_repo_hash or "")
        if not att_ok: reasons.append("contract attestation revalidation failed: " + att_problem)
    risk = state.get("task_risk", "medium")
    if risk in {"high", "critical"} and not state.get("rollback_recovery", {}).get("plan"):
        reasons.append("high/critical-risk task lacks a rollback/recovery plan")
    out = {"decision": "Go" if not reasons else ("Blocked" if blocked else "Partial"), "reasons": reasons,
           "task_id": state["task_id"], "package_version": VERSION, "task_risk": risk, "timestamp": now(),
           "approval_authentication": "Approval records are locally self-attested and not identity-verified."}
    write_json(d / "release-decision.json", out)
    print(json.dumps(out, indent=2))
    return 0 if out["decision"] == "Go" else 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("route", help="route a task and initialize its evidence ledger")
    q.add_argument("--task-id", required=True); q.add_argument("--request", required=True); q.add_argument("--out-dir", required=True)
    q.add_argument("--repo", default="."); q.add_argument("--acceptance", action="append", default=[])
    for name in ["plan", "start", "verify", "status", "recover", "resume", "record-action", "record-criterion", "approve", "run-check"]:
        x = sub.add_parser(name); x.add_argument("--out-dir", required=True)
    sub.choices["verify"].add_argument("--signed-evidence", help="Ed25519-signed evidence envelope; required by default")
    sub.choices["verify"].add_argument("--public-key", help="trusted Ed25519 public key PEM; required by default")
    sub.choices["verify"].add_argument("--required-check", action="append", default=[], help="required PASS check id; repeat for each mandatory check")
    sub.choices["recover"].add_argument("--plan", required=True)
    sub.choices["resume"].add_argument("--change-record", required=True)
    ap = sub.choices["approve"]; ap.add_argument("--approved-by", required=True); ap.add_argument("--scope", required=True); ap.add_argument("--target", required=True); ap.add_argument("--objective", required=True); ap.add_argument("--review-record", required=True); ap.add_argument("--expires", required=True)
    ra = sub.choices["record-action"]; ra.add_argument("--action-id", required=True); ra.add_argument("--idempotency-key")
    cr = sub.choices["record-criterion"]; cr.add_argument("--index", type=int, required=True); cr.add_argument("--status", choices=["pass", "fail"], required=True)
    cr.add_argument("--evidence", required=True); cr.add_argument("--note", default="")
    rc = sub.choices["run-check"]; rc.add_argument("--check-id", required=True)
    sub.add_parser("release-decision").add_argument("--out-dir", required=True)
    sub.add_parser("self-test").add_argument("--out-dir", required=True)
    args = p.parse_args()
    try:
        if args.command == "route": return init(args)
        if args.command == "status": print(json.dumps(load_state(Path(args.out_dir).expanduser().resolve()), indent=2)); return 0
        if args.command == "release-decision": return release(args)
        if args.command == "self-test":
            d = outdir(args); sample = {"task_id": "self-test", "package_version": VERSION, "state": "PLANNED", "events": []}
            event(sample, "self_test", outcome="pass"); verify_event_chain(sample["events"]); write_json(d / "self-test.json", sample)
            print("self-test ok"); return 0
        return cmd(args)
    except (ValueError, OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    sys.exit(main())
