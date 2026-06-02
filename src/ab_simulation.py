from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd

from train_roi_model import ROI_FEATURES


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
MODEL_DIR = ROOT / "models"


def ensure_roi_model() -> None:
    if not (MODEL_DIR / "sponsor_roi_model.pkl").exists():
        from train_roi_model import main as train_roi

        train_roi()


def simulate_core_player_absence(row: pd.Series) -> pd.Series:
    altered = row.copy()
    altered["a_core_player_rating"] *= 0.86
    altered["a_core_market_value_m"] *= 0.55
    altered["a_player_followers_m"] *= 0.72
    altered["fan_score"] *= 0.78
    return altered


def simulate_sponsor_upgrade(row: pd.Series) -> pd.Series:
    altered = row.copy()
    altered["a_sponsor_spend_m"] *= 1.25
    altered["a_brand_fit"] = min(1.0, altered["a_brand_fit"] + 0.12)
    altered["a_activation_quality"] = min(1.0, altered["a_activation_quality"] + 0.16)
    altered["a_sponsor_power_index"] = min(1.0, altered["a_sponsor_power_index"] + 0.14)
    return altered


def simulate_media_cooling(row: pd.Series) -> pd.Series:
    altered = row.copy()
    altered["event_attention_m"] *= 0.68
    altered["media_reposts_k"] *= 0.55
    altered["fan_score"] *= 0.70
    return altered


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for index, row in df.reset_index().iterrows():
        values = []
        for col in headers:
            value = row[col]
            values.append(f"{value:.3f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def predict_roi(model_artifact: dict, X: pd.DataFrame) -> pd.Series:
    features = model_artifact["features"]
    mean = pd.Series(model_artifact["mean"])
    std = pd.Series(model_artifact["std"]).replace(0, 1)
    coef = pd.Series(model_artifact["coef"])
    Xz = (X[features] - mean[features]) / std[features]
    design = pd.concat([pd.Series(1.0, index=X.index, name="intercept"), Xz], axis=1)
    return design.to_numpy() @ coef.to_numpy()


def main() -> None:
    ensure_roi_model()
    REPORT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    with open(MODEL_DIR / "sponsor_roi_model.pkl", "rb") as f:
        model_artifact = pickle.load(f)

    sample = df.sort_values(["event_attention_m", "a_player_followers_m"], ascending=False).head(40).copy()
    rows = []
    scenarios = {
        "A_baseline": lambda x: x,
        "B_core_player_absent": simulate_core_player_absence,
        "C_sponsor_upgrade": simulate_sponsor_upgrade,
        "D_media_cooling": simulate_media_cooling,
    }

    for _, row in sample.iterrows():
        base_roi = None
        for scenario, transform in scenarios.items():
            altered = transform(row)
            pred_roi = float(predict_roi(model_artifact, pd.DataFrame([altered[ROI_FEATURES]]))[0])
            if base_roi is None:
                base_roi = pred_roi
            rows.append(
                {
                    "match_id": int(row["match_id"]),
                    "team_a": row["team_a"],
                    "team_b": row["team_b"],
                    "sponsor": row["a_sponsor"],
                    "scenario": scenario,
                    "predicted_roi": round(pred_roi, 3),
                    "roi_delta_vs_baseline": round(pred_roi - base_roi, 3),
                    "roi_lift_pct": round((pred_roi - base_roi) / base_roi * 100, 2),
                }
            )

    out = pd.DataFrame(rows)
    out.to_csv(REPORT_DIR / "ab_simulation_results.csv", index=False)

    summary = out.groupby("scenario").agg(
        avg_predicted_roi=("predicted_roi", "mean"),
        avg_roi_delta=("roi_delta_vs_baseline", "mean"),
        avg_roi_lift_pct=("roi_lift_pct", "mean"),
    )
    summary.to_csv(REPORT_DIR / "ab_simulation_summary.csv")

    with open(REPORT_DIR / "ab_simulation_summary.md", "w", encoding="utf-8") as f:
        f.write("# Counterfactual A/B Simulation\n\n")
        f.write("This experiment compares baseline sponsor ROI with three counterfactual conditions.\n\n")
        f.write(markdown_table(summary.reset_index().round(3)))
        f.write("\n\n## Research Interpretation\n\n")
        f.write(
            "A player absence scenario tests star dependency; sponsor upgrade tests whether additional activation can "
            "compensate for sporting uncertainty; media cooling tests how fragile ROI is when attention drops. This is "
            "the key user-research layer of the project because it turns behavior signals into actionable brand strategy.\n"
        )

    print(summary.round(3))
    print(f"Saved A/B outputs to {REPORT_DIR}")


if __name__ == "__main__":
    main()
