from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
RANDOM_SEED = 42


def estimate_roi_uncertainty(df: pd.DataFrame, n_samples: int = 500) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    base = df["predicted_roi"].to_numpy() if "predicted_roi" in df.columns else df["sponsor_roi"].to_numpy()
    risk_scale = (
        0.08
        + 0.10 * df.get("injury_risk_score", pd.Series(0.2, index=df.index)).to_numpy()
        + 0.06 * df.get("weather_impact_score", pd.Series(0.3, index=df.index)).to_numpy()
    )
    draws = rng.normal(base[:, None], risk_scale[:, None], size=(len(df), n_samples))
    result = df[["match_id", "team_a", "team_b", "stage"]].copy()
    result["roi_mean"] = draws.mean(axis=1).round(3)
    result["roi_ci_low"] = np.quantile(draws, 0.05, axis=1).round(3)
    result["roi_ci_high"] = np.quantile(draws, 0.95, axis=1).round(3)
    result["negative_roi_probability"] = (draws < 1.0).mean(axis=1).round(3)
    result["ensemble_variance"] = draws.var(axis=1).round(4)
    result["risk_score"] = (
        0.55 * result["negative_roi_probability"]
        + 0.45 * (result["ensemble_variance"] / max(result["ensemble_variance"].max(), 1e-6))
    ).round(3)
    result["conformal_interval_width"] = (result["roi_ci_high"] - result["roi_ci_low"]).round(3)
    return result


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "roi_predictions.csv"
    df = pd.read_csv(path if path.exists() else DATA_DIR / "modeling_dataset.csv")
    uncertainty = estimate_roi_uncertainty(df)
    out_path = DATA_DIR / "roi_uncertainty.csv"
    uncertainty.to_csv(out_path, index=False)
    summary = {
        "avg_negative_roi_probability": round(float(uncertainty["negative_roi_probability"].mean()), 3),
        "avg_interval_width": round(float(uncertainty["conformal_interval_width"].mean()), 3),
        "high_risk_cases": int((uncertainty["risk_score"] > 0.6).sum()),
    }
    (REPORT_DIR / "uncertainty_summary.md").write_text(
        "# ROI Uncertainty Summary\n\n"
        f"- Average negative ROI probability: {summary['avg_negative_roi_probability']}\n"
        f"- Average prediction interval width: {summary['avg_interval_width']}\n"
        f"- High-risk cases: {summary['high_risk_cases']}\n",
        encoding="utf-8",
    )
    print(f"Saved ROI uncertainty outputs to {out_path}")


if __name__ == "__main__":
    main()
