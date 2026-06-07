# WorldCupROI Maintenance Upgrade - 2026-06-07

## Scope

This maintenance pass upgraded the project in three areas:

1. Algorithm structure
2. Platform health and operating workflow
3. README / project summary communication

The full reproducible pipeline was also run with existing committed data snapshots, which refreshed many generated data and report artifacts.

## Algorithm Upgrades

Added:

- `src/algorithm_strategy.py`
- `reports/algorithm_manifest.json`
- `reports/algorithm_strategy.md`
- `reports/match_outcome_model_card.md`
- `reports/match_outcome_model_card.json`
- `reports/sponsor_roi_model_card.md`
- `reports/sponsor_roi_model_card.json`
- `reports/match_feature_group_importance.csv`
- `reports/roi_feature_group_importance.csv`

The algorithm system is now documented as four layers:

| Layer | Current method | Upgrade path |
|---|---|---|
| Match Outcome Layer | CentroidOutcomeModel fallback | calibrated logistic regression, LightGBM, XGBoost |
| Sponsor ROI Layer | standardized RidgeROIModel fallback | ElasticNet, LightGBMRegressor, XGBoostRegressor, stacked ensemble |
| Risk And Recommendation Layer | bootstrap, Monte Carlo, conformal intervals | ensemble variance, Bayesian optimization, portfolio allocation |
| Relationship Intelligence Layer | weighted graph centrality | GraphSAGE, heterogeneous GNN, temporal graph model |

## Platform Upgrades

Added:

- `src/platform_health.py`
- `reports/platform_health.json`
- `reports/platform_health.csv`
- `reports/platform_health.md`
- `make health`

Latest platform health:

- Score: 100 / 100
- Status: healthy

## Documentation Upgrades

Updated:

- `README.md`
- `PROJECT_SUMMARY.md`
- `config/pipeline.yaml`
- `Makefile`

README now explains:

- algorithm layers
- model cards
- algorithm manifest
- platform health check
- updated ROI / conformal / scenario metrics

## Verification

Commands run:

```powershell
ml-python src\algorithm_strategy.py
ml-python src\train_match_model.py
ml-python src\train_roi_model.py
ml-python src\platform_health.py
ml-python -m compileall src
ml-python scripts\run_pipeline.py
```

The full pipeline completed successfully and ended with:

```text
{'health_score': 100.0, 'status': 'healthy'}
```

## Current Key Metrics

| Metric | Value |
|---|---:|
| Match accuracy | 0.5566 |
| Match log loss | 0.9780 |
| ROI MAE | 0.1216 |
| ROI RMSE | 0.1497 |
| ROI R2 | 0.8326 |
| Match conformal coverage | 0.9021 |
| ROI conformal coverage | 0.8505 |
| Average negative ROI probability | 0.0000 |

## Notes

- A full pipeline run refreshed generated data and report files. Review generated artifact diffs separately from source-code diffs.
- Python cache directories were cleaned after validation.
- Optional future upgrade: add calibrated sklearn/LightGBM/XGBoost model selection as a production mode while keeping the dependency-free fallback path.
