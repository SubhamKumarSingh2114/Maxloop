# MaxxLoop

**Focus & recovery through a personal capacity learning loop.**

MaxxLoop is a wellness and productivity prototype for students and knowledge workers. It takes a short self-report check-in, estimates capacity against available personal history, explains contributing signals, offers one small action, and records a follow-up measurement and feedback. It is not a medical device and does not diagnose or treat health conditions.

## Core loop

**Track → Understand → Act → Measure → Improve**

The implementation combines a Next.js/React web app, a FastAPI service, SQLite for product activity, MongoDB for authentication accounts/sessions, and a statistical recommendation engine. The default explanation provider uses deterministic templates; optional model providers are configurable.

## Quick start

Prerequisites: Node.js/npm, Python 3.11+, and MongoDB reachable from the API for signup/login. From the repository root:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item ..\..\.env.example .env
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
cd apps/web
npm ci
npm run dev
```

Open <http://localhost:3000>. API health and interactive docs are at <http://localhost:8000/health> and <http://localhost:8000/docs>. Configure MongoDB in `apps/api/.env` if it is not at the local default. Detailed setup and environment variable descriptions: [Development](docs/DEVELOPMENT.md), [Environment](docs/ENVIRONMENT.md).

## Stack

- Web: Next.js App Router, React, TypeScript, Tailwind CSS, Recharts, Lucide
- API: Python, FastAPI, Pydantic, SQLModel/SQLAlchemy
- Activity data: SQLite (configured by `DATABASE_URL`)
- Accounts and sessions: MongoDB (configured by `MONGODB_URI`)
- Recommendation: action library with user/action Beta priors and Thompson sampling; this is statistical personalization, not a trained ML model

## Project map

```text
apps/web/       Next.js application
apps/api/       FastAPI application, engine, data, and tests
scripts/        Demo seeding and synthetic simulation
docs/           Product, engineering, operating, and presentation docs
docker-compose.yml  Local container configuration (see deployment caveat)
```

## Tests

Backend pytest files are under `apps/api/tests/`. Run them from `apps/api` with `pytest -v tests/`, or from the root with `make test`. The web package defines `build` and `lint` scripts; consult [Testing](docs/TESTING.md) for current coverage and limitations. Tests were not executed during documentation generation.

## Deployment status and limitations

No verified public production deployment is documented here. The supplied Compose configuration does not include MongoDB, while authentication requires MongoDB; review [Deployment](docs/DEPLOYMENT.md) before treating Compose as production-ready. Measurement is based on self-report and estimated drift, not a controlled clinical study. Crisis phrase matching is limited. See [Limitations](docs/LIMITATIONS.md).

## Documentation

Start at [docs/README.md](docs/README.md) for the documentation index. Presenters: [Hackathon guide](docs/HACKATHON_GUIDE.md), [3–5 minute demo](docs/DEMO_SCRIPT.md), and [judge Q&A](docs/JUDGE_QA.md).

## Hackathon positioning

MaxxLoop’s contribution is the complete check-in → explanation → single action → follow-up → feedback experience. Present current behavior and synthetic demo data honestly; do not describe simulation outputs as real-world impact or clinical evidence.
