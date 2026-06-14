# Sponsor ROI Model Metrics

- MAE: 0.1165
- RMSE: 0.1443
- R2: 0.8478
- Model: dependency-free ridge regression fallback
- Model card: [sponsor_roi_model_card.md](sponsor_roi_model_card.md)

## Top ROI Drivers

| feature | importance |
| --- | --- |
| team_a_strength | 0.0994 |
| a_ad_exposure_m | 0.0961 |
| a_sponsor_spend_m | 0.0814 |
| a_brand_heat_index | 0.0774 |
| fan_score | 0.0500 |
| commercial_momentum_score | 0.0459 |
| elo_diff | 0.0403 |
| sponsor_team_fit_score | 0.0318 |
| event_attention_m | 0.0312 |
| a_core_market_value_m | 0.0306 |

## Feature Group Importance

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

## Interpretation

The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.