# Feature Dictionary

## Core Composite Features

| Feature | Formula Concept | Business Meaning |
|---|---|---|
| `fan_score` | followers + event attention + reposts + fan growth + sentiment + availability | fan influence and commercial attention |
| `a_sponsor_power_index` | spend + ad exposure + brand heat + brand fit + activation quality | sponsor activation strength |
| `media_exposure_index` | reposts + event attention + engagement + recency + text signal | earned and paid media visibility |
| `commercial_momentum_score` | FanScore + Sponsor Power + media exposure + fit + stage premium - injury risk | overall sponsorship opportunity |
| `injury_risk_score` | injury risk + availability loss | commercial downside from player uncertainty |
| `sponsor_team_fit_score` | brand fit + activation quality + brand heat + sports presence | sponsor-team strategic alignment |
| `weather_impact_score` | temperature deviation + humidity + weather severity | match environment risk |
| `stage_premium_score` | group to final stage mapping | commercial value of tournament stage |

## Data Feature Groups

| Group | Features |
|---|---|
| Sports performance | `elo_diff`, `market_value_diff_m`, `recent_goal_diff_delta`, `team_a_strength` |
| Player influence | `a_core_player_rating`, `a_core_market_value_m`, `a_player_followers_m`, `a_player_fan_growth_30d_pct` |
| Injury and availability | `a_avg_injury_risk`, `a_avg_availability_score`, `availability_diff`, `injury_risk_diff` |
| Coach context | `coach_exp_diff`, `coach_wc_matches`, `coach_win_rate`, `coach_tenure_years` |
| Weather and venue | `temperature_c`, `humidity`, `weather_severity`, `host_advantage_a`, `stadium_capacity_k` |
| Media and social | `event_attention_m`, `media_reposts_k`, `engagement_rate`, `fan_growth_7d_pct`, `time_decay_attention` |
| Text and sentiment | `sentiment_score`, `news_sentiment_score`, `text_signal_score`, `narrative_topic` |
| Sponsor activation | `a_sponsor_spend_m`, `a_ad_exposure_m`, `a_brand_heat_index`, `a_paid_media_share`, `a_brand_fit` |
| Business outcome | `sponsor_roi`, `predicted_roi`, `roi_lift_vs_spend`, `risk_score` |
