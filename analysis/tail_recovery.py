"""Analysis for the main-track experiment (personas/investigate.py output).

Two separate things live here, deliberately kept apart:

1. Diversity metrics (this file, built now): how spread out are the
   generations within a condition. Needs only embeddings - no hidden target,
   no judge. Reuses the embedding/clustering pattern from
   personas/evaluate.py (all-MiniLM-L6-v2 + agglomerative clustering).

2. Tail-recovery grading and the C(N) rarefaction curve (NOT built yet):
   whether a generation hits each case's hidden `target` in personas/cases.py.
   Needs the LLM-judge + rubric + manual-review pass from the plan
   (Section 5) before it can be computed. Diversity alone was never meant to
   be the finding - the interesting failure mode is high diversity paired
   with flat target recovery, which this file's numbers feed into once
   grading exists.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

CLUSTER_DISTANCE_THRESHOLD = 0.4  # same threshold as personas/evaluate.py


def load_investigations(path: str | Path) -> pd.DataFrame:
    data = json.loads(Path(path).read_text())
    frame = pd.DataFrame(data)
    frame["claim_text"] = frame["primary_hypothesis"] + ". " + frame["mechanism"]
    return frame


def embed_claims(frame: pd.DataFrame, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    model = SentenceTransformer(model_name)
    return model.encode(frame["claim_text"].tolist())


def _mean_pairwise_distance(embeddings: np.ndarray) -> float:
    """DAT-style diversity score: mean pairwise cosine distance (1 - similarity),
    excluding self-pairs. 0 = identical claims, higher = more spread out."""
    if len(embeddings) < 2:
        return 0.0
    sim = cosine_similarity(embeddings)
    n = len(embeddings)
    off_diagonal = sim[~np.eye(n, dtype=bool)]
    return float(1 - off_diagonal.mean())


def _cluster_count(embeddings: np.ndarray) -> int:
    if len(embeddings) < 2:
        return len(embeddings)
    clustering = AgglomerativeClustering(
        n_clusters=None, distance_threshold=CLUSTER_DISTANCE_THRESHOLD, metric="cosine", linkage="average"
    )
    labels = clustering.fit_predict(embeddings)
    return int(len(set(labels)))


def diversity_summary(frame: pd.DataFrame, embeddings: np.ndarray) -> pd.DataFrame:
    """Diversity by case x condition, PLUS a 'persona_pooled' row per case
    combining all 4 persona agents together - directly answers "baseline
    variation vs. all personas combined"."""
    frame = frame.copy()
    frame["_row"] = np.arange(len(frame))
    rows = []

    for case_id, case_frame in frame.groupby("caseId"):
        for condition, sub in case_frame.groupby("condition"):
            idx = sub["_row"].to_numpy()
            rows.append({
                "caseId": case_id, "group": condition, "n": len(sub),
                "diversity": _mean_pairwise_distance(embeddings[idx]),
                "hypothesis_families": _cluster_count(embeddings[idx]),
            })
        # persona condition broken down per individual persona agent too
        persona_sub = case_frame[case_frame["condition"] == "persona"]
        for agent_id, agent_frame in persona_sub.groupby("agentId"):
            idx = agent_frame["_row"].to_numpy()
            rows.append({
                "caseId": case_id, "group": f"persona:{agent_id}", "n": len(agent_frame),
                "diversity": _mean_pairwise_distance(embeddings[idx]),
                "hypothesis_families": _cluster_count(embeddings[idx]),
            })

    return pd.DataFrame(rows).sort_values(["caseId", "group"]).reset_index(drop=True)


def run(input_path: str | Path) -> pd.DataFrame:
    frame = load_investigations(input_path)
    print(f"Loaded {len(frame)} generations from {input_path}")
    print("Embedding claims (primary_hypothesis + mechanism)...")
    embeddings = embed_claims(frame)
    summary = diversity_summary(frame, embeddings)
    print(summary.to_string(index=False))
    return summary


if __name__ == "__main__":
    import sys

    default_path = Path(__file__).resolve().parents[1] / "personas" / "investigation_smoke_test.json"
    path = sys.argv[1] if len(sys.argv) > 1 else default_path
    run(path)
