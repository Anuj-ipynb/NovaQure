from typing import Dict, List, Protocol
from dataclasses import dataclass

@dataclass
class Assessment:
    metric: str
    score: float
    passed: bool
    reason: str

class DecisionStrategy(Protocol):
    def assess(self, molecule: Dict) -> Assessment: ...

class AffinityAssessment:
    def assess(self, molecule: Dict) -> Assessment:
        score = molecule.get("affinity_score", 0.0)
        return Assessment("affinity", score, score >= 0.5, "poor binding affinity" if score < 0.5 else "good binding affinity")

class ReliabilityAssessment:
    def assess(self, molecule: Dict) -> Assessment:
        score = molecule.get("reliability_score", 0.0)
        return Assessment("reliability", score, score >= 0.5, "low reliability score" if score < 0.5 else "high reliability")

class QEDAssessment:
    def assess(self, molecule: Dict) -> Assessment:
        score = molecule.get("qed", 0.0)
        return Assessment("drug-likeness", score, score >= 0.6, "drug-likeness below threshold" if score < 0.6 else "good drug-likeness")

class AMDEService:
    def __init__(self):
        self.strategies = [
            ReliabilityAssessment(),
            AffinityAssessment(),
            QEDAssessment(),
        ]

    def decide(self, molecule: Dict) -> Dict:
        comp = molecule.get("components") or molecule

        assessments = [strategy.assess(comp) for strategy in self.strategies]

        # Reasoning logic
        decision = "keep"
        reason = "molecule meets all quality thresholds"

        for assessment in assessments:
            if not assessment.passed:
                decision = "regenerate" if assessment.metric == "reliability" else "refine"
                reason = assessment.reason
                break

        confidence = round(sum(a.score for a in assessments) / len(assessments), 2)

        return {
            "decision": decision,
            "reason": reason,
            "confidence": confidence
        }
