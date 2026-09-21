# AI Climate Risk and Disaster Impact Assessment Platform #

Submission-oriented starter platform for climate risk analysis with:

- Python backend using FastAPI
- React frontend using Vite
- AI-style risk scoring, impact estimation, and response recommendations

## Project structure

```text
backend/
  app/
    data_store.py
    main.py
    models.py
    schemas.py
    services.py
  requirements.txt
frontend/
  src/
    api.js
    App.jsx
    main.jsx
    styles.css
  index.html
  package.json
  vite.config.js
```

## Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on `http://127.0.0.1:8000`.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```.\.venv\Scripts\activate


Frontend runs on `http://127.0.0.1:5173`.

## Quick start on Windows

You can also start the project with:

- `start_backend.bat`
- `start_frontend.bat`

For moving the project to another laptop, see `TRANSFER_GUIDE.md`.

## Current features

- Dashboard metrics for assessments and incidents
- New assessment form with hazard, exposure, vulnerability, and preparedness inputs
- AI-style summary generation and recommended actions
- Incident watchlist for demo purposes
- In-memory seeded data so the UI is usable immediately

## Scoring methodology

The current scoring model uses a normalized composite risk framework inspired by disaster-risk assessment practice:

- Hazard Index = `0.6 x normalized event severity + 0.4 x climate indicator pressure`
- Risk Score = `100 x (0.30 x Hazard + 0.25 x Exposure + 0.25 x Vulnerability + 0.20 x Preparedness Gap)`
- Impact Score = `100 x (0.35 x Exposure + 0.30 x Vulnerability + 0.20 x Hazard + 0.15 x Preparedness Gap)`

Where:

- `Exposure`, `Vulnerability`, and `Preparedness` are entered on a `0 to 1` scale
- `Preparedness Gap = 1 - Preparedness`
- `Event Severity` is normalized from `0 to 10` into `0 to 1`
- `Climate indicator pressure` is derived from weighted indicators such as rainfall anomaly, river stresps, temperature anomaly, or drought pressure

This makes the platform suitable for demonstration and academic presentation, while still leaving room for later calibration using historical disaster data, GIS layers, or machine learning models.

## Easy next upgrades

- Connect to real climate APIs and geospatial datasets
- Replace rule-based scoring with an ML or LLM pipeline
- Add authentication and role-based access
- Persist data in PostgreSQL or MongoDB

## Jenkins demo

For the Jenkins console dashboard and built-in **Changes** page setup, see `JENKINS_SETUP.md`.

Updated by Lahari as a collaborator.
