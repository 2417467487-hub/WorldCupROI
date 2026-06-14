from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


SCENARIOS = {
    "player_absent": {"roi_multiplier": 0.88, "risk_add": 0.10, "reason": "Core player absence lowers attention and performance confidence."},
    "media_surge": {"roi_multiplier": 1.14, "risk_add": 0.04, "reason": "Paid and earned media surge increases upside but adds volatility."},
    "budget_cut": {"roi_multiplier": 0.93, "risk_add": 0.06, "reason": "Budget cut weakens activation reach and conversion quality."},
    "budget_increase": {"roi_multiplier": 1.08, "risk_add": 0.05, "reason": "Higher spend can lift ROI when brand fit and attention are strong."},
    "negative_news_shock": {"roi_multiplier": 0.82, "risk_add": 0.16, "reason": "Negative sentiment compresses conversion despite exposure."},
}


def markdown_table(df: pd.DataFrame, max_rows: int = 15) -> str:
    view = df.head(max_rows)
    lines = ["| " + " | ".join(view.columns) + " |", "| " + " | ".join(["---"] * len(view.columns)) + " |"]
    for _, row in view.iterrows():
        values = [f"{row[c]:.4f}" if isinstance(row[c], float) else str(row[c]) for c in view.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_counterfactuals(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base = panel.sort_values("predicted_roi", ascending=False).head(250)
    for _, row in base.iterrows():
        for name, config in SCENARIOS.items():
            scenario_roi = float(row["predicted_roi"]) * config["roi_multiplier"]
            risk_width = 0.22 + config["risk_add"]
            rows.append(
                {
                    "team": row["team"],
                    "sponsor": row["sponsor"],
                    "stage": row["stage"],
                    "counterfactual": name,
                    "baseline_roi": round(float(row["predicted_roi"]), 4),
                    "counterfactual_roi": round(scenario_roi, 4),
                    "roi_delta": round(scenario_roi - float(row["predicted_roi"]), 4),
                    "roi_ci_low": round(scenario_roi - risk_width, 4),
                    "roi_ci_high": round(scenario_roi + risk_width, 4),
                    "method": "SCM_synthetic_control_compatible_stress_test",
                    "reason": config["reason"],
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    cf = build_counterfactuals(panel)
    cf.to_csv(REPORT_DIR / "counterfactual_scenarios.csv", index=False)
    summary = (
        cf.groupby("counterfactual", as_index=False)
        .agg(avg_delta=("roi_delta", "mean"), avg_roi=("counterfactual_roi", "mean"), worst_case_roi=("roi_ci_low", "min"))
        .sort_values("avg_delta", ascending=False)
        .round(4)
    )
    summary.to_csv(REPORT_DIR / "counterfactual_summary.csv", index=False)

    lines = [
        "# Counterfactual Engine Report",
        "",
        "## Scope",
        "",
        "Simulate player absence, media change, budget change, and negative news shocks to estimate ROI changes and risk intervals.",
        "",
        "## Method",
        "",
        "Current baseline is SCM/synthetic-control compatible: observed high-ROI sponsor opportunities are perturbed with structured treatment shocks and interval widths. Production upgrade can replace multipliers with synthetic-control donor pools.",
        "",
        "## Scenario Summary",
        "",
        markdown_table(summary),
    ]
    (REPORT_DIR / "counterfactual_engine_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"counterfactual_rows": len(cf)})


if __name__ == "__main__":
    main()
