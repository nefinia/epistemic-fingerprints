# Epistemic Fingerprints

**Many agents. How many minds?**

The project's editorial voice and contribution guidelines are described in [`WRITING_STYLE.md`](WRITING_STYLE.md).

Epistemic Fingerprints is a small empirical pilot for the Apart Research Digital Minds Research Sprint. It asks whether repeated samples, prompted personas, or different formative histories produce stable patterns in how a language model forms hypotheses, selects experiments, and expresses uncertainty.

The project does **not** treat behavioral individuality as evidence of consciousness or moral patienthood. It tests whether epistemic behavior can contribute one operational dimension to the model–instance–persona–conversation individuation problem.

## A wider inquiry

The pilot is the empirical nucleus of a broader interdisciplinary question: what happens when many apparently different voices rely on increasingly shared cognitive infrastructure? This connects the measurement of epistemic fingerprints to art, philosophy, politics and society—not as substitutes for evidence, but as different ways of understanding what the evidence could mean.

- **Art:** make convergence, repetition and unexplored conceptual space perceptible rather than reducing diversity to a single score.
- **Politics:** examine who shapes the models that increasingly mediate public reasoning and institutional decisions.
- **Society:** study whether low-frequency languages, situated knowledge and minority explanations are disproportionately lost.
- **Philosophy:** clarify whether model, instance, persona, conversation, memory or epistemic history is the relevant unit of individuality.

The weekend submission keeps these implications separate from its limited empirical claims. The longer-term programme is described in [`RESEARCH_VISION.md`](RESEARCH_VISION.md).

## Pilot design

- One underlying model is held fixed.
- Three conditions are compared: neutral repeated instances, epistemic personas, and different formative histories.
- Candidate agents solve three synthetic scientific mysteries in fresh conversations.
- Responses use a shared JSON format to separate epistemic choices from writing style.
- The initial target is 54 observations: 3 conditions × 3 agents × 3 mysteries × 2 replicates.

The live dashboard calculates descriptive accuracy, hypothesis diversity, shared-error concentration, and a provisional epistemic fingerprint strength. The included simulated dataset is visibly labeled and exists only to demonstrate the interface.

## Reproduce the analysis

The repository includes both a runnable Jupyter notebook and reusable Python analysis code. The notebook validates a JSON export from the web lab, checks experimental coverage, calculates the four Figure 1 metrics, and generates the comparison plot.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-analysis.txt
jupyter notebook notebooks/epistemic_fingerprints_analysis.ipynb
```

By default the notebook uses an explicitly simulated 54-trial dataset so the full pipeline runs immediately. Set `DATA_PATH` to a JSON file exported by the web lab to analyze empirical observations. The analysis functions live in `analysis/pipeline.py` and can also be imported into scripts.

## Run the reproducible open-model pilot

The manual web-lab workflow preserves access to a subscription model but cannot fully control model version or sampling. A complementary runner executes the same 54-cell design on one declared open-weight model using Modal and vLLM. It records the model name, GPU, sampling parameters, per-trial seed, raw response, parse failures and validated trial data.

```bash
pip install -r requirements-modal.txt
modal setup
modal run experiments/modal_batch.py --output data/modal-qwen3-8b.json
```

The default is `Qwen/Qwen3-8B` on one L4 GPU. Set `EPISTEMIC_MODEL` and `EPISTEMIC_GPU` before the command to change them, but keep both fixed within a reported experiment. Modal's Starter plan currently includes monthly compute credit, and its academic programme advertises larger research grants; these credits cover Modal compute, not proprietary-model API charges. See the [Modal pricing page](https://modal.com/pricing) and [academic programme](https://modal.com/academics).

The open-model run should be reported as a distinct dataset, not silently pooled with subscription-interface trials. This separation makes model and interface effects auditable.

## Pilot report

The submission-ready pilot report is available at [`output/pdf/epistemic-fingerprints-pilot-report.pdf`](output/pdf/epistemic-fingerprints-pilot-report.pdf). It is intentionally framed as a protocol and open research artifact until empirical trial collection is complete.

The more in-depth research paper is available at [`output/pdf/epistemic-fingerprints-research-paper.pdf`](output/pdf/epistemic-fingerprints-research-paper.pdf). It develops the conceptual framework, related-work gap, falsifiable predictions, operational definitions, analysis and robustness plan, threats to validity, ethical interpretation, and longer-term research program. This is the recommended primary submission once the results section has been updated with empirical trials; the shorter pilot report works well as a visual overview.

Rebuild it with:

```bash
python tools/build_submission_pdf.py
python tools/build_research_paper_pdf.py
```

## Run locally

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Validate

```bash
npm run build
npm test
```

## Data handling

Empirical trial data is stored in the browser that records it. Export the JSON file after every collection session. No API key is required for the initial manual-subscription pilot, and no research data is transmitted by this app.

## Status

Protocol and collection instrument are under active development. No empirical result should be inferred from the simulated demonstration dataset.
