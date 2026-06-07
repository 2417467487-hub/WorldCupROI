# Data Card

## Scope

WorldCupROI combines real historical football data, real-source text/news context, and proxy/mock commercial variables to support reproducible sponsor ROI analysis.

## Data Boundary

| Category | Examples | Current Use | Trust Level | Replacement Path |
| --- | --- | --- | --- | --- |
| Real historical data | international match results, World Cup history | Match context, labels, team history | Medium-high | Pin source snapshots, add official FIFA/provider feeds |
| Real text data | Wikipedia/GDELT style article snapshots, media text corpus | Narrative and text-signal features | Medium | Add source freshness checks, use licensed media API |
| Proxy/mock commercial data | sponsor spend, activation quality, player social proxy, conversion proxy | ROI labels, sponsor strategy, dashboard demo | Medium-low | Replace with sponsor CRM, campaign spend, social API, sales/ticketing conversion |

## Dataset Inventory

| dataset | origin_type | trust_level | shape | size_kb | future_replacement_path |
| --- | --- | --- | --- | --- | --- |
| data/advanced_feature_outputs.csv | proxy/mock commercial data | medium-low | 964 rows x 7 columns | 91.6000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/attention_timeseries.csv | proxy/mock commercial data | medium-low | 10604 rows x 7 columns | 449.4000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/coaches.csv | proxy/mock commercial data | medium-low | 82 rows x 7 columns | 6.7000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/fan_score_outputs.csv | proxy/mock commercial data | medium-low | 1440 rows x 4 columns | 56.5000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/historical_matches.csv | real historical/text source | medium-high | 964 rows x 17 columns | 112.8000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/media_text_corpus.csv | real historical/text source | medium-high | 5057 rows x 15 columns | 3110.2000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/modeling_dataset.csv | proxy/mock commercial data | medium-low | 964 rows x 87 columns | 792.0000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/panel_dataset.csv | proxy/mock commercial data | medium-low | 1928 rows x 30 columns | 381.3000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/players.csv | proxy/mock commercial enrichment | medium-low | 246 rows x 10 columns | 22.9000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/raw/gdelt_worldcup_article_batches.json | real historical/text source | medium-high |  | 121.4000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/raw/gdelt_worldcup_articles_deduped.json | real historical/text source | medium-high |  | 106.9000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/raw/gdelt_worldcup_sponsor_articles.json | real historical/text source | medium-high |  | 28.0000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/raw/international_results.csv | real historical/text source | medium-high | 49437 rows x 9 columns | 3683.1000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/raw/wikipedia_pages.json | real historical/text source | medium-high |  | 76.2000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/real_text_articles.csv | real historical/text source | medium-high | 5057 rows x 10 columns | 3026.2000 | Refresh from source APIs and pin source snapshots with data versioning. |
| data/relationship_network.csv | proxy/mock commercial data | medium-low | 328 rows x 4 columns | 16.3000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/roi_predictions.csv | proxy/mock commercial data | medium-low | 964 rows x 89 columns | 800.3000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/roi_uncertainty.csv | proxy/mock commercial data | medium-low | 964 rows x 15 columns | 95.1000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/scenario_recommendations.csv | proxy/mock commercial data | medium-low | 600 rows x 15 columns | 161.9000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/schedule_2026.csv | proxy/mock commercial data | medium-low | 72 rows x 10 columns | 5.6000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/social_media.csv | proxy/mock commercial enrichment | medium-low | 964 rows x 16 columns | 116.8000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/sponsor_panel_summary.csv | proxy/mock commercial data | medium-low | 10 rows x 7 columns | 0.5000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/sponsor_roi_outputs.csv | proxy/mock commercial data | medium-low | 1440 rows x 6 columns | 73.1000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/sponsors.csv | proxy/mock commercial enrichment | medium-low | 82 rows x 11 columns | 9.6000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/team_player_sponsor_match_edges.csv | proxy/mock commercial data | medium-low | 6112 rows x 4 columns | 305.5000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/team_profile.csv | proxy/mock commercial data | medium-low | 82 rows x 7 columns | 3.3000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/team_year_panel.csv | proxy/mock commercial data | medium-low | 489 rows x 11 columns | 31.0000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/text_embeddings_reduced.csv | proxy/mock commercial data | medium-low | 5057 rows x 31 columns | 1436.5000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/user_behavior_chain.csv | proxy/mock commercial data | medium-low | 1928 rows x 42 columns | 526.7000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |
| data/weather.csv | proxy/mock commercial enrichment | medium-low | 964 rows x 10 columns | 50.1000 | Replace with licensed sponsor CRM, sales, broadcast, or social platform data. |

## Limitations

- `sponsor_roi` is a constructed proxy label, not audited sponsor revenue.
- Sponsor spend, activation quality, and conversion fields are demo/proxy variables.
- Text signals are lightweight source-derived features; they are not a substitute for production NLP monitoring.
- Historical match outcomes are real-source oriented, but commercial activation is not historically verified.

## Future Replacement Path

1. Connect licensed sponsorship spend and media value datasets.
2. Replace proxy conversion with CRM, sales, search lift, app installs, ticketing, or merch revenue.
3. Add source versioning with DVC or a data warehouse snapshot table.
4. Add automated freshness and drift checks before model retraining.