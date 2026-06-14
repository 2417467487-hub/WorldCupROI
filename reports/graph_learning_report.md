# Graph Learning Report

## Upgrade

Graph analysis is upgraded into graph learning with future sponsor-team link prediction and future sponsor ROI scoring.

## Current Baseline

- Heterogeneous graph schema: teams, sponsors, players, matches, and events.
- Link prediction baseline: sponsor-team compatibility score from ROI, attention, sponsor power, and fit.
- Upgrade path: HGT or GraphSAGE with typed nodes, temporal edges, and link-prediction loss.

## Top Future Sponsor Links

| team | sponsor | existing_edge | link_prediction_score | future_sponsor_roi_prediction | model_family | rank |
| --- | --- | --- | --- | --- | --- | --- |
| Brazil | Adidas | True | 2.8845 | 2.9813 | HGT_GNN_compatible_link_prediction_baseline | 1 |
| Brazil | Hyundai | False | 2.8525 | 2.9510 | HGT_GNN_compatible_link_prediction_baseline | 2 |
| Brazil | Qatar Airways | False | 2.8293 | 2.9146 | HGT_GNN_compatible_link_prediction_baseline | 3 |
| Brazil | Visa | False | 2.8277 | 2.9189 | HGT_GNN_compatible_link_prediction_baseline | 4 |
| Brazil | Coca-Cola | False | 2.8150 | 2.8964 | HGT_GNN_compatible_link_prediction_baseline | 5 |
| Brazil | Budweiser | False | 2.8142 | 2.9007 | HGT_GNN_compatible_link_prediction_baseline | 6 |
| Argentina | Adidas | False | 2.8028 | 2.8969 | HGT_GNN_compatible_link_prediction_baseline | 7 |
| Brazil | Hisense | False | 2.8011 | 2.8805 | HGT_GNN_compatible_link_prediction_baseline | 8 |
| France | Adidas | False | 2.7849 | 2.8784 | HGT_GNN_compatible_link_prediction_baseline | 9 |
| Hungary | Adidas | True | 2.7831 | 2.8765 | HGT_GNN_compatible_link_prediction_baseline | 10 |
| Netherlands | Adidas | False | 2.7812 | 2.8745 | HGT_GNN_compatible_link_prediction_baseline | 11 |
| Ukraine | Adidas | False | 2.7788 | 2.8720 | HGT_GNN_compatible_link_prediction_baseline | 12 |
| Indonesia | Adidas | False | 2.7772 | 2.8705 | HGT_GNN_compatible_link_prediction_baseline | 13 |
| Denmark | Adidas | True | 2.7708 | 2.8638 | HGT_GNN_compatible_link_prediction_baseline | 14 |
| Argentina | Hyundai | True | 2.7708 | 2.8665 | HGT_GNN_compatible_link_prediction_baseline | 14 |