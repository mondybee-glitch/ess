---
name: llm-tool-contracts
description: LLM tool and agent contract engineering for typed inputs, structured outputs, middleware, retries, streaming, provider portability, and bounded side effects. Use when an AI application calls models, tools, retrievers, or external systems.
version: 0.6.0
---

# LLM Tool Contracts

## Use when
Use when designing an LLM chain, agent, tool, retriever, structured-output flow, middleware layer, or provider abstraction.

## Do not use when
Do not use for prompt copy edits with no runtime contract or for deterministic non-LLM automation.

## Required inputs
Require model/provider versions, tool schemas, data sensitivity, side effects, timeout/retry policy, structured-output schema, streaming behavior, human approval boundaries, and failure budget.

## Workflow
1. Define typed input/output contracts for models, tools, retrievers, and handoffs. Validate model output before invoking side effects.
2. Separate planning from execution. Tools declare capability, authorization, idempotency, timeout, retry safety, and result/error shape.
3. Keep provider-specific behavior behind an adapter. Record model selection, fallback rules, token/cost limits, and incompatible features.
4. Design middleware for tracing, guardrails, rate limits, redaction, cancellation, and policy checks without hiding failures.
5. Handle streaming, partial output, malformed structured data, tool timeouts, duplicate calls, and provider errors explicitly.
6. Use human approval for irreversible or high-impact actions. Never treat a model response as authorization.

## Pass/fail checks
Pass only when schemas are executable, side effects are bounded and authorized, retries cannot duplicate unsafe actions, provider assumptions are recorded, and partial/invalid output is handled.

Required commands or procedures: run schema and contract tests; simulate malformed output, timeout, retry, cancellation, duplicate tool call, and provider fallback; record model/version/cost evidence without secrets.

## Hand-offs
Hand off security policy to `security-review`, retrieval quality to `search-retrieval`, and orchestration across independent agents to `multi-agent-orchestration`.

## Evidence to report
Report schemas, tool permissions, retry/idempotency rules, model/provider versions, traces, cost/time budgets, approval points, and unverified provider behavior.
