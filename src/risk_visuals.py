from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
FIGURE_DIR = ROOT / "assets" / "figures"


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    uncertainty = pd.read_csv(DATA_DIR / "roi_uncertainty.csv")
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv")
    return uncertainty, scenarios


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def save_uncertainty_heatmap(uncertainty: pd.DataFrame) -> Path:
    pivot = (
        uncertainty.pivot_table(
            index="stage",
            columns="risk_level",
            values="conformal_interval_width",
            aggfunc="mean",
            fill_value=0,
        )
        .reindex(columns=["low", "medium", "high"], fill_value=0)
        .round(3)
    )
    fig, ax = plt.subplots(figsize=(9.5, 5.4), dpi=160)
    im = ax.imshow(pivot.to_numpy(), cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)), labels=pivot.columns)
    ax.set_yticks(range(len(pivot.index)), labels=pivot.index)
    ax.set_title("ROI Uncertainty Heatmap: stage x risk level", weight="bold")
    ax.set_xlabel("Risk level")
    ax.set_ylabel("Match stage")
    for y in range(len(pivot.index)):
        for x in range(len(pivot.columns)):
            ax.text(x, y, f"{pivot.iloc[y, x]:.3f}", ha="center", va="center", color="#111827", fontsize=9)
    fig.colorbar(im, ax=ax, label="Average interval width")
    fig.tight_layout()
    out = REPORT_DIR / "uncertainty_heatmap.png"
    fig.savefig(out, bbox_inches="tight")
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / "uncertainty_heatmap.png", bbox_inches="tight")
    plt.close(fig)
    return out


def save_risk_marginal_benefit(scenarios: pd.DataFrame) -> Path:
    summary = (
        scenarios.groupby(["strategy_type", "scenario"], as_index=False)
        .agg(avg_roi_lift=("roi_lift", "mean"), avg_risk=("risk_score", "mean"), avg_roi=("scenario_roi", "mean"))
        .sort_values("avg_roi_lift", ascending=False)
    )
    colors = {"conservative": "#2457c5", "balanced": "#0f8b6f", "aggressive": "#f28c28"}
    fig, ax = plt.subplots(figsize=(9.5, 5.6), dpi=160)
    for strategy, group in summary.groupby("strategy_type"):
        ax.scatter(
            group["avg_risk"],
            group["avg_roi_lift"],
            s=(group["avg_roi"] * 42).clip(lower=80),
            alpha=0.82,
            color=colors.get(strategy, "#68768a"),
            label=strategy,
            edgecolor="white",
            linewidth=1.2,
        )
        for _, row in group.iterrows():
            ax.annotate(row["scenario"].replace("_", " "), (row["avg_risk"], row["avg_roi_lift"]), xytext=(5, 5), textcoords="offset points", fontsize=8)
    ax.axhline(0, color="#9aa6b2", linewidth=1)
    ax.set_title("Risk vs Marginal Benefit", weight="bold")
    ax.set_xlabel("Average scenario risk score")
    ax.set_ylabel("Average ROI lift")
    ax.grid(True, alpha=0.25)
    ax.legend(title="Strategy")
    fig.tight_layout()
    out = REPORT_DIR / "risk_marginal_benefit.png"
    fig.savefig(out, bbox_inches="tight")
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / "risk_marginal_benefit.png", bbox_inches="tight")
    plt.close(fig)
    summary.to_csv(REPORT_DIR / "risk_marginal_benefit.csv", index=False)
    return out


def write_markdown(uncertainty: pd.DataFrame, scenarios: pd.DataFrame) -> None:
    high_width = uncertainty.sort_values("conformal_interval_width", ascending=False).head(5)
    scenarios = scenarios.copy()
    scenarios["roi_ci_width"] = scenarios["roi_ci_high"] - scenarios["roi_ci_low"]
    scenario_summary = (
        scenarios.groupby("strategy_type", as_index=False)
        .agg(avg_roi_lift=("roi_lift", "mean"), avg_risk=("risk_score", "mean"), avg_ci_width=("roi_ci_width", "mean"))
        .round(3)
    )
    lines = [
        "# Risk Visual Explanation",
        "",
        "## uncertainty_heatmap.png",
        "",
        "![Uncertainty heatmap](uncertainty_heatmap.png)",
        "",
        "**What:** Average ROI interval width by match stage and risk level.",
        "",
        "**Why:** Wider intervals indicate less certain sponsor ROI forecasts and should receive more analyst review before budget approval.",
        "",
        "**Business Takeaway:** Use this heatmap as a budget-control layer. High-width cells should default to conservative or performance-based sponsor packages.",
        "",
        "## risk_marginal_benefit.png",
        "",
        "![Risk marginal benefit](risk_marginal_benefit.png)",
        "",
        "**What:** Scenario ROI lift plotted against average scenario risk.",
        "",
        "**Why:** A high-lift strategy is not automatically better if its risk score grows faster than marginal benefit.",
        "",
        "**Business Takeaway:** Favor strategies in the upper-left zone: positive lift with moderate risk. Aggressive strategies need a clear attention or stage premium reason.",
        "",
        "## Highest Interval-Width Cases",
        "",
        markdown_table(high_width[["match_id", "team_a", "team_b", "stage", "risk_level", "conformal_interval_width"]]),
        "",
        "## Strategy Risk Summary",
        "",
        markdown_table(scenario_summary),
    ]
    (REPORT_DIR / "risk_visuals.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    uncertainty, scenarios = load_inputs()
    heatmap = save_uncertainty_heatmap(uncertainty)
    benefit = save_risk_marginal_benefit(scenarios)
    write_markdown(uncertainty, scenarios)
    print({"uncertainty_heatmap": str(heatmap), "risk_marginal_benefit": str(benefit)})


if __name__ == "__main__":
    main()
