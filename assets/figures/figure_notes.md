# README Figure Notes

## roi_feature_importance.svg

![roi_feature_importance.svg](assets/figures/roi_feature_importance.svg)

**What:** Figure ranks the strongest drivers of predicted sponsor ROI.

**Why:** It explains why the model produces high or low ROI forecasts instead of leaving the dashboard as a black box.

**Business Takeaway:** Use the top drivers to decide whether to improve brand fit, media exposure, or sponsor activation before increasing spend.

## scenario_ranking.svg

![scenario_ranking.svg](assets/figures/scenario_ranking.svg)

**What:** Figure compares counterfactual sponsor strategy ROI lift.

**Why:** It shows the marginal effect of sponsor actions before campaign money is committed.

**Business Takeaway:** Prioritize positive-lift strategies unless the risk visuals show a weaker lift-risk tradeoff.

## roi_uncertainty_intervals.svg

![roi_uncertainty_intervals.svg](assets/figures/roi_uncertainty_intervals.svg)

**What:** Figure shows expected ROI with prediction intervals.

**Why:** Intervals reveal forecast reliability, not only point estimates.

**Business Takeaway:** Use wider intervals as a trigger for conservative budgets, staged spend, or performance-based contracts.

## text_embedding_map.svg

![text_embedding_map.svg](assets/figures/text_embedding_map.svg)

**What:** Figure projects real-source text into a sponsor-attention map.

**Why:** It shows whether media narratives cluster around similar attention signals.

**Business Takeaway:** Use text clusters to guide campaign messaging and monitor narrative drift.

## gnn_relationship_explainer.svg

![gnn_relationship_explainer.svg](assets/figures/gnn_relationship_explainer.svg)

**What:** Figure explains the team-player-sponsor-match graph structure.

**Why:** Graph structure makes influence visible beyond flat tables.

**Business Takeaway:** Use graph influence to identify sponsors or players with stronger activation leverage.

## data_flow.svg

![data_flow.svg](assets/figures/data_flow.svg)

**What:** Figure maps how raw match, text, context, and commercial proxy data enter the feature store.

**Why:** It documents the data boundary so users understand which signals are real-source and which are proxy.

**Business Takeaway:** Use the flow to plan future replacement of proxy commercial variables with licensed data.

## architecture.svg

![architecture.svg](assets/figures/architecture.svg)

**What:** Figure shows the full platform architecture from data sources to decisions.

**Why:** It helps reviewers understand how modeling, uncertainty, graph intelligence, and dashboard outputs connect.

**Business Takeaway:** Use it as the project landing explanation for technical and business audiences.

## model_pipeline.svg

![model_pipeline.svg](assets/figures/model_pipeline.svg)

**What:** Figure shows the modeling pipeline and reliability layers.

**Why:** It separates predictive models from interpretability and risk controls.

**Business Takeaway:** Use it to justify why the platform is more than a match predictor.

## decision_workflow.svg

![decision_workflow.svg](assets/figures/decision_workflow.svg)

**What:** Figure summarizes the Discover -> Explain -> Predict -> Simulate -> Recommend workflow.

**Why:** It keeps the product narrative focused on business decisions.

**Business Takeaway:** Use it to onboard users before they open the dashboard.
