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
- Accuracy: 0.5023
- Log loss: 1.0097

### Match Feature Groups

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| team_strength | 1.3420 | recent_goal_diff_delta | 3 |
| player_influence | 1.2839 | core_rating_diff | 4 |
| injury_availability | 0.4122 | availability_diff | 4 |
| coach_context | 0.3630 | coach_exp_diff | 1 |
| venue_weather | 0.2669 | host_advantage_a | 4 |
| media_attention | 0.2477 | time_decay_attention | 4 |
| text_sentiment | 0.0569 | news_sentiment_score | 1 |

## Cross-Validation Generalization

| validation_type | task | model | metric | folds | mean | std | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kfold | match_outcome | CentroidOutcomeModel | accuracy | 5 | 0.5236 | 0.0494 | 0.4639 | 0.6000 |
| kfold | match_outcome | CentroidOutcomeModel | log_loss | 5 | 0.9888 | 0.0189 | 0.9707 | 1.0165 |
| kfold | sponsor_roi | RidgeROIModel | mae | 5 | 0.1159 | 0.0085 | 0.1061 | 0.1278 |
| kfold | sponsor_roi | RidgeROIModel | r2 | 5 | 0.8447 | 0.0108 | 0.8364 | 0.8632 |
| kfold | sponsor_roi | RidgeROIModel | rmse | 5 | 0.1424 | 0.0083 | 0.1325 | 0.1518 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5571 | 0.0000 | 0.5571 | 0.5571 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9801 | 0.0000 | 0.9801 | 0.9801 |
| subsample_55pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1154 | 0.0000 | 0.1154 | 0.1154 |
| subsample_55pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8459 | 0.0000 | 0.8459 | 0.8459 |
| subsample_55pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1432 | 0.0000 | 0.1432 | 0.1432 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5411 | 0.0000 | 0.5411 | 0.5411 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9566 | 0.0000 | 0.9566 | 0.9566 |
| subsample_70pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1120 | 0.0000 | 0.1120 | 0.1120 |
| subsample_70pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8565 | 0.0000 | 0.8565 | 0.8565 |
| subsample_70pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1378 | 0.0000 | 0.1378 | 0.1378 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4863 | 0.0000 | 0.4863 | 0.4863 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0182 | 0.0000 | 1.0182 | 1.0182 |
| subsample_85pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1160 | 0.0000 | 0.1160 | 0.1160 |
| subsample_85pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8358 | 0.0000 | 0.8358 | 0.8358 |
| subsample_85pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1438 | 0.0000 | 0.1438 | 0.1438 |

## Sponsor ROI Model

- Task: regress sponsor ROI proxy.
- Inputs: media exposure, sponsor power, brand fit, activation quality, team strength, stage premium, weather impact, injury risk, text/social momentum.
- Label construction: `sponsor_roi` is a constructed proxy, not audited revenue.
- Training split: same deterministic reproducible holdout split.
- MAE: 0.1165
- RMSE: 0.1443
- R2: 0.8478

### ROI Feature Groups

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.3038 | a_ad_exposure_m | 8 |
| media_attention | 0.1436 | fan_score | 6 |
| team_strength | 0.1396 | team_a_strength | 2 |
| business_intelligence_indices | 0.1176 | commercial_momentum_score | 6 |
| player_influence | 0.0680 | a_core_market_value_m | 5 |
| venue_weather | 0.0203 | host_advantage_a | 1 |
| injury_availability | 0.0177 | a_avg_availability_score | 2 |
| text_sentiment | 0.0159 | news_sentiment_score | 2 |

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