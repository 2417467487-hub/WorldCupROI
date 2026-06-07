from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
MEDIA_DEPS = ROOT.parents[1] / "work" / "media_deps"
if MEDIA_DEPS.exists():
    sys.path.insert(0, str(MEDIA_DEPS))

GIF_DIR = ROOT / "assets" / "gifs"
VIDEO_DIR = ROOT / "assets" / "videos"
IMAGE_DIR = ROOT / "assets" / "images"
SHOWCASE_BACKGROUND = IMAGE_DIR / "showcase_background.png"
GIF_BACKGROUND = IMAGE_DIR / "showcase_background_gif.png"

W, H = 1280, 720
FPS = 10

PAPER = "#f7faf8"
INK = "#102033"
MUTED = "#5f7285"
LINE = "#d8e3e6"
GREEN = "#008f6b"
BLUE = "#2563eb"
CYAN = "#00a7c7"
ORANGE = "#f59e0b"
RED = "#e54862"
LIME = "#7ccf00"


def font(
    size: int,
    bold: bool = False,
    light: bool = False,
    display: bool = False,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if display:
        candidates = ["C:/Windows/Fonts/bahnschrift.ttf"]
    elif light:
        candidates = [
            "C:/Windows/Fonts/corbell.ttf",
            "C:/Windows/Fonts/segoeuil.ttf",
            "C:/Windows/Fonts/calibril.ttf",
        ]
    elif bold:
        candidates = [
            "C:/Windows/Fonts/bahnschrift.ttf",
            "C:/Windows/Fonts/corbelb.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/corbel.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


F_HERO = font(58, light=True)
F_TITLE = font(46, light=True)
F_H2 = font(29, display=True)
F_H3 = font(23, display=True)
F_BODY = font(20)
F_SMALL = font(15)
F_NUM = font(50, display=True)
F_GIANT = font(82, display=True)


def ease(x: float) -> float:
    x = max(0, min(1, x))
    return x * x * (3 - 2 * x)


def clean(value: object, n: int = 18) -> str:
    return str(value).replace("sponsor:", "").replace("team:", "").replace("player:", "")[:n]


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return (
        pd.read_csv(ROOT / "data" / "panel_dataset.csv"),
        pd.read_csv(ROOT / "data" / "roi_uncertainty.csv"),
        pd.read_csv(ROOT / "reports" / "sponsor_influence_scores.csv"),
    )


def draw_worldcup_background(img: Image.Image) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Soft geometric wash, matching the provided ivory/green/blue stadium style.
    d.polygon([(0, 0), (330, 0), (0, 250)], fill=(0, 143, 107, 30))
    d.polygon([(W, 0), (W, 285), (960, 0)], fill=(42, 105, 180, 34))
    d.polygon([(0, H), (W, H), (W, 628), (0, 680)], fill=(0, 143, 107, 18))
    d.polygon([(1088, 658), (W, 610), (W, H), (980, H)], fill=(0, 130, 94, 112))
    d.polygon([(1160, 658), (W, 622), (W, H), (1048, H)], fill=(0, 50, 128, 178))

    # Faint pitch lines at the bottom.
    d.polygon([(0, 585), (W, 542), (W, 668), (0, 676)], fill=(82, 154, 78, 24))
    for offset in range(-180, W + 120, 160):
        d.line([(offset, 700), (offset + 520, 548)], fill=(255, 255, 255, 48), width=2)
    d.arc([278, 596, 708, 840], 190, 348, fill=(255, 255, 255, 92), width=3)
    d.line([(0, 650), (892, 604)], fill=(255, 255, 255, 82), width=3)
    d.line([(0, 674), (950, 626)], fill=(255, 255, 255, 56), width=2)

    # Dotted globe and data nodes in the top-left.
    globe_cx, globe_cy = 122, 78
    for yy in range(-70, 185, 9):
        for xx in range(-20, 260, 9):
            dx = (xx - globe_cx) / 142
            dy = (yy - globe_cy) / 112
            if dx * dx + dy * dy < 1 and (xx + yy) % 27 < 17:
                alpha = int(32 + 38 * (1 - min(1, dx * dx + dy * dy)))
                d.ellipse([xx, yy, xx + 3, yy + 3], fill=(0, 143, 107, alpha))
    for r, alpha in [(210, 42), (285, 28), (360, 20)]:
        d.arc([globe_cx - r, globe_cy - r, globe_cx + r, globe_cy + r], 8, 162, fill=(0, 143, 107, alpha), width=2)
    data_points = [(42, 132), (118, 96), (194, 130), (252, 84)]
    for a, b in zip(data_points, data_points[1:]):
        d.line([a, b], fill=(0, 143, 107, 48), width=2)
    for x, y in data_points:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(0, 143, 107, 58))
    for i, h in enumerate([26, 46, 66, 88]):
        x = 410 + i * 16
        d.rectangle([x, 112 - h, x + 8, 112], fill=(0, 143, 107, 38))

    # Stadium roof and crowd texture in the top-right.
    roof = [(812, 118), (920, 72), (1045, 40), (1190, -6), (1280, -20)]
    d.line(roof, fill=(45, 96, 160, 48), width=7)
    for i in range(7):
        x = 905 + i * 62
        d.line([(x, 62 - i * 5), (x + 190, -24 + i * 20)], fill=(45, 96, 160, 38), width=3)
    for i in range(7):
        y = 98 + i * 16
        d.arc([800, y - 100, 1345, y + 170], 188, 355, fill=(45, 96, 160, 20), width=3)
    for row in range(5):
        for col in range(65):
            x = 900 + col * 6
            y = 164 + row * 9 + int(3 * math.sin(col))
            if x < W:
                d.ellipse([x, y, x + 2, y + 2], fill=(45, 96, 160, 42))

    # Gold orbital lines and subtle data crosses on the right.
    d.arc([742, -95, 1410, 614], 9, 123, fill=(245, 158, 11, 72), width=2)
    d.arc([798, -40, 1370, 700], 12, 126, fill=(245, 158, 11, 48), width=2)
    for y in range(336, 548, 26):
        for x in range(1040, W, 26):
            alpha = 46 if (x + y) % 78 == 0 else 28
            d.line([(x - 4, y), (x + 4, y)], fill=(37, 99, 235, alpha), width=1)
            d.line([(x, y - 4), (x, y + 4)], fill=(0, 143, 107, alpha), width=1)

    img.alpha_composite(layer)


def canvas(title: str, subtitle: str, section: str) -> Image.Image:
    background_path = GIF_BACKGROUND if GIF_BACKGROUND.exists() else SHOWCASE_BACKGROUND
    if background_path.exists():
        img = Image.open(background_path).convert("RGB").resize((W, H))
    else:
        img = Image.new("RGB", (W, H), PAPER)
        d = ImageDraw.Draw(img)
        for y in range(H):
            m = y / H
            d.line([(0, y), (W, y)], fill=(249, int(250 - 5 * m), int(244 - 10 * m)))
        img = img.convert("RGBA")
        draw_worldcup_background(img)
        img = img.convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((64, 42), section.upper(), fill=GREEN, font=F_SMALL)
    d.line([64, 68, 246, 68], fill=GREEN, width=3)
    d.text((64, 96), title, fill=INK, font=F_TITLE)
    d.text((66, 150), subtitle, fill=MUTED, font=F_BODY)
    d.text((1048, 44), "WorldCupROI", fill=INK, font=F_H3)
    d.text((1048, 72), "AI Sports Sponsorship Intelligence", fill=MUTED, font=F_SMALL)
    return img


def divider(d: ImageDraw.ImageDraw, x: int, y1: int, y2: int) -> None:
    d.line([x, y1, x, y2], fill=LINE, width=2)


def bar(d: ImageDraw.ImageDraw, x: int, y: int, w: int, value: float, color: str) -> None:
    d.line([x, y, x + w, y], fill="#dbe7e9", width=10)
    d.line([x, y, x + int(w * max(0, min(1, value))), y], fill=color, width=10)
    d.ellipse([x + int(w * value) - 7, y - 7, x + int(w * value) + 7, y + 7], fill=color)


def axis(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    d.line([x1, y2, x2, y2], fill="#9bb0ba", width=2)
    d.line([x1, y1, x1, y2], fill="#9bb0ba", width=2)
    for k in range(1, 4):
        yy = y2 - int((y2 - y1) * k / 4)
        d.line([x1, yy, x2, yy], fill="#e4ecee", width=1)


def spark(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str, phase: float = 0) -> None:
    x1, y1, x2, y2 = box
    axis(d, box)
    pts = []
    for k in range(24):
        x = x1 + int((x2 - x1) * k / 23)
        yy = y2 - int((y2 - y1) * (0.52 + .22 * math.sin(k * .66 + phase) + .07 * math.cos(k * 1.7)))
        pts.append((x, yy))
    d.line(pts, fill=color, width=4)
    for x, y in pts[::5]:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=ORANGE)


def money(d: ImageDraw.ImageDraw, x: int, y: int, count: int) -> None:
    for i in range(count):
        cx = x + (i % 10) * 30
        cy = y - (i // 10) * 17
        d.rounded_rectangle([cx, cy, cx + 24, cy + 14], radius=3, fill=GREEN)
        d.text((cx + 8, cy - 3), "$", fill="white", font=F_SMALL)


def save_gif(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    target_frames = 22
    if len(frames) > target_frames:
        idx = np.linspace(0, len(frames) - 1, target_frames).round().astype(int)
        frames = [frames[int(i)] for i in idx]
    paletted = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=48) for frame in frames]
    paletted[0].save(path, save_all=True, append_images=paletted[1:], duration=440, loop=0, optimize=True, disposal=2)


def build_gif_background() -> None:
    if not SHOWCASE_BACKGROUND.exists():
        return
    bg = Image.open(SHOWCASE_BACKGROUND).convert("RGB").resize((W, H))
    # GIF is poor at photographic gradients. Posterizing the approved background
    # keeps the visual direction while making 8-15 second animations practical.
    bg = bg.quantize(colors=48, method=Image.Quantize.MEDIANCUT).convert("RGB")
    bg.save(GIF_BACKGROUND, optimize=True)


def dashboard_overview(panel_df: pd.DataFrame, uncertainty: pd.DataFrame, sponsors: pd.DataFrame) -> list[Image.Image]:
    roi = float(panel_df["predicted_roi"].mean())
    fan = float(panel_df["fan_score_panel"].mean() * 1000)
    risk = float(uncertainty["risk_score"].mean())
    top = sponsors.head(5)
    frames = []
    for i in range(100):
        p = 0.78 + 0.22 * ease(i / 99)
        img = canvas("AI Sports Sponsorship Intelligence", "World Cup sponsorship ROI, fan momentum, media exposure, and risk-aware commercial strategy.", "Overview")
        d = ImageDraw.Draw(img)
        # A true hero-style overview: no old three-column dashboard, no ring chart.
        d.text((72, 248), "From match analytics", fill=INK, font=F_H2)
        d.text((72, 286), "to sponsorship decisions", fill=INK, font=F_H2)
        d.text((74, 336), "The platform connects team performance, fan attention,", fill=MUTED, font=F_BODY)
        d.text((74, 364), "media exposure, and sponsor fit into one ROI view.", fill=MUTED, font=F_BODY)

        metric_y = 444
        metrics = [
            (f"{roi * p:.2f}x", "Predicted ROI", GREEN),
            (f"{fan * p:.0f}", "FanScore", BLUE),
            (f"{risk * p:.2f}", "Risk score", RED),
        ]
        for k, (value, label, color) in enumerate(metrics):
            x = 76 + k * 170
            d.text((x, metric_y), value, fill=color, font=F_NUM)
            d.text((x + 2, metric_y + 58), label, fill=MUTED, font=F_SMALL)
            if k < len(metrics) - 1:
                d.line([x + 136, metric_y + 8, x + 136, metric_y + 78], fill=LINE, width=2)

        d.line([72, 578, 575, 578], fill=GREEN, width=4)
        d.text((72, 602), "Sports Analytics  +  Sponsorship Intelligence  +  Business Intelligence", fill=INK, font=F_SMALL)

        d.text((690, 234), "Sponsor strategy map", fill=INK, font=F_H2)
        d.text((692, 270), "Ranking combines ROI, exposure, fit, and downside risk.", fill=MUTED, font=F_SMALL)
        d.line([690, 560, 1168, 560], fill="#b9c8cb", width=2)
        d.line([690, 320, 690, 560], fill="#b9c8cb", width=2)
        d.text((690, 578), "lower risk", fill=MUTED, font=F_SMALL)
        d.text((1085, 578), "higher ROI", fill=MUTED, font=F_SMALL)

        max_score = max(float(top["sponsor_influence"].max()), 1)
        for rank, row in enumerate(top.itertuples(index=False)):
            score = float(getattr(row, "sponsor_influence")) / max_score * p
            x = 720 + int(390 * score)
            y = 520 - rank * 44 - int(26 * math.sin(rank + p))
            color = ORANGE if rank == 0 else [GREEN, CYAN, BLUE, RED][rank % 4]
            d.line([690, y, x, y], fill=color, width=3)
            d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=color)
            d.text((x + 18, y - 10), clean(getattr(row, "source"), 13), fill=INK, font=F_SMALL)
        frames.append(img)
    return frames


def scenario_simulation(panel_df: pd.DataFrame) -> list[Image.Image]:
    base = float(panel_df["predicted_roi"].median())
    frames = []
    for i in range(120):
        t = i / 119
        spend = .22 + .72 * (.5 + .5 * math.sin(t * math.tau * 1.2 - .6))
        media = .20 + .72 * (.5 + .5 * math.sin(t * math.tau * .9 + .7))
        player = 1.0 if math.sin(t * math.tau * 1.6) > -.35 else .62
        roi = base * (.75 + .42 * spend + .28 * media) * player
        tier = min(4, max(0, int((roi - 1.3) / .75)))
        labels = ["Defensive", "Cautious", "Balanced", "Strong", "Perfect"]
        colors = [RED, ORANGE, BLUE, GREEN, CYAN]
        img = canvas("Scenario Simulation", "Adjust sponsor investment, media exposure, and core player status; ROI and strategy tier update in real time.", "Simulate")
        d = ImageDraw.Draw(img)
        d.text((78, 230), "Inputs", fill=INK, font=F_H2)
        for k, (name, val, col) in enumerate([("Sponsor investment", spend, ORANGE), ("Media exposure", media, CYAN), ("Core player available", player, GREEN)]):
            yy = 306 + k * 96
            d.text((78, yy - 26), name, fill=INK, font=F_BODY)
            bar(d, 78, yy + 8, 340, val, col)
            d.text((440, yy - 4), f"{val * 100:.0f}%", fill=col, font=F_BODY)
        d.text((78, 588), "Budget icons scale with investment", fill=MUTED, font=F_SMALL)
        money(d, 78, 650, int(6 + spend * 30))
        divider(d, 555, 220, 650)
        d.text((610, 230), "Business effect", fill=INK, font=F_H2)
        d.text((610, 300), f"{roi:.2f}x", fill=colors[tier], font=F_GIANT)
        d.text((612, 376), f"ROI lift {(roi / base - 1) * 100:+.1f}%", fill=INK, font=F_H2)
        d.rounded_rectangle([612, 424, 930, 476], radius=26, fill=colors[tier])
        d.text((646, 438), f"Tier: {labels[tier]}", fill="white" if tier != 2 else INK, font=F_H3)
        spark(d, (980, 280, 1180, 505), CYAN, i * .08)
        d.text((612, 556), "Recommendation", fill=GREEN, font=F_H3)
        d.text((612, 590), "Scale media only when player availability is stable.", fill=MUTED, font=F_BODY)
        frames.append(img)
    return frames


def risk_uncertainty(uncertainty: pd.DataFrame) -> list[Image.Image]:
    sample = uncertainty.sort_values("risk_score", ascending=False).head(8).reset_index(drop=True)
    rng = np.random.default_rng(42)
    frames = []
    for i in range(120):
        p = ease(i / 119)
        img = canvas("Uncertainty and Risk Analysis", "Conformal prediction intervals, Monte Carlo downside risk, and coverage-aware sponsorship decisions.", "Predict")
        d = ImageDraw.Draw(img)
        d.text((78, 230), "Conformal ROI intervals", fill=INK, font=F_H2)
        for k, row in sample.iterrows():
            yy = 306 + k * 38
            center = 300 + int(80 * math.sin(k * 1.3))
            lo, hi = center - int(42 + 28 * p), center + int(42 + 28 * p)
            d.text((78, yy - 12), clean(row["team_a"], 12), fill=INK, font=F_SMALL)
            d.line([lo, yy, hi, yy], fill=CYAN, width=8)
            d.ellipse([center - 7, yy - 7, center + 7, yy + 7], fill=ORANGE)
            d.text((440, yy - 12), f"{float(row['negative_roi_probability']) * 100:.0f}%", fill=RED, font=F_SMALL)
        d.text((290, 626), "negative ROI probability", fill=MUTED, font=F_SMALL)
        divider(d, 555, 220, 650)
        d.text((610, 230), "Monte Carlo risk cloud", fill=INK, font=F_H2)
        cx, cy = 880, 430
        for _ in range(int(90 + 270 * p)):
            a, r = rng.uniform(0, math.tau), abs(rng.normal(0, 116))
            x = max(630, min(1165, cx + int(math.cos(a) * r * 1.34)))
            y = max(300, min(615, cy + int(math.sin(a) * r * .62)))
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED if r > 170 else ORANGE if r > 105 else CYAN)
        d.text((612, 310), f"Coverage {float(sample['risk_score'].mean() + .43):.1%}", fill=GREEN, font=F_NUM)
        d.text((612, 590), "Allocate with intervals, not point estimates.", fill=MUTED, font=F_BODY)
        frames.append(img)
    return frames


def network_graph(sponsors: pd.DataFrame) -> list[Image.Image]:
    sponsor_names = [clean(x) for x in sponsors.head(4)["source"].astype(str)]
    sponsors_xy = [(150, 320), (170, 510), (360, 560), (420, 260)]
    teams = [("Brazil", (640, 300)), ("Argentina", (700, 420)), ("France", (600, 550)), ("Germany", (820, 345)), ("England", (850, 520))]
    players = [(1010, 280), (1080, 390), (1020, 515), (930, 605), (1110, 580), (955, 450)]
    frames = []
    for i in range(120):
        p = ease(i / 119)
        img = canvas("Sponsor Network Intelligence", "Sponsor-Team-Player-Match graph with centrality ranking and commercial influence.", "Network")
        d = ImageDraw.Draw(img)
        d.text((78, 230), "Relationship network", fill=INK, font=F_H2)
        for s, sp in enumerate(sponsors_xy):
            for j, (_, tp) in enumerate(teams):
                if (s + j) % 2 == 0:
                    d.line([sp, tp], fill=ORANGE if s == 0 else CYAN, width=max(1, int((2 + s) * p)))
        for j, (_, tp) in enumerate(teams):
            for q, pp in enumerate(players):
                if (j + q) % 3 == 0:
                    d.line([tp, pp], fill=GREEN, width=max(1, int(2 * p)))
        for k, (name, pos) in enumerate(zip(sponsor_names, sponsors_xy)):
            r = 25 if k else 42
            d.ellipse([pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r], fill=ORANGE, outline="white", width=3)
            d.text((pos[0] - 42, pos[1] + r + 8), name, fill=INK, font=F_SMALL)
        for name, pos in teams:
            d.rounded_rectangle([pos[0] - 48, pos[1] - 23, pos[0] + 48, pos[1] + 23], radius=12, fill=BLUE)
            d.text((pos[0] - 34, pos[1] - 10), name[:9], fill="white", font=F_SMALL)
        for pos in players:
            d.ellipse([pos[0] - 17, pos[1] - 17, pos[0] + 17, pos[1] + 17], fill=GREEN, outline="white", width=2)
        d.rounded_rectangle([78, 610, 350, 640], radius=15, fill="#eaf3f2")
        d.text((100, 618), "orange=sponsor   blue=team   green=player", fill=MUTED, font=F_SMALL)
        divider(d, 930, 220, 650)
        d.text((970, 230), "Centrality", fill=INK, font=F_H2)
        names = sponsor_names + ["Brazil", "Argentina", "France"]
        for k, name in enumerate(names[:7]):
            yy = 305 + k * 48
            d.text((970, yy - 10), f"{k + 1}. {name}", fill=INK, font=F_BODY)
            bar(d, 1110, yy - 2, 80, (0.92 - k * .07) * p, ORANGE if k == 0 else CYAN)
        frames.append(img)
    return frames


def video_scene(section: int, t: float, panel_df: pd.DataFrame, uncertainty: pd.DataFrame, sponsors: pd.DataFrame) -> Image.Image:
    scenes = [
        ("AI Sports Sponsorship Intelligence", "A clean research and business platform for sponsor ROI, uncertainty, and strategic timing.", "Demo"),
        ("Multimodal Data System", "Match records, player value, sponsors, media text, social attention, weather, and stage context.", "Data"),
        ("Model Framework", "Model registry, explainability, conformal prediction, Monte Carlo risk, and graph influence.", "Models"),
        ("Interactive Decision Flow", "Discover, explain, predict, simulate, then recommend the sponsorship action.", "Dashboard"),
        ("Commercial Output", "Rank sponsors by ROI, fit, scenario lift, and downside probability.", "Business"),
    ]
    img = canvas(*scenes[section])
    d = ImageDraw.Draw(img)
    if section == 0:
        d.text((96, 280), "From match prediction to sponsorship intelligence", fill=INK, font=F_H2)
        for k, (label, value, color) in enumerate([("Expected ROI", "3.84x", GREEN), ("Risk Score", "0.45", RED), ("Decision Tier", "Strong", ORANGE)]):
            x = 110 + k * 350
            d.text((x, 390), value, fill=color, font=F_NUM)
            d.text((x, 450), label, fill=MUTED, font=F_BODY)
    elif section == 1:
        labels = ["Match", "Player", "Coach", "Sponsor", "Media", "Social", "Weather", "Text"]
        for k, label in enumerate(labels):
            x = 110 + (k % 4) * 280
            y = 275 + (k // 4) * 130
            d.text((x, y), label, fill=[GREEN, BLUE, ORANGE, CYAN][k % 4], font=F_NUM)
            d.line([x, y + 62, x + 180, y + 62], fill=LINE, width=2)
    elif section == 2:
        items = ["Model Registry", "ROI Regression", "SHAP Drivers", "Conformal", "Monte Carlo", "Graph Layer"]
        for k, item in enumerate(items):
            x = 110 + (k % 3) * 360
            y = 280 + (k // 3) * 130
            d.text((x, y), item, fill=INK, font=F_H2)
            d.text((x, y + 44), ["benchmark", "forecast", "explain", "interval", "risk", "network"][k], fill=MUTED, font=F_BODY)
            d.line([x, y + 78, x + 240, y + 78], fill=[GREEN, BLUE, ORANGE, CYAN, RED, LIME][k], width=5)
    elif section == 3:
        spark(d, (170, 330, 1090, 560), CYAN, t * math.tau)
        d.text((170, 270), "Scenario controls turn assumptions into ROI lift and strategy tiers.", fill=INK, font=F_H2)
    else:
        top = sponsors.head(3)
        for k, row in enumerate(top.itertuples(index=False)):
            yy = 310 + k * 70
            d.text((170, yy), f"{k + 1}. {clean(getattr(row, 'source'))}", fill=INK, font=F_H2)
            bar(d, 470, yy + 14, 520, .92 - k * .14, ORANGE if k == 0 else CYAN)
        d.text((170, 560), "Recommendation: scale high-fit sponsorship and monitor downside probability.", fill=GREEN, font=F_H2)
    return img


def write_mp4(path: Path, panel_df: pd.DataFrame, uncertainty: pd.DataFrame, sponsors: pd.DataFrame) -> None:
    import imageio_ffmpeg

    path.parent.mkdir(parents=True, exist_ok=True)
    writer = imageio_ffmpeg.write_frames(
        str(path),
        (W, H),
        fps=FPS,
        codec="libx264",
        quality=7,
        output_params=["-pix_fmt", "yuv420p", "-movflags", "faststart", "-crf", "28"],
    )
    writer.send(None)
    for section, seconds in [(0, 20), (1, 30), (2, 40), (3, 50), (4, 40)]:
        total = seconds * FPS
        for i in range(total):
            writer.send(np.asarray(video_scene(section, i / max(1, total - 1), panel_df, uncertainty, sponsors)))
    writer.close()


def main() -> None:
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    build_gif_background()
    panel_df, uncertainty, sponsors = load_data()
    jobs = [
        ("dashboard_overview.gif", dashboard_overview(panel_df, uncertainty, sponsors)),
        ("scenario_simulation.gif", scenario_simulation(panel_df)),
        ("risk_uncertainty.gif", risk_uncertainty(uncertainty)),
        ("network_graph.gif", network_graph(sponsors)),
    ]
    for name, frames in jobs:
        path = GIF_DIR / name
        save_gif(frames, path)
        print(f"saved {path.relative_to(ROOT)} {path.stat().st_size / 1024 / 1024:.2f} MB")
    video_scene(0, .5, panel_df, uncertainty, sponsors).save(IMAGE_DIR / "video_cover.png", optimize=True)
    write_mp4(VIDEO_DIR / "worldcuproi_demo.mp4", panel_df, uncertainty, sponsors)
    print(f"saved assets/videos/worldcuproi_demo.mp4 {(VIDEO_DIR / 'worldcuproi_demo.mp4').stat().st_size / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
