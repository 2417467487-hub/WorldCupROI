# Algorithm Strategy

WorldCupROI separates sports prediction from sponsorship decision intelligence.
The current repository keeps dependency-free fallbacks runnable, while documenting production upgrade paths.

| Layer | Role | Current method | Upgrade path |
|---|---|---|---|
| Match Outcome Layer | Estimate win/draw/loss probability as one input to sponsorship value. | CentroidOutcomeModel fallback with deterministic split | calibrated logistic regression, LightGBM multiclass, XGBoost multi:softprob |
| Sponsor ROI Layer | Predict commercial return from sponsor, attention, team, player, and context signals. | RidgeROIModel fallback with standardized features | ElasticNet, LightGBMRegressor, XGBoostRegressor, stacked tabular ensemble |
| Risk And Recommendation Layer | Convert point forecasts into risk-aware scenario recommendations. | bootstrap, Monte Carlo perturbation, conformal intervals | ensemble variance, Bayesian optimization, portfolio allocation policy |
| Relationship Intelligence Layer | Measure sponsor-team-player-match network influence. | weighted heterogeneous graph centrality | GraphSAGE, heterogeneous GNN, temporal graph model |

## Feature Groups

| Group | Features |
|---|---|
| team_strength | elo_diff, market_value_diff_m, recent_goal_diff_delta, team_a_strength |
| player_influence | core_rating_diff, a_core_player_rating, a_core_market_value_m, a_player_followers_m, a_player_fan_growth_30d_pct, a_player_sentiment_score |
| injury_availability | a_avg_injury_risk, a_avg_availability_score, availability_diff, injury_risk_diff |
| coach_context | coach_exp_diff |
| venue_weather | host_advantage_a, stadium_capacity_k, temperature_c, humidity |
| media_attention | event_attention_m, media_reposts_k, engagement_rate, fan_growth_7d_pct, time_decay_attention, fan_score |
| text_sentiment | news_sentiment_score, text_signal_score |
| sponsor_activation | a_sponsor_power_index, a_sponsor_spend_m, a_ad_exposure_m, a_brand_heat_index, a_paid_media_share, a_brand_fit, a_activation_quality, a_historical_sports_presence |
| business_intelligence_indices | media_exposure_index, commercial_momentum_score, injury_risk_score, sponsor_team_fit_score, weather_impact_score, stage_premium_score |