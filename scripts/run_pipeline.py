from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    "src/real_data_ingestion.py",
    "src/text_dimensionality.py",
    "src/feature_builder.py",
    "src/advanced_features.py",
    "src/data_quality.py",
    "src/train_match_model.py",
    "src/train_roi_model.py",
    "src/uncertainty.py",
    "src/scenario_engine.py",
    "src/build_panel_data.py",
    "src/build_plotly_dashboard.py",
]


def main() -> None:
    for step in STEPS:
        print(f"\n==> {step}")
        subprocess.run([sys.executable, step], cwd=ROOT, check=True)
    print("\nPipeline complete. Open dashboard/panel_dashboard.html")


if __name__ == "__main__":
    main()
