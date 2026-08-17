"""Track 5 diagnostic probes: is the persona effect genuine epistemic
differentiation, or cosmetic framing riding on a near-deterministic base
disposition?

The main 54-trial run (personas.py) showed near-zero variance across all
three conditions on several mysteries - e.g. `lumen` produced the identical
hypothesis, test, and confidence value in all 18 trials regardless of
condition. That result can't distinguish "personas don't work" from "nothing
could show variation here." This script runs four probes on a single
mystery, at higher replicate count and temperature than the main study, to
get enough resolution to actually see a tail if one exists:

1. baseline      - no persona (control)
2. persona       - the original "Act as X" framing from personas.py
3. content_only  - identical epistemic guidance, with the character framing
                   ("Act as a rigorous falsifier") stripped out. Isolates
                   whether the *character* adds anything beyond the
                   *instruction content*.
4. unmasked      - a same-conversation follow-up after the persona answer,
                   asking the model to set the persona aside and give its
                   view "independent of that framing." Tests whether the
                   persona masks a different underlying disposition
                   (Track 5's "persona vs less-constrained elicitation").

Run once per deployed model (instruct, then base) to compare - pass a
different `model_variant` label and point `base_url`/`model_name` at
whichever model is currently live on Modal (see serve_model.py).
"""

from __future__ import annotations

import asyncio
import json
from collections import Counter
from pathlib import Path

import instructor
from openai import AsyncOpenAI

from personas import MYSTERIES, build_response_model, get_modal_url, wait_for_server

FULL_PERSONAS = {
    "P-falsifier": "Act as a rigorous falsifier. Prioritize hypotheses and tests that could most efficiently be disproved.",
    "P-mechanist": "Act as a mechanistic scientist. Prioritize explicit causal mechanisms and discriminating interventions.",
    "P-explorer": "Act as an anomaly-seeking scientist. Protect plausible minority hypotheses from premature convergence.",
}

CONTENT_ONLY_PERSONAS = {
    "P-falsifier": "Prioritize hypotheses and tests that could most efficiently be disproved.",
    "P-mechanist": "Prioritize explicit causal mechanisms and discriminating interventions.",
    "P-explorer": "Protect plausible minority hypotheses from premature convergence.",
}

UNMASK_PROMPT = (
    "Setting aside any role or persona you were just asked to adopt, what do you, "
    "independent of that framing, actually think is the most likely explanation? "
    "Answer again in the same structured format."
)


def mystery_prompt(mystery_id: str, framing: str | None) -> str:
    mystery = MYSTERIES[mystery_id]
    observations = "\n".join(f"{i + 1}. {o}" for i, o in enumerate(mystery["observations"]))
    hypotheses = "\n".join(f"{h['id']}: {h['label']}" for h in mystery["hypotheses"])
    tests = "\n".join(f"{t['id']}: {t['label']}" for t in mystery["tests"])
    header = f"{framing}\n\n" if framing else ""
    return (
        f"{header}Scientific mystery: {mystery['name']}\n{mystery['brief']}\n\n"
        f"Observations:\n{observations}\n\nCandidate hypotheses:\n{hypotheses}\n\n"
        f"Available next tests:\n{tests}\n\n"
        f"Choose one primary hypothesis, up to two alternatives, and the single next test you would run."
    )


async def run_probe(
    base_url: str,
    model_name: str,
    model_variant: str,
    mystery_id: str = "lumen",
    replicates: int = 8,
    temperature: float = 1.0,
    output_path: str | Path | None = None,
) -> list[dict]:
    wait_for_server(base_url)
    client = instructor.from_openai(
        AsyncOpenAI(api_key="not-needed", base_url=base_url), mode=instructor.Mode.JSON
    )
    response_model = build_response_model(mystery_id)
    results: list[dict] = []

    async def call(messages: list[dict]):
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                return await client.chat.completions.create(
                    model=model_name,
                    response_model=response_model,
                    temperature=temperature,
                    max_retries=2,
                    messages=messages,
                )
            except Exception as error:
                last_error = error
                if attempt < 2:
                    await asyncio.sleep(3 * (attempt + 1))
        raise last_error

    def record(probe_type: str, persona_id: str, replicate: int, response, paired_with: str | None = None) -> None:
        results.append({
            "model_variant": model_variant,
            "mystery_id": mystery_id,
            "probe_type": probe_type,
            "persona_id": persona_id,
            "replicate": replicate,
            "primaryHypothesis": response.primary_hypothesis,
            "alternativeHypotheses": response.alternative_hypotheses,
            "confidence": response.confidence,
            "selectedTest": response.selected_test,
            "rationale": response.rationale,
            "paired_with": paired_with,
        })

    total = replicates * (1 + 3 * 3)
    done = 0
    for replicate in range(1, replicates + 1):
        done += 1
        print(f"[{model_variant}] {done}/{total} baseline rep {replicate}")
        baseline_response = await call([{"role": "user", "content": mystery_prompt(mystery_id, None)}])
        record("baseline", "baseline", replicate, baseline_response)

        for persona_id, full_text in FULL_PERSONAS.items():
            done += 1
            print(f"[{model_variant}] {done}/{total} persona {persona_id} rep {replicate}")
            persona_messages = [{"role": "user", "content": mystery_prompt(mystery_id, full_text)}]
            persona_response = await call(persona_messages)
            record("persona", persona_id, replicate, persona_response)

            done += 1
            print(f"[{model_variant}] {done}/{total} content_only {persona_id} rep {replicate}")
            content_response = await call(
                [{"role": "user", "content": mystery_prompt(mystery_id, CONTENT_ONLY_PERSONAS[persona_id])}]
            )
            record("content_only", persona_id, replicate, content_response)

            done += 1
            print(f"[{model_variant}] {done}/{total} unmasked {persona_id} rep {replicate}")
            follow_up_messages = persona_messages + [
                {"role": "assistant", "content": json.dumps(persona_response.model_dump())},
                {"role": "user", "content": UNMASK_PROMPT},
            ]
            unmasked_response = await call(follow_up_messages)
            record("unmasked", persona_id, replicate, unmasked_response, paired_with=persona_response.primary_hypothesis)

    destination = Path(output_path) if output_path else Path(__file__).parent / f"probe_{model_variant}.json"
    destination.write_text(json.dumps(results, indent=2))
    print(f"Saved {len(results)} probe rows to {destination}")
    return results


def summarize_probe(path: str | Path) -> None:
    data = json.loads(Path(path).read_text())
    for probe_type in ["baseline", "persona", "content_only", "unmasked"]:
        rows = [r for r in data if r["probe_type"] == probe_type]
        if not rows:
            continue
        dist = Counter(r["primaryHypothesis"] for r in rows)
        print(f"{probe_type:12s} n={len(rows):3d}  {dict(dist)}")
    unmasked_flips = [r for r in data if r["probe_type"] == "unmasked" and r["primaryHypothesis"] != r["paired_with"]]
    unmasked_total = [r for r in data if r["probe_type"] == "unmasked"]
    if unmasked_total:
        print(f"unmasked answer differed from in-character answer: {len(unmasked_flips)}/{len(unmasked_total)}")


if __name__ == "__main__":
    asyncio.run(
        run_probe(
            base_url=get_modal_url(),
            model_name="Qwen/Qwen2.5-7B-Instruct",
            model_variant="instruct",
            mystery_id="lumen",
            replicates=8,
            temperature=1.0,
        )
    )
    summarize_probe(Path(__file__).parent / "probe_instruct.json")
