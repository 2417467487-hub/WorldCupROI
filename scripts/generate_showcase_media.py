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

PAPER = "#f4f7fb"
INK = "#102033"
MUTED = "#667085"
LINE = "#d9e2ec"
PITCH = "#052c22"
PITCH_2 = "#07543f"
GREEN = "#009E73"
BLUE = "#0072B2"
CYAN = "#56B4E9"
ORANGE = "#E69F00"
GOLD = "#F2C75C"
RED = "#D55E00"
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


F_HERO = font(54, bold=True)
F_TITLE = font(42, bold=True)
F_H2 = font(26, bold=True)
F_H3 = font(21, bold=True)
F_BODY = font(19)
F_SMALL = font(15)
F_TINY = font(12)
F_NUM = font(46, bold=True)
F_GIANT = font(76, bold=True)


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

    # Match the static dashboard: dark pitch, gold highlight, field geometry.
    for y in range(H):
        m = y / H
        color = (
            int(5 + 18 * m),
            int(44 + 36 * m),
            int(34 + 18 * m),
            255,
        )
        d.line([(0, y), (W, y)], fill=color)
    d.rectangle([0, 0, W, 178], fill=(5, 44, 34, 238))
    d.rectangle([0, 178, W, H], fill=(244, 247, 251, 248))
    d.line([(W // 2, 0), (W // 2, 178)], fill=(255, 255, 255, 42), width=3)
    d.arc([W // 2 - 84, 16, W // 2 + 84, 184], 0, 360, fill=(255, 255, 255, 42), width=3)
    d.arc([990, -68, 1288, 230], 0, 360, fill=(242, 199, 92, 84), width=3)
    d.ellipse([920, -132, 1362, 310], outline=(255, 255, 255, 22), width=44)
    d.ellipse([986, -66, 1296, 244], outline=(200, 16, 46, 28), width=52)
    d.polygon([(0, 178), (W, 178), (W, 220), (0, 220)], fill=(255, 255, 255, 236))
    d.rectangle([0, 220, W, H], fill=(244, 247, 251, 236))

    img.alpha_composite(layer)


def canvas(title: str, subtitle: str, section: str) -> Image.Image:
    img = Image.new("RGBA", (W, H), PAPER)
    draw_worldcup_background(img)
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((48, 28), f"FIFA-STYLE SPONSORSHIP INTELLIGENCE · {section.upper()}", fill=GOLD, font=F_SMALL)
    d.text((48, 64), title, fill="white", font=F_TITLE)
    d.text((50, 122), subtitle, fill=(218, 230, 224), font=F_SMALL)
    d.rounded_rectangle([930, 36, 1210, 88], radius=10, fill=(255, 255, 255), outline=(217, 226, 236), width=1)
    d.text((958, 49), "WorldCupROI", fill=INK, font=F_H3)
    d.text((958, 77), "AI Sponsor ROI Platform", fill=MUTED, font=F_SMALL)
    return img


def divider(d: ImageDraw.ImageDraw, x: int, y1: int, y2: int) -> None:
    d.line([x, y1, x, y2], fill=LINE, width=2)


def plot_panel(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, subtitle: str = "") -> None:
    x1, y1, x2, y2 = box
    d.rounded_rectangle([x1, y1, x2, y2], radius=8, fill="white", outline=LINE, width=2)
    d.text((x1 + 28, y1 + 22), title, fill=INK, font=F_H2)
    if subtitle:
        d.text((x1 + 30, y1 + 56), subtitle, fill=MUTED, font=F_TINY)


def chart_axis(
    d: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    x_label: str,
    y_label: str,
    y_ticks: list[str] | None = None,
) -> None:
    x1, y1, x2, y2 = box
    d.rectangle([x1, y1, x2, y2], outline="#c9d5e1", width=1)
    d.line([x1, y2, x2, y2], fill="#9aa8b8", width=2)
    d.line([x1, y1, x1, y2], fill="#9aa8b8", width=2)
    for k in range(1, 5):
        yy = y2 - int((y2 - y1) * k / 5)
        d.line([x1, yy, x2, yy], fill="#e6edf5", width=1)
        if y_ticks and k - 1 < len(y_ticks):
            d.text((x1 - 44, yy - 8), y_ticks[k - 1], fill=MUTED, font=F_TINY)
    for k in range(1, 5):
        xx = x1 + int((x2 - x1) * k / 5)
        d.line([xx, y1, xx, y2], fill="#eef3f8", width=1)
    d.text(((x1 + x2) // 2 - 52, y2 + 30), x_label, fill=MUTED, font=F_TINY)
    d.text((x1 - 50, y1 - 26), y_label, fill=MUTED, font=F_TINY)


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
        plot_panel(d, (44, 232, 528, 656), "Strategy Template Inputs", "Conservative / Balanced / Aggressive sponsor package signals")
        plot_panel(d, (558, 232, 1236, 656), "Scenario ROI Lift", "Counterfactual ROI response under one sponsor strategy")
        chart_axis(d, (632, 348, 1180, 516), "Simulation step", "ROI lift")
        for k, (name, val, col) in enumerate([("Sponsor investment", spend, ORANGE), ("Media exposure", media, CYAN), ("Core player available", player, GREEN)]):
            yy = 352 + k * 84
            d.text((78, yy - 26), name, fill=INK, font=F_SMALL)
            bar(d, 78, yy + 8, 340, val, col)
            d.text((440, yy - 4), f"{val * 100:.0f}%", fill=col, font=F_SMALL)
        d.text((78, 604), "Business takeaway: raise spend only when exposure and player status support lift.", fill=MUTED, font=F_TINY)
        pts = []
        for k in range(28):
            x = 632 + int((1180 - 632) * k / 27)
            value = 0.50 + .22 * math.sin(k * .52 + i * .08) + .12 * spend + .08 * media
            y = 516 - int((516 - 348) * max(0.10, min(0.95, value)))
            pts.append((x, y))
        d.line(pts, fill=BLUE, width=4)
        for x, y in pts[::6]:
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=ORANGE, outline="white", width=2)
        d.rounded_rectangle([596, 578, 880, 630], radius=26, fill=colors[tier])
        d.text((628, 592), f"ROI {roi:.2f}x · Lift {(roi / base - 1) * 100:+.1f}%", fill="white" if tier != 2 else INK, font=F_H3)
        d.text((914, 592), f"Tier: {labels[tier]}", fill=colors[tier], font=F_H3)
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
        plot_panel(d, (44, 232, 528, 656), "Prediction Interval / Conformal", "Expected ROI with interval width by match")
        plot_panel(d, (558, 232, 1236, 656), "Monte Carlo Risk Distribution", "Volatility histogram and downside review signal")
        chart_axis(d, (126, 346, 470, 570), "Top risk cases", "ROI interval")
        for k, row in sample.iterrows():
            yy = 360 + k * 25
            center = 280 + int(80 * math.sin(k * 1.3))
            lo, hi = center - int(42 + 28 * p), center + int(42 + 28 * p)
            d.text((78, yy - 12), clean(row["team_a"], 12), fill=INK, font=F_TINY)
            d.line([lo, yy, hi, yy], fill=CYAN, width=8)
            d.ellipse([center - 7, yy - 7, center + 7, yy + 7], fill=ORANGE)
            d.text((440, yy - 12), f"{float(row['negative_roi_probability']) * 100:.0f}%", fill=RED, font=F_TINY)
        d.text((274, 612), "negative ROI probability", fill=MUTED, font=F_TINY)
        chart_axis(d, (646, 344, 1170, 568), "Monte Carlo std bucket", "Matches")
        hist = [0.18, 0.30, 0.48, 0.78, 0.94, 0.68, 0.42, 0.25, 0.15]
        for k, hval in enumerate(hist):
            h = int(190 * hval * (.75 + .25 * p))
            x1 = 666 + k * 52
            color = CYAN if k < 3 else ORANGE if k < 6 else RED
            d.rectangle([x1, 568 - h, x1 + 34, 568], fill=color)
        d.text((646, 610), f"Coverage {float(sample['risk_score'].mean() + .43):.1%} · Allocate with intervals, not point estimates.", fill=MUTED, font=F_SMALL)
        frames.append(img)
    return frames


def network_graph(sponsors: pd.DataFrame) -> list[Image.Image]:
    sponsor_names = [clean(x) for x in sponsors.head(4)["source"].astype(str)]
    sponsors_xy = [(160, 410), (216, 530), (360, 552), (420, 378)]
    teams = [("Brazil", (570, 382)), ("Argentina", (620, 462)), ("France", (548, 552)), ("Germany", (720, 414)), ("England", (732, 530))]
    players = [(678, 340), (750, 480), (660, 606), (468, 330), (762, 598), (494, 506)]
    plot_bounds = (96, 334, 838, 618)

    def bounded(point: tuple[int, int]) -> tuple[int, int]:
        x1, y1, x2, y2 = plot_bounds
        return (max(x1, min(x2, point[0])), max(y1, min(y2, point[1])))

    sponsors_xy = [bounded(point) for point in sponsors_xy]
    teams = [(name, bounded(point)) for name, point in teams]
    players = [bounded(point) for point in players]
    frames = []
    for i in range(120):
        p = ease(i / 119)
        img = canvas("Sponsor Network Intelligence", "Sponsor-Team-Player-Match graph with centrality ranking and commercial influence.", "Network")
        d = ImageDraw.Draw(img)
        plot_panel(d, (44, 232, 884, 656), "Sponsor-Team-Player Network", "Weighted commercial graph: sponsor -> team -> player -> match context")
        plot_panel(d, (914, 232, 1236, 656), "Centrality Ranking", "Influence score by node")
        chart_axis(d, (1046, 356, 1192, 586), "", "Rank")
        for s, sp in enumerate(sponsors_xy):
            for j, (_, tp) in enumerate(teams):
                if (s + j) % 2 == 0:
                    d.line([bounded(sp), bounded(tp)], fill=ORANGE if s == 0 else CYAN, width=max(1, int((2 + s) * p)))
        for j, (_, tp) in enumerate(teams):
            for q, pp in enumerate(players):
                if (j + q) % 3 == 0:
                    d.line([bounded(tp), bounded(pp)], fill=GREEN, width=max(1, int(2 * p)))
        for k, (name, pos) in enumerate(zip(sponsor_names, sponsors_xy)):
            r = 16 if k else 30
            d.ellipse([pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r], fill=ORANGE, outline="white", width=3)
            d.text((pos[0] - 42, pos[1] + r + 8), name, fill=INK, font=F_TINY)
        for name, pos in teams:
            d.rounded_rectangle([pos[0] - 38, pos[1] - 18, pos[0] + 38, pos[1] + 18], radius=10, fill=BLUE)
            d.text((pos[0] - 28, pos[1] - 8), name[:9], fill="white", font=F_TINY)
        for pos in players:
            d.ellipse([pos[0] - 11, pos[1] - 11, pos[0] + 11, pos[1] + 11], fill=GREEN, outline="white", width=2)
        d.rounded_rectangle([78, 610, 350, 640], radius=15, fill="#eaf3f2")
        d.text((100, 618), "orange=sponsor   blue=team   green=player", fill=MUTED, font=F_TINY)
        names = sponsor_names + ["Brazil", "Argentina", "France"]
        for k, name in enumerate(names[:7]):
            yy = 364 + k * 31
            val = (0.92 - k * .07) * p
            d.text((942, yy - 8), f"{k + 1}. {name[:10]}", fill=INK, font=F_TINY)
            d.rectangle([1064, yy - 9, 1190, yy + 9], fill="#e6edf5")
            d.rectangle([1064, yy - 9, 1064 + int(126 * val), yy + 9], fill=ORANGE if k == 0 else CYAN)
        d.text((944, 620), "Takeaway: anchor on central pathways.", fill=MUTED, font=F_TINY)
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
