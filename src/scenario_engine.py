from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


SCENARIOS = [
    {
        "scenario": "conservative_efficiency",
        "strategy_type": "conservative",
        "spend_multiplier": 0.88,
        "exposure_multiplier": 0.96,
        "availability_delta": 0.00,
        "weather_delta": 0.00,
        "stage_delta": 0.00,
        "risk_delta": -0.10,
        "reason": "Protect downside, prioritize performance-based inventory, and keep spend flexible.",
    },
    {
        "scenario": "balanced_activation",
        "strategy_type": "balanced",
        "spend_multiplier": 1.05,
        "exposure_multiplier": 1.15,
        "availability_delta": 0.02,
        "weather_delta": 0.00,
        "stage_delta": 0.03,
        "risk_delta": 0.00,
        "reason": "Use a mixed media package and lean into proven fan attention signals.",
    },
    {
        "scenario": "aggressive_media_surge",
        "strategy_type": "aggressive",
        "spend_multiplier": 1.32,
        "exposure_multiplier": 1.62,
        "availability_delta": 0.05,
        "weather_delta": -0.02,
        "stage_delta": 0.12,
        "risk_delta": 0.14,
        "reason": "Buy premium moments when attention, stage value, and player availability support scale.",
    },
    {
        "scenario": "player_risk_defense",
        "strategy_type": "conservative",
        "spend_multiplier": 0.82,
        "exposure_multiplier": 0.88,
        "availability_delta": -0.18,
        "weather_delta": 0.03,
        "stage_delta": 0.00,
        "risk_delta": 0.08,
        "reason": "Shift budget away from star-dependent creative if player availability weakens.",
    },
    {
        "scenario": "knockout_takeover",
        "strategy_type": "aggressive",
        "spend_multiplier": 1.45,
        "exposure_multiplier": 1.90,
        "availability_delta": 0.04,
        "weather_delta": 0.00,
        "stage_delta": 0.20,
        "risk_delta": 0.18,
        "reason": "Capture knockout-stage attention when the upside justifies higher variance.",
    },
]


def scenario_roi(row: pd.Series, scenario: dict[str, float | str]) -> float:
    base = float(row.get("predicted_roi", row.get("sponsor_roi", 1.0)))
    exposure_lift = 0.20 * (float(scenario["exposure_multiplier"]) - 1)
    spend_penalty = -0.05 * (float(scenario["spend_multiplier"]) - 1)
    availability_lift = 0.32 * float(scenario["availability_delta"])
    weather_penalty = -0.24 * float(scenario["weather_delta"])
    stage_lift = 0.28 * float(scenario["stage_delta"])
    return round(max(0.2, base + exposure_lift + spend_penalty + availability_lift + weather_penalty + stage_lift), 3)


def confidence_interval(roi: float, risk_score: float, scenario: dict[str, float | str]) -> tuple[float, float]:
    width = 0.12 + 0.34 * risk_score + 0.07 * max(0, float(scenario["spend_multiplier"]) - 1)
    return round(max(0.2, roi - width), 3), round(roi + width, 3)


def strategy_text(lift: float, risk_score: float, scenario: dict[str, float | str]) -> str:
    if lift > 0.18 and risk_score < 0.50:
        return f"Recommended: {scenario['reason']}"
    if lift > 0.05:
        return f"Conditional: {scenario['reason']} Monitor fan sentiment and player availability."
    if risk_score > 0.65:
        return "Defensive posture: reduce exposure risk and shift spend to flexible activation."
    return "Hold baseline until stronger attention or conversion signals appear."


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.head(120).iterrows():
        baseline = float(row.get("predicted_roi", row.get("sponsor_roi", 1.0)))
        risk_score = float(row.get("risk_score", 0.35))
        for scenario in SCENARIOS:
            roi = scenario_roi(row, scenario)
            lift = round(roi - baseline, 3)
            adjusted_risk = round(min(1, max(0, risk_score + float(scenario["risk_delta"]))), 3)
            ci_low, ci_high = confidence_interval(roi, adjusted_risk, scenario)
            rows.append(
                {
                    "match_id": row["match_id"],
                    "team_a": row["team_a"],
                    "team_b": row["team_b"],
                    "stage": row["stage"],
                    "scenario": scenario["scenario"],
                    "strategy_type": scenario["strategy_type"],
                    "scenario_roi": roi,
                    "roi_lift": lift,
                    "risk_score": adjusted_risk,
                    "risk_level": "high" if adjusted_risk > 0.65 else "medium" if adjusted_risk > 0.38 else "low",
                    "roi_ci_low": ci_low,
                    "roi_ci_high": ci_high,
                    "recommendation_reason": scenario["reason"],
                    "strategy_recommendation": strategy_text(lift, adjusted_risk, scenario),
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
    top = out.sort_values(["scenario_rank", "roi_lift"], ascending=[True, False]).head(10)
    strategy_summary = (
        out.groupby("strategy_type", as_index=False)
        .agg(
            avg_roi=("scenario_roi", "mean"),
            avg_lift=("roi_lift", "mean"),
            avg_risk=("risk_score", "mean"),
            avg_ci_low=("roi_ci_low", "mean"),
            avg_ci_high=("roi_ci_high", "mean"),
            high_risk_share=("risk_level", lambda x: round((x == "high").mean(), 3)),
        )
        .round(3)
    )
    strategy_summary.to_csv(REPORT_DIR / "scenario_strategy_summary.csv", index=False)
    (REPORT_DIR / "scenario_ranking.md").write_text(
        "# Scenario Ranking\n\n"
        "Scenarios are grouped into conservative, balanced, and aggressive sponsor strategies.\n\n"
        "## Strategy Summary\n\n"
        + markdown_table(strategy_summary)
        + "\n\n## Top Match-Level Recommendations\n\n"
        + markdown_table(top),
        encoding="utf-8",
    )
    print(f"Saved scenario recommendations to {out_path}")


if __name__ == "__main__":
    main()
