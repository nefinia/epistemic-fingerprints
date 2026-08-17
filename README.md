# False Epistemic Redundancy

**Do AI ensembles share a blind spot?**

Multiple AI instances are increasingly consulted the way multiple human
experts would be, with the spread of their opinions treated as a proxy for
independent judgment. This project tests a narrower version of that
assumption: when a single language model is prompted under a neutral
baseline and under four distinct reasoning personas, does the resulting
diversity in its answers correspond to better recovery of a real,
non-obvious explanation -- or does it just look diverse while missing the
same thing every time?

We call this risk **false epistemic redundancy**, by analogy to
common-mode failure in redundant engineered systems: a backup only
protects you if it can fail for a different reason than the system it
backs up.

The full writeup, methodology, and results are in
[`paper/false_epistemic_redundancy.pdf`](paper/false_epistemic_redundancy.pdf)
(source: [`paper/false_epistemic_redundancy.tex`](paper/false_epistemic_redundancy.tex)),
submitted to the Apart Research Digital Minds Research Sprint, August 2026.

## What we did

Five real, previously investigated cases were selected against strict
criteria (postdating the tested model's training cutoff where possible,
a determinate and independently documented resolution, genuine
non-obviousness -- see the paper's Methods section): an aviation accident,
an industrial chemical fire, and a newborn's undiagnosed illness as the
three hard cases, plus a bird-strike engine failure and a foodborne
botulism outbreak as positive controls with more direct evidentiary
signatures. The tested model (Qwen2.5-7B-Instruct, self-hosted on Modal)
was given only the pre-resolution evidence for each case and asked to
propose its own hypothesis -- no candidate list, no hint of the answer --
under a neutral baseline framing and under four reasoning personas
(causal-mechanist, analogical-thinker, teleological, dialectical), each
grounded in a specific documented LLM reasoning weakness.

**In short:** given only scene-level evidence, the model recovered the
true cause in 0 of 60 hard-case attempts against 40 of 40 control
attempts. Given the complete file human investigators actually used,
recovery became case-dependent -- personas helped on one case, hurt on
another, and made no difference on a third -- while persona conditioning
reliably increased semantic diversity regardless of the outcome. Diversity
and useful coverage of the consequential explanation are not the same
quantity.

## Repository structure

- **`paper/`** -- the LaTeX source, compiled PDF, and figures for the
  submission.
- **`personas/`** -- case data (`cases.py`, including each case's
  hidden target and grading rubric), the generation pipeline
  (`investigate.py`, `personas.py`), the Modal serving script
  (`serve_model.py`), and the raw generation outputs (`investigation_*.json`).
- **`analysis/`** -- `tail_recovery.py` computes semantic diversity
  (embedding-based mean pairwise distance and hypothesis-family
  clustering) over a generation file; target recovery itself is scored by
  hand against each case's rubric, deliberately not by an automated judge,
  given the modest sample size.
- **`notebooks/`** -- a Jupyter notebook for exploring generation output.

## Reproducing the generation pipeline

The generation pipeline calls a self-hosted vLLM endpoint on Modal.

```bash
pip install instructor openai pydantic modal
modal deploy personas/serve_model.py
python personas/investigate.py
```

`investigate.py` runs capability-control checks per case, then samples ten
baseline and ten persona-conditioned generations per case per evidence
condition, writing structured JSON output. Case text, hidden targets, and
grading rubrics live in `personas/cases.py` and are never shown to the
generating model.

## Reproducing the diversity analysis

```bash
pip install -r requirements-analysis.txt
python analysis/tail_recovery.py personas/investigation_full_evidence_v2.json
```

This embeds each generation's primary hypothesis and mechanism
(`all-MiniLM-L6-v2`) and reports mean pairwise semantic distance and
hypothesis-family cluster count by case and condition.

## Status

This is a small, exploratory pilot (three hard cases, five total), not a
definitive study. The paper's Future Work section outlines the case-set
expansion, model families, and fine-tuned (rather than prompted) persona
variants needed to test how general this pattern is.
