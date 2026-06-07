from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from ml_config import MATCH_FEATURES, RANDOM_SEED, ROI_FEATURES
from train_match_model import CentroidOutcomeModel
from train_roi_model import RidgeROIModel


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
ALPHA = 0.10


def three_way_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    idx = rng.permutation(len(df))
    n_train = int(len(df) * 0.60)
    n_cal = int(len(df) * 0.20)
    return df.iloc[idx[:n_train]].copy(), df.iloc[idx[n_train : n_train + n_cal]].copy(), df.iloc[idx[n_train + n_cal :]].copy()


def quantile(scores: np.ndarray, alpha: float = ALPHA) -> float:
    n = len(scores)
    q = np.ceil((n + 1) * (1 - alpha)) / max(n, 1)
    return float(np.quantile(scores, min(q, 1.0), method="higher"))


def match_conformal(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    train, cal, test = three_way_split(df)
    model = CentroidOutcomeModel().fit(train[MATCH_FEATURES], train["result"])
    cal_proba = model.predict_proba(cal[MATCH_FEATURES])
    class_index = {label: idx for idx, label in enumerate(model.classes)}
    cal_scores = 1 - np.array([cal_proba[i, class_index[label]] for i, label in enumerate(cal["result"])])
    qhat = quantile(cal_scores)
    test_proba = model.predict_proba(test[MATCH_FEATURES])
    sets = []
    covered = []
    for i, label in enumerate(test["result"]):
        prediction_set = [cls for cls, idx in class_index.items() if 1 - test_proba[i, idx] <= qhat]
        sets.append(",".join(prediction_set))
        covered.append(label in prediction_set)
    out = test[["match_id", "team_a", "team_b", "stage", "result"]].copy()
    out["prediction_set"] = sets
    out["set_size"] = [len(s.split(",")) if s else 0 for s in sets]
    out["covered"] = covered
    metrics = {
        "coverage_rate": round(float(np.mean(covered)), 4),
        "avg_set_size": round(float(out["set_size"].mean()), 4),
        "qhat": round(qhat, 4),
    }
    return out, metrics


def roi_conformal(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    train, cal, test = three_way_split(df)
    model = RidgeROIModel(alpha=1.5).fit(train[ROI_FEATURES], train["sponsor_roi"])
    cal_pred = model.predict(cal[ROI_FEATURES])
    residual_scores = np.abs(cal["sponsor_roi"].to_numpy() - cal_pred)
    qhat = quantile(residual_scores)
    pred = model.predict(test[ROI_FEATURES])
    out = test[["match_id", "team_a", "team_b", "stage", "sponsor_roi"]].copy()
    out["roi_pred"] = pred.round(3)
    out["roi_interval_low"] = (pred - qhat).round(3)
    out["roi_interval_high"] = (pred + qhat).round(3)
    out["covered"] = out["sponsor_roi"].between(out["roi_interval_low"], out["roi_interval_high"])
    metrics = {
        "coverage_rate": round(float(out["covered"].mean()), 4),
        "avg_interval_width": round(float((out["roi_interval_high"] - out["roi_interval_low"]).mean()), 4),
        "qhat": round(float(qhat), 4),
    }
    return out, metrics


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    match_sets, match_metrics = match_conformal(df)
    roi_intervals, roi_metrics = roi_conformal(df)
    match_sets.to_csv(REPORT_DIR / "match_conformal_sets.csv", index=False)
    roi_intervals.to_csv(REPORT_DIR / "roi_conformal_intervals.csv", index=False)
    lines = [
        "# Conformal Prediction Report",
        "",
        "## Match Prediction Sets",
        "",
        f"- Coverage rate: {match_metrics['coverage_rate']}",
        f"- Average prediction set size: {match_metrics['avg_set_size']}",
        f"- qhat: {match_metrics['qhat']}",
        "",
        "## ROI Prediction Intervals",
        "",
        f"- Coverage rate: {roi_metrics['coverage_rate']}",
        f"- Average interval width: {roi_metrics['avg_interval_width']}",
        f"- qhat: {roi_metrics['qhat']}",
    ]
    (REPORT_DIR / "conformal_prediction_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"match_coverage": match_metrics["coverage_rate"], "roi_coverage": roi_metrics["coverage_rate"]})


if __name__ == "__main__":
    main()
