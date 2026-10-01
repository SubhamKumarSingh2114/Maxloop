# Troubleshooting

## Frontend cannot connect to API

Check the API is listening on the URL in `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`) and `/health` responds. Browser CORS currently allows only localhost:3000 and 127.0.0.1:3000. Restart Next after changing environment variables. The API wrapper calls the configured base directly.

## MongoDB connection failure / auth unavailable

Start MongoDB, confirm `MONGODB_URI`/`MONGODB_DATABASE` in `apps/api/.env`, then restart Uvicorn from `apps/api`. Auth routes connect lazily and return 503 when Mongo is unavailable; `/health` can still report healthy because it does not ping Mongo.

## CORS or session cookie issue

Use matching localhost hostnames (avoid mixing localhost and 127.0.0.1 without considering cookie origin). For a remote frontend, update the API CORS allowlist in `main.py`, keep credentials enabled, use HTTPS in production, and verify cookie Secure/SameSite/domain settings.

## Invalid login / duplicate account

Emails are normalized to lowercase. Signup with an existing email returns 409. Login returns the same 401 for missing email and wrong password. Password minimum on signup is 8 characters.

## API 401

The session cookie may be missing, expired, or invalid. Sign in again and verify browser requests include credentials. Protected API routes require a valid session.

## API 422 / 500

422 usually means a request body or query argument does not match the Pydantic schema/range; check `/docs`. For 500, inspect Uvicorn logs and database availability. Avoid sharing logs containing personal data or secrets.

## Environment variable appears ignored

The backend reads `.env` relative to process working directory; run Uvicorn from `apps/api`. Restart server after edits. `NEXT_PUBLIC_API_URL` is read by the Next app; restart/rebuild as needed.

## Port already in use

Choose a free API port and keep frontend URL, Next rewrite, and CORS configuration aligned. Current defaults are 8000 and 3000. Do not assume changing Uvicorn’s port updates the frontend automatically.

## Production build failure

Run `npm ci` then `npm run build` in `apps/web`; read the first compiler error and confirm compatible Node.js. For API import/dependency errors, activate the intended Python environment and install `requirements.txt`. Build/test status should be reported only after actually running commands.

## Docker auth does not work

The supplied Compose file has no MongoDB service. Its API container cannot reach host Mongo at `localhost` as though it were inside the host. Configure a reachable Mongo service/URI and review inter-container web/API addresses before using Compose.
