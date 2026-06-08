# Sponsor ROI Model Metrics

- MAE: 0.1184
- RMSE: 0.1446
- R2: 0.8779
- Model: dependency-free ridge regression fallback
- Model card: [sponsor_roi_model_card.md](sponsor_roi_model_card.md)

## Top ROI Drivers

| feature | importance |
| --- | --- |
| a_sponsor_spend_m | 0.1375 |
| a_brand_heat_index | 0.1350 |
| a_ad_exposure_m | 0.1343 |
| team_a_strength | 0.1323 |
| commercial_momentum_score | 0.0487 |
| sponsor_team_fit_score | 0.0443 |
| elo_diff | 0.0432 |
| fan_score | 0.0406 |
| event_attention_m | 0.0347 |
| a_sponsor_power_index | 0.0310 |

## Feature Group Importance

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

## Interpretation

The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.