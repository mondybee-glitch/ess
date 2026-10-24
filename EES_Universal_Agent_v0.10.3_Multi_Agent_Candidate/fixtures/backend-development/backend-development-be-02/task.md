# Fixture backend-development/backend-development-be-02

## Input
Add a NOT NULL column to a 10M-row table without downtime.

## Expected checks
- Expand then backfill then constrain plan
- No full-table lock in the plan
- Rollback or forward-fix stated
- Plan reviewed against the stated engine version
