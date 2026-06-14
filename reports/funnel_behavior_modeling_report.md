# Funnel Behavior Modeling Report

## Funnel

Exposure -> Attention -> Engagement -> Conversion -> ROI

## Top Conversion Paths

| team | sponsor | Exposure | Attention | Engagement | Conversion | ROI | exposure_to_attention | attention_to_engagement | engagement_to_conversion | conversion_to_roi | behavior_decay_rate | recommended_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Brazil | Adidas | 0.4959 | 0.4611 | 0.7917 | 1.0000 | 0.7399 | 0.9298 | 1.7170 | 1.2631 | 0.7399 | -0.4920 | tighten_sponsor_offer_and_landing_path |
| Indonesia | Coca-Cola | 0.2881 | 0.0136 | 0.1480 | 0.3959 | 0.7003 | 0.0472 | 3.0000 | 2.6750 | 1.7689 | -1.0000 | scale_high_quality_funnel |
| Argentina | Hyundai | 0.5281 | 0.4037 | 0.7296 | 0.9932 | 0.6374 | 0.7644 | 1.8073 | 1.3613 | 0.6418 | -0.2070 | tighten_sponsor_offer_and_landing_path |
| China | Adidas | 0.6340 | 0.3607 | 0.4798 | 0.7172 | 0.6277 | 0.5689 | 1.3302 | 1.4948 | 0.8752 | 0.0099 | tighten_sponsor_offer_and_landing_path |
| Ukraine | Qatar Airways | 0.6343 | 0.4098 | 0.5794 | 0.7722 | 0.6207 | 0.6461 | 1.4139 | 1.3328 | 0.8038 | 0.0214 | tighten_sponsor_offer_and_landing_path |
| France | Qatar Airways | 0.5450 | 0.4117 | 0.6201 | 0.9090 | 0.6147 | 0.7554 | 1.5062 | 1.4659 | 0.6762 | -0.1279 | tighten_sponsor_offer_and_landing_path |
| Hungary | Adidas | 0.3981 | 0.3431 | 0.6079 | 0.8006 | 0.6131 | 0.8618 | 1.7718 | 1.3170 | 0.7658 | -0.5401 | tighten_sponsor_offer_and_landing_path |
| New Zealand | McDonald's | 0.5916 | 0.3427 | 0.1404 | 0.0982 | 0.6083 | 0.5793 | 0.4097 | 0.6994 | 3.0000 | -0.0282 | improve_creative_and_social_activation |
| Japan | Adidas | 0.6656 | 0.4049 | 0.6191 | 0.7850 | 0.5882 | 0.6083 | 1.5290 | 1.2680 | 0.7493 | 0.1163 | tighten_sponsor_offer_and_landing_path |
| Germany | Coca-Cola | 0.5098 | 0.3720 | 0.6045 | 0.8965 | 0.5873 | 0.7297 | 1.6250 | 1.4830 | 0.6551 | -0.1520 | tighten_sponsor_offer_and_landing_path |
| Russia | Hyundai | 0.4925 | 0.4148 | 0.6505 | 0.9309 | 0.5858 | 0.8422 | 1.5682 | 1.4311 | 0.6293 | -0.1894 | tighten_sponsor_offer_and_landing_path |
| Italy | Visa | 0.4480 | 0.3366 | 0.6104 | 0.9956 | 0.5840 | 0.7513 | 1.8134 | 1.6311 | 0.5866 | -0.3036 | tighten_sponsor_offer_and_landing_path |

## Fan Behavior Decay Model

The decay rate measures how much normalized exposure is lost before becoming ROI. High decay means the audience is visible but not converting efficiently.

## Recommended Uses

- Use low attention-to-engagement ratios to diagnose creative fatigue.
- Use low conversion-to-ROI ratios to diagnose sponsor offer or activation fit.
- Use decay rate as a budget throttle before scaling paid media.