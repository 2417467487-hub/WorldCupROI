from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "assets" / "figures"
REPORT_DIR = ROOT / "reports"

COLORS = {
    "blue": "#0072B2",
    "green": "#009E73",
    "orange": "#E69F00",
    "red": "#D55E00",
    "purple": "#7B61FF",
    "ink": "#111827",
    "muted": "#4B5563",
    "grid": "#D1D5DB",
}


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "font.family": "DejaVu Sans",
            "axes.titlesize": 15,
            "axes.labelsize": 11,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "axes.edgecolor": COLORS["grid"],
            "axes.labelcolor": COLORS["ink"],
            "text.color": COLORS["ink"],
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["muted"],
            "grid.color": COLORS["grid"],
            "grid.alpha": 0.55,
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG_DIR / name, dpi=300, bbox_inches="tight")
    plt.close(fig)


def read(name: str) -> pd.DataFrame:
    path = REPORT_DIR / name
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def sponsor_optimization() -> None:
    df = read("sponsor_optimization_summary.csv")
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(df["budget_cap_m"], df["expected_portfolio_roi"], marker="o", linewidth=2.5, color=COLORS["green"], label="Expected ROI")
    ax.plot(df["budget_cap_m"], df["risk_adjusted_roi"], marker="s", linewidth=2.5, color=COLORS["blue"], label="Risk-adjusted ROI")
    ax.set_title("Sponsor Optimization Under Budget Constraints")
    ax.set_xlabel("Budget cap (USD millions)")
    ax.set_ylabel("Portfolio ROI")
    ax.grid(True, axis="y")
    ax.legend(frameon=True)
    save(fig, "decision_sponsor_optimization.png")


def causal_effects() -> None:
    df = read("causal_effect_estimates.csv")
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 4.8))
    y = np.arange(len(df))
    ax.barh(y - 0.18, df["correlation_with_roi"], height=0.34, color=COLORS["orange"], label="Correlation")
    ax.barh(y + 0.18, df["causal_effect_residualized"], height=0.34, color=COLORS["blue"], label="Residualized causal effect")
    ax.set_yticks(y)
    ax.set_yticklabels(df["treatment"])
    ax.axvline(0, color=COLORS["ink"], linewidth=0.8)
    ax.set_title("Correlation vs Causal Evidence")
    ax.set_xlabel("Effect / association score")
    ax.grid(True, axis="x")
    ax.legend(frameon=True)
    save(fig, "decision_causal_effects.png")


def funnel_decay() -> None:
    df = read("funnel_behavior_paths.csv")
    if df.empty:
        return
    top = df.sort_values("ROI", ascending=False).head(6)
    stages = ["Exposure", "Attention", "Engagement", "Conversion", "ROI"]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for _, row in top.iterrows():
        ax.plot(stages, [row[s] for s in stages], marker="o", linewidth=1.8, alpha=0.75, label=f"{row['team']} x {row['sponsor']}")
    ax.set_title("Fan Funnel Decay Paths")
    ax.set_ylabel("Normalized score")
    ax.grid(True, axis="y")
    ax.legend(fontsize=7, frameon=True)
    save(fig, "decision_funnel_decay.png")


def graph_learning() -> None:
    df = read("graph_learning_link_predictions.csv")
    if df.empty:
        return
    top = df.head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    labels = top["team"].astype(str) + " x " + top["sponsor"].astype(str)
    ax.barh(labels, top["future_sponsor_roi_prediction"], color=COLORS["green"], edgecolor="white")
    ax.set_title("Graph Learning Future Sponsor ROI Prediction")
    ax.set_xlabel("Predicted future sponsor ROI")
    ax.grid(True, axis="x")
    save(fig, "decision_graph_learning.png")


def counterfactual_and_tail_risk() -> None:
    cf = read("counterfactual_summary.csv")
    risk = read("tail_risk_decisions.csv")
    if cf.empty:
        return
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
    colors = [COLORS["green"] if x > 0 else COLORS["red"] for x in cf["avg_delta"]]
    axes[0].bar(cf["counterfactual"], cf["avg_delta"], color=colors, edgecolor="white")
    axes[0].set_title("Counterfactual ROI Delta")
    axes[0].set_ylabel("Average ROI delta")
    axes[0].tick_params(axis="x", rotation=35)
    axes[0].grid(True, axis="y")
    if not risk.empty:
        top = risk.sort_values("risk_sensitive_roi", ascending=False).head(8).iloc[::-1]
        labels = top["team"].astype(str) + " x " + top["sponsor"].astype(str)
        axes[1].barh(labels, top["risk_sensitive_roi"], color=COLORS["blue"], edgecolor="white")
        axes[1].set_title("Tail-Risk Sensitive Ranking")
        axes[1].set_xlabel("Risk-sensitive ROI")
        axes[1].grid(True, axis="x")
    save(fig, "decision_counterfactual_tail_risk.png")


def main() -> None:
    setup_style()
    sponsor_optimization()
    causal_effects()
    funnel_decay()
    graph_learning()
    counterfactual_and_tail_risk()
    print("Generated decision intelligence figures.")


if __name__ == "__main__":
    main()
