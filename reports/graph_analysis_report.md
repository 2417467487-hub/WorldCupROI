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
| sponsor:Hyundai | 262 | 1198.933 | 2.2368 | 0.041791 | 0.001268 | 0.310417 |
| sponsor:Adidas | 233 | 1135.717 | 2.4267 | 0.038248 | 0.000462 | 0.303346 |
| sponsor:Coca-Cola | 235 | 1052.147 | 2.2386 | 0.037356 | 0.00145 | 0.303116 |
| sponsor:Visa | 236 | 1009.061 | 2.1561 | 0.036576 | 0.002679 | 0.304502 |
| sponsor:Hisense | 185 | 829.779 | 2.2548 | 0.029123 | 0.000843 | 0.29193 |
| sponsor:Budweiser | 183 | 786.83 | 2.1736 | 0.028645 | 0.002091 | 0.292144 |
| sponsor:McDonald's | 187 | 726.997 | 1.9755 | 0.02833 | 0.012944 | 0.292357 |
| sponsor:Qatar Airways | 163 | 649.315 | 1.9918 | 0.024955 | 0.00877 | 0.286796 |
| sponsor:Vivo | 152 | 581.324 | 1.9508 | 0.022934 | 0.011185 | 0.284752 |
| sponsor:Mengniu | 98 | 370.042 | 1.9273 | 0.014771 | 0.009577 | 0.273447 |

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
| sponsor:Hyundai | sponsor | 262 | 956.725 | 0.041791 | 0.001268 | 0.310417 |
| sponsor:Adidas | sponsor | 233 | 888.043 | 0.038248 | 0.000462 | 0.303346 |
| sponsor:Coca-Cola | sponsor | 235 | 857.923 | 0.037356 | 0.00145 | 0.303116 |
| sponsor:Visa | sponsor | 236 | 828.233 | 0.036576 | 0.002679 | 0.304502 |
| sponsor:Hisense | sponsor | 185 | 665.004 | 0.029123 | 0.000843 | 0.29193 |
| sponsor:Budweiser | sponsor | 183 | 650.88 | 0.028645 | 0.002091 | 0.292144 |
| sponsor:McDonald's | sponsor | 187 | 633.662 | 0.02833 | 0.012944 | 0.292357 |
| sponsor:Qatar Airways | sponsor | 163 | 552.654 | 0.024955 | 0.00877 | 0.286796 |
| sponsor:Vivo | sponsor | 152 | 505.65 | 0.022934 | 0.011185 | 0.284752 |
| sponsor:Mengniu | sponsor | 98 | 316.865 | 0.014771 | 0.009577 | 0.273447 |