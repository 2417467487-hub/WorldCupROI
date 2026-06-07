from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
RANDOM_SEED = 42


def risk_scale(df: pd.DataFrame) -> np.ndarray:
    return (
        0.08
        + 0.10 * df.get("injury_risk_score", pd.Series(0.2, index=df.index)).to_numpy()
        + 0.06 * df.get("weather_impact_score", pd.Series(0.3, index=df.index)).to_numpy()
        + 0.05 * df.get("stage_premium_score", pd.Series(0.2, index=df.index)).to_numpy()
    )


def monte_carlo_draws(df: pd.DataFrame, n_samples: int = 800) -> np.ndarray:
    rng = np.random.default_rng(RANDOM_SEED)
    base = df["predicted_roi"].to_numpy() if "predicted_roi" in df.columns else df["sponsor_roi"].to_numpy()
    return rng.normal(base[:, None], risk_scale(df)[:, None], size=(len(df), n_samples))


def bootstrap_intervals(df: pd.DataFrame, n_samples: int = 600) -> np.ndarray:
    rng = np.random.default_rng(RANDOM_SEED + 7)
    base = df["predicted_roi"].to_numpy() if "predicted_roi" in df.columns else df["sponsor_roi"].to_numpy()
    if "sponsor_roi" in df.columns and "predicted_roi" in df.columns:
        residuals = df["sponsor_roi"].to_numpy() - df["predicted_roi"].to_numpy()
    else:
        residuals = rng.normal(0, risk_scale(df).mean(), size=len(df))
    sampled_residuals = rng.choice(residuals, size=(len(df), n_samples), replace=True)
    return base[:, None] + sampled_residuals


def risk_level(score: float) -> str:
    if score >= 0.66:
        return "high"
    if score >= 0.38:
        return "medium"
    return "low"


def estimate_roi_uncertainty(df: pd.DataFrame) -> pd.DataFrame:
    mc = monte_carlo_draws(df)
    bs = bootstrap_intervals(df)
    result = df[["match_id", "team_a", "team_b", "stage"]].copy()
    result["roi_mean"] = mc.mean(axis=1).round(3)
    result["roi_ci_low"] = np.quantile(mc, 0.05, axis=1).round(3)
    result["roi_ci_high"] = np.quantile(mc, 0.95, axis=1).round(3)
    result["bootstrap_ci_low"] = np.quantile(bs, 0.05, axis=1).round(3)
    result["bootstrap_ci_high"] = np.quantile(bs, 0.95, axis=1).round(3)
    result["monte_carlo_std"] = mc.std(axis=1).round(4)
    result["negative_roi_probability"] = (mc < 1.0).mean(axis=1).round(3)
    result["ensemble_variance"] = mc.var(axis=1).round(4)
    result["risk_score"] = (
        0.52 * result["negative_roi_probability"]
        + 0.28 * (result["ensemble_variance"] / max(result["ensemble_variance"].max(), 1e-6))
        + 0.20 * (result["monte_carlo_std"] / max(result["monte_carlo_std"].max(), 1e-6))
    ).round(3)
    result["risk_level"] = result["risk_score"].map(risk_level)
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
        "avg_monte_carlo_std": round(float(uncertainty["monte_carlo_std"].mean()), 3),
        "high_risk_cases": int(uncertainty["risk_level"].eq("high").sum()),
        "medium_risk_cases": int(uncertainty["risk_level"].eq("medium").sum()),
    }
    (REPORT_DIR / "uncertainty_summary.md").write_text(
        "# ROI Uncertainty Summary\n\n"
        f"- Average negative ROI probability: {summary['avg_negative_roi_probability']}\n"
        f"- Average prediction interval width: {summary['avg_interval_width']}\n"
        f"- Average Monte Carlo std: {summary['avg_monte_carlo_std']}\n"
        f"- Medium-risk cases: {summary['medium_risk_cases']}\n"
        f"- High-risk cases: {summary['high_risk_cases']}\n"
        "- Methods: Bootstrap residual intervals + Monte Carlo perturbation + variance-based risk score\n",
        encoding="utf-8",
    )
    print(f"Saved ROI uncertainty outputs to {out_path}")


if __name__ == "__main__":
    main()
