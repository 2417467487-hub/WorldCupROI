from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import KFold


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


TREATMENTS = {
    "media_exposure": "exposure_score",
    "event_attention": "event_attention_m",
    "player_performance": "core_player_rating",
    "player_reach": "player_followers_m",
}

CONTROLS = [
    "team_elo",
    "sponsor_power_index",
    "brand_fit",
    "activation_quality",
    "sponsor_spend_m",
    "temperature_c",
    "humidity",
]


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    view = df.head(max_rows)
    lines = ["| " + " | ".join(view.columns) + " |", "| " + " | ".join(["---"] * len(view.columns)) + " |"]
    for _, row in view.iterrows():
        values = [f"{row[c]:.4f}" if isinstance(row[c], float) else str(row[c]) for c in view.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def residualize(y: pd.Series, x: pd.DataFrame) -> np.ndarray:
    model = Ridge(alpha=1.0)
    model.fit(x, y)
    return np.asarray(y) - model.predict(x)


def estimate_effect(df: pd.DataFrame, treatment_name: str, treatment_col: str) -> dict:
    work = df[[treatment_col, "predicted_roi", *CONTROLS]].dropna().copy()
    x = work[CONTROLS]
    t = work[treatment_col]
    y = work["predicted_roi"]

    corr = float(np.corrcoef(t, y)[0, 1])
    t_res = residualize(t, x)
    y_res = residualize(y, x)
    model = LinearRegression()
    model.fit(t_res.reshape(-1, 1), y_res)
    effect = float(model.coef_[0])

    fold_effects = []
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    for train_idx, test_idx in kf.split(work):
        train = work.iloc[train_idx]
        test = work.iloc[test_idx]
        t_test_res = np.asarray(test[treatment_col]) - Ridge(alpha=1.0).fit(train[CONTROLS], train[treatment_col]).predict(test[CONTROLS])
        y_test_res = np.asarray(test["predicted_roi"]) - Ridge(alpha=1.0).fit(train[CONTROLS], train["predicted_roi"]).predict(test[CONTROLS])
        fold = LinearRegression().fit(t_test_res.reshape(-1, 1), y_test_res)
        fold_effects.append(float(fold.coef_[0]))

    ci_low = float(np.percentile(fold_effects, 5))
    ci_high = float(np.percentile(fold_effects, 95))
    sign = "positive" if effect > 0 else "negative"
    return {
        "treatment": treatment_name,
        "column": treatment_col,
        "correlation_with_roi": round(corr, 4),
        "causal_effect_residualized": round(effect, 4),
        "effect_ci_low": round(ci_low, 4),
        "effect_ci_high": round(ci_high, 4),
        "effect_direction": sign,
        "method": "DoWhy/EconML-compatible residualized double-ML baseline",
        "controls": ", ".join(CONTROLS),
        "samples": int(len(work)),
    }


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    rows = [estimate_effect(panel, name, col) for name, col in TREATMENTS.items()]
    effects = pd.DataFrame(rows)
    effects.to_csv(REPORT_DIR / "causal_effect_estimates.csv", index=False)

    lines = [
        "# Causal Inference Report",
        "",
        "## Goal",
        "",
        "Separate correlation from causal evidence for media exposure, event attention, and player performance effects on sponsor ROI.",
        "",
        "## Method",
        "",
        "This module uses a DoWhy/EconML-compatible residualized double-ML baseline: treatment and ROI are residualized against confounders, then the treatment effect is estimated on residuals with fold-based uncertainty.",
        "",
        "Production upgrade path: replace the baseline estimator with DoWhy identification/refutation and EconML DML/DRLearner once audited treatment, outcome, and instrument definitions are available.",
        "",
        "## Correlation vs Causal Effect",
        "",
        markdown_table(effects),
        "",
        "## Interpretation Guardrails",
        "",
        "- Positive correlation is not automatically causal lift.",
        "- Sponsor spend, brand fit, activation quality, and team strength are treated as confounders.",
        "- Proxy/mock commercial outcomes limit causal claims; report effects as decision evidence, not proof.",
    ]
    (REPORT_DIR / "causal_inference_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"causal_effects": len(effects)})


if __name__ == "__main__":
    main()
