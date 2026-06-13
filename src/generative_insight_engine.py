from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def top_rows(path: Path, columns: list[str], n: int = 5) -> str:
    if not path.exists():
        return "Not available."
    df = pd.read_csv(path)
    cols = [c for c in columns if c in df.columns]
    if not cols:
        return "Not available."
    return markdown_table(df[cols].head(n))


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Causal Sports Intelligence Executive Report",
        "",
        "## Executive Thesis",
        "",
        "WorldCupROI is upgraded from an ROI prediction system into a causal decision and optimization platform. The system now separates correlation from causation, recommends budget allocation, models user behavior pathways, evaluates counterfactual interventions, tracks temporal dynamics and translates graph influence into sponsor strategy.",
        "",
        "## Causal Findings",
        "",
        top_rows(REPORT_DIR / "causal_treatment_effects.csv", ["label", "standardized_effect", "ci_low", "ci_high", "method"], 8),
        "",
        "## Optimization Recommendations",
        "",
        top_rows(REPORT_DIR / "optimized_sponsor_allocation.csv", ["allocation_rank", "sponsor", "team", "allocated_budget_m", "expected_roi", "utility_per_m"], 8),
        "",
        "## User Behavior Funnel",
        "",
        top_rows(REPORT_DIR / "user_behavior_funnel.csv", ["sponsor", "stage", "attention_rate", "engagement_rate", "conversion_rate", "predicted_roi"], 8),
        "",
        "## Counterfactual Risk",
        "",
        top_rows(REPORT_DIR / "counterfactual_interventions.csv", ["scenario", "baseline_roi", "counterfactual_roi", "roi_delta", "roi_low", "roi_high"], 8),
        "",
        "## Graph Learning",
        "",
        top_rows(REPORT_DIR / "graph_learning_node_influence.csv", ["node", "node_type", "hgt_influence_proxy"], 8),
        "",
        "## Sponsor Investment Recommendations",
        "",
        top_rows(REPORT_DIR / "sponsor_investment_recommendations.csv", ["sponsor", "team", "expected_roi", "decision_score", "risk_level", "recommendation"], 10),
        "",
        "## Analyst Recommendation",
        "",
        "Use ROI prediction as the forecasting layer, not the final decision. Investment decisions should be made only after checking causal effect direction, funnel conversion efficiency, counterfactual downside and graph influence concentration.",
    ]
    out = REPORT_DIR / "causal_sports_intelligence_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved generative insight report to {out}")


if __name__ == "__main__":
    main()
