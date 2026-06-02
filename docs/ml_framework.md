# Sports Sponsorship Intelligence ML Framework

## Objective

WorldCupROI is organized as a sports business intelligence platform with three connected analytics layers:

1. **Sports Analytics**: estimate match context, team strength, player availability, coach influence, weather impact, and tournament-stage importance.
2. **Sponsorship Intelligence**: estimate sponsor power from investment, ad exposure, brand heat, activation quality, media attention, and brand-team fit.
3. **Business Intelligence**: predict sponsor ROI, compare A/B scenarios, and support commercial decision-making.

The platform uses match outcome prediction as an upstream signal. The main business target is **sponsor ROI**.

## Python Framework

```text
src/
  preprocess.py          # reproducible data generation and API-ready data schemas
  feature_builder.py     # multimodal feature joins, FanScore, Sponsor Power Index, ROI target
  ml_config.py           # model registry, feature groups, task definitions
  train_match_model.py   # match outcome classification
  train_roi_model.py     # sponsor ROI regression
  fan_score.py           # fan influence scoring
  sponsor_roi.py         # sponsor strength and ROI logic
  ab_simulation.py       # counterfactual sponsor/player experiments
  data_quality.py        # dataset quality and coverage report
  report_generator.py    # research/business report generation
```

## Current Reproducible Models

The repository uses lightweight fallback models so the full pipeline can run without heavy dependencies.

| Task | Current Model | Target | Business Use |
|---|---|---|---|
| Match outcome | centroid classifier | `result` | context for sponsor risk and stage value |
| Sponsor ROI | ridge regression | `sponsor_roi` | sponsor return prediction and strategy ranking |
| A/B simulation | model-based counterfactual edits | predicted ROI shift | investment and player-availability decision support |

## Production Upgrade Path

| Task | Recommended Models | Reason |
|---|---|---|
| Match outcome | XGBoost multiclass, LightGBM multiclass, CatBoost | strong tabular performance and probability outputs |
| Temporal form | LSTM, temporal transformer, TCN | captures team momentum and attention time series |
| Sponsor ROI | XGBoostRegressor, LightGBMRegressor, causal forest | models non-linear ROI response to spend, exposure, and sentiment |
| Text analytics | sentence transformers, topic models, sentiment classifiers | extracts media narrative and sponsor conversation signals |
| Network analytics | graph centrality, node embeddings, GNN baseline | measures sponsor-team-player influence networks |
| Interpretability | SHAP, permutation importance, partial dependence | explains ROI and match probability drivers |

## Feature Groups

| Group | Example Features |
|---|---|
| Team strength | Elo difference, market value difference, recent goal difference |
| Player influence | rating, market value, followers, fan growth, sentiment |
| Injury and availability | injury risk, availability score, availability difference |
| Coach context | World Cup matches coached, tenure, win rate |
| Venue/weather | host advantage, capacity, temperature, humidity, weather severity |
| Media attention | event attention, reposts, engagement rate, time-decay attention |
| Text sentiment | news sentiment, narrative topic, text signal score |
| Sponsor activation | spend, ad exposure, brand heat, paid media share, brand fit |
| Business outcome | predicted ROI, ROI lift, Sponsor Power Index |

## Model Flow

```text
raw CSV/API data
   -> preprocess.py
   -> feature_builder.py
   -> modeling_dataset.csv
   -> train_match_model.py
   -> train_roi_model.py
   -> ab_simulation.py
   -> dashboard + reports
```

## Research Value

- Separates sports performance from commercial conversion.
- Measures how fan attention and brand activation amplify or weaken ROI.
- Allows counterfactual analysis for decisions that cannot be tested directly in real tournaments.
- Keeps the project reproducible while remaining ready for real data connectors.
