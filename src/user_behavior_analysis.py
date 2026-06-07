from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def minmax(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return (series - series.min()) / span


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_user_chain(panel: pd.DataFrame, social: pd.DataFrame) -> pd.DataFrame:
    social_cols = [
        "match_id",
        "hashtag_mentions_k",
        "video_views_m",
        "sentiment_score",
        "engagement_rate",
        "fan_growth_7d_pct",
        "text_signal_score",
        "time_decay_attention",
    ]
    merged = panel.merge(social[social_cols], on="match_id", how="left")
    merged["media_exposure_score"] = (
        0.45 * minmax(merged["event_attention_m"])
        + 0.35 * minmax(merged["media_reposts_k"])
        + 0.20 * minmax(merged["video_views_m"].fillna(0))
    )
    merged["user_attention_score"] = (
        0.48 * minmax(merged["time_decay_attention"].fillna(merged["event_attention_m"]))
        + 0.32 * minmax(merged["hashtag_mentions_k"].fillna(0))
        + 0.20 * minmax(merged["fan_growth_7d_pct"].fillna(0))
    )
    merged["social_interaction_score"] = (
        0.42 * minmax(merged["engagement_rate"].fillna(0))
        + 0.30 * minmax(merged["media_reposts_k"])
        + 0.28 * minmax(merged["sentiment_score"].fillna(0))
    )
    merged["sponsor_conversion_proxy"] = (
        0.38 * minmax(merged["predicted_roi"])
        + 0.26 * minmax(merged["roi_per_million_spend"])
        + 0.22 * minmax(merged["brand_fit"])
        + 0.14 * minmax(merged["activation_quality"])
    )
    merged["funnel_efficiency"] = (
        merged["sponsor_conversion_proxy"]
        / (merged["media_exposure_score"].clip(lower=0.05))
    ).clip(upper=6)
    return merged.round(4)


def persona_label(row: pd.Series) -> str:
    if row["avg_conversion_proxy"] >= 0.62 and row["avg_attention"] >= 0.55:
        return "High-intent global fans"
    if row["avg_social_interaction"] >= 0.58:
        return "Social amplifiers"
    if row["avg_media_exposure"] >= 0.62:
        return "Broadcast-led awareness audience"
    if row["avg_efficiency"] >= 1.25:
        return "Efficient niche sponsor audience"
    return "Developing attention segment"


def build_personas(chain: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        chain.groupby(["team", "attention_segment", "commercial_segment"], as_index=False)
        .agg(
            rows=("panel_id", "count"),
            avg_media_exposure=("media_exposure_score", "mean"),
            avg_attention=("user_attention_score", "mean"),
            avg_social_interaction=("social_interaction_score", "mean"),
            avg_conversion_proxy=("sponsor_conversion_proxy", "mean"),
            avg_efficiency=("funnel_efficiency", "mean"),
            avg_roi=("predicted_roi", "mean"),
        )
        .round(4)
    )
    grouped["persona"] = grouped.apply(persona_label, axis=1)
    return grouped.sort_values(["avg_conversion_proxy", "avg_efficiency"], ascending=False)


def build_funnel(chain: pd.DataFrame) -> pd.DataFrame:
    stages = [
        ("media_exposure", "媒体曝光", "media_exposure_score"),
        ("user_attention", "用户关注", "user_attention_score"),
        ("social_interaction", "社交互动", "social_interaction_score"),
        ("sponsor_conversion", "赞助转化", "sponsor_conversion_proxy"),
    ]
    rows = []
    previous = None
    for stage_id, label, column in stages:
        score = float(chain[column].mean())
        retention = 1.0 if previous is None else score / max(previous, 0.001)
        rows.append(
            {
                "stage_id": stage_id,
                "stage": label,
                "avg_score": round(score, 4),
                "retention_vs_previous": round(retention, 4),
                "interpretation": funnel_interpretation(stage_id, retention),
            }
        )
        previous = score
    return pd.DataFrame(rows)


def funnel_interpretation(stage_id: str, retention: float) -> str:
    if stage_id == "media_exposure":
        return "Top-of-funnel reach from match attention, reposts, and video views."
    if retention >= 0.85:
        return "Strong handoff; audience signal remains commercially useful."
    if retention >= 0.55:
        return "Moderate handoff; conversion depends on message fit and activation quality."
    return "Leakage point; improve creative, player availability, or channel targeting."


def write_brief(chain: pd.DataFrame, personas: pd.DataFrame, funnel: pd.DataFrame) -> None:
    top_persona = personas.iloc[0]
    top_team = (
        chain.groupby("team", as_index=False)
        .agg(avg_conversion=("sponsor_conversion_proxy", "mean"), avg_roi=("predicted_roi", "mean"))
        .sort_values("avg_conversion", ascending=False)
        .head(6)
        .round(4)
    )
    stage_summary = (
        chain.groupby("stage", as_index=False)
        .agg(
            avg_media_exposure=("media_exposure_score", "mean"),
            avg_attention=("user_attention_score", "mean"),
            avg_social_interaction=("social_interaction_score", "mean"),
            avg_conversion_proxy=("sponsor_conversion_proxy", "mean"),
        )
        .sort_values("avg_conversion_proxy", ascending=False)
        .round(4)
    )
    lines = [
        "# User Research Brief",
        "",
        "## Research Question",
        "",
        "How does World Cup media exposure translate into user attention, social interaction, and sponsor conversion proxy outcomes?",
        "",
        "## Analysis Chain",
        "",
        "媒体曝光 -> 用户关注 -> 社交互动 -> 赞助转化. The final conversion variable is a proxy built from predicted ROI, ROI per spend, brand fit, and activation quality.",
        "",
        "## Attention Funnel",
        "",
        markdown_table(funnel),
        "",
        "## Top User Personas",
        "",
        markdown_table(personas[["team", "persona", "attention_segment", "commercial_segment", "avg_conversion_proxy", "avg_efficiency", "avg_roi"]].head(10)),
        "",
        "## Team Opportunities",
        "",
        markdown_table(top_team),
        "",
        "## Stage Pattern",
        "",
        markdown_table(stage_summary),
        "",
        "## Recommended Product Actions",
        "",
        f"- Lead audience segment: {top_persona['persona']} around {top_persona['team']}.",
        "- Use high media exposure but low conversion rows as creative or landing-page optimization cases.",
        "- Use high efficiency rows as candidates for performance-based sponsor packages.",
        "- Treat conversion as a proxy until licensed sponsor sales, CRM, or ticketing data is connected.",
    ]
    (REPORT_DIR / "user_research_brief.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel_path = DATA_DIR / "panel_dataset.csv"
    if not panel_path.exists():
        from build_panel_data import main as build_panel

        build_panel()
    panel = pd.read_csv(panel_path)
    social = pd.read_csv(DATA_DIR / "social_media.csv")
    chain = build_user_chain(panel, social)
    personas = build_personas(chain)
    funnel = build_funnel(chain)
    chain.to_csv(DATA_DIR / "user_behavior_chain.csv", index=False)
    personas.to_csv(REPORT_DIR / "user_personas.csv", index=False)
    funnel.to_csv(REPORT_DIR / "attention_funnel.csv", index=False)
    write_brief(chain, personas, funnel)
    print({"user_rows": len(chain), "personas": len(personas), "funnel_stages": len(funnel)})


if __name__ == "__main__":
    main()
