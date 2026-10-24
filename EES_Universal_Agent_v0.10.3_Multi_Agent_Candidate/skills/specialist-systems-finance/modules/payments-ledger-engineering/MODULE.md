---
name: payments-ledger-engineering
type: governed-specialist-module
canonical_route: specialist-systems-finance
---

# Payments & Ledger Engineering

## Domain boundary
Own payment state machines, ledger correctness, reconciliation, idempotency, settlement, refunds, chargebacks, and auditability. Do not route embedded device firmware or hardware timing problems here.

## Hard invariants
- A ledger is append-only by default; corrections are compensating entries, not silent mutation.
- Monetary values use integer minor units or a decimal type with explicit currency and scale; never binary floating point for authoritative money.
- Every money-moving operation has an idempotency key, durable state transition, and reconciliation path.
- Payment state transitions are explicit and validated; never infer settlement from a browser redirect or client callback.
- External provider calls and database writes require an outbox/inbox or equivalent recovery design where atomicity spans systems.
- Reconciliation must compare internal ledger, provider reports, and bank/settlement records with exception queues and ownership.

## Blind-spot traps
- Retrying a timeout when the provider already processed the payment.
- Treating authorization, capture, settlement, refund, and reversal as synonyms.
- Updating a balance without a matching journal entry.
- Using local wall-clock timestamps as a globally ordered event sequence.
- Letting a webhook replay apply a refund or settlement twice.
- Treating a successful API response as proof that money settled.

## Required tests
Concurrent duplicate payment requests; provider timeout after remote success; webhook replay/out-of-order delivery; partial refund; reconciliation mismatch; currency rounding and scale; outbox recovery after process crash; authorization-to-capture expiry; immutable audit evidence.
