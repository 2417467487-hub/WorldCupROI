# Deep Analysis Landing Report

## Executive Summary

WorldCupROI now includes dynamic ROI forecasting, sentiment-event impact analysis, budget/media optimization, graph attention-style influence scoring, extreme scenario stress tests, and integrated commercial decision metrics.

## Key Figures

| Figure | Business question |
| --- | --- |
| ![Future ROI](../assets/figures/future_roi_trend.png) | How is sponsor ROI expected to evolve across future World Cup cycles? |
| ![Sentiment Event Impact](../assets/figures/sentiment_event_roi_impact.png) | Which attention and sentiment events move ROI up or down? |
| ![Budget Sensitivity](../assets/figures/budget_media_sensitivity.png) | Which budget/media mix maximizes risk-adjusted ROI? |
| ![Graph Attention](../assets/figures/graph_attention_roi_contribution.png) | Which sponsor nodes contribute most through graph influence? |
| ![Extreme Scenarios](../assets/figures/extreme_scenario_roi_intervals.png) | How do injury, sentiment, policy, and viral shocks change ROI risk? |
| ![Commercial Scorecard](../assets/figures/commercial_decision_scorecard.png) | Which opportunities score best across ROI and business metrics? |

## Future ROI Forecast

| cycle | forecast_roi | trend_slope_per_cycle | forecast_note |
| --- | --- | --- | --- |
| 2026 | 3.7201 | 0.0048 | linear trend over historical/proxy sponsorship panel |
| 2030 | 3.7249 | 0.0048 | linear trend over historical/proxy sponsorship panel |
| 2034 | 3.7297 | 0.0048 | linear trend over historical/proxy sponsorship panel |

## Sentiment Event Impact

| event_type | stage | avg_roi_delta | avg_roi | avg_attention_sentiment | avg_conversion | samples |
| --- | --- | --- | --- | --- | --- | --- |
| positive_sentiment_spike | group_or_knockout | -0.0333 | 3.7292 | 0.4625 | 0.1406 | 178 |
| stage_attention_spike | group_or_knockout | -0.0436 | 3.7189 | 0.3851 | 0.1380 | 1046 |
| baseline_attention | tournament | -0.0542 | 3.6528 | 0.2835 | 0.1339 | 720 |

## Resource Optimization

| sponsor | budget_m | media_multiplier | expected_roi | risk_adjusted_roi | risk_penalty | recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Adidas | 100 | 1.0000 | 2.2295 | 1.5496 | 0.3050 | test_or_hold |
| Adidas | 100 | 0.8000 | 2.1453 | 1.4911 | 0.3050 | test_or_hold |
| Qatar Airways | 100 | 1.0000 | 2.1278 | 1.4789 | 0.3050 | test_or_hold |
| Vivo | 100 | 1.0000 | 2.1123 | 1.4681 | 0.3050 | test_or_hold |
| Coca-Cola | 100 | 1.0000 | 2.0908 | 1.4532 | 0.3050 | test_or_hold |
| Vivo | 50 | 1.0000 | 1.6714 | 1.1617 | 0.3050 | test_or_hold |
| Mengniu | 50 | 1.0000 | 1.6485 | 1.1458 | 0.3050 | test_or_hold |
| Adidas | 50 | 1.0000 | 1.6302 | 1.1330 | 0.3050 | test_or_hold |
| Vivo | 50 | 0.8000 | 1.6064 | 1.1165 | 0.3050 | test_or_hold |
| Mengniu | 50 | 0.8000 | 1.5841 | 1.1010 | 0.3050 | test_or_hold |
| Vivo | 25 | 1.0000 | 1.1042 | 0.7675 | 0.3050 | test_or_hold |
| Mengniu | 25 | 1.0000 | 1.0866 | 0.7552 | 0.3050 | test_or_hold |

## Graph Attention Sponsor Contributions

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness | sponsor | avg_roi | avg_brand_fit | avg_attention | attention_roi_contribution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sponsor:Adidas | sponsor | 0.2989 | 0.5928 | 0.4606 | 0.6681 | 0.6693 | 0.0306 | 0.9319 | Adidas | 3.8883 | 0.7426 | 52.5688 | 0.8125 |
| sponsor:Coca-Cola | sponsor | 0.3022 | 0.5916 | 0.4614 | 0.6561 | 0.6674 | 0.0592 | 0.9349 | Coca-Cola | 3.7008 | 0.7644 | 52.0972 | 0.7178 |
| sponsor:Hyundai | sponsor | 0.2854 | 0.5345 | 0.4224 | 0.5889 | 0.5918 | 0.0383 | 0.9180 | Hyundai | 3.7894 | 0.7145 | 53.1490 | 0.6166 |
| sponsor:Visa | sponsor | 0.2962 | 0.5676 | 0.4455 | 0.6280 | 0.6374 | 0.0464 | 0.9281 | Visa | 3.7261 | 0.7259 | 51.8098 | 0.6122 |
| sponsor:Hisense | sponsor | 0.2649 | 0.4743 | 0.3801 | 0.5072 | 0.5170 | 0.0380 | 0.9018 | Hisense | 3.6673 | 0.7452 | 54.1317 | 0.5053 |
| sponsor:Qatar Airways | sponsor | 0.2601 | 0.4434 | 0.3609 | 0.4680 | 0.4746 | 0.0382 | 0.8912 | Qatar Airways | 3.7406 | 0.7489 | 52.6172 | 0.4387 |
| sponsor:Budweiser | sponsor | 0.2592 | 0.4453 | 0.3616 | 0.4716 | 0.4786 | 0.0317 | 0.8933 | Budweiser | 3.7004 | 0.7113 | 52.1147 | 0.3357 |
| sponsor:Vivo | sponsor | 0.2553 | 0.4406 | 0.3572 | 0.4323 | 0.4466 | 0.1756 | 0.8860 | Vivo | 3.5283 | 0.7211 | 53.6680 | 0.2959 |
| sponsor:Mengniu | sponsor | 0.2332 | 0.3669 | 0.3067 | 0.3462 | 0.3612 | 0.1246 | 0.8662 | Mengniu | 3.5169 | 0.6901 | 56.3508 | 0.1950 |
| sponsor:McDonald's | sponsor | 0.2468 | 0.3966 | 0.3292 | 0.3858 | 0.4009 | 0.1200 | 0.8769 | McDonald's | 3.4921 | 0.7304 | 52.1158 | 0.1440 |

## Extreme Scenario Stress Test

| team | sponsor | extreme_scenario | baseline_roi | scenario_roi | roi_ci_low | roi_ci_high | risk_interval_width | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Israel | Budweiser | sentiment_crisis | 2.8563 | 2.3422 | 1.9725 | 2.7119 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Brazil | Adidas | sentiment_crisis | 4.0690 | 3.3366 | 2.9668 | 3.7063 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Czech Republic | Mengniu | sentiment_crisis | 3.3232 | 2.7251 | 2.3554 | 3.0948 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Iraq | McDonald's | sentiment_crisis | 3.2923 | 2.6997 | 2.3300 | 3.0694 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Costa Rica | Visa | sentiment_crisis | 3.7775 | 3.0976 | 2.7279 | 3.4673 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Italy | Visa | sentiment_crisis | 3.7860 | 3.1045 | 2.7348 | 3.4742 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Trinidad and Tobago | Mengniu | sentiment_crisis | 3.3450 | 2.7429 | 2.3732 | 3.1126 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Slovakia | McDonald's | sentiment_crisis | 3.3258 | 2.7271 | 2.3574 | 3.0968 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Hungary | Adidas | sentiment_crisis | 3.8387 | 3.1477 | 2.7780 | 3.5175 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| France | Qatar Airways | sentiment_crisis | 3.8416 | 3.1501 | 2.7804 | 3.5198 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| New Zealand | McDonald's | sentiment_crisis | 3.8300 | 3.1406 | 2.7709 | 3.5103 | 0.7394 | Negative social/news sentiment requires defensive spend. |
| Japan | Adidas | sentiment_crisis | 3.7936 | 3.1107 | 2.7410 | 3.4804 | 0.7394 | Negative social/news sentiment requires defensive spend. |

## Integrated Commercial Decision Score

| panel_id | team | sponsor | stage | predicted_roi | media_value_index | fan_conversion_rate | social_spread_index | brand_influence_score | commercial_decision_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2014_833_Brazil | Brazil | Adidas | group_or_knockout | 4.5410 | 0.8036 | 0.8140 | 0.7599 | 0.9006 | 0.8798 |
| 2010_761_Brazil | Brazil | Adidas | group_or_knockout | 4.5180 | 0.6832 | 0.7725 | 0.8329 | 0.9006 | 0.8514 |
| 2014_833_Germany | Germany | Coca-Cola | group_or_knockout | 4.5410 | 0.8036 | 0.6739 | 0.6638 | 0.8341 | 0.8344 |
| 2010_735_Brazil | Brazil | Adidas | group_or_knockout | 4.4450 | 0.6681 | 0.7596 | 0.7713 | 0.9006 | 0.8227 |
| 2010_720_Brazil | Brazil | Adidas | group_or_knockout | 4.4750 | 0.6388 | 0.7529 | 0.7640 | 0.9006 | 0.8200 |
| 2014_835_Brazil | Brazil | Adidas | group_or_knockout | 4.4690 | 0.6480 | 0.7557 | 0.7217 | 0.9006 | 0.8154 |
| 1998_517_Brazil | Brazil | Adidas | group_or_knockout | 4.4540 | 0.6140 | 0.7424 | 0.8060 | 0.9006 | 0.8143 |
| 2022_954_Brazil | Brazil | Adidas | group_or_knockout | 4.4370 | 0.6876 | 0.7614 | 0.6837 | 0.9006 | 0.8135 |
| 2014_835_Netherlands | Netherlands | Hisense | group_or_knockout | 4.4690 | 0.6480 | 0.6928 | 0.7219 | 0.8823 | 0.8023 |
| 2018_869_Russia | Russia | Hyundai | group_or_knockout | 4.3390 | 0.7737 | 0.6667 | 0.7780 | 0.8029 | 0.7994 |
| 2018_894_Brazil | Brazil | Adidas | group_or_knockout | 4.3770 | 0.6565 | 0.7464 | 0.7099 | 0.9006 | 0.7957 |
| 2018_900_France | France | Qatar Airways | group_or_knockout | 4.2450 | 0.8295 | 0.6570 | 0.7393 | 0.8296 | 0.7885 |

## Landing Recommendations

- Use the future ROI trend as a planning prior, not a guaranteed forecast.
- Tie budget increases to both media multiplier sensitivity and risk-adjusted ROI.
- Treat sentiment crisis and key-player injury scenarios as pre-approval triggers for contingency spend.
- Combine SHAP-style tabular drivers with graph attention scores before selecting anchor sponsor partnerships.