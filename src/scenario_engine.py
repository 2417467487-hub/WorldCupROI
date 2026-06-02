from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


SCENARIOS = [
    {"scenario": "baseline", "spend_multiplier": 1.00, "exposure_multiplier": 1.00, "availability_delta": 0.00, "weather_delta": 0.00, "stage_delta": 0.00},
    {"scenario": "premium_media_push", "spend_multiplier": 1.18, "exposure_multiplier": 1.35, "availability_delta": 0.00, "weather_delta": 0.00, "stage_delta": 0.06},
    {"scenario": "core_player_absent", "spend_multiplier": 1.00, "exposure_multiplier": 0.92, "availability_delta": -0.28, "weather_delta": 0.02, "stage_delta": 0.00},
    {"scenario": "bad_weather_low_attention", "spend_multiplier": 1.00, "exposure_multiplier": 0.82, "availability_delta": 0.00, "weather_delta": 0.18, "stage_delta": 0.00},
    {"scenario": "knockout_brand_surge", "spend_multiplier": 1.25, "exposure_multiplier": 1.55, "availability_delta": 0.04, "weather_delta": 0.00, "stage_delta": 0.16},
]


def scenario_roi(row: pd.Series, scenario: dict[str, float | str]) -> float:
    base = float(row.get("predicted_roi", row.get("sponsor_roi", 1.0)))
    exposure_lift = 0.20 * (float(scenario["exposure_multiplier"]) - 1)
    spend_penalty = -0.05 * (float(scenario["spend_multiplier"]) - 1)
    availability_lift = 0.32 * float(scenario["availability_delta"])
    weather_penalty = -0.24 * float(scenario["weather_delta"])
    stage_lift = 0.28 * float(scenario["stage_delta"])
    return round(max(0.2, base + exposure_lift + spend_penalty + availability_lift + weather_penalty + stage_lift), 3)


def strategy_text(lift: float, risk_score: float) -> str:
    if lift > 0.18 and risk_score < 0.45:
        return "Scale sponsor activation and prioritize premium media inventory."
    if lift > 0.05:
        return "Proceed selectively; monitor fan sentiment and player availability."
    if risk_score > 0.65:
        return "Reduce exposure risk; shift budget to flexible or performance-based activation."
    return "Maintain baseline investment and wait for stronger attention signals."


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.head(120).iterrows():
        baseline = float(row.get("predicted_roi", row.get("sponsor_roi", 1.0)))
        risk_score = float(row.get("risk_score", 0.35))
        for scenario in SCENARIOS:
            roi = scenario_roi(row, scenario)
            lift = round(roi - baseline, 3)
            rows.append(
                {
                    "match_id": row["match_id"],
                    "team_a": row["team_a"],
                    "team_b": row["team_b"],
                    "stage": row["stage"],
                    "scenario": scenario["scenario"],
                    "scenario_roi": roi,
                    "roi_lift": lift,
                    "risk_level": "high" if risk_score > 0.65 else "medium" if risk_score > 0.38 else "low",
                    "strategy_recommendation": strategy_text(lift, risk_score),
                }
            )
    out = pd.DataFrame(rows)
    out["scenario_rank"] = out.groupby("match_id")["scenario_roi"].rank(ascending=False, method="dense").astype(int)
    return out


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    base = pd.read_csv(DATA_DIR / "roi_predictions.csv") if (DATA_DIR / "roi_predictions.csv").exists() else pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    if (DATA_DIR / "roi_uncertainty.csv").exists():
        risk = pd.read_csv(DATA_DIR / "roi_uncertainty.csv")[["match_id", "risk_score"]]
        base = base.merge(risk, on="match_id", how="left")
    out = run_scenarios(base)
    out_path = DATA_DIR / "scenario_recommendations.csv"
    out.to_csv(out_path, index=False)
    top = out.sort_values(["scenario_rank", "roi_lift"], ascending=[True, False]).head(8)
    (REPORT_DIR / "scenario_ranking.md").write_text(
        "# Scenario Ranking\n\n" + markdown_table(top),
        encoding="utf-8",
    )
    print(f"Saved scenario recommendations to {out_path}")


if __name__ == "__main__":
    main()
