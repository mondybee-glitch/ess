# EES v0.8.0-Clean — Skill Merge Plan

## Policy
- Proposed consolidation groups only; do not delete original skills during the first pass.
- Build canonical umbrella skills by incorporating each source skill as a named subsection and retaining provenance.
- Keep unique checklists, safety constraints, dependencies, examples, and tests.
- Retire a source skill only after equivalence review and routing/evaluation tests.

## Consolidation matrix

| Proposed canonical skill | Source skills to consolidate | Strategy |
|---|---|---|
| AI evaluation & observability | `llm-evaluation-observability`, `observability-and-ai-evaluation`, `machine-learning-evaluation`, `ml-lifecycle-and-synthetic-media-governance`, `backend-observability` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |
| Agent orchestration & protocols | `multi-agent-orchestration`, `agent-workflow-orchestration`, `agent-workflow-specification`, `ai-agents-rag-mcp`, `mcp-server-engineering`, `llm-tool-contracts` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |
| Frontend engineering | `frontend-development`, `frontend-quality-and-cross-platform-ui`, `frontend-build-quality`, `react-component-library-engineering`, `responsive-utility-engineering`, `web-artifacts-builder` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |
| Design systems & accessibility | `ui-ux-design`, `ui-design-system-accessibility`, `accessible-component-behavior`, `web-motion-accessibility`, `design-system-theming-rtl`, `design-intelligence-recommendation`, `brand-guidelines`, `graphic-design` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |
| Motion & animation | `motion-system-engineering`, `css-motion-performance`, `web-motion-accessibility` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |
| Backend & Node.js | `backend-development`, `backend-production-readiness`, `backend-reliability-recovery`, `backend-performance`, `nodejs-production-performance`, `nodejs-component-architecture`, `fullstack-platform-boundaries`, `async-jobs-messaging` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |
| Applied security | `security-review`, `defensive-security-ops`, `defensive-appsec-assessment`, `security-architecture-and-response`, `api-security-testing`, `defensive-automation-and-audit`, `agent-skill-security-intake`, `prompt-provenance-and-safety` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |
| Extensions, retrieval & skill governance | `browser-editor-extensions`, `editor-plugin-architecture`, `search-retrieval`, `rag-ingestion-and-vector-retrieval`, `skill-creation-and-evaluation`, `skill-package-governance` | Create canonical umbrella; preserve each source as a traceable section; no content deletion in this candidate. |

## Scope and caution
The proposed target of approximately 32 primary routes is implemented as hierarchical routing buckets, not by deleting or rewriting 74 skill bodies. A true reduction in physical skill count requires a reviewed content merge and regression benchmark, so it is deliberately not claimed here.
