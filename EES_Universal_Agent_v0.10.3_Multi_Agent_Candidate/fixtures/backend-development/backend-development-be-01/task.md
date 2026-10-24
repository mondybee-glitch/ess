# Fixture backend-development/backend-development-be-01

## Input
Add GET /orders/{id} where users may only read their own orders.

## Expected checks
- Ownership check in server code
- Test: other user's order returns 403 or 404
- Test: owner succeeds
- Tests run and results shown
