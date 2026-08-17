import modal
import json
import re
import csv

app = modal.App("calculate-diversity")

# A clean environment specifically for the embedding model
evaluate_image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "sentence-transformers", 
        "numpy<2", 
        "scipy", 
        "torch>=2.5.0"
    )
)

@app.function(image=evaluate_image)
def compute_diversity_remote(results):
    from sentence_transformers import SentenceTransformer
    from scipy.spatial.distance import pdist
    import numpy as np
    
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    grouped_data = {}
    for entry in results:
        case = entry['case']
        agent = entry['agent']
        raw_output = entry['raw_output'].strip()
        
        # Strip potential markdown formatting if the model wrapped its JSON output
        cleaned_output = re.sub(r'^```(?:json)?\s*', '', raw_output)
        cleaned_output = re.sub(r'\s*```$', '', cleaned_output)
        
        try:
            parsed_json = json.loads(cleaned_output)
            primary_hyp = parsed_json.get('primary_hypothesis', '')
            mechanism = parsed_json.get('mechanism', '')
            text_to_embed = f"{primary_hyp} {mechanism}".strip()
            
            if not text_to_embed:
                continue

            key = (case, agent)
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(text_to_embed)
            
        except Exception:
            pass

    # Process and package the metrics instead of just printing them
    final_metrics = []
    for case, agent in sorted(grouped_data.keys()):
        texts = grouped_data[(case, agent)]
        if len(texts) < 2:
            final_metrics.append({
                "Case": case, 
                "Agent Condition": agent, 
                "Diversity (Mean Distance)": None, 
                "Valid": len(texts)
            })
            continue
            
        embeddings = model.encode(texts)
        distances = pdist(embeddings, metric='cosine')
        mean_distance = np.mean(distances)
        
        final_metrics.append({
            "Case": case,
            "Agent Condition": agent,
            "Diversity (Mean Distance)": round(float(mean_distance), 4),
            "Valid": len(texts)
        })
        
    return final_metrics

@app.local_entrypoint()
def main():
    print("Loading local evaluation results...")
    try:
        with open('finetuned_evaluation_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("Error: 'finetuned_evaluation_results.json' not found. Run the evaluation script first!")
        return
        
    print("Offloading diversity calculation to Modal...")
    # The remote function returns the final structured list directly to your laptop
    metrics = compute_diversity_remote.remote(results)
    
    # 1. Analyze / View in Terminal
    print("\nMean Pairwise Semantic Distance by Case and Agent:\n" + "="*65)
    for m in metrics:
        mean_dist = str(m['Diversity (Mean Distance)']) if m['Diversity (Mean Distance)'] is not None else "N/A"
        print(f"Case: {m['Case'].ljust(20)} | Agent: {m['Agent Condition'].ljust(12)} | Mean Distance: {mean_dist} (Valid: {m['Valid']}/10)")
        
    # 2. Save Results Locally
    csv_filename = "diversity_metrics.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Case", "Agent Condition", "Diversity (Mean Distance)", "Valid"])
        writer.writeheader()
        writer.writerows(metrics)
        
    print(f"\n✅ Results successfully saved locally to '{csv_filename}'")