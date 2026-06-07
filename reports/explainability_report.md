# ROI Explainability Report

SHAP package available; tree/linear SHAP can be enabled for production models.

## ROI Driver Summary

| feature | importance | mean_abs_contribution | direction |
| --- | --- | --- | --- |
| a_sponsor_spend_m | 0.137375527671942 | 0.11149 | negative |
| a_brand_heat_index | 0.1350231295049905 | 0.11871 | positive |
| team_a_strength | 0.1296067832999324 | 0.10744 | positive |
| a_ad_exposure_m | 0.1066168231526236 | 0.08926 | positive |
| sponsor_team_fit_score | 0.0453497873114412 | 0.03799 | positive |
| commercial_momentum_score | 0.0438740406091631 | 0.03667 | positive |
| elo_diff | 0.0422095135972998 | 0.03476 | positive |
| fan_score | 0.0419835229341548 | 0.03435 | positive |
| event_attention_m | 0.0354876179769886 | 0.0295 | positive |
| a_activation_quality | 0.0347301225958751 | 0.02945 | negative |

## Business Interpretation

- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.
- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.
- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.