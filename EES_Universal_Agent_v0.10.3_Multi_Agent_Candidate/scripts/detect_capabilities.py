#!/usr/bin/env python3
"""Conservative capability probe. Reports local executable presence, not permissions or functional integration."""
from __future__ import annotations
import json, shutil, platform, os, sys, datetime
from pathlib import Path

TOOLS = {
  "python": ["python3", "python"], "git": ["git"], "node": ["node"], "npm": ["npm"],
  "pytest": ["pytest"], "unittest": [], "docker": ["docker"], "podman": ["podman"],
  "curl": ["curl"], "wget": ["wget"], "git-lfs": ["git-lfs"],
}

def main() -> int:
  found = {}
  for name, candidates in TOOLS.items():
    path = next((shutil.which(x) for x in candidates if shutil.which(x)), None)
    if name == "unittest":
      try:
        import unittest  # noqa: F401
        found[name] = {"status":"available", "evidence":"Python standard library import succeeded"}
      except Exception as exc:
        found[name] = {"status":"failed_probe", "evidence":type(exc).__name__}
    else:
      found[name] = {"status":"available" if path else "unavailable", "path":path, "probe":"PATH lookup only"}
  # These are deliberately not inferred from executable presence.
  for name in ("browser", "network_access", "secret_manager", "agent_model_provider", "tool_calling", "workspace_write_permission"):
    found[name] = {"status":"not_tested", "reason":"Cannot be reliably inferred from local executable presence."}
  report = {"schema_version":1,"created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"platform":platform.platform(),"python_version":sys.version.split()[0],"workspace":str(Path.cwd()),"capabilities":found,"limitations":["PATH presence does not prove a tool works, is authorized, or is correctly configured.","Docker daemon access, network reachability, credentials, and provider model quality are not tested.","No commands other than local interpreter imports and PATH lookups were executed."]}
  out = Path("capability-report.json")
  out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"report":str(out.resolve()),"available":sum(x["status"]=="available" for x in found.values()),"unavailable":sum(x["status"]=="unavailable" for x in found.values()),"not_tested":sum(x["status"]=="not_tested" for x in found.values())},indent=2))
  return 0
if __name__ == "__main__": raise SystemExit(main())
