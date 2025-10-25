<!-- .github/copilot-instructions.md - guidance for AI coding agents -->
# Repository overview

This is a small Flask web app for tracking student performance. Main pieces:

- `app.py` – single-file Flask backend exposing HTML views and JSON API endpoints (students, subjects, assessments, performance, analytics). Most server logic is here and uses `flask_mysqldb` for MySQL access.
- `templates/` – Jinja2 HTML templates. `dashboard.html` is the primary interactive UI (uses Chart.js and `static/js/dashboard.js`).
- `static/js/dashboard.js` – client-side logic that calls the REST API and renders charts. (Look here for expected API shapes.)
- `database/schema.sql` and `database/seed_data.sql` – canonical DB schema and sample data. SQL ENUMs and column ordering determine how rows are read in `app.py`.

# Quick engineering contract for edits

- Inputs: HTTP JSON payloads matching current endpoints (see `app.py` routes). DB rows are returned as tuples from MySQL cursor; `app.py` maps tuple indices to object fields.
- Outputs: Maintain existing JSON shapes and Jinja templates. Keep endpoints and their response keys unchanged unless intentionally versioned.
- Errors: API returns `{ "error": "<message>" }` with 500 status for server errors.

# Project-specific patterns and gotchas

- Single-file backend: most changes to behavior live in `app.py`. Search there first for business logic.
- Cursor result ordering matters: `app.py` uses positional tuple indices (e.g., student[5] for enrollment date). If you modify SQL or schema, update corresponding index access sites.
- Date handling: rows with dates are formatted using `.strftime('%Y-%m-%d')` in `app.py` — preserve this format in JSON responses.
- Frontend expectations: `static/js/dashboard.js` expects analytics and performance payload shapes produced by `/api/analytics/<id>` and `/api/performance/<id>`. Breaking keys will break Chart rendering.
- DB config is hard-coded in `app.py` (`MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`). For changes, prefer adding environment variable support (non-breaking) instead of editing defaults.

# Typical tasks and exact commands

- Install deps: `pip install -r requirements.txt` (project uses Flask + flask_mysqldb). Use Python 3.8+.
- Create schema and seed data (MySQL):
  - `mysql -u root -p < database/schema.sql`
  - `mysql -u root -p < database/seed_data.sql`
- Run app locally: `python app.py` → visits `http://localhost:5000`.

# Useful examples from this repo

- Add assessment API (expects JSON): POST `/api/assessments` with body { "student_id", "subject_id", "term_number", "assessment_type", "score", "max_score", "date", "notes" }
- Analytics shape returned by GET `/api/analytics/<student_id>`:
  - `term_performance`: [{ term, percentage }]
  - `subject_performance`: [{ subject, percentage }]
  - `assessment_performance`: [{ type, percentage }]
  - `skills_performance`: [{ skill, percentage }]

# Testing and debugging tips

- If charts are empty: open browser console, check `/api/analytics/<id>` and `/api/performance/<id>` responses. The frontend will fail silently if keys are missing.
- Common DB issues: verify MySQL server is running and credentials in `app.py` match. Seed data assumes the schema order; if you change schema, re-seed.
- When refactoring `app.py`: add unit tests or a small integration script that hits key endpoints (students, performance, analytics) to validate response shapes.

# What NOT to change without coordination

- Public JSON keys returned by endpoints – the frontend relies on specific keys and formatting. If a change is required, either keep backward compatible keys or update `static/js/dashboard.js` accordingly.
- The order/columns in `database/schema.sql` without updating index mapping in `app.py`.

# Where to look next (file pointers)

- `app.py` — primary server logic, routes and SQL queries.
- `static/js/dashboard.js` — client-side API calls and Chart.js usage.
- `database/schema.sql` — canonical schema and ENUMs referenced by UI and server.

If any of the above expectations are incorrect or you want the instructions to include automated test commands / CI steps, tell me which areas to expand and I will iterate.
