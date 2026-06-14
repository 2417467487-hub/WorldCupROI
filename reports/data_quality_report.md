# Data Quality Report

## Quality Principles

- Separate real-source analytical facts from proxy/mock commercial variables.
- Keep demo mode runnable without external APIs.
- Treat proxy labels as decision-support signals, not truth claims.

## Automated Checks

| dataset | rows | columns | missing_cells | duplicate_rows | origin_type | trust_level |
| --- | --- | --- | --- | --- | --- | --- |
| data/media_text_corpus.csv | 4769 | 15 | 9674 | 0 | real historical/text source | medium-high |
| data/real_text_articles.csv | 4769 | 10 | 136 | 0 | real historical/text source | medium-high |
| data/raw/international_results.csv | 49477 | 9 | 128 | 0 | real historical/text source | medium-high |
| data/team_player_sponsor_match_edges.csv | 6160 | 4 | 0 | 1930 | proxy/mock commercial data | medium-low |
| data/advanced_feature_outputs.csv | 972 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/attention_timeseries.csv | 10692 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/coaches.csv | 82 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/commercial_decision_metrics.csv | 1944 | 10 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/dynamic_roi_timeseries.csv | 90 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/fan_score_outputs.csv | 1440 | 4 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/historical_matches.csv | 972 | 17 | 0 | 0 | real historical/text source | medium-high |
| data/modeling_dataset.csv | 972 | 87 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/panel_dataset.csv | 1944 | 30 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/players.csv | 246 | 10 | 0 | 0 | proxy/mock commercial enrichment | medium-low |
| data/relationship_network.csv | 328 | 4 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/roi_predictions.csv | 972 | 89 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/roi_uncertainty.csv | 972 | 15 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/scenario_recommendations.csv | 600 | 15 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/schedule_2026.csv | 72 | 10 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/social_media.csv | 972 | 16 | 0 | 0 | proxy/mock commercial enrichment | medium-low |
| data/sponsor_panel_summary.csv | 10 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/sponsor_roi_outputs.csv | 1440 | 6 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/sponsors.csv | 82 | 11 | 0 | 0 | proxy/mock commercial enrichment | medium-low |
| data/team_profile.csv | 82 | 7 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/team_year_panel.csv | 505 | 11 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/text_embeddings_reduced.csv | 4769 | 31 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/user_behavior_chain.csv | 1944 | 42 | 0 | 0 | proxy/mock commercial data | medium-low |
| data/weather.csv | 972 | 10 | 0 | 0 | proxy/mock commercial enrichment | medium-low |

## Data Trust Summary

| origin_type | trust_level | datasets | total_rows | missing_cells | duplicate_rows |
| --- | --- | --- | --- | --- | --- |
| real historical/text source | medium-high | 4 | 59987 | 9938 | 0 |
| proxy/mock commercial data | medium-low | 20 | 35990 | 0 | 1930 |
| proxy/mock commercial enrichment | medium-low | 4 | 2272 | 0 | 0 |

## Field Types and Coverage

| dataset | field | dtype | coverage_rate | missing_cells | unique_values | origin_type |
| --- | --- | --- | --- | --- | --- | --- |
| data/media_text_corpus.csv | team_a | float64 | 0.0000 | 4769 | 0 | real historical/text source |
| data/media_text_corpus.csv | team_b | float64 | 0.0000 | 4769 | 0 | real historical/text source |
| data/media_text_corpus.csv | source_url | object | 0.9857 | 68 | 110 | real historical/text source |
| data/media_text_corpus.csv | published_at | object | 0.9857 | 68 | 474 | real historical/text source |
| data/real_text_articles.csv | url | object | 0.9857 | 68 | 110 | real historical/text source |
| data/real_text_articles.csv | published_at | object | 0.9857 | 68 | 474 | real historical/text source |
| data/raw/international_results.csv | home_score | float64 | 0.9987 | 64 | 26 | real historical/text source |
| data/raw/international_results.csv | away_score | float64 | 0.9987 | 64 | 22 | real historical/text source |
| data/advanced_feature_outputs.csv | match_id | int64 | 1.0000 | 0 | 972 | proxy/mock commercial data |
| data/advanced_feature_outputs.csv | media_exposure_index | float64 | 1.0000 | 0 | 972 | proxy/mock commercial data |
| data/advanced_feature_outputs.csv | commercial_momentum_score | float64 | 1.0000 | 0 | 972 | proxy/mock commercial data |
| data/advanced_feature_outputs.csv | injury_risk_score | float64 | 1.0000 | 0 | 80 | proxy/mock commercial data |
| data/advanced_feature_outputs.csv | sponsor_team_fit_score | float64 | 1.0000 | 0 | 80 | proxy/mock commercial data |
| data/advanced_feature_outputs.csv | weather_impact_score | float64 | 1.0000 | 0 | 967 | proxy/mock commercial data |
| data/advanced_feature_outputs.csv | stage_premium_score | float64 | 1.0000 | 0 | 1 | proxy/mock commercial data |
| data/attention_timeseries.csv | match_id | int64 | 1.0000 | 0 | 972 | proxy/mock commercial data |
| data/attention_timeseries.csv | day_offset | int64 | 1.0000 | 0 | 11 | proxy/mock commercial data |
| data/attention_timeseries.csv | team_a | object | 1.0000 | 0 | 80 | proxy/mock commercial data |
| data/attention_timeseries.csv | team_b | object | 1.0000 | 0 | 79 | proxy/mock commercial data |
| data/attention_timeseries.csv | attention_index | float64 | 1.0000 | 0 | 4317 | proxy/mock commercial data |
| data/attention_timeseries.csv | engagement_rate | float64 | 1.0000 | 0 | 3204 | proxy/mock commercial data |
| data/attention_timeseries.csv | sentiment_score | float64 | 1.0000 | 0 | 695 | proxy/mock commercial data |
| data/coaches.csv | team | object | 1.0000 | 0 | 82 | proxy/mock commercial data |
| data/coaches.csv | coach_name | object | 1.0000 | 0 | 82 | proxy/mock commercial data |
| data/coaches.csv | coach_wc_matches | int64 | 1.0000 | 0 | 15 | proxy/mock commercial data |
| data/coaches.csv | coach_win_rate | float64 | 1.0000 | 0 | 53 | proxy/mock commercial data |
| data/coaches.csv | coach_tenure_years | float64 | 1.0000 | 0 | 15 | proxy/mock commercial data |
| data/coaches.csv | international_titles | int64 | 1.0000 | 0 | 2 | proxy/mock commercial data |
| data/coaches.csv | data_origin | object | 1.0000 | 0 | 1 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | panel_id | object | 1.0000 | 0 | 1944 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | team | object | 1.0000 | 0 | 82 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | sponsor | object | 1.0000 | 0 | 10 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | stage | object | 1.0000 | 0 | 2 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | predicted_roi | float64 | 1.0000 | 0 | 687 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | media_value_index | float64 | 1.0000 | 0 | 971 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | fan_conversion_rate | float64 | 1.0000 | 0 | 1850 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | social_spread_index | float64 | 1.0000 | 0 | 1932 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | brand_influence_score | float64 | 1.0000 | 0 | 82 | proxy/mock commercial data |
| data/commercial_decision_metrics.csv | commercial_decision_score | float64 | 1.0000 | 0 | 1937 | proxy/mock commercial data |
| data/dynamic_roi_timeseries.csv | cycle | int64 | 1.0000 | 0 | 23 | proxy/mock commercial data |
| data/dynamic_roi_timeseries.csv | stage | object | 1.0000 | 0 | 2 | proxy/mock commercial data |
| data/dynamic_roi_timeseries.csv | player_mix | object | 1.0000 | 0 | 4 | proxy/mock commercial data |
| data/dynamic_roi_timeseries.csv | avg_roi | float64 | 1.0000 | 0 | 90 | proxy/mock commercial data |
| data/dynamic_roi_timeseries.csv | avg_fanscore | float64 | 1.0000 | 0 | 90 | proxy/mock commercial data |
| data/dynamic_roi_timeseries.csv | avg_momentum | float64 | 1.0000 | 0 | 87 | proxy/mock commercial data |
| data/dynamic_roi_timeseries.csv | samples | int64 | 1.0000 | 0 | 41 | proxy/mock commercial data |
| data/fan_score_outputs.csv | panel_id | object | 1.0000 | 0 | 1440 | proxy/mock commercial data |
| data/fan_score_outputs.csv | team | object | 1.0000 | 0 | 24 | proxy/mock commercial data |
| data/fan_score_outputs.csv | sponsor | object | 1.0000 | 0 | 9 | proxy/mock commercial data |
| data/fan_score_outputs.csv | fan_score_module | float64 | 1.0000 | 0 | 1187 | proxy/mock commercial data |
| data/historical_matches.csv | match_id | int64 | 1.0000 | 0 | 972 | real historical/text source |
| data/historical_matches.csv | year | int64 | 1.0000 | 0 | 23 | real historical/text source |
| data/historical_matches.csv | team_a | object | 1.0000 | 0 | 80 | real historical/text source |
| data/historical_matches.csv | team_b | object | 1.0000 | 0 | 79 | real historical/text source |
| data/historical_matches.csv | stage | object | 1.0000 | 0 | 2 | real historical/text source |
| data/historical_matches.csv | neutral_site | bool | 1.0000 | 0 | 2 | real historical/text source |
| data/historical_matches.csv | host_advantage_a | float64 | 1.0000 | 0 | 2 | real historical/text source |
| data/historical_matches.csv | stadium_capacity_k | float64 | 1.0000 | 0 | 439 | real historical/text source |
| data/historical_matches.csv | temperature_c | float64 | 1.0000 | 0 | 267 | real historical/text source |
| data/historical_matches.csv | humidity | float64 | 1.0000 | 0 | 467 | real historical/text source |

## Coverage Summary

| origin_type | fields | avg_coverage | total_missing |
| --- | --- | --- | --- |
| proxy/mock commercial data | 400 | 1.0000 | 0 |
| proxy/mock commercial enrichment | 47 | 1.0000 | 0 |
| real historical/text source | 51 | 0.9596 | 9938 |

## Missing Value and Outlier Signals

| dataset | field | missing_cells | coverage_rate | iqr_outliers | risk_note |
| --- | --- | --- | --- | --- | --- |
| data/raw/international_results.csv | home_score | 64 | 0.9987 | 6338 | Monitor source quality |
| data/text_embeddings_reduced.csv | text_svd_05 | 0 | 1.0000 | 816 | Review before production modeling |
| data/raw/international_results.csv | away_score | 64 | 0.9987 | 697 | Monitor source quality |
| data/text_embeddings_reduced.csv | text_svd_03 | 0 | 1.0000 | 653 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_04 | 0 | 1.0000 | 569 | Review before production modeling |
| data/attention_timeseries.csv | attention_index | 0 | 1.0000 | 533 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_02 | 0 | 1.0000 | 522 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_y | 0 | 1.0000 | 522 | Review before production modeling |
| data/panel_dataset.csv | activation_quality | 0 | 1.0000 | 443 | Review before production modeling |
| data/user_behavior_chain.csv | activation_quality | 0 | 1.0000 | 443 | Review before production modeling |
| data/panel_dataset.csv | sponsor_power_index | 0 | 1.0000 | 369 | Review before production modeling |
| data/user_behavior_chain.csv | sponsor_power_index | 0 | 1.0000 | 369 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_13 | 0 | 1.0000 | 223 | Review before production modeling |
| data/modeling_dataset.csv | a_activation_quality | 0 | 1.0000 | 199 | Review before production modeling |
| data/modeling_dataset.csv | a_sponsor_power_index | 0 | 1.0000 | 199 | Review before production modeling |
| data/roi_predictions.csv | a_activation_quality | 0 | 1.0000 | 199 | Review before production modeling |
| data/roi_predictions.csv | a_sponsor_power_index | 0 | 1.0000 | 199 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_08 | 0 | 1.0000 | 190 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_21 | 0 | 1.0000 | 189 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_15 | 0 | 1.0000 | 176 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_06 | 0 | 1.0000 | 163 | Review before production modeling |
| data/advanced_feature_outputs.csv | sponsor_team_fit_score | 0 | 1.0000 | 159 | Review before production modeling |
| data/modeling_dataset.csv | sponsor_team_fit_score | 0 | 1.0000 | 159 | Review before production modeling |
| data/roi_predictions.csv | sponsor_team_fit_score | 0 | 1.0000 | 159 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_07 | 0 | 1.0000 | 156 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_19 | 0 | 1.0000 | 155 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_14 | 0 | 1.0000 | 138 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_11 | 0 | 1.0000 | 128 | Review before production modeling |
| data/panel_dataset.csv | sponsor_spend_m | 0 | 1.0000 | 125 | Review before production modeling |
| data/user_behavior_chain.csv | sponsor_spend_m | 0 | 1.0000 | 125 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_09 | 0 | 1.0000 | 115 | Review before production modeling |
| data/user_behavior_chain.csv | funnel_efficiency | 0 | 1.0000 | 115 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_12 | 0 | 1.0000 | 108 | Review before production modeling |
| data/team_year_panel.csv | avg_sponsor_power | 0 | 1.0000 | 107 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_20 | 0 | 1.0000 | 104 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_16 | 0 | 1.0000 | 89 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_22 | 0 | 1.0000 | 87 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_18 | 0 | 1.0000 | 84 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_17 | 0 | 1.0000 | 81 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_23 | 0 | 1.0000 | 76 | Review before production modeling |
| data/fan_score_outputs.csv | fan_score_module | 0 | 1.0000 | 61 | Review before production modeling |
| data/modeling_dataset.csv | a_sponsor_spend_m | 0 | 1.0000 | 61 | Review before production modeling |
| data/roi_predictions.csv | a_sponsor_spend_m | 0 | 1.0000 | 61 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_24 | 0 | 1.0000 | 60 | Review before production modeling |
| data/attention_timeseries.csv | sentiment_score | 0 | 1.0000 | 58 | Review before production modeling |
| data/modeling_dataset.csv | a_avg_injury_risk | 0 | 1.0000 | 55 | Review before production modeling |
| data/roi_predictions.csv | a_avg_injury_risk | 0 | 1.0000 | 55 | Review before production modeling |
| data/panel_dataset.csv | roi_per_million_spend | 0 | 1.0000 | 49 | Review before production modeling |
| data/user_behavior_chain.csv | roi_per_million_spend | 0 | 1.0000 | 49 | Review before production modeling |
| data/user_behavior_chain.csv | hashtag_mentions_k | 0 | 1.0000 | 46 | Review before production modeling |
| data/panel_dataset.csv | media_reposts_k | 0 | 1.0000 | 42 | Review before production modeling |
| data/user_behavior_chain.csv | media_reposts_k | 0 | 1.0000 | 42 | Review before production modeling |
| data/text_embeddings_reduced.csv | text_svd_10 | 0 | 1.0000 | 40 | Review before production modeling |
| data/user_behavior_chain.csv | engagement_rate | 0 | 1.0000 | 34 | Review before production modeling |
| data/user_behavior_chain.csv | social_interaction_score | 0 | 1.0000 | 32 | Review before production modeling |
| data/commercial_decision_metrics.csv | social_spread_index | 0 | 1.0000 | 30 | Review before production modeling |
| data/modeling_dataset.csv | a_player_followers_m | 0 | 1.0000 | 28 | Review before production modeling |
| data/panel_dataset.csv | fan_score_panel | 0 | 1.0000 | 28 | Review before production modeling |
| data/roi_predictions.csv | a_player_followers_m | 0 | 1.0000 | 28 | Review before production modeling |
| data/user_behavior_chain.csv | fan_score_panel | 0 | 1.0000 | 28 | Review before production modeling |

## Existing Pipeline Quality Summary

| dataset | rows | columns | missing_cells | duplicate_rows | key_columns |
| --- | --- | --- | --- | --- | --- |
| historical_matches.csv | 972 | 17 | 0 | 0 | match_id, year, team_a, team_b, stage, neutral_site, host_advantage_a, stadium_capacity_k |
| schedule_2026.csv | 72 | 10 | 0 | 0 | match_id, date, year, team_a, team_b, host_city, host_country, neutral |
| players.csv | 246 | 10 | 0 | 0 | team, player_role, player_rating, market_value_m, followers_m, injury_risk, availability_score, fan_growth_30d_pct |
| coaches.csv | 82 | 7 | 0 | 0 | team, coach_name, coach_wc_matches, coach_win_rate, coach_tenure_years, international_titles, data_origin |
| sponsors.csv | 82 | 11 | 0 | 0 | team, sponsor, sponsor_category, sponsor_spend_m, ad_exposure_m, brand_heat_index, paid_media_share, brand_fit |
| weather.csv | 972 | 10 | 0 | 0 | match_id, year, temperature_c, humidity, weather, stadium_capacity_k, neutral_site, host_advantage_a |
| social_media.csv | 972 | 16 | 0 | 0 | match_id, year, team_a, team_b, event_attention_m, media_reposts_k, stage, hashtag_mentions_k |
| real_text_articles.csv | 4769 | 10 | 136 | 0 | text_id, source, title, url, domain, language, sourcecountry, published_at |
| text_embeddings_reduced.csv | 4769 | 31 | 0 | 0 | text_id, source, domain, narrative_topic, sentiment_score, text_svd_01, text_svd_02, text_svd_03 |
| attention_timeseries.csv | 10692 | 7 | 0 | 0 | match_id, day_offset, team_a, team_b, attention_index, engagement_rate, sentiment_score |
| media_text_corpus.csv | 4769 | 15 | 9674 | 0 | text_id, source, sample_headline, source_url, domain, language, sourcecountry, published_at |
| relationship_network.csv | 328 | 4 | 0 | 0 | source, target, edge_type, weight |
| modeling_dataset.csv | 972 | 87 | 0 | 0 | match_id, year, team_a, team_b, stage, neutral_site, host_advantage_a, stadium_capacity_k |
| advanced_feature_outputs.csv | 972 | 7 | 0 | 0 | match_id, media_exposure_index, commercial_momentum_score, injury_risk_score, sponsor_team_fit_score, weather_impact_score, stage_premium_score |
| roi_uncertainty.csv | 964 | 15 | 0 | 0 | match_id, team_a, team_b, stage, roi_mean, roi_ci_low, roi_ci_high, bootstrap_ci_low |
| scenario_recommendations.csv | 600 | 15 | 0 | 0 | match_id, team_a, team_b, stage, scenario, strategy_type, scenario_roi, roi_lift |
| panel_dataset.csv | 1928 | 30 | 0 | 0 | panel_id, year, match_id, team, opponent, team_side, stage, sponsor |

## Highest-Risk Fields

- `sponsor_roi`: proxy label with potential circularity against sponsor features.
- `sponsor_spend_m`: proxy spend; should be replaced by campaign finance data.
- `ad_exposure_m`, `brand_heat_index`, `activation_quality`: modeled commercial assumptions.
- `predicted_roi`: model output; must not be used as a future training label.

## Validation and Governance Risks

- Real historical match data has higher credibility for outcome labels than sponsor conversion variables.
- Real-source text is useful for attention context, but source freshness and deduplication must be monitored.
- Proxy/mock commercial variables make the project reproducible, but production use requires licensed campaign, CRM, sales, or social data.
- Any dashboard decision should display data-origin context when proxy variables drive recommendations.