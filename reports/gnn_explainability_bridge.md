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
| sponsor:Hyundai | sponsor | 0.297283 | 0.591777 | 0.459255 | 0.667633 | 0.668555 | 0.025279 | 0.934261 |
| sponsor:Coca-Cola | sponsor | 0.283463 | 0.545728 | 0.427708 | 0.609817 | 0.607142 | 0.021853 | 0.917156 |
| sponsor:Adidas | sponsor | 0.285922 | 0.538941 | 0.425082 | 0.595246 | 0.598215 | 0.036852 | 0.917306 |
| sponsor:Visa | sponsor | 0.28456 | 0.535037 | 0.422322 | 0.588914 | 0.594271 | 0.035558 | 0.920516 |
| sponsor:Hisense | sponsor | 0.254748 | 0.441387 | 0.357399 | 0.470079 | 0.475719 | 0.018828 | 0.889367 |
| sponsor:Budweiser | sponsor | 0.252457 | 0.43992 | 0.355561 | 0.468215 | 0.472962 | 0.020089 | 0.888974 |
| sponsor:McDonald's | sponsor | 0.250609 | 0.436888 | 0.353062 | 0.443457 | 0.458675 | 0.098117 | 0.887696 |
| sponsor:Qatar Airways | sponsor | 0.246705 | 0.404302 | 0.333384 | 0.419314 | 0.428438 | 0.02391 | 0.876292 |
| sponsor:Vivo | sponsor | 0.231743 | 0.375313 | 0.310706 | 0.365469 | 0.381645 | 0.084963 | 0.867421 |
| sponsor:Mengniu | sponsor | 0.202351 | 0.279401 | 0.244728 | 0.242479 | 0.260296 | 0.070753 | 0.836575 |

## Top GCN / GraphSAGE Player Nodes

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Spain team_attack_unit | player | 0.018627 | 0.014888 | 0.01657 | 0.012285 | 0.024354 | 0.000304 | 0.023692 |
| Uruguay team_attack_unit | player | 0.019089 | 0.014107 | 0.016349 | 0.011848 | 0.022283 | 0.000304 | 0.023692 |
| Uruguay team_defense_unit | player | 0.019089 | 0.013447 | 0.015986 | 0.011117 | 0.021126 | 0.000304 | 0.023692 |
| Denmark team_defense_unit | player | 0.018231 | 0.013707 | 0.015743 | 0.010497 | 0.022067 | 0.000349 | 0.026438 |
| Brazil team_midfield_unit | player | 0.018032 | 0.013812 | 0.015711 | 0.01018 | 0.022944 | 0.000357 | 0.026472 |
| Switzerland team_attack_unit | player | 0.017846 | 0.013807 | 0.015625 | 0.010146 | 0.022988 | 0.000356 | 0.026466 |
| France team_midfield_unit | player | 0.018227 | 0.013367 | 0.015554 | 0.010124 | 0.02246 | 0.000309 | 0.023715 |
| Argentina team_defense_unit | player | 0.017845 | 0.013672 | 0.01555 | 0.010685 | 0.022628 | 0.00031 | 0.023717 |
| Germany team_midfield_unit | player | 0.017913 | 0.013459 | 0.015463 | 0.009699 | 0.022468 | 0.00036 | 0.026483 |
| Croatia team_midfield_unit | player | 0.017783 | 0.013334 | 0.015336 | 0.01043 | 0.021842 | 0.000308 | 0.023711 |

## NetworkX Sponsor Influence

| source | connected_nodes | sponsor_influence | avg_edge_weight | pagerank | betweenness | closeness |
| --- | --- | --- | --- | --- | --- | --- |
| sponsor:Hyundai | 262 | 1295.818 | 2.4176 | 0.0423 | 0.000339 | 0.310417 |
| sponsor:Coca-Cola | 235 | 1160.19 | 2.4685 | 0.038128 | 0.000137 | 0.303116 |
| sponsor:Adidas | 233 | 1139.384 | 2.4346 | 0.037488 | 0.00071 | 0.303346 |
| sponsor:Visa | 236 | 1107.365 | 2.3662 | 0.037248 | 0.000464 | 0.304502 |
| sponsor:Hisense | 185 | 872.702 | 2.3715 | 0.029128 | 0.000294 | 0.29193 |
| sponsor:Budweiser | 183 | 855.746 | 2.3639 | 0.029011 | 0.000527 | 0.292144 |
| sponsor:Qatar Airways | 163 | 773.688 | 2.3733 | 0.025864 | 0.000358 | 0.286796 |
| sponsor:McDonald's | 187 | 745.719 | 2.0264 | 0.028072 | 0.013263 | 0.292357 |
| sponsor:Vivo | 152 | 601.024 | 2.0169 | 0.022854 | 0.011549 | 0.284752 |
| sponsor:Mengniu | 98 | 378.481 | 1.9713 | 0.014644 | 0.009753 | 0.273447 |

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
| sponsor_activation | 0.492464 | a_sponsor_spend_m | 8 |
| team_strength | 0.175457 | team_a_strength | 2 |
| business_intelligence_indices | 0.129332 | commercial_momentum_score | 6 |
| media_attention | 0.12327 | fan_score | 6 |
| player_influence | 0.087321 | a_core_market_value_m | 5 |
| text_sentiment | 0.034823 | text_signal_score | 2 |
| venue_weather | 0.01929 | host_advantage_a | 1 |
| injury_availability | 0.011607 | a_avg_injury_risk | 2 |

## Interpretation

- SHAP-style ROI drivers explain tabular commercial lift; graph scores explain relationship position and indirect influence.
- A sponsor with high SHAP-linked brand fit but low graph influence may need partnership expansion.
- A sponsor with high graph influence but weaker ROI drivers may be overexposed without enough conversion quality.
- Production GCN/GraphSAGE should replace this deterministic baseline only after licensed sponsor conversion labels are available.