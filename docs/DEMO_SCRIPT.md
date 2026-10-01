# MaxxLoop Live Demo Script (3–5 minutes)

Use a test account and synthetic demo persona. Check the running buttons and API health before starting; exact scores/actions can vary. Never show real passwords, personal records, or environment values. A demo seed resets the shared `user_default` dataset, so use demo mode only.

| Time | What to click | What to say | What the judge should notice |
| --- | --- | --- | --- |
| 0:00–0:25 | Open `/` and introduce MaxxLoop | “MaxxLoop connects a short self-check-in to one useful next step and a follow-up measurement. We want to close the gap between tracking and action.” | Clear problem/solution; describe it as a prototype, not a medical tool. |
| 0:25–0:50 | Open `/signup` and create or use a prepared demo account; then `/dashboard` | “Authentication uses email/password. For the demo I use a test account; the auth store is MongoDB and product records are stored separately by the API.” | Actual account flow and dashboard. Do not reveal credentials. |
| 0:50–1:20 | Complete Focus, Energy, Stress check-in; submit | “These are self-reported inputs. The API compares them with available history and returns an estimated capacity score and contributing signal labels.” | Short form, range validation, loading/error response, explanation. |
| 1:20–1:50 | Show drivers and the action/reason panel if one is offered | “When the configured drop and cooldown rules allow it, the system offers one action matched to the active drivers. Selection uses stored per-action Beta priors and Thompson sampling; the default explanation is deterministic template text.” | Single action and inspectable context. A drop is not guaranteed from every input. |
| 1:50–2:20 | Start the action; show timer/steps. If a demo drop is needed, use `/demo` controls. | “The user can start or skip. The action window is normally configured for 25 minutes; demo timewarp can shorten it for presentation.” | Controls correspond to persisted intervention state. Label any seeded data as synthetic. |
| 2:20–3:10 | Complete follow-up Focus/Energy/Stress and submit measurement; send helpful/not helpful feedback | “We record observed self-report change and subtract an estimated no-action drift from prior skipped windows, with a default prior when data is sparse. This is a useful prototype measure, not proof of causation.” | Actual before/after flow and honest caveat. |
| 3:10–3:40 | Open `/history`, then `/insights` | “These views summarize saved signals and outcomes. Helpful ratios and net-effect summaries describe this user’s recorded data, not clinical efficacy.” | Persisted records and summary views. |
| 3:40–4:10 | Open `/privacy`; show consent/export/delete controls without executing destructive action | “Activity records are server-side in SQL storage, while accounts and sessions use MongoDB. The template provider is the default; any external provider must be configured and its data flow disclosed.” | Correct privacy/storage explanation. Do not call it device-only or zero-knowledge. |
| 4:10–4:30 | Conclude | “Our current contribution is the closed user loop. Next we need usability evaluation, stronger safety review, and evidence from real users before making impact claims.” | Clear implementation-versus-roadmap distinction. |

## Recovery plan if live demo stalls

1. Confirm `/health`, MongoDB availability for auth, and frontend/API URLs.
2. If account creation fails, use a previously created test account; do not show an error as a success.
3. If a check-in does not trigger a drop, explain that recommendation is conditional. Use the authenticated demo console’s synthetic trigger only if appropriate.
4. If demo controls fail, continue explaining the actual architecture and be explicit that the live interaction did not complete. A prerecorded clip/screenshot must be identified as prerecorded.

## Judge-safe phrases

- Say “estimated capacity score,” not “clinical stress score.”
- Say “observed self-report difference minus estimated drift,” not “true treatment effect.”
- Say “synthetic demo history,” not “customer data.”
- Say “personalization heuristic,” not “validated AI model.”
