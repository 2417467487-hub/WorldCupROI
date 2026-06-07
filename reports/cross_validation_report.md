# Cross-Validation Generalization Report

Five-fold cross-validation evaluates whether the current fallback models generalize beyond a single deterministic holdout split.

## Summary

| task | model | metric | folds | mean | std | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| match_outcome | CentroidOutcomeModel | accuracy | 5 | 0.5436 | 0.0389 | 0.5026 | 0.6010 |
| match_outcome | CentroidOutcomeModel | log_loss | 5 | 0.9861 | 0.0231 | 0.9584 | 1.0150 |
| sponsor_roi | RidgeROIModel | mae | 5 | 0.1162 | 0.0069 | 0.1070 | 0.1245 |
| sponsor_roi | RidgeROIModel | r2 | 5 | 0.8540 | 0.0226 | 0.8218 | 0.8837 |
| sponsor_roi | RidgeROIModel | rmse | 5 | 0.1425 | 0.0073 | 0.1315 | 0.1492 |

## Interpretation

- Match outcome accuracy should be read as a directional baseline because football outcomes are noisy and class balance changes by tournament era.
- Sponsor ROI R2 and MAE are more stable when commercial proxy features are internally consistent, but they remain bounded by proxy-label realism.
- Large fold-to-fold variance should trigger data leakage review, stronger temporal splits, or calibrated model selection before production use.