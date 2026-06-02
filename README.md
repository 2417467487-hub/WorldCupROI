# WorldCupROI

## AI Sports Sponsorship Intelligence Platform

**An AI-powered sports business intelligence platform for sponsorship ROI prediction, fan attention modeling, commercial decision support, and research-grade sports analytics.**

WorldCupROI has been upgraded from a World Cup match analytics project into an **AI Sports Sponsorship Intelligence Platform**. The platform uses FIFA World Cup data as a focused research environment, but the core idea is broader: connect sports performance, fan behavior, media exposure, brand activation, and sponsor investment into one decision-support system.

项目定位：WorldCupROI 不再只是世界杯比赛预测项目，而是一个面向体育商业分析、赞助 ROI 预测、赞助策略模拟和商业决策支持的 AI 平台。

## Platform Vision

Sports sponsorship decisions are often made with fragmented evidence: match performance, star-player influence, advertising exposure, fan engagement, media narratives, and brand popularity are evaluated separately. WorldCupROI combines these signals into a single intelligence workflow:

1. **Sports Analytics**: team strength, player value, coach experience, injuries, weather, venue, and match stage.
2. **Sponsorship Intelligence**: sponsor spend, ad exposure, brand heat, activation quality, media reposts, and brand-team fit.
3. **Business Intelligence**: ROI prediction, KPI tracking, counterfactual simulation, dashboard reporting, and strategy comparison.

```text
Sports Performance Signals
        +
Fan / Media / Text / Time-Series Signals
        +
Sponsor Investment and Brand Signals
        |
        v
AI Sports Sponsorship Intelligence Platform
        |
        v
ROI Prediction + A/B Simulation + Business Decision Dashboard
```

## Research Questions

WorldCupROI is designed around research questions instead of only model accuracy:

- How do match outcome probability, team strength, and player availability influence sponsor ROI?
- Which commercial signals matter more for ROI: sponsor spend, brand heat, ad exposure, or fan attention?
- How does fan sentiment convert into measurable sponsorship value during high-attention tournament stages?
- Can social media growth and media reposts explain ROI lift beyond team performance?
- What happens to expected ROI if a core player is unavailable, a sponsor increases investment, or media exposure changes?
- How can sports organizations use multi-source data to support sponsorship pricing, activation planning, and post-event evaluation?

## Contributions

- **Business-first ML framing**: match prediction is used as an upstream signal for commercial ROI, not the final objective.
- **Unified sports sponsorship framework**: combines sports analytics, sponsorship intelligence, and business intelligence.
- **Multi-source data design**: tabular, text, time-series, and relationship-network data are represented in the project structure.
- **Decision-oriented dashboard**: sponsor investment, player availability, FanScore, weather, and ROI outputs are interactive.
- **Counterfactual experimentation**: A/B simulation estimates ROI changes under sponsor and player scenarios.
- **Reproducibility with API readiness**: seeded mock datasets keep the project runnable while preserving paths for real API integration.

## Project Structure

```text
WorldCupROI/
|-- data/
|   |-- raw/
|   |   |-- international_results.csv
|   |   |-- gdelt_worldcup_article_batches.json
|   |   |-- gdelt_worldcup_articles_deduped.json
|   |   `-- wikipedia_pages.json
|   |-- historical_matches.csv
|   |-- schedule_2026.csv
|   |-- players.csv
|   |-- coaches.csv
|   |-- sponsors.csv
|   |-- weather.csv
|   |-- social_media.csv
|   |-- attention_timeseries.csv
|   |-- media_text_corpus.csv
|   |-- real_text_articles.csv
|   |-- text_embeddings_reduced.csv
|   |-- relationship_network.csv
|   |-- modeling_dataset.csv
|   `-- panel_dataset.csv
|-- notebooks/
|   |-- 01_EDA.ipynb
|   |-- 02_Model_Training.ipynb
|   |-- 03_AB_Experiment.ipynb
|   |-- 04_Sponsor_ROI_Simulation.ipynb
|   `-- 05_Feature_Engineering.ipynb
|-- src/
|   |-- preprocess.py
|   |-- feature_builder.py
|   |-- ml_config.py
|   |-- train_match_model.py
|   |-- train_roi_model.py
|   |-- ab_simulation.py
|   |-- fan_score.py
|   |-- sponsor_roi.py
|   |-- data_quality.py
|   |-- real_data_ingestion.py
|   |-- text_dimensionality.py
|   |-- build_plotly_dashboard.py
|   `-- report_generator.py
|-- dashboard/
|   |-- app.py
|   `-- panel_dashboard.html
|-- docs/
|   |-- ML_FRAMEWORK.md
|   |-- DATASET_CARD.md
|   |-- MULTIMODAL_DATA_SYSTEM.md
|   |-- RESEARCH_AGENDA.md
|   |-- FEATURE_DICTIONARY.md
|   |-- MODEL_ZOO.md
|   `-- data_dictionary.csv
|-- config/
|   `-- pipeline.yaml
|-- sql/
|   `-- schema.sql
|-- java/
|   `-- SponsorRiskRules.java
|-- .github/workflows/
|   `-- ci.yml
|-- Dockerfile
|-- reports/
|-- models/
|-- README.md
|-- requirements.txt
`-- sample_report.pdf
```

## Unified Intelligence Framework

| Layer | Business Role | Example Signals | Output |
|---|---|---|---|
| Sports Analytics | Understand competitive context | Elo, player value, coach experience, injury risk, weather, stage | Match probability and performance context |
| Fan Intelligence | Measure attention and influence | followers, fan growth, engagement rate, sentiment, reposts | FanScore and attention lift |
| Sponsorship Intelligence | Measure brand activation strength | sponsor spend, ad exposure, brand heat, paid media share, brand fit | Sponsor Power Index |
| Business Intelligence | Support decisions | ROI prediction, scenario comparison, KPI movement | dashboard, report, sponsor recommendations |

## Multi-Source and Multi-Modal Data System

The platform is structured to support four data modalities:

| Data Type | Files | Analytical Value |
|---|---|---|
| Tabular sports data | `historical_matches.csv`, `players.csv`, `coaches.csv`, `weather.csv` | team strength, player quality, coach context, match conditions |
| Commercial data | `sponsors.csv`, `panel_dataset.csv`, `sponsor_roi_outputs.csv` | investment, brand heat, ad exposure, ROI, sponsor ranking |
| Text and sentiment data | `social_media.csv`, `media_text_corpus.csv` | news narratives, sentiment, brand conversation, topic signal |
| Large-scale real text units | `real_text_articles.csv`, `text_embeddings_reduced.csv` | several thousand real-source text units, hashed TF-IDF, 24-dimensional reduction |
| Time-series data | `attention_timeseries.csv` | attention change before and after matches |
| Relationship-network data | `relationship_network.csv` | sponsor-team-player influence graph |

## Machine Learning Framework

The Python framework is modular and designed for research iteration:

| Module | File | Purpose |
|---|---|---|
| Real data ingestion | `src/real_data_ingestion.py` | Crawl public match records, GDELT article metadata, and Wikimedia page text |
| Fallback data generation | `src/preprocess.py` | Build reproducible backup data when network sources are unavailable |
| Text dimensionality reduction | `src/text_dimensionality.py` | Convert real-source text units into low-dimensional text features |
| Feature engineering | `src/feature_builder.py` | Join data and build FanScore, Sponsor Power Index, injury, sentiment, and ROI features |
| Shared ML configuration | `src/ml_config.py` | Centralize feature lists, model registry, random seed, and task definitions |
| Match prediction | `src/train_match_model.py` | Predict win/draw/loss probability |
| Sponsor ROI prediction | `src/train_roi_model.py` | Predict sponsor ROI using commercial and attention features |
| A/B simulation | `src/ab_simulation.py` | Simulate sponsor spend and player availability changes |
| Data quality | `src/data_quality.py` | Generate dataset coverage and quality summaries |
| Report generation | `src/report_generator.py` | Produce project reports |

More detail: [docs/ML_FRAMEWORK.md](docs/ML_FRAMEWORK.md)

Model roadmap: [docs/MODEL_ZOO.md](docs/MODEL_ZOO.md)  
Feature dictionary: [docs/FEATURE_DICTIONARY.md](docs/FEATURE_DICTIONARY.md)

## Modeling Tasks

### 1. Match Outcome Prediction

**Goal**: estimate win/draw/loss probabilities as context for sponsorship decisions.

Feature groups:

- team strength and recent performance
- core player rating and market value
- injury risk and player availability
- coach experience
- host advantage, stadium, weather, and stage
- media attention and sentiment

### 2. Sponsor ROI Prediction

**Goal**: predict sponsor return using commercial signals and sports context.

Feature groups:

- Sponsor Power Index
- sponsor spend and ad exposure
- brand heat and paid media share
- FanScore and fan growth
- social engagement and media reposts
- player influence and availability
- match probability context

### 3. Counterfactual A/B Simulation

**Goal**: support sponsor strategy testing before or during a tournament.

Example simulations:

- increase sponsor investment by 20%
- reduce core player availability
- increase ad exposure during knockout matches
- compare high-brand-fit vs low-brand-fit sponsors
- test sentiment decline after a poor match result

### 4. Uncertainty Quantification

**Goal**: make ROI outputs decision-ready instead of overconfident point estimates.

Outputs:

- conformal-style ROI prediction intervals
- Monte Carlo ROI risk distribution
- negative ROI probability
- ensemble variance proxy
- business risk score
- scenario ranking with strategy recommendations

### 5. Generative Business Reporting

The platform is structured to turn model outputs, feature importance, SHAP-ready explanations, uncertainty estimates, and scenario rankings into Markdown/PDF business reports. This positions the project as a decision-support platform rather than a chart collection.

## Dashboard

The dashboard is designed as a business decision cockpit, not a static visualization page.

Core modules:

- **Match Probability**: win/draw/loss probability and context.
- **Sponsor ROI Visualization**: ROI cards, ring chart, sponsor comparison, investment controls.
- **FanScore and Player Influence**: radar chart, player/fan contribution, availability effect.
- **Weather and Venue Impact**: heatmap and environment signals.
- **A/B Scenario Lab**: sponsor investment, player availability, and ROI shift.

Interactive features:

- team, sponsor, player, and stage filters
- year and round selection
- dynamic KPI cards
- ROI ring/progress indicators
- weather heatmap
- FanScore radar chart
- investment slider with visual money indicators
- five-level outcome feedback from low return to "Perfect"

## Data Strategy

The current repository now uses real public data sources where available. Some commercial features, such as exact sponsor spend and player market value, remain proxy-derived because reliable public contract-level data is not consistently available.

| Domain | Current Data | Source / Notes |
|---|---|---|
| Matches | real World Cup match records | `martj42/international_results` public CSV |
| 2026 schedule | real-source schedule rows when present in public CSV | same public CSV source |
| Text narratives | real-source text units | GDELT article metadata + Wikimedia page text + real match fact text |
| Text reduction | 768 hashed TF-IDF features reduced to 24 dimensions | dependency-light covariance eigendecomposition |
| Players | proxy-derived from real team history | marked with `data_origin` |
| Coaches | proxy-derived from real team history | marked with `data_origin` |
| Weather | proxy context attached to real match records | replaceable with Open-Meteo/Meteostat |
| Sponsors | real sponsor brand names with proxy commercial metrics | exact spend requires commercial datasets |
| Social media | proxy engagement derived from real text sentiment and event attention | replaceable with social APIs |
| Network | sponsor-team-player relationship graph | mixed real brand/team names and proxy weights |

Dataset docs:

- [docs/DATASET_CARD.md](docs/DATASET_CARD.md)
- [docs/MULTIMODAL_DATA_SYSTEM.md](docs/MULTIMODAL_DATA_SYSTEM.md)
- [docs/FEATURE_DICTIONARY.md](docs/FEATURE_DICTIONARY.md)
- [docs/data_dictionary.csv](docs/data_dictionary.csv)

## Engineering

The project includes a reproducible engineering scaffold:

- **Python**: data generation, feature engineering, ML, uncertainty, scenario simulation, dashboard generation.
- **SQL**: `sql/schema.sql` defines analysis-ready database tables.
- **Java**: `java/SponsorRiskRules.java` demonstrates business-rule integration for sponsor risk decisions.
- **Docker**: `Dockerfile` supports containerized dashboard/pipeline execution.
- **GitHub Actions**: `.github/workflows/ci.yml` compiles modules and runs the reproducible pipeline.
- **Configuration**: `config/pipeline.yaml` documents pipeline order and expected outputs.

## Installation

```bash
git clone https://github.com/2417467487-hub/WorldCupROI.git
cd WorldCupROI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
```

## Run The Pipeline

```bash
python src/preprocess.py
python src/real_data_ingestion.py
python src/feature_builder.py
python src/advanced_features.py
python src/text_dimensionality.py
python src/data_quality.py
python src/train_match_model.py
python src/train_roi_model.py
python src/uncertainty.py
python src/scenario_engine.py
python src/ab_simulation.py
python src/report_generator.py
python src/build_plotly_dashboard.py
```

## Launch Dashboard

Streamlit:

```bash
streamlit run dashboard/app.py
```

Static Plotly HTML:

```bash
python src/build_plotly_dashboard.py
```

Then open:

```text
dashboard/panel_dashboard.html
```

## Evaluation

| Area | Metrics |
|---|---|
| Match prediction | accuracy, log loss, probability calibration |
| ROI prediction | MAE, R2, residual analysis |
| Sponsor simulation | predicted ROI lift, investment sensitivity, player availability effect |
| Data quality | row count, missing rate, duplicate keys, schema coverage |
| Dashboard value | decision clarity, KPI readability, scenario comparison speed |

## Roadmap

- Add real API connectors for weather, schedule, social media, and sponsor data.
- Add LightGBM/XGBoost model variants for tabular sports-business prediction.
- Add SHAP explanations directly into the dashboard.
- Add sentiment modeling with transformer embeddings for news and social text.
- Add graph analytics for sponsor-team-player networks.
- Add time-series forecasting for fan attention and campaign momentum.
- Add sponsor category benchmarks for apparel, beverage, finance, airline, technology, and automotive brands.
- Add downloadable executive reports from the dashboard.

## Chinese Summary

WorldCupROI 已升级为 AI Sports Sponsorship Intelligence Platform。项目以世界杯为研究场景，但重点是体育商业智能：把球队、球员、教练、伤病、天气、赛事阶段、赞助商投入、广告曝光、媒体转载、品牌热度、社交媒体互动、粉丝增长和情绪分析统一到一个机器学习与商业决策平台中。

平台目标是预测赞助 ROI、解释商业影响因素、模拟赞助策略变化，并通过互动仪表盘支持体育赞助决策。
