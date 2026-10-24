# Legacy integration status — v0.10.2

`integrations/adaptive-engineering-agent/` is retained for backward compatibility and is **not automatically merged into or invoked by** the primary EES runtime. The current primary runtime and learning-governance entry points are `scripts/task_runtime.py` and `scripts/learning_governor.py`.

Do not treat the legacy `agent_runtime.py` or `feedback_store.py` as equivalent security controls. Before decommissioning or wiring this integration into the primary runtime, perform a separate compatibility review, map persisted feedback formats, test migration/rollback, and audit permissions and secrets. This note deliberately avoids silently redirecting old entry points or deleting user data.
