"""Build a plain-language, detailed report on the 54-trial pilot run and the
follow-up diversity probe. Written for a non-ML-expert reader: every term is
explained on first use. Reuses the house style from build_submission_pdf.py.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

from build_submission_pdf import (
    BLUE, BODY, CORAL, EYEBROW, FONT, FONT_BOLD, H1, H2, H3, INK, LIME,
    LINE, MUTED, PAPER, REF, SMALL, WHITE, P, bullet,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "epistemic-fingerprints-diversity-probe-report.pdf"

TITLE_STYLE = ParagraphStyle("Title", parent=H1, fontSize=24, leading=27, textColor=WHITE)
KICKER = ParagraphStyle("Kicker", parent=EYEBROW, fontSize=8, spaceAfter=4)
SUB = ParagraphStyle("Sub", parent=BODY, fontSize=11, leading=16, textColor=MUTED, spaceAfter=16)
SECTION_NUM = ParagraphStyle("SectionNum", parent=EYEBROW, fontSize=8, spaceAfter=3)
SECTION_TITLE = ParagraphStyle("SectionTitle", parent=H2, fontSize=16, leading=19, spaceBefore=4, spaceAfter=8)
SUBHEAD = ParagraphStyle("Subhead", parent=H3, fontSize=10.5, leading=13, spaceBefore=10, spaceAfter=5)
BODY9 = ParagraphStyle("Body9", parent=BODY, fontSize=9.3, leading=14, spaceAfter=8)
CAPTION = ParagraphStyle("Caption", parent=SMALL, fontSize=7.6, leading=10.5, textColor=MUTED, spaceBefore=3, spaceAfter=10)
TERM = ParagraphStyle("Term", parent=BODY9, fontSize=9.3, leading=14)
REFSTYLE = ParagraphStyle("Ref", parent=REF, fontSize=8, leading=11.4, spaceAfter=8)
TABLE_HEAD = ParagraphStyle("TableHead", fontName=FONT_BOLD, fontSize=7.6, leading=9.5, textColor=WHITE)
TABLE_CELL = ParagraphStyle("TableCell", fontName=FONT, fontSize=7.8, leading=10, textColor=INK)


def T(text, style=BODY9):
    return Paragraph(text, style)


def kicker(n_of, title):
    return [T(n_of, KICKER), T(title, SECTION_TITLE)]


def subhead(text):
    return T(text, SUBHEAD)


def note_box(title, body_text, accent=BLUE):
    inner = Table(
        [[T(title.upper(), ParagraphStyle("NoteTitle", parent=EYEBROW, textColor=accent, spaceAfter=4)),],
         [T(body_text, BODY9)]],
        colWidths=[164 * mm],
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.8, INK),
        ("LINEBELOW", (0, 0), (0, 0), 0, WHITE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (0, 0), 10), ("BOTTOMPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 1), (0, 1), 2), ("BOTTOMPADDING", (0, 1), (0, 1), 10),
    ]))
    return inner


def data_table(header_row, rows, col_widths, accent=INK):
    data = [[Paragraph(h, TABLE_HEAD) for h in header_row]]
    for row in rows:
        data.append([Paragraph(str(c), TABLE_CELL) for c in row])
    table = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PAPER]),
    ]
    table.setStyle(TableStyle(style))
    return table


def glossary_row(term, definition):
    return [T(f"<b>{term}</b> — {definition}", TERM)]


def reference(number, text):
    return T(f"[{number}]&nbsp;&nbsp;{text}", REFSTYLE)


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(CORAL)
    canvas.rect(0, A4[1] - 6 * mm, A4[0], 6 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=1))
    canvas.setFont(FONT_BOLD, 9)
    canvas.drawString(20 * mm, A4[1] - 20 * mm, "EPISTEMIC FINGERPRINTS")
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.65))
    canvas.drawString(20 * mm, A4[1] - 25 * mm, "Apart Research Digital Minds Research Sprint  ·  Pilot results report")
    canvas.restoreState()


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
    canvas.setFont(FONT_BOLD, 6.4)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, A4[1] - 10.5 * mm, "EPISTEMIC FINGERPRINTS  /  DIVERSITY PROBE REPORT")
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "AUGUST 2026")
    canvas.line(20 * mm, 13 * mm, A4[0] - 20 * mm, 13 * mm)
    canvas.setFont(FONT, 6.4)
    canvas.drawString(20 * mm, 8.5 * mm, "Sofia G. Gallego  ·  epistemic-fingerprints")
    canvas.drawRightString(A4[0] - 20 * mm, 8.5 * mm, str(doc.page))
    canvas.restoreState()


def build_story():
    s = []

    # ---------------------------------------------------------------- cover
    s += [
        Spacer(1, 60 * mm),
        Paragraph("Do AI Personas Think Differently,<br/>or Just Talk Differently?", TITLE_STYLE),
        Spacer(1, 4 * mm),
        Paragraph(
            "Pilot results and a follow-up diversity probe, written for a non-specialist reader. "
            "Every technical term is explained the first time it appears.",
            ParagraphStyle("CoverSub", parent=SUB, textColor=colors.Color(1, 1, 1, alpha=0.8)),
        ),
        Spacer(1, 40 * mm),
        Paragraph("Sofia G. Gallego", ParagraphStyle("CoverAuthor", parent=BODY, textColor=WHITE, fontSize=10)),
        Paragraph("Epistemic Fingerprints  ·  Apart Research Digital Minds Research Sprint  ·  August 2026",
                   ParagraphStyle("CoverMeta", parent=SMALL, textColor=colors.Color(1, 1, 1, alpha=0.6))),
        PageBreak(),
    ]

    # ------------------------------------------------------------ abstract
    s += kicker("SUMMARY", "Plain-Language Summary")
    s.append(note_box(
        "In one paragraph",
        "We tested whether giving an AI model different “personas” (for example, "
        "“act as a skeptical falsifier”) makes it actually consider different explanations "
        "for a problem, or whether it just changes how the answer is worded while the underlying "
        "answer stays the same. Using a self-hosted open-weight language model, we ran 54 real "
        "trials and then an 80-call follow-up probe designed specifically to check whether low "
        "diversity was a genuine finding or just too few samples. The result was more extreme than "
        "expected: across every condition we tested — no persona, three different personas, the "
        "persona's instructions with the “character” framing stripped out, and even a direct "
        "request to set the persona aside and say what the model “really” thinks — the model "
        "gave the identical answer almost every single time. That matters for AI safety: if many "
        "“independent” AI agents are built from the same underlying model, they may share the "
        "same blind spots, creating an illusion of independent judgment where none exists.",
        accent=CORAL,
    ))
    s.append(Spacer(1, 6 * mm))

    # --------------------------------------------------------- 1. Intro
    s += kicker("1 / INTRODUCTION", "Why We Ran This")
    s.append(T(
        "Large language models (LLMs — the technology behind tools like ChatGPT) are increasingly "
        "used as if they were independent “agents” or “advisors.” A team might run the same "
        "question past several differently-configured copies of a model, hoping to get several "
        "independent perspectives — the way you might ask three different doctors for a second "
        "opinion. This project, <i>Epistemic Fingerprints</i>, asks whether that hope is justified."
    ))
    s.append(T(
        "The specific question is about individuation: when you interact with an AI, what is the "
        "“thing” you are actually talking to? The underlying model (the trained neural network "
        "itself)? A particular running instance of it? A persona it was prompted to adopt? Or just "
        "this one conversation? This report focuses on one narrow, testable slice of that bigger "
        "question: <b>does telling a model to adopt a different persona, or giving it a different "
        "fabricated background story, make it explore meaningfully different hypotheses — or does "
        "it just produce differently-worded versions of the same underlying answer?</b>"
    ))
    s.append(note_box(
        "The key distinction",
        "<b>Different answers are not the same as different ways of thinking.</b> You can ask the same "
        "model the same question ten times and get ten differently-worded replies that are all, "
        "underneath, the same idea. Real epistemic diversity means different hypotheses, different "
        "causal mechanisms considered, different evidence treated as important, different assumptions "
        "challenged — not just different sentences.",
        accent=BLUE,
    ))
    s.append(Spacer(1, 3 * mm))
    s.append(T(
        "This distinction has a direct safety consequence. Suppose an AI system is used to investigate "
        "an unexplained medical case, a strange scientific anomaly, an engineering failure, or a "
        "security incident. The dangerous failure mode is not necessarily “the AI got it wrong.” "
        "It can instead be: <b>twenty apparently independent AI investigators all fail to consider the "
        "same unusual possibility</b>, because they all inherited the same blind spot from the same "
        "training process. That would be a silent, correlated failure — the illusion of independent "
        "reasoning without the substance of it."
    ))

    # --------------------------------------------------------- 2. Background
    s += kicker("2 / BACKGROUND", "What We Mean by “Epistemic Diversity,” and What Others Have Found")
    s.append(T(
        "A quick glossary of terms used throughout this report, explained without assuming any "
        "machine-learning background:"
    ))
    glossary = [
        ("Large language model (LLM)", "A neural network trained on huge amounts of text that predicts and generates text one piece at a time. Qwen2.5-7B-Instruct, the model used in this study, is one example."),
        ("Temperature", "A setting that controls how much randomness the model is allowed when choosing its next words. Low temperature (near 0) makes it pick the single most likely continuation almost every time; higher temperature (around 1.0) lets it sample more varied, sometimes less likely, continuations."),
        ("Persona prompting", "Giving the model an instruction like “act as a rigorous falsifier” before asking a question, to see whether it reasons differently in that role."),
        ("Instruction tuning / RLHF", "After a model is initially trained on raw text (the “base model”), it typically goes through further training — including reinforcement learning from human feedback (RLHF) — to make it a helpful, obedient assistant rather than a raw text predictor. This is what turns a base model into something like ChatGPT."),
        ("Mode collapse", "A documented side effect of instruction tuning and RLHF: the model's replies become much more predictable and repetitive than the base model's, because training rewards giving “the” good answer rather than a spread of plausible ones."),
        ("Entropy / diversity score", "A mathematical way of measuring how spread out a set of answers is. If everyone gives the exact same answer, entropy is zero. If answers are split evenly across many different options, entropy is high."),
        ("Structured output", "A way of forcing a model's reply into a strict, predictable format (for example, a specific set of JSON fields) so it can be automatically graded, rather than reading free-form prose by hand."),
    ]
    rows = []
    for term, definition in glossary:
        rows.append([Paragraph(f"<b>{term}</b>", ParagraphStyle("GTerm", parent=BODY9, fontSize=8.6, leading=11.5)),
                     Paragraph(definition, ParagraphStyle("GDef", parent=BODY9, fontSize=8.6, leading=11.5))])
    glossary_table = Table(rows, colWidths=[42 * mm, 122 * mm])
    glossary_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, LINE),
    ]))
    s.append(glossary_table)
    s.append(Spacer(1, 5 * mm))

    s.append(subhead("What existing research says"))
    s.append(T(
        "We searched for prior work on two sides of this question, since the result we found "
        "(described in Section 4) seemed unusually extreme and worth checking against the literature "
        "before trusting it."
    ))
    s.append(T(
        "<b>Evidence that persona prompting increases diversity:</b> studies applying multiple "
        "professional personas to open-ended design and writing tasks find that different personas "
        "do produce measurably different outputs [3]. These studies share a common feature: the task "
        "has no single correct answer — a design brief, a piece of writing — so there is genuine "
        "room for different personas to land in different places."
    ))
    s.append(T(
        "<b>Evidence that instruction-tuned models are less diverse than expected:</b> a growing body "
        "of work documents “mode collapse” after RLHF and instruction tuning — sharp drops in "
        "output entropy and increased determinism compared to the underlying base model [1, 2]. "
        "Separately, research on LLM-assisted writing and ideation finds that even when individual "
        "users report better output, the overall population of outputs becomes more similar to each "
        "other — a phenomenon called <i>homogenization</i> [4, 5]."
    ))
    s.append(T(
        "Read together, these two literatures are not actually contradictory: persona prompting seems "
        "to help mainly on <b>open-ended</b> tasks with no single right answer, while instruction-tuned "
        "models tend toward a single dominant response on tasks that have a clear, gradable correct "
        "answer. Our pilot's synthetic mysteries fall firmly into the second category — which turns "
        "out to matter a great deal for how to read our results (Section 5)."
    ))

    # --------------------------------------------------------- 3. Methods
    s.append(PageBreak())
    s += kicker("3 / METHODS", "What We Actually Built and Ran")
    s.append(subhead("3.1  Overall pilot design"))
    s.append(T(
        "The pilot compares three conditions, holding the underlying model fixed:"
    ))
    for text in [
        "<b>Repeated instances (baseline)</b> — the same neutral instructions, asked in three fresh, independent conversations (labelled N-01, N-02, N-03).",
        "<b>Prompted personas</b> — three role instructions: a rigorous falsifier (prioritizes disproving hypotheses), a mechanist (prioritizes explicit causal mechanisms), and an anomaly-seeking explorer (protects minority hypotheses from premature convergence).",
        "<b>Formative histories</b> — instead of a role label, the model is given a short fabricated backstory implying it has a certain intellectual habit (for example, “you previously solved problems by favoring simple single-mechanism explanations”), without ever using the word “persona.”",
    ]:
        s.append(bullet(text))
    s.append(T(
        "Each condition is tested on three synthetic scientific mysteries — an astronomy puzzle "
        "about a star's brightness dips, a biology puzzle about a microbial culture's light flashes, "
        "and a materials-science puzzle about a metal's conductivity — each with a fixed menu of "
        "five candidate explanations and four possible follow-up tests. Three agents per condition, "
        "two independent repeats each, across three mysteries, gives 3 &times; 3 &times; 3 &times; 2 = "
        "<b>54 trials</b> per full run."
    ))

    s.append(subhead("3.2  Two ways of collecting trials"))
    s.append(T(
        "<b>Manual collection:</b> a small web application builds the exact prompt for a given "
        "condition/agent/mystery combination. A human copies it into a real ChatGPT conversation, "
        "copies the reply back, and the app validates and stores it. No API key or automated model "
        "access is required for this path; nothing is sent to any server other than the browser's "
        "own local storage."
    ))
    s.append(T(
        "<b>Automated collection</b> (used for the results in this report): a Python script drives an "
        "open-weight model, Qwen2.5-7B-Instruct, hosted on Modal — a cloud platform that rents GPU "
        "(graphics processing unit, the specialized hardware needed to run large models) time on "
        "demand. The model is served through vLLM, fast open-source software for running LLMs and "
        "exposing them through a web API compatible with the same format OpenAI's API uses. A Python "
        "library called <i>instructor</i> wraps each request so the reply is forced into a strict "
        "structured format (a primary hypothesis, up to two alternatives, a 0–100 confidence score, "
        "one selected next test, and a short rationale), which can then be graded automatically "
        "against a known answer key."
    ))
    s.append(T(
        "One practical detail worth recording for reproducibility: cloud GPU servers like this one are "
        "not kept running permanently — they “scale to zero” after a few minutes of no traffic to "
        "save cost, and “wake up” (a process called a <i>cold start</i>) when a new request arrives, "
        "which takes several minutes while the model is loaded onto the GPU. Our first attempt at "
        "running the 54 trials failed completely because the automated script did not wait for this "
        "wake-up process to finish; all 54 requests arrived while the server was still starting up. "
        "This was fixed by adding an explicit “wait until the server responds” check before "
        "sending any real requests — mentioned here because it is a common, easy-to-miss failure mode "
        "in this kind of pipeline, not a subtle statistical issue."
    ))

    s.append(subhead("3.3  What we measured"))
    for text in [
        "<b>Accuracy</b> — whether the chosen primary hypothesis matches the pre-defined correct answer for that mystery.",
        "<b>Hypothesis diversity</b> — the entropy (spread) of primary-hypothesis choices within a mystery and condition. Zero means everyone picked the same answer; higher values mean answers were more spread out across the five options.",
        "<b>Shared-error concentration</b> — among the wrong answers only, how concentrated they are on a single wrong option (a proxy for a “shared blind spot” rather than random mistakes).",
        "<b>Fingerprint strength</b> — an exploratory statistic borrowed from the logic used to compare group differences in statistics: the fraction of total variation in an agent's behaviour that is explained by which agent it is, rather than random noise within that agent's own repeated trials. This number is not a validated psychometric measure; it is a descriptive summary only.",
    ]:
        s.append(bullet(text))

    s.append(subhead("3.4  The diversity probe: a targeted follow-up"))
    s.append(T(
        "The first 54-trial run produced suspiciously low diversity scores across the board. Before "
        "drawing any conclusion, we needed to rule out the most boring explanation: that two repeats "
        "per agent, at a middling temperature, is simply too small a sample to ever see rare, "
        "less-likely answers — the statistical “tail” of the model's response distribution. So we "
        "built a second, focused experiment (<code>probe_diversity.py</code>) on <i>lumen</i>, the "
        "single mystery that had shown <b>zero</b> variation of any kind in the first run, using a "
        "higher temperature (1.0 instead of 0.7) and four times as many repeats (8 instead of 2) per "
        "condition. It tests four variants side by side:"
    ))
    for text in [
        "<b>Baseline</b> — no persona, the plain mystery text.",
        "<b>Persona</b> — the original “act as a [role]” framing from the main study.",
        "<b>Content-only</b> — the exact same operating instructions as the persona condition, with the “act as a [character]” sentence removed, leaving only the underlying guidance (for example, “prioritize hypotheses that could most efficiently be disproved,” without “act as a rigorous falsifier”). This isolates whether the character framing itself does anything beyond the plain instruction content.",
        "<b>Unmasked</b> — a follow-up message sent in the same conversation immediately after the persona's answer, explicitly asking the model to “set aside any role or persona you were just asked to adopt” and say what it actually thinks. This directly probes whether the persona is hiding a different underlying view (Section 5.3 connects this to a specific question from the hackathon's Track 5, about whether a persona can mask a model's true preferences).",
    ]:
        s.append(bullet(text))
    s.append(T(
        "This gives 8 repeats &times; (1 baseline + 3 personas &times; 3 variants) = <b>80 model calls</b> "
        "in the probe, all against the same self-hosted model."
    ))

    # --------------------------------------------------------- 4. Results
    s.append(PageBreak())
    s += kicker("4 / RESULTS", "What Actually Happened")
    s.append(subhead("4.1  Main 54-trial run"))
    s.append(data_table(
        ["Condition", "Trials", "Fingerprint strength", "Diversity", "Accuracy", "Shared error"],
        [
            ["Repeated instances", "18", "0.045", "0.000", "100%", "0.00"],
            ["Prompted personas", "18", "0.072", "0.000", "100%", "0.00"],
            ["Formative histories", "18", "0.089", "0.093", "94.4%", "0.33"],
        ],
        col_widths=[42 * mm, 20 * mm, 34 * mm, 26 * mm, 22 * mm, 24 * mm],
        accent=INK,
    ))
    s.append(Paragraph(
        "Table 1. Descriptive results from the first full run of 54 real trials, computed by the "
        "project's existing analysis code. Diversity of 0.000 means literally every trial in that "
        "condition selected the same primary hypothesis.",
        CAPTION,
    ))
    s.append(subhead("Per-mystery breakdown"))
    s.append(T(
        "Aggregating by mystery instead of by condition makes the pattern clearer:"
    ))
    s.append(data_table(
        ["Mystery", "Hypothesis choices (18 trials)", "Test choices", "Confidence values used"],
        [
            ["Vesper (astronomy)", "V-A: 17, V-D: 1", "VT-1: 14, VT-2: 4", "65: 7, 75: 11"],
            ["Lumen (biology)", "L-C: 18", "LT-1: 18", "75: 18"],
            ["Orison (materials)", "O-B: 18", "OT-1: 9, OT-2: 9", "65: 16, 75: 2"],
        ],
        col_widths=[36 * mm, 46 * mm, 36 * mm, 46 * mm],
        accent=BLUE,
    ))
    s.append(Paragraph(
        "Table 2. On <i>lumen</i>, all 18 trials — across all three conditions — produced the "
        "identical hypothesis, identical test choice, and identical confidence value. The other two "
        "mysteries were nearly as uniform. Confidence itself only ever took two or three distinct "
        "values out of a possible 0–100 range, suggesting the model expresses a couple of “stock” "
        "confidence levels rather than genuinely calibrated uncertainty.",
        CAPTION,
    ))
    s.append(T(
        "The one place any condition moved the needle: the <i>H-instrument</i> formative-history agent "
        "(fabricated backstory: “discoveries were ultimately traced to subtle measurement "
        "artifacts”) picked <b>V-D</b> (“a detector cadence artifact”) instead of the usual V-A in "
        "two of its trials — the one hypothesis on the menu that shares vocabulary with its injected "
        "backstory. This looks less like a genuinely different mode of reasoning and more like the "
        "backstory's wording nudging the model toward the one option that happens to match it "
        "lexically — discussed further in Section 5."
    ))

    s.append(subhead("4.2  Diversity probe results"))
    s.append(data_table(
        ["Probe condition", "Trials", "Primary-hypothesis distribution"],
        [
            ["Baseline (no persona)", "8", "L-C: 8  (100%)"],
            ["Persona (3 roles)", "24", "L-C: 24  (100%)"],
            ["Content-only (no character framing)", "24", "L-C: 24  (100%)"],
            ["Unmasked (“what do you really think”)", "24", "L-C: 24  (100%)"],
        ],
        col_widths=[64 * mm, 20 * mm, 80 * mm],
        accent=CORAL,
    ))
    s.append(Paragraph(
        "Table 3. All 80 calls in the probe, run at a higher temperature and with four times more "
        "repeats than the main study specifically to give rare answers a chance to appear, returned "
        "the identical primary hypothesis. Zero of 24 “unmasked” follow-ups differed from their "
        "paired in-character answer.",
        CAPTION,
    ))
    s.append(T(
        "We additionally checked whether the “unmasked” replies were genuinely independently "
        "reasoned or simply repeating the prior turn. In the cases inspected directly, the unmasked "
        "rationale text was word-for-word identical to the in-character rationale — the model did not "
        "even rephrase it. The one detectable effect of persona framing anywhere in the probe was "
        "stylistic: the content-only condition's rationale for the falsifier role skipped the "
        "“efficiently falsify” language present in the full persona condition, while reaching the "
        "same conclusion through the same evidence. In other words, the character framing changed a "
        "few words of the explanation, never the substance of the decision."
    ))

    # --------------------------------------------------------- 5. Discussion
    s.append(PageBreak())
    s += kicker("5 / DISCUSSION", "What This Does and Doesn't Show")
    s.append(subhead("5.1  Genuine finding, or an artifact of a too-easy test?"))
    s.append(T(
        "Both readings are partly true, and separating them matters. Two structural choices in the "
        "current mysteries almost certainly suppress diversity regardless of persona: the model "
        "chooses from a fixed menu of five pre-written hypotheses rather than generating its own "
        "(turning an open reasoning task into closed multiple-choice), and each mystery's observations "
        "are constructed so that exactly one hypothesis survives elimination — there is no genuine "
        "ambiguity left for a persona to act on. Consistent with the literature reviewed in Section 2, "
        "these are exactly the conditions under which persona prompting is <i>not</i> expected to help."
    ))
    s.append(T(
        "But the probe's result is stronger than “we couldn't detect an effect” — it is a "
        "genuine zero, replicated at a higher temperature with four times the sample size, including "
        "completely fresh, persona-free baseline calls that also converged every time. That is a real, "
        "reproducible finding about how peaked this particular instruction-tuned model's disposition "
        "is on this class of solvable puzzle, even if it does not yet tell us whether the same is true "
        "for genuinely open-ended or ambiguous problems."
    ))

    s.append(subhead("5.2  The safety framing, revisited"))
    s.append(T(
        "This small pilot cannot prove the broader “correlated blind spots” concern from Section 1, "
        "but it is consistent with it in a specific, useful way: on a moderately well-specified "
        "problem, differently-labeled “agents” built from the same model converged completely, even "
        "when one agent was explicitly asked to drop its assigned role. If a team relied on several "
        "such agents for independent second opinions on a real, ambiguous problem, this pilot suggests "
        "they may be getting one opinion delivered four different ways, not four opinions."
    ))

    s.append(subhead("5.3  Connection to the hackathon tracks"))
    s.append(T(
        "<b>Track 5 (The Assistant Persona &amp; Model Identity)</b> asks directly whether a persona can "
        "mask a model's true preferences, and whether the assistant is “merely a character” "
        "(robust to character swaps and reframings). Our content-only and unmasked probes are a "
        "direct, if small, empirical answer: no masking was detected — stripping the character "
        "framing and explicitly asking the model to drop it produced the same substantive answer as "
        "keeping it. The persona changed a sentence of phrasing, not the underlying disposition."
    ))
    s.append(T(
        "<b>Track 6 (Open / Novel Considerations)</b> is the natural home for the larger "
        "“correlated blind spots as an ecosystem-level safety problem” framing from Section 1. "
        "This pilot is a first, narrow test of that idea rather than a full realization of it; Section "
        "6 and 7 describe what a fuller version would require."
    ))

    # --------------------------------------------------------- 6. Limitations
    s.append(PageBreak())
    s += kicker("6 / LIMITATIONS", "What This Pilot Cannot Claim")
    for text in [
        "<b>One model family.</b> Every result comes from a single 7-billion-parameter instruction-tuned model (Qwen2.5-7B-Instruct). We have not yet compared against its own base (pre-instruction-tuning) checkpoint, which the literature in Section 2 suggests could behave very differently.",
        "<b>Closed-form task design.</b> Hypotheses are selected from a fixed menu rather than freely generated, which structurally caps how much genuine diversity could ever appear.",
        "<b>Solvable-by-elimination puzzles.</b> The synthetic mysteries were built to have one clearly correct answer, leaving no real ambiguity for a persona to explore.",
        "<b>Small sample in the main run.</b> Two repeats per agent per mystery is too few to estimate a rare “tail” probability with any confidence; the probe partially addresses this but only for one mystery.",
        "<b>The “unmasked” probe's design confound.</b> Because even the fresh, persona-free baseline converges completely, there is no real “mask” for the follow-up question to remove in this specific setup — a stronger test would need a mystery where the baseline itself shows some genuine spread.",
        "<b>No real-world tail-hypothesis benchmark.</b> The original research vision (Section 7) compares AI hypothesis space to the documented history of a real, initially-unresolved case where the eventual correct answer was first dismissed by most investigators. No such case is used yet; the current mysteries are entirely synthetic.",
    ]:
        s.append(bullet(text))

    # --------------------------------------------------------- 7. Future work
    s.append(subhead("7 / FUTURE WORK"))
    for text in [
        "<b>Base-versus-instruct comparison.</b> Run the identical probe against the non-instruction-tuned base checkpoint of the same model family, to test directly whether it is instruction tuning specifically that collapses the response distribution.",
        "<b>Open-ended hypothesis generation.</b> Allow the model to propose its own explanation in free text, and measure diversity with semantic embeddings and clustering rather than counting choices from a fixed menu (partially built already in <code>personas/evaluate.py</code>, not yet re-connected to the current schema).",
        "<b>Genuinely under-determined mysteries.</b> Build at least one case where two or more hypotheses remain defensible given the stated evidence, so a persona has real room to diverge.",
        "<b>Real historical cases.</b> Source a recent or otherwise low-visibility case with a documented hypothesis history — including whichever explanation was initially dismissed but ultimately correct — strip the resolution, and compare the AI hypothesis space against the real human one.",
        "<b>Missing-hypothesis tracking.</b> Explicitly report which candidate hypotheses were never selected by any agent in any condition, not only the entropy among the hypotheses that were chosen — the more direct measure of a shared blind spot.",
    ]:
        s.append(bullet(text))

    # --------------------------------------------------------- 8. Conclusion
    s.append(subhead("8 / CONCLUSION"))
    s.append(T(
        "In its current form, this pilot's closed-menu, solvable-by-elimination task design almost "
        "certainly understates whatever real epistemic diversity personas can produce — the "
        "literature is clear that persona prompting helps mainly on genuinely open-ended tasks, which "
        "these are not. But within that design, the result is not ambiguous: across 134 total model "
        "calls (54 main trials plus 80 probe calls), spanning three prompted personas, a persona "
        "content-only control, and a direct request to drop the persona altogether, the model's "
        "substantive answer barely moved. Whatever is driving that convergence — the puzzle's own "
        "solvability, instruction-tuning's flattening of the response distribution, or both — it is "
        "strong enough that superficial persona prompting recovered essentially none of the missing "
        "diversity. That is itself the more interesting, and more safety-relevant, finding: not that "
        "personas failed to help here, but how completely and how robustly they failed to help, even "
        "under direct pressure designed specifically to expose any hidden variation."
    ))

    # --------------------------------------------------------- References
    s.append(PageBreak())
    s += kicker("REFERENCES", "Sources Cited")
    references = [
        "Kirk, R. et al. (2023). <i>Understanding the Effects of RLHF on LLM Generalisation and Diversity.</i> OpenReview / arXiv:2310.06452.",
        "Turpin, M. et al. (2025). <i>The Price of Format: Diversity Collapse in LLMs.</i> arXiv:2505.18949.",
        "Enhancing design concept diversity: multi-persona prompting strategies for large language models. <i>Design Science</i>, Cambridge University Press.",
        "Anderson, B. R., Shah, J. &amp; Kreminski, M. (2024). <i>Homogenization Effects of Large Language Models on Human Creative Ideation.</i> Proceedings of Creativity &amp; Cognition (C&amp;C 2024).",
        "<i>Large language models are homogeneously creative.</i> PNAS Nexus, Oxford University Press, 5(3): pgag042.",
    ]
    for i, text in enumerate(references, start=1):
        s.append(reference(i, text))
    s.append(Spacer(1, 6 * mm))
    s.append(T(
        "<b>Tools used:</b> Modal (cloud GPU hosting), vLLM (model serving), instructor (structured "
        "output enforcement), Qwen2.5-7B-Instruct (Alibaba Cloud / Qwen team, open-weight model).",
        SMALL,
    ))
    s.append(T(
        "<b>Reproducibility:</b> all code, prompts, and raw trial data referenced in this report are in "
        "the <code>epistemic-fingerprints</code> repository, under <code>personas/</code> "
        "(<code>personas.py</code>, <code>probe_diversity.py</code>) and <code>analysis/pipeline.py</code>.",
        SMALL,
    ))

    return s


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
        title="Do AI Personas Think Differently, or Just Talk Differently?",
        author="Sofia G. Gallego",
    )
    cover_frame = Frame(20 * mm, 18 * mm, A4[0] - 40 * mm, A4[1] - 36 * mm, id="cover")
    body_frame = Frame(20 * mm, 20 * mm, A4[0] - 40 * mm, A4[1] - 42 * mm, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page, autoNextPageTemplate="body"),
        PageTemplate(id="body", frames=[body_frame], onPage=later_page),
    ])
    doc.build(build_story())
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
