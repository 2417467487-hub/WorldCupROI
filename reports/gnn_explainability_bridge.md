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
| sponsor:Coca-Cola | sponsor | 0.302217 | 0.591623 | 0.461391 | 0.656058 | 0.667406 | 0.0592 | 0.934913 |
| sponsor:Adidas | sponsor | 0.298936 | 0.592834 | 0.46058 | 0.668131 | 0.66931 | 0.03058 | 0.931937 |
| sponsor:Visa | sponsor | 0.296199 | 0.567602 | 0.445471 | 0.628015 | 0.637437 | 0.046372 | 0.928129 |
| sponsor:Hyundai | sponsor | 0.285392 | 0.534516 | 0.42241 | 0.588913 | 0.591775 | 0.038269 | 0.917957 |
| sponsor:Hisense | sponsor | 0.264911 | 0.474329 | 0.380091 | 0.5072 | 0.51698 | 0.037991 | 0.901841 |
| sponsor:Budweiser | sponsor | 0.259197 | 0.445331 | 0.361571 | 0.471607 | 0.478553 | 0.031701 | 0.893251 |
| sponsor:Qatar Airways | sponsor | 0.260075 | 0.443421 | 0.360915 | 0.468016 | 0.474622 | 0.03825 | 0.891192 |
| sponsor:Vivo | sponsor | 0.255326 | 0.440621 | 0.357238 | 0.432313 | 0.446634 | 0.17561 | 0.886019 |
| sponsor:McDonald's | sponsor | 0.246798 | 0.396602 | 0.32919 | 0.385819 | 0.400854 | 0.119955 | 0.876931 |
| sponsor:Mengniu | sponsor | 0.233177 | 0.366939 | 0.306746 | 0.346182 | 0.361199 | 0.124635 | 0.866179 |

## Top GCN / GraphSAGE Player Nodes

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Brazil team_attack_unit | player | 0.020249 | 0.015031 | 0.017379 | 0.012096 | 0.024099 | 0.000423 | 0.02652 |
| Brazil team_midfield_unit | player | 0.020249 | 0.014891 | 0.017302 | 0.011943 | 0.023848 | 0.000423 | 0.02652 |
| Germany team_defense_unit | player | 0.019659 | 0.01501 | 0.017102 | 0.011597 | 0.024832 | 0.000428 | 0.026537 |
| Switzerland team_defense_unit | player | 0.019901 | 0.01467 | 0.017024 | 0.012712 | 0.022824 | 0.000362 | 0.023742 |
| Switzerland team_midfield_unit | player | 0.019901 | 0.014 | 0.016655 | 0.01195 | 0.021681 | 0.000362 | 0.023742 |
| Netherlands team_defense_unit | player | 0.01974 | 0.014053 | 0.016612 | 0.01144 | 0.022692 | 0.00037 | 0.023773 |
| Sweden team_attack_unit | player | 0.019235 | 0.014347 | 0.016547 | 0.011701 | 0.023326 | 0.000365 | 0.023755 |
| Russia team_defense_unit | player | 0.018976 | 0.014376 | 0.016446 | 0.011361 | 0.023974 | 0.000371 | 0.023778 |
| Denmark team_defense_unit | player | 0.018855 | 0.014034 | 0.016204 | 0.01044 | 0.023256 | 0.000425 | 0.026524 |
| Netherlands team_attack_unit | player | 0.01974 | 0.013259 | 0.016175 | 0.010579 | 0.021271 | 0.00037 | 0.023773 |

## NetworkX Sponsor Influence

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

## NetworkX Player Influence

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

## Bridge to SHAP-Style ROI Drivers

| feature_group | importance_sum | top_feature | feature_count |
| --- | --- | --- | --- |
| sponsor_activation | 0.303772 | a_ad_exposure_m | 8 |
| media_attention | 0.143641 | fan_score | 6 |
| team_strength | 0.139618 | team_a_strength | 2 |
| business_intelligence_indices | 0.11758 | commercial_momentum_score | 6 |
| player_influence | 0.067991 | a_core_market_value_m | 5 |
| venue_weather | 0.020297 | host_advantage_a | 1 |
| injury_availability | 0.017669 | a_avg_availability_score | 2 |
| text_sentiment | 0.015947 | news_sentiment_score | 2 |

## Interpretation

- SHAP-style ROI drivers explain tabular commercial lift; graph scores explain relationship position and indirect influence.
- A sponsor with high SHAP-linked brand fit but low graph influence may need partnership expansion.
- A sponsor with high graph influence but weaker ROI drivers may be overexposed without enough conversion quality.
- Production GCN/GraphSAGE should replace this deterministic baseline only after licensed sponsor conversion labels are available.