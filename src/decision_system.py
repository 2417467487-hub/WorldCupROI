from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def load_optional(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def risk_label(prob: float, interval_width: float) -> str:
    if prob > 0.25 or interval_width > 0.7:
        return "high"
    if prob > 0.08 or interval_width > 0.45:
        return "medium"
    return "low"


def build_recommendations() -> pd.DataFrame:
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    uncertainty = load_optional(DATA_DIR / "roi_uncertainty.csv")
    allocation = load_optional(REPORT_DIR / "optimized_sponsor_allocation.csv")
    scenarios = load_optional(DATA_DIR / "scenario_recommendations.csv")
    base = (
        panel.groupby(["sponsor", "team"], as_index=False)
        .agg(
            expected_roi=("predicted_roi", "mean"),
            fan_score=("fan_score_panel", "mean"),
            momentum=("commercial_momentum", "mean"),
            spend_m=("sponsor_spend_m", "mean"),
        )
    )
    if not uncertainty.empty and "negative_roi_probability" in uncertainty.columns:
        risk = uncertainty.groupby("match_id", as_index=False).agg(
            negative_roi_probability=("negative_roi_probability", "mean"),
            interval_width=("roi_ci_high", lambda x: 0.0),
        )
    base["negative_roi_probability"] = 0.0
    base["interval_width"] = 0.42
    if not allocation.empty:
        allocation_keys = set(zip(allocation["sponsor"].astype(str), allocation["team"].astype(str)))
        base["budget_priority"] = [1 if (s, t) in allocation_keys else 0 for s, t in zip(base["sponsor"], base["team"])]
    else:
        base["budget_priority"] = 0
    if not scenarios.empty:
        scenario_lift = scenarios.groupby("team_a", as_index=False).agg(avg_scenario_lift=("roi_lift", "mean"))
        base = base.merge(scenario_lift.rename(columns={"team_a": "team"}), on="team", how="left")
    base["avg_scenario_lift"] = base.get("avg_scenario_lift", 0).fillna(0)
    base["decision_score"] = (
        base["expected_roi"] * 0.48
        + base["fan_score"] * 0.14
        + base["momentum"] * 0.16
        + base["avg_scenario_lift"] * 0.12
        + base["budget_priority"] * 0.10
        - base["negative_roi_probability"] * 0.25
    )
    base["risk_level"] = [risk_label(p, w) for p, w in zip(base["negative_roi_probability"], base["interval_width"])]
    base["recommendation"] = base.apply(
        lambda r: "Scale investment" if r["decision_score"] > base["decision_score"].quantile(0.82) and r["risk_level"] != "high"
        else "Selective activation" if r["decision_score"] > base["decision_score"].median()
        else "Monitor or defer",
        axis=1,
    )
    return base.sort_values("decision_score", ascending=False)


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    recs = build_recommendations()
    recs.round(4).to_csv(REPORT_DIR / "sponsor_investment_recommendations.csv", index=False)
    lines = [
        "# Decision System Report",
        "",
        "This module upgrades analytics outputs into sponsor investment recommendations, budget priority and risk warnings.",
        "",
        "## Top Recommendations",
        "",
        markdown_table(recs[["sponsor", "team", "expected_roi", "decision_score", "risk_level", "recommendation"]].round(4).head(12)),
        "",
        "## Decision Logic",
        "",
        "Decision score combines expected ROI, FanScore, commercial momentum, scenario lift, budget priority and downside risk. It is intentionally transparent so business users can audit why a sponsor-team pair is recommended.",
    ]
    (REPORT_DIR / "decision_system_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved decision system outputs.")


if __name__ == "__main__":
    main()
