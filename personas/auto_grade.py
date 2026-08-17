import json
import re
import pandas as pd

def check_recovery(case_name, hypothesis_text):
    """
    Applies the strict match rule for target recovery based on the established causes.
    Returns 1 if a match is found, 0 otherwise.
    """
    text = hypothesis_text.lower()
    
    if "aviation" in case_name:
        has_weight = re.search(r'\b(weight|overweight|heavy|load)\b', text)
        has_icing_workload = re.search(r'\b(ice|icing|workload|monitor|distract)\b', text)
        return 1 if (has_weight and has_icing_workload) else 0

    elif "industrial" in case_name:
        has_suppression = re.search(r'\b(sprinkler|suppression|extinguishing|pipe)\b', text)
        has_water_corrosion = re.search(r'\b(corrod|leak|water|moisture)\b', text)
        return 1 if (has_suppression and has_water_corrosion) else 0

    elif "medical" in case_name:
        return 1 if "rubella" in text else 0

    elif "jet_engine" in case_name:
        return 1 if "bird" in text else 0

    elif "botulism" in case_name:
        has_botulism = "botulis" in text or "botulinum" in text
        has_canned = re.search(r'\b(can|canned|preserve|jar)\b', text)
        return 1 if (has_botulism or has_canned) else 0

    return 0

def main():
    print("Loading finetuned_evaluation_results.json...")
    try:
        with open('finetuned_evaluation_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("Error: Could not find evaluation JSON.")
        return

    # 1. Grade the JSON outputs
    grading_tracker = {}
    for entry in results:
        case = entry['case']
        agent = entry['agent']
        raw_output = entry['raw_output'].strip()
        
        cleaned_output = re.sub(r'^```(?:json)?\s*', '', raw_output)
        cleaned_output = re.sub(r'\s*```$', '', cleaned_output)
        
        score = 0
        try:
            parsed_json = json.loads(cleaned_output)
            primary_hyp = parsed_json.get('primary_hypothesis', '')
            score = check_recovery(case, primary_hyp)
        except Exception:
            pass 
            
        key = (case, agent)
        if key not in grading_tracker:
            grading_tracker[key] = []
        grading_tracker[key].append(score)

    recovery_rates = {}
    for key, scores in grading_tracker.items():
        rate = (sum(scores) / len(scores)) * 100 if scores else 0
        recovery_rates[key] = round(rate, 2)

    # 2. Hardcode your pre-computed semantic distances
    distances = {
        ("aviation_scene", "analogical"): 0.2149,
        ("aviation_scene", "baseline"): 0.1459,
        ("aviation_scene", "causal"): 0.0977,
        ("aviation_scene", "dialectical"): 0.2469,
        ("aviation_scene", "teleological"): 0.1540,
        ("botulism_control", "analogical"): 0.3082,
        ("botulism_control", "baseline"): 0.3029,
        ("botulism_control", "causal"): 0.2647,
        ("botulism_control", "dialectical"): 0.3176,
        ("botulism_control", "teleological"): 0.3597,
        ("industrial_scene", "analogical"): 0.2964,
        ("industrial_scene", "baseline"): 0.2484,
        ("industrial_scene", "causal"): 0.3835,
        ("industrial_scene", "dialectical"): 0.3003,
        ("industrial_scene", "teleological"): 0.3442,
        ("jet_engine_control", "analogical"): 0.2042,
        ("jet_engine_control", "baseline"): 0.1524,
        ("jet_engine_control", "causal"): 0.1517,
        ("jet_engine_control", "dialectical"): 0.1301,
        ("jet_engine_control", "teleological"): 0.2125,
        ("medical_complete", "analogical"): 0.2802,
        ("medical_complete", "baseline"): 0.2227,
        ("medical_complete", "causal"): 0.3137,
        ("medical_complete", "dialectical"): 0.1637,
        ("medical_complete", "teleological"): 0.2476,
    }

    # 3. Build the final data structure
    rows = []
    for (case, agent), dist in distances.items():
        rate = recovery_rates.get((case, agent), 0)
        ev_cond = "Complete" if "complete" in case.lower() else "Scene"
        rows.append({
            "Case": case,
            "Agent Condition": agent,
            "Diversity (Mean Distance)": dist,
            "Valid": 10,
            "Evidence Condition": ev_cond,
            "Recovery Rate (%)": rate
        })

    # 4. Generate the CSV from scratch
    df = pd.DataFrame(rows)
    df.to_csv("diversity_metrics.csv", index=False)
    print("✅ diversity_metrics.csv generated successfully from scratch!")
    print("✅ Ready to run plot_results.py!")

if __name__ == "__main__":
    main()