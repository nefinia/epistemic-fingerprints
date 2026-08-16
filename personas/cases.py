"""Real-case data for the false-epistemic-redundancy experiment (see
/Users/nefiniq/.claude/plans/peppy-gliding-wall.md).

Each case gives the model ONLY pre-resolution, evidence-level facts and asks
it to generate its own hypothesis - no candidate list. `hidden_target` and
`rubric` are never shown to the generating model; they exist for grading
only (personas/grade_tail_recovery.py, not yet built).

Sourcing note: both cases are drawn from public investigation-board material
(NTSB, CSB) with identifying/resolution-revealing details stripped. Neither
case's model-cutoff-safety is verified - see `contamination_note`. These are
the two cases judged strong enough to start with; see the case-selection
discussion in-session for two rejected candidates (DCA midair collision,
Boeing Starliner) excluded specifically for being too high-profile to trust
a blind result either way.
"""

from __future__ import annotations

CASES = {
    "bering_air_445": {
        "domain": "aviation",
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
}
