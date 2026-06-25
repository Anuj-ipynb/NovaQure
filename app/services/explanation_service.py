from typing import Dict


class ExplanationService:
    def generate(self, scored_molecule: Dict) -> Dict:
        comp = scored_molecule["components"]

        reasons = []

        # Affinity reasoning
        if comp["affinity_score"] > 0.7:
            reasons.append("strong binding affinity")
        elif comp["affinity_score"] < 0.4:
            reasons.append("weak binding affinity")
        else:
            reasons.append("moderate binding affinity")

        # Reliability reasoning
        if comp["reliability"] > 0.8:
            reasons.append("high reliability")
        elif comp["reliability"] < 0.6:
            reasons.append("low confidence prediction")
        else:
            reasons.append("moderate reliability")

        # Drug-likeness reasoning
        if comp["qed"] > 0.7:
            reasons.append("good drug-likeness")
        elif comp["qed"] < 0.5:
            reasons.append("poor drug-likeness")

        reason_text = ", ".join(reasons)

        return {
            "reason": reason_text,
            "score_breakdown": comp
        }