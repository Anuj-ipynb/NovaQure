from typing import Dict


class ExplanationService:
    def generate(self, scored_molecule: Dict) -> Dict:
        comp = scored_molecule.get("components", scored_molecule)

        reasons = []

        # Affinity reasoning
        affinity_score = comp.get("affinity_score", 0.0)
        if affinity_score > 0.7:
            reasons.append("strong binding affinity")
        elif affinity_score < 0.4:
            reasons.append("weak binding affinity")
        else:
            reasons.append("moderate binding affinity")

        # Reliability reasoning
        reliability = comp.get("reliability_score", 0.0)
        if reliability > 0.8:
            reasons.append("high reliability")
        elif reliability < 0.6:
            reasons.append("low confidence prediction")
        else:
            reasons.append("moderate reliability")

        # Drug-likeness reasoning
        qed = comp.get("qed", 0.0)
        if qed > 0.7:
            reasons.append("high drug-likeness")
        elif qed < 0.6:
            reasons.append("suboptimal drug-likeness")
        else:
            reasons.append("acceptable drug-likeness")

        reason_text = ", ".join(reasons)

        return {
            "reason": reason_text,
            "score_breakdown": comp
        }