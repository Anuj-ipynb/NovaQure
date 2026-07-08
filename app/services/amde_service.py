from typing import Dict


class AMDEService:
    def decide(self, molecule: Dict) -> Dict:
        comp = molecule["components"]

        affinity = comp["affinity_score"]
        reliability = comp["reliability"]
        qed = comp["qed"]

        # Decision logic (EXPLAINABLE — very important)
        if reliability < 0.6:
            decision = "regenerate"
            reason = "low reliability score"

        elif affinity < 0.4:
            decision = "refine"
            reason = "poor binding affinity"

        elif qed < 0.5:
            decision = "refine"
            reason = "low drug-likeness"

        else:
            decision = "keep"
            reason = "meets all quality thresholds"

        # Confidence calculation
        confidence = round((affinity + reliability + qed) / 3, 2)

        return {
            "decision": decision,
            "reason": reason,
            "confidence": confidence
        }
    