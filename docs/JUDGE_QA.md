# Judge Q&A

Answers below reflect the current repository. They are intentionally candid. Add team-specific facts only if you can verify them.

## Product

### 1. What is MaxxLoop?
**Answer:** A focus/recovery prototype that connects a short check-in to an explanation, one suggested action, follow-up measurement, and feedback.  
**Technical detail:** The loop is implemented across `/checkins`, `/loop/*`, and `/insights`.

### 2. Who is it for?
**Answer:** Initially students and knowledge workers who want lightweight support for focus and recovery.  
**Technical detail:** Current account model is general; no institution/role-specific access control is implemented.

### 3. What problem are you solving?
**Answer:** Self-tracking can show a state without a next step, while generic advice may not fit the user’s context. We connect a check-in to one action and a later record.

### 4. What is the main differentiator?
**Answer:** The end-to-end closed loop: check in, understand, try one action, measure again, and use feedback to shape later suggestions. We do not claim no competitor does this.

### 5. Why one action?
**Answer:** The product is designed to reduce choice burden in the moment. The API creates a single offered intervention for an eligible drop.

### 6. What does the user see after a check-in?
**Answer:** An estimated capacity score/status, baseline and change, available drivers, and an action if the drop and cooldown rules permit.

## Technical

### 7. What is the stack?
**Answer:** Next.js/React/TypeScript/Tailwind on the web; FastAPI/Python/Pydantic/SQLModel on the API; SQLite for product data and MongoDB for auth.

### 8. How does the frontend reach the API?
**Answer:** A shared `fetch` wrapper uses `NEXT_PUBLIC_API_URL` (default localhost:8000), JSON, and credentialed requests for the session cookie.

### 9. How is the capacity score computed?
**Answer:** Signal values are compared with baselines, standardized and weighted, then mapped to a bounded 0–100 product score. It is not a clinical measurement.  
**Technical detail:** See `engine/baseline.py`, `capacity.py`, `weights.yaml`, and [Technical architecture](TECHNICAL_ARCHITECTURE.md).

### 10. What happens at cold start?
**Answer:** The baseline engine uses configured population priors/fallback blending when personal history is sparse, then can use more personal history as it accumulates.

### 11. How are drivers selected?
**Answer:** Driver contributions from the capacity calculation are labeled and ranked; up to three are passed into the recommendation path.

### 12. What database tables exist?
**Answer:** User profile, signal, capacity snapshot, intervention, outcome, and action-prior tables are defined in SQLModel. Mongo has users and sessions collections.

### 13. How does user-data isolation work?
**Answer:** Auth dependencies resolve the account ID and product queries use that ID. Demo operations deliberately use a shared `user_default` dataset and should stay in demo-only use.

### 14. What protects passwords?
**Answer:** The auth helper hashes passwords with Argon2 and stores the hash, not plaintext. We have not represented that as a complete security audit.

### 15. How are sessions handled?
**Answer:** A random opaque token is set in an HTTP-only cookie; Mongo stores a SHA-256 hash with expiry. The session is checked on protected requests and removed on logout.

## AI / ML

### 16. Is this machine learning?
**Answer:** It is not a trained ML model. The action selector uses a lightweight statistical Beta/Thompson-sampling method over stored outcomes.

### 17. Is generative AI required?
**Answer:** No. The default provider is deterministic templates. Optional external providers exist, but must be configured and their data flow disclosed.

### 18. How are actions selected?
**Answer:** Candidate actions are filtered by target-driver overlap. The engine samples Beta values and usually chooses the highest sample, with a 15% exploration branch when multiple candidates exist.

### 19. How does feedback change recommendations?
**Answer:** Measurement updates alpha when net effect exceeds two points, otherwise beta. The explicit helpfulness response is stored separately and is not the prior update criterion in the current code.

### 20. Does the algorithm prove which action works?
**Answer:** No. It adapts a heuristic from observed in-app data. Selection bias, self-report, small samples, and the drift estimate limit interpretation.

## Data and measurement

### 21. How do you measure an action?
**Answer:** Compare pre/post self-report scores, then subtract an estimated no-action drift based on skipped-intervention windows, blended with a prior when sparse.

### 22. Is net effect causal?
**Answer:** No. It is an observational estimate and not a randomized controlled comparison.

### 23. What data do you collect automatically?
**Answer:** Do not claim automatic calendar, wearable, or browser collection unless you can demonstrate a working source integration. Current check-in inputs are self-reported; signal endpoints can accept numeric signals.

### 24. Where is data stored?
**Answer:** Auth accounts/sessions are in MongoDB. Product activity and profile/preferences are stored server-side in SQLModel storage, SQLite by default.

### 25. Is demo data real?
**Answer:** No. Demo seeding creates synthetic persona history and sample records.

## Safety, privacy, and security

### 26. Is MaxxLoop a medical product?
**Answer:** No. It does not diagnose or treat conditions, and its score is not clinically validated.

### 27. What happens when crisis language is entered?
**Answer:** A limited phrase scanner can pause the normal check-in flow and return support resources. It can miss meaning and is not emergency monitoring.

### 28. Is a doctor part of the team/product?
**Answer:** There is no clinician built into the current product and no clinical review is established by the repo. Professional review is a future requirement before any clinical positioning.

### 29. Is data zero-knowledge or device-only?
**Answer:** No such claim is supported. Product data is stored by the backend; accounts/sessions use MongoDB.

### 30. Can users export or delete data?
**Answer:** The API has export and product-data deletion endpoints. Deletion retains account/session infrastructure and profile while deleting activity records and priors; it is not account deletion.

## Scalability, business, innovation, and limits

### 31. Is it deployed publicly?
**Answer:** No verified production deployment is documented in this repository. There is a Dockerfile/Compose setup, but Compose does not include MongoDB and needs configuration review.

### 32. How would you scale it?
**Answer:** First establish managed durable storage, deployment secrets/networking, observability, backups, rate limits, and a reviewed security/privacy process. Then measure real workload before scaling architecture.

### 33. What evidence do you have?
**Answer:** There is an implemented software flow and a synthetic simulation. Simulation output is not user evidence or clinical validation.

### 34. What is the business model?
**Answer:** The current code does not implement billing or validate a business model. A possible future path could be explored with users/institutions, but that is a hypothesis.

### 35. What is the biggest risk?
**Answer:** Users may interpret an estimated score or limited recommendation as more authoritative than it is. Clear non-medical language, careful safety review, and real-user evaluation are essential.

### 36. What would you build next?
**Answer:** Usability and API/browser tests, a privacy/security review, clinician-informed safety review, and a careful real-user evaluation before claims of effectiveness.
