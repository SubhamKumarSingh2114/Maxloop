# API Reference

Base URL in local development: `http://localhost:8000`. OpenAPI/Swagger: `/docs`; ReDoc: `/redoc`. Requests that need identity use the HTTP-only session cookie. JSON examples below are based on the Pydantic schemas and route implementation; actual responses include generated IDs/timestamps and may differ by data.

## System and authentication

| Method/path | Auth | Purpose / effect |
| --- | --- | --- |
| `GET /health` | No | API process/config status. Does not prove Mongo is reachable. |
| `POST /auth/signup` | No | Body `{name,email,password}`; creates Mongo account/session, sets cookie; 201, duplicate email 409, Mongo unavailable 503. |
| `POST /auth/login` | No | Body `{email,password}`; sets session cookie; invalid credentials 401. |
| `POST /auth/logout` | No | Invalidates current session if provided, clears cookie. |
| `GET /auth/me` | Yes | Returns `{user:{id,name,email,createdAt}}`. |

## Product endpoints

| Method/path | Auth | Purpose / effect |
| --- | --- | --- |
| `POST /signals` | Yes | Body `{kind,value,source?,ts?}`; stores one numeric signal unless source consent disallows it. |
| `POST /signals/batch` | Yes | Body `{signals:[{kind,value,source?,ts?}]}`; stores allowed signals, returns `saved_count`. |
| `GET /signals?kind=&limit=` | Yes | Current user’s signals, newest first; default limit 50. |
| `POST /checkins` | Yes | Body defined below; records a check-in and may create a snapshot/intervention, or returns crisis interception. |
| `GET /capacity/now?demo=false` | Yes | Latest capacity, drivers, status and 14-day sparkline; demo flag selects demo profile behavior. |
| `GET /loop/active?demo=false` | Yes | Current active loop/stage/action/timing/outcome context. |
| `POST /loop/{intervention_id}/start?demo=false` | Yes | Marks offered intervention started. |
| `POST /loop/{intervention_id}/skip?demo=false` | Yes | Body `{reason?}`; marks intervention skipped. |
| `POST /loop/{intervention_id}/measure?demo=false` | Yes | Body `{focus_self,energy_self,stress_self,note?}`; saves signals/snapshot/outcome, computes measurement and updates prior. |
| `POST /loop/{intervention_id}/feedback?demo=false` | Yes | Body `{helpful,note?}`; records user feedback for outcome when available. |
| `GET /insights?demo=false` | Yes | Aggregates closed loops, helpfulness, improvements, actions, recurring drivers, time distribution, weekly trend. |

### `POST /checkins` request

```json
{
  "focus_self": 3.0,
  "energy_self": 3.0,
  "stress_self": 2.0,
  "note": "Optional text",
  "tags": [],
  "window_context": "normal"
}
```

The three numeric values must each be from 1 to 5. The response normally contains `status`, `snapshot_id`, `score`, `baseline`, `delta`, `is_drop`, `drop_reason`, `cooldown_ok`, `drivers`, and nullable `active_intervention`. If the safety phrase scanner intercepts the note, the response instead has `status: "crisis_intercepted"`, a message, and `crisis_card`; normal persistence/recommendation is paused.

## Privacy and demo endpoints

| Method/path | Auth | Purpose / effect |
| --- | --- | --- |
| `GET /privacy/llm-payload` | Yes | Returns last in-memory provider transaction for that user (not durable audit history). |
| `GET /privacy/export` | Yes | Returns the user profile and product signal/snapshot/intervention/outcome records. |
| `DELETE /privacy/data` | Yes | Deletes the user’s product records and priors; keeps account/profile and changes consent flags. |
| `POST /privacy/consent?...` | Yes | Query args `consent_calendar`, `consent_browser_signals`, `consent_llm_sharing`, optional `llm_provider`; updates SQL profile. |
| `POST /demo/seed` | Yes | Body `{persona:"aarav"|"meera"}`; resets and writes shared synthetic `user_default` data. |
| `POST /demo/trigger-drop` | Yes | Optional `{drop_severity}` body; generates sample demo signals/snapshot/action. |
| `POST /demo/timewarp` | Yes | Optional `{seconds}` body; advances eligible demo intervention timing. |
| `GET /demo/status` | Yes | Reports demo mode/provider/persona and configured timewarp information. |

## Schema constraints and errors

`SignalCreate`: required string `kind`, float `value`, optional `source` default `self_report`, optional timestamp. `CheckinCreate` and loop measurement values are 1–5. Signup email uses `EmailStr`, password limits 8–128. Common HTTP failures include 401 unauthenticated/invalid credentials, 409 duplicate signup, 422 validation errors, and 503 unavailable Mongo authentication storage. Specific route details are available in runtime OpenAPI.

## Example authenticated loop

```text
POST /checkins
GET  /loop/active
POST /loop/{id}/start   (or /skip)
POST /loop/{id}/measure
POST /loop/{id}/feedback
GET  /insights
```

There is no `/api` prefix in FastAPI routes. Frontend requests use the configured base URL directly. See the request wrapper in `apps/web/src/lib/api.ts`.
