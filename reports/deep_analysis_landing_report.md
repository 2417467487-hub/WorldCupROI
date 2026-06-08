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
| 2026 | 3.9428 | 0.0076 | linear trend over historical/proxy sponsorship panel |
| 2030 | 3.9504 | 0.0076 | linear trend over historical/proxy sponsorship panel |
| 2034 | 3.9580 | 0.0076 | linear trend over historical/proxy sponsorship panel |

## Sentiment Event Impact

| event_type | stage | avg_roi_delta | avg_roi | avg_attention_sentiment | avg_conversion | samples |
| --- | --- | --- | --- | --- | --- | --- |
| positive_sentiment_spike | tournament | 0.5080 | 4.4470 | 0.5584 | 0.1325 | 2 |
| positive_sentiment_spike | group_or_knockout | 0.0111 | 3.9566 | 0.4611 | 0.1466 | 150 |
| stage_attention_spike | group_or_knockout | -0.0781 | 3.8674 | 0.3946 | 0.1452 | 1058 |
| baseline_attention | tournament | -0.0866 | 3.8524 | 0.2901 | 0.1375 | 718 |

## Resource Optimization

| sponsor | budget_m | media_multiplier | expected_roi | risk_adjusted_roi | risk_penalty | recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Coca-Cola | 100 | 1.0000 | 2.2751 | 1.5782 | 0.3063 | test_or_hold |
| Hyundai | 100 | 1.0000 | 2.2542 | 1.5637 | 0.3063 | test_or_hold |
| Budweiser | 100 | 1.0000 | 2.2311 | 1.5476 | 0.3063 | test_or_hold |
| Coca-Cola | 100 | 0.8000 | 2.1898 | 1.5190 | 0.3063 | test_or_hold |
| Vivo | 100 | 1.0000 | 2.1848 | 1.5155 | 0.3063 | test_or_hold |
| Mengniu | 50 | 1.0000 | 1.7513 | 1.2149 | 0.3063 | test_or_hold |
| Vivo | 50 | 1.0000 | 1.7403 | 1.2072 | 0.3063 | test_or_hold |
| McDonald's | 50 | 1.0000 | 1.6940 | 1.1750 | 0.3063 | test_or_hold |
| Mengniu | 50 | 0.8000 | 1.6831 | 1.1675 | 0.3063 | test_or_hold |
| Vivo | 50 | 0.8000 | 1.6731 | 1.1606 | 0.3063 | test_or_hold |
| Mengniu | 25 | 1.0000 | 1.1793 | 0.8181 | 0.3063 | test_or_hold |
| Vivo | 25 | 1.0000 | 1.1560 | 0.8019 | 0.3063 | test_or_hold |

## Graph Attention Sponsor Contributions

| node | node_type | gcn_score | graphsage_score | combined_graph_score | embedding_degree | embedding_pagerank | embedding_betweenness | embedding_closeness | sponsor | avg_roi | avg_brand_fit | avg_attention | attention_roi_contribution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sponsor:Coca-Cola | sponsor | 0.2835 | 0.5457 | 0.4277 | 0.6098 | 0.6071 | 0.0219 | 0.9172 | Coca-Cola | 4.0472 | 0.7839 | 53.5794 | 0.8265 |
| sponsor:Hyundai | sponsor | 0.2973 | 0.5918 | 0.4593 | 0.6676 | 0.6686 | 0.0253 | 0.9343 | Hyundai | 3.9884 | 0.7279 | 52.7831 | 0.7604 |
| sponsor:Adidas | sponsor | 0.2859 | 0.5389 | 0.4251 | 0.5952 | 0.5982 | 0.0369 | 0.9173 | Adidas | 3.9826 | 0.7550 | 51.6759 | 0.6942 |
| sponsor:Visa | sponsor | 0.2846 | 0.5350 | 0.4223 | 0.5889 | 0.5943 | 0.0356 | 0.9205 | Visa | 3.8724 | 0.7083 | 51.9973 | 0.5725 |
| sponsor:Hisense | sponsor | 0.2547 | 0.4414 | 0.3574 | 0.4701 | 0.4757 | 0.0188 | 0.8894 | Hisense | 3.8768 | 0.7303 | 53.3436 | 0.5044 |
| sponsor:Budweiser | sponsor | 0.2525 | 0.4399 | 0.3556 | 0.4682 | 0.4730 | 0.0201 | 0.8890 | Budweiser | 3.9148 | 0.7025 | 52.3166 | 0.4509 |
| sponsor:Qatar Airways | sponsor | 0.2467 | 0.4043 | 0.3334 | 0.4193 | 0.4284 | 0.0239 | 0.8763 | Qatar Airways | 3.8860 | 0.7528 | 50.8360 | 0.4230 |
| sponsor:McDonald's | sponsor | 0.2506 | 0.4369 | 0.3531 | 0.4435 | 0.4587 | 0.0981 | 0.8877 | McDonald's | 3.6170 | 0.7292 | 52.9543 | 0.3520 |
| sponsor:Vivo | sponsor | 0.2317 | 0.3753 | 0.3107 | 0.3655 | 0.3816 | 0.0850 | 0.8674 | Vivo | 3.6132 | 0.7369 | 53.5654 | 0.2870 |
| sponsor:Mengniu | sponsor | 0.2024 | 0.2794 | 0.2447 | 0.2425 | 0.2603 | 0.0708 | 0.8366 | Mengniu | 3.5715 | 0.7185 | 57.4964 | 0.2036 |

## Extreme Scenario Stress Test

| team | sponsor | extreme_scenario | baseline_roi | scenario_roi | roi_ci_low | roi_ci_high | risk_interval_width | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qatar | McDonald's | sentiment_crisis | 3.0450 | 2.4969 | 2.1293 | 2.8645 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Germany | Coca-Cola | sentiment_crisis | 4.2217 | 3.4618 | 3.0941 | 3.8294 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Trinidad and Tobago | Mengniu | sentiment_crisis | 3.4303 | 2.8129 | 2.4452 | 3.1805 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Bolivia | Qatar Airways | sentiment_crisis | 3.3850 | 2.7757 | 2.4081 | 3.1433 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Ukraine | Qatar Airways | sentiment_crisis | 3.9666 | 3.2526 | 2.8850 | 3.6203 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Spain | Budweiser | sentiment_crisis | 3.9742 | 3.2588 | 2.8912 | 3.6265 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Ghana | Mengniu | sentiment_crisis | 3.4672 | 2.8431 | 2.4755 | 3.2107 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| DR Congo | Visa | sentiment_crisis | 3.4560 | 2.8339 | 2.4663 | 3.2016 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Saudi Arabia | Visa | sentiment_crisis | 4.0080 | 3.2866 | 2.9189 | 3.6542 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| France | Qatar Airways | sentiment_crisis | 4.0090 | 3.2874 | 2.9197 | 3.6550 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| El Salvador | Budweiser | sentiment_crisis | 3.9967 | 3.2773 | 2.9096 | 3.6449 | 0.7353 | Negative social/news sentiment requires defensive spend. |
| Russia | Hyundai | sentiment_crisis | 3.9915 | 3.2730 | 2.9054 | 3.6406 | 0.7353 | Negative social/news sentiment requires defensive spend. |

## Integrated Commercial Decision Score

| panel_id | team | sponsor | stage | predicted_roi | media_value_index | fan_conversion_rate | social_spread_index | brand_influence_score | commercial_decision_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1982_312_Hungary | Hungary | Adidas | tournament | 4.4470 | 0.8989 | 0.5928 | 0.8959 | 0.7896 | 0.8310 |
| 1994_501_Germany | Germany | Coca-Cola | group_or_knockout | 4.6510 | 0.5979 | 0.6463 | 0.7111 | 0.9647 | 0.8037 |
| 2022_909_Germany | Germany | Coca-Cola | group_or_knockout | 4.6510 | 0.6303 | 0.6566 | 0.6266 | 0.9647 | 0.8009 |
| 2002_582_Germany | Germany | Coca-Cola | group_or_knockout | 4.6520 | 0.6406 | 0.6588 | 0.6055 | 0.9647 | 0.8008 |
| 2014_833_Germany | Germany | Coca-Cola | group_or_knockout | 4.4270 | 0.7421 | 0.6805 | 0.6790 | 0.9647 | 0.7957 |
| 1994_501_Belgium | Belgium | Visa | group_or_knockout | 4.6510 | 0.5979 | 0.6982 | 0.6935 | 0.7422 | 0.7883 |
| 2010_715_Germany | Germany | Coca-Cola | group_or_knockout | 4.6500 | 0.5838 | 0.6396 | 0.6251 | 0.9647 | 0.7872 |
| 2018_846_Germany | Germany | Coca-Cola | group_or_knockout | 4.6160 | 0.5655 | 0.6314 | 0.6333 | 0.9647 | 0.7766 |
| 2006_645_Germany | Germany | Coca-Cola | group_or_knockout | 4.6420 | 0.5756 | 0.6352 | 0.5620 | 0.9647 | 0.7743 |
| 2014_835_Brazil | Brazil | Adidas | group_or_knockout | 4.4720 | 0.6978 | 0.5604 | 0.7103 | 0.9106 | 0.7716 |
| 2010_770_Germany | Germany | Coca-Cola | group_or_knockout | 4.5780 | 0.5520 | 0.6247 | 0.6659 | 0.9647 | 0.7699 |
| 2018_863_Belgium | Belgium | Visa | group_or_knockout | 4.4100 | 0.7145 | 0.7183 | 0.6644 | 0.7422 | 0.7690 |

## Landing Recommendations

- Use the future ROI trend as a planning prior, not a guaranteed forecast.
- Tie budget increases to both media multiplier sensitivity and risk-adjusted ROI.
- Treat sentiment crisis and key-player injury scenarios as pre-approval triggers for contingency spend.
- Combine SHAP-style tabular drivers with graph attention scores before selecting anchor sponsor partnerships.