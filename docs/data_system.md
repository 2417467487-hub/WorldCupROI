# Multi-Source and Multi-Modal Data System

WorldCupROI is structured as a multi-source sports business intelligence platform. The current data is reproducible mock data, but each table is shaped so it can be replaced by public datasets or API feeds.

## Data Modalities

| Modality | Files | Signals | Use |
|---|---|---|---|
| Tabular sports data | `historical_matches.csv`, `players.csv`, `coaches.csv`, `weather.csv` | team, player, coach, injury, venue, weather, stage | match context and sports performance modeling |
| Commercial data | `sponsors.csv`, `sponsor_roi_outputs.csv`, `panel_dataset.csv` | spend, ad exposure, brand heat, paid media, activation quality | Sponsor Power Index and ROI prediction |
| Social engagement data | `social_media.csv` | mentions, reposts, video views, engagement, fan growth | FanScore and attention modeling |
| Text data | `media_text_corpus.csv` | narrative topic, sample headline, sentiment, text signal | media narrative and brand conversation modeling |
| Time-series data | `attention_timeseries.csv` | day-by-day attention, engagement, sentiment | campaign momentum and attention decay |
| Relationship-network data | `relationship_network.csv` | sponsor-team and player-team edges | influence graph and sponsor ecosystem analysis |

## Target Real-Data Connectors

| Domain | Potential Source |
|---|---|
| Match records | FIFA public records, Kaggle World Cup data |
| Schedule | official tournament schedule feeds |
| Player value | Transfermarkt-style data, FBref, public player datasets |
| Injuries | public injury reports, team announcements, news APIs |
| Weather | Open-Meteo, Meteostat, NOAA |
| Sponsor data | annual reports, sponsorship announcements, ad intelligence vendors |
| Social media | YouTube, Instagram, X/Twitter, Google Trends |
| News text | GDELT, NewsAPI, sponsor press releases |

## Unified Modeling Grain

The platform can work at several grains:

- `match`: match-level prediction and weather impact.
- `team-match`: team-specific fan and performance signals.
- `team-sponsor`: sponsor relationship and brand fit.
- `day-match`: time-series attention before and after a match.
- `node-edge`: sponsor, team, and player relationship network.

## Why This Matters

Sponsor ROI is not explained by one data type. Strong business analysis requires combining:

- what happened on the field
- who created attention
- how the brand activated
- how media narratives changed
- how fans reacted over time
- which sponsor/team/player relationships created influence

This design makes the project deeper than a standard match prediction dashboard.
