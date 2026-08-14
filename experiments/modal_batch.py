"""Run the Epistemic Fingerprints pilot on one open-weight model with Modal.

Usage:
    pip install -r requirements-modal.txt
    modal setup
    modal run experiments/modal_batch.py --output data/modal-qwen3-8b.json

Override EPISTEMIC_MODEL or EPISTEMIC_GPU before the command to change the
underlying model or accelerator. Keep both fixed within a reported experiment.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import modal


MODEL_NAME = os.environ.get("EPISTEMIC_MODEL", "Qwen/Qwen3-8B")
GPU_TYPE = os.environ.get("EPISTEMIC_GPU", "L4")
REPLICATES = 2

app = modal.App("epistemic-fingerprints-open-model")
image = (
    modal.Image.from_registry("nvidia/cuda:12.8.1-devel-ubuntu22.04", add_python="3.12")
    .entrypoint([])
    .uv_pip_install("vllm==0.13.0", "huggingface-hub==0.36.0")
)
cache = modal.Volume.from_name("epistemic-fingerprints-hf-cache", create_if_missing=True)


CONDITIONS = {
    "baseline": {
        "label": "Repeated instances",
        "agents": {
            "N-01": "Use careful scientific reasoning. Do not adopt a named role or persona.",
            "N-02": "Use careful scientific reasoning. Do not adopt a named role or persona.",
            "N-03": "Use careful scientific reasoning. Do not adopt a named role or persona.",
        },
    },
    "persona": {
        "label": "Prompted personas",
        "agents": {
            "P-falsifier": "Act as a rigorous falsifier. Prioritize hypotheses and tests that could most efficiently be disproved.",
            "P-mechanist": "Act as a mechanistic scientist. Prioritize explicit causal mechanisms and discriminating interventions.",
            "P-explorer": "Act as an anomaly-seeking scientist. Protect plausible minority hypotheses from premature convergence.",
        },
    },
    "history": {
        "label": "Different histories",
        "agents": {
            "H-simple": "Formative history: in three previous investigations, parsimonious single-mechanism explanations survived testing while elaborate explanations failed.",
            "H-rare": "Formative history: in three previous investigations, initially unlikely interaction effects survived testing while conventional explanations failed.",
            "H-instrument": "Formative history: in three previous investigations, apparent discoveries were ultimately traced to subtle measurement artifacts.",
        },
    },
}

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
        "hypotheses": {
            "V-A": "Two opaque orbiting bodies", "V-B": "Rotating stellar spots",
            "V-C": "An irregular dust cloud", "V-D": "A detector cadence artifact",
            "V-E": "Intrinsic stellar pulsation",
        },
        "tests": {
            "VT-1": "Measure dip-timing shifts over 30 cycles",
            "VT-2": "Repeat one dip with a second telescope",
            "VT-3": "Obtain a single infrared spectrum",
            "VT-4": "Increase brightness sampling between dips",
        },
    },
    "lumen": {
        "name": "The Lumen culture",
        "brief": "A microbial culture emits a blue flash under some combinations of nutrient, oxygen and temperature.",
        "observations": [
            "Nutrient K at 18 C in low oxygen produces a flash.",
            "Nutrient K at 30 C in low oxygen produces no flash.",
            "Nutrient K at 18 C in high oxygen produces no flash.",
            "Without nutrient K, no tested condition produces a flash.",
        ],
        "hypotheses": {
            "L-A": "K alone activates luminescence", "L-B": "Low oxygen alone activates luminescence",
            "L-C": "K, low oxygen and low temperature interact", "L-D": "Temperature is the sole trigger",
            "L-E": "The flashes are random contamination",
        },
        "tests": {
            "LT-1": "Vary temperature continuously with K and low oxygen fixed",
            "LT-2": "Repeat the 18 C low-oxygen condition", "LT-3": "Sequence the culture after one flash",
            "LT-4": "Double nutrient K at 30 C",
        },
    },
    "orison": {
        "name": "The Orison alloy",
        "brief": "An alloy abruptly becomes conductive after heating, but its return path does not mirror its heating path.",
        "observations": [
            "Conductivity jumps near 71 C during slow heating.",
            "During cooling, high conductivity persists until 54 C.",
            "The thresholds recur across five cycles.",
            "A thinner sample shows the same thresholds but switches faster.",
        ],
        "hypotheses": {
            "O-A": "A reversible linear temperature response", "O-B": "A first-order phase transition with hysteresis",
            "O-C": "Irreversible thermal damage", "O-D": "A contact-resistance artifact",
            "O-E": "Thickness-dependent quantum confinement",
        },
        "tests": {
            "OT-1": "Map partial heating/cooling loops between 50-75 C",
            "OT-2": "Repeat with a third sample thickness", "OT-3": "Hold the sample at 80 C for twice as long",
            "OT-4": "Replace the electrical contacts",
        },
    },
}


def build_prompt(condition: str, agent_id: str, mystery_id: str) -> str:
    condition_data = CONDITIONS[condition]
    mystery = MYSTERIES[mystery_id]
    observations = "\n".join(f"{index}. {value}" for index, value in enumerate(mystery["observations"], 1))
    hypotheses = "\n".join(f"{key}: {value}" for key, value in mystery["hypotheses"].items())
    tests = "\n".join(f"{key}: {value}" for key, value in mystery["tests"].items())
    return f"""EPISTEMIC FINGERPRINTS - PILOT TRIAL

Agent: {agent_id}
Condition: {condition_data['label']}
{condition_data['agents'][agent_id]}

Scientific mystery: {mystery['name']}
{mystery['brief']}

Observations:
{observations}

Candidate hypotheses:
{hypotheses}

Available next tests:
{tests}

Choose one primary hypothesis, up to two alternatives, and the single next test you would run. Return only valid JSON in this exact form:
{{
  "agent_id": "{agent_id}",
  "mystery_id": "{mystery_id}",
  "primary_hypothesis": "ID",
  "alternative_hypotheses": ["ID"],
  "confidence": 0,
  "selected_test": "ID",
  "rationale": "80 words maximum"
}}"""


def trial_specs() -> list[dict[str, Any]]:
    rows = []
    seed = 140826
    for condition, condition_data in CONDITIONS.items():
        for mystery_id in MYSTERIES:
            for agent_id in condition_data["agents"]:
                for replicate in range(1, REPLICATES + 1):
                    rows.append({
                        "condition": condition, "agent_id": agent_id,
                        "mystery_id": mystery_id, "replicate": replicate,
                        "seed": seed, "prompt": build_prompt(condition, agent_id, mystery_id),
                    })
                    seed += 1
    return rows


def parse_object(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found")
    return json.loads(match.group(0))


@app.cls(
    image=image,
    gpu=GPU_TYPE,
    timeout=30 * 60,
    volumes={"/root/.cache/huggingface": cache},
)
class OpenModelPilot:
    @modal.enter()
    def load(self):
        from vllm import LLM

        self.llm = LLM(model=MODEL_NAME, max_model_len=4096)

    @modal.method()
    def run(self, specs: list[dict[str, Any]]) -> dict[str, Any]:
        from vllm import SamplingParams

        trials, failures = [], []
        for spec in specs:
            params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=280, seed=spec["seed"])
            response = self.llm.chat(
                [{"role": "user", "content": spec["prompt"]}],
                sampling_params=params,
                chat_template_kwargs={"enable_thinking": False},
            )[0].outputs[0].text
            try:
                parsed = parse_object(response)
                mystery = MYSTERIES[spec["mystery_id"]]
                if parsed["primary_hypothesis"] not in mystery["hypotheses"]:
                    raise ValueError("Invalid primary hypothesis")
                if parsed["selected_test"] not in mystery["tests"]:
                    raise ValueError("Invalid selected test")
                trials.append({
                    "id": f"modal-{spec['condition']}-{spec['mystery_id']}-{spec['agent_id']}-{spec['replicate']}",
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                    "condition": spec["condition"], "agentId": spec["agent_id"],
                    "mysteryId": spec["mystery_id"], "replicate": spec["replicate"],
                    "primaryHypothesis": parsed["primary_hypothesis"],
                    "alternativeHypotheses": parsed.get("alternative_hypotheses", [])[:2],
                    "confidence": max(0, min(100, int(parsed["confidence"]))),
                    "selectedTest": parsed["selected_test"],
                    "rationale": parsed.get("rationale", "")[:800],
                    "modelLabel": MODEL_NAME, "seed": spec["seed"], "rawOutput": response,
                })
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                failures.append({**spec, "prompt": "[stored in source]", "rawOutput": response, "error": str(error)})
        return {
            "exportedAt": datetime.now(timezone.utc).isoformat(),
            "provenance": {
                "runner": "Modal + vLLM", "model": MODEL_NAME, "gpu": GPU_TYPE,
                "temperature": 0.7, "top_p": 0.95, "seeded": True,
            },
            "trials": trials, "failures": failures,
        }


@app.local_entrypoint()
def main(output: str = "data/modal-open-model-trials.json"):
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    result = OpenModelPilot().run.remote(trial_specs())
    destination.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {len(result['trials'])} valid trials and {len(result['failures'])} failures to {destination}")

