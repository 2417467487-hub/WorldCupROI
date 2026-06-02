# WorldCupROI

**FIFA World Cup sponsorship ROI intelligence: match prediction, fan attention, media exposure, and business conversion modeling.**  
**世界杯赞助 ROI 智能分析系统：融合比赛预测、球迷影响力、媒体曝光与商业转化建模。**

WorldCupROI is an end-to-end machine learning and business analytics project built around FIFA World Cup historical matches from 1930-2022, a reproducible 2026 schedule layer, team sponsors, player fan base, coach experience, weather, venue context, and media coverage.

WorldCupROI 的核心并不是单纯预测“哪支球队会赢”，而是研究世界杯商业场景中，竞技表现、球员影响力、球迷关注、天气场地、媒体传播和赞助投入如何共同转化为赞助商 ROI。

## What Makes It Different

- **Multi-task ML system**: match outcome classification and sponsor ROI regression are connected in one pipeline.
- **Business-first target**: match probability is treated as an upstream signal for commercial conversion, not the final product.
- **Interactive decision lab**: sponsor investment, player availability, fan exposure, media coverage, weather, and match stage can be changed in the dashboard.
- **Explainable modeling**: feature importance files are generated for match outcome and ROI models, with SHAP-ready model outputs.
- **User research angle**: dashboard modules are designed around sponsor analyst workflows: scan, compare, simulate, and justify.
- **Reproducible data layer**: public-data-compatible schemas are included, while mock CSVs keep the project runnable without paid APIs.

## Project Structure

```text
WorldCupROI/
├── data/
│   ├── historical_matches.csv
│   ├── schedule_2026.csv
│   ├── players.csv
│   ├── coaches.csv
│   ├── sponsors.csv
│   ├── weather.csv
│   ├── social_media.csv
│   ├── modeling_dataset.csv
│   └── panel_dataset.csv
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling.ipynb
│   ├── 04_sponsor_roi_simulation.ipynb
│   └── 05_ab_experiment.ipynb
├── src/
│   ├── preprocess.py
│   ├── feature_builder.py
│   ├── ml_config.py
│   ├── train_match_model.py
│   ├── train_roi_model.py
│   ├── ab_simulation.py
│   ├── fan_score.py
│   ├── sponsor_roi.py
│   ├── data_quality.py
│   ├── build_plotly_dashboard.py
│   └── report_generator.py
├── dashboard/
│   ├── app.py
│   └── panel_dashboard.html
├── docs/
│   ├── ML_FRAMEWORK.md
│   ├── DATASET_CARD.md
│   └── data_dictionary.csv
├── reports/
├── models/
├── README.md
├── requirements.txt
└── sample_report.pdf
```

## Machine Learning Framework

The project uses a modular Python ML structure instead of placing all logic in notebooks.

| Layer | File | Responsibility |
|---|---|---|
| Data cleaning | `src/preprocess.py` | Load raw CSVs, standardize keys, prepare clean tables |
| Feature engineering | `src/feature_builder.py` | Build match, team, player, coach, weather, fan, and sponsor features |
| Shared ML config | `src/ml_config.py` | Central feature lists, random seed, train/test settings, model registry |
| Match model | `src/train_match_model.py` | Predict win/draw/loss probabilities |
| ROI model | `src/train_roi_model.py` | Predict sponsor ROI from business and attention features |
| Fan influence | `src/fan_score.py` | Calculate FanScore from fans, event attention, and media sharing |
| Sponsor logic | `src/sponsor_roi.py` | Calculate Sponsor Power Index and ROI signals |
| A/B simulation | `src/ab_simulation.py` | Run counterfactual sponsor and player availability experiments |
| Data QA | `src/data_quality.py` | Profile dataset rows, columns, missing rate, and duplicate keys |
| Reporting | `src/report_generator.py` | Produce Markdown/PDF-style project reports |

详细说明见 [docs/ML_FRAMEWORK.md](docs/ML_FRAMEWORK.md)。

## Modeling Strategy

### 1. Match Win/Draw/Loss Prediction

**Task type**: multi-class classification  
**Target**: home win / draw / away win  
**Baseline implementation**: `RandomForestClassifier` for full reproducibility  
**Production-ready alternatives**: XGBoost, LightGBM, CatBoost, LSTM sequence model

Main feature groups:

- Team form: FIFA-style rating, historical win rate, goals for, goals against
- Player strength: player rating, core player market value, injury/availability proxy
- Coach signal: coach experience, previous tournament experience
- Venue context: home/away flag, host advantage, match stage
- Environment: temperature, humidity, wind speed
- Attention signal: FanScore, media reposts, social media attention

Outputs:

- `models/match_outcome_model.joblib`
- `reports/match_model_metrics.md`
- `reports/match_feature_importance.csv`

### 2. Sponsor ROI Prediction

**Task type**: regression  
**Target**: sponsor ROI  
**Baseline implementation**: `RandomForestRegressor`  
**Production-ready alternatives**: LightGBM/XGBoost regression, ElasticNet, causal forests

ROI is modeled as a business conversion outcome influenced by:

- Sponsor investment
- Sponsor Power Index
- Match outcome probability
- FanScore
- Media exposure
- Social attention
- Player market value
- Match stage
- Weather and venue context

Outputs:

- `models/roi_model.joblib`
- `reports/roi_model_metrics.md`
- `reports/roi_feature_importance.csv`

### 3. Sponsor Power Index

Sponsor Power Index is designed as a compact commercial strength feature:

```text
Sponsor Power Index =
  normalized(investment)
+ normalized(brand strength)
+ normalized(media exposure)
+ normalized(team popularity)
+ normalized(stage premium)
```

The index is not only a descriptive metric. It becomes an input to ROI prediction and A/B simulation.

### 4. FanScore

FanScore combines fan base, match attention, and media spread:

```text
FanScore =
  player fan base signal
+ event attention signal
+ social media attention signal
+ news repost signal
+ core player market value signal
```

It captures the commercial difference between “a strong team” and “a team that creates sponsor-visible attention”.

### 5. Counterfactual A/B Simulation

The simulation module compares scenarios such as:

- Sponsor A increases investment by 20%
- Core player becomes unavailable
- Media exposure rises during knockout stage
- Fan attention drops after an unexpected loss
- Weather conditions reduce match quality or attendance proxy

The output shows predicted ROI shift, KPI changes, and scenario ranking.

## Data Strategy

The project supports public-data replacement while remaining fully reproducible with mock CSVs.

| Dataset | Current Source | Upgrade Direction |
|---|---|---|
| Historical matches | Reproducible CSV mock aligned with World Cup structure | Kaggle World Cup match datasets, FIFA public records |
| 2026 schedule | Reproducible schedule table | Official 2026 match schedule once finalized |
| Players | Mock player ratings, fans, value | Transfermarkt-style value, FBref, Kaggle player tables |
| Coaches | Mock experience and tournament history | Public coach career records |
| Sponsors | Mock sponsor investment and category | Public sponsorship announcements and brand reports |
| Weather | Mock venue weather | Meteostat, Open-Meteo, NOAA-style weather APIs |
| Social media | Mock attention and reposts | YouTube, X/Twitter, Instagram, Google Trends, news API |

Data documentation:

- [docs/DATASET_CARD.md](docs/DATASET_CARD.md)
- [docs/data_dictionary.csv](docs/data_dictionary.csv)
- `reports/data_quality_summary.md`

Example schema:

```text
matches: match_id, year, stage, home_team, away_team, home_goals, away_goals, venue, host_country
players: player_id, team, player_name, rating, market_value_m, fan_followers_m, is_core_player
coaches: team, coach_name, years_experience, world_cup_experience, win_rate
sponsors: sponsor_id, team, sponsor_name, category, investment_m, brand_strength
weather: match_id, temperature_c, humidity_pct, wind_kmh, condition
social_media: match_id, team, social_mentions_k, media_reposts_k, search_interest
```

## Interactive Dashboard

The dashboard is designed as an analyst-facing decision platform rather than a static chart page.

### Modules

- **Match Win/Draw/Loss Probability**: team and stage filters with dynamic probability charts.
- **Sponsor ROI Visualization**: KPI cards, ROI ring chart, investment controls, and sponsor ranking.
- **FanScore / Player & Fan Influence**: radar chart and player impact comparison.
- **Weather & Home/Away Impact**: heatmap for venue/weather effect and contextual match signals.
- **A/B Simulation Window**: compare sponsor investment and core player availability scenarios.

### Interactivity

- Team, sponsor, player, and match stage dropdowns
- Time/year slider
- Dynamic KPI cards
- ROI progress/ring visualization
- Radar chart for FanScore components
- Weather impact heatmap
- Investment slider with changing money icons
- Player availability controls
- Five-level benefit feedback states, from low performance to “Perfect”

### Theme

The visual design uses a World Cup-inspired palette:

- pitch green
- stadium blue
- white cards
- orange highlights
- metric-based color gradients
- rounded cards, shadows, and responsive grid layout

## Installation

```bash
git clone https://github.com/2417467487-hub/WorldCupROI.git
cd WorldCupROI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux activation:

```bash
source .venv/bin/activate
```

## Run The Pipeline

```bash
python src/preprocess.py
python src/feature_builder.py
python src/data_quality.py
python src/train_match_model.py
python src/train_roi_model.py
python src/ab_simulation.py
python src/report_generator.py
python src/build_plotly_dashboard.py
```

## Launch Dashboard

Streamlit version:

```bash
streamlit run dashboard/app.py
```

Static Plotly HTML version:

```bash
python src/build_plotly_dashboard.py
```

Then open:

```text
dashboard/panel_dashboard.html
```

## Evaluation Metrics

| Model | Metrics |
|---|---|
| Match outcome classification | Accuracy, log loss, class probability calibration |
| Sponsor ROI regression | MAE, R2, residual inspection |
| A/B simulation | Predicted ROI lift, investment sensitivity, player availability impact |
| Data quality | Missing rate, duplicate keys, row count, schema coverage |

## README Optimization Notes

This README is structured for a GitHub portfolio-style technical project:

- The opening explains the business problem before listing tools.
- The ML pipeline is separated from the dashboard section.
- The data strategy is honest about mock data while showing clear public-data upgrade paths.
- The dashboard description emphasizes interaction, decision-making, and visual feedback.
- The project avoids personal interview language and keeps the tone project-centered.

## Roadmap

- Replace mock match records with a public World Cup dataset.
- Add LightGBM/XGBoost model variants behind the same `ml_config.py` registry.
- Add SHAP waterfall and beeswarm visualizations to the dashboard.
- Add calibration curves for match probability reliability.
- Add sponsor category segmentation by apparel, beverage, finance, and technology brands.
- Add downloadable PDF export from the Streamlit dashboard.

## 中文摘要

WorldCupROI 是一个世界杯赞助 ROI 预测与交互分析项目。项目将 1930-2022 世界杯历史比赛、2026 赛程、球队赞助、球员粉丝量、核心球员市场价值、教练经验、天气、主客场、社交媒体关注度和新闻转载量整合为一个多任务机器学习系统。

项目重点不是“预测比赛结果”本身，而是将比赛胜率、粉丝影响力、媒体曝光和赞助投入转化为可解释的商业 ROI 预测，并通过互动仪表盘支持赞助商投入、球员变动、天气影响和 A/B 方案模拟。
