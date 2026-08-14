# Epistemic Fingerprints

**Many agents. How many minds?**

Epistemic Fingerprints is a small empirical pilot for the Apart Research Digital Minds Research Sprint. It asks whether repeated samples, prompted personas, or different formative histories produce stable patterns in how a language model forms hypotheses, selects experiments, and expresses uncertainty.

The project does **not** treat behavioral individuality as evidence of consciousness or moral patienthood. It tests whether epistemic behavior can contribute one operational dimension to the model–instance–persona–conversation individuation problem.

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
