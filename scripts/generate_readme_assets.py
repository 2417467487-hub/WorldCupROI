from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
IMAGE_DIR = ROOT / "assets" / "images"
ASSET_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/bahnschrift.ttf" if bold else "C:/Windows/Fonts/corbel.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def multiline(draw: ImageDraw.ImageDraw, xy: tuple[int, int], lines: Iterable[str], fill: str, font_obj: ImageFont.ImageFont, gap: int = 8) -> None:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, fill=fill, font=font_obj)
        y += font_obj.size + gap if hasattr(font_obj, "size") else 24


def readme_hero() -> None:
    """Generate a top-ML-paper-style method overview for the README opening."""
    w, h = 1800, 1080
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    ink = "#111827"
    muted = "#4b5563"
    grid = "#d6d9df"
    faint = "#f6f7f9"
    blue = "#0072B2"
    orange = "#E69F00"
    green = "#009E73"
    red = "#D55E00"
    purple = "#6A5ACD"

    d.text((72, 54), "WorldCupROI", fill=ink, font=font(60, True))
    d.text((76, 122), "A multi-source machine learning pipeline for sponsorship ROI under uncertainty", fill=muted, font=font(25))
    d.line([72, 172, 1728, 172], fill=grid, width=2)

    def panel(x: int, y: int, pw: int, ph: int, tag: str, title_text: str, desc: str) -> None:
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10, fill="#ffffff", outline=grid, width=2)
        d.rectangle([x, y, x + 48, y + 40], fill=faint, outline=grid, width=1)
        d.text((x + 14, y + 8), tag, fill=ink, font=font(20, True))
        d.text((x + 64, y + 10), title_text, fill=ink, font=font(21, True))
        d.text((x + 24, y + ph - 34), desc, fill=muted, font=font(13))

    def arrow_between(x1: int, y1: int, x2: int, y2: int) -> None:
        d.line([x1, y1, x2, y2], fill="#737a84", width=3)
        d.polygon([(x2, y2), (x2 - 12, y2 - 7), (x2 - 12, y2 + 7)], fill="#737a84")

    # A. Multi-modal evidence: table, mini heatmap, and text tokens.
    panel(72, 210, 390, 330, "A", "Multi-source evidence", "Aligned sponsor-event evidence.")
    d.text((98, 268), "tabular panel", fill=muted, font=font(16))
    d.rectangle([98, 294, 244, 414], outline=grid, width=1)
    for i in range(1, 5):
        d.line([98, 294 + i * 24, 244, 294 + i * 24], fill=grid)
    for i in range(1, 4):
        d.line([98 + i * 36, 294, 98 + i * 36, 414], fill=grid)
    heat = [[0.2, 0.8, 0.5, 0.7], [0.6, 0.3, 0.9, 0.4], [0.7, 0.5, 0.2, 0.8], [0.4, 0.7, 0.6, 0.3]]
    for r, row in enumerate(heat):
        for c, v in enumerate(row):
            shade = int(245 - v * 95)
            d.rectangle([108 + c * 30, 420 + r * 22, 132 + c * 30, 438 + r * 22], fill=(shade, shade + 6, 252), outline="#ffffff")
    d.text((278, 268), "text evidence", fill=muted, font=font(16))
    tokens = ["brand heat", "match stage", "fan growth", "media tone"]
    yy = 304
    for t in tokens:
        d.rounded_rectangle([278, yy, 432, yy + 30], radius=5, fill="#eef5fb", outline="#c8d9e8")
        d.text((288, yy + 7), t, fill=blue, font=font(14, True))
        yy += 42

    # B. Feature construction: formulas and feature groups.
    panel(542, 210, 390, 330, "B", "Feature construction", "Encodes attention, fit and risk.")
    formula_lines = [
        "FanScore = followers + attention + reposts",
        "SPI = spend x exposure x brand fit",
        "Momentum = stage premium + text signal",
        "Risk = injury + weather + interval width",
    ]
    yy = 284
    for i, line in enumerate(formula_lines):
        color = [green, blue, orange, red][i]
        d.rectangle([572, yy - 10, 586, yy + 10], fill=color)
        d.text((604, yy - 12), line, fill=ink, font=font(15))
        yy += 52
    d.rectangle([572, 458, 900, 486], fill=faint, outline=grid)
    d.text((586, 465), "feature store: panel x text x graph x time", fill=muted, font=font(14, True))

    # C. Model system: shared representation with heads.
    panel(1012, 210, 390, 330, "C", "Multi-task model", "Prediction and graph heads share features.")
    d.rectangle([1064, 324, 1230, 424], fill=faint, outline=grid, width=2)
    d.text((1092, 356), "shared", fill=ink, font=font(18, True))
    d.text((1082, 386), "representation", fill=ink, font=font(18, True))
    heads = [("match", green, 1258, 270), ("ROI", blue, 1258, 350), ("GNN", purple, 1258, 430)]
    for label, color, hx, hy in heads:
        d.line([1230, 374, hx, hy + 24], fill="#808792", width=2)
        d.rectangle([hx, hy, hx + 118, hy + 48], fill="#ffffff", outline=color, width=3)
        d.text((hx + 34, hy + 14), label, fill=color, font=font(16, True))
    for i in range(4):
        d.rectangle([1044 + i * 26, 474 - i * 20, 1064 + i * 26, 490], fill=orange if i % 2 else blue)

    # D. Decision outputs: SHAP bars, interval, ranking.
    panel(72, 610, 650, 285, "D", "Explainable outputs", "Drivers and intervals precede decisions.")
    shap_names = ["brand heat", "team strength", "sponsor spend", "ad exposure", "fit"]
    shap_vals = [0.135, 0.133, 0.133, 0.114, 0.045]
    max_v = max(shap_vals)
    yy = 680
    for name, val in zip(shap_names, shap_vals):
        d.text((98, yy + 3), name, fill=ink, font=font(14))
        d.rectangle([236, yy, 436, yy + 17], fill="#eef0f3")
        d.rectangle([236, yy, 236 + int(200 * val / max_v), yy + 17], fill=green)
        d.text((450, yy - 1), f"{val:.3f}", fill=muted, font=font(13))
        yy += 34
    pts = [(552, 784), (586, 734), (620, 762), (654, 714), (688, 736)]
    d.line(pts, fill=blue, width=3)
    for x, y in pts:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=blue)
    d.text((540, 680), "ROI interval", fill=muted, font=font(14, True))
    d.line([540, 820, 704, 820], fill=grid)

    # E. GNN interpretability.
    panel(802, 610, 590, 285, "E", "Heterogeneous graph explanation", "Message passing aggregates graph signals.")
    nodes = {
        "Sponsor": (900, 750, blue),
        "Team": (1060, 704, green),
        "Player": (1060, 810, orange),
        "Match": (1240, 750, purple),
    }
    for a, b, lw in [("Sponsor", "Team", 5), ("Team", "Player", 4), ("Player", "Match", 4), ("Team", "Match", 3), ("Sponsor", "Player", 2)]:
        x1, y1, _ = nodes[a]
        x2, y2, _ = nodes[b]
        d.line([x1, y1, x2, y2], fill="#9aa1aa", width=lw)
    for label, (x, y, color) in nodes.items():
        d.ellipse([x - 42, y - 42, x + 42, y + 42], fill="#ffffff", outline=color, width=5)
        bbox = d.textbbox((0, 0), label, font=font(15, True))
        d.text((x - (bbox[2] - bbox[0]) / 2, y - 8), label, fill=ink, font=font(15, True))
    d.line([1188, 670, 1248, 670], fill="#9aa1aa", width=5)
    d.text((1260, 664), "edge weight", fill=muted, font=font(13))

    # F. Business layer.
    panel(1482, 210, 246, 685, "F", "Decision layer", "Guides sponsor strategy.")
    kpis = [("0.8687", "ROI R^2"), ("0.1177", "MAE"), ("0.9021", "coverage"), ("5,450", "text units")]
    yy = 302
    for value, label in kpis:
        d.text((1510, yy), value, fill=ink, font=font(26, True))
        d.text((1510, yy + 32), label, fill=muted, font=font(14))
        d.line([1510, yy + 58, 1704, yy + 58], fill=grid)
        yy += 92
    d.rectangle([1510, 690, 1704, 800], fill=faint, outline=grid)
    d.text((1528, 722), "Discover -> Explain", fill=ink, font=font(14, True))
    d.text((1528, 754), "Predict -> Simulate", fill=ink, font=font(14, True))
    d.text((1528, 786), "Recommend", fill=red, font=font(14, True))

    # Cross-panel arrows.
    for x1, y1, x2, y2 in [(462, 374, 542, 374), (932, 374, 1012, 374), (1402, 374, 1482, 374), (1190, 540, 1050, 610), (722, 752, 802, 752), (1392, 752, 1482, 752)]:
        arrow_between(x1, y1, x2, y2)

    d.text((72, 972), "Figure 1. Method overview. WorldCupROI links multi-source evidence to multi-task learning, graph influence, explainability and uncertainty-aware sponsorship decisions.", fill=muted, font=font(15))
    d.text((72, 1010), "Generated by Python: scripts/generate_readme_assets.py; metrics are read from the current reproducible project outputs.", fill=muted, font=font(12))

    img.save(IMAGE_DIR / "readme_hero.png", dpi=(300, 300))


def svg_card(title: str, subtitle: str, body: str, filename: str, accent: str = "#0f8b6f") -> None:
    content = f"""<svg width="1280" height="640" viewBox="0 0 1280 640" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1280" height="640" rx="0" fill="#07140f"/>
  <rect x="58" y="58" width="1164" height="524" rx="26" fill="#f7fbff"/>
  <rect x="58" y="58" width="1164" height="120" rx="26" fill="{accent}"/>
  <text x="96" y="132" font-family="Segoe UI, Arial" font-size="48" font-weight="700" fill="#ffffff">{title}</text>
  <text x="96" y="224" font-family="Segoe UI, Arial" font-size="30" font-weight="700" fill="#0d1726">{subtitle}</text>
  <text x="96" y="280" font-family="Segoe UI, Arial" font-size="24" fill="#485568">{body}</text>
  <circle cx="1112" cy="390" r="92" fill="#f28c28" opacity="0.18"/>
  <circle cx="1034" cy="438" r="56" fill="#2457c5" opacity="0.18"/>
  <circle cx="1148" cy="474" r="42" fill="{accent}" opacity="0.28"/>
</svg>"""
    (ASSET_DIR / filename).write_text(content, encoding="utf-8")


def architecture_svg() -> None:
    boxes = [
        ("Real data", "matches, news, text, sponsors", 80, 170, "#0f8b6f"),
        ("Feature layer", "FanScore, sponsor power, momentum", 380, 170, "#2457c5"),
        ("Models", "match probability + ROI regression", 700, 170, "#f28c28"),
        ("Decision cockpit", "risk, scenarios, recommendations", 1000, 170, "#6d5bd0"),
    ]
    lines = []
    for title, subtitle, x, y, color in boxes:
        lines.append(f'<rect x="{x}" y="{y}" width="220" height="150" rx="18" fill="{color}"/>')
        lines.append(f'<text x="{x+24}" y="{y+55}" font-family="Segoe UI, Arial" font-size="25" font-weight="700" fill="#fff">{title}</text>')
        lines.append(f'<text x="{x+24}" y="{y+96}" font-family="Segoe UI, Arial" font-size="16" fill="#eef6ff">{subtitle}</text>')
    arrows = """
      <path d="M310 245H365" stroke="#0d1726" stroke-width="5" marker-end="url(#a)"/>
      <path d="M610 245H685" stroke="#0d1726" stroke-width="5" marker-end="url(#a)"/>
      <path d="M930 245H985" stroke="#0d1726" stroke-width="5" marker-end="url(#a)"/>
    """
    svg = f"""<svg width="1280" height="520" viewBox="0 0 1280 520" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#0d1726"/></marker></defs>
      <rect width="1280" height="520" fill="#f6f8fb"/>
      <text x="70" y="82" font-family="Segoe UI, Arial" font-size="42" font-weight="700" fill="#0d1726">Platform Architecture</text>
      <text x="70" y="126" font-family="Segoe UI, Arial" font-size="20" fill="#627085">Sports analytics + sponsorship intelligence + business decision support</text>
      {''.join(lines)}
      {arrows}
    </svg>"""
    (ASSET_DIR / "architecture.svg").write_text(svg, encoding="utf-8")


def dashboard_preview() -> None:
    panel = pd.read_csv(ROOT / "data" / "panel_dataset.csv")
    roi = panel["predicted_roi"].mean()
    momentum = panel["commercial_momentum"].mean()
    svg = f"""<svg width="1280" height="720" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
      <rect width="1280" height="720" fill="#07140f"/>
      <rect x="48" y="48" width="1184" height="624" rx="28" fill="#f7fbff"/>
      <text x="84" y="112" font-family="Segoe UI, Arial" font-size="38" font-weight="700" fill="#0d1726">Dashboard Preview</text>
      <text x="84" y="150" font-family="Segoe UI, Arial" font-size="18" fill="#627085">Discover -> Explain -> Predict -> Simulate -> Recommend</text>
      <rect x="84" y="204" width="245" height="132" rx="18" fill="#0f8b6f"/>
      <text x="112" y="254" font-family="Segoe UI, Arial" font-size="22" font-weight="700" fill="#fff">Avg ROI</text>
      <text x="112" y="308" font-family="Segoe UI, Arial" font-size="44" font-weight="700" fill="#fff">{roi:.2f}x</text>
      <rect x="365" y="204" width="245" height="132" rx="18" fill="#2457c5"/>
      <text x="393" y="254" font-family="Segoe UI, Arial" font-size="22" font-weight="700" fill="#fff">Momentum</text>
      <text x="393" y="308" font-family="Segoe UI, Arial" font-size="44" font-weight="700" fill="#fff">{momentum:.2f}</text>
      <rect x="646" y="204" width="245" height="132" rx="18" fill="#f28c28"/>
      <text x="674" y="254" font-family="Segoe UI, Arial" font-size="22" font-weight="700" fill="#fff">Text units</text>
      <text x="674" y="308" font-family="Segoe UI, Arial" font-size="44" font-weight="700" fill="#fff">5,450</text>
      <rect x="84" y="386" width="520" height="220" rx="18" fill="#fff" stroke="#d7e0ea"/>
      <polyline points="124,548 198,510 270,530 342,470 414,492 486,430 560,454" fill="none" stroke="#0f8b6f" stroke-width="7"/>
      <text x="116" y="430" font-family="Segoe UI, Arial" font-size="22" font-weight="700" fill="#0d1726">ROI trend</text>
      <rect x="646" y="386" width="502" height="220" rx="18" fill="#fff" stroke="#d7e0ea"/>
      <circle cx="754" cy="492" r="52" fill="#0f8b6f" opacity=".80"/>
      <circle cx="884" cy="526" r="34" fill="#2457c5" opacity=".75"/>
      <circle cx="986" cy="462" r="44" fill="#f28c28" opacity=".75"/>
      <text x="684" y="430" font-family="Segoe UI, Arial" font-size="22" font-weight="700" fill="#0d1726">Sponsor opportunity map</text>
    </svg>"""
    (ASSET_DIR / "dashboard_preview.svg").write_text(svg, encoding="utf-8")


def gif_demo() -> None:
    frames = []
    labels = [
        ("Discover", "Filter teams, stages, sponsors"),
        ("Explain", "Inspect ROI and commercial momentum"),
        ("Predict", "Review confidence intervals"),
        ("Simulate", "Change exposure, weather, player status"),
        ("Recommend", "Rank scenarios and actions"),
    ]
    for title, subtitle in labels:
        img = Image.new("RGB", (960, 540), "#f6f8fb")
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 960, 92], fill="#07140f")
        d.text((42, 26), "WorldCupROI Decision Flow", fill="#ffffff", font=font(34, True))
        d.rounded_rectangle([54, 136, 906, 456], radius=24, fill="#ffffff", outline="#d7e0ea", width=2)
        d.text((94, 188), title, fill="#0f8b6f", font=font(54, True))
        d.text((96, 260), subtitle, fill="#485568", font=font(28))
        d.rounded_rectangle([96, 346, 804, 384], radius=18, fill="#e8eef5")
        widths = {"Discover": 160, "Explain": 290, "Predict": 430, "Simulate": 580, "Recommend": 708}
        d.rounded_rectangle([96, 346, 96 + widths[title], 384], radius=18, fill="#f28c28")
        frames.append(img)
    frames[0].save(
        ASSET_DIR / "dashboard_walkthrough.gif",
        save_all=True,
        append_images=frames[1:],
        duration=850,
        loop=0,
        optimize=True,
    )


def main() -> None:
    readme_hero()
    svg_card(
        "WorldCupROI",
        "Sports sponsorship intelligence for match context, fan attention, and ROI decisions",
        "Real match records, real-source text units, scenario simulation, uncertainty, and dashboard reporting.",
        "hero_banner.svg",
    )
    svg_card(
        "Demo Video",
        "Two-minute walkthrough storyboard",
        "Use this cover for the recorded demo once the dashboard screen capture is uploaded.",
        "demo_video_cover.svg",
        "#2457c5",
    )
    gif_demo()
    print(f"Generated README assets in {ASSET_DIR}")


if __name__ == "__main__":
    main()
