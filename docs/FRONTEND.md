# Frontend

The Next.js App Router source is `apps/web/src/app`. Shared components are under `src/components`; API methods are centralized in `src/lib/api.ts`.

| Route | Purpose / interaction | Auth |
| --- | --- | --- |
| `/` | Public product landing and navigation | Public |
| `/login` | Email/password sign-in | Public |
| `/signup` | Create account | Public |
| `/dashboard` | Capacity, check-in, active action loop, follow-up | Authenticated data/API |
| `/demo` | Seed persona, trigger drop, time-warp demo | Authenticated API |
| `/insights` | Personal aggregates, trends, action summaries | Authenticated API |
| `/history` | Signal/history view | Authenticated API |
| `/profile` | Profile and preference surface | Auth-related/product APIs as implemented |
| `/onboarding` | Initial setup/preferences flow | Product route; API requirements depend on page actions |
| `/privacy` | Consent, payload inspection, export, delete controls | Authenticated API |

These route files exist in the source tree. This list is not a claim that a browser test was run during documentation generation.

## Important components

`AuthProvider` restores current user state; `AuthLayout` frames auth pages; `Navbar` links product pages; `CapacityGauge` and `SparklineChart` visualize status/history; `LoopRing` and `CycleProgress` communicate stages; `DriverChip` and `WhyThisDrawer` show context; `ActionTimer` supports timed actions; `DemoBar` exposes demo controls; `CrisisModal` presents the crisis-intercept result; `ThemeProvider` controls theme state; `StatusMessage` renders status feedback.

## API communication

The API wrapper at `src/lib/api.ts` uses `NEXT_PUBLIC_API_URL` or `http://localhost:8000`, JSON requests, and browser credentials. It exposes auth, check-in, capacity, loop, insights, signals, privacy, and demo operations. Non-2xx responses become JavaScript errors using API `detail` where available. Per-page components own loading and error presentation.

## Styling and responsiveness

Tailwind and global CSS define styles; responsive behavior should be confirmed at the target browser sizes. No automated browser/responsive test configuration was found in the inspected repository. Refer to [Testing](TESTING.md).
