from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


STAGES = ["Exposure", "Attention", "Engagement", "Conversion", "ROI"]


def markdown_table(df: pd.DataFrame, max_rows: int = 15) -> str:
    view = df.head(max_rows)
    lines = ["| " + " | ".join(view.columns) + " |", "| " + " | ".join(["---"] * len(view.columns)) + " |"]
    for _, row in view.iterrows():
        values = [f"{row[c]:.4f}" if isinstance(row[c], float) else str(row[c]) for c in view.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def normalize(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce").fillna(0.0)
    lo, hi = float(x.min()), float(x.max())
    if hi <= lo:
        return pd.Series(np.zeros(len(x)), index=x.index)
    return (x - lo) / (hi - lo)


def build_paths(panel: pd.DataFrame) -> pd.DataFrame:
    work = panel.copy()
    work["Exposure"] = normalize(work["event_attention_m"] + 6 * work["exposure_score"])
    work["Attention"] = normalize(work["fan_score_panel"] + 0.004 * work["media_reposts_k"])
    work["Engagement"] = normalize(work["commercial_momentum"] + 0.15 * work["activation_quality"])
    work["Conversion"] = normalize(0.55 * work["brand_fit"] + 0.45 * work["sponsor_power_index"])
    work["ROI"] = normalize(work["predicted_roi"])
    path = (
        work.groupby(["team", "sponsor"], as_index=False)[STAGES]
        .mean()
        .sort_values("ROI", ascending=False)
        .round(4)
    )
    for left, right in zip(STAGES, STAGES[1:]):
        path[f"{left.lower()}_to_{right.lower()}"] = (path[right] / path[left].replace(0, np.nan)).fillna(0).clip(0, 3).round(4)
    path["behavior_decay_rate"] = (1 - (path["ROI"] / path["Exposure"].replace(0, np.nan))).fillna(1).clip(-1, 1).round(4)
    path["recommended_action"] = np.where(
        path["attention_to_engagement"] < 0.85,
        "improve_creative_and_social_activation",
        np.where(path["conversion_to_roi"] < 0.9, "tighten_sponsor_offer_and_landing_path", "scale_high_quality_funnel"),
    )
    return path


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    paths = build_paths(panel)
    paths.to_csv(REPORT_DIR / "funnel_behavior_paths.csv", index=False)

    lines = [
        "# Funnel Behavior Modeling Report",
        "",
        "## Funnel",
        "",
        "Exposure -> Attention -> Engagement -> Conversion -> ROI",
        "",
        "## Top Conversion Paths",
        "",
        markdown_table(paths.head(12)),
        "",
        "## Fan Behavior Decay Model",
        "",
        "The decay rate measures how much normalized exposure is lost before becoming ROI. High decay means the audience is visible but not converting efficiently.",
        "",
        "## Recommended Uses",
        "",
        "- Use low attention-to-engagement ratios to diagnose creative fatigue.",
        "- Use low conversion-to-ROI ratios to diagnose sponsor offer or activation fit.",
        "- Use decay rate as a budget throttle before scaling paid media.",
    ]
    (REPORT_DIR / "funnel_behavior_modeling_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"funnel_paths": len(paths)})


if __name__ == "__main__":
    main()
