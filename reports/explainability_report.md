# ROI Explainability Report

SHAP package available; tree/linear SHAP can be enabled for production models.

## ROI Driver Summary

| feature | importance | mean_abs_contribution | direction |
| --- | --- | --- | --- |
| a_sponsor_spend_m | 0.1389838745830899 | 0.1128 | negative |
| a_brand_heat_index | 0.1376415011403514 | 0.12101 | positive |
| team_a_strength | 0.1313983068427144 | 0.10893 | positive |
| a_ad_exposure_m | 0.1042782919074796 | 0.06035 | positive |
| sponsor_team_fit_score | 0.0520033203158611 | 0.04356 | positive |
| elo_diff | 0.0444862271555914 | 0.03664 | positive |
| commercial_momentum_score | 0.041980473444034 | 0.03443 | positive |
| fan_score | 0.038694946933084 | 0.03166 | positive |
| event_attention_m | 0.0360413245944141 | 0.02996 | positive |
| a_core_market_value_m | 0.031887279221416 | 0.02608 | positive |

## Business Interpretation

- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.
- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.
- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.