# EES v0.8.0-Clean — Hierarchical Skill Routing

> Compatibility design: preserve all original specialist skill files. The 32 primary routes below are routing bundles, not claims that 74 source skills have been deleted or losslessly rewritten.

## Routing policy
1. Stage 1 selects one primary route from the table below.
2. Stage 2 loads only the listed specialist skills needed for the task.
3. Load dependencies only when the selected skill declares them.
4. If confidence is low or two domains fit, inspect the routing matrix and use the narrowest specialist.
5. Never load all specialist files by default.

## Stage 1: primary routes

| Primary route | Specialist skills available at Stage 2 |
|---|---|
| Agent workflows & orchestration | `agent-workflow-orchestration`, `agent-workflow-specification`, `multi-agent-orchestration` |
| LLM tools & MCP | `llm-tool-contracts`, `mcp-server-engineering`, `ai-agents-rag-mcp` |
| RAG & search | `search-retrieval`, `rag-ingestion-and-vector-retrieval` |
| LLM evaluation & observability | `llm-evaluation-observability`, `observability-and-ai-evaluation`, `machine-learning-evaluation` |
| ML lifecycle & synthetic media governance | `ml-lifecycle-and-synthetic-media-governance` |
| Prompt provenance & safety | `prompt-provenance-and-safety` |
| Frontend implementation | `frontend-development`, `frontend-quality-and-cross-platform-ui`, `frontend-build-quality` |
| React & component systems | `react-component-library-engineering`, `accessible-component-behavior` |
| Responsive UI & cross-platform | `responsive-utility-engineering`, `mobile-desktop-development` |
| UX, design systems & RTL | `ui-ux-design`, `ui-design-system-accessibility`, `design-system-theming-rtl`, `design-intelligence-recommendation` |
| Brand & graphic design | `brand-guidelines`, `graphic-design`, `web-artifacts-builder` |
| Motion & animation | `motion-system-engineering`, `css-motion-performance`, `web-motion-accessibility` |
| Backend architecture | `backend-development`, `fullstack-platform-boundaries`, `system-design` |
| Backend production readiness | `backend-production-readiness`, `backend-reliability-recovery` |
| Backend performance | `backend-performance`, `nodejs-production-performance` |
| Node.js architecture & testing | `nodejs-component-architecture`, `nodejs-outcome-testing` |
| API contracts & integrations | `api-design-contracts`, `api-integrations` |
| Identity & authorization | `backend-auth-authorization` |
| API security | `api-security-testing`, `defensive-appsec-assessment` |
| Security review & response | `security-review`, `security-architecture-and-response`, `defensive-security-ops` |
| Security automation & skill intake | `defensive-automation-and-audit`, `agent-skill-security-intake`, `skill-package-governance` |
| Databases & migrations | `database-engineering` |
| Data engineering & analytics | `data-engineering-analytics`, `data-performance-scalability` |
| Async jobs & messaging | `async-jobs-messaging` |
| Testing & diagnostics | `software-testing`, `browser-e2e-and-test-diagnostics`, `backend-integration-testing` |
| Debugging & reverse engineering | `debugging-and-code-repair`, `reverse-engineering` |
| DevOps & deployment | `devops-and-deployment`, `cloud-architecture-cost` |
| Platform operations & research | `gitea-platform-operations`, `github-research` |
| Browser & editor extensions | `browser-editor-extensions`, `editor-plugin-architecture` |
| Documentation & SEO | `technical-documentation`, `seo-digital-content` |
| Media, games & desktop workflows | `media-production`, `game-development`, `local-desktop-media-lifecycle` |
| Specialist systems & finance | `embedded-iot`, `payments-financial`, `backend-observability`, `skill-creation-and-evaluation` |

## Preservation guarantee
All original `skills/<skill-id>/SKILL.md` files remain in the package. This release changes routing organization and fixture identity; it does not claim a semantic merge of source skill text.
