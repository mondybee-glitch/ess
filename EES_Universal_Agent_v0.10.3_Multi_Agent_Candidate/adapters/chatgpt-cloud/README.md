# ChatGPT / cloud-agent compatibility notes

This folder documents the portable contract for a ChatGPT-based or other cloud agent; it does not claim that ChatGPT automatically reads `AGENTS.md` or executes this repository. In a chat UI, provide the core instructions and relevant Markdown skill files as project knowledge. For a cloud coding workspace, place files in the workspace and use its supported project-instruction mechanism.

Execution of Python, shell, Docker, network calls, connectors, and provider APIs depends on the selected product, workspace, permissions, and configuration. The agent must declare unavailable tools and must not simulate results. Never upload secrets in knowledge files.
