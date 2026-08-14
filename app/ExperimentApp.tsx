"use client";

import { useEffect, useMemo, useState } from "react";
import { buildPrompt, calculateMetrics, conditions, makeDemoTrials, mysteries, type ConditionId, type Trial } from "./experiment";

const STORAGE_KEY = "epistemic-fingerprints-trials-v1";

const percent = (value: number) => `${Math.round(value * 100)}%`;

function download(name: string, content: string, type: string) {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = name;
  anchor.click();
  URL.revokeObjectURL(url);
}

export function ExperimentApp() {
  const [trials, setTrials] = useState<Trial[]>([]);
  const [view, setView] = useState<"live" | "demo">("demo");
  const [conditionId, setConditionId] = useState<ConditionId>("baseline");
  const [agentId, setAgentId] = useState("N-01");
  const [mysteryId, setMysteryId] = useState("vesper");
  const [modelLabel, setModelLabel] = useState("subscription model");
  const [rawOutput, setRawOutput] = useState("");
  const [notice, setNotice] = useState("");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) setTrials(JSON.parse(saved));
      } catch {
        setNotice("Saved trials could not be read on this device.");
      }
      setReady(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (ready) localStorage.setItem(STORAGE_KEY, JSON.stringify(trials));
  }, [ready, trials]);

  const activeCondition = conditions.find((condition) => condition.id === conditionId)!;
  const activeMystery = mysteries.find((mystery) => mystery.id === mysteryId)!;
  const dataset = useMemo(() => view === "demo" ? makeDemoTrials() : trials, [trials, view]);
  const metrics = conditions.map((condition) => ({ ...condition, metrics: calculateMetrics(dataset, condition.id) }));
  const prompt = buildPrompt(conditionId, agentId, activeMystery);

  function changeCondition(next: ConditionId) {
    const condition = conditions.find((item) => item.id === next)!;
    setConditionId(next);
    setAgentId(condition.agents[0]);
    setRawOutput("");
  }

  async function copyPrompt() {
    await navigator.clipboard.writeText(prompt);
    setNotice("Prompt copied. Run it in a fresh chat, then paste the JSON response below.");
  }

  function recordTrial() {
    try {
      const parsed = JSON.parse(rawOutput);
      const validHypotheses = new Set(activeMystery.hypotheses.map((item) => item.id));
      const validTests = new Set(activeMystery.tests.map((item) => item.id));
      if (!validHypotheses.has(parsed.primary_hypothesis) || !validTests.has(parsed.selected_test)) {
        throw new Error("The hypothesis or test ID is not valid for this mystery.");
      }
      const replicate = trials.filter((trial) => trial.condition === conditionId && trial.agentId === agentId && trial.mysteryId === mysteryId).length + 1;
      const trial: Trial = {
        id: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
        condition: conditionId,
        agentId,
        mysteryId,
        replicate,
        primaryHypothesis: parsed.primary_hypothesis,
        alternativeHypotheses: Array.isArray(parsed.alternative_hypotheses)
          ? parsed.alternative_hypotheses.filter((item: string) => validHypotheses.has(item)).slice(0, 2)
          : [],
        confidence: Math.max(0, Math.min(100, Number(parsed.confidence) || 0)),
        selectedTest: parsed.selected_test,
        rationale: String(parsed.rationale ?? ""),
      };
      setTrials((current) => [...current, trial]);
      setRawOutput("");
      setView("live");
      setNotice(`Recorded ${agentId} · ${activeMystery.name} · replicate ${replicate}. Model note: ${modelLabel}.`);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "That response is not valid JSON.");
    }
  }

  function exportData() {
    download("epistemic-fingerprints-trials.json", JSON.stringify({ exportedAt: new Date().toISOString(), trials }, null, 2), "application/json");
  }

  function importData(file: File) {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = JSON.parse(String(reader.result));
        const imported = Array.isArray(parsed) ? parsed : parsed.trials;
        if (!Array.isArray(imported)) throw new Error();
        setTrials(imported);
        setView("live");
        setNotice(`Imported ${imported.length} trials.`);
      } catch {
        setNotice("This file does not contain a valid trial dataset.");
      }
    };
    reader.readAsText(file);
  }

  return (
    <main>
      <nav className="nav shell" aria-label="Project navigation">
        <a className="wordmark" href="#top"><span>EF</span> Epistemic Fingerprints</a>
        <div className="nav-links">
          <a href="#idea">The idea</a>
          <a href="#ecology">The wider inquiry</a>
          <a href="#results">Results</a>
          <a href="#lab">Run a trial</a>
          <a href="#protocol">Protocol</a>
          <a href="#references">References</a>
        </div>
        <span className="status"><i /> Pilot · 2026</span>
      </nav>

      <header id="top" className="hero shell">
        <div className="hero-copy">
          <p className="eyebrow">Digital minds × epistemic diversity</p>
          <h1>Many agents.<br /><em>How many minds?</em></h1>
          <p className="lede">A behavioral pilot asking whether sampling, prompted personas, or different histories produce stable ways of forming and revising beliefs.</p>
          <div className="hero-actions">
            <a className="button primary" href="#lab">Run the first trial <span>↘</span></a>
            <a className="button ghost" href="#protocol">Read the protocol</a>
          </div>
        </div>
        <div className="fingerprint-card" aria-label="Conceptual fingerprint visualization">
          <div className="orbital orbital-a" /><div className="orbital orbital-b" />
          <div className="fp-center"><span>?</span><small>unit of<br />identity</small></div>
          <div className="fp-label label-a">model</div>
          <div className="fp-label label-b">persona</div>
          <div className="fp-label label-c">history</div>
          <div className="fp-label label-d">sample</div>
          <p>EPISODE 000<br />NO CLAIMS YET</p>
        </div>
      </header>

      <section className="question-band">
        <div className="shell question-grid">
          <p>THE QUESTION</p>
          <blockquote>Can we recognize an agent by <em>how it explores</em>—even after we remove its voice and name?</blockquote>
          <span>Epistemic individuality is not evidence of consciousness. It is one behavioral dimension relevant to individuation.</span>
        </div>
      </section>

      <section id="idea" className="section shell idea-section">
        <div className="section-head">
          <div><p className="eyebrow">00 · The idea</p><h2>More output is not necessarily more exploration</h2></div>
          <p>This pilot begins with epistemic diversity, then asks what it can tell us about digital minds.</p>
        </div>
        <div className="idea-grid">
          <div className="idea-statement">
            <p>AI lets us generate vastly more papers, hypotheses, designs and arguments. But are we exploring more of the space of possible ideas—or producing more variations around the same conceptual centers?</p>
            <p>The concern is not that humans are creative and AI is not. The interesting unit is the whole human–AI knowledge ecosystem: the models, people, institutions, observations and feedback loops through which ideas are produced and selected.</p>
          </div>
          <div className="idea-points">
            <article><span>01</span><div><h3>Apparent plurality</h3><p>Many agents can differ in voice while relying on the same assumptions, favoring the same hypotheses and making the same mistakes.</p></div></article>
            <article><span>02</span><div><h3>Epistemic plurality</h3><p>A stronger kind of difference would persist across tasks: what an agent notices, doubts, preserves as possible and chooses to test.</p></div></article>
            <article><span>03</span><div><h3>The empirical move</h3><p>Hold the model fixed, vary how candidate agents are formed, remove stylistic cues and compare their structured scientific choices.</p></div></article>
          </div>
        </div>
        <aside className="scope-note"><strong>The larger question</strong><p>Could the number of apparent cognitive agents increase dramatically while effective epistemic diversity decreases? This weekend study cannot answer that. It builds one small instrument for investigating it.</p></aside>
      </section>

      <section id="ecology" className="section ecology-section">
        <div className="shell">
          <div className="section-head light">
            <div><p className="eyebrow">01 · The wider inquiry</p><h2>When many voices share the same blind spots</h2></div>
            <p>The experiment is small. The world around the question is not.</p>
          </div>
          <p className="ecology-intro">If a few foundation models become part of how millions of people write, imagine, research and decide, epistemic diversity becomes more than a technical metric. It becomes a question about culture, power and what a society remains able to notice.</p>
          <div className="ecology-grid">
            <article><span>ART</span><h3>Can we perceive what is absent?</h3><p>Art can make convergence visible: repeated metaphors, familiar futures and conceptual regions that no agent enters. An epistemic atlas could show not only the ideas produced, but the negative space around them.</p></article>
            <article><span>POLITICS</span><h3>Who shapes the cognitive infrastructure?</h3><p>A population of assistants may appear plural while inheriting correlated assumptions from a small number of models. That matters for public reasoning, institutional decisions and the power to define which possibilities appear reasonable.</p></article>
            <article><span>SOCIETY</span><h3>Which experiences survive compression?</h3><p>Low-frequency languages, situated knowledge and minority explanations may be especially easy to lose. Social diversity and epistemic diversity are not identical, but neither can be treated as irrelevant to the other.</p></article>
            <article><span>PHILOSOPHY</span><h3>What makes one mind different from another?</h3><p>Is individuality a voice, a memory, a history, a stable way of questioning—or something else entirely? Behavioral differentiation cannot establish consciousness, but it can sharpen what we mean when we count models, personas and conversations as distinct agents.</p></article>
          </div>
          <p className="ecology-boundary"><strong>Two layers, kept distinct:</strong> the pilot produces a limited empirical result; the wider programme asks what such results could mean for digital identity and for human–AI knowledge ecosystems.</p>
        </div>
      </section>

      <section id="results" className="section shell">
        <div className="section-head">
          <div><p className="eyebrow">02 · Measurement</p><h2>Results observatory</h2></div>
          <div className="dataset-controls">
            <button className={view === "demo" ? "active" : ""} onClick={() => setView("demo")}>Simulated demo</button>
            <button className={view === "live" ? "active" : ""} onClick={() => setView("live")}>Live data <b>{trials.length}</b></button>
          </div>
        </div>

        {view === "demo" && <div className="warning"><strong>Illustrative data only.</strong> These values demonstrate the analysis interface; they are not research findings.</div>}
        {view === "live" && trials.length === 0 && <div className="empty"><span>∅</span><div><strong>No empirical observations yet.</strong><p>Record the first response in the Pilot Lab below. The dashboard will update immediately.</p></div></div>}

        <div className="metric-grid">
          <article><span>Recorded trials</span><strong>{dataset.length}</strong><small>target: 54</small></article>
          <article><span>Conditions</span><strong>{new Set(dataset.map((trial) => trial.condition)).size}</strong><small>sampling · persona · history</small></article>
          <article><span>Mysteries</span><strong>{new Set(dataset.map((trial) => trial.mysteryId)).size}</strong><small>synthetic, contamination-resistant</small></article>
          <article><span>Candidate agents</span><strong>{new Set(dataset.map((trial) => trial.agentId)).size}</strong><small>three per condition</small></article>
        </div>

        <div className="chart-card">
          <div className="chart-title"><div><span>FIGURE 01</span><h3>Do conditions leave different epistemic traces?</h3></div><p>Descriptive pilot metrics · 0–100</p></div>
          <div className="chart-legend"><span>Fingerprint strength</span><span>Hypothesis diversity</span><span>Accuracy</span><span>Shared-error concentration</span></div>
          <div className="chart-body">
            {metrics.map((item) => (
              <div className="chart-row" key={item.id}>
                <div className="condition-name"><i style={{ background: item.accent }} /><strong>{item.label}</strong><small>{item.metrics.trials} trials</small></div>
                {[
                  item.metrics.fingerprint,
                  item.metrics.diversity,
                  item.metrics.accuracy,
                  item.metrics.sharedError,
                ].map((value, index) => (
                  <div className="bar-cell" key={index}><div className="bar-track"><span style={{ width: `${value * 100}%`, background: item.accent }} /></div><b>{percent(value)}</b></div>
                ))}
              </div>
            ))}
          </div>
          <p className="chart-note"><b>How to read Figure 1:</b> compare rows across the four columns; no single bar means “better.” In demo mode, every bar is simulated to show what the finished comparison will look like. Switch to Live data to see recorded observations.</p>
        </div>
        <div className="figure-guide" aria-label="Explanation of Figure 1 metrics">
          <article><span>01</span><h3>Fingerprint strength</h3><p>Are differences between candidate agents larger than variation within each agent across repeated trials? Higher means a more stable trace, not a more conscious mind.</p></article>
          <article><span>02</span><h3>Hypothesis diversity</h3><p>How widely does a condition distribute its primary hypotheses? Higher means more alternatives are represented across the population.</p></article>
          <article><span>03</span><h3>Accuracy</h3><p>How often is the keyed explanation selected? Diversity without contact with truth can simply be noise, so exploration and performance are shown separately.</p></article>
          <article><span>04</span><h3>Shared-error concentration</h3><p>When agents are wrong, do they choose the same wrong answer? Higher concentration suggests correlated blind spots and therefore less epistemic independence.</p></article>
        </div>
        <p className="method-caveat"><strong>Important:</strong> these are descriptive pilot measures, not validated psychometric scales. With only 54 planned observations, the study is designed to reveal useful patterns and failure modes—not establish a general theory of digital identity.</p>
      </section>

      <section id="lab" className="lab-section">
        <div className="shell section-head light"><div><p className="eyebrow">03 · Collection</p><h2>Pilot lab</h2></div><p>One prompt. One fresh chat. One structured observation.</p></div>
        <div className="shell lab-grid">
          <div className="lab-controls">
            <label>Condition<select value={conditionId} onChange={(event) => changeCondition(event.target.value as ConditionId)}>{conditions.map((condition) => <option key={condition.id} value={condition.id}>{condition.label}</option>)}</select></label>
            <label>Candidate agent<select value={agentId} onChange={(event) => setAgentId(event.target.value)}>{activeCondition.agents.map((agent) => <option key={agent}>{agent}</option>)}</select></label>
            <label>Scientific mystery<select value={mysteryId} onChange={(event) => setMysteryId(event.target.value)}>{mysteries.map((mystery) => <option key={mystery.id} value={mystery.id}>{mystery.number} · {mystery.name}</option>)}</select></label>
            <label>Model note<input value={modelLabel} onChange={(event) => setModelLabel(event.target.value)} placeholder="e.g. ChatGPT subscription model" /></label>
            <button className="button coral" onClick={copyPrompt}>Copy controlled prompt <span>⌘C</span></button>
            <div className="lab-rule"><span /><p>Run every trial in a fresh conversation. Do not reveal the answer key or previous responses.</p></div>
          </div>
          <div className="prompt-panel">
            <div className="panel-head"><span>CONTROLLED PROMPT</span><button onClick={copyPrompt}>COPY</button></div>
            <pre>{prompt}</pre>
          </div>
          <div className="record-panel">
            <div className="panel-head"><span>MODEL RESPONSE</span><small>JSON only</small></div>
            <textarea value={rawOutput} onChange={(event) => setRawOutput(event.target.value)} placeholder={'Paste the model response here…\n\n{\n  "primary_hypothesis": "V-A",\n  …\n}'} />
            <button className="button lime" disabled={!rawOutput.trim()} onClick={recordTrial}>Validate & record <span>＋</span></button>
          </div>
        </div>
        {notice && <div className="shell notice" role="status">{notice}<button onClick={() => setNotice("")} aria-label="Dismiss notice">×</button></div>}
        <div className="shell data-strip">
          <div><strong>Your research data stays in this browser.</strong><span>Export it after every collection session.</span></div>
          <button onClick={exportData} disabled={!trials.length}>Export JSON</button>
          <label className="import">Import JSON<input type="file" accept="application/json" onChange={(event) => event.target.files?.[0] && importData(event.target.files[0])} /></label>
          <button className="danger" onClick={() => { if (confirm("Delete all locally recorded trials?")) setTrials([]); }} disabled={!trials.length}>Clear</button>
        </div>
      </section>

      <section id="protocol" className="section shell protocol">
        <div className="section-head"><div><p className="eyebrow">04 · Research design</p><h2>A small, falsifiable pilot</h2></div><p>Primary track: Assistant Persona & Model Identity</p></div>
        <div className="protocol-grid">
          <article><span>1</span><h3>Hold the model fixed</h3><p>Compare ordinary sampling, explicit personas, and formative histories without changing the underlying model.</p></article>
          <article><span>2</span><h3>Remove the costume</h3><p>Measure structured choices—not prose style: ranked hypotheses, uncertainty, and selected experiments.</p></article>
          <article><span>3</span><h3>Look for persistence</h3><p>Ask whether differences recur across unrelated mysteries and exceed ordinary within-agent variation.</p></article>
          <article><span>4</span><h3>Keep null results valuable</h3><p>If personas or histories leave no stable trace, that constrains claims about instance-level individuality.</p></article>
        </div>
        <div className="hypothesis">
          <p>PRIMARY RESEARCH QUESTION</p>
          <h3>Does conversational history create a more stable epistemic fingerprint than a prompted persona—or ordinary stochastic sampling?</h3>
          <div><span>H₀</span><p>Between-agent variation does not exceed within-agent variation.</p><span>H₁</span><p>At least one intervention creates a persistent, cross-task epistemic trace.</p></div>
        </div>
      </section>

      <section id="references" className="section references-section">
        <div className="shell">
          <div className="section-head">
            <div><p className="eyebrow">05 · Context</p><h2>Why ask this now?</h2></div>
            <p>The evidence does not point in only one direction. That is exactly why the question needs experiments.</p>
          </div>
          <div className="context-grid">
            <p>Recursive training can erode the tails of a distribution; populations built from different language models may resist some forms of knowledge collapse; and generative tools can make a group&apos;s creative output more homogeneous.</p>
            <p>But AI-generated ideas can also increase collective diversity under some conditions. The useful question is not whether AI is intrinsically homogenizing. It is <em>when</em> human–AI systems expand conceptual space, when they contract it, and what interventions change the outcome.</p>
          </div>
          <ol className="reference-list">
            <li><span>2024</span><div><a href="https://www.nature.com/articles/s41586-024-07566-y" target="_blank" rel="noreferrer">Shumailov et al. · AI models collapse when trained on recursively generated data ↗</a><p>Distributional degradation under recursive training on generated data. <i>Nature</i>.</p></div></li>
            <li><span>2024</span><div><a href="https://proceedings.mlr.press/v235/hughes24a.html" target="_blank" rel="noreferrer">Hughes et al. · Open-Endedness is Essential for Artificial Superhuman Intelligence ↗</a><p>Why continually producing new challenges and possibilities may be central to advanced intelligence.</p></div></li>
            <li><span>2024</span><div><a href="https://arxiv.org/abs/2401.13481" target="_blank" rel="noreferrer">Ashkinaze et al. · AI ideas and collective idea diversity ↗</a><p>Counterevidence showing that exposure to AI-generated ideas can increase collective diversity in some settings.</p></div></li>
            <li><span>2025</span><div><a href="https://arxiv.org/abs/2510.04226" target="_blank" rel="noreferrer">Wright et al. · Epistemic Diversity and Knowledge Collapse in LLMs ↗</a><p>An operational account of epistemic diversity in model-generated information.</p></div></li>
            <li><span>2025</span><div><a href="https://arxiv.org/abs/2512.15011" target="_blank" rel="noreferrer">Hodel &amp; West · Epistemic diversity across LMs mitigates knowledge collapse ↗</a><p>How heterogeneous model populations may make knowledge ecosystems more resilient.</p></div></li>
            <li><span>2026</span><div><a href="https://research.tilburguniversity.edu/en/publications/generative-ai-makes-creative-output-more-homogeneous/" target="_blank" rel="noreferrer">de Rooij &amp; Biskjaer · Generative AI Makes Creative Output More Homogeneous ↗</a><p>Individual creative gains alongside reduced variation across a population of outputs.</p></div></li>
          </ol>
          <div className="invitation">
            <p className="eyebrow">A LONGER INQUIRY</p>
            <h3>This is a beginning, not just a hackathon project.</h3>
            <p>I&apos;m interested in improving the experiment, exchanging ideas and connecting it to a broader interdisciplinary inquiry into epistemic diversity—in AI, science, culture and collective intelligence. Criticism, references, replications and contributions are welcome.</p>
            <a className="button primary" href="https://github.com/nefinia/epistemic-fingerprints" target="_blank" rel="noreferrer">Contribute on GitHub <span>↗</span></a>
          </div>
        </div>
      </section>

      <footer>
        <div className="shell"><div className="wordmark"><span>EF</span> Epistemic Fingerprints</div><p>A weekend pilot by Sofia · built as the first experiment of a longer inquiry into epistemic diversity.</p><a href="#top">Back to top ↑</a></div>
      </footer>
    </main>
  );
}
