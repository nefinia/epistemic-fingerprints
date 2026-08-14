"""Reproducible analysis for the Epistemic Fingerprints pilot.

The browser app exports ``{"trials": [...]}`` JSON. This module validates that
format, calculates the same descriptive metrics shown in Figure 1, and plots
the condition comparison. The fingerprint statistic is exploratory.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CONDITIONS = ["baseline", "persona", "history"]
CONDITION_LABELS = {
    "baseline": "Repeated instances",
    "persona": "Prompted personas",
    "history": "Different histories",
}
COLORS = {"baseline": "#6c7df2", "persona": "#f36f55", "history": "#9ac94f"}
ANSWER_KEY = {"vesper": "V-A", "lumen": "L-C", "orison": "O-B"}
TEST_INFORMATION = {
    "VT-1": 1.0, "VT-2": 0.7, "VT-3": 0.45, "VT-4": 0.25,
    "LT-1": 1.0, "LT-2": 0.35, "LT-3": 0.4, "LT-4": 0.65,
    "OT-1": 1.0, "OT-2": 0.45, "OT-3": 0.3, "OT-4": 0.55,
}
REQUIRED_COLUMNS = {
    "condition", "agentId", "mysteryId", "replicate", "primaryHypothesis",
    "alternativeHypotheses", "confidence", "selectedTest",
}


def load_trials(path: str | Path) -> pd.DataFrame:
    """Load and validate a JSON export from the web lab."""
    with Path(path).open(encoding="utf-8") as handle:
        payload: Any = json.load(handle)
    records = payload if isinstance(payload, list) else payload.get("trials", [])
    if not isinstance(records, list):
        raise ValueError("Expected a JSON list or an object containing a 'trials' list.")
    frame = pd.DataFrame(records)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing))}")
    unknown = set(frame["condition"].dropna()).difference(CONDITIONS)
    if unknown:
        raise ValueError(f"Unknown conditions: {', '.join(sorted(unknown))}")
    frame = frame.copy()
    frame["confidence"] = pd.to_numeric(frame["confidence"], errors="raise").clip(0, 100)
    return frame


def _normalized_entropy(values: pd.Series) -> float:
    if len(values) < 2 or values.nunique() == 1:
        return 0.0
    probabilities = values.value_counts(normalize=True).to_numpy()
    entropy = float(-(probabilities * np.log(probabilities)).sum())
    return entropy / math.log(min(len(values), 5))


def _variance_ratio(frame: pd.DataFrame, feature: str) -> float:
    agent_means = frame.groupby("agentId")[feature].mean()
    between = float(agent_means.var(ddof=0))
    within = float(frame.groupby("agentId")[feature].agg(lambda x: x.var(ddof=0)).mean())
    denominator = between + within
    return 0.0 if denominator == 0 or np.isnan(denominator) else between / denominator


def summarize(trials: pd.DataFrame) -> pd.DataFrame:
    """Calculate the four descriptive Figure 1 metrics by condition."""
    rows: list[dict[str, float | int | str]] = []
    for condition in CONDITIONS:
        subset = trials.loc[trials["condition"] == condition].copy()
        if subset.empty:
            rows.append({"condition": condition, "trials": 0, "fingerprint": 0.0,
                         "diversity": 0.0, "accuracy": 0.0, "shared_error": 0.0})
            continue

        subset["correct"] = subset.apply(
            lambda row: float(row["primaryHypothesis"] == ANSWER_KEY.get(row["mysteryId"])), axis=1
        )
        subset["breadth"] = subset["alternativeHypotheses"].apply(
            lambda values: min(len(values) + 1, 3) / 3
        )
        subset["information"] = subset["selectedTest"].map(TEST_INFORMATION).fillna(0.0)
        subset["confidence_scaled"] = subset["confidence"] / 100

        diversity = np.mean([
            _normalized_entropy(group["primaryHypothesis"])
            for _, group in subset.groupby("mysteryId")
        ])
        error_concentrations = []
        for mystery_id in ANSWER_KEY:
            errors = subset.loc[
                (subset["mysteryId"] == mystery_id) & (subset["correct"] == 0),
                "primaryHypothesis",
            ]
            error_concentrations.append(0.0 if errors.empty else float(errors.value_counts().max() / len(errors)))

        feature_ratios = [
            _variance_ratio(subset, feature)
            for feature in ["confidence_scaled", "breadth", "information", "correct"]
        ]
        rows.append({
            "condition": condition,
            "trials": len(subset),
            "fingerprint": float(np.mean(feature_ratios)),
            "diversity": float(diversity),
            "accuracy": float(subset["correct"].mean()),
            "shared_error": float(np.mean(error_concentrations)),
        })
    return pd.DataFrame(rows).set_index("condition")


def make_demo_trials(seed: int = 14) -> pd.DataFrame:
    """Create an explicitly simulated 54-row dataset for testing the pipeline."""
    rng = np.random.default_rng(seed)
    agents = {
        "baseline": ["N-01", "N-02", "N-03"],
        "persona": ["P-falsifier", "P-mechanist", "P-explorer"],
        "history": ["H-simple", "H-rare", "H-instrument"],
    }
    hypotheses = {
        "vesper": ["V-A", "V-B", "V-C", "V-D", "V-E"],
        "lumen": ["L-A", "L-B", "L-C", "L-D", "L-E"],
        "orison": ["O-A", "O-B", "O-C", "O-D", "O-E"],
    }
    tests = {
        "vesper": ["VT-1", "VT-2", "VT-3", "VT-4"],
        "lumen": ["LT-1", "LT-2", "LT-3", "LT-4"],
        "orison": ["OT-1", "OT-2", "OT-3", "OT-4"],
    }
    records = []
    for condition in CONDITIONS:
        for mystery_id in ANSWER_KEY:
            for agent_index, agent_id in enumerate(agents[condition]):
                for replicate in [1, 2]:
                    probability_correct = {"baseline": 0.70, "persona": 0.66, "history": 0.58}[condition]
                    primary = ANSWER_KEY[mystery_id] if rng.random() < probability_correct else rng.choice(
                        [item for item in hypotheses[mystery_id] if item != ANSWER_KEY[mystery_id]]
                    )
                    alternatives = [item for item in hypotheses[mystery_id] if item != primary]
                    records.append({
                        "condition": condition,
                        "agentId": agent_id,
                        "mysteryId": mystery_id,
                        "replicate": replicate,
                        "primaryHypothesis": primary,
                        "alternativeHypotheses": alternatives[: int(rng.integers(0, 3))],
                        "confidence": int(np.clip(rng.normal(62 + agent_index * 7, 8), 0, 100)),
                        "selectedTest": tests[mystery_id][(agent_index + replicate) % 4],
                    })
    return pd.DataFrame(records)


def plot_figure_1(summary: pd.DataFrame, title: str = "Epistemic traces by condition"):
    """Plot the dashboard metrics and return the Matplotlib figure."""
    metrics = ["fingerprint", "diversity", "accuracy", "shared_error"]
    labels = ["Fingerprint\nstrength", "Hypothesis\ndiversity", "Accuracy", "Shared-error\nconcentration"]
    figure, axes = plt.subplots(1, 4, figsize=(14, 4), sharey=True)
    for axis, metric, label in zip(axes, metrics, labels):
        values = summary.reindex(CONDITIONS)[metric]
        axis.bar(range(len(CONDITIONS)), values, color=[COLORS[item] for item in CONDITIONS])
        axis.set_title(label, fontsize=10)
        axis.set_xticks(range(len(CONDITIONS)), [CONDITION_LABELS[item] for item in CONDITIONS], rotation=35, ha="right")
        axis.set_ylim(0, 1)
        axis.grid(axis="y", alpha=0.2)
    axes[0].set_ylabel("Descriptive score (0–1)")
    figure.suptitle(title, fontsize=15, x=0.07, ha="left")
    figure.tight_layout()
    return figure
