from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
FIGURE_DIR = ROOT / "assets" / "figures"

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


def finish(fig: plt.Figure, filename: str) -> Path:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    out = FIGURE_DIR / filename
    fig.savefig(out, bbox_inches="tight", dpi=300)
    report_out = REPORT_DIR / filename
    fig.savefig(report_out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return out


def markdown_table(df: pd.DataFrame, max_rows: int = 12) -> str:
    view = df.head(max_rows)
    headers = list(view.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in view.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def normalize(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce").fillna(0.0)
    lo, hi = float(s.min()), float(s.max())
    if hi <= lo:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - lo) / (hi - lo)


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    social = pd.read_csv(DATA_DIR / "social_media.csv") if (DATA_DIR / "social_media.csv").exists() else pd.DataFrame()
    text = pd.read_csv(DATA_DIR / "media_text_corpus.csv") if (DATA_DIR / "media_text_corpus.csv").exists() else pd.DataFrame()
    uncertainty = pd.read_csv(DATA_DIR / "roi_uncertainty.csv") if (DATA_DIR / "roi_uncertainty.csv").exists() else pd.DataFrame()
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv") if (DATA_DIR / "scenario_recommendations.csv").exists() else pd.DataFrame()
    gnn = pd.read_csv(REPORT_DIR / "gnn_baseline_node_scores.csv") if (REPORT_DIR / "gnn_baseline_node_scores.csv").exists() else pd.DataFrame()
    return panel, social, text, uncertainty, scenarios, gnn


def dynamic_roi(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = panel.copy()
    work["cycle"] = (work["year"] // 4) * 4
    work["player_mix"] = pd.cut(
        work["core_player_rating"],
        bins=[0, 68, 75, 82, 100],
        labels=["developing", "solid", "star", "elite"],
        include_lowest=True,
    ).astype(str)
    summary = (
        work.groupby(["cycle", "stage", "player_mix"], as_index=False)
        .agg(
            avg_roi=("predicted_roi", "mean"),
            avg_fanscore=("fan_score_panel", "mean"),
            avg_momentum=("commercial_momentum", "mean"),
            samples=("panel_id", "count"),
        )
        .round(4)
    )
    cycle = work.groupby("cycle", as_index=False).agg(avg_roi=("predicted_roi", "mean"), avg_momentum=("commercial_momentum", "mean"))
    years = cycle["cycle"].to_numpy(dtype=float)
    values = cycle["avg_roi"].to_numpy(dtype=float)
    if len(cycle) >= 2:
        coef = np.polyfit(years, values, deg=1)
        slope, intercept = float(coef[0]), float(coef[1])
    else:
        slope, intercept = 0.0, float(values.mean()) if len(values) else 0.0
    future_years = np.array([2026, 2030, 2034], dtype=float)
    future = pd.DataFrame(
        {
            "cycle": future_years.astype(int),
            "forecast_roi": np.round(intercept + slope * future_years, 4),
            "trend_slope_per_cycle": round(slope * 4, 4),
            "forecast_note": "linear trend over historical/proxy sponsorship panel",
        }
    )
    out = pd.concat(
        [
            cycle.assign(kind="observed").rename(columns={"avg_roi": "roi"})[["cycle", "roi", "kind"]],
            future.rename(columns={"forecast_roi": "roi"}).assign(kind="forecast")[["cycle", "roi", "kind"]],
        ],
        ignore_index=True,
    )
    fig, ax = plt.subplots(figsize=(10.5, 5.7))
    observed = out[out["kind"].eq("observed")]
    forecast = out[out["kind"].eq("forecast")]
    ax.plot(observed["cycle"], observed["roi"], color=PALETTE["green"], marker="o", linewidth=2.8, label="Observed panel ROI")
    ax.plot(forecast["cycle"], forecast["roi"], color=PALETTE["orange"], marker="o", linestyle="--", linewidth=2.5, label="Future forecast")
    ax.fill_between(forecast["cycle"], forecast["roi"] - 0.18, forecast["roi"] + 0.18, color=PALETTE["orange"], alpha=0.16, label="Planning band")
    ax.set_title("Future Event ROI Trend Forecast", loc="left", weight="bold")
    ax.set_xlabel("World Cup cycle")
    ax.set_ylabel("Sponsor ROI")
    ax.grid(axis="y")
    ax.legend()
    finish(fig, "future_roi_trend.png")
    summary.to_csv(DATA_DIR / "dynamic_roi_timeseries.csv", index=False)
    future.to_csv(REPORT_DIR / "future_roi_forecast.csv", index=False)
    return summary, future


def sentiment_event_impact(panel: pd.DataFrame, social: pd.DataFrame, text: pd.DataFrame) -> pd.DataFrame:
    work = panel.copy()
    if not social.empty:
        social_cols = [col for col in ["match_id", "sentiment_score", "engagement_rate", "mentions_k", "share_rate"] if col in social.columns]
        if "match_id" in social_cols:
            social_agg = social[social_cols].groupby("match_id", as_index=False).mean(numeric_only=True)
            work = work.merge(social_agg, on="match_id", how="left")
    if not text.empty:
        text_cols = [col for col in ["match_id", "news_sentiment_score", "text_signal_score", "article_count"] if col in text.columns]
        if "match_id" in text_cols:
            text_agg = text[text_cols].groupby("match_id", as_index=False).mean(numeric_only=True)
            work = work.merge(text_agg, on="match_id", how="left")

    sentiment = work.get("sentiment_score", pd.Series(0.0, index=work.index)).fillna(work.get("news_sentiment_score", 0.0)).fillna(0.0)
    engagement = work.get("engagement_rate", pd.Series(0.0, index=work.index)).fillna(0.0)
    mentions = work.get("mentions_k", pd.Series(0.0, index=work.index)).fillna(work["media_reposts_k"]).fillna(0.0)
    work["attention_sentiment_score"] = 0.42 * normalize(work["event_attention_m"]) + 0.28 * normalize(engagement) + 0.20 * normalize(mentions) + 0.10 * normalize(sentiment)
    roi_base = work.groupby("stage")["predicted_roi"].transform("median")
    work["event_roi_delta"] = work["predicted_roi"] - roi_base
    work["event_type"] = np.select(
        [
            (sentiment < -0.15) & (work["event_attention_m"] > work["event_attention_m"].quantile(0.70)),
            (sentiment > 0.20) & (work["event_attention_m"] > work["event_attention_m"].quantile(0.70)),
            work["stage"].astype(str).str.contains("knockout|final", case=False, na=False),
        ],
        ["negative_sentiment_spike", "positive_sentiment_spike", "stage_attention_spike"],
        default="baseline_attention",
    )
    event = (
        work.groupby(["event_type", "stage"], as_index=False)
        .agg(
            avg_roi_delta=("event_roi_delta", "mean"),
            avg_roi=("predicted_roi", "mean"),
            avg_attention_sentiment=("attention_sentiment_score", "mean"),
            avg_conversion=("roi_per_million_spend", "mean"),
            samples=("panel_id", "count"),
        )
        .round(4)
    )
    chain = (
        work.groupby("stage", as_index=False)
        .agg(
            media_exposure=("event_attention_m", "mean"),
            sentiment=("attention_sentiment_score", "mean"),
            fan_conversion=("roi_per_million_spend", "mean"),
            avg_roi=("predicted_roi", "mean"),
        )
        .round(4)
    )
    event.to_csv(REPORT_DIR / "sentiment_event_roi_impact.csv", index=False)
    chain.to_csv(REPORT_DIR / "attention_sentiment_conversion_chain.csv", index=False)

    fig, ax = plt.subplots(figsize=(11, 6.0))
    plot_data = event.sort_values("avg_roi_delta")
    labels = plot_data["event_type"] + "\n" + plot_data["stage"].astype(str)
    colors = np.where(plot_data["avg_roi_delta"] >= 0, PALETTE["green"], PALETTE["red"])
    ax.barh(labels, plot_data["avg_roi_delta"], color=colors, edgecolor="white")
    ax.axvline(0, color=PALETTE["ink"], linewidth=1)
    ax.set_title("Key Event Sentiment Impact on ROI", loc="left", weight="bold")
    ax.set_xlabel("ROI delta vs stage median")
    ax.grid(axis="x")
    finish(fig, "sentiment_event_roi_impact.png")
    return event


def resource_optimization(panel: pd.DataFrame, uncertainty: pd.DataFrame) -> pd.DataFrame:
    base = panel.groupby("sponsor", as_index=False).agg(
        avg_roi=("predicted_roi", "mean"),
        avg_spend=("sponsor_spend_m", "mean"),
        avg_attention=("event_attention_m", "mean"),
        brand_fit=("brand_fit", "mean"),
        activation=("activation_quality", "mean"),
    )
    if not uncertainty.empty:
        risk = uncertainty.groupby("stage", as_index=False).agg(avg_risk=("risk_score", "mean"))
        stage_risk = float(risk["avg_risk"].mean())
    else:
        stage_risk = 0.35
    budgets = [10, 25, 50, 100]
    media_levels = [0.8, 1.0, 1.25, 1.5]
    rows = []
    for _, sponsor in base.iterrows():
        for budget in budgets:
            for media in media_levels:
                efficiency = sponsor["avg_roi"] * (0.58 + 0.18 * media + 0.14 * sponsor["brand_fit"] + 0.10 * sponsor["activation"])
                saturation = 1 - np.exp(-budget / max(float(sponsor["avg_spend"]) * 1.8, 1.0))
                risk_penalty = 1 - min(stage_risk * (1.08 if media > 1.2 else 0.92), 0.72)
                expected_roi = efficiency * saturation * risk_penalty
                rows.append(
                    {
                        "sponsor": sponsor["sponsor"],
                        "budget_m": budget,
                        "media_multiplier": media,
                        "expected_roi": round(float(expected_roi), 4),
                        "risk_adjusted_roi": round(float(expected_roi * risk_penalty), 4),
                        "risk_penalty": round(float(1 - risk_penalty), 4),
                        "recommendation": "scale" if expected_roi > base["avg_roi"].median() else "test_or_hold",
                    }
                )
    opt = pd.DataFrame(rows)
    top = opt.sort_values("risk_adjusted_roi", ascending=False).groupby("budget_m", as_index=False).head(5)
    opt.to_csv(REPORT_DIR / "resource_optimization_recommendations.csv", index=False)
    top.to_csv(REPORT_DIR / "resource_optimization_top_budget_mix.csv", index=False)

    pivot = opt.pivot_table(index="budget_m", columns="media_multiplier", values="risk_adjusted_roi", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    im = ax.imshow(pivot.values, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"{x:.2f}x" for x in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([f"${int(x)}M" for x in pivot.index])
    ax.set_title("Budget and Media Sensitivity Analysis", loc="left", weight="bold")
    ax.set_xlabel("Media multiplier")
    ax.set_ylabel("Budget")
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            ax.text(j, i, f"{pivot.values[i, j]:.2f}", ha="center", va="center", fontsize=9, color=PALETTE["ink"])
    fig.colorbar(im, ax=ax, label="Risk-adjusted ROI")
    finish(fig, "budget_media_sensitivity.png")
    return top


def graph_attention(panel: pd.DataFrame, gnn: pd.DataFrame) -> pd.DataFrame:
    if gnn.empty:
        return pd.DataFrame()
    sponsors = panel.groupby("sponsor", as_index=False).agg(
        avg_roi=("predicted_roi", "mean"),
        avg_brand_fit=("brand_fit", "mean"),
        avg_attention=("event_attention_m", "mean"),
    )
    sponsor_scores = gnn[gnn["node_type"].eq("sponsor")].copy()
    sponsor_scores["sponsor"] = sponsor_scores["node"].str.replace("sponsor:", "", regex=False)
    out = sponsor_scores.merge(sponsors, on="sponsor", how="left")
    out["attention_roi_contribution"] = (
        0.46 * normalize(out["combined_graph_score"])
        + 0.24 * normalize(out["avg_roi"])
        + 0.18 * normalize(out["avg_attention"])
        + 0.12 * normalize(out["avg_brand_fit"])
    ).round(6)
    out = out.sort_values("attention_roi_contribution", ascending=False)
    out.to_csv(REPORT_DIR / "graph_attention_roi_contributions.csv", index=False)

    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    view = out.head(12).iloc[::-1]
    ax.barh(view["sponsor"], view["attention_roi_contribution"], color=PALETTE["purple"])
    ax.set_title("Graph Attention ROI Contribution", loc="left", weight="bold")
    ax.set_xlabel("Attention-weighted contribution score")
    ax.grid(axis="x")
    finish(fig, "graph_attention_roi_contribution.png")

    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.scatter(out["combined_graph_score"], out["avg_roi"], s=out["avg_attention"] * 3, c=out["attention_roi_contribution"], cmap="viridis", alpha=0.82, edgecolor="white")
    for _, row in out.head(8).iterrows():
        ax.text(row["combined_graph_score"], row["avg_roi"], row["sponsor"], fontsize=8)
    ax.set_title("Sponsor Influence and ROI Network", loc="left", weight="bold")
    ax.set_xlabel("GCN / GraphSAGE combined graph score")
    ax.set_ylabel("Average sponsor ROI")
    ax.grid(True)
    finish(fig, "sponsor_player_influence_network.png")
    return out


def extreme_scenarios(panel: pd.DataFrame, uncertainty: pd.DataFrame) -> pd.DataFrame:
    base = panel.groupby(["team", "sponsor"], as_index=False).agg(
        baseline_roi=("predicted_roi", "mean"),
        avg_attention=("event_attention_m", "mean"),
        avg_risk_proxy=("roi_per_million_spend", "std"),
    )
    avg_std = float(uncertainty["monte_carlo_std"].mean()) if not uncertainty.empty and "monte_carlo_std" in uncertainty else 0.14
    shock_defs = [
        ("key_player_injury", -0.14, 1.24, "Player availability shock lowers expected activation."),
        ("sentiment_crisis", -0.18, 1.42, "Negative social/news sentiment requires defensive spend."),
        ("sponsor_policy_change", -0.10, 1.18, "Policy restriction reduces activation quality."),
        ("positive_viral_moment", 0.16, 1.28, "Positive viral attention can lift upside but increases volatility."),
    ]
    rows = []
    for _, row in base.sort_values("baseline_roi", ascending=False).head(120).iterrows():
        for scenario, lift, risk_mult, reason in shock_defs:
            roi = float(row["baseline_roi"]) * (1 + lift)
            interval = avg_std * risk_mult * 1.96
            rows.append(
                {
                    "team": row["team"],
                    "sponsor": row["sponsor"],
                    "extreme_scenario": scenario,
                    "baseline_roi": round(float(row["baseline_roi"]), 4),
                    "scenario_roi": round(roi, 4),
                    "roi_ci_low": round(roi - interval, 4),
                    "roi_ci_high": round(roi + interval, 4),
                    "risk_interval_width": round(interval * 2, 4),
                    "recommendation_reason": reason,
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(REPORT_DIR / "extreme_scenario_roi_risk.csv", index=False)
    summary = out.groupby("extreme_scenario", as_index=False).agg(avg_roi=("scenario_roi", "mean"), avg_width=("risk_interval_width", "mean"))
    fig, ax = plt.subplots(figsize=(10, 5.7))
    ax.errorbar(summary["extreme_scenario"], summary["avg_roi"], yerr=summary["avg_width"] / 2, fmt="o", color=PALETTE["blue"], ecolor=PALETTE["red"], capsize=5, linewidth=2.2)
    ax.set_title("Extreme Scenario ROI and Risk Intervals", loc="left", weight="bold")
    ax.set_xlabel("Scenario")
    ax.set_ylabel("Scenario ROI")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y")
    finish(fig, "extreme_scenario_roi_intervals.png")
    return out


def commercial_metrics(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy()
    out["media_value_index"] = (0.62 * normalize(out["event_attention_m"]) + 0.38 * normalize(out["media_reposts_k"])).round(6)
    out["fan_conversion_rate"] = (0.55 * normalize(out["fan_score_panel"]) + 0.45 * normalize(out["roi_per_million_spend"])).round(6)
    out["social_spread_index"] = (0.52 * normalize(out["media_reposts_k"]) + 0.30 * normalize(out["player_followers_m"]) + 0.18 * normalize(out["commercial_momentum"])).round(6)
    out["brand_influence_score"] = (0.45 * normalize(out["brand_fit"]) + 0.35 * normalize(out["sponsor_power_index"]) + 0.20 * normalize(out["activation_quality"])).round(6)
    out["commercial_decision_score"] = (
        0.36 * normalize(out["predicted_roi"])
        + 0.22 * out["media_value_index"]
        + 0.18 * out["fan_conversion_rate"]
        + 0.14 * out["social_spread_index"]
        + 0.10 * out["brand_influence_score"]
    ).round(6)
    cols = [
        "panel_id",
        "team",
        "sponsor",
        "stage",
        "predicted_roi",
        "media_value_index",
        "fan_conversion_rate",
        "social_spread_index",
        "brand_influence_score",
        "commercial_decision_score",
    ]
    decision = out[cols].sort_values("commercial_decision_score", ascending=False)
    decision.to_csv(DATA_DIR / "commercial_decision_metrics.csv", index=False)
    decision.head(120).to_csv(REPORT_DIR / "commercial_decision_metrics_top.csv", index=False)

    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    top = decision.head(18).iloc[::-1]
    labels = top["team"] + " x " + top["sponsor"]
    ax.barh(labels, top["commercial_decision_score"], color=PALETTE["green"])
    ax.set_title("Integrated Commercial Decision Score", loc="left", weight="bold")
    ax.set_xlabel("Composite score: ROI + media value + conversion + spread + brand")
    ax.grid(axis="x")
    finish(fig, "commercial_decision_scorecard.png")
    return decision


def generated_reports(
    future: pd.DataFrame,
    event: pd.DataFrame,
    opt: pd.DataFrame,
    attention: pd.DataFrame,
    extreme: pd.DataFrame,
    decision: pd.DataFrame,
) -> None:
    lines = [
        "# Deep Analysis Landing Report",
        "",
        "## Executive Summary",
        "",
        "WorldCupROI now includes dynamic ROI forecasting, sentiment-event impact analysis, budget/media optimization, graph attention-style influence scoring, extreme scenario stress tests, and integrated commercial decision metrics.",
        "",
        "## Key Figures",
        "",
        "| Figure | Business question |",
        "| --- | --- |",
        "| ![Future ROI](../assets/figures/future_roi_trend.png) | How is sponsor ROI expected to evolve across future World Cup cycles? |",
        "| ![Sentiment Event Impact](../assets/figures/sentiment_event_roi_impact.png) | Which attention and sentiment events move ROI up or down? |",
        "| ![Budget Sensitivity](../assets/figures/budget_media_sensitivity.png) | Which budget/media mix maximizes risk-adjusted ROI? |",
        "| ![Graph Attention](../assets/figures/graph_attention_roi_contribution.png) | Which sponsor nodes contribute most through graph influence? |",
        "| ![Extreme Scenarios](../assets/figures/extreme_scenario_roi_intervals.png) | How do injury, sentiment, policy, and viral shocks change ROI risk? |",
        "| ![Commercial Scorecard](../assets/figures/commercial_decision_scorecard.png) | Which opportunities score best across ROI and business metrics? |",
        "",
        "## Future ROI Forecast",
        "",
        markdown_table(future, max_rows=10),
        "",
        "## Sentiment Event Impact",
        "",
        markdown_table(event.sort_values("avg_roi_delta", ascending=False), max_rows=12),
        "",
        "## Resource Optimization",
        "",
        markdown_table(opt.sort_values("risk_adjusted_roi", ascending=False), max_rows=12),
        "",
        "## Graph Attention Sponsor Contributions",
        "",
        markdown_table(attention.head(12), max_rows=12) if not attention.empty else "Graph attention baseline unavailable.",
        "",
        "## Extreme Scenario Stress Test",
        "",
        markdown_table(extreme.sort_values("risk_interval_width", ascending=False), max_rows=12),
        "",
        "## Integrated Commercial Decision Score",
        "",
        markdown_table(decision.head(12), max_rows=12),
        "",
        "## Landing Recommendations",
        "",
        "- Use the future ROI trend as a planning prior, not a guaranteed forecast.",
        "- Tie budget increases to both media multiplier sensitivity and risk-adjusted ROI.",
        "- Treat sentiment crisis and key-player injury scenarios as pre-approval triggers for contingency spend.",
        "- Combine SHAP-style tabular drivers with graph attention scores before selecting anchor sponsor partnerships.",
    ]
    (REPORT_DIR / "deep_analysis_landing_report.md").write_text("\n".join(lines), encoding="utf-8")

    pdf_path = REPORT_DIR / "deep_analysis_landing_report.pdf"
    figures = [
        ("Future Event ROI Trend Forecast", FIGURE_DIR / "future_roi_trend.png"),
        ("Key Event Sentiment Impact on ROI", FIGURE_DIR / "sentiment_event_roi_impact.png"),
        ("Budget and Media Sensitivity", FIGURE_DIR / "budget_media_sensitivity.png"),
        ("Graph Attention ROI Contribution", FIGURE_DIR / "graph_attention_roi_contribution.png"),
        ("Extreme Scenario ROI Intervals", FIGURE_DIR / "extreme_scenario_roi_intervals.png"),
        ("Commercial Decision Scorecard", FIGURE_DIR / "commercial_decision_scorecard.png"),
    ]
    with PdfPages(pdf_path) as pdf:
        cover = plt.figure(figsize=(11, 8.5))
        cover.text(0.06, 0.86, "WorldCupROI Deep Analysis Landing Report", fontsize=22, weight="bold")
        cover.text(0.06, 0.78, "Dynamic ROI, sentiment impact, budget optimization, graph attention, extreme scenarios, and commercial scorecard.", fontsize=12)
        cover.text(0.06, 0.66, "Top recommendation: combine ROI forecasts with uncertainty and relationship influence before scaling sponsor spend.", fontsize=12)
        cover.text(0.06, 0.58, "Generated from committed local artifacts; demo mode remains runnable without external APIs.", fontsize=11, color=PALETTE["muted"])
        cover.patch.set_visible(False)
        pdf.savefig(cover, bbox_inches="tight")
        plt.close(cover)
        for title, path in figures:
            if not path.exists():
                continue
            fig = plt.figure(figsize=(11, 8.5))
            fig.text(0.06, 0.94, title, fontsize=17, weight="bold")
            image = plt.imread(path)
            ax = fig.add_axes([0.06, 0.08, 0.88, 0.78])
            ax.imshow(image)
            ax.axis("off")
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)


def write_figure_notes() -> None:
    notes = [
        ("future_roi_trend.png", "Future Event ROI Trend Forecast", "Shows historical cycle ROI and future cycle forecasts with a planning band.", "It makes time dependence visible instead of treating every tournament as identical.", "Use as a budget planning prior for 2026/2030/2034 sponsorship cycles."),
        ("sentiment_event_roi_impact.png", "Sentiment Event Impact on ROI", "Compares ROI deltas for positive, negative, and stage-driven attention events.", "Sentiment shocks can change conversion quality even when exposure is high.", "Prepare contingency messaging and spend limits around high-attention negative events."),
        ("budget_media_sensitivity.png", "Budget and Media Sensitivity", "Maps risk-adjusted ROI under budget and media multiplier combinations.", "Optimization converts model output into a resource allocation recommendation.", "Scale spend where the sensitivity surface is high and stable."),
        ("graph_attention_roi_contribution.png", "Graph Attention ROI Contribution", "Ranks sponsor nodes by graph attention-style contribution to ROI.", "It explains relationship leverage beyond flat sponsor ranking.", "Use high-contribution sponsors as anchor nodes in portfolio planning."),
        ("extreme_scenario_roi_intervals.png", "Extreme Scenario ROI and Risk Intervals", "Stress-tests key player injury, sentiment crisis, policy change, and viral upside.", "Extreme cases reveal downside intervals that average ROI hides.", "Pre-approve response playbooks before the tournament starts."),
        ("commercial_decision_scorecard.png", "Integrated Commercial Decision Score", "Combines ROI, media value, fan conversion, social spread, and brand influence.", "A sponsor decision is multi-objective; ROI alone is too narrow.", "Prioritize high composite score opportunities, then review risk intervals."),
    ]
    lines = ["# Deep Analysis Figure Notes", ""]
    for filename, title, what, why, takeaway in notes:
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
    (FIGURE_DIR / "deep_analysis_figure_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    setup_style()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel, social, text, uncertainty, scenarios, gnn = load_inputs()
    _, future = dynamic_roi(panel)
    event = sentiment_event_impact(panel, social, text)
    opt = resource_optimization(panel, uncertainty)
    attention = graph_attention(panel, gnn)
    extreme = extreme_scenarios(panel, uncertainty)
    decision = commercial_metrics(panel)
    generated_reports(future, event, opt, attention, extreme, decision)
    write_figure_notes()
    print(
        {
            "future_rows": len(future),
            "event_rows": len(event),
            "optimization_rows": len(opt),
            "graph_attention_rows": len(attention),
            "extreme_rows": len(extreme),
            "decision_rows": len(decision),
        }
    )


if __name__ == "__main__":
    main()
