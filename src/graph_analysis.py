from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

try:
    import networkx as nx
except Exception:  # pragma: no cover - optional dependency fallback
    nx = None


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def infer_node_type(node: object) -> str:
    text = str(node)
    if text.startswith("sponsor:"):
        return "sponsor"
    if text.startswith("team:"):
        return "team"
    if text.startswith("match_"):
        return "match"
    if "team_attack_unit" in text or "team_midfield_unit" in text or "team_defense_unit" in text:
        return "player"
    return text.split(":", 1)[0] if ":" in text else text.split("_", 1)[0]


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
                "node_type": infer_node_type(node),
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
            "node_type": infer_node_type(node),
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


def gnn_baseline(edges: pd.DataFrame, central: pd.DataFrame) -> pd.DataFrame:
    """Lightweight GCN/GraphSAGE-style propagation baseline.

    The project needs to run in offline demo mode, so this intentionally avoids
    heavyweight graph neural network dependencies. It still preserves the core
    graph-modeling idea: initialize node features from centrality and propagate
    weighted neighbor information for two hops.
    """
    nodes = sorted(set(edges["source"]).union(set(edges["target"])))
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    n = len(nodes)
    adjacency = np.zeros((n, n), dtype=float)
    for _, edge in edges.iterrows():
        i = node_to_idx[edge["source"]]
        j = node_to_idx[edge["target"]]
        weight = float(edge["weight"])
        adjacency[i, j] += weight
        adjacency[j, i] += weight
    row_sum = adjacency.sum(axis=1, keepdims=True)
    norm_adj = np.divide(adjacency, row_sum, out=np.zeros_like(adjacency), where=row_sum != 0)

    central_idx = central.set_index("node")
    features = np.zeros((n, 4), dtype=float)
    for node, idx in node_to_idx.items():
        if node in central_idx.index:
            row = central_idx.loc[node]
            features[idx] = [
                float(row.get("weighted_degree", 0.0)),
                float(row.get("pagerank", 0.0)),
                float(row.get("betweenness", 0.0)),
                float(row.get("closeness", 0.0)),
            ]
    scale = features.max(axis=0)
    features = np.divide(features, scale, out=np.zeros_like(features), where=scale != 0)
    graphsage_embedding = 0.55 * features + 0.30 * (norm_adj @ features) + 0.15 * (norm_adj @ norm_adj @ features)
    gcn_embedding = norm_adj @ (0.65 * features + 0.35 * (norm_adj @ features))
    graphsage_score = graphsage_embedding @ np.array([0.46, 0.28, 0.16, 0.10])
    gcn_score = gcn_embedding @ np.array([0.40, 0.34, 0.16, 0.10])
    combined = 0.55 * graphsage_score + 0.45 * gcn_score
    rows = []
    for node, idx in node_to_idx.items():
        node_type = infer_node_type(node)
        rows.append(
            {
                "node": node,
                "node_type": node_type,
                "gcn_score": round(float(gcn_score[idx]), 6),
                "graphsage_score": round(float(graphsage_score[idx]), 6),
                "combined_graph_score": round(float(combined[idx]), 6),
                "embedding_degree": round(float(graphsage_embedding[idx, 0]), 6),
                "embedding_pagerank": round(float(graphsage_embedding[idx, 1]), 6),
                "embedding_betweenness": round(float(graphsage_embedding[idx, 2]), 6),
                "embedding_closeness": round(float(graphsage_embedding[idx, 3]), 6),
            }
        )
    return pd.DataFrame(rows).sort_values("combined_graph_score", ascending=False)


def write_gnn_bridge_report(
    gnn_scores: pd.DataFrame,
    sponsor_influence: pd.DataFrame,
    player_influence: pd.DataFrame,
) -> None:
    shap_path = REPORT_DIR / "roi_feature_group_importance.csv"
    shap = pd.read_csv(shap_path) if shap_path.exists() else pd.DataFrame()
    sponsor_gnn = gnn_scores[gnn_scores["node_type"].eq("sponsor")].head(10)
    player_gnn = gnn_scores[gnn_scores["node_type"].eq("player")].head(10)
    lines = [
        "# GNN Baseline and SHAP Bridge",
        "",
        "## Purpose",
        "",
        "This baseline upgrades graph intelligence from centrality-only reporting to a reproducible graph-modeling layer. It is intentionally lightweight so `--demo` and CI can run without external APIs or PyTorch Geometric.",
        "",
        "## Baseline Design",
        "",
        "- Node features: weighted degree, PageRank, betweenness, and closeness.",
        "- GCN-style score: normalized weighted adjacency propagation over centrality features.",
        "- GraphSAGE-style score: self features plus first-hop and second-hop weighted neighbor aggregation.",
        "- Output label proxy: `combined_graph_score`, used as a sponsor/player influence prior rather than a supervised production GNN.",
        "",
        "## Top GCN / GraphSAGE Sponsor Nodes",
        "",
        markdown_table(sponsor_gnn),
        "",
        "## Top GCN / GraphSAGE Player Nodes",
        "",
        markdown_table(player_gnn),
        "",
        "## NetworkX Sponsor Influence",
        "",
        markdown_table(sponsor_influence.head(10)),
        "",
        "## NetworkX Player Influence",
        "",
        markdown_table(player_influence.head(10)),
        "",
        "## Bridge to SHAP-Style ROI Drivers",
        "",
        markdown_table(shap.head(12)) if not shap.empty else "Run `src/explainability.py` to generate ROI feature group importance.",
        "",
        "## Interpretation",
        "",
        "- SHAP-style ROI drivers explain tabular commercial lift; graph scores explain relationship position and indirect influence.",
        "- A sponsor with high SHAP-linked brand fit but low graph influence may need partnership expansion.",
        "- A sponsor with high graph influence but weaker ROI drivers may be overexposed without enough conversion quality.",
        "- Production GCN/GraphSAGE should replace this deterministic baseline only after licensed sponsor conversion labels are available.",
    ]
    (REPORT_DIR / "gnn_explainability_bridge.md").write_text("\n".join(lines), encoding="utf-8")


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
    gnn_scores = gnn_baseline(edges, node_centrality)
    edges.to_csv(DATA_DIR / "team_player_sponsor_match_edges.csv", index=False)
    node_centrality.to_csv(REPORT_DIR / "graph_node_centrality.csv", index=False)
    sponsor_influence.to_csv(REPORT_DIR / "sponsor_influence_scores.csv", index=False)
    player_influence.to_csv(REPORT_DIR / "player_commercial_influence.csv", index=False)
    gnn_scores.to_csv(REPORT_DIR / "gnn_baseline_node_scores.csv", index=False)
    write_gnn_bridge_report(gnn_scores, sponsor_influence, player_influence)
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
        "- GCN / GraphSAGE baseline: deterministic two-hop weighted propagation over centrality features, producing `reports/gnn_baseline_node_scores.csv`.",
        "- SHAP bridge: `reports/gnn_explainability_bridge.md` connects graph influence to tabular ROI driver explanations.",
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
        "",
        "## Top GCN / GraphSAGE Baseline Nodes",
        "",
        markdown_table(gnn_scores.head(10)),
    ]
    (REPORT_DIR / "graph_analysis_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"edges": len(edges), "nodes": len(node_centrality)})


if __name__ == "__main__":
    main()
