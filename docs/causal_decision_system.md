# Causal Sports Intelligence System

WorldCupROI has been upgraded from a sponsor ROI prediction project into a causal decision and optimization system for sports sponsorship strategy.

## System Shift

| Previous layer | Upgraded layer | Why it matters |
|---|---|---|
| ROI prediction | Causal treatment effect estimation | Avoids treating correlation as business causation. |
| Scenario simulation | Counterfactual intervention engine | Tests player injury, media shocks and budget changes before action. |
| Sponsor ranking | Budget-constrained optimization | Converts model scores into allocation strategy. |
| FanScore metrics | User behavior funnel | Explains how exposure turns into conversion and ROI. |
| Static dashboard | Decision workflow | Produces recommendations, budget priority and risk warnings. |
| Graph analysis | Graph learning proxy | Adds link prediction and HGT-style influence ranking. |

## Module Map

| Module | File | Outputs |
|---|---|---|
| Causal inference | `src/causal_inference.py` | `reports/causal_treatment_effects.csv`, `docs/assets/causal_treatment_effects.svg` |
| Sponsor optimization | `src/sponsor_optimization.py` | `reports/optimized_sponsor_allocation.csv`, `reports/bandit_sponsor_policy.csv` |
| User behavior funnel | `src/user_behavior_model.py` | `reports/user_behavior_funnel.csv`, `docs/assets/user_behavior_funnel.svg` |
| Temporal dynamics | `src/temporal_dynamics.py` | `reports/temporal_roi_dynamics.csv`, `docs/assets/temporal_roi_dynamics.svg` |
| Counterfactual engine | `src/counterfactual_engine.py` | `reports/counterfactual_interventions.csv`, `docs/assets/counterfactual_roi_interventions.svg` |
| Graph learning | `src/graph_learning.py` | `reports/graph_link_prediction.csv`, `reports/graph_learning_node_influence.csv` |
| Decision system | `src/decision_system.py` | `reports/sponsor_investment_recommendations.csv` |
| Generative insight engine | `src/generative_insight_engine.py` | `reports/causal_sports_intelligence_report.md` |

## Causal Interpretation

The current implementation uses a lightweight backdoor-adjusted OLS baseline so the full project remains reproducible without heavy causal libraries. The design is intentionally compatible with:

- DoWhy for graph assumptions, refutation tests and placebo checks.
- EconML and Causal Forest for heterogeneous treatment effects.
- Synthetic control for sponsor/team counterfactual baselines.
- Structural causal models for injury, media exposure and budget interventions.

## Decision Logic

The system produces recommendations by combining:

- expected sponsor ROI
- causal-style treatment effects
- funnel conversion efficiency
- scenario lift
- budget allocation priority
- graph influence
- uncertainty and downside risk

The goal is not to maximize a single prediction score. The goal is to support sponsor decisions that are explainable, robust under counterfactual stress and feasible under budget constraints.
