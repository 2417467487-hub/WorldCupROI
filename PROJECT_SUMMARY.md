# PROJECT_SUMMARY

## Project Goal

WorldCupROI is a sports sponsorship intelligence platform. It connects World Cup match context, fan attention, media narratives, player/team strength, sponsor activation, uncertainty, and scenario simulation into one ROI decision workflow.

The project is designed to answer a business question rather than only a match-prediction question:

> Which sponsor/team/scenario combination produces the best expected ROI after accounting for attention, uncertainty, and downside risk?

## Data Sources

- Historical match records: `data/raw/international_results.csv`
- 2026 schedule and venue context: `data/schedule_2026.csv`
- Sponsor and activation inputs: `data/sponsors.csv`
- Player/team/coach context: `data/players.csv`, `data/team_profile.csv`, `data/coaches.csv`
- Real-source text evidence: GDELT and Wikimedia snapshots under `data/raw`
- Dashboard panel data: `data/panel_dataset.csv`

Public data is used where available. Sponsor spend and commercial ROI fields are proxy-derived when contract-level data is not public.

## Algorithm System

The upgraded algorithm structure is documented in:

- `reports/algorithm_strategy.md`
- `reports/algorithm_manifest.json`

Current layers:

1. Match Outcome Layer
   - Current method: deterministic centroid classifier fallback
   - Output: win/draw/loss probability, feature importance, conformal prediction set
   - Upgrade path: calibrated logistic regression, LightGBM multiclass, XGBoost multi-class

2. Sponsor ROI Layer
   - Current method: standardized ridge regression fallback
   - Output: predicted ROI, ROI lift, ROI driver ranking, prediction interval
   - Upgrade path: ElasticNet, LightGBMRegressor, XGBoostRegressor, stacked tabular ensemble

3. Risk And Recommendation Layer
   - Current method: bootstrap, Monte Carlo perturbation, conformal intervals
   - Output: negative ROI probability, scenario ranking, lift-risk recommendation
   - Upgrade path: ensemble variance, Bayesian optimization, portfolio allocation policy

4. Relationship Intelligence Layer
   - Current method: weighted heterogeneous graph centrality
   - Output: sponsor influence score, player/team/sponsor graph metrics
   - Upgrade path: GraphSAGE, heterogeneous GNN, temporal graph model

## ROI Logic

ROI is modeled as a commercial return signal driven by:

- sponsor power and spend
- ad exposure and paid media share
- sponsor-team fit
- event attention and media reposts
- fan growth and engagement rate
- text sentiment and text signal score
- team strength and player influence
- injury, weather, and stage premium risk

The platform reports both point estimates and risk signals:

- predicted ROI
- ROI lift vs spend
- conformal ROI intervals
- Monte Carlo standard deviation
- negative ROI probability
- scenario ranking

## Platform

Platform entry points:

- Streamlit dashboard: `streamlit run dashboard/app.py`
- Static dashboard: `dashboard/panel_dashboard.html`
- Health check: `python src/platform_health.py` or `make health`
- Full pipeline: `python scripts/run_pipeline.py`

The platform workflow is:

```text
Discover -> Explain -> Predict -> Simulate -> Recommend
```

## Current Health

Latest platform health check:

- Health score: 100 / 100
- Status: healthy
- Report: `reports/platform_health.md`

## Next Stage Plan

- Add calibrated scikit-learn/LightGBM/XGBoost model selection as an optional production mode.
- Add experiment tracking with MLflow or DVC metrics snapshots.
- Add sponsor portfolio optimization under budget constraints.
- Add GNN baseline for team-player-sponsor-match relationships.
- Add live-data connectors for weather, social attention, injury feeds, and campaign performance.
