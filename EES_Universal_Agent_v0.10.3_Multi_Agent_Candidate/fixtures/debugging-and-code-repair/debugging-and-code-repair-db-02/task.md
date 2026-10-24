# Fixture debugging-and-code-repair/debugging-and-code-repair-db-02

## Input
A test fails 1 run in 10 in CI.

## Expected checks
- No more than 5 diagnostic reruns
- Failure rate recorded
- Cause identified (race, clock, order, data) or honestly marked unresolved
- No blind retry added as a 'fix'
