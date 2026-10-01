# Authentication

## Signup

`POST /auth/signup` accepts `name`, valid email, and password length 8–128. The schema trims the name and lowercases/normalizes email. The auth helper hashes passwords using Argon2 and inserts a MongoDB user. A unique email index prevents duplicate accounts (409). Successful signup immediately creates a session and sets the session cookie.

## Login and session

`POST /auth/login` accepts email/password and verifies the stored Argon2 hash. Unknown emails and mismatched passwords return the same 401 message. A random opaque token is generated; its SHA-256 hash is stored in MongoDB. The raw token is set as an HTTP-only, SameSite=Lax cookie, with seven-day max age. The `secure` attribute is enabled when `APP_ENV` is not development/dev/local/test. A Mongo TTL index supports expiry cleanup, and requests also check expiry.

## Logout/current user

`POST /auth/logout` deletes the current server-side session when present and clears the cookie. `GET /auth/me` resolves the session and returns public user fields. Product endpoints use FastAPI auth dependencies and return 401 if unauthenticated. A SQL profile keyed by authenticated user ID is created/synchronized on demand.

## Authorization and limitations

Product queries use the current user ID; demo APIs are a special case that manipulate a shared synthetic `user_default` dataset. Do not treat demo operations as a production multi-user demonstration. Auth account data and product records live in different databases. This describes implementation, not a full security audit; production needs HTTPS, secret management, deployment configuration review, monitoring, and security testing.
