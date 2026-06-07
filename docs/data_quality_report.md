# Data Quality Report

## Quality Principles

- Separate real-source analytical facts from proxy/mock commercial variables.
- Keep demo mode runnable without external APIs.
- Treat proxy labels as decision-support signals, not truth claims.

## Automated Checks

| dataset | rows | columns | missing_cells | duplicate_rows | origin_type | trust_level |
| --- | --- | --- | --- | --- | --- | --- |
| data/media_text_corpus.csv | 6249 | 15 | 12578 | 0 | real historical/text source | medium-high |
| data/raw/international_results.csv | 49437 | 9 | 144 | 0 | real historical/text source | medium-high |
| data/real_text_articles.csv | 6249 | 10 | 80 | 0 | real historical/text source | medium-high |
| data/team_player_sponsor_match_edges.csv | 6112 | 4 | 0 | 1922 | proxy/mock commercial data | medium-low |
| data/advanced_feature_outputs.csv | 964 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/attention_timeseries.csv | 10604 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/coaches.csv | 82 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/fan_score_outputs.csv | 1440 | 4 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/historical_matches.csv | 964 | 17 | 0 | 0 | real historical/text source | medium-high |
| data/modeling_dataset.csv | 964 | 87 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/panel_dataset.csv | 1928 | 30 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/players.csv | 246 | 10 | 0 | 0 | proxy/mock commercial enrichment | medium-low |
| data/relationship_network.csv | 328 | 4 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/roi_predictions.csv | 964 | 89 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/roi_uncertainty.csv | 964 | 15 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/scenario_recommendations.csv | 600 | 15 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/schedule_2026.csv | 72 | 10 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/social_media.csv | 964 | 16 | 0 | 0 | proxy/mock commercial enrichment | medium-low |
| data/sponsor_panel_summary.csv | 10 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/sponsor_roi_outputs.csv | 1440 | 6 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/sponsors.csv | 82 | 11 | 0 | 0 | proxy/mock commercial enrichment | medium-low |
| data/team_profile.csv | 82 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/team_year_panel.csv | 489 | 11 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/text_embeddings_reduced.csv | 6249 | 31 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/user_behavior_chain.csv | 1928 | 42 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/weather.csv | 964 | 10 | 0 | 0 | proxy/mock commercial enrichment | medium-low |

## Existing Pipeline Quality Summary

| dataset | rows | columns | missing_cells | duplicate_rows | key_columns |
| --- | --- | --- | --- | --- | --- |
| historical_matches.csv | 964 | 17 | 0 | 0 | match_id, year, team_a, team_b, stage, neutral_site, host_advantage_a, stadium_capacity_k |
| schedule_2026.csv | 72 | 10 | 0 | 0 | match_id, date, year, team_a, team_b, host_city, host_country, neutral |
| players.csv | 246 | 10 | 0 | 0 | team, player_role, player_rating, market_value_m, followers_m, injury_risk, availability_score, fan_growth_30d_pct |
| coaches.csv | 82 | 7 | 0 | 0 | team, coach_name, coach_wc_matches, coach_win_rate, coach_tenure_years, international_titles, data_origin |
| sponsors.csv | 82 | 11 | 0 | 0 | team, sponsor, sponsor_category, sponsor_spend_m, ad_exposure_m, brand_heat_index, paid_media_share, brand_fit |
| weather.csv | 964 | 10 | 0 | 0 | match_id, year, temperature_c, humidity, weather, stadium_capacity_k, neutral_site, host_advantage_a |
| social_media.csv | 964 | 16 | 0 | 0 | match_id, year, team_a, team_b, event_attention_m, media_reposts_k, stage, hashtag_mentions_k |
| real_text_articles.csv | 6249 | 10 | 80 | 0 | text_id, source, title, url, domain, language, sourcecountry, published_at |
| text_embeddings_reduced.csv | 6249 | 31 | 0 | 0 | text_id, source, domain, narrative_topic, sentiment_score, text_svd_01, text_svd_02, text_svd_03 |
| attention_timeseries.csv | 10604 | 7 | 0 | 0 | match_id, day_offset, team_a, team_b, attention_index, engagement_rate, sentiment_score |
| media_text_corpus.csv | 6249 | 15 | 12578 | 0 | text_id, source, sample_headline, source_url, domain, language, sourcecountry, published_at |
| relationship_network.csv | 328 | 4 | 0 | 0 | source, target, edge_type, weight |
| modeling_dataset.csv | 964 | 87 | 0 | 0 | match_id, year, team_a, team_b, stage, neutral_site, host_advantage_a, stadium_capacity_k |
| advanced_feature_outputs.csv | 964 | 7 | 0 | 0 | match_id, media_exposure_index, commercial_momentum_score, injury_risk_score, sponsor_team_fit_score, weather_impact_score, stage_premium_score |
| roi_uncertainty.csv | 720 | 15 | 0 | 0 | match_id, team_a, team_b, stage, roi_mean, roi_ci_low, roi_ci_high, bootstrap_ci_low |
| scenario_recommendations.csv | 600 | 15 | 0 | 0 | match_id, team_a, team_b, stage, scenario, strategy_type, scenario_roi, roi_lift |
| panel_dataset.csv | 1440 | 30 | 0 | 0 | panel_id, year, match_id, team, opponent, team_side, stage, sponsor |

## Highest-Risk Fields

- `sponsor_roi`: proxy label with potential circularity against sponsor features.
- `sponsor_spend_m`: proxy spend; should be replaced by campaign finance data.
- `ad_exposure_m`, `brand_heat_index`, `activation_quality`: modeled commercial assumptions.
- `predicted_roi`: model output; must not be used as a future training label.