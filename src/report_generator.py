from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def ensure_outputs() -> None:
    if not (DATA_DIR / "panel_dataset.csv").exists():
        from build_panel_data import main as build_panel

        build_panel()
    if not (REPORT_DIR / "ab_simulation_summary.csv").exists():
        from ab_simulation import main as run_ab

        run_ab()


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_simple_pdf(path: Path, lines: list[str]) -> None:
    # Minimal single-page PDF writer, dependency-free for reproducible demo output.
    content_lines = ["BT", "/F1 14 Tf", "50 780 Td"]
    for i, line in enumerate(lines[:34]):
        size = 18 if i == 0 else 11
        content_lines.append(f"/F1 {size} Tf")
        content_lines.append(f"({pdf_escape(line)}) Tj")
        content_lines.append("0 -22 Td")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for off in offsets:
        pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    path.write_bytes(pdf)


def main() -> None:
    ensure_outputs()
    REPORT_DIR.mkdir(exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    ab = pd.read_csv(REPORT_DIR / "ab_simulation_summary.csv")
    top = panel.sort_values("predicted_roi", ascending=False).head(1).iloc[0]
    lines = [
        "WorldCupROI Sample Report",
        f"Panel rows: {len(panel):,}",
        f"Teams: {panel['team'].nunique()}",
        f"Sponsors: {panel['sponsor'].nunique()}",
        f"Average predicted ROI: {panel['predicted_roi'].mean():.3f}x",
        f"Average commercial momentum: {panel['commercial_momentum'].mean():.3f}",
        f"Top opportunity: {top['team']} x {top['sponsor']} vs {top['opponent']}",
        f"Top predicted ROI: {top['predicted_roi']:.3f}x",
        "",
        "A/B Simulation Summary:",
    ]
    for _, row in ab.reset_index().iterrows():
        scenario = row["scenario"] if "scenario" in row else row.iloc[0]
        delta = row["avg_roi_delta"] if "avg_roi_delta" in row else row.iloc[2]
        lift = row["avg_roi_lift_pct"] if "avg_roi_lift_pct" in row else row.iloc[3]
        lines.append(f"- {scenario}: delta {float(delta):.3f}, lift {float(lift):.2f}%")
    lines.extend(
        [
            "",
            "Dashboard modules: match probabilities, sponsor ROI, FanScore radar, weather impact heatmap.",
            "Models: fallback ML pipeline with XGBoost/LightGBM/SHAP upgrade path.",
        ]
    )
    md = "\n".join(["# " + lines[0], *[f"- {line}" if line else "" for line in lines[1:]]])
    (REPORT_DIR / "sample_report.md").write_text(md, encoding="utf-8")
    write_simple_pdf(ROOT / "sample_report.pdf", lines)
    print(f"Saved sample report to {ROOT / 'sample_report.pdf'}")


if __name__ == "__main__":
    main()

