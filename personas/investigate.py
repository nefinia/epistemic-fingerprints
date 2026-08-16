"""Main-track experiment: free-text hypothesis generation on real cases,
testing false epistemic redundancy (see /Users/nefiniq/.claude/plans/peppy-gliding-wall.md).

Unlike personas.py (calibration track: closed 5-option menu, synthetic
mysteries with a known answer key), this script shows the model ONLY
pre-resolution evidence for a real case and asks it to generate its own
hypothesis - no candidate list, no answer key in the prompt. Scoring against
the case's hidden `target` happens later, in grade_tail_recovery.py (not yet
built), never at generation time.

Personas are Anya's original cognitive-mode framings from the first version
of personas.py (commit 475c8c2) - causal_mechanist, analogical_thinker,
teleological_tmk, dialectical_siev - reused verbatim. They were dropped in
personas.py's rewrite only because that rewrite needed IDs constrained to a
fixed menu for answer-key grading; that constraint doesn't apply here, and
her personas (each with a distinct reasoning architecture, not just a role
label) are a better fit for open generation than the simpler persona set
used in the calibration track.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import List

import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from cases import CASES
from personas import get_modal_url, wait_for_server

# Anya's original cognitive-mode personas (personas/personas.py @ 475c8c2),
# reused verbatim. "baseline" doubles as the repeated-instances condition.
BASELINE_PROMPT = "You are a helpful scientific assistant. Analyze the given case and provide a logical explanation."

PERSONAS = {
    "causal_mechanist": "You are a Causal Mechanist. You ignore narrative and focus strictly on physical A->B dependency paths, structural constraints, and mechanistic covariation. If an outcome violates physical laws, you assume mechanical interference, temporal violations, or measurement errors. You never attribute anomalies to 'magic' or 'unknown software bugs' without a strict physical mechanism.",
    "analogical_thinker": "You are an Analogical Thinker. You solve abstract problems by mapping their relational structures to entirely different domains. When presented with a mystery, do not take the nouns literally. Map the structural relations to a different phenomenon (e.g., biology, orbital mechanics, economics) to find the solution.",
    "teleological_tmk": "You are a Teleological Analyst operating strictly under the Task-Method-Knowledge (TMK) cognitive architecture.\nDo not rely on mechanistic causes. Evaluate this case by explicitly decomposing it into:\n1. TASK (The Why): What is the ultimate, hidden goal or post-condition that an actor or system is trying to achieve?\n2. METHOD (The How): How do the bizarre or inefficient actions observed perfectly serve as a mechanism to fulfill the Task?\n3. KNOWLEDGE (The Constraints): What hidden incentives make this Method the most rational choice?\nAssume all anomalies are perfectly executed Methods designed to achieve an unstated Task.",
    "dialectical_siev": "You are a Dialectical Thinker using the SIEV framework. You aggressively search for contradictions. For every piece of evidence, you formulate its exact opposite. You do not accept consensus or pick one side of conflicting data. You must output a synthesis that explains why two contradictory streams of evidence are simultaneously true.",
}


class Investigation(BaseModel):
    primary_hypothesis: str = Field(..., description="Your single best explanation for the case, in your own words.")
    alternative_hypotheses: List[str] = Field(default_factory=list, max_length=3, description="Up to three other explanations you considered.")
    mechanism: str = Field(..., description="The specific causal mechanism you believe is responsible.")
    evidence_for: List[str] = Field(..., description="Which stated facts support your primary hypothesis.")
    evidence_against: List[str] = Field(default_factory=list, description="Any stated facts that are hard to reconcile with your primary hypothesis.")
    missing_information: List[str] = Field(default_factory=list, description="What additional information would most help distinguish between hypotheses.")
    confidence: int = Field(..., ge=0, le=100, description="Confidence in your primary hypothesis, 0-100.")
    next_test: str = Field(..., description="The single most informative next investigative step.")


def build_prompt(case_id: str, framing: str | None) -> str:
    case = CASES[case_id]
    header = f"{framing}\n\n" if framing else ""
    return (
        f"{header}You are investigating a real, documented incident. You are being shown only the "
        f"evidence that was available before the case was resolved - the explanation is not known to "
        f"you and is not implied by the framing of this prompt.\n\n"
        f"Evidence:\n{case['evidence']}\n\n"
        f"Generate your own hypothesis for what happened. Do not assume a predetermined list of "
        f"explanations exists - propose whatever you judge most likely, including anything unusual."
    )


async def run_investigation(
    base_url: str,
    model_name: str,
    case_ids: list[str],
    n_per_condition: int = 10,
    temperature: float = 1.0,
    output_path: str | Path | None = None,
) -> list[dict]:
    """Generate `n_per_condition` samples for baseline and persona conditions,
    per case. Persona samples cycle round-robin through PERSONAS so a small n
    still covers all four cognitive modes."""
    wait_for_server(base_url)
    client = instructor.from_openai(AsyncOpenAI(api_key="not-needed", base_url=base_url), mode=instructor.Mode.JSON)

    async def call(prompt: str):
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                return await client.chat.completions.create(
                    model=model_name,
                    response_model=Investigation,
                    temperature=temperature,
                    max_retries=2,
                    messages=[{"role": "user", "content": prompt}],
                )
            except Exception as error:
                last_error = error
                if attempt < 2:
                    await asyncio.sleep(3 * (attempt + 1))
        raise last_error

    results: list[dict] = []
    persona_names = list(PERSONAS)
    total = len(case_ids) * n_per_condition * 2
    done = 0

    for case_id in case_ids:
        for replicate in range(1, n_per_condition + 1):
            done += 1
            print(f"{done}/{total}: {case_id} | baseline | rep {replicate}")
            response = await call(build_prompt(case_id, BASELINE_PROMPT))
            results.append({
                "caseId": case_id, "condition": "baseline", "agentId": "baseline", "replicate": replicate,
                **{k: getattr(response, k) for k in Investigation.model_fields},
            })

            persona_id = persona_names[(replicate - 1) % len(persona_names)]
            done += 1
            print(f"{done}/{total}: {case_id} | persona:{persona_id} | rep {replicate}")
            response = await call(build_prompt(case_id, PERSONAS[persona_id]))
            results.append({
                "caseId": case_id, "condition": "persona", "agentId": persona_id, "replicate": replicate,
                **{k: getattr(response, k) for k in Investigation.model_fields},
            })

    destination = Path(output_path) if output_path else Path(__file__).parent / "investigation_results.json"
    destination.write_text(json.dumps(results, indent=2))
    print(f"Saved {len(results)} generations to {destination}")
    return results


async def run_capability_controls(base_url: str, model_name: str, case_ids: list[str]) -> dict:
    """Single capability-control call per case: present the hidden target
    explicitly and ask for a plausibility rating. A case where this fails is
    not usable as evidence of a blind spot (see plan Section 6)."""
    wait_for_server(base_url)
    client = instructor.from_openai(AsyncOpenAI(api_key="not-needed", base_url=base_url), mode=instructor.Mode.JSON)

    class PlausibilityCheck(BaseModel):
        plausibility: int = Field(..., ge=1, le=5)
        reasoning: str

    out = {}
    for case_id in case_ids:
        prompt = CASES[case_id]["capability_control_prompt"]
        response = await client.chat.completions.create(
            model=model_name, response_model=PlausibilityCheck, temperature=0.3, max_retries=2,
            messages=[{"role": "user", "content": prompt}],
        )
        out[case_id] = {"plausibility": response.plausibility, "reasoning": response.reasoning}
        print(f"{case_id}: plausibility={response.plausibility}/5 - {response.reasoning[:150]}")
    return out


if __name__ == "__main__":
    url = get_modal_url()
    model = "Qwen/Qwen2.5-7B-Instruct"

    print("=== Capability controls ===")
    asyncio.run(run_capability_controls(url, model, list(CASES)))

    print("\n=== Smoke test (n=1 per condition per case) ===")
    asyncio.run(run_investigation(url, model, list(CASES), n_per_condition=1, output_path=Path(__file__).parent / "investigation_smoke_test.json"))
