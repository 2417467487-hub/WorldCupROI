# Sponsor Optimization Engine

## Objective

Maximize sponsor ROI under explicit budget constraints while penalizing downside risk and rewarding fan attention, media exposure, and commercial momentum.

## Optimization Methods

- Bayesian optimization baseline: upper-confidence style acquisition score over sponsor-team-stage candidates.
- Reinforcement learning baseline: contextual bandit value score that rewards ROI, exposure, and repeated evidence while penalizing risk.
- Portfolio policy: greedy budget allocation with sponsor diversity control and risk-adjusted ROI ranking.

## Portfolio Summary

| budget_cap_m | allocated_budget_m | expected_portfolio_roi | risk_score | risk_adjusted_roi | sponsor_count |
| --- | --- | --- | --- | --- | --- |
| 25.0000 | 25.0000 | 4.1407 | 0.3424 | 3.9524 | 1.0000 |
| 50.0000 | 50.0000 | 4.0790 | 0.3387 | 3.8928 | 2.0000 |
| 100.0000 | 99.8900 | 4.0337 | 0.3381 | 3.8478 | 2.0000 |
| 150.0000 | 146.8750 | 4.0012 | 0.3397 | 3.8144 | 3.0000 |

## Top Recommended Allocations

| budget_cap_m | team | sponsor | stage | recommended_budget_m | expected_roi | risk_score | optimizer_score | decision_rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 25.0000 | Brazil | Adidas | group_or_knockout | 25.0000 | 4.1407 | 0.3424 | 4.3543 | bayesian_ucb_plus_rl_value |
| 50.0000 | Brazil | Adidas | group_or_knockout | 26.5000 | 4.1407 | 0.3424 | 4.3543 | bayesian_ucb_plus_rl_value |
| 50.0000 | Russia | Hyundai | group_or_knockout | 23.5000 | 4.0095 | 0.3345 | 4.1832 | bayesian_ucb_plus_rl_value |
| 100.0000 | Brazil | Adidas | group_or_knockout | 26.5000 | 4.1407 | 0.3424 | 4.3543 | bayesian_ucb_plus_rl_value |
| 100.0000 | Russia | Hyundai | group_or_knockout | 27.7000 | 4.0095 | 0.3345 | 4.1832 | bayesian_ucb_plus_rl_value |
| 100.0000 | Hungary | Adidas | group_or_knockout | 20.2200 | 4.0503 | 0.3297 | 4.1433 | bayesian_ucb_plus_rl_value |
| 100.0000 | Argentina | Hyundai | group_or_knockout | 25.4700 | 3.9357 | 0.3444 | 4.0950 | bayesian_ucb_plus_rl_value |
| 150.0000 | Brazil | Adidas | group_or_knockout | 26.5000 | 4.1407 | 0.3424 | 4.3543 | bayesian_ucb_plus_rl_value |
| 150.0000 | Russia | Hyundai | group_or_knockout | 27.7000 | 4.0095 | 0.3345 | 4.1832 | bayesian_ucb_plus_rl_value |
| 150.0000 | Hungary | Adidas | group_or_knockout | 20.2200 | 4.0503 | 0.3297 | 4.1433 | bayesian_ucb_plus_rl_value |
| 150.0000 | Argentina | Hyundai | group_or_knockout | 25.4700 | 3.9357 | 0.3444 | 4.0950 | bayesian_ucb_plus_rl_value |
| 150.0000 | Brazil | Adidas | tournament | 19.8750 | 3.9960 | 0.3513 | 4.0553 | bayesian_ucb_plus_rl_value |
| 150.0000 | France | Qatar Airways | group_or_knockout | 27.1100 | 3.8852 | 0.3369 | 4.0366 | bayesian_ucb_plus_rl_value |

## Decision Guardrails

- Treat this as a decision baseline, not a binding media plan.
- Replace proxy commercial variables with audited sponsor revenue data before production use.
- Use causal and counterfactual reports before increasing budget materially.