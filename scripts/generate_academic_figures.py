from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
FIGURE_DIR = ROOT / "assets" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "green": "#009E73",
    "blue": "#0072B2",
    "sky": "#56B4E9",
    "orange": "#E69F00",
    "red": "#D55E00",
    "purple": "#7B61FF",
    "ink": "#111827",
    "muted": "#4B5563",
    "grid": "#D1D5DB",
}

FIGURE_NOTES = {
    "model_performance_comparison.png": (
        "Model Performance Comparison",
        "Compares trained baseline and benchmark models on their primary evaluation metrics.",
        "It reveals whether the current model choice is a stable analytical baseline or only a weak placeholder.",
        "Use the benchmark spread to decide which model family deserves production tuning first.",
    ),
    "roi_feature_importance_shap.png": (
        "ROI Feature Importance / SHAP",
        "Ranks the strongest sponsor ROI drivers using SHAP-style feature contribution scores.",
        "Explainability keeps ROI recommendations auditable and helps detect proxy-label overdependence.",
        "Improve brand heat, sponsor-team fit, media exposure, and activation quality before scaling spend.",
    ),
    "sponsor_roi_ranking.png": (
        "Sponsor ROI Ranking",
        "Ranks sponsors by predicted commercial ROI and network influence evidence.",
        "A sponsor can look attractive either because expected ROI is high or because relationship influence is broad.",
        "Prioritize sponsors that combine high ROI with strong team-player-network leverage.",
    ),
    "scenario_roi_lift.png": (
        "Scenario ROI Lift",
        "Shows conservative, balanced, and aggressive strategy lift against the baseline.",
        "Scenario analysis turns the model from prediction into a decision simulator.",
        "Select aggressive strategies only when lift is positive and risk remains tolerable.",
    ),
    "monte_carlo_risk_distribution.png": (
        "Monte Carlo Risk Distribution",
        "Shows the distribution of Monte Carlo ROI standard deviation and risk scores.",
        "The spread of risk is often more important than average ROI for sponsorship planning.",
        "Use high-risk tails as triggers for staged spend, insurance clauses, or additional analyst review.",
    ),
    "prediction_interval_conformal.png": (
        "Prediction Interval / Conformal Prediction",
        "Displays ROI point estimates with conformal-style prediction intervals.",
        "Prediction intervals show forecast reliability, not just expected value.",
        "Prefer narrow-interval opportunities when sponsor budgets are constrained.",
    ),
    "sponsor_team_player_network.png": (
        "Sponsor-Team-Player Network",
        "Visualizes sponsor, team, and player relationships as a weighted commercial graph.",
        "Graph position captures activation leverage that flat tables miss.",
        "Use central sponsors and teams as anchor partnerships for campaign portfolios.",
    ),
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
            "axes.edgecolor": PALETTE["grid"],
            "axes.labelcolor": PALETTE["ink"],
            "text.color": PALETTE["ink"],
            "xtick.color": PALETTE["muted"],
            "ytick.color": PALETTE["muted"],
            "grid.color": PALETTE["grid"],
            "grid.alpha": 0.55,
        }
    )


def finish(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / filename, bbox_inches="tight", dpi=300)
    plt.close(fig)


def model_performance() -> None:
    df = pd.read_csv(REPORT_DIR / "model_registry_comparison.csv")
    trained = df[df["status"].eq("trained")].copy()
    trained["score"] = pd.to_numeric(trained["score"], errors="coerce")
    trained["label"] = trained["task"].str.replace("_", " ", regex=False) + "\n" + trained["model"]
    colors = np.where(trained["task"].eq("sponsor_roi"), PALETTE["green"], PALETTE["blue"])
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.barh(trained["label"], trained["score"], color=colors, edgecolor="white", linewidth=1.2)
    ax.set_title("Model Performance Comparison", loc="left", weight="bold")
    ax.set_xlabel("Primary metric score (accuracy for match, R2 for ROI)")
    ax.grid(axis="x")
    ax.invert_yaxis()
    for y, value in enumerate(trained["score"]):
        ax.text(value + 0.015, y, f"{value:.3f}", va="center", fontsize=9)
    finish(fig, "model_performance_comparison.png")


def roi_feature_importance() -> None:
    df = pd.read_csv(REPORT_DIR / "roi_feature_importance.csv").head(14).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.barh(df["feature"].str.replace("_", " ", regex=False), df["importance"], color=PALETTE["green"])
    ax.set_title("ROI Feature Importance / SHAP", loc="left", weight="bold")
    ax.set_xlabel("Mean absolute contribution")
    ax.grid(axis="x")
    finish(fig, "roi_feature_importance_shap.png")


def sponsor_roi_ranking() -> None:
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    influence_path = REPORT_DIR / "sponsor_influence_scores.csv"
    influence = pd.read_csv(influence_path) if influence_path.exists() else pd.DataFrame()
    roi = panel.groupby("sponsor", as_index=False).agg(avg_roi=("predicted_roi", "mean"))
    if not influence.empty:
        influence = influence.assign(sponsor=influence["source"].str.replace("sponsor:", "", regex=False))
        roi = roi.merge(influence[["sponsor", "sponsor_influence"]], on="sponsor", how="left")
    roi["sponsor_influence"] = roi["sponsor_influence"].fillna(roi["sponsor_influence"].median())
    top = roi.sort_values("avg_roi", ascending=False).head(10).iloc[::-1]
    fig, ax1 = plt.subplots(figsize=(10.5, 6.1))
    ax1.barh(top["sponsor"], top["avg_roi"], color=PALETTE["orange"], label="Avg ROI")
    ax1.set_xlabel("Average predicted ROI")
    ax1.grid(axis="x")
    ax2 = ax1.twiny()
    ax2.plot(top["sponsor_influence"], top["sponsor"], color=PALETTE["blue"], marker="o", linewidth=2.4, label="Influence")
    ax2.set_xlabel("Sponsor network influence")
    ax1.set_title("Sponsor ROI Ranking", loc="left", weight="bold")
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="lower right")
    finish(fig, "sponsor_roi_ranking.png")


def scenario_roi_lift() -> None:
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv")
    summary = (
        scenarios.groupby(["strategy_type", "scenario"], as_index=False)
        .agg(avg_lift=("roi_lift", "mean"), avg_risk=("risk_score", "mean"))
        .sort_values("avg_lift")
    )
    color_map = {"conservative": PALETTE["blue"], "balanced": PALETTE["green"], "aggressive": PALETTE["orange"]}
    colors = summary["strategy_type"].map(color_map).fillna(PALETTE["muted"])
    labels = summary["strategy_type"] + " | " + summary["scenario"].str.replace("_", " ", regex=False)
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.barh(labels, summary["avg_lift"], color=colors, edgecolor="white", linewidth=1)
    ax.axvline(0, color=PALETTE["ink"], linewidth=1)
    ax.set_title("Scenario ROI Lift", loc="left", weight="bold")
    ax.set_xlabel("Average ROI lift vs baseline")
    ax.grid(axis="x")
    finish(fig, "scenario_roi_lift.png")


def monte_carlo_risk() -> None:
    risk = pd.read_csv(DATA_DIR / "roi_uncertainty.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4))
    axes[0].hist(risk["monte_carlo_std"], bins=28, color=PALETTE["purple"], edgecolor="white", alpha=0.9)
    axes[0].set_title("Monte Carlo volatility")
    axes[0].set_xlabel("Monte Carlo std")
    axes[0].set_ylabel("Matches")
    axes[0].grid(axis="y")
    axes[1].hist(risk["risk_score"], bins=28, color=PALETTE["red"], edgecolor="white", alpha=0.9)
    axes[1].set_title("Risk score distribution")
    axes[1].set_xlabel("Risk score")
    axes[1].set_ylabel("Matches")
    axes[1].grid(axis="y")
    fig.suptitle("Monte Carlo Risk Distribution", x=0.02, ha="left", weight="bold", fontsize=15)
    finish(fig, "monte_carlo_risk_distribution.png")


def prediction_intervals() -> None:
    risk = pd.read_csv(DATA_DIR / "roi_uncertainty.csv").sort_values("roi_mean", ascending=False).head(45)
    risk = risk.sort_values("roi_mean")
    y = np.arange(len(risk))
    xerr = np.vstack([risk["roi_mean"] - risk["roi_ci_low"], risk["roi_ci_high"] - risk["roi_mean"]])
    fig, ax = plt.subplots(figsize=(10.8, 7.2))
    ax.errorbar(risk["roi_mean"], y, xerr=xerr, fmt="o", color=PALETTE["orange"], ecolor=PALETTE["blue"], elinewidth=1.7, capsize=2.8)
    ax.set_yticks(y[::4])
    ax.set_yticklabels((risk["team_a"] + " vs " + risk["team_b"]).iloc[::4])
    ax.set_title("Prediction Interval / Conformal Prediction", loc="left", weight="bold")
    ax.set_xlabel("Predicted sponsor ROI with interval")
    ax.grid(axis="x")
    finish(fig, "prediction_interval_conformal.png")


def sponsor_network() -> None:
    edges = pd.read_csv(DATA_DIR / "team_player_sponsor_match_edges.csv")
    sponsors = pd.read_csv(REPORT_DIR / "sponsor_influence_scores.csv").head(7)
    keep_sponsors = sponsors["source"].str.replace("sponsor:", "", regex=False).tolist()
    graph_edges = edges[
        edges["source"].isin(keep_sponsors)
        | edges["target"].isin(keep_sponsors)
    ].head(130)
    G = nx.Graph()
    for _, row in graph_edges.iterrows():
        G.add_edge(str(row["source"]), str(row["target"]), weight=float(row.get("weight", 1.0)), edge_type=str(row.get("edge_type", "")))
    degree = dict(G.degree())
    top_nodes = sorted(degree, key=degree.get, reverse=True)[:55]
    G = G.subgraph(top_nodes).copy()
    pos = nx.spring_layout(G, seed=42, k=0.55)
    node_colors = []
    node_sizes = []
    for node in G.nodes:
        if node in keep_sponsors:
            node_colors.append(PALETTE["orange"])
            node_sizes.append(620)
        elif node.startswith("player:") or "Player" in node:
            node_colors.append(PALETTE["purple"])
            node_sizes.append(260)
        else:
            node_colors.append(PALETTE["green"])
            node_sizes.append(360)
    fig, ax = plt.subplots(figsize=(11.5, 8.0))
    nx.draw_networkx_edges(G, pos, ax=ax, width=0.9, alpha=0.25, edge_color=PALETTE["muted"])
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes, linewidths=1.1, edgecolors="white")
    labels = {node: node.replace("player:", "")[:16] for node in G.nodes if node in keep_sponsors or degree.get(node, 0) > 5}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color=PALETTE["ink"], ax=ax)
    ax.set_title("Sponsor-Team-Player Network", loc="left", weight="bold")
    ax.axis("off")
    finish(fig, "sponsor_team_player_network.png")


def write_notes() -> None:
    lines = ["# Academic Figure Notes", ""]
    for filename, (title, what, why, takeaway) in FIGURE_NOTES.items():
        lines.extend(
            [
                f"## {title}",
                "",
                f"![{title}]({filename})",
                "",
                f"**What it shows:** {what}",
                "",
                f"**Why it matters:** {why}",
                "",
                f"**Business takeaway:** {takeaway}",
                "",
            ]
        )
    (FIGURE_DIR / "academic_figure_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    setup_style()
    model_performance()
    roi_feature_importance()
    sponsor_roi_ranking()
    scenario_roi_lift()
    monte_carlo_risk()
    prediction_intervals()
    sponsor_network()
    write_notes()
    print(f"Generated academic figures in {FIGURE_DIR}")


if __name__ == "__main__":
    main()
