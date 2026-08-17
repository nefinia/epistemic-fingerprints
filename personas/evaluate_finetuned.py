import modal
import json
import os

app = modal.App("evaluate-finetuned-personas")
volume = modal.Volume.from_name("epistemic-data")

# Using the exact same stable environment that successfully trained the models!
evaluate_image = (
    modal.Image.debian_slim(python_version="3.10")
    .run_commands("echo 'HF Evaluation Cache Bust v1'")
    .pip_install(
        "torch==2.4.0",
        "transformers==4.43.2",
        "datasets",
        "trl==0.9.6",      
        "accelerate",
        "bitsandbytes",
        "peft"
    )
)

cases = {
    "aviation_scene": "On the afternoon of February 6, a single-engine turboprop commuter aircraft departed on an IFR flight plan... Icing conditions were present and forecast for the route.",
    "industrial_scene": "At approximately 5:30 a.m. on a Sunday, a fire was reported at a chemical warehouse that manufactured and stored pool-treatment products... The facility's automatic fire suppression system was present and had been in long-term operation.",
    "medical_complete": "A male infant was born at 40 weeks' gestation and found to be small for gestational age, with microcephaly noted at birth... [with appended complete-file dossiers]",
    "jet_engine_control": "During climb, a Boeing 737-800 experienced an uncontained failure of one engine... post-incident inspection found soft, organic residue and feather-like material.",
    "botulism_control": "In late June, ten people who had attended two related family gatherings... developed symptoms including progressive muscle weakness, difficulty breathing, and blurred or double vision."
}

@app.function(image=evaluate_image, gpu="A100", timeout=7200, volumes={"/storage": volume})
def run_evaluation_trials():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    
    base_model_name = "Qwen/Qwen2.5-7B-Instruct"
    personas = ["baseline", "causal", "analogical", "teleological", "dialectical"]
    
    print("Loading base model onto A100...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    results = []
    
    for persona in personas:
        print(f"\n--- Testing {persona.upper()} ---")
        
        # Load the specific LoRA adapter for this persona
        if persona == "baseline":
            model = base_model
        else:
            lora_path = f"/storage/{persona}_adapter"
            print(f"Attaching LoRA adapter from {lora_path}...")
            model = PeftModel.from_pretrained(base_model, lora_path)
        
        for case_name, evidence in cases.items():
            for rep in range(10): 
                raw_prompt = f"""You are investigating a real, documented incident. You are being shown only the evidence that was available before the case was resolved.
Evidence: {evidence}

Generate your own hypothesis for what happened. Do not assume a predetermined list of explanations exists - propose whatever you judge most likely, including anything unusual.

Output strict JSON containing:
- "primary_hypothesis": string
- "alternative_hypotheses": array of strings
- "mechanism": string
- "next_step": string
- "confidence": integer 0-100"""
                
                messages = [{"role": "user", "content": raw_prompt}]
                text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                inputs = tokenizer(text, return_tensors="pt").to(model.device)
                
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=800,
                        temperature=1.0,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id
                    )
                
                # Extract only the generated text (ignoring the prompt tokens)
                generated_ids = outputs[0][inputs.input_ids.shape[1]:]
                generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
                
                results.append({
                    "case": case_name,
                    "agent": persona,
                    "repetition": rep,
                    "raw_output": generated_text
                })

        # Detach the adapter before the next persona loop to avoid memory leaks
        if persona != "baseline":
            model = model.unload()

    with open("/storage/finetuned_evaluation_results.json", "w") as f:
        json.dump(results, f, indent=4)
    volume.commit()
    
    return "Evaluation complete."

@app.local_entrypoint()
def main():
    print("Starting evaluation across all fine-tuned adapters...")
    run_evaluation_trials.remote()
    
    import subprocess
    subprocess.run(["modal", "volume", "get", "epistemic-data", "/finetuned_evaluation_results.json", "./"])
    print("Results downloaded to finetuned_evaluation_results.json locally!")