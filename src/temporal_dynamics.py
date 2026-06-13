from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "docs" / "assets"


STAGE_ORDER = {"group": 1, "tournament": 2, "round_of_16": 3, "quarter_final": 4, "semi_final": 5, "final": 6}


def stage_index(stage: str) -> int:
    return STAGE_ORDER.get(str(stage).lower(), 2)


def build_temporal(panel: pd.DataFrame) -> pd.DataFrame:
    work = panel.copy()
    work["stage_index"] = work["stage"].map(stage_index)
    summary = (
        work.groupby(["year", "stage", "stage_index"], as_index=False)
        .agg(
            avg_roi=("predicted_roi", "mean"),
            avg_momentum=("commercial_momentum", "mean"),
            avg_attention=("event_attention_m", "mean"),
            avg_fan_score=("fan_score_panel", "mean"),
        )
        .sort_values(["year", "stage_index"])
        .round(4)
    )
    summary["roi_stage_delta"] = summary.groupby("year")["avg_roi"].diff().fillna(0).round(4)
    return summary


def svg_temporal(summary: pd.DataFrame) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    recent = summary[summary["year"].ge(summary["year"].max() - 20)]
    if recent.empty:
        recent = summary
    vals = recent.groupby("stage_index", as_index=False).agg(avg_roi=("avg_roi", "mean")).sort_values("stage_index")
    width, height = 1280, 560
    x0, y0, w, h = 120, 150, 980, 280
    ymin, ymax = vals["avg_roi"].min(), vals["avg_roi"].max()
    span = max(float(ymax - ymin), 1e-9)
    points = []
    for i, row in vals.iterrows():
        x = x0 + i * w / max(len(vals) - 1, 1)
        y = y0 + h - (float(row["avg_roi"]) - ymin) / span * h
        points.append((x, y))
    rows = ['<svg width="1280" height="560" viewBox="0 0 1280 560" xmlns="http://www.w3.org/2000/svg">', '<rect width="1280" height="560" fill="#ffffff"/>']
    rows.append('<text x="64" y="72" font-family="Arial" font-size="34" font-weight="700" fill="#111827">Temporal ROI Dynamics</text>')
    rows.append('<text x="64" y="106" font-family="Arial" font-size="17" fill="#4b5563">Stage-aware ROI movement across tournament phases.</text>')
    rows.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#ffffff" stroke="#d1d5db"/>')
    if len(points) > 1:
        rows.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in points) + '" fill="none" stroke="#0072B2" stroke-width="4"/>')
    for x, y in points:
        rows.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#0072B2"/>')
    rows.append('<text x="120" y="482" font-family="Arial" font-size="15" fill="#4b5563">Upgrade path: time-aware GNN or temporal transformer over match-stage sequences.</text>')
    rows.append("</svg>")
    (ASSET_DIR / "temporal_roi_dynamics.svg").write_text("\n".join(rows), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    temporal = build_temporal(panel)
    temporal.to_csv(REPORT_DIR / "temporal_roi_dynamics.csv", index=False)
    svg_temporal(temporal)
    lines = [
        "# Temporal Dynamics Report",
        "",
        "This module upgrades static ROI analysis into stage-aware dynamic modeling.",
        "",
        markdown_table(temporal.sort_values(["year", "stage_index"]).tail(12)),
        "",
        "## Research Upgrade Path",
        "",
        "- Time-aware GNN: propagate sponsor influence over match-stage graph snapshots.",
        "- Temporal Transformer: learn exposure and attention trajectories by stage.",
        "- Dynamic treatment effects: estimate how media exposure effects change from group stage to final.",
    ]
    (REPORT_DIR / "temporal_dynamics_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved temporal dynamics outputs.")


if __name__ == "__main__":
    main()
