# Causal Sports Intelligence Executive Report

## Executive Thesis

WorldCupROI is upgraded from an ROI prediction system into a causal decision and optimization platform. The system now separates correlation from causation, recommends budget allocation, models user behavior pathways, evaluates counterfactual interventions, tracks temporal dynamics and translates graph influence into sponsor strategy.

## Causal Findings

| label | standardized_effect | ci_low | ci_high | method |
| --- | --- | --- | --- | --- |
| Media exposure | 0.2786 | 0.2466 | 0.3106 | backdoor-adjusted OLS baseline |
| Fan influence | 0.3775 | 0.3455 | 0.4095 | backdoor-adjusted OLS baseline |
| Team strength | 0.3106 | 0.2742 | 0.347 | backdoor-adjusted OLS baseline |
| Commercial momentum | 0.688 | 0.661 | 0.7151 | backdoor-adjusted OLS baseline |

## Optimization Recommendations

| allocation_rank | sponsor | team | allocated_budget_m | expected_roi | utility_per_m |
| --- | --- | --- | --- | --- | --- |
| 1 | Vivo | Slovenia | 14.76 | 3.277333333333333 | 0.1329310134217302 |
| 2 | Mengniu | Bosnia and Herzegovina | 16.77 | 3.6556666666666655 | 0.1307936775524361 |
| 3 | McDonald's | Ecuador | 16.55 | 3.544 | 0.1296661248457512 |
| 4 | Mengniu | Turkey | 18.0 | 3.717666666666666 | 0.1234792109904718 |
| 5 | Mengniu | Slovakia | 15.95 | 3.27225 | 0.1233065519791187 |
| 6 | Qatar Airways | Yugoslavia | 17.82 | 3.5922 | 0.1206596608282887 |
| 7 | Mengniu | Portugal | 17.76 | 3.437862068965517 | 0.1179428311457633 |

## User Behavior Funnel

| sponsor | stage | attention_rate | engagement_rate | conversion_rate | predicted_roi |
| --- | --- | --- | --- | --- | --- |
| Adidas | group_or_knockout | 0.6003 | 0.36 | 0.2455 | 3.8192 |
| Adidas | tournament | 0.5789 | 0.351 | 0.2484 | 3.7476 |
| Budweiser | group_or_knockout | 0.6029 | 0.3444 | 0.2369 | 3.6467 |
| Budweiser | tournament | 0.5752 | 0.3252 | 0.2313 | 3.593 |
| Coca-Cola | group_or_knockout | 0.6063 | 0.351 | 0.2521 | 3.7052 |
| Coca-Cola | tournament | 0.5983 | 0.3442 | 0.259 | 3.7659 |
| Hisense | group_or_knockout | 0.6052 | 0.3486 | 0.2469 | 3.6494 |
| Hisense | tournament | 0.5426 | 0.3226 | 0.2344 | 3.465 |

## Counterfactual Risk

| scenario | baseline_roi | counterfactual_roi | roi_delta | roi_low | roi_high |
| --- | --- | --- | --- | --- | --- |
| player_injury_shock | 4.476 | 4.2128 | -0.2632 | 4.0558 | 4.3698 |
| media_surge | 4.476 | 4.704 | 0.228 | 4.561 | 4.847 |
| budget_cut | 4.476 | 4.3356 | -0.1404 | 4.2136 | 4.4576 |
| budget_reallocation | 4.476 | 4.5888 | 0.1128 | 4.4773 | 4.7003 |
| late_stage_activation | 4.476 | 4.6644 | 0.1884 | 4.5319 | 4.7969 |
| player_injury_shock | 4.476 | 4.2128 | -0.2632 | 4.0558 | 4.3698 |
| media_surge | 4.476 | 4.704 | 0.228 | 4.561 | 4.847 |
| budget_cut | 4.476 | 4.3356 | -0.1404 | 4.2136 | 4.4576 |

## Graph Learning

| node | node_type | hgt_influence_proxy |
| --- | --- | --- |
| sponsor:Hyundai | sponsor | 1261.417 |
| sponsor:Adidas | sponsor | 1079.883 |
| sponsor:Coca-Cola | sponsor | 1046.33 |
| sponsor:Visa | sponsor | 1030.583 |
| sponsor:Hisense | sponsor | 787.907 |
| sponsor:Budweiser | sponsor | 775.724 |
| sponsor:McDonald's | sponsor | 725.071 |
| sponsor:Qatar Airways | sponsor | 647.604 |

## Sponsor Investment Recommendations

| sponsor | team | expected_roi | decision_score | risk_level | recommendation |
| --- | --- | --- | --- | --- | --- |
| Hyundai | Argentina | 4.0004 | 2.1141 | low | Scale investment |
| Coca-Cola | Germany | 3.8867 | 2.0628 | low | Scale investment |
| Adidas | Brazil | 3.8687 | 2.0414 | low | Scale investment |
| Visa | Belgium | 3.8204 | 2.035 | low | Scale investment |
| Hyundai | Russia | 3.838 | 2.0197 | low | Scale investment |
| Mengniu | Turkey | 3.6691 | 2.0086 | low | Scale investment |
| Hisense | Croatia | 3.7395 | 1.9972 | low | Scale investment |
| Hyundai | Mexico | 3.7813 | 1.996 | low | Scale investment |
| Adidas | Jamaica | 3.8407 | 1.982 | low | Scale investment |
| Mengniu | Bosnia and Herzegovina | 3.6557 | 1.9778 | low | Scale investment |

## Analyst Recommendation

Use ROI prediction as the forecasting layer, not the final decision. Investment decisions should be made only after checking causal effect direction, funnel conversion efficiency, counterfactual downside and graph influence concentration.