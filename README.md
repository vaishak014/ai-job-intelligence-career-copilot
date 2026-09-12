# AI Job Intelligence & Career Copilot

A FastAPI backend for tracking jobs, matching candidates to opportunities, analysing skill demand, and producing career recommendations.

## What it provides

- Job listings and filtered job search
- Candidate profiles, skills, match scores, recommendations, and skill gaps
- Market skill-demand analysis
- Application-status and application-notes tracking
- Job ingestion from JSON, CSV, API, and Hopin sources

## Requirements

- Python 3.10 or newer
- PostgreSQL 14 or newer

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with the PostgreSQL database credentials, create the database, then initialise its schema:

```powershell
psql -U postgres -d ai_job_copilot -f database_schema.sql
```

The supplied `data/jobs.json` file can be imported and enriched with the starter skill relationships after the database is initialised:

```powershell
python -m app.ingest_jobs
python -m app.setup_job_skills
```

Run the server:

```powershell
uvicorn app.main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Verification

Run all tests with:

```powershell
python -m pytest -q
```

The suite includes database integration tests, so PostgreSQL must be running and configured through `.env`.

## Useful endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Service health check |
| GET | `/jobs` | List jobs |
| GET | `/jobs/search?title=Python&location=Bengaluru&minimum_salary=6` | Search jobs |
| GET | `/jobs/{job_id}` | Get one job |
| GET | `/candidates/{candidate_id}/intelligence` | Career intelligence summary |
| GET | `/market/skills` | Skill-demand analysis |
| PUT | `/jobs/{job_id}/application-status` | Update application status |
| PUT | `/jobs/{job_id}/application-notes` | Update application notes |

Valid application statuses are `Not Applied`, `Applied`, `Interview`, `Rejected`, and `Offer`.
