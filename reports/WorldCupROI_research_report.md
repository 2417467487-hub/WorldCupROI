# WorldCupROI Research Report

## 1. Research Question

World Cup sponsorship is not only a bet on strong teams. Sponsor return depends on how sporting performance, star-player attention, media amplification, and brand activation combine into commercial conversion.

WorldCupROI frames this problem as a multi-task machine learning system:

- predict match outcomes as an upstream sporting signal
- predict sponsor ROI as the core commercial target
- convert fan and media attention into quantified behavioral indicators
- simulate sponsor strategy under counterfactual A/B scenarios

The research focus is the transformation of sports attention into measurable sponsor ROI.

## 2. Data Design

The project supports public CSV or API-based datasets. When stable public data is unavailable, reproducible synthetic data is generated with a fixed random seed.

Included data layers:

- World Cup match samples from 1930-2022
- mock 2026 schedule
- team Elo, recent form, coach experience, and squad market value
- core player rating, followers, and market value
- sponsor spend, brand fit, activation quality, and historical sports presence
- weather, stadium capacity, match stage, media reposts, and event attention

## 3. Metric System

### FanScore

FanScore captures fan attention and media propagation potential.

```text
FanScore = 0.45 * player_fans_scaled
         + 0.35 * event_attention_scaled
         + 0.20 * media_reposts_scaled
```

Interpretation:

- player followers represent baseline reach
- event attention represents contextual demand
- media reposts represent amplification

### Sponsor Power Index

Sponsor Power Index captures the ability of a brand to convert attention into ROI.

```text
SPI = 0.40 * sponsor_spend_scaled
    + 0.25 * brand_fit
    + 0.20 * activation_quality
    + 0.15 * historical_sports_presence
```

Interpretation:

- spend determines campaign scale
- brand fit determines relevance
- activation quality determines conversion efficiency
- sports presence determines credibility in the category

### Commercial Momentum

Commercial Momentum is a panel-level business signal used to rank team-sponsor opportunities.

```text
Commercial Momentum = 0.38 * FanScore
                    + 0.34 * Sponsor Power Index
                    + 0.18 * Exposure Score
                    + 0.10 * Match Points
```

## 4. Model Design

### Match Outcome Model

The match model predicts Team A win, draw, and Team B win probabilities using Elo difference, market value difference, player rating difference, coach experience, venue factors, weather, and media attention.

This module provides a sporting uncertainty signal for the ROI model.

### Sponsor ROI Model

The ROI model predicts sponsor return using FanScore, Sponsor Power Index, event attention, media reposts, player followers, team strength, sponsor spend, and activation features.

The model tests whether commercial return is explained by attention quality and sponsor execution, rather than match results alone.

## 5. Panel Data

The panel dataset has the grain:

```text
year x match_id x team x sponsor
```

This structure supports longitudinal and cross-sectional analysis of sponsor exposure opportunities.

Core variables:

- `fan_score_panel`
- `sponsor_power_index`
- `commercial_momentum`
- `predicted_roi`
- `roi_per_million_spend`
- `attention_segment`
- `commercial_segment`

The panel format makes the project suitable for dashboarding, sponsor ranking, team comparison, and scenario analysis.

## 6. Counterfactual A/B Experiment

Three scenarios are simulated:

- **Core player absent**: lower player rating, market value, followers, and FanScore.
- **Sponsor upgrade**: higher sponsor spend, brand fit, activation quality, and sponsor power.
- **Media cooling**: lower event attention, media reposts, and FanScore.

The generated results show that media cooling creates the largest average ROI decline. This indicates that sponsor performance is strongly exposed to attention decay and media amplification risk.

## 7. Key Contribution

WorldCupROI converts a sports analytics task into a commercial intelligence system.

The project contribution is threefold:

- Match prediction is treated as an input to business forecasting, not the final product.
- FanScore and Sponsor Power Index provide interpretable bridges between user attention, brand strategy, and machine learning.
- Counterfactual A/B simulation turns model outputs into sponsor decision support.

## 8. Interactive Platform

The project includes two visualization surfaces:

- a browser-ready HTML dashboard for interactive filtering and panel exploration
- a Streamlit app for exploratory data analysis and sponsor ROI comparison

The dashboard supports top-team ranking, sponsor efficiency inspection, segment analysis, and high-momentum opportunity discovery.

