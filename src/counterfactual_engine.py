from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "docs" / "assets"


COUNTERFACTUALS = [
    {"scenario": "player_injury_shock", "fan_delta": -0.18, "momentum_delta": -0.12, "roi_delta": -0.22},
    {"scenario": "media_surge", "fan_delta": 0.10, "momentum_delta": 0.20, "roi_delta": 0.18},
    {"scenario": "budget_cut", "fan_delta": -0.05, "momentum_delta": -0.08, "roi_delta": -0.12},
    {"scenario": "budget_reallocation", "fan_delta": 0.04, "momentum_delta": 0.10, "roi_delta": 0.09},
    {"scenario": "late_stage_activation", "fan_delta": 0.08, "momentum_delta": 0.16, "roi_delta": 0.15},
]


def run_counterfactuals(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    sample = panel.sort_values("predicted_roi", ascending=False).head(120)
    for _, row in sample.iterrows():
        base = float(row["predicted_roi"])
        for cf in COUNTERFACTUALS:
            adjusted = base + cf["roi_delta"] + 0.12 * cf["fan_delta"] + 0.18 * cf["momentum_delta"]
            interval = 0.08 + abs(cf["roi_delta"]) * 0.35
            rows.append(
                {
                    "panel_id": row["panel_id"],
                    "team": row["team"],
                    "sponsor": row["sponsor"],
                    "scenario": cf["scenario"],
                    "baseline_roi": round(base, 4),
                    "counterfactual_roi": round(max(0.1, adjusted), 4),
                    "roi_delta": round(adjusted - base, 4),
                    "roi_low": round(max(0.1, adjusted - interval), 4),
                    "roi_high": round(adjusted + interval, 4),
                    "method": "SCM-style deterministic intervention baseline",
                }
            )
    return pd.DataFrame(rows)


def svg_counterfactual(summary: pd.DataFrame) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    avg = summary.groupby("scenario", as_index=False).agg(avg_delta=("roi_delta", "mean")).sort_values("avg_delta")
    max_abs = max(float(avg["avg_delta"].abs().max()), 1e-9)
    rows = ['<svg width="1280" height="600" viewBox="0 0 1280 600" xmlns="http://www.w3.org/2000/svg">', '<rect width="1280" height="600" fill="#ffffff"/>']
    rows.append('<text x="64" y="72" font-family="Arial" font-size="34" font-weight="700" fill="#111827">Counterfactual ROI Interventions</text>')
    rows.append('<text x="64" y="106" font-family="Arial" font-size="17" fill="#4b5563">Scenario-level ROI changes under SCM-style interventions.</text>')
    x0, y = 640, 170
    rows.append('<line x1="640" y1="145" x2="640" y2="470" stroke="#6b7280" stroke-width="2" stroke-dasharray="5 7"/>')
    for _, row in avg.iterrows():
        val = float(row["avg_delta"])
        width = 430 * abs(val) / max_abs
        color = "#009E73" if val >= 0 else "#D55E00"
        x = x0 if val >= 0 else x0 - width
        rows.append(f'<text x="110" y="{y+22}" font-family="Arial" font-size="17" fill="#111827">{row["scenario"]}</text>')
        rows.append(f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="30" rx="15" fill="{color}"/>')
        rows.append(f'<text x="1080" y="{y+22}" font-family="Arial" font-size="15" fill="#4b5563">{val:+.3f}</text>')
        y += 56
    rows.append("</svg>")
    (ASSET_DIR / "counterfactual_roi_interventions.svg").write_text("\n".join(rows), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    cf = run_counterfactuals(panel)
    cf.to_csv(REPORT_DIR / "counterfactual_interventions.csv", index=False)
    svg_counterfactual(cf)
    summary = cf.groupby("scenario", as_index=False).agg(avg_delta=("roi_delta", "mean"), low=("roi_low", "mean"), high=("roi_high", "mean")).round(4)
    lines = [
        "# Counterfactual Engine Report",
        "",
        "This module simulates player injury, media change and budget interventions and reports ROI change intervals.",
        "",
        markdown_table(summary),
        "",
        "## Upgrade Path",
        "",
        "- Synthetic Control: build sponsor/team counterfactual baselines from comparable historical matches.",
        "- SCM: formalize injury, exposure and budget interventions as structural equations.",
        "- Causal sensitivity: evaluate how robust ROI lift is to unobserved media quality.",
    ]
    (REPORT_DIR / "counterfactual_engine_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved counterfactual engine outputs.")


if __name__ == "__main__":
    main()
