# Research Agenda

## Research Questions

1. How do sports performance signals influence sponsorship ROI?
2. Does sponsor spend create ROI by itself, or only when combined with brand heat and media exposure?
3. How much does player availability change expected commercial return?
4. Can social engagement and sentiment explain ROI beyond win probability?
5. Which data modality is most important for sponsor decision support: tabular sports data, social media, text narratives, time series, or relationship networks?

## Research Contributions

- Builds a multi-task machine learning framework for sports sponsorship intelligence.
- Treats match prediction as a context signal rather than the final objective.
- Introduces FanScore and Sponsor Power Index as interpretable business features.
- Creates a reproducible mock data layer with real API upgrade paths.
- Provides an interactive dashboard for sponsor strategy simulation.

## Methodology

```text
Data generation / ingestion
  -> data quality profiling
  -> feature engineering
  -> match outcome modeling
  -> sponsor ROI modeling
  -> counterfactual A/B simulation
  -> dashboard decision support
```

## Future Research Directions

- Add causal inference models for sponsor activation effect.
- Add SHAP explanations for ROI prediction.
- Add graph-based sponsor ecosystem analysis.
- Add transformer-based sentiment and topic modeling.
- Add time-series forecasting for sponsor campaign momentum.
- Compare model performance across tournament stages and sponsor categories.
