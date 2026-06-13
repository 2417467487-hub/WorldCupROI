from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "docs" / "assets"


def load_edges() -> pd.DataFrame:
    path = DATA_DIR / "team_player_sponsor_match_edges.csv"
    if not path.exists():
        from graph_analysis import main as graph_main

        graph_main()
    return pd.read_csv(path)


def node_type(node: str) -> str:
    node = str(node)
    if node.startswith("sponsor"):
        return "sponsor"
    if node.startswith("team"):
        return "team"
    if node.startswith("match"):
        return "match"
    return "player_or_entity"


def link_prediction(edges: pd.DataFrame) -> pd.DataFrame:
    sponsor_neighbors: dict[str, set[str]] = defaultdict(set)
    team_neighbors: dict[str, set[str]] = defaultdict(set)
    for _, row in edges.iterrows():
        s, t = str(row["source"]), str(row["target"])
        if "sponsor" in s:
            sponsor_neighbors[s].add(t)
        if "team" in t:
            team_neighbors[t].add(s)
    rows = []
    sponsors = list(sponsor_neighbors)[:40]
    teams = [n for n in set(edges["target"].astype(str)) if "team" in n][:80]
    for sponsor in sponsors:
        existing = sponsor_neighbors[sponsor]
        for team in teams:
            if team in existing:
                continue
            overlap = len(existing.intersection(team_neighbors.get(team, set())))
            score = overlap + 0.01 * len(existing) + 0.02 * len(team_neighbors.get(team, set()))
            rows.append({"sponsor": sponsor, "candidate_team": team, "link_prediction_score": round(score, 4), "method": "common-neighbor HGT proxy"})
    return pd.DataFrame(rows).sort_values("link_prediction_score", ascending=False).head(50)


def influence_ranking(edges: pd.DataFrame) -> pd.DataFrame:
    score = defaultdict(float)
    type_count = defaultdict(int)
    for _, row in edges.iterrows():
        weight = float(row["weight"])
        score[str(row["source"])] += weight
        score[str(row["target"])] += weight * 0.55
        type_count[node_type(str(row["source"]))] += 1
    out = pd.DataFrame(
        [{"node": node, "node_type": node_type(node), "hgt_influence_proxy": round(val, 4)} for node, val in score.items()]
    ).sort_values("hgt_influence_proxy", ascending=False)
    return out


def svg_graph_learning(influence: pd.DataFrame) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    top = influence.head(8)
    max_v = max(float(top["hgt_influence_proxy"].max()), 1)
    rows = ['<svg width="1280" height="600" viewBox="0 0 1280 600" xmlns="http://www.w3.org/2000/svg">', '<rect width="1280" height="600" fill="#ffffff"/>']
    rows.append('<text x="64" y="72" font-family="Arial" font-size="34" font-weight="700" fill="#111827">Graph Learning Influence Ranking</text>')
    rows.append('<text x="64" y="106" font-family="Arial" font-size="17" fill="#4b5563">HGT proxy scores for sponsor-team-player-match nodes.</text>')
    y = 160
    for _, row in top.iterrows():
        width = 760 * float(row["hgt_influence_proxy"]) / max_v
        rows.append(f'<text x="76" y="{y+20}" font-family="Arial" font-size="16" fill="#111827">{row["node"]}</text>')
        rows.append(f'<rect x="430" y="{y}" width="780" height="28" rx="14" fill="#eef0f3"/>')
        rows.append(f'<rect x="430" y="{y}" width="{width:.1f}" height="28" rx="14" fill="#6A5ACD"/>')
        y += 46
    rows.append("</svg>")
    (ASSET_DIR / "graph_learning_influence.svg").write_text("\n".join(rows), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    edges = load_edges()
    links = link_prediction(edges)
    influence = influence_ranking(edges)
    links.to_csv(REPORT_DIR / "graph_link_prediction.csv", index=False)
    influence.to_csv(REPORT_DIR / "graph_learning_node_influence.csv", index=False)
    svg_graph_learning(influence)
    lines = [
        "# Graph Learning Report",
        "",
        "This module upgrades graph analysis into graph learning proxies: link prediction and heterogeneous influence ranking.",
        "",
        "## Top Link Predictions",
        "",
        markdown_table(links.head(10)),
        "",
        "## Node Influence Ranking",
        "",
        markdown_table(influence.head(10)),
        "",
        "## Upgrade Path",
        "",
        "- Heterogeneous Graph Transformer: learn type-specific attention over Sponsor, Team, Player and Match nodes.",
        "- Link prediction: forecast future sponsor-team effectiveness before contract allocation.",
        "- Temporal graph learning: use stage snapshots to model changing influence.",
    ]
    (REPORT_DIR / "graph_learning_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved graph learning outputs.")


if __name__ == "__main__":
    main()
