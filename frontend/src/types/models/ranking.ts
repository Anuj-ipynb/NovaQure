export interface Ranking {
  id: string;
  molecule_id: string;
  rank: number;
  score: number;
  confidence: number;
  created_at: string;
  updated_at: string;
  smiles?: string;
  reliability?: number;
  affinity?: number;
  qed?: number;
  sa?: number;
  iupac_name?: string;
}

