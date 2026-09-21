# Flask application

This directory contains the runnable CapstoneFlow Flask application.

## Current modules

- `__init__.py` — application factory and configuration
- `routes.py` — sign-in, sign-out, index, and protected dashboard routes
- `auth.py` — reusable session-based `login_required` protection
- `demo_data.py` — fictional development users and checkpoint data
- `services/readiness.py` — proposal-aligned readiness calculation
- `templates/` — Jinja pages for the sign-in flow and dashboard
- `static/styles.css` — responsive interface styling

## Current limitation

Authentication is a development implementation using fictional demo users stored in application code. It is suitable for demonstrating protected routes and roles, but it is not intended for production deployment.

The next application increments are planned to replace hard-coded project data with SQLite models and add requirement management, evidence tracking, weekly status reports, and reviewer feedback.
