# Counterfactual Engine Report

## Scope

Simulate player absence, media change, budget change, and negative news shocks to estimate ROI changes and risk intervals.

## Method

Current baseline is SCM/synthetic-control compatible: observed high-ROI sponsor opportunities are perturbed with structured treatment shocks and interval widths. Production upgrade can replace multipliers with synthetic-control donor pools.

## Scenario Summary

| counterfactual | avg_delta | avg_roi | worst_case_roi |
| --- | --- | --- | --- |
| media_surge | 0.5886 | 4.7928 | 4.3718 |
| budget_increase | 0.3363 | 4.5406 | 4.1180 |
| budget_cut | -0.2943 | 3.9099 | 3.4986 |
| player_absent | -0.5045 | 3.6997 | 3.2554 |
| negative_news_shock | -0.7568 | 3.4475 | 2.9517 |