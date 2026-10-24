---
name: payments-financial
description: Specialist workflow for payments, refunds, webhooks, reconciliation, pricing, tax boundaries, and financial auditability. Use when the task materially involves this boundary.
version: 0.6.0
---

# payments-financial

## Use when

Use when the main deliverable involves payments, refunds, webhooks, reconciliation, pricing, tax boundaries, and financial auditability.

## Do not use when

Do not load this skill for non-financial CRUD or display-only change with no money/state authority.

## Required inputs

Require provider/version, server authority, idempotency, ledger, currency, tax owner, webhook, dispute, PCI boundary.

## Workflow

trace money source; implement server-authoritative state; test duplicate/out-of-order webhooks, retries, refunds, reconciliation, and failure; obtain approval

## Pass/fail checks

no double charge/refund; ledger reconciles; authorization and audit evidence exist; recovery is tested

Required commands or procedures: run sandbox provider tests, idempotency, replay, reconciliation, negative auth, timeout, and rollback/forward-fix checks

## Hand-offs

Coordinate with backend, security, API, data, devops, and owner/finance. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve redacted provider responses, ledger diff, reconciliation, audit trail, approvals, and limitations. Report exact versions, commands, expected/actual results, and what remains Unverified.

## AI blind-spot traps
1. **Webhook/commit race:** a provider event may arrive before the local order transaction commits. Persist verified events durably and retry resolution with bounded exponential backoff; never discard an unknown-order event.
2. **Idempotency payload mismatch:** bind each idempotency key to a canonical request hash and authenticated principal. Same key + different amount/currency/order must fail closed.
3. **Money precision:** use integer minor units or a fixed-precision decimal with an explicit currency exponent and rounding policy; never binary floating point for posted amounts.
4. **Signature verification:** verify provider signatures over the exact raw request bytes before trusting parsed fields; enforce timestamp tolerance and provider-specific rotation rules.
5. **Mutable balance without ledger:** use append-only double-entry postings and derive/reconcile balances; never make a balance column the sole financial record.

## Hard invariants
- Every posted journal transaction balances: sum(debits) = sum(credits), per currency, before commit.
- A provider operation is not repeated with a new idempotency key merely because the client timed out; resolve `UNKNOWN` by querying/reconciling the original operation.
- Never hold a database row lock across a network call. Use local `PENDING` reservation → provider call outside lock → immutable result posting.
- Enforce replay protection using the provider's documented signature timestamp semantics; 300 seconds is a common policy, not a universal provider constant. Configure and test per provider.
- Never store or log PAN/CVV, secrets, full payment tokens, or unnecessary personal data.

## Decision matrix
| Scenario | Required decision | Reject |
|---|---|---|
| Duplicate purchase request | Same key + same canonical payload returns the original result | Charging again |
| Same key, changed amount/currency | Conflict response and security/audit event | Reusing cached success for altered payload |
| Provider timeout / HTTP 504 | Mark outcome `UNKNOWN`; query provider/reconcile using original key | Generate a new key and blindly retry |
| Partial refund | Unique key includes order/refund sequence/amount or provider-supported stable operation ID | Key based on order alone when multiple refunds are allowed |
| Concurrent transfers | Lock accounts in stable sorted order; enforce ledger balance and sufficient funds atomically | Read-modify-write without version/lock |

## Adversarial kill-switch
Reject the implementation if a 5 ms double click can charge twice; a crash after provider success can lose the financial outcome without reconciliation; webhook replay can post twice; journal entries can be unbalanced; or logs can expose payment credentials.

