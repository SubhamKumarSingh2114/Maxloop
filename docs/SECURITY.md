# Security

This document records observable implementation safeguards and gaps; it is not a security certification.

## Implemented

- Argon2 password hashing; plaintext passwords are not persisted by the auth helper.
- Random opaque session token; Mongo stores its SHA-256 hash, with expiry and per-user indexes.
- HTTP-only, SameSite=Lax cookie, seven-day max age; Secure set outside local/test environments.
- Protected API dependencies resolve sessions and use authenticated user IDs for product queries.
- Pydantic validates key request fields and numeric ranges.
- Unique normalized email index; duplicate account returns 409.
- LLM provider output is parsed into a schema and checked against banned phrases/driver consistency; provider exceptions fall back to template.

## Configuration and limits

- CORS currently allows only localhost:3000 and 127.0.0.1:3000, with credentials. Production origins need explicit configuration/code review.
- No rate limiting, account lockout, password reset, email verification, or account deletion endpoint was found in the inspected implementation.
- CSRF protections beyond SameSite cookie behavior were not identified. Production cookie/domain/CORS and CSRF threat model require review.
- Do not expose `.env`, API keys, MongoDB credentials, or user exports. Keep secrets in the deployment’s secret manager.
- SQL migrations, security monitoring, backup encryption, vulnerability scanning, and external security audit are not established by repository code.
- The shared demo profile has destructive reset behavior; keep demo operations away from production data.

## Production checklist

Use HTTPS, restrict CORS to the real frontend origin, use managed secret storage and private database networking, configure durable backups and access controls, review authentication/session/CSRF/rate-limit behavior, and verify deletion/retention requirements before public use.
