# Graph Analysis Report

Team-player-sponsor-match relationships are represented as a weighted graph.

## Graph Intelligence Upgrade

- NetworkX centrality is used for degree, weighted degree, PageRank, betweenness, and closeness.
- Sponsor Influence combines sponsor-team, sponsor-match exposure, and centrality signals.
- Player Influence uses player-team edges and is ready to be joined with player availability or injury feeds.
- GCN / GraphSAGE baseline: deterministic two-hop weighted propagation over centrality features, producing `reports/gnn_baseline_node_scores.csv`.
- SHAP bridge: `reports/gnn_explainability_bridge.md` connects graph influence to tabular ROI driver explanations.

## Top Sponsor Influence

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

## Top Player Commercial Influence

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

## Top Network Centrality

| node | node_type | degree | weighted_degree | pagerank | betweenness | closeness |
| --- | --- | --- | --- | --- | --- | --- |
| sponsor:Hyundai | sponsor | 262 | 1018.259 | 0.0423 | 0.000339 | 0.310417 |
| sponsor:Coca-Cola | sponsor | 235 | 923.755 | 0.038128 | 0.000137 | 0.303116 |
| sponsor:Adidas | sponsor | 233 | 899.095 | 0.037488 | 0.00071 | 0.303346 |
| sponsor:Visa | sponsor | 236 | 889.534 | 0.037248 | 0.000464 | 0.304502 |
| sponsor:Hisense | sponsor | 185 | 693.459 | 0.029128 | 0.000294 | 0.29193 |
| sponsor:Budweiser | sponsor | 183 | 692.192 | 0.029011 | 0.000527 | 0.292144 |
| sponsor:McDonald's | sponsor | 187 | 652.361 | 0.028072 | 0.013263 | 0.292357 |
| sponsor:Qatar Airways | sponsor | 163 | 609.262 | 0.025864 | 0.000358 | 0.286796 |
| sponsor:Vivo | sponsor | 152 | 525.303 | 0.022854 | 0.011549 | 0.284752 |
| sponsor:Mengniu | sponsor | 98 | 325.213 | 0.014644 | 0.009753 | 0.273447 |

## Top GCN / GraphSAGE Baseline Nodes

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sponsor:Hyundai | sponsor | 0.297283 | 0.591777 | 0.459255 | 0.667633 | 0.668555 | 0.025279 | 0.934261 |
| sponsor:Coca-Cola | sponsor | 0.283463 | 0.545728 | 0.427708 | 0.609817 | 0.607142 | 0.021853 | 0.917156 |
| sponsor:Adidas | sponsor | 0.285922 | 0.538941 | 0.425082 | 0.595246 | 0.598215 | 0.036852 | 0.917306 |
| sponsor:Visa | sponsor | 0.28456 | 0.535037 | 0.422322 | 0.588914 | 0.594271 | 0.035558 | 0.920516 |
| match_370 | match | 0.560123 | 0.299262 | 0.41665 | 0.29033 | 0.291858 | 0.019534 | 0.808643 |
| match_390 | match | 0.556257 | 0.296919 | 0.413621 | 0.287484 | 0.28898 | 0.018055 | 0.808728 |
| match_923 | match | 0.552988 | 0.295706 | 0.411483 | 0.285547 | 0.286985 | 0.019182 | 0.809291 |
| match_950 | match | 0.551991 | 0.295342 | 0.410834 | 0.283616 | 0.28492 | 0.02576 | 0.809799 |
| match_853 | match | 0.5498 | 0.29383 | 0.409017 | 0.283793 | 0.285228 | 0.015772 | 0.808979 |
| match_10 | match | 0.549579 | 0.293854 | 0.40893 | 0.281713 | 0.283009 | 0.025288 | 0.809771 |