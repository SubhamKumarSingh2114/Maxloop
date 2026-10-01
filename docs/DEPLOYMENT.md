# Deployment

## Current repository configuration

An API Dockerfile and `docker-compose.yml` are present. The Compose file exposes API port 8000 and web port 3000, uses SQLite and template provider defaults, and mounts an API data volume. It does **not** define MongoDB even though auth requires MongoDB. The web container sets `NEXT_PUBLIC_API_URL=http://localhost:8000`; inside a browser this means the user’s machine, and inside containers service DNS differs. The Next rewrite is also hard-coded to localhost:8000. Therefore do not assume the supplied Compose file is a working public deployment without testing and configuration changes.

No verified Vercel/Render/Atlas deployment or provider manifest was found in the repository inventory. This document gives deployment requirements, not a claim deployment exists.

## Production requirements

1. Deploy the web app and API to reachable HTTPS origins.
2. Provide MongoDB reachable only by the API; configure `MONGODB_URI` and `MONGODB_DATABASE` using a secret store.
3. Configure `DATABASE_URL` for durable product data or mount the SQLite file on a persistent volume. SQLite on ephemeral serverless filesystems is not durable.
4. Set `APP_ENV=production` so auth cookies use `Secure`; use HTTPS and configure correct cookie domain/SameSite behavior for the chosen topology.
5. Set the frontend API URL to the public API origin. Update API CORS allowlist to the exact frontend origin and verify credentialed cookie behavior.
6. Configure LLM provider credentials only if using that provider; review data disclosures/consent.
7. Configure backups, logs/monitoring, database access, privacy retention, and deletion procedures.

## Build/run references

- Web: `cd apps/web && npm ci && npm run build`; serving: `npm run start` (package script binds port 3000).
- API: install `apps/api/requirements.txt`; start with `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- API Docker image: build from `apps/api` context using its Dockerfile.

Do not publish until the production URL, auth cookies, CORS, Mongo connectivity, durable SQL storage, and data isolation are verified in the target hosting environment.
