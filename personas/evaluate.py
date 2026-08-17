import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering

def analyze_and_plot_epistemic_diversity(input_json_path="epistemic_fingerprints_54_trials.json"):
    # 1. Load the Data
    with open(input_json_path, "r") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # 2. Embed the Main Hypotheses
    print("Loading Sentence Transformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Embedding hypotheses...")
    embeddings = model.encode(df['primaryHypothesis'].tolist())
    
    # 3. Cluster Hypotheses to Measure "Epistemic Diversity"
    # Using Agglomerative Clustering. A distance threshold of 0.4 implies 
    # that hypotheses must be reasonably distinct to form a new cluster.
    clustering_model = AgglomerativeClustering(
        n_clusters=None, 
        distance_threshold=0.4, 
        metric='cosine', 
        linkage='average'
    )
    df['claim_cluster_id'] = clustering_model.fit_predict(embeddings)
    
    # 4. Save the Evaluated Data
    evaluated_json_path = "evaluated_epistemic_fingerprints.json"
    df.to_json(evaluated_json_path, orient="records", indent=4)
    print(f"Clustered data saved to {evaluated_json_path}")

    # ==========================================
    # VISUALIZATION 1: FINGERPRINT STRENGTH (HEATMAP)
    # Proves if agents are distinct or redundant
    # ==========================================
    plt.figure(figsize=(10, 8))
    
    # Calculate average similarity between different agents across all trials
    agents = df['agentId'].unique()
    sim_matrix = np.zeros((len(agents), len(agents)))

    for i, agent_a in enumerate(agents):
        for j, agent_b in enumerate(agents):
            embed_a = embeddings[df['agentId'] == agent_a]
            embed_b = embeddings[df['agentId'] == agent_b]
            
            # Cross-similarity between all hypotheses of agent A and agent B
            cross_sim = cosine_similarity(embed_a, embed_b)
            sim_matrix[i, j] = np.mean(cross_sim)
            
    sns.heatmap(sim_matrix, annot=True, xticklabels=agents, yticklabels=agents, 
                cmap="YlGnBu", vmin=0.5, vmax=1.0)
    plt.title("Epistemic Redundancy (Cosine Similarity Between Agents)", pad=20)
    plt.xlabel("Agent Persona")
    plt.ylabel("Agent Persona")
    plt.tight_layout()
    plt.savefig("fig_1_similarity_heatmap.png", dpi=300)
    print("Saved Similarity Heatmap -> fig_1_similarity_heatmap.png")

    # ==========================================
    # VISUALIZATION 2: EPISTEMIC DIVERSITY (BAR CHART)
    # Shows how many unique claims each condition/agent generated
    # ==========================================
    plt.figure(figsize=(12, 6))
    
    # Group by Condition and Agent, count unique clusters
    diversity_df = df.groupby(['condition', 'agentId'])['claim_cluster_id'].nunique().reset_index()
    diversity_df.rename(columns={'claim_cluster_id': 'Unique Hypotheses'}, inplace=True)

    sns.barplot(data=diversity_df, x="agentId", y="Unique Hypotheses", hue="condition", palette="viridis")
    plt.title("Epistemic Diversity: Unique Hypothesis Clusters per Agent", pad=20)
    plt.ylabel("Number of Unique Claims")
    plt.xlabel("Agent Persona")
    plt.legend(title="Condition (History/Prompt)")
    plt.tight_layout()
    plt.savefig("fig_2_epistemic_diversity.png", dpi=300)
    print("Saved Epistemic Diversity Chart -> fig_2_epistemic_diversity.png")

if __name__ == "__main__":
    analyze_and_plot_epistemic_diversity()