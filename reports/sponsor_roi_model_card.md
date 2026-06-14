# Sponsor Roi Model Card

- Model: RidgeROIModel
- Target: `sponsor_roi`
- Feature count: 32
- Artifact: `models\sponsor_roi_model.pkl`
- Report: `reports\roi_model_metrics.md`
- Random seed: 42
- Test size: 0.22

## Metrics

| Metric | Value |
|---|---:|
| mae | 0.1165 |
| rmse | 0.1443 |
| r2 | 0.8478 |

## Notes

Fallback ROI model uses standardized ridge regression so the platform remains reproducible without optional boosting libraries.