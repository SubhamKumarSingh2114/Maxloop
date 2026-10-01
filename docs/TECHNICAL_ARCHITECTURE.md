# Technical Architecture

## Frontend

- Next.js `16.3.7` and React `19.3.0` according to `apps/web/package.json`.
- TypeScript, Tailwind CSS 3, Recharts, Lucide React, `clsx`, and `tailwind-merge`.
- App Router pages live under `apps/web/src/app`; shared components under `src/components`; request wrapper and browser consent storage under `src/lib`.
- Auth state uses a React context provider. The request helper uses `fetch`, JSON headers, and `credentials: "include"`. `NEXT_PUBLIC_API_URL` selects the API base; default is `http://localhost:8000`.
- No separate global state framework is configured in the package manifest. Page/component React state is used.

## Backend

- Python >=3.11; FastAPI, Uvicorn, Pydantic 2, SQLModel/SQLAlchemy.
- Routers are in `apps/api/app/routers`; schemas in `models/schemas.py` and `models/auth_schemas.py`.
- Engine modules under `engine/` implement baselines, scoring, driver labels, drop rules, action selection, and measurement.
- Auth helpers use PyMongo, Argon2, secure random tokens, and FastAPI dependencies.
- Data/config files: `actions.json`, `weights.yaml`, `population_priors.yaml`.
- Optional numerical packages include NumPy, SciPy, pandas (declared dependency; inspect imports for actual usage before attributing a specific feature).

## Data stores

SQLite via SQLModel stores `User` profile/preferences, `Signal`, `CapacitySnapshot`, `Intervention`, `Outcome`, and `ActionPrior`. MongoDB stores account and session documents. Indexes created in Mongo: unique normalized email, session expiry TTL, and session user ID. SQL fields have selected indexes on IDs/timestamps/kinds; no migration framework is present in the inspected repository.

## Runtime configuration

Backend settings are Pydantic settings loaded from environment and `.env` (see [Environment](ENVIRONMENT.md)). The frontend has a `NEXT_PUBLIC_API_URL` variable. Next rewrites `/api/*` to `http://localhost:8000/*`; separately, current frontend code calls the API base directly. Verify actual deployment routing before using this rewrite as a production proxy.

## Production status

The repository has an API Dockerfile and Compose file. No Vercel/Render deployment manifest was found in the inspected file inventory. Compose does not include the MongoDB service required for authentication. Production topology is therefore not established by these files alone.
