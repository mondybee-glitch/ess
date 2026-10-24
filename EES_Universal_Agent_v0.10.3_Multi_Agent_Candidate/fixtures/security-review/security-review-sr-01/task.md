# Fixture security-review/security-review-sr-01

## Input
Review a small Flask endpoint that builds SQL by string concatenation and returns any user's record by id.

## Expected checks
- Finds SQL injection
- Finds the missing ownership check
- Gives a parameterized-query fix and an authorization fix
- Evidence cites the exact lines
