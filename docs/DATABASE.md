# Database

## Two-store arrangement

| Store | Purpose | Configuration |
| --- | --- | --- |
| SQLModel relational DB (SQLite by default) | Product profile/preferences and signals, snapshots, interventions, outcomes, action priors | `DATABASE_URL` |
| MongoDB | Authentication accounts and server-side sessions | `MONGODB_URI`, `MONGODB_DATABASE` |

Default SQLite URL: `sqlite:///./maxxloop.db`. The relative file location depends on API process working directory; standard instructions launch from `apps/api`.

## SQL tables

See [Data model](DATA_MODEL.md) for fields. SQLModel creates tables at app startup via `SQLModel.metadata.create_all`; no schema migration tool was found. Some columns store JSON strings (`drivers_json`, `explanation_json`) and are converted by model properties or route code.

## Mongo collections and indexes

- `users`: generated `_id`, name, normalized email, `passwordHash`, creation/update timestamps. Unique index on email.
- `sessions`: `_id` is SHA-256 hash of opaque cookie token, `userId`, `createdAt`, `expiresAt`. TTL index on `expiresAt`, plus `userId` index.

The Mongo client connects lazily on auth operations. TTL cleanup is managed by MongoDB TTL behavior; request authentication also checks expiry.

## User scoping

Protected dependencies map the authenticated Mongo user ID to a SQL `User` profile. Product routers generally filter records by that ID. Outcomes are linked to an intervention, which is scoped to a user when the intervention is retrieved/queried. Demo endpoints intentionally operate on the shared `user_default` synthetic profile and reset its product records; do not use this feature as normal user storage.

## Lifecycle and limitations

SQLite data is server-side wherever the API runs. A persistent volume and backups are needed for a container deployment. Deleting `/privacy/data` removes the user’s product records and action priors while preserving the account and disabling consent flags; it does not delete the Mongo account/session. Account deletion is not exposed by this endpoint.
