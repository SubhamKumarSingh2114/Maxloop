# Testing

## Existing automated backend tests

The repository contains pytest modules:

- `test_auth.py` — authentication behavior
- `test_e2e_loop.py` — end-to-end API loop behavior
- `test_engine.py` — capacity/baseline/driver engine behavior
- `test_measurement.py` — outcome measurement behavior
- `test_recommender.py` — action selection behavior
- `test_safety.py` — safety phrase behavior

Run from `apps/api`:

```bash
pytest -v tests/
```

or from the repository root: `make test`.

## Frontend checks

The web package scripts are `dev`, `build`, `start`, and `lint`. It declares a Next build and a lint script (`next lint`); verify the lint command against the installed Next version because script compatibility can change. TypeScript is configured with `tsconfig.json`, but no dedicated test runner script or browser automation configuration was found in the inspected files.

## Coverage boundaries

No frontend unit test, browser automation, or responsive visual regression configuration was found. Backend tests do not alone demonstrate production database behavior, accessibility, or cross-browser responsiveness.

**Tests were not executed during documentation generation.** This documentation change has not been verified by running the app/build/test suites.
