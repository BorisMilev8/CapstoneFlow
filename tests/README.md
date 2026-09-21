# Test suite

CapstoneFlow uses pytest with Flask's test client.

## Implemented coverage

- sign-in page loads
- dashboard redirects unauthenticated visitors
- valid student sign-in
- valid reviewer sign-in and session-backed role
- invalid-password rejection
- logout clears the authenticated session
- readiness requires Complete + evidence + no blocking feedback
- optional items do not affect the readiness denominator
- zero required items return Not configured

Run all tests from the repository root:

```bash
pytest
```

Future tests will cover SQLite persistence, project membership, cross-project authorization, requirement forms, evidence validation, weekly reports, reviewer feedback, and full R1–R12 acceptance flows.
