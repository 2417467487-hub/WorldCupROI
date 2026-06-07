# ROI Explainability Report

SHAP package available; tree/linear SHAP can be enabled for production models.

## ROI Driver Summary

| feature | importance | mean_abs_contribution | direction |
| --- | --- | --- | --- |
| a_brand_heat_index | 0.1612056009405758 | 0.14173 | positive |
| a_sponsor_spend_m | 0.1491269267781066 | 0.12103 | negative |
| a_ad_exposure_m | 0.1245955718195028 | 0.09734 | positive |
| team_a_strength | 0.1185800718169232 | 0.0983 | positive |
| sponsor_team_fit_score | 0.057914714625762 | 0.04851 | positive |
| commercial_momentum_score | 0.0498566150526403 | 0.04135 | positive |
| elo_diff | 0.0438775635591465 | 0.03614 | positive |
| fan_score | 0.0398208861032124 | 0.03258 | positive |
| event_attention_m | 0.0350117138869699 | 0.0291 | positive |
| a_core_market_value_m | 0.0298232105120834 | 0.02439 | positive |

## Business Interpretation

- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.
- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.
- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.