# Sponsor ROI Model Metrics

- MAE: 0.1177
- RMSE: 0.1435
- R2: 0.8838
- Model: dependency-free ridge regression fallback
- Model card: [sponsor_roi_model_card.md](sponsor_roi_model_card.md)

## Top ROI Drivers

| feature | importance |
| --- | --- |
| a_brand_heat_index | 0.1568 |
| a_sponsor_spend_m | 0.1300 |
| a_ad_exposure_m | 0.1252 |
| team_a_strength | 0.1153 |
| sponsor_team_fit_score | 0.0527 |
| commercial_momentum_score | 0.0512 |
| a_activation_quality | 0.0445 |
| elo_diff | 0.0426 |
| fan_score | 0.0403 |
| event_attention_m | 0.0336 |

## Feature Group Importance

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.5081 | a_brand_heat_index | 8 |
| team_strength | 0.1579 | team_a_strength | 2 |
| business_intelligence_indices | 0.1395 | sponsor_team_fit_score | 6 |
| media_attention | 0.1216 | fan_score | 6 |
| player_influence | 0.0785 | a_player_followers_m | 5 |
| text_sentiment | 0.0355 | text_signal_score | 2 |
| venue_weather | 0.0181 | host_advantage_a | 1 |
| injury_availability | 0.0121 | a_avg_injury_risk | 2 |

## Interpretation

The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.