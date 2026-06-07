# Academic Figure Notes

## Model Performance Comparison

![Model Performance Comparison](model_performance_comparison.png)

**What it shows:** Compares trained baseline and benchmark models on their primary evaluation metrics.

**Why it matters:** It reveals whether the current model choice is a stable analytical baseline or only a weak placeholder.

**Business takeaway:** Use the benchmark spread to decide which model family deserves production tuning first.

## ROI Feature Importance / SHAP

![ROI Feature Importance / SHAP](roi_feature_importance_shap.png)

**What it shows:** Ranks the strongest sponsor ROI drivers using SHAP-style feature contribution scores.

**Why it matters:** Explainability keeps ROI recommendations auditable and helps detect proxy-label overdependence.

**Business takeaway:** Improve brand heat, sponsor-team fit, media exposure, and activation quality before scaling spend.

## Sponsor ROI Ranking

![Sponsor ROI Ranking](sponsor_roi_ranking.png)

**What it shows:** Ranks sponsors by predicted commercial ROI and network influence evidence.

**Why it matters:** A sponsor can look attractive either because expected ROI is high or because relationship influence is broad.

**Business takeaway:** Prioritize sponsors that combine high ROI with strong team-player-network leverage.

## Scenario ROI Lift

![Scenario ROI Lift](scenario_roi_lift.png)

**What it shows:** Shows conservative, balanced, and aggressive strategy lift against the baseline.

**Why it matters:** Scenario analysis turns the model from prediction into a decision simulator.

**Business takeaway:** Select aggressive strategies only when lift is positive and risk remains tolerable.

## Monte Carlo Risk Distribution

![Monte Carlo Risk Distribution](monte_carlo_risk_distribution.png)

**What it shows:** Shows the distribution of Monte Carlo ROI standard deviation and risk scores.

**Why it matters:** The spread of risk is often more important than average ROI for sponsorship planning.

**Business takeaway:** Use high-risk tails as triggers for staged spend, insurance clauses, or additional analyst review.

## Prediction Interval / Conformal Prediction

![Prediction Interval / Conformal Prediction](prediction_interval_conformal.png)

**What it shows:** Displays ROI point estimates with conformal-style prediction intervals.

**Why it matters:** Prediction intervals show forecast reliability, not just expected value.

**Business takeaway:** Prefer narrow-interval opportunities when sponsor budgets are constrained.

## Sponsor-Team-Player Network

![Sponsor-Team-Player Network](sponsor_team_player_network.png)

**What it shows:** Visualizes sponsor, team, and player relationships as a weighted commercial graph.

**Why it matters:** Graph position captures activation leverage that flat tables miss.

**Business takeaway:** Use central sponsors and teams as anchor partnerships for campaign portfolios.
