import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the visual style to look academic and clean
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update({'font.size': 12, 'figure.dpi': 300})

def plot_training_curves(base_dir="."):
    """Extracts loss from trainer_state.json and plots training curves."""
    personas = ["causal", "analogical", "teleological", "dialectical"]
    plt.figure(figsize=(10, 6))
    
    data_found = False
    for persona in personas:
        # Assuming you downloaded the adapter folders locally, or point this to your mounted volume
        state_path = os.path.join(base_dir, f"{persona}_adapter", "trainer_state.json")
        
        if os.path.exists(state_path):
            data_found = True
            with open(state_path, 'r') as f:
                state = json.load(f)
            
            steps = []
            losses = []
            for log in state.get("log_history", []):
                if "loss" in log and "step" in log:
                    steps.append(log["step"])
                    losses.append(log["loss"])
            
            if steps:
                plt.plot(steps, losses, marker='o', label=persona.capitalize())

    if not data_found:
        print("⚠️ Could not find trainer_state.json files. Skipping training curves.")
        return

    plt.title("Fine-Tuning Training Loss per Persona")
    plt.xlabel("Training Steps")
    plt.ylabel("Loss")
    plt.legend(title="Persona")
    plt.tight_layout()
    plt.savefig("training_curves.png")
    print("✅ Saved training_curves.png")

def plot_target_recovery():
    """Recreates Figure 1: Target recovery rate by case and agent condition."""
    # NOTE: You must manually grade the outputs to fill in this data!
    # These are placeholder numbers based on the structure of Figure 1.
    data = {
        "Case": [
            "Aviation (scene)", "Aviation (complete)", 
            "Industrial (scene)", "Industrial (complete)",
            "Medical (scene)", "Medical (complete)",
            "Jet Engine (control)", "Botulism (control)"
        ] * 2,
        "Agent Condition": ["Baseline"] * 8 + ["Persona"] * 8,
        "Recovery Rate (%)": [
            0, 0, 0, 0, 0, 40, 100, 100,  # Baseline placeholders
            0, 0, 0, 40, 0, 0, 100, 100   # Persona placeholders
        ]
    }
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df, 
        x="Case", 
        y="Recovery Rate (%)", 
        hue="Agent Condition",
        palette=["#4C72B0", "#DD8452"]
    )
    
    plt.title("Target Recovery Rate by Case, Evidence, and Condition")
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0, 105)
    plt.tight_layout()
    plt.savefig("target_recovery_fig1.png")
    print("✅ Saved target_recovery_fig1.png")

def plot_diversity_vs_recovery(csv_path="diversity_metrics.csv"):
    """Recreates Figure 2: Diversity vs Target Recovery Rate from CSV."""
    if not os.path.exists(csv_path):
        print(f"⚠️ Could not find {csv_path}. Make sure the file is in the same directory.")
        return

    df = pd.read_csv(csv_path)
    
    # Safety check to ensure you added the manual grading columns!
    if "Recovery Rate (%)" not in df.columns or "Evidence Condition" not in df.columns:
        print("⚠️ Missing columns! Please open diversity_metrics.csv and manually add 'Recovery Rate (%)' and 'Evidence Condition' columns.")
        return
    
    plt.figure(figsize=(10, 7))
    
    sns.scatterplot(
        data=df,
        x="Diversity (Mean Distance)",
        y="Recovery Rate (%)",
        hue="Case",
        style="Agent Condition",
        size="Evidence Condition",
        sizes=(150, 150),
        palette="Set2"
    )
    
    plt.title("Semantic Diversity vs. Target Recovery Rate")
    plt.ylim(-5, 105)
    # You may need to adjust xlim depending on your actual min/max diversity scores
    plt.xlim(df["Diversity (Mean Distance)"].min() - 0.05, df["Diversity (Mean Distance)"].max() + 0.05)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("diversity_vs_recovery_fig2.png")
    print("✅ Saved diversity_vs_recovery_fig2.png")

if __name__ == "__main__":
    print("Generating plots...")
    plot_training_curves()
    plot_target_recovery()
    plot_diversity_vs_recovery()