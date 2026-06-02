# WorldCupROI Dataset Card

## Dataset Purpose

The dataset layer supports an AI Sports Sponsorship Intelligence Platform. It is designed to study how sports performance, sponsor investment, brand exposure, fan behavior, sentiment, and media attention combine to influence sponsorship ROI.

## Current Data Strategy

The repository ships with seeded mock data for reproducibility. The mock data follows public-data-compatible schemas so each file can be replaced by real datasets or API outputs.

Random seed: `42`

## Dataset Layers

| File | Grain | Purpose |
|---|---|---|
| `historical_matches.csv` | match | 1930-2022 match context, teams, stage, weather, attention, result |
| `schedule_2026.csv` | match | mock 2026 tournament schedule |
| `players.csv` | team-player role | player rating, market value, followers, injury risk, availability, sentiment |
| `coaches.csv` | team | coach experience, tenure, win rate, titles |
| `sponsors.csv` | team-sponsor | sponsor spend, ad exposure, brand heat, category, activation quality |
| `weather.csv` | match | venue region, temperature, humidity, weather severity |
| `social_media.csv` | match | mentions, reposts, video views, engagement, fan growth, sentiment, text signal |
| `attention_timeseries.csv` | match-day | attention, engagement, and sentiment before/after match day |
| `media_text_corpus.csv` | match-text | narrative topic, sample headline, sentiment, text signal score |
| `relationship_network.csv` | edge | sponsor-team and player-team relationship graph |
| `modeling_dataset.csv` | match with joined features | model training for match outcome and sponsor ROI |
| `panel_dataset.csv` | year-match-team-sponsor | dashboard and business intelligence layer |

## Data Modalities

| Modality | Role |
|---|---|
| Tabular | structured sports, sponsor, weather, and ROI features |
| Text | narrative topic and sentiment signal for media framing |
| Time series | attention movement before and after matches |
| Network | sponsor-team-player influence relationships |

## API Readiness

The following real-data connectors can be added without changing the overall project design:

- match data: FIFA records, Kaggle World Cup datasets
- schedule data: official 2026 tournament schedule
- weather data: Open-Meteo, Meteostat, NOAA
- player data: Transfermarkt-style values, FBref, public player datasets
- injury data: team announcements, news APIs
- sponsor data: annual reports, sponsorship announcements, ad intelligence platforms
- social data: YouTube, Instagram, X/Twitter, Google Trends
- news text: NewsAPI, GDELT, sponsor press releases

## Known Limitations

- Mock sponsorship spend and ROI are simulated and should not be interpreted as real commercial performance.
- Sentiment and text signals are simplified placeholders for future NLP models.
- Relationship-network edges are synthetic and are meant to demonstrate graph-data readiness.
- Real deployment should add data validation, source licensing checks, and API refresh jobs.
