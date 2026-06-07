from __future__ import annotations

import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
HASH_FEATURES = 768
N_COMPONENTS = 24


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z']{2,}", str(text).lower())
    stop = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "from",
        "are",
        "was",
        "were",
        "will",
        "world",
        "cup",
        "fifa",
    }
    return [token for token in tokens if token not in stop]


def stable_hash(token: str) -> int:
    return int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % HASH_FEATURES


def hashed_tfidf(docs: pd.Series) -> np.ndarray:
    matrix = np.zeros((len(docs), HASH_FEATURES), dtype=np.float32)
    doc_freq = np.zeros(HASH_FEATURES, dtype=np.float32)
    for row_idx, doc in enumerate(docs):
        seen = set()
        for token in tokenize(doc):
            col = stable_hash(token)
            matrix[row_idx, col] += 1.0
            seen.add(col)
        for col in seen:
            doc_freq[col] += 1.0
    idf = np.log((1 + len(docs)) / (1 + doc_freq)) + 1
    matrix *= idf
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return matrix / norms


def reduce_with_covariance(matrix: np.ndarray, n_components: int) -> tuple[np.ndarray, np.ndarray]:
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    covariance = centered.T @ centered / max(1, len(matrix) - 1)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1][:n_components]
    components = eigenvectors[:, order]
    reduced = centered @ components
    mins = reduced.min(axis=0, keepdims=True)
    spans = reduced.max(axis=0, keepdims=True) - mins
    spans[spans == 0] = 1
    return (reduced - mins) / spans, eigenvalues[order]


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    text_path = DATA_DIR / "real_text_articles.csv"
    text = pd.read_csv(text_path)
    docs = text["title"].fillna("").astype(str)

    matrix = hashed_tfidf(docs)
    n_components = min(N_COMPONENTS, HASH_FEATURES, len(text) - 1)
    reduced, eigenvalues = reduce_with_covariance(matrix, n_components)

    out = text[["text_id", "source", "domain", "narrative_topic", "sentiment_score"]].copy()
    for idx in range(n_components):
        out[f"text_svd_{idx + 1:02d}"] = reduced[:, idx].round(6)
    out["text_x"] = out["text_svd_01"]
    out["text_y"] = out["text_svd_02"]
    out.to_csv(DATA_DIR / "text_embeddings_reduced.csv", index=False)

    source_summary = text.groupby("source", as_index=False).size().sort_values("size", ascending=False)
    source_summary.to_csv(REPORT_DIR / "text_source_summary.csv", index=False)
    variance_proxy = eigenvalues / max(eigenvalues.sum(), 1e-9)
    (REPORT_DIR / "text_dimensionality_summary.md").write_text(
        "# Text Dimensionality Reduction Summary\n\n"
        f"- Input text units: {len(text)}\n"
        f"- Hashed TF-IDF features: {HASH_FEATURES}\n"
        f"- Reduced dimensions: {n_components}\n"
        f"- Top-24 variance proxy sum: {variance_proxy.sum():.4f}\n"
        "- Method: dependency-light hashed TF-IDF + covariance eigendecomposition\n"
        "- Output: `data/text_embeddings_reduced.csv`\n",
        encoding="utf-8",
    )
    print({"text_units": len(text), "hashed_features": HASH_FEATURES, "reduced_dimensions": n_components})


if __name__ == "__main__":
    main()
