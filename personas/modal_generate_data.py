import modal
import json
import os

app = modal.App("epistemic-data-generation")

# The clean, stable Hugging Face image
hf_image = (
    modal.Image.debian_slim(python_version="3.10")
    .run_commands("echo 'HF Fallback Cache Bust v1'")
    .pip_install("torch", "transformers", "accelerate")
)

personas = {
    "causal": "You are a Causal Mechanist. You ignore narrative and focus strictly on physical A-->B dependency paths, structural constraints, and mechanistic covariation. If an outcome violates physical laws, you assume mechanical interference, temporal violations, or measurement errors.",
    "analogical": "You are an Analogical Thinker. You solve abstract problems by mapping their relational structures to entirely different domains (e.g., biology, orbital mechanics, economics).",
    "teleological": "You are a Teleological Analyst operating strictly under the Task-Method-Knowledge (TMK) cognitive architecture. Explicitly decompose into: 1. TASK (The Why), 2. METHOD (The How), 3. KNOWLEDGE (The Constraints). Assume all anomalies are perfectly executed Methods designed to achieve an unstated Task.",
    "dialectical": "You are a Dialectical Thinker using the SIEV framework. You aggressively search for contradictions. Formulate the exact opposite for every piece of evidence, and output a synthesis that explains why two contradictory streams of evidence are simultaneously true."
}

domains = [
    "aerospace engineering", "distributed computing", "marine biology", 
    "chemical manufacturing", "cybersecurity", "quantum physics", "macroeconomics"
]

@app.function(image=hf_image, gpu="A100", timeout=3600)
def generate_synthetic_data(persona_name: str, sys_prompt: str, num_examples: int = 200):
    from transformers import pipeline
    import torch
    
    print(f"[{persona_name.upper()}] Loading Qwen-2.5-7B-Instruct via Transformers...")
    
    # Initialize the Hugging Face pipeline
    llm = pipeline(
        "text-generation", 
        model="Qwen/Qwen2.5-7B-Instruct", 
        device_map="auto",
        torch_dtype=torch.bfloat16
    )
    
    prompts = []
    for i in range(num_examples):
        domain = domains[i % len(domains)]
        raw_prompt = f"""Write a brief, highly technical mystery in the domain of {domain}. Then, provide the solution exactly as the following persona would, using their specific cognitive framework: {sys_prompt}
        
Format your output strictly as:
MYSTERY:
[text]
SOLUTION:
[text]"""
        
        # Format the prompt using Qwen's specific ChatML template
        messages = [{"role": "user", "content": raw_prompt}]
        formatted_prompt = llm.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        prompts.append(formatted_prompt)
        
    print(f"[{persona_name.upper()}] Running Hugging Face batch generation for {num_examples} examples...")
    
    # Generate text (equivalent to vLLM's llm.generate)
    outputs = llm(
        prompts, 
        max_new_tokens=1500, 
        temperature=0.8, 
        do_sample=True,
        return_full_text=False, # Ensures we only get the new text, not the prompt repeated
        batch_size=4 # Adjusts memory usage for the GPU
    )
    
    dataset = []
    for output in outputs:
        # Hugging Face returns a list containing a dict for each prompt
        raw_text = output[0]["generated_text"]
        parts = raw_text.split("SOLUTION:")
        
        if len(parts) == 2:
            mystery = parts[0].replace("MYSTERY:", "").strip()
            solution = parts[1].strip()
            
            chat_example = {
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": mystery},
                    {"role": "assistant", "content": solution}
                ]
            }
            dataset.append(chat_example)
            
    return dataset

@app.local_entrypoint()
def main():
    os.makedirs("data", exist_ok=True)
    print("🚀 Spawning Hugging Face GPU workers to generate data concurrently...")
    
    results = list(generate_synthetic_data.starmap([
        (name, prompt, 200) for name, prompt in personas.items()
    ]))
    
    for persona_name, dataset in zip(personas.keys(), results):
        file_path = f"data/{persona_name}_train.jsonl"
        with open(file_path, "w", encoding="utf-8") as f:
            for item in dataset:
                f.write(json.dumps(item) + "\n")
        print(f"✅ Saved {len(dataset)} examples to {file_path}")
        
    print("🎉 All synthetic data generated locally and ready for fine-tuning!")