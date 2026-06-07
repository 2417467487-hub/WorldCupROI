from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from ml_config import ROI_FEATURES


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
MODEL_DIR = ROOT / "models"


def shap_like_roi_contributions(df: pd.DataFrame) -> pd.DataFrame:
    artifact_path = MODEL_DIR / "sponsor_roi_model.pkl"
    if not artifact_path.exists():
        from train_roi_model import main as train_roi

        train_roi()
    artifact = pickle.loads(artifact_path.read_bytes())
    features = artifact["features"]
    coef = np.array(artifact["coef"][1:])
    mean = pd.Series(artifact["mean"])
    std = pd.Series(artifact["std"]).replace(0, 1)
    Xz = (df[features] - mean[features]) / std[features]
    contrib = Xz.multiply(coef, axis=1)
    rows = []
    for feature in features:
        rows.append(
            {
                "feature": feature,
                "mean_abs_contribution": round(float(contrib[feature].abs().mean()), 5),
                "direction": "positive" if float(coef[features.index(feature)]) >= 0 else "negative",
            }
        )
    return pd.DataFrame(rows).sort_values("mean_abs_contribution", ascending=False)


def shap_status() -> str:
    try:
        import shap  # noqa: F401

        return "SHAP package available; tree/linear SHAP can be enabled for production models."
    except Exception:
        return "SHAP package not installed in the runtime; generated dependency-free SHAP-style linear contributions."


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_DIR / "roi_predictions.csv") if (DATA_DIR / "roi_predictions.csv").exists() else pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    contributions = shap_like_roi_contributions(df)
    contributions.to_csv(REPORT_DIR / "roi_shap_like_contributions.csv", index=False)

    feature_importance = pd.read_csv(REPORT_DIR / "roi_feature_importance.csv")
    drivers = feature_importance.head(12).merge(contributions.head(20), on="feature", how="left")
    drivers.to_csv(REPORT_DIR / "roi_driver_explanations.csv", index=False)
    md = [
        "# ROI Explainability Report",
        "",
        shap_status(),
        "",
        "## ROI Driver Summary",
        "",
        markdown_table(drivers.head(10)),
        "",
        "## Business Interpretation",
        "",
        "- Sponsor ROI is explained through sponsor activation, brand heat, media exposure, team strength, FanScore, and stage premium.",
        "- `mean_abs_contribution` approximates per-feature SHAP-style impact for the dependency-free ridge model.",
        "- When XGBoost/LightGBM/CatBoost and SHAP are installed, this module can be extended to exact model-specific SHAP outputs.",
    ]
    (REPORT_DIR / "explainability_report.md").write_text("\n".join(md), encoding="utf-8")
    print({"explainability_rows": len(contributions), "top_driver": contributions.iloc[0]["feature"]})


if __name__ == "__main__":
    main()
