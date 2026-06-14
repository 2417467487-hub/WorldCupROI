# ROI Explainability Report

SHAP package available; tree/linear SHAP can be enabled for production models.

## ROI Driver Summary

| feature | importance | mean_abs_contribution | direction |
| --- | --- | --- | --- |
| team_a_strength | 0.0993670273040379 | 0.08322 | positive |
| a_ad_exposure_m | 0.0960826108340894 | 0.0847 | positive |
| a_sponsor_spend_m | 0.081420490446591 | 0.05893 | negative |
| a_brand_heat_index | 0.0774443722707214 | 0.06196 | positive |
| fan_score | 0.0500240355066434 | 0.03964 | positive |
| commercial_momentum_score | 0.0458596807888955 | 0.03693 | positive |
| elo_diff | 0.0402506478790506 | 0.03343 | positive |
| sponsor_team_fit_score | 0.0317696872934176 | 0.02512 | positive |
| event_attention_m | 0.031174080590329 | 0.02556 | positive |
| a_core_market_value_m | 0.0305956980612154 | 0.02564 | positive |

## Business Interpretation

- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.
- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.
- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.