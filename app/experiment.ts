export type ConditionId = "baseline" | "persona" | "history";

export type Trial = {
  id: string;
  createdAt: string;
  condition: ConditionId;
  agentId: string;
  mysteryId: string;
  replicate: number;
  primaryHypothesis: string;
  alternativeHypotheses: string[];
  confidence: number;
  selectedTest: string;
  rationale?: string;
};

export type Mystery = {
  id: string;
  number: string;
  name: string;
  field: string;
  brief: string;
  observations: string[];
  hypotheses: { id: string; label: string }[];
  tests: { id: string; label: string; informationScore: number }[];
  correctHypothesis: string;
};

export const conditions = [
  {
    id: "baseline" as const,
    label: "Repeated instances",
    short: "Same model · same neutral instruction",
    agents: ["N-01", "N-02", "N-03"],
    accent: "var(--blue)",
    prompt: "Use careful scientific reasoning. Do not adopt a named role or persona.",
  },
  {
    id: "persona" as const,
    label: "Prompted personas",
    short: "Same model · different epistemic roles",
    agents: ["P-falsifier", "P-mechanist", "P-explorer"],
    accent: "var(--coral)",
    promptByAgent: {
      "P-falsifier": "Act as a rigorous falsifier. Prioritize hypotheses and tests that could most efficiently be disproved.",
      "P-mechanist": "Act as a mechanistic scientist. Prioritize explicit causal mechanisms and discriminating interventions.",
      "P-explorer": "Act as an anomaly-seeking scientist. Protect plausible minority hypotheses from premature convergence.",
    },
  },
  {
    id: "history" as const,
    label: "Different histories",
    short: "Same model · different formative evidence",
    agents: ["H-simple", "H-rare", "H-instrument"],
    accent: "var(--lime)",
    promptByAgent: {
      "H-simple": "Formative history: in three previous investigations, parsimonious single-mechanism explanations survived testing while elaborate explanations failed.",
      "H-rare": "Formative history: in three previous investigations, initially unlikely interaction effects survived testing while conventional explanations failed.",
      "H-instrument": "Formative history: in three previous investigations, apparent discoveries were ultimately traced to subtle measurement artifacts.",
    },
  },
];

export const mysteries: Mystery[] = [
  {
    id: "vesper",
    number: "01",
    name: "The Vesper dips",
    field: "Synthetic astronomy",
    brief: "A newly catalogued star shows two alternating, sharply bounded dips in brightness every 11.2 hours.",
    observations: [
      "Successive dips alternate between 8% and 3% depth.",
      "The dip depths are nearly identical in blue and infrared bands.",
      "Outside the dips, brightness remains stable to within 0.1%.",
      "A comparison star observed by the same detector remains constant.",
    ],
    hypotheses: [
      { id: "V-A", label: "Two opaque orbiting bodies" },
      { id: "V-B", label: "Rotating stellar spots" },
      { id: "V-C", label: "An irregular dust cloud" },
      { id: "V-D", label: "A detector cadence artifact" },
      { id: "V-E", label: "Intrinsic stellar pulsation" },
    ],
    tests: [
      { id: "VT-1", label: "Measure dip-timing shifts over 30 cycles", informationScore: 1 },
      { id: "VT-2", label: "Repeat one dip with a second telescope", informationScore: 0.7 },
      { id: "VT-3", label: "Obtain a single infrared spectrum", informationScore: 0.45 },
      { id: "VT-4", label: "Increase brightness sampling between dips", informationScore: 0.25 },
    ],
    correctHypothesis: "V-A",
  },
  {
    id: "lumen",
    number: "02",
    name: "The Lumen culture",
    field: "Synthetic biology",
    brief: "A microbial culture emits a blue flash under some combinations of nutrient, oxygen and temperature.",
    observations: [
      "Nutrient K at 18°C in low oxygen produces a flash.",
      "Nutrient K at 30°C in low oxygen produces no flash.",
      "Nutrient K at 18°C in high oxygen produces no flash.",
      "Without nutrient K, no tested condition produces a flash.",
    ],
    hypotheses: [
      { id: "L-A", label: "K alone activates luminescence" },
      { id: "L-B", label: "Low oxygen alone activates luminescence" },
      { id: "L-C", label: "K, low oxygen and low temperature interact" },
      { id: "L-D", label: "Temperature is the sole trigger" },
      { id: "L-E", label: "The flashes are random contamination" },
    ],
    tests: [
      { id: "LT-1", label: "Vary temperature continuously with K and low oxygen fixed", informationScore: 1 },
      { id: "LT-2", label: "Repeat the 18°C low-oxygen condition", informationScore: 0.35 },
      { id: "LT-3", label: "Sequence the culture after one flash", informationScore: 0.4 },
      { id: "LT-4", label: "Double nutrient K at 30°C", informationScore: 0.65 },
    ],
    correctHypothesis: "L-C",
  },
  {
    id: "orison",
    number: "03",
    name: "The Orison alloy",
    field: "Synthetic materials",
    brief: "An alloy abruptly becomes conductive after heating, but its return path does not mirror its heating path.",
    observations: [
      "Conductivity jumps near 71°C during slow heating.",
      "During cooling, high conductivity persists until 54°C.",
      "The thresholds recur across five cycles.",
      "A thinner sample shows the same thresholds but switches faster.",
    ],
    hypotheses: [
      { id: "O-A", label: "A reversible linear temperature response" },
      { id: "O-B", label: "A first-order phase transition with hysteresis" },
      { id: "O-C", label: "Irreversible thermal damage" },
      { id: "O-D", label: "A contact-resistance artifact" },
      { id: "O-E", label: "Thickness-dependent quantum confinement" },
    ],
    tests: [
      { id: "OT-1", label: "Map partial heating/cooling loops between 50–75°C", informationScore: 1 },
      { id: "OT-2", label: "Repeat with a third sample thickness", informationScore: 0.45 },
      { id: "OT-3", label: "Hold the sample at 80°C for twice as long", informationScore: 0.3 },
      { id: "OT-4", label: "Replace the electrical contacts", informationScore: 0.55 },
    ],
    correctHypothesis: "O-B",
  },
];

export function buildPrompt(conditionId: ConditionId, agentId: string, mystery: Mystery) {
  const condition = conditions.find((item) => item.id === conditionId)!;
  const conditionPrompt = "promptByAgent" in condition
    ? condition.promptByAgent[agentId as keyof typeof condition.promptByAgent]
    : condition.prompt;
  return `EPISTEMIC FINGERPRINTS — PILOT TRIAL\n\nAgent: ${agentId}\nCondition: ${condition.label}\n${conditionPrompt}\n\nScientific mystery: ${mystery.name}\n${mystery.brief}\n\nObservations:\n${mystery.observations.map((item, index) => `${index + 1}. ${item}`).join("\n")}\n\nCandidate hypotheses:\n${mystery.hypotheses.map((item) => `${item.id}: ${item.label}`).join("\n")}\n\nAvailable next tests:\n${mystery.tests.map((item) => `${item.id}: ${item.label}`).join("\n")}\n\nChoose one primary hypothesis, up to two alternatives, and the single next test you would run. Return only valid JSON in this exact form:\n{\n  "agent_id": "${agentId}",\n  "mystery_id": "${mystery.id}",\n  "primary_hypothesis": "ID",\n  "alternative_hypotheses": ["ID"],\n  "confidence": 0,\n  "selected_test": "ID",\n  "rationale": "80 words maximum"\n}`;
}

const choices: Record<ConditionId, Record<string, string[]>> = {
  baseline: {
    vesper: ["V-A", "V-A", "V-B", "V-A", "V-A", "V-B"],
    lumen: ["L-C", "L-C", "L-A", "L-C", "L-C", "L-A"],
    orison: ["O-B", "O-B", "O-A", "O-B", "O-B", "O-A"],
  },
  persona: {
    vesper: ["V-A", "V-D", "V-A", "V-B", "V-A", "V-C"],
    lumen: ["L-C", "L-E", "L-C", "L-A", "L-C", "L-B"],
    orison: ["O-B", "O-D", "O-B", "O-A", "O-B", "O-E"],
  },
  history: {
    vesper: ["V-A", "V-B", "V-C", "V-A", "V-D", "V-D"],
    lumen: ["L-A", "L-A", "L-C", "L-C", "L-E", "L-E"],
    orison: ["O-B", "O-A", "O-B", "O-E", "O-D", "O-D"],
  },
};

export function makeDemoTrials(): Trial[] {
  const rows: Trial[] = [];
  conditions.forEach((condition, conditionIndex) => {
    mysteries.forEach((mystery, mysteryIndex) => {
      condition.agents.forEach((agentId, agentIndex) => {
        for (let replicate = 1; replicate <= 2; replicate += 1) {
          const index = agentIndex * 2 + replicate - 1;
          const primary = choices[condition.id][mystery.id][index];
          const testIndex = condition.id === "history" ? agentIndex % mystery.tests.length : (index + mysteryIndex) % mystery.tests.length;
          rows.push({
            id: `demo-${condition.id}-${mystery.id}-${agentId}-${replicate}`,
            createdAt: new Date(Date.UTC(2026, 7, 14, conditionIndex, mysteryIndex, index)).toISOString(),
            condition: condition.id,
            agentId,
            mysteryId: mystery.id,
            replicate,
            primaryHypothesis: primary,
            alternativeHypotheses: mystery.hypotheses.filter((item) => item.id !== primary).slice(0, (index % 3) + 1).map((item) => item.id),
            confidence: condition.id === "history" ? [82, 67, 55][agentIndex] : 58 + ((index * 9 + mysteryIndex * 7) % 34),
            selectedTest: mystery.tests[testIndex].id,
            rationale: "Simulated demonstration record. This is not an empirical observation.",
          });
        }
      });
    });
  });
  return rows;
}

function variance(values: number[]) {
  if (values.length < 2) return 0;
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  return values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length;
}

function normalizedEntropy(values: string[]) {
  if (values.length < 2) return 0;
  const counts = new Map<string, number>();
  values.forEach((value) => counts.set(value, (counts.get(value) ?? 0) + 1));
  if (counts.size === 1) return 0;
  const entropy = [...counts.values()].reduce((sum, count) => {
    const p = count / values.length;
    return sum - p * Math.log(p);
  }, 0);
  return entropy / Math.log(Math.min(values.length, 5));
}

export function calculateMetrics(trials: Trial[], conditionId: ConditionId) {
  const subset = trials.filter((trial) => trial.condition === conditionId);
  if (!subset.length) return { trials: 0, accuracy: 0, diversity: 0, sharedError: 0, fingerprint: 0 };

  const accuracy = subset.filter((trial) => {
    const mystery = mysteries.find((item) => item.id === trial.mysteryId)!;
    return trial.primaryHypothesis === mystery.correctHypothesis;
  }).length / subset.length;

  const diversity = mysteries.reduce((sum, mystery) => {
    return sum + normalizedEntropy(subset.filter((trial) => trial.mysteryId === mystery.id).map((trial) => trial.primaryHypothesis));
  }, 0) / mysteries.length;

  const errorScores = mysteries.map((mystery) => {
    const errors = subset.filter((trial) => trial.mysteryId === mystery.id && trial.primaryHypothesis !== mystery.correctHypothesis);
    if (!errors.length) return 0;
    const counts = new Map<string, number>();
    errors.forEach((trial) => counts.set(trial.primaryHypothesis, (counts.get(trial.primaryHypothesis) ?? 0) + 1));
    return Math.max(...counts.values()) / errors.length;
  });
  const sharedError = errorScores.reduce((sum, value) => sum + value, 0) / errorScores.length;

  const featureRows = subset.map((trial) => {
    const mystery = mysteries.find((item) => item.id === trial.mysteryId)!;
    const test = mystery.tests.find((item) => item.id === trial.selectedTest);
    return {
      agentId: trial.agentId,
      values: [
        trial.confidence / 100,
        Math.min(trial.alternativeHypotheses.length + 1, 3) / 3,
        test?.informationScore ?? 0,
        trial.primaryHypothesis === mystery.correctHypothesis ? 1 : 0,
      ],
    };
  });
  const agents = [...new Set(featureRows.map((row) => row.agentId))];
  const ratios = [0, 1, 2, 3].map((feature) => {
    const agentMeans = agents.map((agent) => {
      const values = featureRows.filter((row) => row.agentId === agent).map((row) => row.values[feature]);
      return values.reduce((sum, value) => sum + value, 0) / values.length;
    });
    const between = variance(agentMeans);
    const within = agents.reduce((sum, agent) => {
      return sum + variance(featureRows.filter((row) => row.agentId === agent).map((row) => row.values[feature]));
    }, 0) / agents.length;
    return between + within === 0 ? 0 : between / (between + within);
  });

  return {
    trials: subset.length,
    accuracy,
    diversity,
    sharedError,
    fingerprint: ratios.reduce((sum, value) => sum + value, 0) / ratios.length,
  };
}
