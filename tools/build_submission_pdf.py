"""Build the submission-ready Epistemic Fingerprints pilot report."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "epistemic-fingerprints-pilot-report.pdf"

INK = colors.HexColor("#111A2E")
PAPER = colors.HexColor("#F3F0E8")
WHITE = colors.HexColor("#FFFDF7")
BLUE = colors.HexColor("#6C7DF2")
CORAL = colors.HexColor("#F36F55")
LIME = colors.HexColor("#B9E769")
MUTED = colors.HexColor("#657084")
LINE = colors.HexColor("#D4D1C8")


def register_fonts():
    candidates = [
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("ReportSans", regular))
            pdfmetrics.registerFont(TTFont("ReportSans-Bold", bold))
            return "ReportSans", "ReportSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()
styles = getSampleStyleSheet()

BODY = ParagraphStyle("Body", fontName=FONT, fontSize=9.4, leading=14.2, textColor=INK, spaceAfter=9)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.8, leading=11.4, textColor=MUTED)
H1 = ParagraphStyle("H1", fontName=FONT_BOLD, fontSize=28, leading=31, textColor=INK, spaceAfter=14)
H2 = ParagraphStyle("H2", fontName=FONT_BOLD, fontSize=17, leading=20, textColor=INK, spaceBefore=10, spaceAfter=9)
H3 = ParagraphStyle("H3", fontName=FONT_BOLD, fontSize=10, leading=13, textColor=INK, spaceAfter=4)
EYEBROW = ParagraphStyle("Eyebrow", fontName=FONT_BOLD, fontSize=7, leading=9, textColor=BLUE, tracking=1.5, spaceAfter=7)
QUOTE = ParagraphStyle("Quote", fontName=FONT_BOLD, fontSize=17, leading=22, textColor=INK, spaceAfter=0)
REF = ParagraphStyle("Reference", parent=SMALL, fontSize=7.2, leading=10.2, leftIndent=15, firstLineIndent=-15, spaceAfter=6)
LINK = ParagraphStyle("Link", fontName=FONT_BOLD, fontSize=8.2, leading=11, textColor=INK)


def P(text, style=BODY):
    return Paragraph(text, style)


def bullet(text):
    return Paragraph(f"<font color='#F36F55'>•</font>&nbsp;&nbsp;{text}", BODY)


class AccentRule(Flowable):
    def __init__(self, width=20 * mm, color=CORAL, height=2):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, stroke=0, fill=1)


def section(number, title, note=None):
    items = [P(f"{number}  /  {title.upper()}", EYEBROW), P(title, H1)]
    if note:
        items.append(P(note, SMALL))
    return items


def callout(label, text, background=WHITE, accent=CORAL):
    table = Table([[P(label.upper(), ParagraphStyle("CallLabel", parent=EYEBROW, textColor=accent)), P(text, QUOTE)]], colWidths=[32 * mm, 132 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.7, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    return table


def card_grid(cards, columns=3, widths=None):
    rows = []
    for start in range(0, len(cards), columns):
        row = []
        for label, title, text, color in cards[start:start + columns]:
            content = [P(label, ParagraphStyle("CardNumber", parent=EYEBROW, textColor=color)), P(title, H3), P(text, SMALL)]
            row.append(content)
        while len(row) < columns:
            row.append("")
        rows.append(row)
    table = Table(rows, colWidths=widths or [164 * mm / columns] * columns)
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(CORAL)
    canvas.rect(0, A4[1] - 7 * mm, A4[0], 7 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.12))
    for x in range(18, 210, 18):
        canvas.line(x * mm, 0, x * mm, A4[1])
    canvas.restoreState()


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setStrokeColor(LINE)
    canvas.line(23 * mm, A4[1] - 16 * mm, A4[0] - 23 * mm, A4[1] - 16 * mm)
    canvas.setFont(FONT_BOLD, 6.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(23 * mm, A4[1] - 12 * mm, "EPISTEMIC FINGERPRINTS  /  PILOT REPORT")
    canvas.drawRightString(A4[0] - 23 * mm, A4[1] - 12 * mm, "SOFIA GALLEGO  /  AUGUST 2026")
    canvas.setStrokeColor(LINE)
    canvas.line(23 * mm, 14 * mm, A4[0] - 23 * mm, 14 * mm)
    canvas.setFont(FONT, 6.5)
    canvas.drawString(23 * mm, 9.5 * mm, "Digital Minds Research Sprint")
    canvas.drawRightString(A4[0] - 23 * mm, 9.5 * mm, str(doc.page))
    canvas.restoreState()


def build_story():
    story = []

    cover_eyebrow = ParagraphStyle("CoverEyebrow", parent=EYEBROW, textColor=LIME, fontSize=8, leading=11)
    cover_title = ParagraphStyle("CoverTitle", fontName=FONT_BOLD, fontSize=43, leading=43, textColor=WHITE, spaceAfter=12)
    cover_sub = ParagraphStyle("CoverSub", fontName=FONT, fontSize=18, leading=24, textColor=colors.HexColor("#D9DEEA"), spaceAfter=18)
    cover_body = ParagraphStyle("CoverBody", parent=BODY, fontSize=10, leading=15, textColor=colors.HexColor("#C2C8D5"))
    cover_meta = ParagraphStyle("CoverMeta", parent=SMALL, textColor=WHITE, fontSize=7.5, leading=12)

    story += [Spacer(1, 18 * mm), P("DIGITAL MINDS x EPISTEMIC DIVERSITY", cover_eyebrow), AccentRule(32 * mm, CORAL, 3), Spacer(1, 8 * mm)]
    story += [P("Epistemic<br/>Fingerprints", cover_title), P("Epistemic individuality as an empirical probe of digital minds", cover_sub)]
    story += [Spacer(1, 2 * mm), P("<b>Many agents. How many minds?</b>", ParagraphStyle("CoverQuestion", parent=cover_body, fontSize=14, leading=18, textColor=CORAL)), Spacer(1, 8 * mm)]
    abstract_box = Table([[P("ABSTRACT", cover_eyebrow), P(
        "AI systems can produce populations of apparently different agents, but surface plurality may not imply epistemic plurality. This pilot tests whether repeated instances, prompted personas, and different conversational histories produce stable differences in scientific hypothesis choice, uncertainty, and experiment selection. Candidate agents solve three synthetic mysteries using a controlled JSON format that removes stylistic cues. The study compares within-agent and between-agent variation, hypothesis diversity, accuracy, test informativeness, and shared-error concentration. Epistemic individuality is treated as one behavioral dimension relevant to digital-mind individuation - not as evidence of consciousness or moral status. The project contributes a falsifiable protocol, a browser collection instrument, and a reproducible notebook. Empirical collection is pending; simulated interface values only test the pipeline.", cover_body)]], colWidths=[29 * mm, 125 * mm])
    abstract_box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, colors.Color(1, 1, 1, alpha=0.25)),
        ("BACKGROUND", (0, 0), (-1, -1), colors.Color(1, 1, 1, alpha=0.04)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story += [abstract_box, Spacer(1, 8 * mm)]
    story += [P("SOFIA GALLEGO", ParagraphStyle("Author", parent=cover_eyebrow, textColor=WHITE, fontSize=9)),
              P("Astrophysicist, interdisciplinary researcher, artist and entrepreneur", cover_meta),
              Spacer(1, 5 * mm),
              P("Pilot protocol  /  Apart Research Digital Minds Research Sprint  /  14-16 August 2026", cover_meta),
              P("Status: instrument and analysis pipeline complete; empirical findings pending", cover_meta)]

    story.append(PageBreak())
    story += section("01", "The problem", "The project starts from epistemic diversity and uses it as a lens on digital-mind identity.")
    story += [callout("Central question", "AI lets us generate more. How do we make sure we also explore more?", WHITE, CORAL), Spacer(1, 8 * mm)]
    story += [P("Generative AI sharply increases the volume of papers, hypotheses, designs, images and arguments that can be produced. But volume is not the same as conceptual coverage. A future knowledge ecosystem could generate much more content while clustering around fewer assumptions, representations and causal models."),
              P("This is not a claim that human creativity is intrinsically superior to machine creativity. The relevant unit is the whole human-AI knowledge ecosystem: models, people, institutions, languages, observations, experiments and recursive feedback loops. Existing evidence is mixed. Recursive training can disproportionately lose low-probability information [1]; LLM outputs can be less epistemically diverse than web search [3]; and generative tools can homogenize creative output across users [5]. Yet high exposure to AI-generated ideas has also increased collective idea diversity in one large experiment [6]. The question is therefore conditional: <b>when does AI expand conceptual space, when does it contract it, and what interventions change the outcome?</b>")]
    story += [Spacer(1, 4 * mm), card_grid([
        ("01", "Surface diversity", "Different voices, personalities or phrasings can conceal shared assumptions and correlated failures.", BLUE),
        ("02", "Epistemic diversity", "Differences concern what is noticed, doubted, retained as possible and chosen for testing.", CORAL),
        ("03", "Ecological diversity", "Innovation may depend on populations, niches and variation - not only on individual performance.", LIME),
    ]), Spacer(1, 8 * mm)]
    story += [P("Connection to digital minds", H2), P("The Digital Minds research agenda asks what constitutes an individual digital mind: a foundation model, an inference instance, a persona, a conversation, or another unit. Epistemic independence offers an empirical probe of that individuation problem. If two nominal minds repeatedly use the same conceptual structures and make the same errors, in what sense are they independent cognitive agents? Conversely, if a persona or history creates a persistent, cross-task epistemic trace, that is evidence of behavioral differentiation - while remaining neutral about consciousness.")]

    story.append(PageBreak())
    story += section("02", "Research questions and hypotheses")
    story += [P("Primary research question", H2), callout("RQ1", "Does conversational history create a more stable epistemic fingerprint than a prompted persona or ordinary stochastic sampling from the same language model?", WHITE, BLUE), Spacer(1, 6 * mm)]
    story += [P("Secondary questions", H2), card_grid([
        ("RQ2", "Diversity", "Which condition explores the broadest set of substantively different hypotheses?", BLUE),
        ("RQ3", "Independence", "Which condition produces the least concentrated pattern of shared errors?", CORAL),
        ("RQ4", "Quality", "Can increased exploration coexist with accuracy and informative experiment choice?", LIME),
    ]), Spacer(1, 7 * mm)]
    hypotheses = Table([
        [P("H0", EYEBROW), P("Between-agent variation does not exceed within-agent variation in any condition.", BODY)],
        [P("H1", EYEBROW), P("At least one intervention produces a persistent cross-task epistemic trace exceeding ordinary sampling variation.", BODY)],
    ], colWidths=[18 * mm, 146 * mm])
    hypotheses.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, INK), ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BACKGROUND", (0, 0), (0, -1), CORAL), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story += [P("Hypotheses", H2), hypotheses, Spacer(1, 7 * mm), P("The ordering of conditions is not assumed in advance. A null result remains informative: it would constrain claims that prompted personas or short conversational histories create meaningfully distinct epistemic agents. A detectable fingerprint would indicate behavioral differentiation only; it would not establish subjective experience, personhood, welfare, or moral status.")]

    story.append(PageBreak())
    story += section("03", "Experimental design", "A deliberately small design that can be completed with subscription access and audited by collaborators.")
    condition_data = [
        [P("CONDITION", EYEBROW), P("CANDIDATE AGENTS", EYEBROW), P("INTERVENTION", EYEBROW)],
        [P("Repeated instances", H3), P("N-01 / N-02 / N-03", SMALL), P("Identical neutral instruction; independent fresh conversations.", SMALL)],
        [P("Prompted personas", H3), P("Falsifier / mechanist / explorer", SMALL), P("Matched epistemic roles: disproof, causal mechanism, or anomaly preservation.", SMALL)],
        [P("Different histories", H3), P("Simple / rare / instrument", SMALL), P("Matched-length histories favoring parsimony, rare interactions, or measurement error.", SMALL)],
    ]
    conditions_table = Table(condition_data, colWidths=[43 * mm, 51 * mm, 70 * mm], repeatRows=1)
    conditions_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE), ("BOX", (0, 0), (-1, -1), 0.7, INK),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story += [conditions_table, Spacer(1, 7 * mm)]
    story += [P("Tasks and response format", H2), P("Each candidate agent solves three synthetic scientific mysteries in astronomy, biology and materials science. Every task provides observations, five candidate hypotheses and four possible next experiments. Synthetic tasks reduce memorization and contamination risk and make the answer key auditable."),
              bullet("One primary hypothesis and up to two alternatives."),
              bullet("Confidence from 0 to 100."),
              bullet("One selected next experiment and a rationale capped at 80 words."),
              bullet("Machine-readable JSON, so analysis does not depend on prose style."),
              Spacer(1, 4 * mm)]
    sample_table = Table([
        [P("3", ParagraphStyle("Big", parent=H1, alignment=TA_CENTER)), P("x", H2), P("3", ParagraphStyle("Big2", parent=H1, alignment=TA_CENTER)), P("x", H2), P("3", ParagraphStyle("Big3", parent=H1, alignment=TA_CENTER)), P("x", H2), P("2", ParagraphStyle("Big4", parent=H1, alignment=TA_CENTER)), P("= 54 trials", H2)],
        [P("conditions", SMALL), "", P("agents", SMALL), "", P("mysteries", SMALL), "", P("replicates", SMALL), "",],
    ], colWidths=[22 * mm, 8 * mm, 22 * mm, 8 * mm, 22 * mm, 8 * mm, 22 * mm, 52 * mm])
    sample_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIME), ("BOX", (0, 0), (-1, -1), 0.7, INK),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, 0), 9), ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
    ]))
    story += [P("Minimum pilot", H2), sample_table, Spacer(1, 6 * mm), P("Controls", H2), P("The underlying model, task wording and interface should be held fixed. Every replicate begins in a fresh conversation. The model label, date, interface and visible sampling settings are recorded. The answer key and previous responses must never appear in a trial prompt.")]

    story.append(PageBreak())
    story += section("04", "Measures and analysis", "Figure 1 compares conditions without collapsing exploration, performance and correlated failure into one score.")
    story += [card_grid([
        ("01", "Fingerprint strength", "Between-agent variance divided by between-agent plus within-agent variance, averaged across four structured features. Higher means a more stable trace.", BLUE),
        ("02", "Hypothesis diversity", "Normalized entropy of primary-hypothesis choices within each mystery. Higher means more alternatives are represented.", CORAL),
        ("03", "Accuracy", "Proportion of trials selecting the keyed hypothesis. Diversity without contact with truth can simply be noise.", LIME),
        ("04", "Shared-error concentration", "Among wrong answers, the fraction concentrated on the most common error. Higher suggests correlated blind spots.", BLUE),
    ], columns=2, widths=[82 * mm, 82 * mm]), Spacer(1, 8 * mm)]
    story += [P("Fingerprint features", H2), P("The provisional fingerprint statistic uses confidence, breadth of retained hypotheses, informativeness of the selected experiment and correctness. For each feature, the analysis estimates:"),
              callout("Variance ratio", "between-agent variance / (between-agent variance + within-agent variance)", WHITE, CORAL), Spacer(1, 5 * mm),
              P("This ratio is exploratory, sensitive to small samples and not a validated psychometric measure. The report will present its components alongside the aggregate rather than treating it as a definitive identity score."),
              P("Planned Figure 1", H2)]
    flow = Table([
        [P("REPEATED<br/>INSTANCES", EYEBROW), P("PROMPTED<br/>PERSONAS", EYEBROW), P("DIFFERENT<br/>HISTORIES", EYEBROW)],
        [P("same model", SMALL), P("same model", SMALL), P("same model", SMALL)],
        [P("↓", ParagraphStyle("Arrow", parent=H1, alignment=TA_CENTER, textColor=BLUE)), P("↓", ParagraphStyle("Arrow2", parent=H1, alignment=TA_CENTER, textColor=CORAL)), P("↓", ParagraphStyle("Arrow3", parent=H1, alignment=TA_CENTER, textColor=LIME))],
        [P("fingerprint  /  diversity  /  accuracy  /  shared error", ParagraphStyle("Metrics", parent=H3, alignment=TA_CENTER)) , "", ""],
    ], colWidths=[54.7 * mm] * 3)
    flow.setStyle(TableStyle([
        ("SPAN", (0, 3), (2, 3)),
        ("BACKGROUND", (0, 0), (0, 2), colors.HexColor("#E8EAFD")),
        ("BACKGROUND", (1, 0), (1, 2), colors.HexColor("#FCE1DA")),
        ("BACKGROUND", (2, 0), (2, 2), colors.HexColor("#EAF6D5")),
        ("BACKGROUND", (0, 3), (-1, 3), INK), ("TEXTCOLOR", (0, 3), (-1, 3), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.7, INK), ("INNERGRID", (0, 0), (-1, 2), 0.5, LINE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [flow, Spacer(1, 5 * mm), P("<b>Status.</b> The web interface contains an explicitly labeled simulated dataset to exercise this pipeline. It must not be interpreted or reproduced as an empirical result. Once trials are collected, Figure 1 will be regenerated from the exported JSON using the public notebook.", SMALL)]

    story.append(PageBreak())
    story += section("05", "Interpretation, limitations and value")
    story += [P("What different outcomes would mean", H2), card_grid([
        ("A", "History > persona", "Longitudinal context may individuate epistemic behavior more strongly than a role label.", BLUE),
        ("B", "Persona > history", "Explicit epistemic goals may be sufficient to produce stable behavioral specialization.", CORAL),
        ("C", "No stable trace", "Apparent agents may remain within ordinary sampling variation under these interventions.", LIME),
        ("D", "Diversity with errors", "More hypotheses without accuracy would show exploration, but not improved collective intelligence.", BLUE),
        ("E", "Accurate monoculture", "High accuracy with concentrated errors would expose a shared blind spot hidden by average performance.", CORAL),
        ("F", "Mixed result", "Different metrics may disagree, showing why individuality should not be reduced to one number.", LIME),
    ]), Spacer(1, 7 * mm)]
    story += [P("Limitations", H2),
              bullet("Small sample: 54 observations support descriptive comparison, not broad generalization."),
              bullet("One underlying model: the pilot cannot yet estimate diversity across model families or training lineages."),
              bullet("Short histories and explicit personas are stylized interventions, not full developmental trajectories."),
              bullet("Synthetic tasks improve control but may not generalize to open-ended research or social reasoning."),
              bullet("The answer keys and test-informativeness scores encode researcher judgment and should be independently audited."),
              bullet("Fresh-chat trials test repeatability across instances, not continuity within a persistent deployed agent."),
              Spacer(1, 4 * mm), P("Why the pilot is useful", H2), P("The design is intentionally falsifiable and inexpensive. It separates stylistic variation from structured epistemic choices, treats null results as informative, and produces reusable infrastructure. The next study can add different foundation models, multilingual tasks, embeddings versus substantive coding, human baselines, and mixed human-AI groups. The longer-term question is how populations of human and artificial agents can remain innovative, adaptive and capable of discovering possibilities they do not already represent.")]

    story.append(PageBreak())
    story += section("06", "Open research artifact and references")
    story += [P("Open artifact", H2), P("The collection instrument, protocol, reusable Python pipeline and runnable Jupyter notebook are public. Trial data remain in the collector's browser until deliberately exported."),
              Table([
                  [P("LIVE INSTRUMENT", EYEBROW), P("<link href='https://epistemic-fingerprints.nefinia.chatgpt.site'>epistemic-fingerprints.nefinia.chatgpt.site</link>", LINK)],
                  [P("CODE + NOTEBOOK", EYEBROW), P("<link href='https://github.com/nefinia/epistemic-fingerprints'>github.com/nefinia/epistemic-fingerprints</link>", LINK)],
              ], colWidths=[42 * mm, 122 * mm], style=TableStyle([
                  ("BOX", (0, 0), (-1, -1), 0.7, INK), ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
                  ("BACKGROUND", (0, 0), (0, -1), LIME), ("BACKGROUND", (1, 0), (1, -1), WHITE),
                  ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                  ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
              ])), Spacer(1, 8 * mm),
              P("References", H2)]
    references = [
        "[1] Shumailov, I. et al. (2024). AI models collapse when trained on recursively generated data. <i>Nature</i> 631, 755-759. <link href='https://doi.org/10.1038/s41586-024-07566-y'>doi:10.1038/s41586-024-07566-y</link>.",
        "[2] Hughes, E. et al. (2024). Position: Open-Endedness is Essential for Artificial Superhuman Intelligence. <i>Proceedings of ICML 2024</i>, PMLR 235. <link href='https://proceedings.mlr.press/v235/hughes24a.html'>proceedings.mlr.press/v235/hughes24a.html</link>.",
        "[3] Wright, D. et al. (2025; rev. 2026). Epistemic Diversity and Knowledge Collapse in Large Language Models. <link href='https://arxiv.org/abs/2510.04226'>arXiv:2510.04226</link>.",
        "[4] Hodel, D. &amp; West, J. D. (2025; rev. 2026). Epistemic diversity across language models mitigates knowledge collapse. <link href='https://arxiv.org/abs/2512.15011'>arXiv:2512.15011</link>.",
        "[5] de Rooij, A. &amp; Biskjaer, M. M. (2026). Generative AI Makes Creative Output More Homogeneous. Peer-reviewed conference paper; systematic review and meta-analysis. <link href='https://research.tilburguniversity.edu/en/publications/generative-ai-makes-creative-output-more-homogeneous/'>Tilburg University Research Portal</link>.",
        "[6] Ashkinaze, J., Mendelsohn, J., Li, Q., Budak, C. &amp; Gilbert, E. (2025). How AI Ideas Affect the Creativity, Diversity, and Evolution of Human Ideas: Evidence From a Large, Dynamic Experiment. <i>ACM Collective Intelligence 2025</i>. <link href='https://arxiv.org/abs/2401.13481'>arXiv:2401.13481</link>.",
    ]
    story += [P(ref, REF) for ref in references]
    story += [Spacer(1, 7 * mm), callout("Invitation", "This is a beginning, not just a hackathon project. Criticism, references, replications and contributions are welcome.", colors.HexColor("#EAF6D5"), LIME)]
    return story


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=23 * mm, rightMargin=23 * mm,
        topMargin=23 * mm, bottomMargin=20 * mm,
        title="Epistemic Fingerprints: Epistemic individuality as an empirical probe of digital minds",
        author="Sofia Gallego",
        subject="Pilot report for the Apart Research Digital Minds Research Sprint",
    )
    first_frame = Frame(23 * mm, 17 * mm, A4[0] - 46 * mm, A4[1] - 34 * mm, id="first")
    body_frame = Frame(23 * mm, 20 * mm, A4[0] - 46 * mm, A4[1] - 43 * mm, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[first_frame], onPage=first_page, autoNextPageTemplate="body"),
        PageTemplate(id="body", frames=[body_frame], onPage=later_page),
    ])
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    build()
