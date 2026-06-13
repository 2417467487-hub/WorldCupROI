from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "docs" / "assets"


FUNNEL_STAGES = ["Exposure", "Attention", "Engagement", "Conversion", "ROI"]


def build_funnel(panel: pd.DataFrame) -> pd.DataFrame:
    work = panel.copy()
    work["exposure"] = work["event_attention_m"].clip(lower=1) * work["exposure_score"].clip(lower=0.05)
    work["attention"] = work["exposure"] * (0.35 + 0.45 * work["fan_score_panel"].clip(0, 1))
    work["engagement"] = work["attention"] * (0.18 + 0.28 * work["commercial_momentum"].clip(0, 1))
    work["conversion"] = work["engagement"] * (0.08 + 0.22 * work["brand_fit"].clip(0, 1))
    work["roi_value"] = work["conversion"] * work["predicted_roi"].clip(lower=0.1)
    summary = (
        work.groupby(["sponsor", "stage"], as_index=False)
        .agg(
            exposure=("exposure", "mean"),
            attention=("attention", "mean"),
            engagement=("engagement", "mean"),
            conversion=("conversion", "mean"),
            roi_value=("roi_value", "mean"),
            predicted_roi=("predicted_roi", "mean"),
        )
        .round(4)
    )
    summary["attention_rate"] = (summary["attention"] / summary["exposure"]).round(4)
    summary["engagement_rate"] = (summary["engagement"] / summary["attention"]).round(4)
    summary["conversion_rate"] = (summary["conversion"] / summary["engagement"]).round(4)
    summary["roi_efficiency"] = (summary["roi_value"] / summary["conversion"]).round(4)
    return summary


def svg_funnel(summary: pd.DataFrame) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    avg = summary[["exposure", "attention", "engagement", "conversion", "roi_value"]].mean()
    vals = [float(avg[c]) for c in avg.index]
    max_v = max(vals) or 1
    colors = ["#0072B2", "#56B4E9", "#009E73", "#E69F00", "#D55E00"]
    rows = ['<svg width="1280" height="600" viewBox="0 0 1280 600" xmlns="http://www.w3.org/2000/svg">', '<rect width="1280" height="600" fill="#ffffff"/>']
    rows.append('<text x="64" y="72" font-family="Arial" font-size="34" font-weight="700" fill="#111827">User Behavior Funnel</text>')
    rows.append('<text x="64" y="106" font-family="Arial" font-size="17" fill="#4b5563">Exposure -> Attention -> Engagement -> Conversion -> ROI.</text>')
    y = 150
    for stage, val, color in zip(FUNNEL_STAGES, vals, colors):
        width = 760 * val / max_v
        x = 640 - width / 2
        rows.append(f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="58" rx="10" fill="{color}" opacity="0.9"/>')
        rows.append(f'<text x="640" y="{y+36}" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#ffffff">{stage}</text>')
        rows.append(f'<text x="{x+width+18:.1f}" y="{y+36}" font-family="Arial" font-size="15" fill="#4b5563">{val:.2f}</text>')
        y += 74
    rows.append("</svg>")
    (ASSET_DIR / "user_behavior_funnel.svg").write_text("\n".join(rows), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    funnel = build_funnel(panel)
    funnel.to_csv(REPORT_DIR / "user_behavior_funnel.csv", index=False)
    svg_funnel(funnel)
    top = funnel.sort_values("roi_value", ascending=False).head(10)
    lines = [
        "# User Behavior Funnel Report",
        "",
        "This module models the path Exposure -> Attention -> Engagement -> Conversion -> ROI.",
        "",
        "## Top Sponsor-Stage Paths",
        "",
        markdown_table(top[["sponsor", "stage", "attention_rate", "engagement_rate", "conversion_rate", "predicted_roi"]]),
        "",
        "## Interpretation",
        "",
        "ROI is treated as the final business outcome of an attention funnel rather than a standalone prediction target. Sponsors with lower exposure can still perform well if fan attention and conversion efficiency are strong.",
    ]
    (REPORT_DIR / "user_behavior_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved user behavior funnel outputs.")


if __name__ == "__main__":
    main()
