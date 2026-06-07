# Graph Analysis Report

Team-player-sponsor-match relationships are represented as a weighted graph.

## Graph Intelligence Upgrade

- NetworkX centrality is used for degree, weighted degree, PageRank, betweenness, and closeness.
- Sponsor Influence combines sponsor-team, sponsor-match exposure, and centrality signals.
- Player Influence uses player-team edges and is ready to be joined with player availability or injury feeds.
- GCN / GraphSAGE baseline placeholder: use this edge list as a heterogeneous graph where node features come from team profile, player profile, sponsor attributes, and match context. Candidate labels are sponsor conversion proxy, ROI lift, or high-risk scenario flag.

## Top Sponsor Influence

| source | connected_nodes | sponsor_influence | avg_edge_weight | pagerank | betweenness | closeness |
| --- | --- | --- | --- | --- | --- | --- |
| sponsor:Hyundai | 262 | 1244.283 | 2.3214 | 0.042276 | 0.000309 | 0.310417 |
| sponsor:Adidas | 233 | 1107.369 | 2.3662 | 0.037711 | 0.00047 | 0.303346 |
| sponsor:Coca-Cola | 235 | 1052.637 | 2.2397 | 0.037335 | 0.001105 | 0.303116 |
| sponsor:Visa | 236 | 1015.704 | 2.1703 | 0.03664 | 0.001399 | 0.304502 |
| sponsor:Hisense | 185 | 799.936 | 2.1737 | 0.028665 | 0.001115 | 0.29193 |
| sponsor:Budweiser | 183 | 786.948 | 2.1739 | 0.0286 | 0.001507 | 0.292144 |
| sponsor:McDonald's | 187 | 725.069 | 1.9703 | 0.028382 | 0.012697 | 0.292357 |
| sponsor:Qatar Airways | 163 | 647.848 | 1.9873 | 0.025 | 0.008462 | 0.286796 |
| sponsor:Vivo | 152 | 580.338 | 1.9474 | 0.022989 | 0.010975 | 0.284752 |
| sponsor:Mengniu | 98 | 367.795 | 1.9156 | 0.01478 | 0.009563 | 0.273447 |

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
| sponsor:Hyundai | sponsor | 262 | 965.545 | 0.042276 | 0.000309 | 0.310417 |
| sponsor:Adidas | sponsor | 233 | 861.446 | 0.037711 | 0.00047 | 0.303346 |
| sponsor:Coca-Cola | sponsor | 235 | 850.251 | 0.037335 | 0.001105 | 0.303116 |
| sponsor:Visa | sponsor | 236 | 823.834 | 0.03664 | 0.001399 | 0.304502 |
| sponsor:Hisense | sponsor | 185 | 643.427 | 0.028665 | 0.001115 | 0.29193 |
| sponsor:Budweiser | sponsor | 183 | 643.73 | 0.0286 | 0.001507 | 0.292144 |
| sponsor:McDonald's | sponsor | 187 | 630.562 | 0.028382 | 0.012697 | 0.292357 |
| sponsor:Qatar Airways | sponsor | 163 | 550.108 | 0.025 | 0.008462 | 0.286796 |
| sponsor:Vivo | sponsor | 152 | 503.732 | 0.022989 | 0.010975 | 0.284752 |
| sponsor:Mengniu | sponsor | 98 | 314.433 | 0.01478 | 0.009563 | 0.273447 |