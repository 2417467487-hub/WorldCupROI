# Sponsorship Intelligence Brief

## Executive Summary

WorldCupROI links match context, fan attention, media exposure, sponsor activation, and risk analysis into a repeatable sponsor decision workflow.

## Model Signals

- Match model: - Accuracy: 0.5566
- ROI model: - R2: 0.8687
- Key ROI drivers: a_brand_heat_index, team_a_strength, a_sponsor_spend_m, a_ad_exposure_m, sponsor_team_fit_score, commercial_momentum_score

## Risk and Uncertainty

# ROI Uncertainty Summary

- Average negative ROI probability: 0.0
- Average prediction interval width: 0.434
- Average Monte Carlo std: 0.132
- Medium-risk cases: 119
- High-risk cases: 0
- Methods: Bootstrap residual intervals + Monte Carlo perturbation + variance-based risk score


## Conformal Prediction

# Conformal Prediction Report

## Match Prediction Sets

- Coverage rate: 0.9021
- Average prediction set size: 2.3814
- qhat: 0.811

## ROI Prediction Intervals

- Coverage rate: 0.8814
- Average interval width: 0.4708
- qhat: 0.2354

## Scenario Recommendations

| scenario | roi_lift | risk_level | strategy_recommendation |
| --- | --- | --- | --- |
| knockout_brand_surge | 0.155 | low | Proceed selectively; monitor fan sentiment and player availability. |
| knockout_brand_surge | 0.155 | low | Proceed selectively; monitor fan sentiment and player availability. |
| knockout_brand_surge | 0.155 | low | Proceed selectively; monitor fan sentiment and player availability. |
| knockout_brand_surge | 0.155 | low | Proceed selectively; monitor fan sentiment and player availability. |
| knockout_brand_surge | 0.155 | low | Proceed selectively; monitor fan sentiment and player availability. |
| knockout_brand_surge | 0.155 | low | Proceed selectively; monitor fan sentiment and player availability. |

## Recommended Action

Prioritize sponsor strategies with positive ROI lift and low or medium risk. Use high-risk scenarios as watchlist cases unless media exposure or player availability can be improved.

## Analyst Notes

- Exact sponsor spend remains replaceable with licensed commercial data.
- Text signals are real-source but use lightweight sentiment scoring.
- Production deployment should add SHAP for tree models and calibrated conformal coverage monitoring.