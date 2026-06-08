# GNN Baseline and SHAP Bridge

## Purpose

This baseline upgrades graph intelligence from centrality-only reporting to a reproducible graph-modeling layer. It is intentionally lightweight so `--demo` and CI can run without external APIs or PyTorch Geometric.

## Baseline Design

- Node features: weighted degree, PageRank, betweenness, and closeness.
- GCN-style score: normalized weighted adjacency propagation over centrality features.
- GraphSAGE-style score: self features plus first-hop and second-hop weighted neighbor aggregation.
- Output label proxy: `combined_graph_score`, used as a sponsor/player influence prior rather than a supervised production GNN.

## Top GCN / GraphSAGE Sponsor Nodes

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sponsor:Hyundai | sponsor | 0.296904 | 0.591577 | 0.458974 | 0.667283 | 0.668377 | 0.025295 | 0.934344 |
| sponsor:Adidas | sponsor | 0.284529 | 0.536526 | 0.423128 | 0.5914 | 0.595773 | 0.03714 | 0.917236 |
| sponsor:Coca-Cola | sponsor | 0.280435 | 0.538863 | 0.422571 | 0.599159 | 0.600037 | 0.022214 | 0.916854 |
| sponsor:Visa | sponsor | 0.28276 | 0.531649 | 0.419649 | 0.58341 | 0.590577 | 0.036767 | 0.920366 |
| sponsor:Hisense | sponsor | 0.253007 | 0.437633 | 0.354551 | 0.464103 | 0.471604 | 0.019866 | 0.889173 |
| sponsor:McDonald's | sponsor | 0.249224 | 0.434102 | 0.350907 | 0.439202 | 0.455811 | 0.097936 | 0.887715 |
| sponsor:Budweiser | sponsor | 0.248246 | 0.429304 | 0.347828 | 0.449568 | 0.460505 | 0.029625 | 0.888217 |
| sponsor:Qatar Airways | sponsor | 0.244893 | 0.400505 | 0.330479 | 0.413511 | 0.42449 | 0.023883 | 0.876116 |
| sponsor:Vivo | sponsor | 0.230291 | 0.372381 | 0.308441 | 0.360857 | 0.378594 | 0.085211 | 0.867464 |
| sponsor:Mengniu | sponsor | 0.201062 | 0.277339 | 0.243014 | 0.239365 | 0.258139 | 0.070584 | 0.836587 |

## Top GCN / GraphSAGE Player Nodes

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Spain team_attack_unit | player | 0.018517 | 0.014803 | 0.016474 | 0.012212 | 0.02417 | 0.000305 | 0.023692 |
| Uruguay team_attack_unit | player | 0.018976 | 0.014028 | 0.016255 | 0.011778 | 0.022115 | 0.000305 | 0.023692 |
| Uruguay team_defense_unit | player | 0.018976 | 0.013372 | 0.015894 | 0.011052 | 0.020966 | 0.000305 | 0.023692 |
| Denmark team_defense_unit | player | 0.018126 | 0.013632 | 0.015655 | 0.010436 | 0.0219 | 0.00035 | 0.026438 |
| Brazil team_midfield_unit | player | 0.017928 | 0.013736 | 0.015622 | 0.010121 | 0.022771 | 0.000358 | 0.026472 |
| Switzerland team_attack_unit | player | 0.017744 | 0.013732 | 0.015537 | 0.010087 | 0.022814 | 0.000357 | 0.026466 |
| France team_midfield_unit | player | 0.018119 | 0.013292 | 0.015464 | 0.010065 | 0.02229 | 0.00031 | 0.023715 |
| Argentina team_defense_unit | player | 0.017741 | 0.013596 | 0.015461 | 0.010622 | 0.022457 | 0.000311 | 0.023717 |
| Germany team_midfield_unit | player | 0.01781 | 0.013385 | 0.015376 | 0.009642 | 0.022298 | 0.000361 | 0.026483 |
| Croatia team_midfield_unit | player | 0.017679 | 0.01326 | 0.015249 | 0.010369 | 0.021677 | 0.000309 | 0.023711 |

## NetworkX Sponsor Influence

| source | connected_nodes | sponsor_influence | avg_edge_weight | pagerank | betweenness | closeness |
| --- | --- | --- | --- | --- | --- | --- |
| sponsor:Hyundai | 262 | 1307.498 | 2.4394 | 0.042622 | 0.000305 | 0.310417 |
| sponsor:Adidas | 233 | 1136.814 | 2.4291 | 0.037632 | 0.000768 | 0.303346 |
| sponsor:Coca-Cola | 235 | 1136.317 | 2.4177 | 0.037973 | 0.000257 | 0.303116 |
| sponsor:Visa | 236 | 1098.354 | 2.3469 | 0.037307 | 0.00072 | 0.304502 |
| sponsor:Hisense | 185 | 860.286 | 2.3377 | 0.029092 | 0.000491 | 0.29193 |
| sponsor:Budweiser | 183 | 801.59 | 2.2143 | 0.028419 | 0.002216 | 0.292144 |
| sponsor:Qatar Airways | 163 | 762.458 | 2.3388 | 0.025816 | 0.000396 | 0.286796 |
| sponsor:McDonald's | 187 | 743.355 | 2.02 | 0.028115 | 0.013172 | 0.292357 |
| sponsor:Vivo | 152 | 597.471 | 2.0049 | 0.022846 | 0.01153 | 0.284752 |
| sponsor:Mengniu | 98 | 376.205 | 1.9594 | 0.014637 | 0.009675 | 0.273447 |

## NetworkX Player Influence

| source | connected_teams | player_commercial_influence | avg_influence | pagerank | betweenness | closeness |
| --- | --- | --- | --- | --- | --- | --- |
| Spain team_attack_unit | 1 | 10.417 | 10.417 | 0.000842 | 0.0 | 0.006563 |
| Uruguay team_attack_unit | 1 | 8.684 | 8.684 | 0.000678 | 0.0 | 0.006563 |
| Argentina team_defense_unit | 1 | 8.479 | 8.479 | 0.000739 | 0.0 | 0.006563 |
| Switzerland team_attack_unit | 1 | 8.226 | 8.226 | 0.000765 | 0.0 | 0.007326 |
| Brazil team_midfield_unit | 1 | 8.108 | 8.108 | 0.000752 | 0.0 | 0.007326 |
| Denmark team_defense_unit | 1 | 7.995 | 7.995 | 0.000695 | 0.0 | 0.007326 |
| Croatia team_midfield_unit | 1 | 7.929 | 7.929 | 0.000688 | 0.0 | 0.006563 |
| Austria team_attack_unit | 1 | 7.539 | 7.539 | 0.000797 | 0.0 | 0.006563 |
| Germany team_midfield_unit | 1 | 7.469 | 7.469 | 0.000714 | 0.0 | 0.007326 |
| Hungary team_defense_unit | 1 | 7.461 | 7.461 | 0.000704 | 0.0 | 0.007326 |

## Bridge to SHAP-Style ROI Drivers

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.508117 | a_brand_heat_index | 8 |
| team_strength | 0.157933 | team_a_strength | 2 |
| business_intelligence_indices | 0.139516 | sponsor_team_fit_score | 6 |
| media_attention | 0.121553 | fan_score | 6 |
| player_influence | 0.078465 | a_player_followers_m | 5 |
| text_sentiment | 0.035528 | text_signal_score | 2 |
| venue_weather | 0.01805 | host_advantage_a | 1 |
| injury_availability | 0.012089 | a_avg_injury_risk | 2 |

## Interpretation

- SHAP-style ROI drivers explain tabular commercial lift; graph scores explain relationship position and indirect influence.
- A sponsor with high SHAP-linked brand fit but low graph influence may need partnership expansion.
- A sponsor with high graph influence but weaker ROI drivers may be overexposed without enough conversion quality.
- Production GCN/GraphSAGE should replace this deterministic baseline only after licensed sponsor conversion labels are available.