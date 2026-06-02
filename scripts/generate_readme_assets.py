from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
ASSET_DIR.mkdir(parents=True, exist_ok=True)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


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
    architecture_svg()
    dashboard_preview()
    gif_demo()
    print(f"Generated README assets in {ASSET_DIR}")


if __name__ == "__main__":
    main()
