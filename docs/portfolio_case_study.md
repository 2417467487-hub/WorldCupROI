# WorldCupROI: portfolio case study

## Decision question

The project asks how match context, attention signals, and uncertainty can be assembled into a **sponsorship decision demo**. It is a reproducible analysis and product prototype, not an estimate of audited campaign revenue.

## Data and target boundary

| Part | Input or target | What can be concluded |
| --- | --- | --- |
| Match task | Historical match results and derived context; match result is constructed from scores | Match-outcome baselines can be evaluated against historical results. |
| Sponsor task | Engineered sponsor, attention, spend, and conversion proxy variables; `sponsor_roi` is a constructed proxy label | ROI models can be compared **on this proxy dataset**. Their scores do not validate real sponsor return. |
| Text and media | Source-oriented news and lightweight text signals | These are contextual features, not a production media measurement system. |

See [the data card](../reports/data_card.md) and [the model card](../reports/model_card.md) for field-level origins, splits, and limitations.

## Implementation and evaluation

```text
Data ingestion and quality checks
    -> feature engineering
    -> match and ROI proxy baselines
    -> holdout / cross-validation reports
    -> conformal sets and intervals
    -> scenario analysis
    -> Streamlit and static dashboards
```

The committed model cards report a **centroid match classifier** (accuracy `0.5023`, log loss `1.0097`) and a **ridge ROI proxy regressor** (MAE `0.1165`, R² `0.8478`). The committed conformal report records match coverage `0.9231` and ROI proxy interval coverage `0.8564`. These numbers describe the repository snapshot and its evaluation splits; they are not claims of business lift or deployment readiness. Sources: [match card](../reports/match_outcome_model_card.md), [ROI metrics](../reports/roi_model_metrics.md), and [conformal report](../reports/conformal_prediction_report.md).

## Try it

1. Install the dependencies in [`requirements.txt`](../requirements.txt) with Python 3.11.
2. Run `python src/pipeline.py --skip-ingestion` to reproduce the checked-in pipeline from local snapshots.
3. Run `streamlit run dashboard/app.py` for the interactive dashboard, or open the [static dashboard](../dashboard/panel_dashboard.html).
4. Read the [business report](../reports/business_insights.md) together with the data and model cards before interpreting ROI results.

The [CI workflow](../.github/workflows/ci.yml) compiles the Python modules and runs the reproducible pipeline. The [platform health report](../reports/platform_health.md) checks artifact presence; its `100/100` score is **not** predictive performance.

## What this project demonstrates

- Joining heterogeneous data into an inspectable modeling workflow.
- Reporting baselines, uncertainty, and limitations alongside a usable interface.
- Separating real historical outcomes from simulated commercial targets.

## What it does not establish

- Real sponsor ROI, causal campaign lift, or a production recommendation policy.
- Generalization to unseen commercial campaigns without licensed campaign data.
- A model improvement over industry recommendation systems.

The next evidence step is replacing the commercial proxy label with permissioned campaign outcomes and rerunning model selection and evaluation. Until then, the strongest supported claim is **a reproducible ML/data product prototype**.
