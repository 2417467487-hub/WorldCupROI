# WorldCupROI Dataset Card

## Data Strategy

WorldCupROI is designed to accept public World Cup CSVs or API data. When stable APIs are unavailable, the project generates seeded mock datasets with realistic sports-business relationships.

## Dataset Layers

| File | Grain | Purpose |
| --- | --- | --- |
| `historical_matches.csv` | match | 1930-2022 match context and result |
| `schedule_2026.csv` | match | mock 2026 schedule |
| `players.csv` | team-player role | player rating, market value, fan followers |
| `coaches.csv` | team | coach experience and tenure |
| `sponsors.csv` | team-sponsor | sponsor spend, brand fit, activation quality |
| `weather.csv` | match | venue, weather, temperature, humidity |
| `social_media.csv` | match | attention, reposts, mentions, video views, sentiment |
| `modeling_dataset.csv` | match with joined features | match and ROI model training |
| `panel_dataset.csv` | year-match-team-sponsor | dashboard and business analysis |

## Reproducibility

- Random seed: `42`
- Data generator: `src/preprocess.py`
- Feature builder: `src/feature_builder.py`
- Panel builder: `src/build_panel_data.py`
- Quality report: `src/data_quality.py`

## Known Limitations

- Mock data is not a substitute for real FIFA, sponsor, or social platform data.
- The current version prioritizes reproducible project structure and analytics workflow.
- Real deployment should add API connectors and historical sponsorship contracts.

