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
| sponsor:Hyundai | 262 | 1253.053 | 2.3378 | 0.0424 | 0.000303 | 0.310417 |
| sponsor:Adidas | 233 | 1111.494 | 2.375 | 0.037782 | 0.000488 | 0.303346 |
| sponsor:Coca-Cola | 235 | 1049.82 | 2.2337 | 0.037289 | 0.001223 | 0.303116 |
| sponsor:Visa | 236 | 1025.272 | 2.1908 | 0.036782 | 0.001233 | 0.304502 |
| sponsor:Hisense | 185 | 794.249 | 2.1583 | 0.028589 | 0.001524 | 0.29193 |
| sponsor:Budweiser | 183 | 782.731 | 2.1622 | 0.028545 | 0.001779 | 0.292144 |
| sponsor:McDonald's | 187 | 725.708 | 1.972 | 0.028368 | 0.012799 | 0.292357 |
| sponsor:Qatar Airways | 163 | 648.289 | 1.9886 | 0.024983 | 0.008504 | 0.286796 |
| sponsor:Vivo | 152 | 580.812 | 1.949 | 0.022979 | 0.01103 | 0.284752 |
| sponsor:Mengniu | 98 | 367.986 | 1.9166 | 0.014767 | 0.009589 | 0.273447 |

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
| sponsor:Hyundai | sponsor | 262 | 972.246 | 0.0424 | 0.000303 | 0.310417 |
| sponsor:Adidas | sponsor | 233 | 866.056 | 0.037782 | 0.000488 | 0.303346 |
| sponsor:Coca-Cola | sponsor | 235 | 850.747 | 0.037289 | 0.001223 | 0.303116 |
| sponsor:Visa | sponsor | 236 | 830.813 | 0.036782 | 0.001233 | 0.304502 |
| sponsor:Hisense | sponsor | 185 | 642.457 | 0.028589 | 0.001524 | 0.29193 |
| sponsor:Budweiser | sponsor | 183 | 643.441 | 0.028545 | 0.001779 | 0.292144 |
| sponsor:McDonald's | sponsor | 187 | 631.633 | 0.028368 | 0.012799 | 0.292357 |
| sponsor:Qatar Airways | sponsor | 163 | 550.901 | 0.024983 | 0.008504 | 0.286796 |
| sponsor:Vivo | sponsor | 152 | 504.559 | 0.022979 | 0.01103 | 0.284752 |
| sponsor:Mengniu | sponsor | 98 | 314.679 | 0.014767 | 0.009589 | 0.273447 |