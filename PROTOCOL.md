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
