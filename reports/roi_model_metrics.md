# Sponsor ROI Model Metrics

- MAE: 0.1216
- RMSE: 0.1497
- R2: 0.8326
- Model: dependency-free ridge regression fallback
- Model card: [sponsor_roi_model_card.md](sponsor_roi_model_card.md)

## Top ROI Drivers

| feature | importance |
| --- | --- |
| a_sponsor_spend_m | 0.1390 |
| a_brand_heat_index | 0.1376 |
| team_a_strength | 0.1314 |
| a_ad_exposure_m | 0.1043 |
| sponsor_team_fit_score | 0.0520 |
| elo_diff | 0.0445 |
| commercial_momentum_score | 0.0420 |
| fan_score | 0.0387 |
| event_attention_m | 0.0360 |
| a_core_market_value_m | 0.0319 |

## Feature Group Importance

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.4348 | a_sponsor_spend_m | 8 |
| team_strength | 0.1759 | team_a_strength | 2 |
| business_intelligence_indices | 0.1316 | sponsor_team_fit_score | 6 |
| media_attention | 0.1261 | fan_score | 6 |
| player_influence | 0.0976 | a_core_market_value_m | 5 |
| text_sentiment | 0.0357 | text_signal_score | 2 |
| venue_weather | 0.0213 | host_advantage_a | 1 |
| injury_availability | 0.0174 | a_avg_injury_risk | 2 |

## Interpretation

The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.