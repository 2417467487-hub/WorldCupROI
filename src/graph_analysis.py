from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def build_edges() -> pd.DataFrame:
    edges = []
    if (DATA_DIR / "relationship_network.csv").exists():
        base = pd.read_csv(DATA_DIR / "relationship_network.csv")
        for _, row in base.iterrows():
            edges.append(
                {
                    "source": row["source"],
                    "target": row["target"],
                    "edge_type": row["edge_type"],
                    "weight": float(row["weight"]),
                }
            )
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    for _, row in panel.head(2500).iterrows():
        match_node = f"match_{int(row['match_id'])}"
        team_node = f"team:{row['team']}"
        sponsor_node = f"sponsor:{row['sponsor']}"
        edges.extend(
            [
                {"source": team_node, "target": match_node, "edge_type": "team_match", "weight": float(row["fan_score_panel"])},
                {"source": sponsor_node, "target": team_node, "edge_type": "sponsor_team_panel", "weight": float(row["sponsor_power_index"])},
                {"source": sponsor_node, "target": match_node, "edge_type": "sponsor_match_exposure", "weight": float(row["predicted_roi"])},
            ]
        )
    return pd.DataFrame(edges)


def centrality(edges: pd.DataFrame) -> pd.DataFrame:
    degree = defaultdict(float)
    weighted_degree = defaultdict(float)
    for _, edge in edges.iterrows():
        src, tgt, weight = edge["source"], edge["target"], float(edge["weight"])
        degree[src] += 1
        degree[tgt] += 1
        weighted_degree[src] += weight
        weighted_degree[tgt] += weight
    rows = [
        {"node": node, "degree": degree[node], "weighted_degree": round(weighted_degree[node], 4)}
        for node in sorted(degree)
    ]
    return pd.DataFrame(rows).sort_values("weighted_degree", ascending=False)


def influence_tables(edges: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    sponsor = (
        edges[edges["source"].astype(str).str.startswith("sponsor")]
        .groupby("source", as_index=False)
        .agg(
            connected_nodes=("target", "nunique"),
            sponsor_influence=("weight", "sum"),
            avg_edge_weight=("weight", "mean"),
        )
        .sort_values("sponsor_influence", ascending=False)
        .round(4)
    )
    player = (
        edges[edges["edge_type"].eq("player_team")]
        .groupby("source", as_index=False)
        .agg(
            connected_teams=("target", "nunique"),
            player_commercial_influence=("weight", "sum"),
            avg_influence=("weight", "mean"),
        )
        .sort_values("player_commercial_influence", ascending=False)
        .round(4)
    )
    return sponsor, player


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    edges = build_edges()
    node_centrality = centrality(edges)
    sponsor_influence, player_influence = influence_tables(edges)
    edges.to_csv(DATA_DIR / "team_player_sponsor_match_edges.csv", index=False)
    node_centrality.to_csv(REPORT_DIR / "graph_node_centrality.csv", index=False)
    sponsor_influence.to_csv(REPORT_DIR / "sponsor_influence_scores.csv", index=False)
    player_influence.to_csv(REPORT_DIR / "player_commercial_influence.csv", index=False)
    lines = [
        "# Graph Analysis Report",
        "",
        "Team-player-sponsor-match relationships are represented as a weighted network.",
        "",
        "## Top Sponsor Influence",
        "",
        markdown_table(sponsor_influence.head(10)),
        "",
        "## Top Player Commercial Influence",
        "",
        markdown_table(player_influence.head(10)),
        "",
        "## Top Network Centrality",
        "",
        markdown_table(node_centrality.head(10)),
    ]
    (REPORT_DIR / "graph_analysis_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"edges": len(edges), "nodes": len(node_centrality)})


if __name__ == "__main__":
    main()
