# Fixture backend-development/backend-development-be-03

## Input
A payment webhook is delivered twice by the provider.

## Expected checks
- Idempotency key or dedupe table
- Test delivers the event twice and asserts a single effect
- Timeout and retry behavior stated
