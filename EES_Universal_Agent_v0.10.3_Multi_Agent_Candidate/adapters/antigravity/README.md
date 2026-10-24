# Google Antigravity adapter

Use the root `GEMINI.md` where the installed Antigravity version recognizes Gemini project instructions, and `.agent/rules/ees.md` for a project rule file if supported by that version. Keep `AGENTS.md` as the portable baseline. Verify the exact instruction-discovery behavior against the installed Antigravity release; file presence alone does not prove it was loaded.

Before accepting a task, confirm the agent can read `capability-registry.json`, `hierarchical-routing.json`, and the selected skill file. Run the same acceptance checks as the other adapters. Tool availability, terminal permissions, browser access, and model selection depend on local Antigravity settings and must not be assumed.
