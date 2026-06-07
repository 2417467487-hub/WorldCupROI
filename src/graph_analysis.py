from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    import networkx as nx
except Exception:  # pragma: no cover - optional dependency fallback
    nx = None


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
    if nx is None:
        return fallback_centrality(edges)

    graph = nx.Graph()
    for _, edge in edges.iterrows():
        graph.add_edge(edge["source"], edge["target"], weight=float(edge["weight"]), edge_type=edge["edge_type"])
    degree = dict(graph.degree())
    weighted_degree = dict(graph.degree(weight="weight"))
    pagerank = nx.pagerank(graph, weight="weight")
    betweenness = nx.betweenness_centrality(graph, weight="weight", normalized=True)
    closeness = nx.closeness_centrality(graph)
    rows = []
    for node in sorted(graph.nodes):
        rows.append(
            {
                "node": node,
                "node_type": str(node).split(":", 1)[0] if ":" in str(node) else str(node).split("_", 1)[0],
                "degree": degree.get(node, 0),
                "weighted_degree": round(weighted_degree.get(node, 0.0), 4),
                "pagerank": round(pagerank.get(node, 0.0), 6),
                "betweenness": round(betweenness.get(node, 0.0), 6),
                "closeness": round(closeness.get(node, 0.0), 6),
            }
        )
    return pd.DataFrame(rows).sort_values(["pagerank", "weighted_degree"], ascending=False)


def fallback_centrality(edges: pd.DataFrame) -> pd.DataFrame:
    degree: dict[str, float] = {}
    weighted_degree: dict[str, float] = {}
    for _, edge in edges.iterrows():
        src, tgt, weight = edge["source"], edge["target"], float(edge["weight"])
        degree[src] = degree.get(src, 0) + 1
        degree[tgt] = degree.get(tgt, 0) + 1
        weighted_degree[src] = weighted_degree.get(src, 0) + weight
        weighted_degree[tgt] = weighted_degree.get(tgt, 0) + weight
    rows = [
        {
            "node": node,
            "node_type": str(node).split(":", 1)[0] if ":" in str(node) else str(node).split("_", 1)[0],
            "degree": degree[node],
            "weighted_degree": round(weighted_degree[node], 4),
            "pagerank": 0.0,
            "betweenness": 0.0,
            "closeness": 0.0,
        }
        for node in sorted(degree)
    ]
    return pd.DataFrame(rows).sort_values("weighted_degree", ascending=False)


def influence_tables(edges: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    central = centrality(edges)
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
    sponsor = sponsor.merge(
        central[["node", "pagerank", "betweenness", "closeness"]].rename(columns={"node": "source"}),
        on="source",
        how="left",
    ).sort_values(["sponsor_influence", "pagerank"], ascending=False)
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
    if not player.empty:
        player = player.merge(
            central[["node", "pagerank", "betweenness", "closeness"]].rename(columns={"node": "source"}),
            on="source",
            how="left",
        ).sort_values(["player_commercial_influence", "pagerank"], ascending=False)
    return sponsor.round(6), player.round(6)


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
        "Team-player-sponsor-match relationships are represented as a weighted graph.",
        "",
        "## Graph Intelligence Upgrade",
        "",
        "- NetworkX centrality is used for degree, weighted degree, PageRank, betweenness, and closeness.",
        "- Sponsor Influence combines sponsor-team, sponsor-match exposure, and centrality signals.",
        "- Player Influence uses player-team edges and is ready to be joined with player availability or injury feeds.",
        "- GCN / GraphSAGE baseline placeholder: use this edge list as a heterogeneous graph where node features come from team profile, player profile, sponsor attributes, and match context. Candidate labels are sponsor conversion proxy, ROI lift, or high-risk scenario flag.",
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
