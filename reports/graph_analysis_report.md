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
| sponsor:Hyundai | sponsor | 262 | 1024.272 | 0.042622 | 0.000305 | 0.310417 |
| sponsor:Coca-Cola | sponsor | 235 | 912.955 | 0.037973 | 0.000257 | 0.303116 |
| sponsor:Adidas | sponsor | 233 | 899.006 | 0.037632 | 0.000768 | 0.303346 |
| sponsor:Visa | sponsor | 236 | 886.688 | 0.037307 | 0.00072 | 0.304502 |
| sponsor:Hisense | sponsor | 185 | 688.56 | 0.029092 | 0.000491 | 0.29193 |
| sponsor:Budweiser | sponsor | 183 | 666.82 | 0.028419 | 0.002216 | 0.292144 |
| sponsor:McDonald's | sponsor | 187 | 650.121 | 0.028115 | 0.013172 | 0.292357 |
| sponsor:Qatar Airways | sponsor | 163 | 604.204 | 0.025816 | 0.000396 | 0.286796 |
| sponsor:Vivo | sponsor | 152 | 521.768 | 0.022846 | 0.01153 | 0.284752 |
| sponsor:Mengniu | sponsor | 98 | 323.016 | 0.014637 | 0.009675 | 0.273447 |

## Top GCN / GraphSAGE Baseline Nodes

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sponsor:Hyundai | sponsor | 0.296904 | 0.591577 | 0.458974 | 0.667283 | 0.668377 | 0.025295 | 0.934344 |
| sponsor:Adidas | sponsor | 0.284529 | 0.536526 | 0.423128 | 0.5914 | 0.595773 | 0.03714 | 0.917236 |
| sponsor:Coca-Cola | sponsor | 0.280435 | 0.538863 | 0.422571 | 0.599159 | 0.600037 | 0.022214 | 0.916854 |
| sponsor:Visa | sponsor | 0.28276 | 0.531649 | 0.419649 | 0.58341 | 0.590577 | 0.036767 | 0.920366 |
| match_370 | match | 0.560576 | 0.299498 | 0.416983 | 0.290653 | 0.292163 | 0.019505 | 0.808715 |
| match_390 | match | 0.556764 | 0.297169 | 0.413987 | 0.287846 | 0.289313 | 0.017953 | 0.808799 |
| match_923 | match | 0.553655 | 0.296044 | 0.411969 | 0.286016 | 0.287444 | 0.019106 | 0.809357 |
| match_950 | match | 0.552578 | 0.295633 | 0.411258 | 0.284063 | 0.285343 | 0.025516 | 0.809854 |
| match_853 | match | 0.550391 | 0.29412 | 0.409442 | 0.284211 | 0.285628 | 0.015642 | 0.809046 |
| match_10 | match | 0.55026 | 0.294188 | 0.40942 | 0.282226 | 0.283499 | 0.025006 | 0.809829 |