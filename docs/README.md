# MaxxLoop Documentation

Use this index to find product, implementation, and presentation documentation. Code is the source of truth where a document and implementation differ. Planned items are labeled; they are not current capabilities.

| Document | Purpose |
| --- | --- |
| [Project overview](PROJECT_OVERVIEW.md) | Elevator explanations and problem/solution |
| [Product](PRODUCT.md) | Product scope, audience, and user value |
| [User flow](USER_FLOW.md) | Account, loop, demo, and UI states |
| [Architecture](ARCHITECTURE.md) | System components and data flow |
| [Technical architecture](TECHNICAL_ARCHITECTURE.md) | Frameworks, services, configuration, deployment shape |
| [Frontend](FRONTEND.md) | Routes, components, client behavior |
| [Backend](BACKEND.md) | FastAPI routers, engines, persistence |
| [API](API.md) | Implemented routes, schemas, and effects |
| [Database](DATABASE.md) | SQLite/MongoDB responsibilities and lifecycle |
| [Data model](DATA_MODEL.md) | Tables and auth collections |
| [Authentication](AUTHENTICATION.md) | Account/session flow and implementation safeguards |
| [MaxxLoop loop](MAXXLOOP_LOOP.md) | Full technical walkthrough of a loop |
| [Recommender](RECOMMENDER.md) | Candidate filtering, priors, sampling, feedback |
| [Insights](INSIGHTS.md) | Metrics and interpretation |
| [Security](SECURITY.md) | Implemented security controls and open concerns |
| [Privacy](PRIVACY.md) | Data collection, storage, consent, export, deletion |
| [Testing](TESTING.md) | Existing test suites and commands |
| [Development](DEVELOPMENT.md) | Local setup and run instructions |
| [Environment](ENVIRONMENT.md) | Configuration reference; no real secrets |
| [Deployment](DEPLOYMENT.md) | Current config and production gaps |
| [Troubleshooting](TROUBLESHOOTING.md) | Common local-development failures |
| [Hackathon guide](HACKATHON_GUIDE.md) | Judge-facing story, criteria, claims, limitations |
| [Demo script](DEMO_SCRIPT.md) | Timed live walkthrough |
| [Judge Q&A](JUDGE_QA.md) | 30 truthful likely questions and answers |
| [Limitations](LIMITATIONS.md) | Known boundaries and technical limitations |
| [Roadmap](ROADMAP.md) | Current, next, and future work |
| [Evaluation](EVALUATION.md) | Existing synthetic evaluation (not real-user evidence) |

## Documentation rules

- “Implemented” means present in this repository; it does not imply production deployment or independent validation.
- “Planned” means a possible future direction only.
- Do not publish credentials, user data, or environment-file contents.
- Simulation metrics are synthetic outputs and must be labeled as such.
