from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "docs" / "assets"


TREATMENTS = [
    ("media_exposure_index", "Media exposure"),
    ("fan_score", "Fan influence"),
    ("team_a_strength", "Team strength"),
    ("commercial_momentum_score", "Commercial momentum"),
]
OUTCOME = "sponsor_roi"
CONTROLS = [
    "team_a_strength",
    "stage_premium_score",
    "weather_impact_score",
    "sponsor_team_fit_score",
    "injury_risk_score",
    "a_sponsor_spend_m",
]


def standardize(series: pd.Series) -> pd.Series:
    std = float(series.std())
    if std == 0 or np.isnan(std):
        return series * 0
    return (series - float(series.mean())) / std


def ols_coef(X: pd.DataFrame, y: pd.Series) -> np.ndarray:
    design = np.column_stack([np.ones(len(X)), X.to_numpy(dtype=float)])
    return np.linalg.pinv(design.T @ design) @ design.T @ y.to_numpy(dtype=float)


def estimate_effect(df: pd.DataFrame, treatment: str) -> dict[str, float | str]:
    cols = [treatment] + [c for c in CONTROLS if c != treatment and c in df.columns]
    work = df[[OUTCOME] + cols].dropna().copy()
    for col in cols + [OUTCOME]:
        work[col] = standardize(work[col])
    coef = ols_coef(work[cols], work[OUTCOME])
    effect = float(coef[1])
    residual = work[OUTCOME].to_numpy() - np.column_stack([np.ones(len(work)), work[cols].to_numpy()]) @ coef
    se = float(np.sqrt(np.mean(residual**2) / max(len(work) - len(cols) - 1, 1)))
    return {
        "treatment": treatment,
        "label": dict(TREATMENTS)[treatment],
        "standardized_effect": round(effect, 4),
        "ci_low": round(effect - 1.96 * se, 4),
        "ci_high": round(effect + 1.96 * se, 4),
        "method": "backdoor-adjusted OLS baseline",
        "sample_size": int(len(work)),
    }


def svg_effects(effects: pd.DataFrame) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    width, height = 1280, 620
    x0, y0, chart_w, chart_h = 420, 120, 710, 360
    min_v = min(float(effects["ci_low"].min()), -0.2)
    max_v = max(float(effects["ci_high"].max()), 0.2)
    span = max(max_v - min_v, 1e-9)

    def sx(v: float) -> float:
        return x0 + (v - min_v) / span * chart_w

    rows = [
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        '<text x="64" y="72" font-family="Arial" font-size="34" font-weight="700" fill="#111827">Causal Treatment Effects on Sponsor ROI</text>',
        '<text x="64" y="108" font-family="Arial" font-size="17" fill="#4b5563">Backdoor-adjusted baseline estimates; positive values indicate higher predicted ROI after controlling for observed confounders.</text>',
        f'<line x1="{sx(0):.1f}" y1="{y0-10}" x2="{sx(0):.1f}" y2="{y0+chart_h+20}" stroke="#6b7280" stroke-width="2" stroke-dasharray="5 7"/>',
    ]
    y = y0 + 42
    for _, row in effects.iterrows():
        low, high, effect = float(row["ci_low"]), float(row["ci_high"]), float(row["standardized_effect"])
        color = "#009E73" if effect >= 0 else "#D55E00"
        rows.append(f'<text x="76" y="{y+6}" font-family="Arial" font-size="18" fill="#111827">{row["label"]}</text>')
        rows.append(f'<line x1="{sx(low):.1f}" y1="{y}" x2="{sx(high):.1f}" y2="{y}" stroke="#9ca3af" stroke-width="8" stroke-linecap="round"/>')
        rows.append(f'<circle cx="{sx(effect):.1f}" cy="{y}" r="11" fill="{color}"/>')
        rows.append(f'<text x="{sx(high)+18:.1f}" y="{y+6}" font-family="Arial" font-size="15" fill="#4b5563">{effect:+.3f}</text>')
        y += 72
    rows.append('<text x="64" y="552" font-family="Arial" font-size="15" fill="#4b5563">Interpretation: correlation is not treated as causation; estimates are adjusted for observed sponsor, team, stage, weather and injury context.</text>')
    (ASSET_DIR / "causal_treatment_effects.svg").write_text("\n".join(rows), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    effects = pd.DataFrame([estimate_effect(df, t) for t, _ in TREATMENTS])
    effects.to_csv(REPORT_DIR / "causal_treatment_effects.csv", index=False)
    svg_effects(effects)

    lines = [
        "# Causal Inference Report",
        "",
        "## Objective",
        "",
        "Estimate whether media exposure, fan influence, team strength and commercial momentum have plausible causal effects on sponsor ROI after adjusting for observed confounders.",
        "",
        "## Correlation vs Causation",
        "",
        "A raw correlation can be inflated by tournament stage, team strength, sponsor spend or player availability. This module therefore reports a backdoor-adjusted baseline estimate. It is designed so DoWhy, EconML or Causal Forest can replace the estimator without changing downstream reports.",
        "",
        "## Treatment Effects",
        "",
        markdown_table(effects),
        "",
        "## Upgrade Path",
        "",
        "- DoWhy: define graph assumptions and run refutation tests.",
        "- EconML / Causal Forest: estimate heterogeneous treatment effects by sponsor category, tournament stage and team profile.",
        "- Sensitivity analysis: test unobserved confounding around player injury and sponsor contract quality.",
    ]
    (REPORT_DIR / "causal_inference_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved causal inference outputs.")


if __name__ == "__main__":
    main()
