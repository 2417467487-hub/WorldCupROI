# ROI Explainability Report

SHAP package not installed in the runtime; generated dependency-free SHAP-style linear contributions.

## ROI Driver Summary

| feature | importance | mean_abs_contribution | direction |
| --- | --- | --- | --- |
| a_brand_heat_index | 0.134803718381491 | 0.11852 | positive |
| team_a_strength | 0.1334579869501301 | 0.11064 | positive |
| a_sponsor_spend_m | 0.1328897978770402 | 0.10785 | negative |
| a_ad_exposure_m | 0.1136093484215305 | 0.09634 | positive |
| sponsor_team_fit_score | 0.0450525583062206 | 0.03774 | positive |
| commercial_momentum_score | 0.0445787963680799 | 0.03714 | positive |
| elo_diff | 0.0425995294465618 | 0.03509 | positive |
| fan_score | 0.0401241603341231 | 0.03283 | positive |
| event_attention_m | 0.0345506740259435 | 0.02872 | positive |
| a_activation_quality | 0.0341170808924483 | 0.02893 | negative |

## Business Interpretation

- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.
- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.
- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.