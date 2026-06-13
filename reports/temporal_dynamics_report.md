# Temporal Dynamics Report

This module upgrades static ROI analysis into stage-aware dynamic modeling.

| year | stage | stage_index | avg_roi | avg_momentum | avg_attention | avg_fan_score | roi_stage_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1978 | tournament | 2 | 3.7345 | 0.5527 | 48.4053 | 0.4981 | 0.0 |
| 1982 | tournament | 2 | 3.7005 | 0.528 | 50.1369 | 0.4875 | 0.0 |
| 1986 | group_or_knockout | 2 | 3.6432 | 0.5519 | 51.0046 | 0.5291 | 0.0 |
| 1990 | group_or_knockout | 2 | 3.6308 | 0.5243 | 51.7454 | 0.4871 | 0.0 |
| 1994 | group_or_knockout | 2 | 3.5943 | 0.539 | 54.2954 | 0.4878 | 0.0 |
| 1998 | group_or_knockout | 2 | 3.6588 | 0.547 | 55.6681 | 0.5137 | 0.0 |
| 2002 | group_or_knockout | 2 | 3.629 | 0.5485 | 56.7844 | 0.5321 | 0.0 |
| 2006 | group_or_knockout | 2 | 3.6672 | 0.5401 | 57.7631 | 0.5043 | 0.0 |
| 2010 | group_or_knockout | 2 | 3.6123 | 0.5528 | 59.1544 | 0.5225 | 0.0 |
| 2014 | group_or_knockout | 2 | 3.7212 | 0.5788 | 61.4983 | 0.5533 | 0.0 |
| 2018 | group_or_knockout | 2 | 3.7484 | 0.595 | 62.8894 | 0.5862 | 0.0 |
| 2022 | group_or_knockout | 2 | 3.6571 | 0.5899 | 64.4525 | 0.5798 | 0.0 |

## Research Upgrade Path

- Time-aware GNN: propagate sponsor influence over match-stage graph snapshots.
- Temporal Transformer: learn exposure and attention trajectories by stage.
- Dynamic treatment effects: estimate how media exposure effects change from group stage to final.