# Data Quality Summary

WorldCupROI uses seeded mock data when public APIs are unavailable. This report checks the multi-source data system across tabular, text, time-series, and relationship-network files.

| dataset | rows | columns | missing_cells | duplicate_rows |
| --- | ---: | ---: | ---: | ---: |
| historical_matches.csv | 964 | 17 | 0 | 0 |
| schedule_2026.csv | 72 | 10 | 0 | 0 |
| players.csv | 246 | 10 | 0 | 0 |
| coaches.csv | 82 | 7 | 0 | 0 |
| sponsors.csv | 82 | 11 | 0 | 0 |
| weather.csv | 964 | 10 | 0 | 0 |
| social_media.csv | 964 | 16 | 0 | 0 |
| real_text_articles.csv | 5450 | 10 | 164 | 0 |
| text_embeddings_reduced.csv | 5450 | 31 | 0 | 0 |
| attention_timeseries.csv | 10604 | 7 | 0 | 0 |
| media_text_corpus.csv | 5450 | 15 | 11064 | 0 |
| relationship_network.csv | 328 | 4 | 0 | 0 |
| modeling_dataset.csv | 964 | 87 | 0 | 0 |
| advanced_feature_outputs.csv | 964 | 7 | 0 | 0 |
| roi_uncertainty.csv | 964 | 11 | 0 | 0 |
| scenario_recommendations.csv | 600 | 10 | 0 | 0 |
| panel_dataset.csv | 1928 | 30 | 0 | 0 |