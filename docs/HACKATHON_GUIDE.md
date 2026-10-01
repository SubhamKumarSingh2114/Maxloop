# MaxxLoop Hackathon Guide

This is the current, implementation-grounded guide to explaining and demonstrating MaxxLoop. Use this document over older pitch notes when they make stronger claims than the running code supports. In particular, do not describe MaxxLoop as a doctor, clinically validated, zero-knowledge, or already deployed to production.

## 1. MaxxLoop in one sentence

**MaxxLoop helps students and knowledge workers notice when their focus and energy are slipping, choose one small recovery action, and check whether it helped them personally.**

The product loop is **Track → Understand → Act → Measure → Improve**. The main idea is to make a wellness check-in lead to a useful next step and a follow-up measurement, instead of stopping at a chart or a generic list of advice.

### 30-second pitch

“Students and knowledge workers often realize they are overloaded only after their focus has already dropped. Most tools show historical charts or offer generic tips. MaxxLoop uses lightweight self-reported signals to estimate a person’s current capacity against their own recent baseline. It explains the main contributors, suggests one small action, and asks for a follow-up check-in to learn what seems helpful for that person. It is a wellness-support prototype, not a medical device or a substitute for professional care.”

## 2. Problem, users, and solution

### The problem

People have limited attention and energy, especially during study or demanding work. A dashboard may show a low score without telling someone what to do next. A long list of wellness tips can also make a tired person choose among too many options. There is room for a simple experience that connects a check-in, an understandable explanation, one action, and a follow-up.

### Who it is for

The initial audience is students and knowledge workers who want lightweight support for focus and recovery. The current product does not diagnose burnout, anxiety, depression, ADHD, or any other condition.

### What the app does today

1. The user signs in and completes a short check-in for focus, energy, and stress, with an optional note.
2. The API compares recent signals with the user’s available baseline and estimates a capacity score.
3. The app presents contributing factors in plain language and recommends a single small action.
4. The user can start or skip the action, then record another check-in after the action window.
5. The user can say whether the action felt helpful. The app records the outcome and uses past results to inform later recommendations.
6. Insights and history show the user’s recorded activity and outcomes.

The current demo also has seeded personas and controls to create a sample capacity drop or advance a measurement window. Demo data is illustrative and may not produce identical scores every time.

## 3. What makes it different

Describe this as MaxxLoop’s product distinction, not as a claim that no other product does something similar:

- **It closes the loop.** The experience connects a check-in to an action and a later measurement, instead of only collecting data or displaying a trend.
- **It starts with the individual’s baseline.** When enough history exists, the scoring logic compares signals with that user’s own recent pattern; sparse history uses prior values until more observations exist.
- **It gives one next action.** The product aims to reduce decision effort when the user reports low capacity.
- **It makes the reasoning inspectable.** The app can show contributing signal categories and recommendation context rather than presenting a mysterious score alone.
- **It learns from feedback.** A lightweight Beta/Thompson-sampling recommender balances actions that have worked in prior observations with some exploration. This is an engineering approach in a prototype, not clinical proof that an action works.
- **It has a safety interruption.** Certain crisis-related phrases in check-in notes are intercepted and routed toward support information before the usual recommendation flow. This keyword scanner is limited and cannot guarantee that a crisis is detected.

### Simple comparison for judges

| Typical experience | MaxxLoop’s intended contribution |
| --- | --- |
| A chart reports a trend | A check-in leads to an explanation and a next step |
| A list shows many tips | The app offers one small action at a time |
| Advice is not followed up | A later check-in records the user’s observed response |
| Generic suggestions | Recommendations can adapt to the user’s recorded feedback |

Avoid naming competitors or saying “first,” “only,” “proven,” or “guaranteed” unless you have independent evidence.

## 4. Fit with the hackathon

The official ASYNC’26 Wellness & Lifestyle problem statement calls for turning everyday signals into understanding and improvement, and describes a flow of Track → Understand → Act → Measure → Improve. That aligns closely with MaxxLoop’s product loop. The published idea-deck guidance asks for the project/team, track, problem, idea, solution, technical architecture/workflow, technologies, and differentiator. Its published idea-stage scoring weights are technical execution/architecture 30%, innovation 20%, impact 20%, product experience/usability 15%, and demo/completeness 15%.

The event page also lists the final build period as September 30–October 1, 2026. Treat the published weights as the rubric on that page; do not assume they necessarily constitute a separate final-round judging rubric unless the organizers say so.

Sources: [ASYNC’26 problem statements and idea-deck criteria](https://async26.vercel.app/problem-statements-pdf) · [ASYNC’26 rules](https://async26.vercel.app/rules)

### How to map your explanation to the published criteria

- **Technical execution / architecture:** show the real frontend-to-API flow, auth boundary, scoring, recommendation, and measurement.
- **Innovation:** explain the complete personal feedback loop and one-action experience. Frame it as your design contribution, not a universal first.
- **Impact:** explain the focused initial audience and why a timely, small action could help. Present this as a hypothesis to validate with users.
- **Product experience:** demonstrate a concise check-in, understandable explanation, one recommendation, and follow-up.
- **Demo / completeness:** finish one full loop and show its record in history or insights. Be transparent about seeded demo controls and the limits of the current evidence.

## 5. Technical overview

### Stack

- **Web:** Next.js App Router, React, TypeScript, Tailwind CSS, Recharts, and Lucide icons.
- **API:** Python FastAPI, Pydantic, SQLModel/SQLAlchemy.
- **Product records:** SQLite stores signals, check-ins, capacity snapshots, interventions, outcomes, and related consent/profile data through the configured `DATABASE_URL` (local default: `sqlite:///./maxxloop.db`).
- **Authentication:** MongoDB stores account and server-side session records, configured with `MONGODB_URI` and `MONGODB_DATABASE`. In the local setup, the URI points to the developer’s MongoDB service. Do not publish connection strings or credentials.
- **Language layer:** a deterministic template provider works without an external API key. Optional provider integrations exist in the code; do not claim a remote model is active unless you have configured and verified it for the demo.

### Architecture at a glance

```text
Browser (Next.js / React)
       │ HTTP requests, session cookie
       ▼
FastAPI application
  ├── Authentication and session checks ── MongoDB
  ├── Check-ins, scoring, loops, insights ── SQLite
  ├── Recommendation and measurement logic
  └── Optional language provider (template by default)
```

### Main request flow

1. The browser sends a request to the FastAPI service; the frontend’s API URL is controlled by its configuration/environment.
2. Protected API routes resolve the authenticated user from the session cookie.
3. User-owned product records are read or written with that user identity in scope.
4. The check-in is evaluated, a capacity estimate and contributing factors are computed, and a candidate action is selected.
5. Starting/skipping, measuring, and helpfulness feedback update the loop record and recommendation history.
6. Insights and history read back the user’s stored records.

The repository includes endpoints grouped around `/health`, `/auth/*`, `/signals`, `/checkins`, `/capacity/now`, `/loop/*`, `/insights`, `/privacy/*`, and `/demo/*`. The API docs and route implementation are the source of truth for request schemas.

### How to explain the scoring

Use a simple explanation first: **“The score is an estimate of current capacity relative to recent patterns, not a medical measurement.”**

For a technical judge:

- The system uses recent personal history where enough observations exist and falls back or blends with broader prior values where history is sparse.
- It uses robust statistics (including a median and median absolute deviation) to reduce the influence of unusual observations.
- Available signals are standardized, direction-adjusted where needed, weighted, and combined into a bounded 0–100 estimate. A score near 50 is the reference point in this scoring scheme, not a population norm or clinical threshold.
- A drop may open a recommendation loop. Cooldowns and daily limits constrain repeated interventions.

Do not call this a clinically validated biomarker or say a score diagnoses a person’s state.

### How to explain personalization

“We keep lightweight success/failure evidence for actions and use Thompson sampling over Beta distributions to choose between actions with promising history and some exploration. It is a way to personalize recommendations from observed app feedback. Our current simulation is synthetic, so we still need real-user evaluation before making effectiveness claims.”

The measurement compares the user’s before and after self-report and estimates expected no-action drift from prior control-like windows. Some values fall back to a prior when there is little history. This is **not a randomized controlled trial and does not establish that the action caused the change**.

## 6. Privacy, authentication, and data

Be precise about where information currently lives:

- MongoDB is used for authentication accounts and sessions.
- SQLite is used by the API for product activity and recommendation records. In a deployed setup, that would be server-side storage with a persistent volume; it is not device-only storage.
- Passwords are stored as password hashes, not plaintext. Session cookies are HTTP-only; server-side session tokens are stored in hashed form.
- The privacy UI includes consent, export, and deletion-related controls. Explain what these do only after confirming the current deployed environment and retention behavior.
- The default language provider is a local deterministic template implementation. If an external LLM provider is enabled, explain its configured data flow and consent accurately. Do not promise that no information ever leaves the device.
- The app’s optional note is sensitive. The safety scanner intercepts recognized crisis phrases before the normal flow; the scanner is not a complete safety monitor.

**Do not repeat older repository pitch claims** that MaxxLoop is “zero-knowledge,” that all data stays on the user’s device, or that the app is GDPR/DPDP compliant. Those are not established by the current architecture or this guide. Also do not expose `.env` contents, passwords, MongoDB credentials, or real user records during a demo.

## 7. The doctor / clinical part

There is no doctor or clinician built into the current product, and no clinical review or validation is established by the current project materials. MaxxLoop is a **non-medical focus and wellness-support prototype**. It does not diagnose, treat, prescribe, or replace a clinician.

The responsible answer to “What does the doctor do?” is:

> “A doctor is not part of the current product, and we are not presenting this as medical care. The current safety behavior is a limited phrase-based interruption that displays support resources. Before using this with real users at scale, we would want qualified mental-health professionals to review the language, low-risk action library, escalation flow, and evaluation plan.”

If someone may be in immediate danger, direct them to local emergency services or a trusted person. For India, the Ministry of Health and Family Welfare lists Tele-MANAS at **14416** and **1-800-891-4416**. Confirm current availability and local resources before presenting them as live support. [National Mental Health Programme / Tele-MANAS](https://dghs.mohfw.gov.in/national-mental-health-programme.php)

Do not say keyword detection is reliable, that it prevents suicide, or that the app monitors a user continuously.

## 8. Live demo walkthrough

Run the app from the repository configuration and verify both services are healthy before presenting. Use your actual configured frontend/API URLs; do not hard-code a port in a slide unless you checked it on that machine.

Recommended route sequence:

1. **Home (`/`)** — explain the user problem and the single-loop promise.
2. **Sign in / sign up** — show the account boundary only with a demo account; never put real credentials on screen.
3. **Dashboard** — complete Focus, Energy, and Stress check-in. Explain the score and drivers as estimates.
4. **Recommendation** — explain why one action was selected. Start or skip it.
5. **Measurement** — complete the follow-up and helpfulness feedback. Point out the observed change and explain the no-action estimate cautiously.
6. **History / Insights (`/history`, `/insights`)** — show that the loop was recorded and how prior user feedback informs later choices.
7. **Privacy (`/privacy`)** — describe the controls and actual storage split honestly.
8. **Demo (`/demo`)** — optional: use seeded personas and time controls to make a repeatable short presentation. Clearly say the personas are demo data.

The other available pages include `/onboarding`, `/profile`, `/login`, and `/signup`. Avoid relying on exact score, action, confidence interval, or net-effect numbers: these may vary with data and state.

### 90-second spoken demo

> “MaxxLoop starts with a quick check-in about focus, energy, and stress. It compares that check-in with the user’s recent pattern and explains the main contributors. Instead of handing an overloaded user a long list, it offers one small action. The user can try it, check in again, and say whether it felt helpful. That response becomes part of the user’s recommendation history. The score and measured change are product estimates, not clinical measurements or proof of causality. This demo persona is seeded data; we still need real-world evaluation to assess impact.”

Then complete one actual loop on screen. If a stage fails, narrate the failure honestly and use the demo console only if the issue is clearly due to live data/setup; do not claim a successful live action that did not complete.

## 9. Likely judge questions and good answers

**“Is this a medical app?”**  
“No. It is a non-medical wellness and focus-support prototype. It does not diagnose or treat conditions. Its capacity score is an estimate, and its safety phrase matching is limited.”

**“What is AI about it?”**  
“The recommendation layer personalizes from recorded feedback using a lightweight Thompson-sampling approach. The default text layer is deterministic templates. We do not need to pretend a generative model is making the core score or that one is active in this demo.”

**“How do you know the action worked?”**  
“We collect a self-reported before/after check-in and compare it with an estimated no-action drift based on prior windows. It helps us track observed response, but it is not randomized evidence or proof of causation.”

**“Where is data stored?”**  
“Authentication accounts and sessions use MongoDB. Activity and recommendation records use the API’s SQLite database. In a hosted deployment, storage and retention would need production configuration and clear disclosure.”

**“What happens with crisis language?”**  
“A limited English/Hindi/Kannada phrase scanner can interrupt the normal recommendation and show support resources. It can miss language or context and is not an emergency monitoring service.”

**“What is your evidence?”**  
“We have a working software flow and synthetic simulations for exercising the recommendation logic. Those simulations are not real-user studies. The next evidence step is supervised usability work and an appropriately reviewed study.”

**“How will it scale?”**  
“The current prototype separates the web client, API, auth store, and product records. Before broader deployment we would address managed persistent storage, operational monitoring, security review, privacy disclosures, and a reviewed safety process. Those are production work, not claims about the current local demo.”

## 10. Evidence and limitations

The repository contains a synthetic simulation of 200 generated users over 30 rounds (6,000 simulated loops). The accompanying evaluation document reports simulation metrics such as helpfulness and capacity change. These are **simulation outputs**, not participant results, independent verification, a clinical study, or evidence that MaxxLoop improves mental health. If you mention the numbers, put “synthetic simulation” beside them on the slide and in your spoken explanation.

Current limitations to acknowledge when relevant:

- No established clinician partnership, clinical validation, or real-user efficacy study.
- Crisis matching relies on a limited phrase list and can miss context, language, spelling, or indirect expressions.
- Before/after self-report and estimated drift do not demonstrate causation.
- The default text provider is template-based; optional external model providers require explicit configuration and data-flow review.
- MongoDB and SQLite need appropriate managed/backup/persistent configuration before a public production deployment. Do not say this project is production-hosted unless it has actually been deployed and verified.
- Direct calendar, wearable, or browser-history integrations should only be described as existing if you can demonstrate their working implementation. Do not imply that the app reads private sources automatically based on the roadmap or old slides.

## 11. Final preparation checklist

- Confirm the frontend and API start with the project’s current configuration and show healthy status.
- Use a demo account and seeded persona; do not display secrets or personal data.
- Rehearse one complete check-in → recommendation → action → measurement → feedback loop.
- Confirm the exact labels and buttons in the running UI before putting them on slides.
- Keep one backup screenshot or short recording in case the live environment fails; label it as a recording.
- Keep simulation numbers visibly labeled as synthetic.
- State the non-medical boundary and measurement limitations plainly.
- Keep the pitch focused: problem, working loop, why the feedback matters, how you protect the user, and what evidence you still need.

## 12. Implemented versus planned

### Implemented in the current repository

- Email/password signup, login, logout, and current-user endpoint with MongoDB-backed accounts/sessions.
- Next.js pages for landing, auth, dashboard, demo, insights, history, profile, onboarding, and privacy.
- Self-report check-in, capacity/baseline estimate, driver labels, drop/cooldown checks, action selection, timer controls, follow-up measurement, feedback, and aggregate insights.
- SQLModel product records and privacy export/delete/consent endpoints.
- Deterministic template explanation provider; optional provider adapters exist in code.
- Authenticated synthetic demo seeding/drop/timewarp endpoints.

### Not currently established as implemented or validated

- Public production deployment or production operations.
- Clinician partnership, clinical review, diagnostic validity, or health outcomes.
- Real-user efficacy evidence; simulation output is synthetic.
- Guaranteed crisis detection, emergency monitoring, or guaranteed safety.
- Automatic calendar, browser history, or wearable collection unless a working integration is separately demonstrated.
- Device-only or zero-knowledge storage, or a legal compliance certification.

### Planned / future work

Usability evaluation, security/privacy review, expert safety review, improved measurement and evaluation, production-ready durable storage/operations, and optional integrations with explicit consent. These are goals, not current features; see [Roadmap](ROADMAP.md).

## 13. Competition positioning and presentation discipline

Position MaxxLoop around a complete user journey and an inspectable prototype architecture. The defensible innovation claim is the project’s integration of check-in, personal-baseline estimate, one action, follow-up, and feedback-driven recommendation state. Avoid “first,” “only,” “proven,” “clinically safe,” or “guaranteed improvement” unless independently substantiated.

The ASYNC’26 official Wellness & Lifestyle prompt describes turning everyday signals into understanding/improvement and the Track → Understand → Act → Measure → Improve pattern. The official page lists idea-deck requirements and published idea-stage weights; those should not be represented as a confirmed final-round rubric unless organizers confirm it. [Problem statements / criteria](https://async26.vercel.app/problem-statements-pdf) · [Rules](https://async26.vercel.app/rules).

For exact click order, use [Demo Script](DEMO_SCRIPT.md); for challenging questions, use [Judge Q&A](JUDGE_QA.md).
