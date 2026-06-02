# WorldCupROI Machine Learning Framework

## Objective

WorldCupROI is organized as a multi-task machine learning project:

1. **Match outcome prediction**: estimate win/draw/loss probability.
2. **Sponsor ROI prediction**: estimate commercial return from attention, exposure, sponsor investment, and team/player factors.
3. **Counterfactual simulation**: test sponsor strategies and player availability scenarios.

## Python Framework

```text
src/
  preprocess.py          # reproducible data generation and public-data shaped CSVs
  feature_builder.py     # feature joins, FanScore, Sponsor Power Index, ROI target
  ml_config.py           # model registry, feature groups, ML task definitions
  train_match_model.py   # match outcome classification
  train_roi_model.py     # sponsor ROI regression
  fan_score.py           # standalone FanScore computation
  sponsor_roi.py         # standalone sponsor ROI scoring
  ab_simulation.py       # counterfactual experiments
  data_quality.py        # dataset profiling and data quality summary
  report_generator.py    # sample Markdown/PDF reporting
```

## Current Reproducible Models

The repository uses dependency-free fallback models so the full pipeline can run without heavy package installation.

| Task | Current model | Target | Metrics |
| --- | --- | --- | --- |
| Match outcome | centroid classifier | `result` | accuracy, log loss |
| Sponsor ROI | ridge regression | `sponsor_roi` | MAE, R2 |

## Production Upgrade Path

| Task | Recommended models | Why |
| --- | --- | --- |
| Match outcome | XGBoost `multi:softprob`, LightGBM multiclass | strong tabular performance and probability outputs |
| Match sequence modeling | LSTM / temporal transformer | useful if chronological team form sequences are expanded |
| Sponsor ROI | XGBoostRegressor, LightGBMRegressor | non-linear ROI response to attention, spend, and activation |
| Interpretability | SHAP TreeExplainer | explains feature contribution for sponsor and match predictions |

## Feature Groups

| Group | Example features |
| --- | --- |
| Team strength | Elo difference, squad market value, recent goal difference |
| Player influence | core rating, market value, followers |
| Coach context | World Cup matches coached, tenure, win rate |
| Venue/weather | host advantage, stadium capacity, temperature, humidity |
| Media attention | event attention, media reposts, social video views |
| Sponsor activation | spend, brand fit, activation quality, sports presence |

## Modeling Notes

- Match prediction is treated as an upstream signal, not the final business output.
- ROI prediction is the commercial target and combines FanScore, Sponsor Power Index, exposure, and match context.
- A/B simulation edits input features and recomputes ROI to estimate strategy sensitivity.
- SHAP is listed as an upgrade path because the fallback model avoids heavy dependencies for reproducibility.

