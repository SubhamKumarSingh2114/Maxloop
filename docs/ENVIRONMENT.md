# Environment Variables

Backend settings are defined in `apps/api/app/core/config.py`; `.env.example` is the safe template. Never copy real secrets into documentation or source control.

| Variable | Required? | Default/example | Purpose |
| --- | --- | --- | --- |
| `APP_ENV` | No | `development` | Cookie Secure behavior and environment label. |
| `PORT` | No | `8000` | Settings value; documented Uvicorn command explicitly supplies port. |
| `DEBUG` | No | `true` | Settings flag; inspect consumers before relying on behavior. |
| `DATABASE_URL` | No | `sqlite:///./maxxloop.db` | SQLModel product database. |
| `MONGODB_URI` | Required for auth use | `mongodb://localhost:27017/` | Mongo connection string; treat as secret if credentials included. |
| `MONGODB_DATABASE` | No | `maxxloop` | Mongo database name. |
| `SESSION_COOKIE_NAME` | No | `maxxloop_session` | Session cookie key. |
| `LLM_PROVIDER` | No | `template` | `template`, `gemini`, `ollama`, or `openai`; unavailable/keyless providers fall back to templates. |
| `GEMINI_API_KEY` | Only for Gemini | unset | Gemini credential. |
| `OLLAMA_BASE_URL` | Only for Ollama | `http://localhost:11434` | Ollama service endpoint. |
| `OLLAMA_MODEL` | Only for Ollama | `llama3.2` | Ollama model identifier. |
| `OPENAI_API_KEY` | Only for OpenAI-compatible | unset | Provider credential. |
| `OPENAI_BASE_URL` | No | `https://api.openai.com/v1` | Compatible API base URL. |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Requested model identifier. |
| `DEMO_MODE` | No | `true` | Demo status/config flag. |
| `TIMEWARP_SECONDS` | No | `20` | Demo timewarp duration. |
| `STANDARD_WINDOW_MINUTES` | No | `25` | Standard action measurement window. |
| `DROP_THRESHOLD_POINTS` | No | `10.0` | Drop threshold setting. |
| `RAPID_DROP_POINTS` | No | `15.0` | Rapid drop setting. |
| `MIN_COOLDOWN_MINUTES` | No | `45` | Intervention cooldown setting. |
| `MAX_INTERVENTIONS_PER_DAY` | No | `3` | Daily intervention cap. |
| `NEXT_PUBLIC_API_URL` | No | `http://localhost:8000` | Frontend browser API base, set in web environment. |

Backend variables are loaded by Pydantic settings. The web client in `apps/web/src/lib/api.ts` reads `NEXT_PUBLIC_API_URL` at build/runtime according to Next.js public env behavior. Do not set public variables to credentials.
