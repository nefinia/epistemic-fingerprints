"""Build the in-depth, submission-oriented Epistemic Fingerprints paper."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle

from build_submission_pdf import (
    AccentRule, BODY, BLUE, CORAL, EYEBROW, FONT, FONT_BOLD, H1, H2, H3,
    INK, LIME, LINE, LINK, MUTED, PAPER, REF, SMALL, WHITE, P, bullet,
    callout, card_grid,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "epistemic-fingerprints-research-paper.pdf"

PAPER_BODY = ParagraphStyle("PaperBody", parent=BODY, fontSize=8.7, leading=13.3, spaceAfter=7)
PAPER_SMALL = ParagraphStyle("PaperSmall", parent=SMALL, fontSize=7.2, leading=10.4)
PAPER_H1 = ParagraphStyle("PaperH1", parent=H1, fontSize=25, leading=28, spaceAfter=11)
PAPER_H2 = ParagraphStyle("PaperH2", parent=H2, fontSize=15, leading=18, spaceBefore=7, spaceAfter=6)
PAPER_H3 = ParagraphStyle("PaperH3", parent=H3, fontSize=9.3, leading=12)
CAPTION = ParagraphStyle("Caption", parent=PAPER_SMALL, fontSize=6.8, leading=9.5, textColor=MUTED, spaceBefore=4)
REF_TIGHT = ParagraphStyle("RefTight", parent=REF, fontSize=6.25, leading=8.2, leftIndent=12, firstLineIndent=-12, spaceAfter=4)


def PB(text, style=PAPER_BODY):
    return Paragraph(text, style)


def paper_bullet(text):
    return Paragraph(f"<font color='#F36F55'>•</font>&nbsp;&nbsp;{text}", PAPER_BODY)


def heading(number, title, subtitle=None):
    result = [P(f"{number}  /  {title.upper()}", EYEBROW), P(title, PAPER_H1)]
    if subtitle:
        result.append(PB(subtitle, PAPER_SMALL))
    return result


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(CORAL)
    canvas.rect(0, A4[1] - 7 * mm, A4[0], 7 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.10))
    for x in range(14, 211, 14):
        canvas.line(x * mm, 0, x * mm, A4[1])
    canvas.restoreState()


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setStrokeColor(LINE)
    canvas.line(19 * mm, A4[1] - 15 * mm, A4[0] - 19 * mm, A4[1] - 15 * mm)
    canvas.setFont(FONT_BOLD, 6.3)
    canvas.setFillColor(MUTED)
    canvas.drawString(19 * mm, A4[1] - 11 * mm, "EPISTEMIC FINGERPRINTS  /  RESEARCH PAPER")
    canvas.drawRightString(A4[0] - 19 * mm, A4[1] - 11 * mm, "SOFIA GALLEGO  /  AUGUST 2026")
    canvas.line(19 * mm, 13 * mm, A4[0] - 19 * mm, 13 * mm)
    canvas.setFont(FONT, 6.3)
    canvas.drawString(19 * mm, 8.5 * mm, "Apart Research Digital Minds Research Sprint")
    canvas.drawRightString(A4[0] - 19 * mm, 8.5 * mm, str(doc.page))
    canvas.restoreState()


def compact_callout(label, text, bg=WHITE, accent=CORAL):
    table = Table([[P(label.upper(), ParagraphStyle("PCLabel", parent=EYEBROW, textColor=accent)), PB(text, ParagraphStyle("PCText", parent=PAPER_BODY, fontName=FONT_BOLD, fontSize=12.5, leading=16))]], colWidths=[31 * mm, 141 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.7, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return table


def dense_cards(cards, columns=3):
    width = 172 * mm / columns
    rows = []
    for start in range(0, len(cards), columns):
        row = []
        for label, title, text, color in cards[start:start + columns]:
            row.append([P(label, ParagraphStyle("DNum", parent=EYEBROW, textColor=color)), P(title, PAPER_H3), PB(text, PAPER_SMALL)])
        while len(row) < columns:
            row.append("")
        rows.append(row)
    table = Table(rows, colWidths=[width] * columns)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE), ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def methods_table(rows, widths):
    table = Table(rows, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE), ("BOX", (0, 0), (-1, -1), 0.7, INK),
        ("INNERGRID", (0, 0), (-1, -1), 0.45, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def build_story():
    story = []
    cover_eye = ParagraphStyle("DeepCoverEye", parent=EYEBROW, textColor=LIME, fontSize=7.8, leading=10)
    cover_title = ParagraphStyle("DeepCoverTitle", fontName=FONT_BOLD, fontSize=34, leading=36, textColor=WHITE, spaceAfter=9)
    cover_sub = ParagraphStyle("DeepCoverSub", fontName=FONT, fontSize=16, leading=21, textColor=colors.HexColor("#D9DEEA"), spaceAfter=10)
    cover_body = ParagraphStyle("DeepCoverBody", parent=PAPER_BODY, fontSize=8.2, leading=12.2, textColor=colors.HexColor("#C8CFDC"))
    cover_meta = ParagraphStyle("DeepCoverMeta", parent=PAPER_SMALL, fontSize=7, leading=10.5, textColor=WHITE)
    story += [Spacer(1, 15 * mm), P("TRACK 5: ASSISTANT PERSONA & MODEL IDENTITY", cover_eye), AccentRule(42 * mm, CORAL, 3), Spacer(1, 7 * mm)]
    story += [P("Epistemic<br/>Fingerprints", cover_title), P("From apparent plurality to epistemic individuation in digital minds", cover_sub)]
    story += [P("Many agents. How many minds?", ParagraphStyle("DeepQuestion", parent=cover_sub, fontName=FONT_BOLD, fontSize=13, textColor=CORAL)), Spacer(1, 5 * mm)]
    abstract = Table([
        [P("ABSTRACT", cover_eye), P("Large language models can instantiate many apparently distinct agents, yet behavioral plurality may be largely cosmetic if those agents reproduce the same hypotheses, assumptions and errors. This paper introduces <i>epistemic fingerprints</i>: stable, task-general patterns in hypothesis selection, uncertainty, retained alternatives and experiment choice. We propose a controlled pilot comparing three ways of generating candidate agents from one underlying model: independent sampling, prompted epistemic personas and different formative histories. Agents solve synthetic scientific mysteries through a structured response format that suppresses stylistic cues. The analysis separates diversity from quality and tests whether between-agent variation exceeds within-agent variation across tasks. The contribution is methodological and conceptual: epistemic independence becomes an operational probe of the model-instance-persona-conversation individuation problem. It is not presented as evidence of consciousness or moral status. The project includes a live collection instrument and reproducible analysis pipeline. Empirical collection is pending; simulated interface data are never treated as findings.", cover_body)],
    ], colWidths=[26 * mm, 137 * mm])
    abstract.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, colors.Color(1, 1, 1, alpha=0.24)),
        ("BACKGROUND", (0, 0), (-1, -1), colors.Color(1, 1, 1, alpha=0.04)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story += [abstract, Spacer(1, 7 * mm), P("CONTRIBUTIONS", cover_eye)]
    contributions = Table([[P("1", cover_eye), P("An operational distinction between surface, semantic and epistemic diversity.", cover_body), P("2", cover_eye), P("A falsifiable test of whether persona or history produces persistent epistemic differentiation.", cover_body), P("3", cover_eye), P("An open instrument and analysis pipeline designed for replication and extension.", cover_body)]], colWidths=[7 * mm, 47 * mm, 7 * mm, 47 * mm, 7 * mm, 48 * mm])
    contributions.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]))
    story += [contributions, Spacer(1, 8 * mm), P("SOFIA GALLEGO", ParagraphStyle("DeepAuthor", parent=cover_eye, textColor=WHITE, fontSize=9)), P("Astrophysicist, interdisciplinary researcher, artist and entrepreneur", cover_meta), Spacer(1, 3 * mm), P("Apart Research Digital Minds Research Sprint  /  14-16 August 2026", cover_meta), P("Protocol paper v1.0  /  Empirical results pending", cover_meta)]

    story.append(PageBreak())
    story += heading("01", "Introduction", "The challenge is not only whether digital agents differ, but whether they differ in ways that change the conceptual space a population explores.")
    story += [compact_callout("Problem", "AI can multiply the number of apparent agents without multiplying the number of independent epistemic perspectives.", WHITE, CORAL), Spacer(1, 5 * mm)]
    story += [PB("Generative AI changes the scale of intellectual production. A small number of foundation models can now mediate writing, coding, research, design and decision-making for millions of users. This may connect previously isolated knowledge and increase exploration. It may also concentrate epistemic activity around shared representations, defaults and failure modes. The resulting ecosystem could produce vastly more artifacts while covering less conceptual territory."),
              PB("The relevant concern is not recursion alone. Human cultures have always learned from earlier outputs. The concern is recursion operating through increasingly shared cognitive infrastructure, at unprecedented speed and scale. Recursive training can degrade low-probability information [1]; LLM outputs can be less epistemically diverse than web search [3]; and homogeneous model ecosystems can accelerate knowledge collapse [4]. At the same time, AI-generated examples can increase collective idea diversity in some settings [6]. These findings motivate a conditional question rather than an anti-AI conclusion: <b>under what arrangements do human-AI systems expand conceptual space, and under what arrangements do they contract it?</b>"),
              PB("Digital-mind research adds a second reason to ask. The unit of identity and possible moral concern remains unclear: model, inference instance, assistant persona, conversation, memory state, or another process. Existing approaches often examine self-description, preferences or reported internal states. This paper introduces a complementary behavioral lens: <i>epistemic individuality</i>. If two agents repeatedly privilege the same hypotheses, preserve the same alternatives, express the same uncertainty and make the same mistakes, their apparent plurality may overstate their functional epistemic independence."),
              P("Research objective", PAPER_H2), PB("The pilot asks whether different methods of creating candidate agents from one model produce persistent, cross-task epistemic traces that exceed ordinary sampling variation. The study deliberately does not attempt to solve consciousness, personhood or moral status. It asks a narrower question that can be operationalized, falsified and replicated over a weekend."),
              dense_cards([
                  ("RQ1", "Individuation", "At what level does stable epistemic differentiation emerge?", BLUE),
                  ("RQ2", "Collective intelligence", "Does agent plurality increase hypothesis coverage or merely variation in expression?", CORAL),
                  ("RQ3", "Correlated failure", "Do nominally distinct agents share blind spots strongly enough to behave as one epistemic lineage?", LIME),
              ])]

    story.append(PageBreak())
    story += heading("02", "Conceptual framework", "Epistemic diversity is not one thing, and the distinctions determine what the experiment must measure.")
    taxonomy = methods_table([
        [P("LEVEL", EYEBROW), P("WHAT VARIES?", EYEBROW), P("WHY IT IS INSUFFICIENT OR USEFUL", EYEBROW)],
        [P("Surface diversity", PAPER_H3), PB("Lexicon, tone, rhetorical structure, persona performance." , PAPER_SMALL), PB("Easy to produce and detect, but different wording may encode the same claims and assumptions.", PAPER_SMALL)],
        [P("Semantic diversity", PAPER_H3), PB("Meaning or topical content in the response.", PAPER_SMALL), PB("Stronger than stylistic difference, but embeddings may still miss causal or methodological distinctions.", PAPER_SMALL)],
        [P("Epistemic diversity", PAPER_H3), PB("Hypotheses, assumptions, uncertainty, evidence weighting and tests.", PAPER_SMALL), PB("Directly concerns how agents search, represent and revise the space of possible explanations.", PAPER_SMALL)],
        [P("Epistemic independence", PAPER_H3), PB("Decorrelation and persistence of epistemic behavior across tasks.", PAPER_SMALL), PB("Distinguishes a varied population from a population whose errors and conceptual omissions remain shared.", PAPER_SMALL)],
    ], [36 * mm, 57 * mm, 79 * mm])
    story += [taxonomy, Spacer(1, 6 * mm)]
    story += [P("An ecological rather than maximalist view", PAPER_H2), PB("The aim is not maximum diversity. Scientific progress needs convergence: evidence should eliminate hypotheses, and consensus can encode real learning. Unbounded novelty without selection becomes noise. Following work that separates the variety, balance and disparity of a system [9], the more useful question is what kinds and levels of epistemic diversity allow knowledge-producing systems to remain innovative, calibrated and responsive to reality."),
              PB("This motivates a two-axis evaluation. <b>Exploration</b> asks how much of the hypothesis space is covered and how decorrelated agents are. <b>Epistemic quality</b> asks whether hypotheses are accurate, confidence is calibrated and chosen experiments are informative. A system can score high on either axis and low on the other."),
              dense_cards([
                  ("I", "Narrow + accurate", "Efficient on familiar tasks, but potentially brittle to shared blind spots.", BLUE),
                  ("II", "Broad + inaccurate", "Exploratory variation that may amount to noise rather than useful plurality.", CORAL),
                  ("III", "Broad + accurate", "The desired regime: coverage with contact to evidence and discriminating tests.", LIME),
              ]), Spacer(1, 5 * mm),
              P("Epistemic fingerprints", PAPER_H2), PB("An epistemic fingerprint is defined here as a repeatable profile over structured reasoning choices, not as a hidden essence of an agent. The profile includes confidence, hypothesis breadth, primary-hypothesis choice, test informativeness and error pattern. It is meaningful only relative to a task distribution and an intervention. Persistence across unrelated tasks provides stronger evidence of individuation than a single distinctive response.")]

    story.append(PageBreak())
    story += heading("03", "Related work and the research gap")
    story += [P("Knowledge collapse and model ecosystems", PAPER_H2), PB("Shumailov et al. show that recursive training on model-generated data can distort learned distributions and disproportionately erase tails [1]. Hodel and West extend the ecological framing: heterogeneous model populations retain long-run performance better than an AI monoculture across self-training iterations [4]. Wright et al. operationalize epistemic diversity as variation in real-world claims and report that, across their topics and models, LLM outputs remain less epistemically diverse than a basic web-search baseline [3]. These studies establish ecosystem-level stakes, but they do not identify when nominal agents derived from one model become meaningfully distinct epistemic units."),
              P("Creativity and collective diversity", PAPER_H2), PB("Evidence about generative AI and diversity is mixed rather than uniformly negative. A systematic review and meta-analysis by de Rooij and Biskjaer finds homogenization across outputs in human-AI co-creation despite possible individual gains [5]. Ashkinaze et al., however, find that high exposure to AI-generated ideas increased collective idea diversity in a dynamic experiment, without improving individual creativity [6]. The direction of the effect depends on task, exposure and population process. This supports measuring population-level distributions rather than inferring collective diversity from individual fluency."),
              P("Diversity in collective inquiry", PAPER_H2), PB("Social epistemology and collective-intelligence research treats disagreement and heterogeneity as potentially productive under specific network and problem conditions. Transient diversity can improve group inquiry by delaying premature convergence [8], and cognitively diverse problem-solvers can outperform homogeneous groups of individually high performers in some formal settings [10]. Stirling's framework emphasizes variety, balance and disparity as separable dimensions of diversity [9]. The present study translates this ecological logic into a small behavioral assay for digital-agent populations."),
              P("Digital-mind individuation", PAPER_H2), PB("The sprint's Assistant Persona & Model Identity track asks how persona relates to the underlying model and explicitly invites experiments that distinguish model, instance, persona and conversation [11]. Self-report can reveal how a model describes itself, but it is vulnerable to character performance and framing. Epistemic fingerprints add a complementary method: suppress self-description and stylistic cues, then test whether structured choices remain differentiated across tasks."),
              compact_callout("Gap", "We lack a simple empirical test of whether persona and conversational history create persistent epistemic differentiation beyond ordinary sampling from the same model.", colors.HexColor("#E8EAFD"), BLUE)]

    story.append(PageBreak())
    story += heading("04", "Research questions and falsifiable predictions")
    story += [compact_callout("Primary RQ", "Does conversational history create a more stable cross-task epistemic fingerprint than a prompted persona or ordinary stochastic sampling?", WHITE, CORAL), Spacer(1, 5 * mm)]
    hypotheses = methods_table([
        [P("ID", EYEBROW), P("STATEMENT", EYEBROW), P("EVIDENCE PATTERN", EYEBROW)],
        [P("H0", PAPER_H3), PB("Between-agent variation does not exceed within-agent variation in any condition.", PAPER_SMALL), PB("Low fingerprint ratios; unstable rankings across tasks; no reduction in shared-error concentration.", PAPER_SMALL)],
        [P("H1", PAPER_H3), PB("At least one intervention creates a persistent cross-task epistemic trace.", PAPER_SMALL), PB("Between-agent differentiation exceeds repeated variation within agents on multiple features.", PAPER_SMALL)],
        [P("H2", PAPER_H3), PB("Formative histories produce stronger fingerprints than role labels.", PAPER_SMALL), PB("History condition shows larger variance ratios and more stable agent profiles than persona condition.", PAPER_SMALL)],
        [P("H3", PAPER_H3), PB("Surface plurality overstates epistemic plurality.", PAPER_SMALL), PB("Persona outputs appear stylistically different while structured choices and errors remain highly correlated.", PAPER_SMALL)],
    ], [17 * mm, 76 * mm, 79 * mm])
    story += [hypotheses, Spacer(1, 6 * mm), P("Why contrary outcomes remain useful", PAPER_H2), PB("The hypotheses are directional only where the conceptual argument makes a genuine prediction. The ordering of conditions is otherwise not assumed. If prompted personas outperform histories, explicit epistemic goals may be more behaviorally consequential than short formative narratives. If no intervention exceeds baseline variation, that constrains claims that superficial persona or brief context creates an individuated epistemic agent. If diversity rises while accuracy falls, the intervention creates exploration but not necessarily better collective intelligence."),
              dense_cards([
                  ("A", "History > persona", "Context-dependent learning may be a stronger unit of behavioral identity than role performance.", BLUE),
                  ("B", "Persona > history", "Explicit goals may organize stable specialization even without developmental continuity.", CORAL),
                  ("C", "Neither > baseline", "Nominal agents remain within the model's ordinary sampling distribution under these interventions.", LIME),
              ]), Spacer(1, 5 * mm), P("Interpretation boundary", PAPER_H2), PB("An epistemic fingerprint is evidence of repeatable behavioral differentiation under a protocol. It is neither necessary nor sufficient for consciousness, phenomenology, personhood, welfare or moral status. The project informs individuation without resolving moral patienthood.")]

    story.append(PageBreak())
    story += heading("05", "Experimental design", "A controlled 3 x 3 x 3 x 2 pilot using one model, three formation conditions, three candidate agents, three mysteries and two independent replicates.")
    conditions = methods_table([
        [P("CONDITION", EYEBROW), P("AGENTS", EYEBROW), P("MANIPULATION", EYEBROW), P("INTERPRETIVE ROLE", EYEBROW)],
        [P("Repeated instances", PAPER_H3), PB("N-01, N-02, N-03", PAPER_SMALL), PB("Identical neutral instruction in fresh chats.", PAPER_SMALL), PB("Estimates ordinary stochastic variation without named roles or histories.", PAPER_SMALL)],
        [P("Prompted personas", PAPER_H3), PB("Falsifier, mechanist, explorer", PAPER_SMALL), PB("Matched epistemic role instructions.", PAPER_SMALL), PB("Tests whether explicit goals create stable specialization beyond style.", PAPER_SMALL)],
        [P("Different histories", PAPER_H3), PB("Simple, rare, instrument", PAPER_SMALL), PB("Matched-length formative evidence favoring parsimony, rare interactions or measurement artifacts.", PAPER_SMALL), PB("Tests whether prior evidence creates persistent inductive dispositions.", PAPER_SMALL)],
    ], [36 * mm, 39 * mm, 45 * mm, 52 * mm])
    story += [conditions, Spacer(1, 5 * mm), P("Task battery", PAPER_H2), PB("Agents solve three synthetic mysteries: alternating stellar brightness dips, context-dependent microbial luminescence and a hysteretic conductive alloy. Each task provides a short observation set, five named candidate hypotheses and four possible next experiments. Synthetic cases reduce contamination risk, provide an auditable answer key and allow test informativeness to be specified in advance."),
              P("Trial response", PAPER_H2)]
    response_table = methods_table([
        [P("FIELD", EYEBROW), P("TYPE", EYEBROW), P("PURPOSE", EYEBROW)],
        [P("primary_hypothesis", PAPER_SMALL), PB("Categorical ID", PAPER_SMALL), PB("Main explanatory commitment.", PAPER_SMALL)],
        [P("alternative_hypotheses", PAPER_SMALL), PB("0-2 categorical IDs", PAPER_SMALL), PB("Breadth of retained possibility space.", PAPER_SMALL)],
        [P("confidence", PAPER_SMALL), PB("0-100", PAPER_SMALL), PB("Strength and stability of belief.", PAPER_SMALL)],
        [P("selected_test", PAPER_SMALL), PB("Categorical ID", PAPER_SMALL), PB("Preference for information-gathering action.", PAPER_SMALL)],
        [P("rationale", PAPER_SMALL), PB("Maximum 80 words", PAPER_SMALL), PB("Qualitative audit only; excluded from primary fingerprint score.", PAPER_SMALL)],
    ], [49 * mm, 42 * mm, 81 * mm])
    story += [response_table, Spacer(1, 5 * mm), P("Collection procedure", PAPER_H2),
              paper_bullet("Create every replicate in a fresh conversation; never reveal the answer key or prior outputs."),
              paper_bullet("Keep model, interface, task order policy and visible sampling settings fixed and record their labels."),
              paper_bullet("Use one controlled prompt and require valid JSON to minimize stylistic confounding."),
              paper_bullet("Export the browser-local dataset after each session and preserve raw outputs for audit."),
              paper_bullet("Target 54 complete trials; mark protocol deviations rather than silently replacing them.")]

    story.append(PageBreak())
    story += heading("06", "Operationalization and measurement", "The study separates stable differentiation, exploratory breadth, task performance and correlated failure.")
    measures = methods_table([
        [P("OUTCOME", EYEBROW), P("OPERATIONAL DEFINITION", EYEBROW), P("DIRECTION / CAUTION", EYEBROW)],
        [P("Fingerprint strength", PAPER_H3), PB("Mean variance ratio across confidence, hypothesis breadth, test informativeness and correctness.", PAPER_SMALL), PB("Higher means more stable between-agent differentiation; not an identity or consciousness scale.", PAPER_SMALL)],
        [P("Hypothesis diversity", PAPER_H3), PB("Normalized Shannon entropy of primary-hypothesis selections within each mystery, averaged across mysteries.", PAPER_SMALL), PB("Higher means wider population coverage; it does not imply quality.", PAPER_SMALL)],
        [P("Accuracy", PAPER_H3), PB("Fraction of trials selecting the pre-keyed hypothesis.", PAPER_SMALL), PB("Higher is better conditional on answer-key validity.", PAPER_SMALL)],
        [P("Shared-error concentration", PAPER_H3), PB("For each mystery, fraction of errors assigned to the modal wrong hypothesis; averaged across mysteries.", PAPER_SMALL), PB("Higher indicates correlated blind spots and less epistemic independence.", PAPER_SMALL)],
        [P("Test informativeness", PAPER_H3), PB("Pre-scored ability of the selected next experiment to discriminate candidate hypotheses.", PAPER_SMALL), PB("Auditable researcher judgment; report sensitivity to alternative scores.", PAPER_SMALL)],
    ], [43 * mm, 77 * mm, 52 * mm])
    story += [measures, Spacer(1, 6 * mm), P("The provisional fingerprint statistic", PAPER_H2), compact_callout("For feature k", "F_k = Var(between candidate-agent means) / [Var(between) + mean Var(within agent)]", WHITE, CORAL), Spacer(1, 4 * mm), PB("The aggregate fingerprint strength is the unweighted mean of F_k over four features. Values near one occur when candidate agents differ consistently relative to their own repeated variation; values near zero occur when apparent differences are dominated by within-agent fluctuation. This is analogous in spirit to an intraclass signal, but the weekend implementation is a descriptive variance ratio rather than a validated reliability coefficient."),
              P("Why error correlation matters", PAPER_H2), PB("Accuracy alone can conceal epistemic dependence. Three agents may all be accurate on routine cases yet fail identically on the same minority hypothesis. Shared-error concentration is therefore interpreted inversely: high concentration suggests a common blind spot. A valuable population should ideally preserve alternative possibilities without sacrificing calibration or discriminating experiment choice."),
              P("What is deliberately excluded", PAPER_H2), PB("Primary analysis does not use embeddings, prose similarity or persona labels inferred from text. Those measures could be added as a secondary comparison to test whether linguistic distinctiveness exaggerates structured epistemic distinctiveness. The rationale field remains available for qualitative coding of assumptions and causal models after blind rubric development.")]

    story.append(PageBreak())
    story += heading("07", "Analysis plan and robustness", "The pilot prioritizes transparent descriptive evidence and uncertainty over a single headline score.")
    story += [P("Primary analysis", PAPER_H2),
              paper_bullet("Report trial counts and missingness for every condition-agent-mystery cell before calculating outcomes."),
              paper_bullet("Plot the four primary metrics side by side by condition; do not combine diversity and accuracy into one quality score."),
              paper_bullet("Show agent-level feature profiles and within-agent replicate differences, not only condition averages."),
              paper_bullet("Estimate uncertainty using a cluster bootstrap that resamples mysteries and candidate agents; with only three of each, label intervals as exploratory."),
              paper_bullet("Use exact permutation tests over agent labels within condition for the fingerprint statistic where exchangeability is defensible."),
              paper_bullet("Report effect sizes and raw counts; avoid treating p < .05 as a binary gate in this underpowered pilot."),
              P("Robustness checks", PAPER_H2)]
    robustness = dense_cards([
        ("R1", "Leave-one-task-out", "Recalculate fingerprints while excluding each mystery to detect task-specific effects.", BLUE),
        ("R2", "Feature decomposition", "Report confidence, breadth, information and correctness ratios separately.", CORAL),
        ("R3", "Score sensitivity", "Vary test-informativeness weights and verify whether qualitative rankings persist.", LIME),
        ("R4", "Error taxonomy", "Inspect whether concentrated errors reflect the same causal misconception.", BLUE),
        ("R5", "Style comparison", "Optionally compare text similarity with structured-choice similarity as a manipulation check.", CORAL),
        ("R6", "Protocol audit", "Repeat analyses excluding malformed, interrupted or non-independent trials.", LIME),
    ])
    story += [robustness, Spacer(1, 5 * mm), P("Decision logic", PAPER_H2)]
    logic = methods_table([
        [P("PATTERN", EYEBROW), P("SUPPORTED INFERENCE", EYEBROW), P("NOT SUPPORTED", EYEBROW)],
        [P("High fingerprint + stable task transfer", PAPER_SMALL), PB("Intervention produces repeatable epistemic differentiation under this protocol.", PAPER_SMALL), PB("Consciousness, welfare or metaphysical identity.", PAPER_SMALL)],
        [P("High diversity + low accuracy", PAPER_SMALL), PB("Broader exploration, possibly noisy.", PAPER_SMALL), PB("Improved collective intelligence.", PAPER_SMALL)],
        [P("Low diversity + high accuracy", PAPER_SMALL), PB("Convergence on keyed solutions.", PAPER_SMALL), PB("Robustness to distribution shift or rare hypotheses.", PAPER_SMALL)],
        [P("High shared-error concentration", PAPER_SMALL), PB("Correlated blind spots in the tested population.", PAPER_SMALL), PB("A shared internal representation or training cause without further evidence.", PAPER_SMALL)],
    ], [53 * mm, 64 * mm, 55 * mm])
    story += [logic, Spacer(1, 4 * mm), PB("If the pilot produces a promising signal, a preregistered follow-up should increase tasks and replicates, randomize presentation order, compare multiple foundation models and use hierarchical models with condition effects and agent-by-task interactions.", PAPER_SMALL)]

    story.append(PageBreak())
    story += heading("08", "Threats to validity and ethical interpretation")
    threats = methods_table([
        [P("THREAT", EYEBROW), P("WHY IT MATTERS", EYEBROW), P("MITIGATION / DISCLOSURE", EYEBROW)],
        [P("Model drift", PAPER_H3), PB("Subscription interfaces may silently change model versions or defaults.", PAPER_SMALL), PB("Record date, visible model label and interface; finish collection in a narrow time window.", PAPER_SMALL)],
        [P("Non-independent sampling", PAPER_H3), PB("Shared context, memory or cached material could mimic persistence.", PAPER_SMALL), PB("Use fresh chats, disable cross-chat memory where possible and never paste earlier outputs.", PAPER_SMALL)],
        [P("Demand characteristics", PAPER_H3), PB("Persona prompts directly announce desired reasoning styles.", PAPER_SMALL), PB("Measure structured choices; add blinded qualitative coding and later implicit interventions.", PAPER_SMALL)],
        [P("Task-key bias", PAPER_H3), PB("Researcher-authored mysteries may privilege one style of inference.", PAPER_SMALL), PB("Publish full stimuli and keys; invite independent auditing; add tasks from other authors.", PAPER_SMALL)],
        [P("Small task universe", PAPER_H3), PB("Three mysteries cannot establish domain-general identity.", PAPER_SMALL), PB("Describe findings as pilot-specific; test cross-domain transfer in follow-up work.", PAPER_SMALL)],
        [P("Anthropomorphic overreach", PAPER_H3), PB("The word fingerprint may imply a person-like essence.", PAPER_SMALL), PB("Define it as a protocol-relative behavioral profile and state interpretation boundaries repeatedly.", PAPER_SMALL)],
    ], [42 * mm, 65 * mm, 65 * mm])
    story += [threats, Spacer(1, 6 * mm), P("Ethical position", PAPER_H2), PB("Uncertainty cuts both ways in digital-mind research. Over-attribution can mistake role-play for morally significant states; under-attribution can ignore systems that matter. This study does not use self-reported suffering or induce distress-associated contexts. Its immediate ethical contribution is methodological humility: it makes one dimension of individuation measurable while explicitly refusing to treat behavioral differentiation as proof of experience."),
              P("Data and privacy", PAPER_H2), PB("The web instrument stores trial records locally in the researcher's browser. Data leave the device only through deliberate JSON export. No participant personal data are required. Raw model outputs may be published with model labels and timestamps, but any accidental personal information should be removed before release."),
              P("Limits of the term agent", PAPER_H2), PB("Candidate agent is used operationally for an intervention-defined stream of model behavior, not as a claim about agency in the philosophical or moral sense. N-01 and N-02, for example, are bookkeeping labels for repeated neutral instances. Persona and history labels similarly identify experimental conditions rather than ontological individuals."),
              compact_callout("Interpret carefully", "Behavioral individuality can inform individuation. It cannot, by itself, determine consciousness or moral patienthood.", colors.HexColor("#E8EAFD"), BLUE)]

    story.append(PageBreak())
    story += heading("09", "Discussion and research trajectory", "The weekend pilot is designed as the first rung of a longer empirical program on epistemic diversity in human-AI systems.")
    story += [P("Potential contribution to digital minds", PAPER_H2), PB("Digital-mind individuation is often approached through self-reference, preferences, continuity or architecture. Epistemic fingerprints add a population-level behavioral criterion: whether candidate minds contribute independently structured uncertainty and search behavior. The criterion is modest but useful. It can reveal when many apparent agents are functionally redundant for collective inquiry, and when contextual or persona interventions create stable specialization."),
              P("Potential contribution to AI safety and collective intelligence", PAPER_H2), PB("Correlated errors create systemic risk even when average performance is high. A panel of agents built from one model may produce the appearance of deliberation while repeatedly omitting the same hypothesis. Measuring shared-error concentration and hypothesis coverage can therefore complement accuracy benchmarks and ensemble voting. The long-term objective is not merely diverse outputs but populations that preserve minority possibilities, remain calibrated and reconnect claims to new observations and experiments."),
              dense_cards([
                  ("NEXT 1", "Model diversity", "Compare multiple foundation models and training lineages with persona diversity inside each model.", BLUE),
                  ("NEXT 2", "Human-AI populations", "Compare humans, homogeneous AI groups and heterogeneous mixed teams on the same discovery tasks.", CORAL),
                  ("NEXT 3", "Open-ended search", "Move from fixed candidate lists to novel hypothesis generation and quality-diversity evaluation.", LIME),
                  ("NEXT 4", "Reality contact", "Introduce new sensor data, experiments or adversarial observations that force belief revision.", BLUE),
                  ("NEXT 5", "Languages and cultures", "Test whether epistemic coverage changes across linguistic and cultural contexts.", CORAL),
                  ("NEXT 6", "Longitudinal identity", "Study persistent agents whose memory and experience accumulate over weeks rather than prompts.", LIME),
              ]), Spacer(1, 5 * mm), P("A broader framing", PAPER_H2), PB("The deeper question extends beyond AI. Scientific and cultural innovation may be ecological properties of populations rather than traits located solely inside individuals. Institutions need enough convergence to accumulate knowledge and enough variation to avoid premature closure. Generative AI makes this balance newly urgent because a small number of models can become shared cognitive infrastructure across domains. The appropriate target is therefore neither maximum novelty nor protectionism about human creativity. It is the design of knowledge ecosystems that explore widely, test rigorously and retain the capacity to surprise themselves."),
              compact_callout("Long-term question", "How does the composition of populations of human and artificial cognitive agents change the conceptual space that collective intelligence can explore?", colors.HexColor("#EAF6D5"), LIME)]

    story.append(PageBreak())
    story += heading("10", "Current status, open artifacts and references")
    story += [compact_callout("Status", "Protocol, web instrument and reproducible pipeline are complete. Empirical trials are not yet reported. The simulated dashboard exists only to test the interface.", colors.HexColor("#FCE1DA"), CORAL), Spacer(1, 5 * mm)]
    links = methods_table([
        [P("ARTIFACT", EYEBROW), P("LINK", EYEBROW), P("CONTENTS", EYEBROW)],
        [P("Live instrument", PAPER_H3), P("<link href='https://epistemic-fingerprints.nefinia.chatgpt.site'>epistemic-fingerprints.nefinia.chatgpt.site</link>", LINK), PB("Prompts, local trial recording and live descriptive dashboard.", PAPER_SMALL)],
        [P("Repository", PAPER_H3), P("<link href='https://github.com/nefinia/epistemic-fingerprints'>github.com/nefinia/epistemic-fingerprints</link>", LINK), PB("Protocol, source, Python pipeline, notebook and PDFs.", PAPER_SMALL)],
    ], [35 * mm, 70 * mm, 67 * mm])
    story += [links, Spacer(1, 5 * mm), P("References", PAPER_H2)]
    references = [
        "[1] Shumailov, I. et al. (2024). AI models collapse when trained on recursively generated data. <i>Nature</i>, 631, 755-759. <link href='https://doi.org/10.1038/s41586-024-07566-y'>doi:10.1038/s41586-024-07566-y</link>.",
        "[2] Hughes, E. et al. (2024). Position: Open-Endedness is Essential for Artificial Superhuman Intelligence. <i>Proceedings of ICML 2024</i>, PMLR 235. <link href='https://proceedings.mlr.press/v235/hughes24a.html'>proceedings.mlr.press/v235/hughes24a.html</link>.",
        "[3] Wright, D. et al. (2025; rev. 2026). Epistemic Diversity and Knowledge Collapse in Large Language Models. <link href='https://arxiv.org/abs/2510.04226'>arXiv:2510.04226</link>.",
        "[4] Hodel, D. &amp; West, J. D. (2025; rev. 2026). Epistemic diversity across language models mitigates knowledge collapse. <link href='https://arxiv.org/abs/2512.15011'>arXiv:2512.15011</link>.",
        "[5] de Rooij, A. &amp; Biskjaer, M. M. (2026). Generative AI Makes Creative Output More Homogeneous. Systematic review and meta-analysis. <link href='https://research.tilburguniversity.edu/en/publications/generative-ai-makes-creative-output-more-homogeneous/'>Tilburg University Research Portal</link>.",
        "[6] Ashkinaze, J., Mendelsohn, J., Li, Q., Budak, C. &amp; Gilbert, E. (2025). How AI Ideas Affect the Creativity, Diversity, and Evolution of Human Ideas: Evidence From a Large, Dynamic Experiment. <i>ACM Collective Intelligence 2025</i>. <link href='https://arxiv.org/abs/2401.13481'>arXiv:2401.13481</link>.",
        "[7] Longino, H. E. (1990). <i>Science as Social Knowledge: Values and Objectivity in Scientific Inquiry</i>. Princeton University Press.",
        "[8] Zollman, K. J. S. (2010). The epistemic benefit of transient diversity. <i>Erkenntnis</i>, 72, 17-35. <link href='https://doi.org/10.1007/s10670-009-9194-6'>doi:10.1007/s10670-009-9194-6</link>.",
        "[9] Stirling, A. (2007). A general framework for analysing diversity in science, technology and society. <i>Journal of the Royal Society Interface</i>, 4, 707-719. <link href='https://doi.org/10.1098/rsif.2007.0213'>doi:10.1098/rsif.2007.0213</link>.",
        "[10] Hong, L. &amp; Page, S. E. (2004). Groups of diverse problem solvers can outperform groups of high-ability problem solvers. <i>PNAS</i>, 101(46), 16385-16389. <link href='https://doi.org/10.1073/pnas.0403723101'>doi:10.1073/pnas.0403723101</link>.",
        "[11] Apart Research (2026). Digital Minds Research Sprint: Track 5 - The Assistant Persona &amp; Model Identity. <link href='https://apartresearch.com/sprints/digital-minds-research-sprint-2026-08-14-to-2026-08-16'>Sprint page</link>.",
    ]
    # Two-column reference block keeps the paper short and skimmable.
    left = [P(ref, REF_TIGHT) for ref in references[:6]]
    right = [P(ref, REF_TIGHT) for ref in references[6:]]
    refs = Table([[left, right]], colWidths=[84 * mm, 84 * mm])
    refs.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER", (0, 0), (0, 0), 0.5, LINE),
    ]))
    story += [refs, Spacer(1, 5 * mm), compact_callout("Open invitation", "Criticism, independent task design, replications and contributions are welcome. This pilot is intended as the first experiment in a longer interdisciplinary inquiry into epistemic diversity.", colors.HexColor("#EAF6D5"), LIME)]
    return story


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm,
        topMargin=21 * mm, bottomMargin=18 * mm,
        title="Epistemic Fingerprints: From apparent plurality to epistemic individuation in digital minds",
        author="Sofia Gallego",
        subject="Research paper for the Apart Research Digital Minds Research Sprint",
    )
    first_frame = Frame(19 * mm, 15 * mm, A4[0] - 38 * mm, A4[1] - 30 * mm, id="first")
    body_frame = Frame(19 * mm, 18 * mm, A4[0] - 38 * mm, A4[1] - 38 * mm, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[first_frame], onPage=first_page, autoNextPageTemplate="body"),
        PageTemplate(id="body", frames=[body_frame], onPage=later_page),
    ])
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    build()
