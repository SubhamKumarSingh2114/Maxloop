# Backend

## Application

`apps/api/app/main.py` creates the FastAPI application, initializes SQLModel tables in lifespan, configures credentialed CORS for `http://localhost:3000` and `http://127.0.0.1:3000`, mounts domain routers, and exposes `GET /health`. Swagger UI is `/docs`; ReDoc is `/redoc`.

## Routers and processing

- `auth`: signup/login/logout/current account; MongoDB-backed account/session storage.
- `signals`: create, batch-create, list numeric signals; calendar/browser-source values respect profile consent booleans.
- `checkins`: scan note, save self-report signals, compute capacity/baseline/drivers/drop, optionally create action and explanation.
- `capacity`: latest capacity response and recent sparkline.
- `loop`: active loop, start/skip, measure, feedback.
- `insights`: aggregate saved outcomes, drivers, timestamps, and trends.
- `privacy`: inspect in-memory latest provider transaction, export product records, delete product records, update consent/preferences.
- `demo`: authenticated seed, trigger drop, timewarp, and status controls.

## Engine services

`BaselineEngine`, `CapacityEngine`, `DriverEngine`, `DropDetectionEngine`, `RecommenderEngine`, and `MeasurementEngine` are called from the route handlers. Validation is mostly Pydantic request/response models. SQL operations use injected SQLModel sessions. Auth uses FastAPI dependencies to resolve the session and profile.

## Request lifecycle example

`POST /checkins` → validate values → crisis scan optional note → persist focus/energy/stress signals → load latest ancillary signals → compute score/baseline/drivers → evaluate drop and cooldown → if eligible, sample an action and generate explanation → save snapshot/intervention → return response. See [MaxxLoop loop](MAXXLOOP_LOOP.md).

## Errors and operations

FastAPI/Pydantic emits standard validation errors; auth uses 401 for invalid credentials/unauthenticated access and 503 when Mongo auth storage is unavailable. Duplicate email signup returns 409. Database operational errors may surface according to route and driver behavior. Health reports process/config status, not a full readiness check for MongoDB or SQLite.
