from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


DATASETS = [
    "historical_matches.csv",
    "schedule_2026.csv",
    "players.csv",
    "coaches.csv",
    "sponsors.csv",
    "weather.csv",
    "social_media.csv",
    "attention_timeseries.csv",
    "media_text_corpus.csv",
    "relationship_network.csv",
    "modeling_dataset.csv",
    "advanced_feature_outputs.csv",
    "roi_uncertainty.csv",
    "scenario_recommendations.csv",
    "panel_dataset.csv",
]


def profile_dataset(path: Path) -> dict[str, object]:
    df = pd.read_csv(path)
    return {
        "dataset": path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "key_columns": ", ".join(df.columns[:8]),
    }


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    rows = [profile_dataset(DATA_DIR / name) for name in DATASETS if (DATA_DIR / name).exists()]
    summary = pd.DataFrame(rows)
    summary.to_csv(REPORT_DIR / "data_quality_summary.csv", index=False)

    lines = [
        "# Data Quality Summary",
        "",
        "WorldCupROI uses seeded mock data when public APIs are unavailable. This report checks the multi-source data system across tabular, text, time-series, and relationship-network files.",
        "",
        "| dataset | rows | columns | missing_cells | duplicate_rows |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['rows']} | {row['columns']} | {row['missing_cells']} | {row['duplicate_rows']} |"
        )
    (REPORT_DIR / "data_quality_summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved data quality summary to {REPORT_DIR / 'data_quality_summary.csv'}")


if __name__ == "__main__":
    main()
