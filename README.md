# WorldCupROI

**AI Sports Sponsorship Intelligence Platform**

WorldCupROI turns the World Cup attention market into a sponsorship decision engine. It is not a simple match-result predictor: it blends match performance, media narratives, fan influence, sponsor investment, and uncertainty risk into one ROI decision platform.

[![CI](https://github.com/2417467487-hub/WorldCupROI/actions/workflows/ci.yml/badge.svg)](https://github.com/2417467487-hub/WorldCupROI/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-2457c5)
![ML](https://img.shields.io/badge/ML-ROI%20Prediction-0f8b6f)
![Explainability](https://img.shields.io/badge/Explainability-SHAP%20Style-f28c28)
![Risk](https://img.shields.io/badge/Risk-Conformal%20%2B%20Monte%20Carlo-6d5bd0)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit%20%2B%20Plotly-1167b1)

![WorldCupROI method overview](assets/images/readme_hero.png)

The opening figure is generated with Python from `scripts/generate_readme_assets.py`. It summarizes the project as a machine-learning method overview: multi-source evidence, feature construction, multi-task prediction, explainability, graph intelligence, and ROI decision support.

## Interactive Platform Preview

![WorldCupROI interactive dashboard preview](assets/gifs/dashboard_overview.gif)

The platform is not only a modeling pipeline. It includes an interactive sponsorship intelligence dashboard for KPI discovery, sponsor ROI ranking, FanScore analysis, scenario simulation, uncertainty review, and graph-based sponsor influence exploration.

| Experience | Open |
|---|---|
| Live Streamlit dashboard | `streamlit run dashboard/app.py` |
| Static dashboard preview | [dashboard/panel_dashboard.html](dashboard/panel_dashboard.html) |
| Full MP4 demo | [assets/videos/worldcuproi_demo.mp4](assets/videos/worldcuproi_demo.mp4) |
| Visual preview page | [preview_visuals.html](preview_visuals.html) |

| Dashboard area | What the interface shows |
|---|---|
| Discover | KPI cards, team/sponsor filters, ROI ranking, FanScore summary. |
| Explain | SHAP-style ROI drivers, text signals, sponsor-team fit, media exposure. |
| Predict | Match probability, predicted ROI, interval coverage, risk score. |
| Simulate | Sponsor spend, player status, media exposure, weather and stage changes. |
| Recommend | Scenario ROI lift, negative ROI probability, sponsor strategy ranking. |

| Link | Target |
|---|---|
| Live Demo | `streamlit run dashboard/app.py` |
| Static Demo | [dashboard/panel_dashboard.html](dashboard/panel_dashboard.html) |
| Demo Video | [assets/videos/worldcuproi_demo.mp4](assets/videos/worldcuproi_demo.mp4) |
| Report | [sample_report.pdf](sample_report.pdf) |
| Research Brief | [reports/sponsorship_intelligence_brief.md](reports/sponsorship_intelligence_brief.md) |

| Key result | Current value |
|---|---:|
| Match prediction accuracy | 0.5566 |
| Match prediction log loss | 0.9780 |
| Sponsor ROI model MAE | 0.1216 |
| Sponsor ROI model R2 | 0.8326 |
| Match conformal coverage | 0.9021 |
| ROI interval coverage | 0.8505 |
| Average negative ROI probability | 0.0000 |

**Chinese summary:** WorldCupROI 不是单纯预测世界杯胜负，而是把比赛表现、真实文本信号、赞助曝光、粉丝影响力与 ROI 风险整合为体育赞助商业智能平台。

## 10-Second Overview

| Capability | Output | Business value |
|---|---|---|
| Sponsor ROI prediction | Expected ROI, ROI lift, ranking | Moves beyond match prediction into commercial decision support. |
| Real-source text signals | Media heat, narrative momentum, text embeddings | Captures attention shifts that tabular sports data misses. |
| Uncertainty quantification | Prediction intervals, coverage, negative ROI probability | Makes sponsorship decisions risk-aware instead of point-estimate driven. |
| Scenario simulation | Spend, exposure, player, weather, stage changes | Tests strategy before campaign money is committed. |
| Interactive dashboard | Discover -> Explain -> Predict -> Simulate -> Recommend | Turns model outputs into a repeatable business workflow. |

## Results Showcase

Results come first because sponsorship teams need to see the business signal before reading the engineering stack. The tables are intentionally kept compact and consistent so they render cleanly on GitHub.

### Results Overview

| Area | Metric | Current value | Decision meaning |
|---|---|---:|---|
| Match prediction | Accuracy | 0.5566 | Baseline signal for team outcome probability. |
| Match prediction | Log loss | 0.9780 | Measures probability calibration quality. |
| Sponsor ROI | MAE | 0.1216 | Average ROI prediction error. |
| Sponsor ROI | R2 | 0.8326 | Share of ROI variance explained by model signals. |
| Conformal prediction | Match coverage | 0.9021 | Reliability of match prediction sets. |
| Conformal prediction | ROI coverage | 0.8505 | Reliability of ROI interval estimates. |
| Uncertainty | Negative ROI probability | 0.0000 | Current average downside probability in generated panel. |

### Model Performance Comparison

| Task | Model | Metrics | Status |
|---|---|---|---|
| Match outcome | Centroid classifier | Accuracy 0.5566, Log loss 0.9780 | Reproducible baseline |
| Sponsor ROI | Ridge regression | R2 0.8326, MAE 0.1216 | Reproducible baseline |
| Tabular modeling | XGBoost | Accuracy, Log loss, feature gain | Optional package |
| Tabular modeling | LightGBM | Accuracy, Log loss, feature gain | Optional package |
| Categorical modeling | CatBoost | Accuracy, Log loss, categorical splits | Optional package |

### ROI Feature Importance / SHAP

![ROI feature importance](docs/assets/roi_feature_importance.svg)

**What it shows:** Figure 1 ranks the strongest drivers of predicted sponsor ROI, including brand heat, team strength, sponsor spend, ad exposure, sponsor-team fit, and commercial momentum.

**Why it matters:** Sponsor value is driven by both football performance and attention dynamics, so ROI cannot be explained by match results alone.

**Business takeaway:** Brands should evaluate team strength together with media exposure, fan attention, and sponsor-team fit before increasing campaign spend.

### Sponsor ROI Ranking

| Rank | Sponsor | Influence score | Connected nodes | Average edge weight |
|---:|---|---:|---:|---:|
| 1 | Hyundai | 1261.417 | 262 | 2.3534 |
| 2 | Adidas | 1079.883 | 233 | 2.3074 |
| 3 | Coca-Cola | 1046.330 | 235 | 2.2262 |
| 4 | Visa | 1030.583 | 236 | 2.2021 |
| 5 | Hisense | 787.907 | 185 | 2.1411 |

**What it shows:** The sponsor ranking summarizes commercial network influence across team, player, sponsor, and match relationships.

**Why it matters:** Sponsors with broader and stronger network positions are more likely to convert event attention into measurable commercial value.

**Business takeaway:** Sponsorship planning should prioritize both spend level and network fit, not only brand size.

### Scenario ROI Lift

![Scenario ROI lift](docs/assets/scenario_ranking.svg)

| Scenario | Average predicted ROI | Average ROI delta | Average ROI lift |
|---|---:|---:|---:|
| A_baseline | 3.818 | 0.000 | 0.000% |
| B_core_player_absent | 3.738 | -0.080 | -2.074% |
| C_sponsor_upgrade | 3.606 | -0.213 | -5.580% |
| D_media_cooling | 3.608 | -0.210 | -5.521% |

**What it shows:** Figure 2 compares baseline ROI with counterfactual scenarios such as player absence, sponsor activation change, and media cooling.

**Why it matters:** Sponsorship ROI is sensitive to player availability and attention shocks.

**Business takeaway:** Scenario planning should be part of sponsor budget allocation before tournament exposure peaks.

### Prediction Interval / Conformal Prediction

![Prediction interval](docs/assets/roi_uncertainty_intervals.svg)

| Prediction target | Coverage rate | Average interval or set size | qhat |
|---|---:|---:|---:|
| Match prediction sets | 0.9021 | 2.3814 | 0.8110 |
| ROI prediction intervals | 0.8505 | 0.4488 | 0.2244 |

**What it shows:** Figure 3 shows prediction intervals and conformal coverage for match outcomes and ROI estimates.

**Why it matters:** Decision makers need ranges and reliability estimates, not only point predictions.

**Business takeaway:** Sponsors can use interval width and coverage as risk controls before approving higher spend.

### Monte Carlo Risk Distribution

| Risk signal | Current value | Decision use |
|---|---:|---|
| Average negative ROI probability | 0.0000 | Downside screen for sponsor scenarios. |
| Average interval width | 0.4340 | Confidence band for ROI planning. |
| Average Monte Carlo standard deviation | 0.1320 | Volatility signal under scenario perturbation. |
| Medium-risk cases | 119 | Cases needing additional review. |
| High-risk cases | 0 | Current generated panel has no high-risk cases. |

**What it shows:** The risk summary combines bootstrap intervals, Monte Carlo perturbation, and variance-based risk scoring.

**Why it matters:** ROI forecasts are more useful when the downside distribution is visible.

**Business takeaway:** Sponsors should compare expected ROI with risk score and interval width before selecting a campaign scenario.

### Text Signal Projection

![Text signal projection](docs/assets/text_embedding_map.svg)

**What it shows:** Figure 4 projects real-source text signals from GDELT and Wikimedia into reduced dimensions for modeling.

**Why it matters:** Media narratives and sponsor news can change commercial momentum before the match result is known.

**Business takeaway:** Text evidence should be treated as an early signal for sponsor attention and campaign timing.

### Sponsor-Team-Player Network

![GNN relationship explanation](docs/assets/gnn_relationship_explainer.svg)

| Network signal | Current value | Decision use |
|---|---:|---|
| Graph edges | 6112 | Relationship density across sports and sponsor entities. |
| Graph nodes | 1394 | Scale of the commercial network. |
| Top sponsor by influence | Hyundai | Current strongest sponsor-network position. |
| Top sponsor influence score | 1261.417 | Comparable influence score for ranking. |

**What it shows:** The graph layer connects sponsors, teams, players, and matches into a weighted heterogeneous network.

**Why it matters:** Sponsorship effectiveness depends on how brand exposure, team context, player influence, and match stage pass information through the relationship network.

**Business takeaway:** Network centrality and edge strength can help identify sponsors with stronger activation leverage and more resilient commercial pathways.

## Problem

Sports sponsorship is a race against a moving attention market. A brand often invests before the tournament story is fully written, while the return depends on conditions that can change within hours:

- Match importance and tournament stage.
- Team strength and player availability.
- Fan attention and media reposts.
- Sponsor spend, ad exposure, brand heat, and brand fit.
- Weather, venue, and home/away context.
- News narratives and public sentiment.

Most sports analytics projects stop at predicting who wins. WorldCupROI treats match probability as only one signal inside a broader sponsor ROI, risk, and recommendation system.

## Why It Matters

Major tournaments compress global attention into a short decision window. Sponsors need to act before all information is known, and poor timing can turn a high-profile campaign into weak commercial return.

| Audience | Value |
|---|---|
| Sports business analysts | Compare sponsors, teams, stages, and ROI risk. |
| ML and data science reviewers | Inspect reproducible modeling, feature engineering, and uncertainty outputs. |
| Researchers | Study how sports performance, media attention, sentiment, and sponsorship signals interact. |

The goal is to connect predictions to business decisions: what to sponsor, when to activate, where the upside is, and how much risk sits behind the headline ROI.

## Key Innovations

![Data flow](docs/assets/data_flow.svg)

| Innovation | Implementation |
|---|---|
| Multi-source data system | World Cup match records, GDELT article metadata, Wikimedia text, sponsor tables, and weather context. |
| Multimodal text layer | 5,450 real-source text units -> hashed TF-IDF -> 24-dimensional reduced text features. |
| Sponsorship feature store | FanScore, Sponsor Power Index, Media Exposure Index, and Commercial Momentum Score. |
| Model stack | Match outcome classification, sponsor ROI regression, scenario simulation, and model registry. |
| Explainability | SHAP-style contribution tables and ROI driver reports. |
| Uncertainty quantification | Conformal prediction, bootstrap intervals, Monte Carlo risk, negative ROI probability, and risk score. |
| Graph intelligence | Team-player-sponsor-match graph with sponsor and player commercial influence scores. |
| Product workflow | Discover -> Explain -> Predict -> Simulate -> Recommend. |

## Research Questions

1. How much do match probability, team strength, and player availability affect sponsor ROI?
2. Do sponsor spend and ad exposure matter more than fan attention and media narratives?
3. Can real-source text signals improve commercial momentum analysis?
4. Which scenarios create the strongest ROI lift under risk constraints?
5. How can uncertainty intervals make sponsor decisions more defensible?
6. What role can graph models play in team-player-sponsor-match relationships?

## Dataset & Data Sources

| Dataset | Role | Boundary |
|---|---|---|
| `data/raw/international_results.csv` | Public international match records used to derive World Cup match history. | Historical public data. |
| `data/raw/gdelt_worldcup_articles_deduped.json` | GDELT article metadata related to World Cup sponsorship and media. | Real-source text metadata. |
| `data/raw/wikipedia_pages.json` | Wikimedia page text for tournament, marketing, and sponsor context. | Real-source reference text. |
| `data/real_text_articles.csv` | 5,450 real-source text units and evidence windows. | Real-source text layer. |
| `data/text_embeddings_reduced.csv` | 24-dimensional reduced text features. | Reproducible derived features. |
| `data/modeling_dataset.csv` | Joined modeling table. | Feature-engineered analysis data. |
| `data/panel_dataset.csv` | Dashboard-ready panel data. | Dashboard and reporting layer. |
| Sponsor spend and ROI fields | Commercial sponsor inputs and ROI targets. | Proxy/mock values where contract-level data is unavailable. |

Commercial metrics such as exact sponsor spend are proxy-derived where public contract-level data is unavailable. These columns are documented so they can be replaced by licensed sponsor datasets or future API connectors.

## Architecture

```mermaid
flowchart LR
    A["Historical matches<br/>1930-2022"] --> F["Unified Feature Store"]
    B["2026 schedule<br/>stage + venue"] --> F
    C["Sponsors<br/>spend + exposure"] --> F
    D["Players + coaches<br/>ability + experience"] --> F
    E["Real-source text<br/>GDELT + Wikimedia"] --> F
    W["Weather + home/away<br/>context"] --> F

    F --> M["Match Outcome Model<br/>win/draw/loss probability"]
    F --> R["Sponsor ROI Model<br/>commercial return regression"]
    F --> G["Graph Intelligence<br/>team-player-sponsor-match network"]

    M --> C1["Conformal Prediction<br/>coverage + prediction sets"]
    R --> U["Uncertainty Engine<br/>bootstrap + Monte Carlo"]
    G --> I["Influence Scores<br/>sponsor + player centrality"]

    C1 --> S["Insight Generator"]
    U --> S
    I --> S
    S --> D1["Dashboard<br/>Discover -> Explain -> Predict -> Simulate -> Recommend"]
    S --> D2["Reports<br/>Markdown + PDF + CSV"]
```

This flow is the spine of the platform: data enters once, features are reused across models, and every prediction is routed through explanation, uncertainty, and business reporting before it reaches the dashboard.

### Algorithm Upgrade Structure

WorldCupROI now documents the algorithm system as four connected layers instead of isolated scripts. The current implementation keeps lightweight fallback models runnable, while making the production upgrade path explicit.

| Layer | Current method | Output | Upgrade path |
|---|---|---|---|
| Match Outcome Layer | CentroidOutcomeModel with deterministic split | win/draw/loss probability, feature importance, conformal set | calibrated logistic regression, LightGBM multiclass, XGBoost multi-class |
| Sponsor ROI Layer | Standardized RidgeROIModel | predicted ROI, ROI lift, ROI driver ranking, interval estimate | ElasticNet, LightGBMRegressor, XGBoostRegressor, stacked tabular ensemble |
| Risk & Recommendation Layer | bootstrap, Monte Carlo, conformal intervals | negative ROI probability, scenario ranking, lift-risk recommendation | ensemble variance, Bayesian optimization, portfolio allocation |
| Relationship Intelligence Layer | weighted heterogeneous graph centrality | sponsor influence, player/team/sponsor graph metrics | GraphSAGE, heterogeneous GNN, temporal graph model |

The structured algorithm manifest is generated at:

```text
reports/algorithm_manifest.json
reports/algorithm_strategy.md
```

Each trained fallback model now also writes a model card:

```text
reports/match_outcome_model_card.md
reports/sponsor_roi_model_card.md
```

This makes the repository easier to review as a research project: model target, feature count, metrics, artifact path, random seed, and upgrade notes are tracked as explicit artifacts.

![Architecture diagram](docs/assets/architecture.svg)

**What it shows:** Figure 5 summarizes the platform architecture from data sources to features, models, uncertainty, report generation, and dashboard delivery.

**Why it matters:** The system is designed as a reproducible analytics platform rather than a one-off notebook.

**Business takeaway:** Sponsors can trace a recommendation back to data, features, models, and risk logic.

![Model architecture](docs/assets/model_pipeline.svg)

**What it shows:** Figure 6 shows the modeling pipeline for match prediction, ROI prediction, uncertainty, and scenario analysis.

**Why it matters:** Separating match outcome modeling from sponsor ROI modeling keeps the business target clear.

**Business takeaway:** Match probability becomes one commercial input rather than the final product.

![Decision flow](docs/assets/decision_workflow.svg)

```mermaid
flowchart LR
    D["Discover<br/>select team, sponsor, stage"] --> E["Explain<br/>inspect ROI drivers"]
    E --> P["Predict<br/>match + ROI forecast"]
    P --> S["Simulate<br/>spend, exposure, player status"]
    S --> R["Recommend<br/>lift-risk tradeoff"]
```

**What it shows:** Figure 7 maps dashboard use to the business workflow Discover -> Explain -> Predict -> Simulate -> Recommend.

**Why it matters:** Each module answers a decision question instead of presenting disconnected charts.

**Business takeaway:** The dashboard supports repeated sponsor planning, not only static reporting.

## Dashboard Gallery

The dashboard is structured around a business decision sequence rather than a loose chart collection. Each screen is designed to answer one sponsor question, then hand the user to the next decision.

| Dashboard module | Main interaction | Decision value |
|---|---|---|
| Overview | KPI cards, ROI ranking, FanScore summary | Identify the strongest commercial opportunities quickly. |
| Scenario simulation | Sponsor spend, media exposure, player status controls | See ROI move as strategy assumptions change. |
| Risk analysis | Intervals, Monte Carlo distribution, negative ROI probability | Separate attractive upside from fragile forecasts. |
| Network analysis | Sponsor-team-player graph and centrality ranking | Find brands and players with stronger activation leverage. |

| Preview | GIF |
|---|---|
| Dashboard overview | ![Dashboard overview](assets/gifs/dashboard_overview.gif) |
| Scenario simulation | ![Scenario simulation](assets/gifs/scenario_simulation.gif) |
| Risk analysis | ![Risk uncertainty](assets/gifs/risk_uncertainty.gif) |
| Network analysis | ![Sponsor network graph](assets/gifs/network_graph.gif) |

### Platform Demo Video

![WorldCupROI dashboard walkthrough](assets/gifs/dashboard_overview.gif)

GitHub README pages do not always render HTML5 video controls reliably. The GIF above plays directly on the page; the full MP4 below can be opened for pause and timeline scrubbing.

[![Watch the full WorldCupROI platform demo](assets/images/video_cover.png)](assets/videos/worldcuproi_demo.mp4)

Watch the full MP4 demo: [assets/videos/worldcuproi_demo.mp4](assets/videos/worldcuproi_demo.mp4).

Generated showcase files are indexed in [docs/project_artifacts.md](docs/project_artifacts.md), including GIF previews, demo video assets, background images, and regeneration commands.

| Workflow step | Question answered | Output |
|---|---|---|
| Discover | Which teams, sponsors, stages, and years are being compared? | Filtered sponsor and match context. |
| Explain | Which features drive ROI and attention? | ROI drivers, FanScore, SHAP-style ranking. |
| Predict | What are the expected match and sponsorship outcomes? | Win/draw/loss probability and ROI estimate. |
| Simulate | How does ROI shift under sponsor, player, weather, and stage changes? | Counterfactual ROI lift and risk movement. |
| Recommend | Which scenario has the best lift-risk tradeoff? | Strategy ranking and business recommendation. |

Static dashboard:

```text
dashboard/panel_dashboard.html
```

Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/2417467487-hub/WorldCupROI.git
cd WorldCupROI
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

Direct pipeline entrypoint:

```bash
python src/pipeline.py
```

Makefile shortcuts:

```bash
make pipeline
make dashboard
make assets
```

Docker:

```bash
docker build -t worldcuproi .
docker run --rm -p 8501:8501 worldcuproi
```

Engineering reproducibility:

| Component | Role |
|---|---|
| `src/pipeline.py` | End-to-end reproducible analytics pipeline. |
| `src/algorithm_strategy.py` | Algorithm layers, feature groups, model cards, and upgrade manifest. |
| `src/platform_health.py` | Checks required data, model, report, dashboard, and media artifacts. |
| `.github/workflows/ci.yml` | GitHub Actions validation. |
| `Dockerfile` | Containerized execution. |
| `config/pipeline.yaml` | Pipeline configuration and output tracking. |

Platform health check:

```bash
python src/platform_health.py
```

or:

```bash
make health
```

Latest generated health artifacts:

```text
reports/platform_health.json
reports/platform_health.md
reports/platform_health.csv
```

## Contributions

### Academic Contribution

- Frames sponsorship ROI as a multi-signal modeling problem rather than a post-event descriptive metric.
- Combines sports analytics, media text signals, business features, uncertainty analysis, and graph intelligence.
- Provides a reproducible research scaffold for studying fan attention, sponsor exposure, and commercial return.
- Documents future extensions for GNN sponsor networks, conformal prediction, SHAP explanations, and generated business reports.

### Engineering Contribution

- Provides a one-command pipeline and modular source structure.
- Adds model registry, explainability, uncertainty, conformal prediction, graph analysis, and generated reporting modules.
- Includes Docker and GitHub Actions for reproducible execution.
- Produces dashboard-ready data, reports, visual assets, and PDF output.

### Business Contribution

- Helps compare sponsorship strategies before or during tournament windows.
- Gives executives risk-aware ROI estimates rather than only point predictions.
- Supports scenario planning for media exposure, player availability, weather, and stage premium.
- Turns sports performance and media attention into sponsor ROI decision support.

## Roadmap

| Version | Product direction | Planned capability |
|---|---|---|
| v1 | Match Prediction | Improve calibrated win/draw/loss forecasting and historical validation. |
| v2 | Sponsor ROI Modeling | Expand sponsor spend, exposure, and conversion features. |
| v3 | Graph Intelligence | Add Team-Player-Sponsor-Match graph modeling with GNN baselines. |
| v4 | Uncertainty-Aware Forecasting | Strengthen conformal coverage, bootstrap intervals, and risk dashboards. |
| v5 | LLM Sponsorship Analyst | Generate sponsor briefs, scenario explanations, and executive reports. |
| v6 | Real-Time Sports Intelligence Platform | Connect live APIs for weather, media, social attention, injuries, and campaign monitoring. |
