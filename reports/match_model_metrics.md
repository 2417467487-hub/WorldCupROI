# Match Outcome Model Metrics

- Accuracy: 0.5566
- Log loss: 0.9780
- Model: dependency-free centroid classifier fallback
- Model card: [match_outcome_model_card.md](match_outcome_model_card.md)

## Top Features

| feature | importance |
| --- | --- |
| recent_goal_diff_delta | 0.4463 |
| elo_diff | 0.4317 |
| market_value_diff_m | 0.4314 |
| core_rating_diff | 0.3945 |
| coach_exp_diff | 0.3501 |
| a_core_player_rating | 0.3165 |
| a_core_market_value_m | 0.3131 |
| a_player_followers_m | 0.2389 |
| host_advantage_a | 0.1245 |
| availability_diff | 0.1124 |

## Feature Group Importance

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| team_strength | 1.3094 | recent_goal_diff_delta | 3 |
| player_influence | 1.2631 | core_rating_diff | 4 |
| coach_context | 0.3501 | coach_exp_diff | 1 |
| venue_weather | 0.2818 | host_advantage_a | 4 |
| media_attention | 0.2649 | media_reposts_k | 4 |
| injury_availability | 0.2500 | availability_diff | 4 |
| text_sentiment | 0.0641 | news_sentiment_score | 1 |