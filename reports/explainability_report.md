# ROI Explainability Report

SHAP package available; tree/linear SHAP can be enabled for production models.

## ROI Driver Summary

| feature | importance | mean_abs_contribution | direction |
| --- | --- | --- | --- |
| a_brand_heat_index | 0.1568154357897503 | 0.12392 | positive |
| a_sponsor_spend_m | 0.1300426559020262 | 0.10179 | negative |
| a_ad_exposure_m | 0.125219167319632 | 0.10924 | positive |
| team_a_strength | 0.1153372763410352 | 0.09561 | positive |
| sponsor_team_fit_score | 0.0526729831428175 | 0.04145 | positive |
| commercial_momentum_score | 0.0512481777707158 | 0.04177 | positive |
| a_activation_quality | 0.0444864523730867 | 0.03418 | negative |
| elo_diff | 0.0425958198226457 | 0.03508 | positive |
| fan_score | 0.0402561308892874 | 0.03293 | positive |
| event_attention_m | 0.0336303241229898 | 0.02795 | positive |

## Business Interpretation

- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.
- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.
- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.