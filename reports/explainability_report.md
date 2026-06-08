# ROI Explainability Report

SHAP package available; tree/linear SHAP can be enabled for production models.

## ROI Driver Summary

| feature | importance | mean_abs_contribution | direction |
| --- | --- | --- | --- |
| a_sponsor_spend_m | 0.1374944677895308 | 0.10762 | negative |
| a_brand_heat_index | 0.1350113340193232 | 0.10669 | positive |
| a_ad_exposure_m | 0.1342510159182726 | 0.10692 | positive |
| team_a_strength | 0.1322968216127188 | 0.10967 | positive |
| commercial_momentum_score | 0.0486639677749725 | 0.0391 | positive |
| sponsor_team_fit_score | 0.0443118243346333 | 0.03487 | positive |
| elo_diff | 0.0431601605236608 | 0.03555 | positive |
| fan_score | 0.0405822453066129 | 0.0332 | positive |
| event_attention_m | 0.0346887556420902 | 0.02883 | positive |
| a_sponsor_power_index | 0.0310148133161391 | 0.02421 | positive |

## Business Interpretation

- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.
- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.
- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.