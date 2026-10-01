# Limitations

- **Prototype evidence:** no real-user efficacy study or clinical validation is established. Synthetic simulation is not participant data.
- **Medical boundary:** the score is not validated clinically; the product does not diagnose or treat conditions.
- **Crisis safety:** phrase matching is limited, can miss indirect language/context and can false-positive. It is not continuous monitoring or guaranteed protection.
- **Measurement:** self-report before/after plus estimated drift cannot prove causation; fallback drift is used when control history is sparse.
- **Recommendation:** priors and the threshold-based update are simple heuristics. Feedback volume, selection bias, and synthetic/demo records can affect apparent results.
- **Data integrations:** repository signal kinds support manual/import-style numeric inputs, but automatic calendar, wearable, or browser-history integration should not be claimed without a working implementation.
- **Privacy:** product data is stored server-side in SQL DB; auth is in Mongo. No privacy certification or legal compliance assessment is documented.
- **Operations:** Compose omits Mongo and no verified production deployment configuration was found. SQLite durability needs explicit volume/backup planning.
- **Auth features:** no password reset, email verification, or account deletion route was found.
- **Testing:** backend tests exist; no browser automation or frontend test runner configuration was found in the inspected project files.
- **Demo:** seeded persona uses shared `user_default` data, resets that demo dataset, and includes generated synthetic history. Keep it separate from real users.
