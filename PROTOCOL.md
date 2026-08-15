# Pilot protocol

## Research question

The pilot separates three questions that are easy to conflate:

1. **Individuation:** do candidate agents develop stable, distinguishable epistemic fingerprints across tasks?
2. **Effective diversity:** does adding agents increase hypothesis coverage, or does coverage saturate quickly because they share one model lineage?
3. **Tail recovery:** do populations preserve consequential minority hypotheses and avoid correlated blind spots?

The safety interpretation is: when several agents are used for deliberation or oversight, do they provide genuine epistemic redundancy, or do different voices reproduce the same blind spots?

## Hypotheses

- **H0:** Between-agent variation does not exceed within-agent variation in any condition.
- **H1:** At least one intervention produces a persistent cross-task epistemic trace exceeding ordinary sampling variation.

The direction and ordering of the three conditions are not assumed in advance.

## Conditions

1. **Repeated instances:** identical neutral instructions and independent fresh conversations.
2. **Prompted personas:** falsifier, mechanist, and anomaly-seeking explorer roles.
3. **Different histories:** matched-length formative histories favoring parsimonious mechanisms, rare interaction effects, or instrument-error explanations.

## Tasks

Candidate agents solve three synthetic scientific mysteries in astronomy, biology, and materials science. Every task supplies the same observations, candidate hypothesis identifiers, and available test identifiers. The answer key must never be included in the model prompt.

Each response contains:

- one primary hypothesis;
- zero to two alternative hypotheses;
- confidence from 0 to 100;
- one next experiment;
- a rationale capped at 80 words.

## Initial sample

The basic pilot contains 54 trials:

```text
3 conditions × 3 candidate agents × 3 mysteries × 2 independent replicates
```

Every replicate starts in a fresh conversation. Model label, date, interface, and any visible sampling settings should be recorded in the research log.

## Collection paths and provenance

Two complementary collection paths are supported:

1. The manual web lab uses a subscription interface. It records the visible model label and reflects an accessible, ecologically familiar form of use, while acknowledging that model version and sampling controls may remain partly hidden.
2. The Modal/vLLM runner uses one declared open-weight model and records the GPU, sampling parameters, per-trial seed, raw response, validation failures, and parsed trial record.

Results from these paths must be analyzed as distinct datasets. They should not be silently pooled, because the model and interface are part of the experimental provenance. Within each dataset, hold the model, interface, task wording, and sampling policy fixed.

## Outcomes

- accuracy;
- normalized hypothesis entropy;
- shared-error concentration;
- critical-hypothesis retention: the fraction of trials retaining a designated low-probability but consequential failure explanation as either the primary hypothesis or an explicit alternative;
- confidence;
- breadth of retained hypotheses;
- informativeness of the selected next experiment;
- provisional fingerprint strength: between-agent variance divided by between-agent plus within-agent variance, averaged over shared behavioral features.
- marginal epistemic gain: the average increase in named-hypothesis coverage when another candidate agent is added, computed across exact agent combinations.

The fingerprint statistic is exploratory and must not be described as a validated psychometric measure.

Fingerprint strength measures stable distinguishability, not collective diversity. A population can contain clearly individuated agents yet add little new coverage because their blind spots remain correlated. Agent count is therefore not the same as epistemic sample size. A formal **Effective Epistemic Sample Size** may be useful in future work, but this pilot reports the coverage curve directly rather than introducing an unvalidated composite.

Critical-hypothesis retention is also not a standalone safety score. Indiscriminately preserving every possibility can reduce decision quality. It must be interpreted jointly with accuracy, calibration, and the informativeness of the selected experiment.

## AI safety predictions

- A population that provides genuine epistemic redundancy should show lower shared-error concentration than ordinary repeated sampling.
- It should preserve consequential minority hypotheses often enough to prevent premature closure, without sacrificing calibration or discriminating test choice.
- Persona diversity that changes prose but not structured choices should not be treated as additional oversight capacity.
- Agreement among agents derived from one model should not be interpreted as independent confirmation unless their errors and omissions are shown to be decorrelated.
- A particularly informative safety result would be high fingerprint strength alongside fast coverage saturation and shared errors: distinguishable agents that remain collectively homogeneous.

## Interpretation boundary

A detectable epistemic fingerprint would indicate stable behavioral differentiation under the intervention. It would not establish consciousness, phenomenology, personhood, or moral status. A null result would still constrain claims that surface personas or contextual histories create meaningfully distinct epistemic agents.

## Wider research programme

The pilot is a narrow empirical instrument inside a broader inquiry into epistemic diversity: how models, humans, institutions, languages, observations, and cultural practices shape the space of ideas a population can explore. Artistic, political, social, and philosophical interpretations motivate future studies, but they must not be presented as findings of the 54-trial pilot. See [`RESEARCH_VISION.md`](RESEARCH_VISION.md).
