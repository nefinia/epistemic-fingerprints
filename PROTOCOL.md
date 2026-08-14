# Pilot protocol

## Research question

Does conversational history create a more stable cross-task epistemic fingerprint than a prompted persona or ordinary stochastic sampling from the same language model?

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
- confidence;
- breadth of retained hypotheses;
- informativeness of the selected next experiment;
- provisional fingerprint strength: between-agent variance divided by between-agent plus within-agent variance, averaged over shared behavioral features.

The fingerprint statistic is exploratory and must not be described as a validated psychometric measure.

## Interpretation boundary

A detectable epistemic fingerprint would indicate stable behavioral differentiation under the intervention. It would not establish consciousness, phenomenology, personhood, or moral status. A null result would still constrain claims that surface personas or contextual histories create meaningfully distinct epistemic agents.

## Wider research programme

The pilot is a narrow empirical instrument inside a broader inquiry into epistemic diversity: how models, humans, institutions, languages, observations, and cultural practices shape the space of ideas a population can explore. Artistic, political, social, and philosophical interpretations motivate future studies, but they must not be presented as findings of the 54-trial pilot. See [`RESEARCH_VISION.md`](RESEARCH_VISION.md).
