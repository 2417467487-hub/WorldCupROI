# Sponsor ROI Model Metrics

- MAE: 0.1183
- RMSE: 0.1442
- R2: 0.8595
- Model: dependency-free ridge regression fallback
- Model card: [sponsor_roi_model_card.md](sponsor_roi_model_card.md)

## Top ROI Drivers

| feature | importance |
| --- | --- |
| a_sponsor_spend_m | 0.1374 |
| a_brand_heat_index | 0.1350 |
| team_a_strength | 0.1296 |
| a_ad_exposure_m | 0.1066 |
| sponsor_team_fit_score | 0.0453 |
| commercial_momentum_score | 0.0439 |
| elo_diff | 0.0422 |
| fan_score | 0.0420 |
| event_attention_m | 0.0355 |
| a_activation_quality | 0.0347 |

## Feature Group Importance

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.4591 | a_sponsor_spend_m | 8 |
| team_strength | 0.1718 | team_a_strength | 2 |
| business_intelligence_indices | 0.1269 | sponsor_team_fit_score | 6 |
| media_attention | 0.1261 | fan_score | 6 |
| player_influence | 0.0839 | a_player_followers_m | 5 |
| text_sentiment | 0.0348 | text_signal_score | 2 |
| venue_weather | 0.0195 | host_advantage_a | 1 |
| injury_availability | 0.0147 | a_avg_injury_risk | 2 |

## Interpretation

The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.