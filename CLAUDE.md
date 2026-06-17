# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Dev setup

```bash
# Activate the virtual environment (Windows)
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run the dev server (port 5001)
python app.py
```

App runs at http://127.0.0.1:5001

## Testing

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_routes.py
```

Uses `pytest-flask`. No test directory exists yet — tests go in `tests/`.

## Architecture

This is a Flask + SQLite expense tracker structured as a guided student project. Routes are added step-by-step; many are currently stubs.

**`app.py`** — all routes live here. Fully implemented: `/`, `/register`, `/login`, `/terms`, `/privacy`. Stubs (returning plain strings): `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`.

**`database/db.py`** — not yet implemented. Will contain `get_db()`, `init_db()`, and `seed_db()` using SQLite with `row_factory` and foreign keys enabled. Students write this in Step 1.

**`templates/base.html`** — shared layout. Defines `{% block content %}`, `{% block head %}`, and `{% block scripts %}`. Loads Google Fonts (DM Serif Display, DM Sans) and `static/css/style.css`. Every page template extends this.

**`static/css/style.css`** — single stylesheet for the entire app. No per-page CSS files. Sections are clearly delimited with banner comments. Modal, legal page, auth, and landing styles are all in here.

**`static/js/main.js`** — intentionally empty placeholder. Page-specific JS goes in `{% block scripts %}` inside each template (see `landing.html` for the video modal example).

## Key conventions

- All CSS goes in `static/css/style.css` — there is no `landing.css` or other per-page stylesheet.
- Page-specific JavaScript goes in `{% block scripts %}` at the bottom of the template, not in `main.js`.
- Currency is in Indian Rupees (₹); month/date context assumes Indian locale.
- The app is a teaching project — stub routes intentionally return plain strings until students implement them.
