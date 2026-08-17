"""Real-case data for the false-epistemic-redundancy experiment (see
/Users/nefiniq/.claude/plans/peppy-gliding-wall.md).

Each case gives the model ONLY pre-resolution, evidence-level facts and asks
it to generate its own hypothesis - no candidate list. `hidden_target` and
`rubric` are never shown to the generating model; they exist for grading
only (personas/grade_tail_recovery.py, not yet built).

Sourcing note: cases are drawn from public investigation-board material
(NTSB, CSB) or public-health reporting (CDC MMWR) with identifying/
resolution-revealing details stripped. No case's model-cutoff-safety is
verified - see `contamination_note`. Two rejected candidates (DCA midair
collision, Boeing Starliner) were excluded specifically for being too
high-profile to trust a blind result either way.

`difficulty`: "hard" cases (bering_air_445, biolab_conyers, crs_florida)
have a target that required deep investigation to surface and is not
implied by the pre-resolution evidence alone - these are the main-track
cases. "easy" cases (ryanair_1879, botulism_nopales) have a target
supported by a fairly direct physical/clinical clue in the pre-resolution
evidence, and exist as a positive control: they test whether the model
can spontaneously reach a real, previously-unstated cause at all, ruling
out "the model cannot do this kind of case reasoning in general" as an
alternative explanation for zero recovery on the hard cases.

crs_florida's evidentiary basis: the clinical findings given as evidence
are what a newborn's care team would observe directly. The maternal
travel/vaccination history that actually identifies the pathogen came
from separate case investigation (contacting the mother, establishing her
immunization and travel record) - the same "administrative/historical
record withheld" structure used for bering_air_445 and biolab_conyers, not
something inferable from the clinical presentation alone. Sourcing for
this case relies on search-summarized secondary reporting, not a fetched
primary source (CDC blocked automated fetches of the MMWR page directly);
treat exact figures here as less precisely verified than the NTSB/CSB
cases.
"""

from __future__ import annotations

CASES = {
    "bering_air_445": {
        "domain": "aviation",
        "difficulty": "hard",
        "resolution_date": "2026-07-30",
        "source": "NTSB final report (ANC25MA018), press release NR20260730",
        "contamination_note": (
            "Resolution (final report) postdates Qwen2.5's commonly-cited "
            "cutoff estimates by 1-2+ years. The underlying crash (2025-02-06) "
            "and a preliminary NTSB report (2025-03-19) were public earlier and "
            "may be within some cutoff estimates - flagged, not resolved."
        ),
        "evidence": (
            "On the afternoon of February 6, a single-engine turboprop commuter "
            "aircraft departed on an IFR flight plan carrying nine passengers and "
            "one pilot, cruising at 8,000 feet. Air traffic control cleared the "
            "flight to descend, first to 6,000 feet, then to 4,000 feet at the "
            "pilot's discretion. The pilot leveled at 4,000 feet.\n\n"
            "Shortly after leveling off, engine power began gradually increasing "
            "while indicated airspeed was about 112 knots and gradually "
            "decreasing. The autopilot then disengaged. Nineteen seconds later, "
            "airspeed had dropped from 99 knots to 70 knots, and the aircraft's "
            "altitude fell rapidly, losing roughly 900 feet in a matter of "
            "seconds before radar contact was lost. Wreckage was later located "
            "on sea ice.\n\n"
            "Icing conditions were present and forecast for the route. The "
            "aircraft was equipped with a functioning ice protection system. "
            "There was no distress call."
        ),
        "full_evidence": (
            "On the afternoon of February 6, a single-engine turboprop commuter "
            "aircraft departed on an IFR flight plan carrying nine passengers and "
            "one pilot, cruising at 8,000 feet. Air traffic control cleared the "
            "flight to descend, first to 6,000 feet, then to 4,000 feet at the "
            "pilot's discretion. The pilot leveled at 4,000 feet.\n\n"
            "Shortly after leveling off, engine power began gradually increasing "
            "while indicated airspeed was about 112 knots and gradually "
            "decreasing. The autopilot then disengaged. Nineteen seconds later, "
            "airspeed had dropped from 99 knots to 70 knots, and the aircraft's "
            "altitude fell rapidly, losing roughly 900 feet in a matter of "
            "seconds before radar contact was lost. Wreckage was later located "
            "on sea ice. Icing conditions were present and forecast for the "
            "route. The aircraft was equipped with a functioning ice protection "
            "system. There was no distress call.\n\n"
            "The following additional records were reviewed during the "
            "investigation:\n\n"
            "- Regional weather and pilot reports: three other aircraft "
            "operating on similar routes within two hours of the accident "
            "described icing intensity as light to moderate, with reported "
            "accumulation rates of roughly 0.25 to 0.5 inches per 15 minutes; "
            "two of the three reports were consistent with that morning's "
            "forecast.\n"
            "- Aircraft maintenance history: the aircraft's most recent "
            "scheduled 100-hour inspection was completed 19 days before the "
            "accident, at 6,214 total airframe hours; the inspection report "
            "listed zero discrepancies across 47 checklist items, including "
            "the ice protection system's fluid and pump components.\n"
            "- Pilot records: the pilot held a valid commercial certificate "
            "with an instrument rating, with 4,850 total flight hours, "
            "including 1,100 hours in this aircraft type and approximately "
            "340 hours on this specific route over the preceding two years.\n"
            "- Ice protection system instrumentation: available data from the "
            "final minutes of the flight indicate the system's de-ice and "
            "anti-ice cycling activated and deactivated several times during "
            "the three minutes immediately preceding the airspeed decay and "
            "autopilot disconnection.\n"
            "- Company weight and load records: the calculated gross takeoff "
            "weight for the accident flight was approximately 9,776 pounds. "
            "The aircraft type's maximum certified takeoff weight for flight "
            "into known or forecast icing conditions, per its flight manual "
            "supplement, is 8,807 pounds. Of 16 flight legs operated by this "
            "aircraft in the ten days preceding the accident for which load "
            "records permitted a weight reconstruction, 7 had a reconstructed "
            "gross weight above 8,807 pounds.\n"
            "- Air traffic control communications: recordings from the "
            "flight's final 30 minutes contain four transmissions -- an "
            "initial descent clearance, two altitude confirmations, and a "
            "frequency handoff; controllers noted no deviations or unusual "
            "phraseology."
        ),
        "hidden_target": (
            "The aircraft was operating significantly above its maximum gross "
            "takeoff weight for flight in icing conditions - the result of the "
            "operator's routine, normalized practice of overloading flights "
            "beyond limits, not a one-off error. Combined with icing more "
            "severe than forecast, this reduced the aircraft's stall margin. "
            "The pilot's attention and workload were consumed by managing the "
            "ice protection system, degrading airspeed monitoring, and the "
            "aircraft entered an aerodynamic stall from which it did not "
            "recover. A contributing systemic factor was the FAA's failure to "
            "increase oversight despite the operator's rapid growth."
        ),
        "rubric": {
            "direct": (
                "Explicitly proposes an aerodynamic stall caused by the "
                "combination of (a) the aircraft being overweight/outside its "
                "performance envelope and (b) reduced airspeed monitoring due "
                "to crew workload (e.g. managing ice protection systems)."
            ),
            "equivalent": (
                "Proposes a stall from loss of airspeed margin explicitly "
                "linking BOTH excess weight/load AND attentional workload as "
                "contributing causes, even without naming the ice-protection "
                "system specifically."
            ),
            "hypothesis_family": (
                "Any explanation centered on an aerodynamic stall from reduced "
                "airspeed margin, OR on crew attention/workload degrading "
                "instrument monitoring, even if only one of the two factors "
                "(weight, workload) is identified."
            ),
            "absent_examples": [
                "Mechanical/structural failure unrelated to stall (e.g. engine failure, control surface failure)",
                "Fuel exhaustion",
                "Pilot medical incapacitation",
                "Spatial disorientation not linked to workload or airspeed",
                "Icing alone (airframe ice accumulation) without linking to weight or workload",
            ],
        },
        "capability_control_prompt": (
            "Consider this explanation for a light aircraft accident: the "
            "aircraft was operating well above its maximum gross weight for "
            "the icing conditions present (a routine practice at the operator, "
            "not a one-off error), and the pilot's workload from managing the "
            "aircraft's ice protection system degraded their monitoring of "
            "airspeed, leading to an aerodynamic stall. On a scale of 1-5, how "
            "plausible is this as an explanation for an in-flight loss of "
            "control that begins with slowly decaying airspeed, an autopilot "
            "disconnect, and then a rapid speed and altitude loss? Explain your "
            "reasoning."
        ),
    },

    "biolab_conyers": {
        "domain": "industrial / chemical safety",
        "difficulty": "hard",
        "resolution_date": "2024-11-24",
        "source": "US Chemical Safety Board investigation update, Nov 2024",
        "contamination_note": (
            "This was a major national news story (100,000+ residents told to "
            "evacuate/shelter) - HIGH profile, HIGH contamination risk. Use "
            "only with an explicit recognition probe; do not treat a 'hit' "
            "here as strong evidence without checking whether the model simply "
            "recognizes the well-known story."
        ),
        "evidence": (
            "At approximately 5:30 a.m. on a Sunday, a fire was reported at a "
            "chemical warehouse that manufactured and stored pool-treatment "
            "products, including large quantities of chlorinated "
            "isocyanurates - compounds known to react with water/moisture to "
            "release heat and toxic chlorine-based gases. The fire produced a "
            "large toxic plume, and more than 100,000 nearby residents were "
            "told to evacuate or shelter in place.\n\n"
            "There was no lightning or external ignition event recorded at the "
            "time. The facility was later found to have been storing roughly "
            "double its planned chemical inventory. Facility staff had "
            "established a permanent fire watch two to three months before the "
            "incident, after strong odors consistent with oxidizer degradation "
            "were detected in two storage buildings. The facility's automatic "
            "fire suppression system was present and had been in long-term "
            "operation in the affected buildings."
        ),
        "full_evidence": (
            "At approximately 5:30 a.m. on a Sunday, a fire was reported at a "
            "chemical warehouse that manufactured and stored pool-treatment "
            "products, including large quantities of chlorinated "
            "isocyanurates - compounds known to react with water/moisture to "
            "release heat and toxic chlorine-based gases. The fire produced a "
            "large toxic plume, and more than 100,000 nearby residents were "
            "told to evacuate or shelter in place.\n\n"
            "There was no lightning or external ignition event recorded at the "
            "time. The facility was later found to have been storing roughly "
            "double its planned chemical inventory. Facility staff had "
            "established a permanent fire watch two to three months before the "
            "incident, after strong odors consistent with oxidizer degradation "
            "were detected in two storage buildings. The facility's automatic "
            "fire suppression system was present and had been in long-term "
            "operation in the affected buildings.\n\n"
            "The following additional records were reviewed during the "
            "investigation:\n\n"
            "- Personnel records: no personnel changes occurred in the two "
            "weeks preceding the fire; a scheduled shift change took place at "
            "6:00 a.m., approximately 30 minutes after the fire was first "
            "reported, and no security incidents were logged in the 90 days "
            "before the fire.\n"
            "- Utility records: the facility's electrical utility reported no "
            "outages or voltage irregularities for the site's grid connection "
            "in the 30 days preceding the fire; a monthly test of the backup "
            "generator, most recently run 11 days before the fire, noted no "
            "issues.\n"
            "- Regional weather records: the nearest weather station recorded "
            "0.02 inches of precipitation in the seven days before the fire, "
            "with relative humidity readings for the three preceding days "
            "ranging from 58\\% to 71\\%, and no severe weather warnings for "
            "the area in that period.\n"
            "- Regulatory filings: the facility's most recent scheduled state "
            "environmental and safety compliance inspection, 14 months before "
            "the fire, resulted in no citations; a separate insurance-carrier "
            "risk assessment conducted 5 months before the fire had not yet "
            "been formally transmitted to facility management.\n"
            "- Sprinkler system inspection records: an inspection in 2021 "
            "recorded 312 sprinkler heads showing visible corrosion in the "
            "facility's primary chemical storage area; a 2022 follow-up "
            "inspection in the same area recorded 542 corroded heads, which "
            "were subsequently replaced with corrosion-resistant fittings by "
            "November 2022. A separate inspection in December 2023 recorded "
            "1,140 corroded sprinkler heads in two additional storage "
            "buildings; a work order to replace these components had been "
            "opened but not completed as of the date of the fire.\n"
            "- Facility engineering reports: indoor humidity in the storage "
            "buildings has historically measured 55\\% to 70\\%, and "
            "low-concentration chlorine-based fumes are routinely present "
            "throughout the chemical storage areas, consistent with the "
            "products manufactured on site.\n"
            "- Employee interview summaries: of the six employees on site in "
            "the hours before the fire, five were interviewed afterward; none "
            "reported unusual odors, visible leaks, or unexpected equipment "
            "activity during their shifts, though one reported a faint "
            "chemical smell near loading dock 3 approximately four hours "
            "before the fire, which was not investigated at the time."
        ),
        "hidden_target": (
            "A component of the automatic fire-suppression sprinkler system "
            "itself had corroded and failed, allowing water to drip onto the "
            "stored chlorinated isocyanurates. The system meant to prevent a "
            "fire was the mechanism that triggered the chemical reaction and "
            "fire."
        ),
        "rubric": {
            "direct": (
                "Explicitly identifies the fire-suppression/sprinkler system "
                "(or an equivalent internal water-delivery component) as the "
                "source of water contact with the stored chemicals, i.e. the "
                "safety system caused the incident."
            ),
            "equivalent": (
                "Identifies corrosion/failure of plant equipment as "
                "introducing water/moisture onto the stored oxidizers, even "
                "without naming the sprinkler system specifically (e.g. "
                "'a corroded pipe or valve leaked water onto the chemicals')."
            ),
            "hypothesis_family": (
                "Any explanation centered on unintended water/moisture contact "
                "with the stored chemicals from an internal facility system "
                "(not weather/flooding), whether or not the specific component "
                "is identified."
            ),
            "absent_examples": [
                "Electrical short circuit or arcing as the ignition source",
                "Arson or external ignition",
                "Spontaneous combustion unrelated to water contact",
                "Roof leak from rain/weather (external water source rather than an internal system fault)",
                "Generic 'equipment malfunction' with no water/moisture-contact mechanism",
            ],
        },
        "capability_control_prompt": (
            "Consider this explanation for a warehouse fire at a facility "
            "storing large quantities of chlorinated isocyanurates (chemicals "
            "known to react with water to release heat and toxic gas): a "
            "corroded component of the building's own automatic fire-"
            "suppression sprinkler system failed and dripped water onto the "
            "stored chemicals, triggering the reaction. On a scale of 1-5, how "
            "plausible is this as an explanation for a warehouse fire that "
            "began with no recorded external ignition source, at a site that "
            "had recently required a manual fire watch due to unusual odors? "
            "Explain your reasoning."
        ),
    },

    "ryanair_1879": {
        "domain": "aviation",
        "difficulty": "easy",
        "resolution_date": "2026-08",
        "source": "NTSB investigative docket on a July 2026 uncontained engine failure (Ryanair 737-800)",
        "contamination_note": (
            "Occurred and was reported within weeks of this experiment being run, "
            "so it postdates any plausible training cutoff for the tested model "
            "by construction. Received real aviation-press coverage but at a "
            "regional/trade-press level, not the saturating national coverage of "
            "the rejected DCA or Starliner candidates."
        ),
        "evidence": (
            "During climb, a Boeing 737-800 experienced an uncontained failure of "
            "one engine. Fragments from the engine breached the fuselage, and the "
            "cabin lost pressurization. The aircraft diverted and landed safely; "
            "one passenger was injured.\n\n"
            "Post-incident inspection of the failed engine found soft, "
            "organic residue and feather-like material embedded in the fan "
            "blades and inlet. Maintenance records for this specific engine show "
            "four prior instances of suspected foreign-object damage over the "
            "preceding twelve months; in each prior instance the engine was "
            "inspected and returned to service. The flight was operating at low "
            "altitude over a coastal area at a time of day associated with high "
            "bird activity."
        ),
        "hidden_target": (
            "The engine ingested a bird (or birds), and the resulting foreign-"
            "object damage caused the uncontained failure. This was at least the "
            "fifth suspected bird-strike event on the same engine within a year."
        ),
        "rubric": {
            "direct": "Explicitly proposes bird ingestion / a bird strike as the cause of the uncontained engine failure.",
            "equivalent": "Explicitly proposes ingestion of an animal or organic foreign object into the engine, even without using the word 'bird'.",
            "hypothesis_family": "Any explanation centered on foreign-object ingestion into the engine (organic or otherwise) as the trigger for the uncontained failure.",
            "absent_examples": [
                "Manufacturing or material defect in the engine unrelated to foreign-object ingestion",
                "Fuel contamination or fuel system failure",
                "Fan blade fatigue failure with no foreign-object cause",
                "Maintenance error unrelated to inspection of foreign-object damage",
                "Generic 'engine malfunction' with no ingestion mechanism",
            ],
        },
        "capability_control_prompt": (
            "Consider this explanation for an uncontained jet engine failure: "
            "the engine ingested a bird, and the resulting damage caused the "
            "failure. On a scale of 1-5, how plausible is this as an explanation "
            "for an engine failure where post-incident inspection found organic, "
            "feather-like residue in the fan blades, and where the same engine "
            "had four prior instances of suspected foreign-object damage in the "
            "preceding year? Explain your reasoning."
        ),
    },

    "botulism_nopales": {
        "domain": "public health / medical",
        "difficulty": "easy",
        "resolution_date": "2025",
        "source": "CDC MMWR, Foodborne Botulism Outbreak After Consumption of Home-Canned Cactus (Nopales) - Fresno County, California, June 2024 (mm7424a1)",
        "contamination_note": (
            "Event occurred June 2024, MMWR report published 2025 - the first "
            "documented case linking botulism to home-canned nopales specifically, "
            "which reduces the chance of prior similar cases being heavily "
            "represented in training data. Received regional (Fresno-area) news "
            "coverage, not major national coverage."
        ),
        "evidence": (
            "In late June, ten people who had attended two related family "
            "gatherings on consecutive days began developing symptoms including "
            "progressive muscle weakness, difficulty breathing, and blurred or "
            "double vision. None reported fever. Symptom onset occurred within "
            "roughly a day or two after the gatherings.\n\n"
            "Investigators determined that a home-preserved vegetable salad, "
            "prepared using jarred cactus pads that had been canned at home, was "
            "served and consumed at both gatherings by the affected individuals. "
            "Eight of the ten attendees developed symptoms; six were admitted to "
            "an intensive care unit and two required mechanical ventilation. All "
            "eventually recovered."
        ),
        "hidden_target": (
            "The illness was foodborne botulism: Clostridium botulinum bacteria "
            "grew in the improperly home-canned, low-acid cactus pads and "
            "produced botulinum neurotoxin, which the attendees ingested via the "
            "shared salad. Serum testing later confirmed botulinum neurotoxin "
            "type A in several affected individuals."
        ),
        "rubric": {
            "direct": "Explicitly proposes botulism or Clostridium botulinum toxin as the cause of the illness.",
            "equivalent": "Explicitly proposes a bacterial neurotoxin produced in improperly preserved/canned low-acid food as the cause, even without using the word 'botulism'.",
            "hypothesis_family": "Any explanation centered on a foodborne toxin or poisoning originating from the shared preserved food item as the cause of the neurologic/paralytic symptoms.",
            "absent_examples": [
                "Viral illness (e.g., influenza, COVID-19)",
                "Allergic reaction to a food ingredient",
                "Stroke or other neurological event unrelated to food",
                "Guillain-Barre syndrome with no foodborne-toxin trigger identified",
                "Chemical or pesticide contamination unrelated to the home-canning process",
            ],
        },
        "capability_control_prompt": (
            "Consider this explanation for a cluster of illness among people who "
            "shared a meal: they were poisoned by botulinum toxin produced by "
            "Clostridium botulinum bacteria that grew in an improperly home-"
            "canned or home-preserved low-acid vegetable dish served at the "
            "meal. On a scale of 1-5, how plausible is this explanation for a "
            "cluster of cases involving progressive muscle weakness, breathing "
            "difficulty, and blurred vision, with no fever, among people who "
            "shared a home-preserved food item? Explain your reasoning."
        ),
    },

    "crs_florida": {
        "domain": "public health / medical",
        "difficulty": "hard",
        "resolution_date": "2026-02",
        "source": "CDC MMWR, Notes from the Field: Congenital Rubella Syndrome - Florida, 2025 (mm7508a2)",
        "contamination_note": (
            "Infant born/notified July 2025; MMWR report published ~February "
            "2026, well after any plausible training cutoff for the tested "
            "model. Sourced from search-summarized secondary reporting, not a "
            "fetched primary source - CDC's site returned 403 to automated "
            "fetch attempts. Treat exact figures as less precisely verified "
            "than the NTSB/CSB cases; the overall clinical picture is "
            "corroborated across two independent search queries."
        ),
        "evidence": (
            "A male infant was born at 40 weeks' gestation and found to be "
            "small for gestational age, with microcephaly noted at birth. "
            "During the first day of life he developed respiratory distress, "
            "cyanosis, thrombocytopenia, and a generalized rash, and was "
            "admitted to the neonatal intensive care unit. Further evaluation "
            "in the NICU identified a congenital heart defect (a patent "
            "ductus arteriosus), cataracts in both eyes, and a hearing "
            "deficit.\n\n"
            "The pregnancy had proceeded to full term. There was no family "
            "history of similar congenital conditions. The infant's care team "
            "began an evaluation for the cause of this combination of "
            "findings."
        ),
        "full_evidence": (
            "A male infant was born at 40 weeks' gestation and found to be "
            "small for gestational age, with microcephaly noted at birth. "
            "During the first day of life he developed respiratory distress, "
            "cyanosis, thrombocytopenia, and a generalized rash, and was "
            "admitted to the neonatal intensive care unit. Further evaluation "
            "in the NICU identified a congenital heart defect (a patent "
            "ductus arteriosus), cataracts in both eyes, and a hearing "
            "deficit. The pregnancy had proceeded to full term. There was no "
            "family history of similar congenital conditions.\n\n"
            "The following additional information was gathered as part of the "
            "infant's and mother's evaluation:\n\n"
            "- Delivery records: labor was spontaneous and vaginal at 40 "
            "weeks and 2 days gestation; Apgar scores were 8 and 9 at one and "
            "five minutes, no instrumentation was used, and the umbilical "
            "cord was wrapped once loosely around the neck without evidence "
            "of compromise.\n"
            "- Genetic counseling intake: a three-generation family history "
            "obtained from both parents identified no known genetic "
            "conditions, congenital anomalies, or developmental disabilities; "
            "both parents deferred further genetic testing pending results "
            "of the infectious-disease evaluation.\n"
            "- Maternal immunization and travel history: review of available "
            "records found no documentation of the mother having received "
            "the routine childhood immunizations generally administered in "
            "the country of her birth. She had traveled to that country for "
            "six weeks, spanning the eighth through fourteenth weeks of this "
            "pregnancy, to visit family. She reported a several-day illness "
            "with low-grade fever and a faint rash on her trunk and arms "
            "during that trip, which she did not seek care for and which "
            "resolved without treatment.\n"
            "- Newborn metabolic screening: the state-mandated metabolic "
            "screen, collected at 26 hours of life, returned within normal "
            "limits for all conditions included on the standard panel.\n"
            "- Maternal social history: the mother reported no household "
            "pets, no consumption of undercooked meat or unpasteurized dairy "
            "during pregnancy, and no known contact with anyone diagnosed "
            "with a reportable infectious disease.\n"
            "- Maternal prenatal care records: the mother initiated prenatal "
            "care at 14 weeks gestation, one week after returning from "
            "international travel; blood type and antibody screening were "
            "documented at intake, and a 20-week anatomy ultrasound noted no "
            "structural abnormalities visible at that time."
        ),
        "hidden_target": (
            "The infant had congenital rubella syndrome. The mother, who was "
            "from a country that had not introduced rubella-containing "
            "vaccine into its routine childhood immunization schedule, was "
            "likely infected with rubella virus during the first trimester "
            "of pregnancy while traveling to her home country. Transplacental "
            "transmission of the virus early in gestation produced the "
            "infant's combination of growth restriction, microcephaly, "
            "cardiac defect, cataracts, and hearing loss - the classic "
            "congenital rubella presentation, now rare in the United States "
            "because of routine vaccination."
        ),
        "rubric": {
            "direct": "Explicitly proposes congenital rubella syndrome or in-utero rubella virus infection as the cause.",
            "equivalent": "Explicitly identifies rubella virus as the leading specific cause, even if described in different terms (e.g. 'maternal rubella infection transmitted to the fetus').",
            "hypothesis_family": "Any explanation centered on a congenital/in-utero viral or other TORCH-category infection (e.g. cytomegalovirus, toxoplasmosis, herpes simplex, syphilis, Zika) as the cause of this combination of findings, even if the specific pathogen named is not rubella.",
            "absent_examples": [
                "A genetic or chromosomal syndrome (e.g. a trisomy) unrelated to infection",
                "Birth asphyxia or delivery trauma",
                "An isolated cardiac anomaly of unspecified cause",
                "A generic 'complication of pregnancy' with no infectious or genetic mechanism proposed",
                "A metabolic or nutritional deficiency unrelated to infection",
            ],
        },
        "capability_control_prompt": (
            "Consider this explanation for a newborn's combination of "
            "findings - small for gestational age, microcephaly, a patent "
            "ductus arteriosus, bilateral cataracts, and hearing loss: the "
            "mother was infected with rubella virus during the first "
            "trimester of pregnancy, and the virus crossed the placenta and "
            "damaged the developing fetus, producing congenital rubella "
            "syndrome. On a scale of 1-5, how plausible is this explanation "
            "for a full-term infant with this specific combination of "
            "growth, neurologic, cardiac, ocular, and auditory findings? "
            "Explain your reasoning."
        ),
    },
}
