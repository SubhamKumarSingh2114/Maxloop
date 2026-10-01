# Insights

`GET /insights` builds a response from stored snapshots, interventions, outcomes, and drivers for the authenticated user (or demo profile when explicitly selected).

The response schema includes:

- `total_loops_closed` and `current_streak`
- `pct_helpful` from recorded helpfulness responses
- `avg_score_improvement` based on stored measurement outcomes
- `top_actions` with action ID/title/category, use count, mean net effect, interval bounds, and helpful ratio
- recurring drivers, time-of-day distribution, weekly trend

These are descriptive aggregates of available records. A stored `net_effect` subtracts an estimated no-action drift; it is not a measured causal treatment effect. Action confidence labels/interval calculations should be interpreted as prototype estimates. Sparse data can produce empty or low-information results. Demo seed data includes synthetic records and should be labeled accordingly.

The frontend’s `/insights` page renders the API response and charts/components. `/history` calls the signals endpoint with a limit. Exact charts and empty-state copy should be read from the current route files.
