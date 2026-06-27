export interface Molecule {
    id: string;

    experiment_id: string;

    smiles: string;

    affinity_score: number;

    confidence_score: number;

    toxicity_score: number;

    created_at: string;

    updated_at: string;
}
