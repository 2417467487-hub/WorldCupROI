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
| sponsor:Adidas | 246 | 1181.877 | 2.3638 | 0.039471 | 0.000798 | 0.306554 |
| sponsor:Coca-Cola | 253 | 1127.993 | 2.2118 | 0.039392 | 0.002738 | 0.307841 |
| sponsor:Visa | 239 | 1092.408 | 2.2664 | 0.037438 | 0.0013 | 0.304817 |
| sponsor:Hyundai | 220 | 1014.342 | 2.3265 | 0.034533 | 0.000943 | 0.300501 |
| sponsor:Hisense | 194 | 840.322 | 2.1883 | 0.0298 | 0.00237 | 0.294467 |
| sponsor:Budweiser | 177 | 777.636 | 2.2346 | 0.027287 | 0.001297 | 0.290542 |
| sponsor:Qatar Airways | 174 | 768.503 | 2.2471 | 0.027033 | 0.001549 | 0.289915 |
| sponsor:Vivo | 170 | 654.003 | 1.9581 | 0.025342 | 0.020464 | 0.289188 |
| sponsor:McDonald's | 151 | 571.764 | 1.9581 | 0.022303 | 0.012939 | 0.284998 |
| sponsor:Mengniu | 134 | 507.249 | 1.951 | 0.019882 | 0.014714 | 0.281418 |

## Top Player Commercial Influence

| source | connected_teams | player_commercial_influence | avg_influence | pagerank | betweenness | closeness |
| --- | --- | --- | --- | --- | --- | --- |
| Switzerland team_defense_unit | 1 | 8.396 | 8.396 | 0.000644 | 0.0 | 0.006526 |
| Germany team_defense_unit | 1 | 8.364 | 8.364 | 0.000753 | 0.0 | 0.007284 |
| Brazil team_attack_unit | 1 | 8.21 | 8.21 | 0.000694 | 0.0 | 0.007284 |
| Russia team_defense_unit | 1 | 8.072 | 8.072 | 0.00072 | 0.0 | 0.006526 |
| Sweden team_attack_unit | 1 | 8.013 | 8.013 | 0.000679 | 0.0 | 0.006526 |
| Brazil team_midfield_unit | 1 | 7.952 | 7.952 | 0.000676 | 0.0 | 0.007284 |
| Colombia team_midfield_unit | 1 | 7.73 | 7.73 | 0.000737 | 0.0 | 0.006526 |
| Denmark team_defense_unit | 1 | 7.171 | 7.171 | 0.000678 | 0.0 | 0.007284 |
| England team_defense_unit | 1 | 7.14 | 7.14 | 0.000686 | 0.0 | 0.006526 |
| Netherlands team_defense_unit | 1 | 7.114 | 7.114 | 0.000607 | 0.0 | 0.006526 |

## Top Network Centrality

| node | node_type | degree | weighted_degree | pagerank | betweenness | closeness |
| --- | --- | --- | --- | --- | --- | --- |
| sponsor:Adidas | sponsor | 246 | 927.416 | 0.039471 | 0.000798 | 0.306554 |
| sponsor:Coca-Cola | sponsor | 253 | 910.462 | 0.039392 | 0.002738 | 0.307841 |
| sponsor:Visa | sponsor | 239 | 867.482 | 0.037438 | 0.0013 | 0.304817 |
| sponsor:Hyundai | sponsor | 220 | 808.922 | 0.034533 | 0.000943 | 0.300501 |
| sponsor:Hisense | sponsor | 194 | 687.414 | 0.0298 | 0.00237 | 0.294467 |
| sponsor:Budweiser | sponsor | 177 | 632.555 | 0.027287 | 0.001297 | 0.290542 |
| sponsor:Qatar Airways | sponsor | 174 | 627.124 | 0.027033 | 0.001549 | 0.289915 |
| sponsor:Vivo | sponsor | 170 | 575.851 | 0.025342 | 0.020464 | 0.289188 |
| sponsor:McDonald's | sponsor | 151 | 503.418 | 0.022303 | 0.012939 | 0.284998 |
| sponsor:Mengniu | sponsor | 134 | 446.62 | 0.019882 | 0.014714 | 0.281418 |

## Top GCN / GraphSAGE Baseline Nodes

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sponsor:Coca-Cola | sponsor | 0.302217 | 0.591623 | 0.461391 | 0.656058 | 0.667406 | 0.0592 | 0.934913 |
| sponsor:Adidas | sponsor | 0.298936 | 0.592834 | 0.46058 | 0.668131 | 0.66931 | 0.03058 | 0.931937 |
| sponsor:Visa | sponsor | 0.296199 | 0.567602 | 0.445471 | 0.628015 | 0.637437 | 0.046372 | 0.928129 |
| sponsor:Hyundai | sponsor | 0.285392 | 0.534516 | 0.42241 | 0.588913 | 0.591775 | 0.038269 | 0.917957 |
| match_41 | match | 0.561099 | 0.306393 | 0.421011 | 0.291066 | 0.294628 | 0.024271 | 0.861232 |
| match_129 | match | 0.559294 | 0.305863 | 0.419907 | 0.288563 | 0.291917 | 0.032531 | 0.861827 |
| match_107 | match | 0.55897 | 0.304983 | 0.419277 | 0.289543 | 0.293019 | 0.022555 | 0.861393 |
| match_383 | match | 0.557249 | 0.305955 | 0.419038 | 0.284337 | 0.287758 | 0.052419 | 0.862011 |
| match_128 | match | 0.55792 | 0.304042 | 0.418288 | 0.288975 | 0.292446 | 0.019352 | 0.861329 |
| match_430 | match | 0.556131 | 0.304279 | 0.417612 | 0.284244 | 0.287807 | 0.042795 | 0.860935 |