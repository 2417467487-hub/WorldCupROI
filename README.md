# WorldCupROI

**Turning FIFA World Cup attention into sponsorship ROI intelligence.**  
**把世界杯注意力转化为赞助 ROI 决策智能。**

WorldCupROI is a machine learning, business analytics, and user research project built around FIFA World Cup data from 1930-2022, a mock 2026 schedule, sponsors, player fan bases, coach statistics, weather, venue context, and media coverage.

WorldCupROI 是一个结合机器学习、商业分析和用户研究洞察的世界杯赞助 ROI 项目，覆盖 1930-2022 历史比赛、2026 赛程、球队赞助商、球员粉丝、教练统计、天气、场馆和媒体传播数据。

## Project Highlights / 项目亮点

- Match win/draw/loss probability modeling
- Sponsor ROI regression and commercial momentum scoring
- FanScore for player and fan influence analysis
- Sponsor Power Index for brand activation strength
- Counterfactual A/B simulation for sponsor strategy and player availability
- Interactive FIFA-themed dashboard with KPI cards, radar chart, heatmap, ring chart, filters, scenario presets, and animated effects
- Reproducible mock CSV pipeline when public APIs are unavailable

## Repository Structure / 项目结构

```text
WorldCupROI/
  data/
    historical_matches.csv
    schedule_2026.csv
    players.csv
    coaches.csv
    sponsors.csv
    weather.csv
    social_media.csv
    modeling_dataset.csv
    panel_dataset.csv
    fan_score_outputs.csv
    sponsor_roi_outputs.csv
  notebooks/
    01_EDA.ipynb
    02_Model_Training.ipynb
    03_AB_Experiment.ipynb
    04_Sponsor_ROI_Simulation.ipynb
    05_Feature_Engineering.ipynb
  src/
    preprocess.py
    feature_builder.py
    train_match_model.py
    train_roi_model.py
    ab_simulation.py
    fan_score.py
    sponsor_roi.py
    report_generator.py
    build_panel_data.py
  dashboard/
    app.py
    panel_dashboard.html
  reports/
    WorldCupROI_research_report.md
    sample_report.md
  README.md
  requirements.txt
  sample_report.pdf
```

## Dashboard / 互动平台

The project includes two dashboard surfaces:

- `dashboard/app.py`: Streamlit + Plotly dashboard
- `dashboard/panel_dashboard.html`: browser-ready Plotly dashboard with World Cup visual styling

Dashboard modules:

- **Match Win/Draw/Loss Probability**: stacked Plotly probability bars with hover tooltips
- **Sponsor ROI Visualization**: ROI scatter map, dynamic KPI cards, sponsor ROI ring chart
- **FanScore / Player & Fan Influence**: radar chart for player followers, attention, media reposts, FanScore, and momentum
- **Weather & Home/Away Impact**: weather-stage heatmap and temperature impact scatter plot
- **A/B Simulation**: sponsor strategy and player availability scenario comparison

Interactivity:

- Team, sponsor, player/team proxy, match stage filters
- Year / round time slider
- Dynamic KPI cards
- Hover tooltips on Plotly charts
- Color gradients based on ROI and scenario lift
- HTML version includes scenario presets: `Balanced Play`, `All-in Sponsor`, `Star Out`, `Media Surge`
- Animated ROI signal, money markers, player availability tags, and five-level verdict labels

## Machine Learning Pipeline / 机器学习流程

```text
preprocess.py
  -> mock/public-style CSV generation
feature_builder.py
  -> team/player/sponsor/weather/media feature engineering
train_match_model.py
  -> win/draw/loss probability model
train_roi_model.py
  -> sponsor ROI regression model
ab_simulation.py
  -> counterfactual sponsor/player scenarios
fan_score.py
  -> FanScore computation
sponsor_roi.py
  -> ROI formula score and sponsor efficiency outputs
report_generator.py
  -> sample Markdown/PDF report
```

Model notes:

- The repository includes dependency-free fallback models for reproducibility.
- `requirements.txt` includes scikit-learn / Plotly / Streamlit / SHAP.
- XGBoost, LightGBM, or LSTM can replace the fallback model in production.
- SHAP-style feature importance is supported through saved feature importance reports and can be upgraded with `shap` when the package is installed.

Current reproducible run:

| Model | Metric | Value |
| --- | ---: | ---: |
| Match outcome model | Accuracy | 0.3481 |
| Match outcome model | Log loss | 1.0939 |
| Sponsor ROI model | MAE | 0.1439 |
| Sponsor ROI model | R2 | 0.7346 |

## Metric Definitions / 指标定义

### FanScore

```text
FanScore = 0.45 * player_fans_scaled
         + 0.35 * event_attention_scaled
         + 0.20 * media_reposts_scaled
```

### Sponsor Power Index

```text
SPI = 0.40 * sponsor_spend_scaled
    + 0.25 * brand_fit
    + 0.20 * activation_quality
    + 0.15 * historical_sports_presence
```

### Commercial Momentum

```text
Commercial Momentum = 0.38 * FanScore
                    + 0.34 * Sponsor Power Index
                    + 0.18 * Exposure Score
                    + 0.10 * Match Points
```

## Example Data Schema / 示例数据结构

### historical_matches.csv

| Column | Description |
| --- | --- |
| `match_id` | match identifier |
| `year` | World Cup year |
| `team_a`, `team_b` | competing teams |
| `stage` | group, round_16, quarter_final, semi_final, final |
| `result` | A_win, draw, B_win |
| `event_attention_m` | event attention in millions |
| `media_reposts_k` | media repost count in thousands |

### players.csv

| Column | Description |
| --- | --- |
| `team` | team name |
| `player_role` | core_forward, core_midfielder, core_defender |
| `player_rating` | simulated performance rating |
| `market_value_m` | market value in millions |
| `followers_m` | fan followers in millions |

### coaches.csv

| Column | Description |
| --- | --- |
| `team` | team name |
| `coach_wc_matches` | World Cup matches coached |
| `coach_win_rate` | simulated coach win rate |
| `coach_tenure_years` | tenure length |

### sponsors.csv

| Column | Description |
| --- | --- |
| `team` | sponsored team |
| `sponsor` | sponsor name |
| `sponsor_spend_m` | sponsorship spend in millions |
| `brand_fit` | brand-team fit score |
| `activation_quality` | campaign activation quality |

### weather.csv

| Column | Description |
| --- | --- |
| `match_id` | match identifier |
| `temperature_c` | temperature |
| `humidity` | humidity |
| `weather` | clear, cloudy, rain, hot, windy |
| `venue_region` | venue region |
| `weather_severity` | normalized weather severity |

### social_media.csv

| Column | Description |
| --- | --- |
| `match_id` | match identifier |
| `event_attention_m` | attention volume |
| `media_reposts_k` | repost volume |
| `hashtag_mentions_k` | hashtag mentions |
| `video_views_m` | video views |
| `sentiment_score` | social sentiment |

## Installation / 安装

```bash
pip install -r requirements.txt
```

## Run Pipeline / 运行流程

```bash
python src/preprocess.py
python src/feature_builder.py
python src/train_match_model.py
python src/train_roi_model.py
python src/ab_simulation.py
python src/build_panel_data.py
python src/fan_score.py
python src/sponsor_roi.py
python src/report_generator.py
```

## Launch Dashboard / 启动 Dashboard

Streamlit + Plotly:

```bash
streamlit run dashboard/app.py
```

Static interactive HTML:

```text
dashboard/panel_dashboard.html
```

## Outputs / 输出

- `dashboard/app.py`: Streamlit + Plotly dashboard
- `dashboard/panel_dashboard.html`: static interactive website
- `src/build_plotly_dashboard.py`: generates the Plotly-based static website
- `sample_report.pdf`: generated sample report
- `reports/ab_simulation_results.csv`: A/B scenario rows
- `reports/match_feature_importance.csv`: match model feature importance
- `reports/roi_feature_importance.csv`: ROI model feature importance
- `data/panel_dataset.csv`: `year x match_id x team x sponsor` panel data

## Roadmap / 路线图

- Add public API connectors for real FIFA and club sponsorship datasets
- Add native XGBoost / LightGBM profiles
- Add SHAP summary plots into the dashboard
- Deploy the HTML dashboard to GitHub Pages
- Add real 2026 venue weather API integration
