# Fixture devops-and-deployment/devops-and-deployment-do-02

## Input
Add a CI pipeline with dependency caching and secret scanning.

## Expected checks
- Stages ordered lint, test, build, scan
- Cache configured
- Secret scan step present
- Pipeline syntax validated or marked unverified
