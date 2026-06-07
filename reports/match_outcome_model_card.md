# Match Outcome Model Card

- Model: CentroidOutcomeModel
- Target: `result`
- Feature count: 21
- Artifact: `models\match_outcome_model.pkl`
- Report: `reports\match_model_metrics.md`
- Random seed: 42
- Test size: 0.22

## Metrics

| Metric | Value |
|---|---:|
| accuracy | 0.5566 |
| log_loss | 0.9780 |

## Notes

Fallback match model estimates class probability from standardized distance to class centroids.