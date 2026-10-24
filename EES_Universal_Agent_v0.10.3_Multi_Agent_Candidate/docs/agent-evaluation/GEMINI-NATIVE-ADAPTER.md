# Native Gemini adapter

The `scripts/gemini_native_agent_adapter.py` adapter implements `ees-agent-eval/v1` using the Google GenAI SDK (not the OpenAI-compatible endpoint). Install the optional dependency with `python -m pip install -r requirements-gemini.txt`, set `GEMINI_API_KEY`, and optionally set `EES_GEMINI_MODEL` (default `gemini-3.8-flash`) and `EES_MAX_TOOL_STEPS` (default 8).

## Context caching

Context caching is opt-in. Set `EES_GEMINI_CONTEXT_CACHE=1` to cache the stable policy + skill prefix; `EES_GEMINI_CACHE_TTL_SECONDS` defaults to 3600 and must be 60–86400. If cache creation fails, the adapter falls back to uncached mode by default; set `EES_GEMINI_CACHE_FALLBACK=0` to fail closed instead. The adapter attempts to delete the cache after the run and reports cleanup failure. Verify model support, token thresholds, region, billing, and TTL behavior in the target Google project before relying on caching. Never cache secrets or tenant-specific data across trust boundaries.

## Security boundary

The adapter provides path validation and an allowlist for local commands, but subprocesses still execute on the adapter host. Run it inside the repository's disposable sandbox for untrusted tasks. Do not pass production credentials to the process. Commands are invoked without a shell; fixture and skill instruction files are read-only to write operations.

## Evaluation invocation

```bash
GEMINI_API_KEY=... python scripts/run_agent_evals.py \
  --command "python /absolute/path/to/scripts/gemini_native_agent_adapter.py" \
  --skill frontend-engineering --limit 1 --timeout 300 \
  --output reports/gemini-native-eval.json
```

A successful adapter process is not evidence of agent effectiveness. Grade each criterion independently and inspect the changed artifacts.
