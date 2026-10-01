# Recommendation Engine

## What it is

The recommender is a statistical selection mechanism over a curated JSON action library. It is not a trained neural network or general-purpose AI model. The language provider creates explanatory text and is separate from action selection.

## Inputs and candidate filtering

The engine receives the user ID and top driver kinds from the capacity/check-in path. It loads `apps/api/app/data/actions.json` (24 action records in the current file). Candidate actions are those whose `target_drivers` overlap active drivers. If no overlap exists, it falls back to selected general restorative categories.

## Selection

Each `(user_id, action_id)` has an `ActionPrior` with `alpha` and `beta`. A new prior is initialized from action `prior_effect` using total strength 4: `alpha = effect × 4`, `beta = (1-effect) × 4`. The engine samples `theta ~ Beta(alpha,beta)` per candidate and usually selects the highest draw. With default probability 0.15 it chooses a random candidate as exploration when there is more than one. This is Thompson-sampling-style selection with an explicit exploration branch.

## Outcome update

At measurement, the engine calculates observed post-minus-pre score, subtracts estimated no-action drift, and labels confidence from sample count/variance. If net effect is greater than 2 points, alpha increments; otherwise beta increments. User helpfulness is separately recorded. The current code’s prior update is based on net effect threshold, not solely on the explicit helpful/not-helpful boolean.

## Interpretation and limits

Self-report changes, estimated drift, action selection, and prior updates are not randomized evidence. A positive net score does not prove the action caused improvement. Synthetic simulation is not a user study. No validated ML model, online training infrastructure, or causal inference design is implemented.
