# Temporal Modeling Report

## Scope

Model ROI as a time-aware sponsorship signal across World Cup cycles, stages, player strength, and attention context.

## Current Baseline

- Time-aware baseline: stage-level exponential weighted ROI trend.
- Transformer proxy: attention-weighted temporal score that blends event attention and player quality.
- Upgrade path: replace proxy with sequence Transformer or Time-aware GNN over match/team/sponsor histories.

## Future ROI Forecast

| year | stage | avg_roi | avg_attention | avg_player_rating | samples | ewm_roi | temporal_attention_score | model_family |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | group_or_knockout | nan | nan | nan | 0 | 3.5856 | 0.9332 | temporal_ewm_with_transformer_attention_proxy |
| 2026 | tournament | nan | nan | nan | 0 | 3.8466 | 0.9126 | temporal_ewm_with_transformer_attention_proxy |
| 2030 | tournament | nan | nan | nan | 0 | 3.7181 | 0.9126 | temporal_ewm_with_transformer_attention_proxy |
| 2034 | group_or_knockout | nan | nan | nan | 0 | 3.5750 | 0.9378 | temporal_ewm_with_transformer_attention_proxy |
| 2034 | tournament | nan | nan | nan | 0 | 3.7181 | 0.9126 | temporal_ewm_with_transformer_attention_proxy |