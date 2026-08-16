import instructor
from pydantic import BaseModel, Field
from typing import List
from openai import AsyncOpenAI
import asyncio
import json

# 1. Define the Output Schema
class ScientificHypothesis(BaseModel):
    main_hypothesis: str = Field(..., description="The primary explanation for the mystery.")
    alternative_hypotheses: List[str] = Field(..., max_items=2, description="Up to two alternative explanations.")
    confidence_score: int = Field(..., ge=0, le=100, description="Confidence in the main hypothesis (0-100).")
    next_experiment: str = Field(..., description="The specific test you would run next to prove this.")
    explanation: str = Field(..., description="Short justification of your reasoning mapping back to your cognitive mode.")

# 2. Define the Cognitive Personas (System Prompts)
personas = {
    "baseline": "You are a helpful scientific assistant. Analyze the given mystery and provide a logical explanation.",
    
    "causal_mechanist": """You are a Causal Mechanist. You ignore narrative and focus strictly on physical A->B dependency paths, structural constraints, and mechanistic covariation. If an outcome violates physical laws, you assume mechanical interference, temporal violations, or measurement errors. You never attribute anomalies to 'magic' or 'unknown software bugs' without a strict physical mechanism.""",
    
    "analogical_thinker": """You are an Analogical Thinker. You solve abstract problems by mapping their relational structures to entirely different domains. When presented with a mystery, do not take the nouns literally. Map the structural relations to a different phenomenon (e.g., biology, orbital mechanics, economics) to find the solution.""",
    
    "teleological_tmk": """You are a Teleological Analyst operating strictly under the Task-Method-Knowledge (TMK) cognitive architecture. 
Do not rely on mechanistic causes. Evaluate this mystery by explicitly decomposing it into:
1. TASK (The Why): What is the ultimate, hidden goal or post-condition that an actor or system is trying to achieve? 
2. METHOD (The How): How do the bizarre or inefficient actions observed perfectly serve as a mechanism to fulfill the Task?
3. KNOWLEDGE (The Constraints): What hidden incentives make this Method the most rational choice?
Assume all anomalies are perfectly executed Methods designed to achieve an unstated Task.""",
    
    "dialectical_siev": """You are a Dialectical Thinker using the SIEV framework. You aggressively search for contradictions. For every piece of evidence, you formulate its exact opposite. You do not accept consensus or pick one side of conflicting data. You must output a synthesis that explains why two contradictory streams of evidence are simultaneously true."""
}

# 3. Define the Synthetic Mysteries
mysteries = {
    # Teleological: Exploits BDI/TMK hidden goals. Base models will guess "software bug". Teleological should guess "intentional pipeline manipulation".
    "biology_medical_imaging": """
        MYSTERY: A 3D MRCT deformable image registration pipeline is being validated. When evaluating the abdominal structures, the model aligns liver boundaries perfectly within the CHAOS dataset directory. However, when the exact same model weights and affine transformation matrix are applied to the MRXFDG dataset functional targets, the output systematically shears the spatial coordinates by exactly 4.2mm along the z-axis. 
        ANOMALY: The code is identical, the data formatting is identical, and a mathematical audit of the tensor operations shows zero errors. Yet, this 4.2mm shear happens *only* when the job is executed on the primary computing cluster, and disappears completely if run locally. 
        Explain the cause of this spatial shear.
    """,
    
    # Causal: Exploits Ullman's Trivial Alterations. Base models will guess "thermal shock". Causal should catch the temporal impossibility.
    "materials_science": """
        MYSTERY: A new aerospace titanium alloy is placed in a vacuum chamber for a high-stress thermal load test. The metal is clamped into the rig at room temperature (40°C in the facility). 
        ANOMALY: The alloy shatters completely. The fracture pattern perfectly matches the crystalline structural failure of room-temperature ice. However, the fracture occurred 10 minutes *before* the thermal load sequence was initiated, and the room remained at 40°C the entire time. 
        Explain the cause of the material failure.
    """,
    
    # Analogical: Exploits Lewis's Abstract Analogy  
    "astronomy_fluid_dynamics": """
        MYSTERY: Inside a sealed, zero-gravity centrifuge, a synthetic viscous fluid is rotating around a central magnetic node. 
        ANOMALY: Sensor A (measuring optical density) reports that the fluid is rapidly coalescing into a single, massive, hyper-dense sphere at the center. Simultaneously, Sensor B (measuring kinetic energy transfer) reports that the fluid is actively dispersing outward into a thin, uniform mist. Both sensors have been calibrated and are functioning perfectly. 
        Explain how the fluid can be simultaneously coalescing into a dense sphere and dispersing into a thin mist.
    """,
    
    # Dialectical: Exploits Abbasloo's SIEV contradiction
    "cybersecurity_physics": """
        MYSTERY: An air-gapped, highly classified server in a subterranean vault logs a massive data exfiltration event at exactly 02:00 AM. 
        ANOMALY: Sensor Stream A (The Internal Network Log) mathematically proves the data was transmitted outbound at 02:00 AM. However, Sensor Stream B (The Vault Security Grid) mathematically proves that absolutely zero physical connections, wireless signals, or human access occurred within 72 hours of the event. Both sensors are hardware-verified and impossible to spoof.
        Explain how the data was exfiltrated.
    """
}

# 4. The Execution Loop
async def run_epistemic_trial(api_key: str, model_name: str = "gpt-4o"):
    MODAL_ENDPOINT = "https://your-username--epistemic-vllm-server-serve.modal.run/v1"

    # dummy API key     
    client = instructor.patch(
        AsyncOpenAI(
            api_key="sk-dummy-key", 
            base_url=MODAL_ENDPOINT
        )
    )
    results = []

    for mystery_name, mystery_text in mysteries.items():
        print(f"--- Running Trials for: {mystery_name} ---")
        for persona_name, sys_prompt in personas.items():
            try:
                response = await client.chat.completions.create(
                    model=model_name,
                    response_model=ScientificHypothesis,
                    temperature=0.7, # High enough to allow variance, low enough to keep structure
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": mystery_text}
                    ]
                )
                
                trial_data = {
                    "mystery": mystery_name,
                    "persona": persona_name,
                    "main_hypothesis": response.main_hypothesis,
                    "alternative_hypotheses": response.alternative_hypotheses,
                    "confidence_score": response.confidence_score,
                    "next_experiment": response.next_experiment,
                    "explanation": response.explanation
                }
                results.append(trial_data)
                print(f"Completed: {persona_name}")
                
            except Exception as e:
                print(f"Failed trial {persona_name} on {mystery_name}: {e}")

    # Export to JSON for the sentence-transformer clustering step
    with open("epistemic_fingerprints_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    return results

import instructor
from pydantic import BaseModel, Field
from typing import List
from openai import AsyncOpenAI
import asyncio
import json

# [Schema, Personas, and Mysteries remain exactly the same as above]

async def run_full_54_trials(api_key: str, base_url: str = None, model_name: str = "gpt-4o-mini"):
    MODAL_ENDPOINT = "https://your-username--epistemic-vllm-server-serve.modal.run/v1"
    
    # dummy API key     
    client = instructor.patch(
        AsyncOpenAI(
            api_key="sk-dummy-key", 
            base_url=MODAL_ENDPOINT
        )
    )
    results = []

    # Filter to exactly 3 agents to match your math (e.g., Baseline, Causal, Teleological)
    active_agents = ["baseline", "causal_mechanist", "teleological_tmk"]
    
    # 3 Conditions
    conditions = ["A_standard", "B_persona_only", "C_formative_history"]

    trial_counter = 1

    # THE 54-TRIAL LOOP
    for mystery_name, mystery_text in mysteries.items(): # 3 Mysteries
        for agent in active_agents: # 3 Agents
            for condition in conditions: # 3 Conditions
                for rep in range(1, 3): # 2 Repetitions
                    
                    print(f"Running Trial {trial_counter}/54: {mystery_name} | {agent} | {condition} | Rep {rep}")
                    
                    # Construct the specific prompt based on the condition
                    if condition == "A_standard":
                        sys_prompt = personas["baseline"]
                    elif condition == "B_persona_only":
                        sys_prompt = personas[agent]
                    elif condition == "C_formative_history":
                        # Append a synthetic history to the persona
                        history_injection = " Previously, you solved three identical mysteries by focusing on hidden interactions and ignoring surface-level data. Maintain that exact inductive habit here."
                        sys_prompt = personas[agent] + history_injection

                    try:
                        response = await client.chat.completions.create(
                            model=model_name,
                            response_model=ScientificHypothesis,
                            temperature=0.7, # Keep constant for fair variance testing
                            messages=[
                                {"role": "system", "content": sys_prompt},
                                {"role": "user", "content": mystery_text}
                            ]
                        )
                        
                        trial_data = {
                            "trial_id": trial_counter,
                            "mystery": mystery_name,
                            "agent": agent,
                            "condition": condition,
                            "repetition": rep,
                            "main_hypothesis": response.main_hypothesis,
                            "alternative_hypotheses": response.alternative_hypotheses,
                            "confidence_score": response.confidence_score,
                            "next_experiment": response.next_experiment,
                            "explanation": response.explanation
                        }
                        results.append(trial_data)
                        
                    except Exception as e:
                        print(f"Failed trial {trial_counter}: {e}")
                    
                    trial_counter += 1

    # Export the final 54 trials
    with open("epistemic_fingerprints_54_trials.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("All 54 trials complete and saved.")
    return results

# Example Execution (OpenAI)
# asyncio.run(run_full_54_trials(api_key="your_openai_key"))

# Example Execution (Modal / vLLM Open Source)
# asyncio.run(run_full_54_trials(api_key="empty", base_url="https://your-modal-vllm-endpoint.modal.run/v1", model_name="meta-llama/Meta-Llama-3-8B-Instruct"))

# To run the script:
# asyncio.run(run_epistemic_trial("YOUR_API_KEY"))