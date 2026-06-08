# Model Card

## Model Governance Summary

| Area | Current status | Risk control |
| --- | --- | --- |
| Data credibility | Historical match outcomes are real-source; commercial ROI labels are proxy/mock | Keep data card visible and replace proxy labels before production decisions |
| Label construction | `result` from match scores; `sponsor_roi` from engineered commercial proxy | Avoid using model outputs or post-decision artifacts as labels |
| Training validation | Deterministic holdout plus k-fold, sub-sample, and temporal sliding validation | Monitor fold variance, sample-size sensitivity, and tournament-era drift before production |
| Deployment use | Decision support and portfolio demo | Use risk intervals and data-origin labels in business review |

## Match Outcome Model

- Task: classify match result as `A_win`, `draw`, or `B_win`.
- Inputs: Elo difference, market value difference, coach experience, player availability, injury risk, weather, stage, and attention context.
- Label construction: historical `result` from match score data.
- Training split: deterministic split defined in `algorithm_strategy.deterministic_split`; current pipeline uses a reproducible holdout split.
- Accuracy: 0.5566
- Log loss: 0.9780

### Match Feature Groups

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| team_strength | 1.3094 | recent_goal_diff_delta | 3 |
| player_influence | 1.2631 | core_rating_diff | 4 |
| coach_context | 0.3501 | coach_exp_diff | 1 |
| venue_weather | 0.2818 | host_advantage_a | 4 |
| media_attention | 0.2649 | media_reposts_k | 4 |
| injury_availability | 0.2500 | availability_diff | 4 |
| text_sentiment | 0.0641 | news_sentiment_score | 1 |

## Cross-Validation Generalization

| validation_type | task | model | metric | folds | mean | std | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kfold | match_outcome | CentroidOutcomeModel | accuracy | 5 | 0.5436 | 0.0389 | 0.5026 | 0.6010 |
| kfold | match_outcome | CentroidOutcomeModel | log_loss | 5 | 0.9861 | 0.0230 | 0.9584 | 1.0150 |
| kfold | sponsor_roi | RidgeROIModel | mae | 5 | 0.1165 | 0.0072 | 0.1084 | 0.1254 |
| kfold | sponsor_roi | RidgeROIModel | r2 | 5 | 0.8813 | 0.0131 | 0.8670 | 0.8991 |
| kfold | sponsor_roi | RidgeROIModel | rmse | 5 | 0.1426 | 0.0074 | 0.1329 | 0.1495 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5438 | 0.0000 | 0.5438 | 0.5438 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9784 | 0.0000 | 0.9784 | 0.9784 |
| subsample_55pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1167 | 0.0000 | 0.1167 | 0.1167 |
| subsample_55pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8830 | 0.0000 | 0.8830 | 0.8830 |
| subsample_55pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1439 | 0.0000 | 0.1439 | 0.1439 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5552 | 0.0000 | 0.5552 | 0.5552 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9401 | 0.0000 | 0.9401 | 0.9401 |
| subsample_70pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1150 | 0.0000 | 0.1150 | 0.1150 |
| subsample_70pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8797 | 0.0000 | 0.8797 | 0.8797 |
| subsample_70pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1409 | 0.0000 | 0.1409 | 0.1409 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5310 | 0.0000 | 0.5310 | 0.5310 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0107 | 0.0000 | 1.0107 | 1.0107 |
| subsample_85pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1126 | 0.0000 | 0.1126 | 0.1126 |
| subsample_85pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8921 | 0.0000 | 0.8921 | 0.8921 |
| subsample_85pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1407 | 0.0000 | 0.1407 | 0.1407 |

## Sponsor ROI Model

- Task: regress sponsor ROI proxy.
- Inputs: media exposure, sponsor power, brand fit, activation quality, team strength, stage premium, weather impact, injury risk, text/social momentum.
- Label construction: `sponsor_roi` is a constructed proxy, not audited revenue.
- Training split: same deterministic reproducible holdout split.
- MAE: 0.1184
- RMSE: 0.1446
- R2: 0.8779

### ROI Feature Groups

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.4925 | a_sponsor_spend_m | 8 |
| team_strength | 0.1755 | team_a_strength | 2 |
| business_intelligence_indices | 0.1293 | commercial_momentum_score | 6 |
| media_attention | 0.1233 | fan_score | 6 |
| player_influence | 0.0873 | a_core_market_value_m | 5 |
| text_sentiment | 0.0348 | text_signal_score | 2 |
| venue_weather | 0.0193 | host_advantage_a | 1 |
| injury_availability | 0.0116 | a_avg_injury_risk | 2 |

## Limitations

- ROI accuracy is bounded by proxy commercial labels.
- Historical match data may not represent 2026 sponsor behavior.
- Lightweight text features do not capture full narrative causality.
- Current models are interpretable fallbacks; production should compare calibrated tree/boosting and causal uplift models.

## Potential Data Leakage Risks

- Post-match engagement or result-derived variables can leak future information if used for pre-match prediction.
- `commercial_momentum_score` may blend variables close to the ROI label construction.
- Generated `predicted_roi` must never be fed back as a training label.
- Scenario outputs should remain downstream decision artifacts, not supervised labels.