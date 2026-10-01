# Project Overview

## In one sentence

MaxxLoop turns a short focus/energy/stress check-in into an explanation, one small suggested action, and a follow-up record that can inform future suggestions.

## 30-second explanation

Students and knowledge workers can notice that they feel overloaded without knowing what small step to take next or whether it helped. MaxxLoop compares a user’s check-in with available recent signals, explains the main contributors, offers one action from a curated library, and asks for another check-in. Feedback is saved so later recommendations can adapt. It is a wellness/productivity prototype, not a medical device or clinical diagnosis system.

## One-minute explanation

MaxxLoop is designed around a personal learning loop: Track, Understand, Act, Measure, Improve. A person reports focus, energy, and stress on a short check-in. The API combines those values with available activity signals and historical baselines to compute a bounded capacity estimate. It identifies contributors, applies drop/cooldown rules, and may recommend one action. After the action window, the user can report their state again and whether the action felt helpful. The system records the before/after difference, an estimated no-action drift, and feedback. A statistical recommender uses prior outcomes to adjust which actions it samples. These are self-report measurements and estimates; they do not establish medical status or causal effectiveness.

## Technical explanation

The web client is Next.js App Router with React and TypeScript. It calls a FastAPI API using credentialed HTTP requests and a session cookie. MongoDB stores account/session records; SQLModel persists product records in the configured relational database (SQLite by default). The API’s baseline, capacity, driver, drop-detection, recommender, and measurement modules implement deterministic/statistical logic. Explanation text defaults to a template provider, with optional Gemini, Ollama, and OpenAI-compatible providers. See [Architecture](ARCHITECTURE.md), [Recommender](RECOMMENDER.md), and [API](API.md).

## Problem and core idea

The product addresses a product-design gap: self-tracking can produce information without an immediate next step, generic advice may not fit the moment, and users may not record whether an action helped them. MaxxLoop connects these stages in one repeatable flow. This is the project’s intended value proposition, not a market-wide claim that competitors lack these features.

## Audience and output

Initial intended users are students and knowledge workers who want lightweight focus/recovery support. Each loop can produce a capacity estimate, signal-driver labels, an offered action, a measured outcome, and a helpfulness response. Insights summarize records already present for the signed-in user.

## What the system learns

For each user/action pair, an `ActionPrior` stores Beta parameters (`alpha`, `beta`). Measurement updates one parameter based on whether the computed net effect crosses a threshold. This is a lightweight online statistical heuristic, not a trained model and not proof that the action caused a change.

## Non-medical boundary

MaxxLoop does not diagnose, treat, prescribe, or replace professional care. Its capacity score is a product estimate, not a validated clinical measure. Crisis phrase scanning is limited. See [Privacy](PRIVACY.md) and [Limitations](LIMITATIONS.md).
