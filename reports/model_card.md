# Model Card

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
| text_sentiment | 0.0640 | news_sentiment_score | 1 |

## Sponsor ROI Model

- Task: regress sponsor ROI proxy.
- Inputs: media exposure, sponsor power, brand fit, activation quality, team strength, stage premium, weather impact, injury risk, text/social momentum.
- Label construction: `sponsor_roi` is a constructed proxy, not audited revenue.
- Training split: same deterministic reproducible holdout split.
- MAE: 0.1213
- RMSE: 0.1489
- R2: 0.8590

### ROI Feature Groups

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.5237 | a_brand_heat_index | 8 |
| team_strength | 0.1625 | team_a_strength | 2 |
| business_intelligence_indices | 0.1436 | sponsor_team_fit_score | 6 |
| media_attention | 0.1260 | fan_score | 6 |
| player_influence | 0.0953 | a_core_market_value_m | 5 |
| text_sentiment | 0.0348 | text_signal_score | 2 |
| venue_weather | 0.0202 | host_advantage_a | 1 |
| injury_availability | 0.0124 | a_avg_injury_risk | 2 |

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