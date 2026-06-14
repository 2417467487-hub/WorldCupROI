# Match Outcome Model Metrics

- Accuracy: 0.5023
- Log loss: 1.0097
- Model: dependency-free centroid classifier fallback
- Model card: [match_outcome_model_card.md](match_outcome_model_card.md)

## Top Features

| feature | importance |
| --- | --- |
| recent_goal_diff_delta | 0.4572 |
| elo_diff | 0.4425 |
| market_value_diff_m | 0.4423 |
| core_rating_diff | 0.4117 |
| coach_exp_diff | 0.3630 |
| a_core_player_rating | 0.3240 |
| a_core_market_value_m | 0.3098 |
| a_player_followers_m | 0.2384 |
| availability_diff | 0.1633 |
| host_advantage_a | 0.1223 |

## Feature Group Importance

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| team_strength | 1.3420 | recent_goal_diff_delta | 3 |
| player_influence | 1.2839 | core_rating_diff | 4 |
| injury_availability | 0.4122 | availability_diff | 4 |
| coach_context | 0.3630 | coach_exp_diff | 1 |
| venue_weather | 0.2669 | host_advantage_a | 4 |
| media_attention | 0.2477 | time_decay_attention | 4 |
| text_sentiment | 0.0569 | news_sentiment_score | 1 |