import sqlite3
import pandas as pd
import json

def run_audit():
    # Connect to SQLite database
    conn = sqlite3.connect("novaqure.db")
    
    print("======================================================================")
    print("                  NOVAQURE SCIENTIFIC AUDIT REPORT                     ")
    print("======================================================================")
    
    # 1. Fetch Experiment Info
    experiment = pd.read_sql_query("SELECT * FROM experiments ORDER BY created_at DESC LIMIT 1", conn)
    if experiment.empty:
        print("No experiments found in the database. Run the pipeline first.")
        conn.close()
        return
        
    exp_id = experiment.iloc[0]['id']
    print(f"Target Protein : {experiment.iloc[0]['target_protein']}")
    print(f"Iterations     : {experiment.iloc[0]['iterations']}")
    print(f"Status         : {experiment.iloc[0]['status']}")
    print(f"Experiment ID  : {exp_id}")
    print("----------------------------------------------------------------------")
    
    # 2. Fetch Molecules and Evaluations
    query = """
        SELECT m.id as molecule_id, m.smiles, e.qed, e.sa_score, e.binding_affinity, 
               r.rank, r.score as final_score, r.confidence
        FROM molecules m
        JOIN evaluations e ON m.id = e.molecule_id
        LEFT JOIN rankings r ON m.id = r.molecule_id
        WHERE m.experiment_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(exp_id,))
    
    if df.empty:
        print("No molecule evaluations found for this experiment.")
        conn.close()
        return

    print(f"Total Evaluated Molecules: {len(df)}")
    print("\n[1] CHEMINFORMATICS METRICS:")
    print(f"  * QED (Drug-likeness)     - Mean: {df['qed'].mean():.4f} | Min: {df['qed'].min():.4f} | Max: {df['qed'].max():.4f}")
    print(f"  * SA Score (Synthesizability) - Mean: {df['sa_score'].mean():.4f} | Min: {df['sa_score'].min():.4f} | Max: {df['sa_score'].max():.4f}")
    
    print("\n[2] BINDING AFFINITY METRICS:")
    print(f"  * Predicted Affinity (GNN) - Mean: {df['binding_affinity'].mean():.4f} | Min: {df['binding_affinity'].min():.4f} | Max: {df['binding_affinity'].max():.4f}")
    
    print("\n[3] SELECTION & CONFIDENCE METRICS:")
    print(f"  * Final Ranked Score       - Mean: {df['final_score'].mean():.4f} | Min: {df['final_score'].min():.4f} | Max: {df['final_score'].max():.4f}")
    print(f"  * Reliability Confidence   - Mean: {df['confidence'].mean():.4f} | Min: {df['confidence'].min():.4f} | Max: {df['confidence'].max():.4f}")
    
    print("\n[4] TOP 5 HIGHEST RANKED CANDIDATES:")
    top_5 = df.sort_values(by="rank").head(5)
    for idx, row in top_5.iterrows():
        print(f"  Rank {row['rank']} | Score: {row['final_score']:.4f} | QED: {row['qed']:.3f} | SMILES: {row['smiles']}")
        
    print("======================================================================")
    conn.close()

if __name__ == "__main__":
    run_audit()
