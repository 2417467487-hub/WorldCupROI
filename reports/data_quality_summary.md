# Data Quality Summary

WorldCupROI uses seeded mock data when public APIs are unavailable. This report checks the multi-source data system across tabular, text, time-series, and relationship-network files.

| dataset | rows | columns | missing_cells | duplicate_rows |
| --- | ---: | ---: | ---: | ---: |
| historical_matches.csv | 972 | 17 | 0 | 0 |
| schedule_2026.csv | 72 | 10 | 0 | 0 |
| players.csv | 246 | 10 | 0 | 0 |
| coaches.csv | 82 | 7 | 0 | 0 |
| sponsors.csv | 82 | 11 | 0 | 0 |
| weather.csv | 972 | 10 | 0 | 0 |
| social_media.csv | 972 | 16 | 0 | 0 |
| real_text_articles.csv | 4769 | 10 | 136 | 0 |
| text_embeddings_reduced.csv | 4769 | 31 | 0 | 0 |
| attention_timeseries.csv | 10692 | 7 | 0 | 0 |
| media_text_corpus.csv | 4769 | 15 | 9674 | 0 |
| relationship_network.csv | 328 | 4 | 0 | 0 |
| modeling_dataset.csv | 972 | 87 | 0 | 0 |
| advanced_feature_outputs.csv | 972 | 7 | 0 | 0 |
| roi_uncertainty.csv | 964 | 15 | 0 | 0 |
| scenario_recommendations.csv | 600 | 15 | 0 | 0 |
| panel_dataset.csv | 1928 | 30 | 0 | 0 |