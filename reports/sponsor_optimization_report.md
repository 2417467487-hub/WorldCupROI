# Sponsor Strategy Optimization Report

This module upgrades ROI prediction into budget-constrained sponsor allocation.

## Optimized Allocation

| allocation_rank | sponsor | team | stage | allocated_budget_m | expected_roi | utility_per_m |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Vivo | Slovenia | group_or_knockout | 14.76 | 3.2773 | 0.1329 |
| 2 | Mengniu | Bosnia and Herzegovina | group_or_knockout | 16.77 | 3.6557 | 0.1308 |
| 3 | McDonald's | Ecuador | group_or_knockout | 16.55 | 3.544 | 0.1297 |
| 4 | Mengniu | Turkey | tournament | 18.0 | 3.7177 | 0.1235 |
| 5 | Mengniu | Slovakia | group_or_knockout | 15.95 | 3.2722 | 0.1233 |
| 6 | Qatar Airways | Yugoslavia | group_or_knockout | 17.82 | 3.5922 | 0.1207 |
| 7 | Mengniu | Portugal | group_or_knockout | 17.76 | 3.4379 | 0.1179 |

## Multi-Armed Bandit Baseline

| sponsor | team | stage | expected_roi | ucb_score |
| --- | --- | --- | --- | --- |
| Hyundai | Russia | group_or_knockout | 4.053 | 2.5278 |
| Coca-Cola | Germany | group_or_knockout | 3.9293 | 2.46 |
| Visa | Belgium | group_or_knockout | 3.8522 | 2.423 |
| Hyundai | Mexico | group_or_knockout | 3.8088 | 2.3752 |
| McDonald's | New Zealand | tournament | 3.9337 | 2.3739 |
| Mengniu | Bosnia and Herzegovina | group_or_knockout | 3.6557 | 2.3655 |
| Mengniu | Turkey | tournament | 3.7177 | 2.3443 |
| Adidas | North Korea | group_or_knockout | 3.77 | 2.317 |
| Mengniu | Turkey | group_or_knockout | 3.6483 | 2.3152 |
| Visa | Saudi Arabia | group_or_knockout | 3.7425 | 2.3079 |

## Upgrade Path

- Bayesian Optimization: tune spend and exposure jointly under budget and risk constraints.
- Contextual Bandit: learn sponsor allocation by team, stage, media heat and fan response.
- Portfolio Optimization: add concentration limits and downside ROI probability constraints.