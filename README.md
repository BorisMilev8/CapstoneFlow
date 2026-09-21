# CapstoneFlow

CapstoneFlow is a SENG 701 capstone project focused on connecting project requirements, weekly status reports, reviewer feedback, evidence links, and checkpoint readiness in one workflow.

## Current status

The repository now contains both the original proposal-stage browser prototype and the first runnable Flask application increment.

### Implemented in the Flask app

- Student and reviewer demo sign-in
- Session-backed authentication state
- Protected `/dashboard` route
- Role-aware dashboard heading
- Proposal-aligned checkpoint readiness calculation
- Missing-evidence and blocking-feedback counts
- Responsive Flask/Jinja interface
- Automated route/authentication tests
- Automated readiness-rule tests

The current sign-in is intentionally a **development/demo authentication layer**, not production identity management.

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/BorisMilev8/CapstoneFlow.git
   cd CapstoneFlow
   ```

2. Create and activate a virtual environment:

   macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Optional: set a development secret key using `.env.example` as a reference.

5. Start the app:

   ```bash
   python run.py
   ```

6. Open the local URL shown by Flask, normally `http://127.0.0.1:5000`.

## Demo accounts

These accounts contain fictional development data only.

| Role | Email | Password |
| --- | --- | --- |
| Student | `student@capstoneflow.local` | `Student123!` |
| Reviewer | `reviewer@capstoneflow.local` | `Reviewer123!` |

## Run tests

```bash
pytest
```

The test suite currently covers protected-route behavior, successful and failed sign-in, session-backed roles, logout, readiness calculation, optional requirements, and the zero-required-item case.

## Repository structure

- `app/` — runnable Flask application
- `app/templates/` — Jinja pages
- `app/static/` — application styling
- `app/services/` — business rules such as readiness calculation
- `tests/` — automated tests
- `docs/` — proposal summary, development plan, and R1–R12 requirements
- `prototype/` — original interactive browser prototype
- `releases/` — planned checkpoint artifacts for Alpha, Beta, and Final

## Readiness rule

A required item counts as ready only when:

1. its status is **Complete**,
2. it has at least one evidence link, and
3. it has no open blocking feedback.

Optional items are excluded from the denominator. A checkpoint with no required items displays **Not configured** instead of 100%.

The readiness indicator is a workflow aid. It is not a grade and does not represent faculty approval.

## Baseline scope

The proposal defines 12 baseline user stories (R1–R12). Core areas are project setup, requirements planning, weekly reporting, reviewer feedback, evidence traceability, readiness rules, and protected access.

## Planned technology

- Python
- Flask
- SQLite
- HTML / CSS / JavaScript
- pytest
- Git and GitHub

## Official repository

https://github.com/BorisMilev8/CapstoneFlow
