# Causal Inference Report

## Goal

Separate correlation from causal evidence for media exposure, event attention, and player performance effects on sponsor ROI.

## Method

This module uses a DoWhy/EconML-compatible residualized double-ML baseline: treatment and ROI are residualized against confounders, then the treatment effect is estimated on residuals with fold-based uncertainty.

Production upgrade path: replace the baseline estimator with DoWhy identification/refutation and EconML DML/DRLearner once audited treatment, outcome, and instrument definitions are available.

## Correlation vs Causal Effect

| treatment | column | correlation_with_roi | causal_effect_residualized | effect_ci_low | effect_ci_high | effect_direction | method | controls | samples |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| media_exposure | exposure_score | 0.2243 | 0.7113 | 0.5427 | 0.8595 | positive | DoWhy/EconML-compatible residualized double-ML baseline | team_elo, sponsor_power_index, brand_fit, activation_quality, sponsor_spend_m, temperature_c, humidity | 1944 |
| event_attention | event_attention_m | 0.1971 | 0.0095 | 0.0078 | 0.0117 | positive | DoWhy/EconML-compatible residualized double-ML baseline | team_elo, sponsor_power_index, brand_fit, activation_quality, sponsor_spend_m, temperature_c, humidity | 1944 |
| player_performance | core_player_rating | 0.2833 | 0.0066 | 0.0019 | 0.0129 | positive | DoWhy/EconML-compatible residualized double-ML baseline | team_elo, sponsor_power_index, brand_fit, activation_quality, sponsor_spend_m, temperature_c, humidity | 1944 |
| player_reach | player_followers_m | 0.2397 | 0.0009 | -0.0039 | 0.0064 | positive | DoWhy/EconML-compatible residualized double-ML baseline | team_elo, sponsor_power_index, brand_fit, activation_quality, sponsor_spend_m, temperature_c, humidity | 1944 |

## Interpretation Guardrails

- Positive correlation is not automatically causal lift.
- Sponsor spend, brand fit, activation quality, and team strength are treated as confounders.
- Proxy/mock commercial outcomes limit causal claims; report effects as decision evidence, not proof.