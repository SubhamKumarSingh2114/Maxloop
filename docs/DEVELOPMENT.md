# Local Development

## Prerequisites

- Git
- Node.js and npm (lockfile is `apps/web/package-lock.json`)
- Python 3.11 or newer and pip
- MongoDB running/reachable for signup, login, and protected authenticated requests

SQLite is the default product database and is created by SQLModel on API startup. No separate SQLite server is required.

## Clone and configure

```bash
git clone https://github.com/Kingtheblaze/MaxxLOOP.git
cd MaxxLOOP
```

Create backend environment file from `.env.example` at `apps/api/.env`; edit Mongo URI if needed. Do not commit real credentials. The settings loader reads `.env` relative to the current process directory, so run the API from `apps/api`.

## Install

PowerShell:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item ..\..\.env.example .env
```

Bash equivalent for venv activation: `source .venv/bin/activate`. Then install web dependencies:

```bash
cd apps/web
npm ci
```

## Run in two terminals

Terminal 1, from `apps/api` with the virtual environment active:

```bash
uvicorn app.main:app --reload --port 8000
```

Terminal 2, from `apps/web`:

```bash
npm run dev
```

Open `http://localhost:3000`. API docs: `http://localhost:8000/docs`; health: `http://localhost:8000/health`. Authentication requires MongoDB; the health route does not check Mongo readiness.

## Other commands

- Backend tests: `cd apps/api && pytest -v tests/`.
- Web production build: `cd apps/web && npm run build`.
- Docker Compose: `docker compose up --build`; see [Deployment](DEPLOYMENT.md) because Compose currently omits MongoDB and has container URL caveats.
- `make dev` prints instructions; it does not run two servers concurrently.
