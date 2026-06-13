# Graph Learning Report

This module upgrades graph analysis into graph learning proxies: link prediction and heterogeneous influence ranking.

## Top Link Predictions

| sponsor | candidate_team | link_prediction_score | method |
| --- | --- | --- | --- |
| sponsor:Hyundai | team:Algeria | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Hungary | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Slovakia | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:France | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Saudi Arabia | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Canada | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Cuba | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Israel | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Denmark | 2.64 | common-neighbor HGT proxy |
| sponsor:Hyundai | team:Brazil | 2.64 | common-neighbor HGT proxy |

## Node Influence Ranking

| node | node_type | hgt_influence_proxy |
| --- | --- | --- |
| sponsor:Hyundai | sponsor | 1261.417 |
| sponsor:Adidas | sponsor | 1079.883 |
| sponsor:Coca-Cola | sponsor | 1046.33 |
| sponsor:Visa | sponsor | 1030.583 |
| sponsor:Hisense | sponsor | 787.907 |
| sponsor:Budweiser | sponsor | 775.724 |
| sponsor:McDonald's | sponsor | 725.071 |
| sponsor:Qatar Airways | sponsor | 647.604 |
| sponsor:Vivo | sponsor | 580.617 |
| sponsor:Mengniu | sponsor | 367.196 |

## Upgrade Path

- Heterogeneous Graph Transformer: learn type-specific attention over Sponsor, Team, Player and Match nodes.
- Link prediction: forecast future sponsor-team effectiveness before contract allocation.
- Temporal graph learning: use stage snapshots to model changing influence.