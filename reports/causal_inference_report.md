# Causal Inference Report

## Objective

Estimate whether media exposure, fan influence, team strength and commercial momentum have plausible causal effects on sponsor ROI after adjusting for observed confounders.

## Correlation vs Causation

A raw correlation can be inflated by tournament stage, team strength, sponsor spend or player availability. This module therefore reports a backdoor-adjusted baseline estimate. It is designed so DoWhy, EconML or Causal Forest can replace the estimator without changing downstream reports.

## Treatment Effects

| treatment | label | standardized_effect | ci_low | ci_high | method | sample_size |
| --- | --- | --- | --- | --- | --- | --- |
| media_exposure_index | Media exposure | 0.2786 | 0.2466 | 0.3106 | backdoor-adjusted OLS baseline | 964 |
| fan_score | Fan influence | 0.3775 | 0.3455 | 0.4095 | backdoor-adjusted OLS baseline | 964 |
| team_a_strength | Team strength | 0.3106 | 0.2742 | 0.347 | backdoor-adjusted OLS baseline | 964 |
| commercial_momentum_score | Commercial momentum | 0.688 | 0.661 | 0.7151 | backdoor-adjusted OLS baseline | 964 |

## Upgrade Path

- DoWhy: define graph assumptions and run refutation tests.
- EconML / Causal Forest: estimate heterogeneous treatment effects by sponsor category, tournament stage and team profile.
- Sensitivity analysis: test unobserved confounding around player injury and sponsor contract quality.