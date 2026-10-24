#!/usr/bin/env python3
"""Preflight checks for the bounded v0.7.6 Pilot; does not call a provider."""
import json, os, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def add(name,ok,detail): checks.append({"check":name,"ok":bool(ok),"detail":detail})
add("provider_api_key_present",bool(os.environ.get("EES_API_KEY")),"EES_API_KEY is set" if os.environ.get("EES_API_KEY") else "Set EES_API_KEY in host environment; never in the workspace or container.")
add("provider_model_present",bool(os.environ.get("EES_MODEL")),"EES_MODEL is set" if os.environ.get("EES_MODEL") else "Set EES_MODEL to the provider's supported Chat Completions model.")
docker=shutil.which("docker")
add("docker_cli_present",bool(docker),docker or "Docker CLI is not installed; no sandboxed pilot can be run here.")
image=os.environ.get("EES_SANDBOX_IMAGE","ees-pilot-sandbox:0.7.6")
image_ok=False
if docker:
 try:
  p=subprocess.run([docker,"image","inspect",image],capture_output=True,text=True,timeout=15)
  image_ok=p.returncode==0
 except Exception: image_ok=False
add("sandbox_image_present",image_ok,f"{image} is available" if image_ok else f"Build image with scripts/build_pilot_sandbox.sh (image name: {image}).")
base=os.environ.get("EES_API_BASE_URL","https://api.openai.com/v1")
add("provider_base_url_present",base.startswith("https://") or base.startswith("http://127.0.0.1") or base.startswith("http://localhost"),"Base URL is configured; this check does not prove reachability or compatibility.")
try:
 manifest=json.loads((ROOT/"reports/pilot-manifest-v076.json").read_text())
 add("pilot_manifest_has_15_cases",len(manifest.get("selected_cases",[]))==15,f"selected_cases={len(manifest.get('selected_cases',[]))}")
except Exception as e: add("pilot_manifest_valid",False,str(e))
add("provider_pricing_configured",("EES_INPUT_PRICE_PER_1M" in os.environ and "EES_OUTPUT_PRICE_PER_1M" in os.environ),"Pricing configured for cost estimate" if ("EES_INPUT_PRICE_PER_1M" in os.environ and "EES_OUTPUT_PRICE_PER_1M" in os.environ) else "Set provider/model-specific input and output price per 1M tokens before a budgeted run.")
result={"schema_version":1,"package_version":"0.7.6","checks":checks,"passed":sum(x["ok"] for x in checks),"total":len(checks),"status":"ready" if all(x["ok"] for x in checks) else "blocked","claim_boundary":"Preflight only; no provider call, container run, or task quality result is implied."}
print(json.dumps(result,indent=2,ensure_ascii=False))
sys.exit(0 if result["status"]=="ready" else 1)
