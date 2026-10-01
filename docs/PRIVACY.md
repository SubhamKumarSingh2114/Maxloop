# Privacy and Data Handling

## Data currently handled

- Account name/email, password hash, and session records are stored in MongoDB.
- Product profile preferences, numeric signals, capacity snapshots, driver labels, intervention/action status, outcomes, and optional measurement note are stored in the API’s SQL database (SQLite by default).
- Check-in note text is scanned for configured crisis phrases before the standard check-in persistence path. On a detected phrase, that route returns a crisis card without saving the check-in note/signals. This is limited phrase matching, not comprehensive detection.
- The default template provider is deterministic and requires no third-party call. Optional providers can send structured score/baseline/driver/action data to configured model services. Provider-specific data flows must be disclosed when enabled.

## Consent and user controls

Profile fields include calendar/browser/LLM consent flags; signal ingestion skips calendar/browser source data when their consent is false. `/privacy/consent` changes those fields and the selected provider. The UI/API provide payload inspection, data export, and product-data deletion. Deletion retains account/session infrastructure and SQL profile while deleting product records and disabling consent flags.

The LLM payload inspector is process-memory state, not a durable per-user audit log. Its exclusion list is application metadata; do not interpret it as an independent network inspection or guarantee.

## Accurate claims

Activity data is not device-only: it is persisted by the backend. Do not claim zero-knowledge, GDPR/DPDP compliance, or that no information leaves the server. No privacy certification/legal review is documented. Production operators must define retention, backups, access, and deletion behavior for both Mongo and SQL stores.
