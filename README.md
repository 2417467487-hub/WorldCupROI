# WorldCupROI

**AI Sports Sponsorship Intelligence Platform**

WorldCupROI blends match performance, media attention, fan behavior, sponsor investment, scenario simulation, and uncertainty risk into one sponsor ROI decision platform. The goal is not only to predict football results, but to help answer: **which sponsorship strategy should a brand choose, under what risk, and why?**

[![CI](https://github.com/2417467487-hub/WorldCupROI/actions/workflows/ci.yml/badge.svg)](https://github.com/2417467487-hub/WorldCupROI/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-2457c5)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit%20%2B%20Plotly-0f8b6f)
![Explainability](https://img.shields.io/badge/Explainability-SHAP%20Style-f28c28)
![Risk](https://img.shields.io/badge/Risk-Conformal%20%2B%20Monte%20Carlo-7B61FF)
![Graph](https://img.shields.io/badge/Graph-NetworkX-D55E00)
![Docker](https://img.shields.io/badge/Deploy-Docker%20%2B%20Actions-111827)

| Link | Target |
|---|---|
| Live Demo | `make dashboard` |
| Static Dashboard | [dashboard/panel_dashboard.html](dashboard/panel_dashboard.html) |
| Executive Summary | [reports/executive_summary.pdf](reports/executive_summary.pdf) |
| Business Report | [reports/business_insights.md](reports/business_insights.md) |
| Data Card | [reports/data_card.md](reports/data_card.md) |
| Model Card | [reports/model_card.md](reports/model_card.md) |
| Deployment Guide | [docs/deployment.md](docs/deployment.md) |

![WorldCupROI static dashboard preview](assets/gifs/static_platform_dashboard.gif?v=20260608-static-platform)

**Core result snapshot**

| Area | Current value |
|---|---:|
| Platform health score | 100 / 100 |
| Match accuracy | 0.5566 |
| Match log loss | 0.9780 |
| Sponsor ROI MAE | 0.1183 |
| Sponsor ROI R2 | 0.8595 |
| Match conformal coverage | 0.9021 |
| ROI interval coverage | 0.8814 |
| Average Monte Carlo std | 0.1320 |

## 10-Second Overview

WorldCupROI is a reproducible sports sponsorship analytics project with four layers:

| Layer | What it does | Business value |
|---|---|---|
| Data intelligence | Separates real historical data, real text data, and proxy/mock commercial data | Makes data boundaries visible before decisions |
| ML modeling | Trains match outcome and sponsor ROI models with validation outputs | Converts sports and attention signals into measurable ROI forecasts |
| Risk and explainability | Adds SHAP-style drivers, conformal intervals, Monte Carlo risk, and scenario lift | Turns point estimates into defensible decisions |
| Product dashboard | Discover -> Explain -> Predict -> Simulate -> Recommend | Makes the work usable by analysts and business reviewers |

## Results Showcase

### Model Performance Comparison

![Model Performance Comparison](assets/figures/model_performance_comparison.png)

**What it shows:** Compares trained baseline and benchmark models on primary evaluation metrics.

**Why it matters:** It shows whether the current model choice is a stable baseline or only a placeholder.

**Business takeaway:** Use the benchmark spread to decide which model family deserves production tuning first.

| Task | Model | Metric | Value |
|---|---|---|---:|
| Match outcome | Centroid classifier | Accuracy | 0.5566 |
| Match outcome | Centroid classifier | Log loss | 0.9780 |
| Sponsor ROI | Ridge regression | MAE | 0.1183 |
| Sponsor ROI | Ridge regression | R2 | 0.8595 |

### ROI Feature Importance / SHAP

![ROI Feature Importance / SHAP](assets/figures/roi_feature_importance_shap.png)

**What it shows:** Ranks the strongest sponsor ROI drivers using SHAP-style feature contribution scores.

**Why it matters:** Explainability keeps ROI recommendations auditable and helps detect proxy-label overdependence.

**Business takeaway:** Improve brand heat, sponsor-team fit, media exposure, and activation quality before scaling spend.

### Sponsor ROI Ranking

![Sponsor ROI Ranking](assets/figures/sponsor_roi_ranking.png)

**What it shows:** Ranks sponsors by predicted commercial ROI and network influence evidence.

**Why it matters:** A sponsor can look attractive because expected ROI is high or because relationship influence is broad.

**Business takeaway:** Prioritize sponsors that combine high ROI with strong team-player-network leverage.

### Scenario ROI Lift

![Scenario ROI Lift](assets/figures/scenario_roi_lift.png)

**What it shows:** Shows conservative, balanced, and aggressive strategy lift against the baseline.

**Why it matters:** Scenario analysis turns the model from prediction into a decision simulator.

**Business takeaway:** Select aggressive strategies only when lift is positive and risk remains tolerable.

### Prediction Interval / Conformal Prediction

![Prediction Interval / Conformal Prediction](assets/figures/prediction_interval_conformal.png)

**What it shows:** Displays ROI point estimates with conformal-style prediction intervals.

**Why it matters:** Prediction intervals show forecast reliability, not just expected value.

**Business takeaway:** Prefer narrow-interval opportunities when sponsor budgets are constrained.

### Monte Carlo Risk Distribution

![Monte Carlo Risk Distribution](assets/figures/monte_carlo_risk_distribution.png)

**What it shows:** Shows the distribution of Monte Carlo ROI standard deviation and risk scores.

**Why it matters:** The spread of risk is often more important than average ROI for sponsorship planning.

**Business takeaway:** Use high-risk tails as triggers for staged spend, insurance clauses, or additional analyst review.

### Sponsor-Team-Player Network

![Sponsor-Team-Player Network](assets/figures/sponsor_team_player_network.png)

**What it shows:** Visualizes sponsor, team, and player relationships as a weighted commercial graph.

**Why it matters:** Graph position captures activation leverage that flat tables miss.

**Business takeaway:** Use central sponsors and teams as anchor partnerships for campaign portfolios.

## Problem

Most football analytics projects stop at predicting who wins. Sponsorship decisions need more: media exposure, fan attention, brand fit, player availability, commercial momentum, downside risk, and an explanation a non-technical stakeholder can trust.

WorldCupROI frames the World Cup as an attention market where sponsor ROI depends on both match context and business activation.

## Why It Matters

Tournament sponsorship budgets are committed before all outcomes are known. A high-profile campaign can underperform if the model ignores uncertainty, audience behavior, or sponsor-team fit.

| Audience | Value |
|---|---|
| Sports business analysts | Compare ROI, risk, sponsor fit, and scenario lift |
| ML reviewers | Inspect model cards, validation, feature importance, and leakage risks |
| Researchers | Study links between match performance, text signals, user attention, and ROI |
| Product reviewers | Open a dashboard and reproduce the analysis end to end |

## Key Innovations

| Innovation | Implementation |
|---|---|
| Data boundary documentation | `reports/data_card.md`, `reports/data_quality_report.md` |
| Generalization checks | Five-fold CV plus holdout metrics in `reports/cross_validation_summary.csv` |
| User research chain | Media exposure -> user attention -> social interaction -> sponsor conversion |
| Explainable ROI modeling | SHAP-style feature contributions and grouped driver reports |
| Risk-aware decisions | Conformal intervals, bootstrap intervals, Monte Carlo risk, scenario ranking |
| Graph intelligence | NetworkX centrality, sponsor influence, player influence, GCN/GraphSAGE roadmap |
| Productized workflow | Dashboard pages: Discover -> Explain -> Predict -> Simulate -> Recommend |

## Research Questions

1. How much do match strength, player availability, and tournament stage change sponsor ROI?
2. Do media narratives and fan behavior improve ROI analysis beyond match results?
3. Which sponsor features create the strongest ROI lift under uncertainty?
4. How stable are ROI predictions under cross-validation and subsample checks?
5. Can graph centrality reveal sponsor-team-player influence patterns?
6. How can a dashboard convert model output into a business recommendation?

## Dataset & Data Sources

| Data category | Examples | Trust level | Boundary |
|---|---|---|---|
| Real historical data | International match records, World Cup history | Medium-high | Public historical sports facts |
| Real text data | GDELT/Wikimedia style article metadata and text windows | Medium | Real-source text, lightweight NLP features |
| Proxy/mock commercial data | Sponsor spend, ad exposure, activation quality, conversion proxy | Medium-low | Reproducible demo data, not audited revenue |
| Derived model outputs | Predicted ROI, risk score, scenario lift | Model-dependent | Decision support only |

Detailed documentation:

```text
reports/data_card.md
reports/data_quality_report.md
docs/data_card.md
```

## Model Performance

Cross-validation is generated by `src/model_validation.py` and saved to `reports/cross_validation_summary.csv`.

| Task | Model | Metric | Folds | Mean | Std | Min | Max |
|---|---|---|---:|---:|---:|---:|---:|
| match_outcome | CentroidOutcomeModel | accuracy | 5 | 0.5436 | 0.0389 | 0.5026 | 0.6010 |
| match_outcome | CentroidOutcomeModel | log_loss | 5 | 0.9861 | 0.0231 | 0.9584 | 1.0150 |
| sponsor_roi | RidgeROIModel | mae | 5 | 0.1162 | 0.0069 | 0.1070 | 0.1245 |
| sponsor_roi | RidgeROIModel | r2 | 5 | 0.8540 | 0.0226 | 0.8218 | 0.8837 |
| sponsor_roi | RidgeROIModel | rmse | 5 | 0.1425 | 0.0073 | 0.1315 | 0.1492 |

Model governance:

```text
reports/model_card.md
reports/match_outcome_model_card.md
reports/sponsor_roi_model_card.md
```

## Explainability & SHAP

Explainability artifacts:

```text
reports/roi_feature_importance.csv
reports/roi_driver_explanations.csv
reports/explainability_report.md
assets/figures/roi_feature_importance_shap.png
```

The ROI explanation layer is designed for business review: it connects model output to sponsor spend, brand heat, media exposure, FanScore, stage premium, player influence, and sponsor-team fit.

## Uncertainty & Conformal Prediction

| Reliability layer | Output | Current value |
|---|---|---:|
| Match conformal prediction | Coverage rate | 0.9021 |
| Match conformal prediction | Average set size | 2.3814 |
| ROI conformal prediction | Coverage rate | 0.8814 |
| ROI conformal prediction | Average interval width | 0.4771 |
| Monte Carlo risk | Average std | 0.1320 |
| Monte Carlo risk | Medium-risk cases | 119 |

Risk artifacts:

```text
data/roi_uncertainty.csv
reports/conformal_prediction_report.md
reports/uncertainty_summary.md
assets/figures/monte_carlo_risk_distribution.png
assets/figures/prediction_interval_conformal.png
```

## Scenario Simulation

WorldCupROI supports conservative, balanced, and aggressive sponsor strategies. Each scenario includes ROI, lift, risk score, confidence interval, recommendation reason, and rank.

| Strategy | Intended use |
|---|---|
| Conservative | Reduce downside when uncertainty is high |
| Balanced | Default planning mode for stable sponsor activation |
| Aggressive | Capture high-attention stages when upside justifies risk |

Generated artifacts:

```text
data/scenario_recommendations.csv
reports/scenario_ranking.md
reports/scenario_strategy_summary.csv
assets/figures/scenario_roi_lift.png
```

## Graph Intelligence

The graph layer upgrades a flat sponsor table into a heterogeneous team-player-sponsor-match network.

| Graph output | File |
|---|---|
| Node centrality | `reports/graph_node_centrality.csv` |
| Sponsor influence | `reports/sponsor_influence_scores.csv` |
| Graph report | `reports/graph_analysis_report.md` |
| Network figure | `assets/figures/sponsor_team_player_network.png` |

Production roadmap includes GCN/GraphSAGE baselines, temporal graph features, and relationship decay by tournament stage.

## Architecture

![Architecture](assets/figures/architecture.svg)

**What it shows:** The full platform architecture from data sources to features, models, risk controls, reports, and dashboard delivery.

**Why it matters:** Reviewers can understand how data, modeling, uncertainty, graph intelligence, and product outputs connect.

**Business takeaway:** Sponsors can trace a recommendation back to evidence rather than treating the dashboard as a black box.

![Model Pipeline](assets/figures/model_pipeline.svg)

**What it shows:** The modeling pipeline for match prediction, ROI prediction, explanation, conformal intervals, and scenario outputs.

**Why it matters:** Separating match outcome modeling from sponsor ROI modeling keeps the business target clear.

**Business takeaway:** Match probability becomes one commercial input, not the final product.

## Dashboard Gallery

The Streamlit app is structured as five decision pages:

```text
Discover -> Explain -> Predict -> Simulate -> Recommend
```

| Page | Purpose | Interactive/exportable outputs |
|---|---|---|
| Discover | Select team, sponsor, stage, and year context | KPI export |
| Explain | Inspect ROI, sponsor ranking, and attention map | Chart hover and filtered tables |
| Predict | Review FanScore and prediction intervals | Risk CSV / PDF / Markdown |
| Simulate | Compare weather, venue, and stage effects | Scenario charts |
| Recommend | Compare conservative/balanced/aggressive strategies and inspect sponsor network influence | Scenario and Network CSV / PDF / Markdown |

![Dashboard Gallery](assets/figures/dashboard_gallery.svg)

**What it shows:** The dashboard pages as a decision workflow, not a loose chart wall.

**Why it matters:** Each page answers one business question and passes the user to the next step.

**Business takeaway:** Analysts can move from evidence to recommendation without leaving the platform.

Additional GIF previews:

| Preview | GIF |
|---|---|
| Static dashboard overview | ![Static dashboard overview](assets/gifs/static_platform_dashboard.gif?v=20260608-static-platform) |
| Scenario simulation | ![Scenario simulation](assets/gifs/scenario_simulation.gif?v=20260608-static-platform) |
| Risk analysis | ![Risk uncertainty](assets/gifs/risk_uncertainty.gif?v=20260608-static-platform) |
| Network analysis | ![Sponsor network graph](assets/gifs/network_graph.gif?v=20260608-static-platform) |

## Demo Video

The repository includes generated demo media:

```text
assets/videos/worldcuproi_demo.mp4
assets/gifs/static_platform_dashboard.gif
assets/gifs/scenario_simulation.gif
assets/gifs/risk_uncertainty.gif
assets/gifs/network_graph.gif
```

The main README GIF is captured from the polished static HTML dashboard, so the GitHub preview works without a server while still reflecting the five-page World Cup styled decision workflow.

## Installation & Reproducibility

### Windows PowerShell

```powershell
git clone https://github.com/2417467487-hub/WorldCupROI.git
cd WorldCupROI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/pipeline.py --demo
streamlit run dashboard/app.py -- --demo
```

### macOS

```bash
git clone https://github.com/2417467487-hub/WorldCupROI.git
cd WorldCupROI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py --demo
streamlit run dashboard/app.py -- --demo
```

### Linux

```bash
git clone https://github.com/2417467487-hub/WorldCupROI.git
cd WorldCupROI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py --demo
streamlit run dashboard/app.py -- --demo
```

### Make Shortcuts

```bash
make pipeline
make dashboard
make assets
make demo
```

### Docker

```bash
docker build -t worldcuproi .
docker run --rm -p 8501:8501 worldcuproi
```

### CI/CD

```text
.github/workflows/ci.yml
.github/workflows/streamlit-cloud.yml
docs/deployment.md
```

The Streamlit Cloud workflow runs the demo pipeline, smoke-tests the Streamlit app, and optionally calls `STREAMLIT_DEPLOY_HOOK_URL` when configured.

## Contributions

| Contribution type | What this project contributes |
|---|---|
| Academic | Data card, model card, validation reports, uncertainty quantification, graph intelligence roadmap |
| Engineering | Reproducible pipeline, Makefile, Dockerfile, CI/CD, dashboard, generated assets |
| Business | Sponsor ROI ranking, strategy templates, risk-aware recommendations, user research funnel |

## Roadmap

| Phase | Product goal |
|---|---|
| v1 Portfolio platform | Stable demo mode, generated reports, dashboard, README showcase |
| v2 Data upgrade | Replace proxy commercial data with licensed sponsor CRM, broadcast, social, and sales data |
| v3 Model upgrade | Calibrated boosted models, uplift modeling, temporal validation, drift monitoring |
| v4 Graph AI | GraphSAGE/GCN baseline, temporal graph influence, sponsor portfolio optimization |
| v5 Deployment | Hosted Streamlit Cloud demo, GitHub Pages static site, automated release artifacts |

## License / Contact

This repository is a portfolio and research demonstration project. Commercial sponsor variables are documented as proxy/mock where audited campaign data is unavailable.

Repository: [github.com/2417467487-hub/WorldCupROI](https://github.com/2417467487-hub/WorldCupROI)
