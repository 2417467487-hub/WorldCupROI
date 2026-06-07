# Sponsor ROI Model Metrics

- MAE: 0.1213
- RMSE: 0.1489
- R2: 0.8590
- Model: dependency-free ridge regression fallback
- Model card: [sponsor_roi_model_card.md](sponsor_roi_model_card.md)

## Top ROI Drivers

| feature | importance |
| --- | --- |
| a_brand_heat_index | 0.1612 |
| a_sponsor_spend_m | 0.1491 |
| a_ad_exposure_m | 0.1246 |
| team_a_strength | 0.1186 |
| sponsor_team_fit_score | 0.0579 |
| commercial_momentum_score | 0.0499 |
| elo_diff | 0.0439 |
| fan_score | 0.0398 |
| event_attention_m | 0.0350 |
| a_core_market_value_m | 0.0298 |

## Feature Group Importance

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

## Interpretation

The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.