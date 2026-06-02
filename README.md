# WorldCupROI

![WorldCupROI hero](docs/assets/hero_banner.svg)

**Sports sponsorship intelligence for FIFA World Cup data: real match records, real-source text signals, ROI prediction, uncertainty analysis, and scenario-based business recommendations.**

[![Dashboard walkthrough](docs/assets/dashboard_walkthrough.gif)](dashboard/panel_dashboard.html)

WorldCupROI is a sports business analytics platform built around the FIFA World Cup. It connects match performance, fan attention, media narratives, sponsor activation, and commercial return into one reproducible decision-support workflow.

中文摘要：WorldCupROI 不是单纯的世界杯胜负预测项目，而是一个体育赞助商业智能平台。项目使用真实公开比赛数据和真实来源文本数据，结合赞助 ROI 预测、风险区间、场景模拟和交互式 Dashboard，支持赞助策略分析和商业决策展示。

## Problem

Sports sponsorship teams rarely make decisions from one clean metric. A sponsor needs to know:

- whether the match is likely to attract attention
- which team, player, or stage drives commercial momentum
- how brand heat and media exposure affect ROI
- how risky a campaign is under player, weather, or stage uncertainty
- which sponsor strategy should be prioritized

WorldCupROI treats match prediction as context. The main business target is **sponsor ROI and decision quality**.

## Background

Major tournaments create a short, intense attention market. A brand may pay for sponsorship before the event, but the return depends on conditions that move quickly: match importance, team form, player availability, media framing, social attention, and the timing of sponsor activation.

Traditional sports dashboards usually stop at match results or audience metrics. WorldCupROI connects those signals to a business question:

> Which sponsorship strategy is likely to create measurable return, and how much risk does that decision carry?

The project follows a style often seen in strong open-source analytics repositories: a clear problem statement, reproducible data pipeline, visual model explanation, benchmark results, and a dashboard that turns predictions into decisions.

## Innovation

| Area | What the project adds |
|---|---|
| Real-source data layer | Public World Cup match records, GDELT article metadata, Wikimedia text, and real match fact text |
| Text intelligence | 5,450 text units transformed with hashed TF-IDF and reduced to 24 dimensions |
| Sponsorship metrics | FanScore, Sponsor Power Index, Media Exposure Index, Commercial Momentum Score |
| Risk analytics | Monte Carlo-style ROI uncertainty, prediction intervals, negative ROI probability |
| Scenario engine | Sponsor spend, media exposure, player availability, weather, and stage simulations |
| Dashboard flow | Discover -> Explain -> Predict -> Simulate -> Recommend |

## Architecture

![Architecture](docs/assets/architecture.svg)

```text
real match data + real-source text + sponsor signals
        -> feature engineering
        -> match probability model
        -> sponsor ROI model
        -> uncertainty and scenario engines
        -> dashboard, reports, recommendations
```

## Model Visuals

![Modeling pipeline](docs/assets/model_pipeline.svg)

| Model view | Purpose |
|---|---|
| ![ROI feature importance](docs/assets/roi_feature_importance.svg) | Shows which business and sports signals drive ROI predictions |
| ![ROI uncertainty intervals](docs/assets/roi_uncertainty_intervals.svg) | Shows prediction intervals instead of only point estimates |
| ![Text embedding map](docs/assets/text_embedding_map.svg) | Shows reduced real-source text signals used for narrative and sentiment context |
| ![Scenario ranking](docs/assets/scenario_ranking.svg) | Compares sponsor strategy simulations by expected ROI lift |

## Results

| Output | Current value |
|---|---:|
| Historical World Cup matches | 964 |
| 2026 schedule rows | 72 |
| Real-source text units | 5,450 |
| Text embedding dimensions | 24 |
| Dashboard panel rows | 1,928 |
| Match model accuracy | 0.5566 |
| Match model log loss | 0.9780 |
| ROI model MAE | 0.1177 |
| ROI model R2 | 0.8687 |

Top ROI drivers include brand heat, team strength, sponsor spend, ad exposure, sponsor-team fit, commercial momentum, Elo difference, and FanScore.

## Dashboard

![Dashboard preview](docs/assets/dashboard_preview.svg)

The dashboard is organized around a business decision workflow:

| Step | Purpose |
|---|---|
| Discover | filter teams, sponsors, stages, and tournament years |
| Explain | inspect ROI, FanScore, media attention, weather, and sponsor power |
| Predict | review match probability and ROI confidence intervals |
| Simulate | change sponsor investment, media exposure, player status, weather, and stage |
| Recommend | rank scenarios and generate sponsor strategy actions |

Open the static version:

```text
dashboard/panel_dashboard.html
```

Run the Streamlit version:

```bash
streamlit run dashboard/app.py
```

## Demo Video

[![Demo video cover](docs/assets/demo_video_cover.svg)](docs/demo_video.md)

A 2-3 minute demo storyboard is available in [docs/demo_video.md](docs/demo_video.md). The file is ready to be replaced by a recorded GitHub Release, YouTube, or Loom link after screen capture.

## Data

| Dataset | Role |
|---|---|
| `data/raw/international_results.csv` | public international match records used to derive World Cup match history |
| `data/raw/gdelt_worldcup_articles_deduped.json` | real GDELT article metadata related to World Cup sponsorship and media |
| `data/raw/wikipedia_pages.json` | real Wikimedia page text for tournament, marketing, and sponsor context |
| `data/real_text_articles.csv` | 5,450 real-source text units and evidence windows |
| `data/text_embeddings_reduced.csv` | 24-dimensional reduced text features |
| `data/modeling_dataset.csv` | joined modeling table |
| `data/panel_dataset.csv` | dashboard-ready panel data |

Commercial metrics such as exact sponsor spend are proxy-derived where public contract-level data is unavailable. These columns are marked and documented so they can be replaced by licensed commercial datasets.

## Modeling

| Module | File |
|---|---|
| Real data ingestion | `src/real_data_ingestion.py` |
| Text dimensionality reduction | `src/text_dimensionality.py` |
| Feature engineering | `src/feature_builder.py` |
| Advanced business indices | `src/advanced_features.py` |
| Match outcome model | `src/train_match_model.py` |
| Sponsor ROI model | `src/train_roi_model.py` |
| ROI uncertainty | `src/uncertainty.py` |
| Scenario recommendations | `src/scenario_engine.py` |
| Dashboard builder | `src/build_plotly_dashboard.py` |

Key documentation:

- [Machine learning framework](docs/ml_framework.md)
- [Dataset card](docs/dataset_card.md)
- [Data system](docs/data_system.md)
- [Feature dictionary](docs/feature_dictionary.md)
- [Model registry](docs/model_registry.md)
- [Research agenda](docs/research_agenda.md)

## Project Structure

```text
WorldCupROI/
|-- data/
|   |-- raw/
|   |-- historical_matches.csv
|   |-- schedule_2026.csv
|   |-- real_text_articles.csv
|   |-- text_embeddings_reduced.csv
|   |-- modeling_dataset.csv
|   `-- panel_dataset.csv
|-- dashboard/
|   |-- app.py
|   `-- panel_dashboard.html
|-- docs/
|   |-- assets/
|   |-- dataset_card.md
|   |-- data_system.md
|   |-- feature_dictionary.md
|   |-- ml_framework.md
|   |-- model_registry.md
|   `-- research_agenda.md
|-- notebooks/
|   |-- 01_eda.ipynb
|   |-- 02_model_training.ipynb
|   |-- 03_ab_experiment.ipynb
|   |-- 04_sponsor_roi_simulation.ipynb
|   `-- 05_feature_engineering.ipynb
|-- reports/
|-- src/
|-- config/
|-- sql/
|-- java/
|-- Dockerfile
|-- requirements.txt
`-- README.md
```

## Quick Start

```bash
git clone https://github.com/2417467487-hub/WorldCupROI.git
cd WorldCupROI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the full workflow:

```bash
python src/real_data_ingestion.py
python src/text_dimensionality.py
python src/feature_builder.py
python src/advanced_features.py
python src/data_quality.py
python src/train_match_model.py
python src/train_roi_model.py
python src/uncertainty.py
python src/scenario_engine.py
python src/build_panel_data.py
python src/build_plotly_dashboard.py
```

## Contributions

- Connects sports analytics with sponsorship intelligence and business intelligence.
- Uses real-source public data instead of relying only on generated examples.
- Converts large text evidence into compact, dashboard-ready features.
- Adds ROI uncertainty and scenario ranking for decision support.
- Keeps the workflow reproducible with scripts, reports, Docker, CI, SQL schema, and configuration.

## Roadmap

- Replace proxy sponsor spend with licensed sponsorship contract data.
- Add Open-Meteo or Meteostat connectors for venue-level weather.
- Add SHAP visual explanations directly to the dashboard.
- Add graph analytics for sponsor-team-player relationships.
- Add recorded demo video to GitHub Releases.
- Add downloadable executive report export from the dashboard.
