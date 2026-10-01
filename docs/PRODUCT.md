# Product

## Product promise

Help a user move from “I feel off” to one reasonable next action and a follow-up check-in, with a personal history that can guide future suggestions.

## Product principles visible in the implementation

- Short self-report check-in: Focus, Energy, Stress (1–5) and optional note.
- Explainability: capacity response includes score, baseline, delta, status, drivers, sparkline, and timestamp.
- One offered micro-action per triggered intervention.
- A measured follow-up and optional helpfulness feedback.
- User history and insights derived from saved records.
- Non-medical language and a limited safety interruption for detected crisis phrases.

## Current scope

Implemented routes include home, login, signup, dashboard, demo, insights, history, profile, onboarding, and privacy. The API contains check-in, signals, capacity, loop, insights, privacy, demo, authentication, and health routes. See [Frontend](FRONTEND.md) and [API](API.md).

## Product terminology

- **Signal:** one timestamped numeric observation, such as a self-report or imported/manual value.
- **Snapshot:** computed capacity score and baseline at one moment.
- **Intervention:** one offered action linked to a snapshot.
- **Outcome:** before/after scores, estimated drift, net effect, confidence label, and optional feedback.
- **Loop:** the product journey across check-in, action, follow-up, and learning; it is represented through related records rather than a dedicated Loop database table.

## Product non-goals

The current product is not a clinician service, diagnostic tool, emergency monitor, validated clinical intervention, or automatically connected calendar/wearable/browser agent. Any such integrations or clinical use require future implementation, consent, review, and validation.
