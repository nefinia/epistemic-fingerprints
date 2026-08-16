"""Automated trial collection for the Epistemic Fingerprints pilot.

Drives a self-hosted model (via Modal + vLLM, see serve_model.py) through the
same 3 conditions x 3 mysteries x 3 agents x 2 replicates design used by the
web lab (app/experiment.ts), and writes a JSON file with the exact schema
analysis/pipeline.py expects: condition, agentId, mysteryId, replicate,
primaryHypothesis, alternativeHypotheses, confidence, selectedTest, rationale.
"""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import List, Literal

import httpx
import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, create_model

# 1. Conditions and agents (mirrors app/experiment.ts `conditions`)
CONDITIONS = {
    "baseline": {
        "agents": ["N-01", "N-02", "N-03"],
        "prompt": "Use careful scientific reasoning. Do not adopt a named role or persona.",
    },
    "persona": {
        "agents": ["P-falsifier", "P-mechanist", "P-explorer"],
        "prompt_by_agent": {
            "P-falsifier": "Act as a rigorous falsifier. Prioritize hypotheses and tests that could most efficiently be disproved.",
            "P-mechanist": "Act as a mechanistic scientist. Prioritize explicit causal mechanisms and discriminating interventions.",
            "P-explorer": "Act as an anomaly-seeking scientist. Protect plausible minority hypotheses from premature convergence.",
        },
    },
    "history": {
        "agents": ["H-simple", "H-rare", "H-instrument"],
        "prompt_by_agent": {
            "H-simple": "Formative history: in three previous investigations, parsimonious single-mechanism explanations survived testing while elaborate explanations failed.",
            "H-rare": "Formative history: in three previous investigations, initially unlikely interaction effects survived testing while conventional explanations failed.",
            "H-instrument": "Formative history: in three previous investigations, apparent discoveries were ultimately traced to subtle measurement artifacts.",
        },
    },
}

# 2. The three synthetic mysteries (mirrors app/experiment.ts `mysteries` exactly,
#    so real trials can be graded with the same ANSWER_KEY / TEST_INFORMATION
#    used in analysis/pipeline.py).
MYSTERIES = {
    "vesper": {
        "name": "The Vesper dips",
        "brief": "A newly catalogued star shows two alternating, sharply bounded dips in brightness every 11.2 hours.",
        "observations": [
            "Successive dips alternate between 8% and 3% depth.",
            "The dip depths are nearly identical in blue and infrared bands.",
            "Outside the dips, brightness remains stable to within 0.1%.",
            "A comparison star observed by the same detector remains constant.",
        ],
        "hypotheses": [
            {"id": "V-A", "label": "Two opaque orbiting bodies"},
            {"id": "V-B", "label": "Rotating stellar spots"},
            {"id": "V-C", "label": "An irregular dust cloud"},
            {"id": "V-D", "label": "A detector cadence artifact"},
            {"id": "V-E", "label": "Intrinsic stellar pulsation"},
        ],
        "tests": [
            {"id": "VT-1", "label": "Measure dip-timing shifts over 30 cycles"},
            {"id": "VT-2", "label": "Repeat one dip with a second telescope"},
            {"id": "VT-3", "label": "Obtain a single infrared spectrum"},
            {"id": "VT-4", "label": "Increase brightness sampling between dips"},
        ],
    },
    "lumen": {
        "name": "The Lumen culture",
        "brief": "A microbial culture emits a blue flash under some combinations of nutrient, oxygen and temperature.",
        "observations": [
            "Nutrient K at 18C in low oxygen produces a flash.",
            "Nutrient K at 30C in low oxygen produces no flash.",
            "Nutrient K at 18C in high oxygen produces no flash.",
            "Without nutrient K, no tested condition produces a flash.",
        ],
        "hypotheses": [
            {"id": "L-A", "label": "K alone activates luminescence"},
            {"id": "L-B", "label": "Low oxygen alone activates luminescence"},
            {"id": "L-C", "label": "K, low oxygen and low temperature interact"},
            {"id": "L-D", "label": "Temperature is the sole trigger"},
            {"id": "L-E", "label": "The flashes are random contamination"},
        ],
        "tests": [
            {"id": "LT-1", "label": "Vary temperature continuously with K and low oxygen fixed"},
            {"id": "LT-2", "label": "Repeat the 18C low-oxygen condition"},
            {"id": "LT-3", "label": "Sequence the culture after one flash"},
            {"id": "LT-4", "label": "Double nutrient K at 30C"},
        ],
    },
    "orison": {
        "name": "The Orison alloy",
        "brief": "An alloy abruptly becomes conductive after heating, but its return path does not mirror its heating path.",
        "observations": [
            "Conductivity jumps near 71C during slow heating.",
            "During cooling, high conductivity persists until 54C.",
            "The thresholds recur across five cycles.",
            "A thinner sample shows the same thresholds but switches faster.",
        ],
        "hypotheses": [
            {"id": "O-A", "label": "A reversible linear temperature response"},
            {"id": "O-B", "label": "A first-order phase transition with hysteresis"},
            {"id": "O-C", "label": "Irreversible thermal damage"},
            {"id": "O-D", "label": "A contact-resistance artifact"},
            {"id": "O-E", "label": "Thickness-dependent quantum confinement"},
        ],
        "tests": [
            {"id": "OT-1", "label": "Map partial heating/cooling loops between 50-75C"},
            {"id": "OT-2", "label": "Repeat with a third sample thickness"},
            {"id": "OT-3", "label": "Hold the sample at 80C for twice as long"},
            {"id": "OT-4", "label": "Replace the electrical contacts"},
        ],
    },
}


def build_prompt(condition_id: str, agent_id: str, mystery_id: str) -> str:
    condition = CONDITIONS[condition_id]
    condition_prompt = (
        condition["prompt"] if "prompt" in condition else condition["prompt_by_agent"][agent_id]
    )
    mystery = MYSTERIES[mystery_id]
    observations = "\n".join(f"{i + 1}. {o}" for i, o in enumerate(mystery["observations"]))
    hypotheses = "\n".join(f"{h['id']}: {h['label']}" for h in mystery["hypotheses"])
    tests = "\n".join(f"{t['id']}: {t['label']}" for t in mystery["tests"])
    return (
        f"EPISTEMIC FINGERPRINTS - PILOT TRIAL\n\n"
        f"Agent: {agent_id}\nCondition: {condition_id}\n{condition_prompt}\n\n"
        f"Scientific mystery: {mystery['name']}\n{mystery['brief']}\n\n"
        f"Observations:\n{observations}\n\n"
        f"Candidate hypotheses:\n{hypotheses}\n\n"
        f"Available next tests:\n{tests}\n\n"
        f"Choose one primary hypothesis, up to two alternatives, and the single next test you would run."
    )


def build_response_model(mystery_id: str) -> type[BaseModel]:
    """Dynamic Pydantic model constraining IDs to this mystery's valid set,
    so instructor validates/retries instead of pipeline.py silently getting
    an unscoreable row."""
    mystery = MYSTERIES[mystery_id]
    hypothesis_ids = tuple(h["id"] for h in mystery["hypotheses"])
    test_ids = tuple(t["id"] for t in mystery["tests"])
    return create_model(
        "ScientificHypothesis",
        primary_hypothesis=(Literal[hypothesis_ids], Field(..., description="ID of the primary hypothesis.")),
        alternative_hypotheses=(
            List[Literal[hypothesis_ids]],
            Field(default_factory=list, max_length=2, description="Up to two alternative hypothesis IDs."),
        ),
        confidence=(int, Field(..., ge=0, le=100, description="Confidence in the primary hypothesis, 0-100.")),
        selected_test=(Literal[test_ids], Field(..., description="ID of the single next test to run.")),
        rationale=(str, Field(..., description="Reasoning, 80 words maximum.")),
    )


def wait_for_server(base_url: str, timeout: int = 600, interval: int = 5) -> None:
    """Block until the vLLM server answers /models.

    Modal's Flash routing (used by @app.server) returns 503 "no upstreams
    available" immediately while a container is still cold-starting, instead
    of queueing the request - so callers must poll before sending traffic.
    """
    models_url = base_url.rstrip("/") + "/models"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            if httpx.get(models_url, timeout=10).status_code == 200:
                return
        except httpx.HTTPError:
            pass
        print(f"Waiting for model server at {base_url} ...")
        time.sleep(interval)
    raise RuntimeError(f"Server at {base_url} did not become ready within {timeout}s.")


async def run_full_54_trials(
    base_url: str,
    model_name: str = "Qwen/Qwen2.5-7B-Instruct",
    api_key: str = "not-needed",
    output_path: str | Path | None = None,
) -> list[dict]:
    """Run all 54 trials against an OpenAI-compatible endpoint (e.g. the
    Modal-hosted vLLM server from serve_model.py) and write results next to
    this file, in the schema analysis/pipeline.py expects.

    base_url must be the server's real URL with a trailing /v1, e.g. the
    value printed by get_modal_url() below.
    """
    wait_for_server(base_url)
    client = instructor.from_openai(
        AsyncOpenAI(api_key=api_key, base_url=base_url),
        mode=instructor.Mode.JSON,
    )

    results: list[dict] = []
    trial_counter = 0
    total = len(CONDITIONS) * len(MYSTERIES) * 3 * 2

    for condition_id, condition in CONDITIONS.items():
        for mystery_id in MYSTERIES:
            response_model = build_response_model(mystery_id)
            for agent_id in condition["agents"]:
                for replicate in (1, 2):
                    trial_counter += 1
                    print(f"Trial {trial_counter}/{total}: {condition_id} | {mystery_id} | {agent_id} | rep {replicate}")
                    try:
                        response = None
                        last_error: Exception | None = None
                        for attempt in range(3):
                            try:
                                response = await client.chat.completions.create(
                                    model=model_name,
                                    response_model=response_model,
                                    temperature=0.7,
                                    max_retries=2,
                                    messages=[
                                        {"role": "user", "content": build_prompt(condition_id, agent_id, mystery_id)},
                                    ],
                                )
                                break
                            except Exception as call_error:
                                last_error = call_error
                                if attempt < 2:
                                    await asyncio.sleep(3 * (attempt + 1))
                        if response is None:
                            raise last_error
                        results.append({
                            "condition": condition_id,
                            "agentId": agent_id,
                            "mysteryId": mystery_id,
                            "replicate": replicate,
                            "primaryHypothesis": response.primary_hypothesis,
                            "alternativeHypotheses": response.alternative_hypotheses,
                            "confidence": response.confidence,
                            "selectedTest": response.selected_test,
                            "rationale": response.rationale,
                        })
                    except Exception as error:
                        print(f"Failed trial {trial_counter}: {error}")

    destination = Path(output_path) if output_path else Path(__file__).parent / "epistemic_fingerprints_54_trials.json"
    destination.write_text(json.dumps(results, indent=2))
    print(f"Saved {len(results)}/{total} trials to {destination}")
    return results


def get_modal_url(app_name: str = "epistemic-vllm-server", server_name: str = "Server") -> str:
    """Look up the live URL of a deployed Modal server (`modal deploy
    serve_model.py` must have already run). Server URLs are assigned at
    deploy time and are not predictable from the app/class names."""
    import modal

    server = modal.Server.from_name(app_name, server_name)
    url = server.get_url()
    if not url:
        raise RuntimeError(f"Server '{app_name}/{server_name}' has no live URL. Is it deployed and running?")
    return url.rstrip("/") + "/v1"


if __name__ == "__main__":
    asyncio.run(
        run_full_54_trials(
            base_url=get_modal_url(),
            model_name="Qwen/Qwen2.5-7B-Instruct",
        )
    )
