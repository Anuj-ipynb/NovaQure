from typing import List, Dict
from dataclasses import dataclass


@dataclass
class MoleculeScore:
    molecule_id: str
    qed: float
    sa: float
    affinity: float
    reliability: float


class RankingService:
    def __init__(self):
        # Explainable weights
        self.weights = {
            "qed": 0.25,
            "sa": 0.20,
            "affinity": 0.30,
            "reliability": 0.25
        }

    def normalize_affinity(self, affinity: float) -> float:
        """
        Convert negative affinity to positive scale (0 to 1)
        More negative = better
        """
        return max(0.0, min(1.0, (-affinity) / 10))

    def compute_score(self, mol: MoleculeScore) -> Dict:
        affinity_score = self.normalize_affinity(mol.affinity)

        final_score = (
            mol.qed * self.weights["qed"] +
            mol.sa * self.weights["sa"] +
            affinity_score * self.weights["affinity"] +
            mol.reliability * self.weights["reliability"]
        )

        return {
            "molecule_id": mol.molecule_id,
            "final_score": round(final_score * 100, 2),
            "components": {
                "qed": mol.qed,
                "sa": mol.sa,
                "affinity_score": affinity_score,
                "reliability": mol.reliability
            }
        }

    def rank(self, molecules: List[MoleculeScore]) -> List[Dict]:
        scored = [self.compute_score(m) for m in molecules]

        ranked = sorted(
            scored,
            key=lambda x: x["final_score"],
            reverse=True
        )

        for idx, mol in enumerate(ranked):
            mol["rank"] = idx + 1

        return ranked