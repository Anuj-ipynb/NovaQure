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

import logging

logger = logging.getLogger(__name__)

class AMDEService:
    def __init__(self):
        self.strategies = {
            "reliability": ReliabilityAssessment(),
            "affinity": AffinityAssessment(),
            "qed": QEDAssessment(),
        }

    def decide(self, molecule: Dict) -> Dict:
        comp = molecule.get("components") or molecule

        # ReAct Loop Simulation (Reasoning and Acting)
        thoughts_and_actions = []
        assessments = []
        
        # Step 1: Assess Reliability
        thoughts_and_actions.append("Thought: I need to check the reliability score to ensure quantum simulation validity.")
        reliability_assessment = self.strategies["reliability"].assess(comp)
        thoughts_and_actions.append(f"Action: Query Reliability -> Score: {reliability_assessment.score}, Passed: {reliability_assessment.passed}")
        assessments.append(reliability_assessment)
        
        # Step 2: Assess Affinity
        thoughts_and_actions.append("Thought: Reliability check completed. Now I need to evaluate the binding affinity.")
        affinity_assessment = self.strategies["affinity"].assess(comp)
        thoughts_and_actions.append(f"Action: Query Affinity -> Score: {affinity_assessment.score}, Passed: {affinity_assessment.passed}")
        assessments.append(affinity_assessment)
        
        # Step 3: Assess QED
        thoughts_and_actions.append("Thought: Affinity checked. Lastly, I must verify the QED score for drug-likeness.")
        qed_assessment = self.strategies["qed"].assess(comp)
        thoughts_and_actions.append(f"Action: Query QED -> Score: {qed_assessment.score}, Passed: {qed_assessment.passed}")
        assessments.append(qed_assessment)

        # Log reasoning traces for auditing
        for trace in thoughts_and_actions:
            logger.info("[AMDE ReAct Agent] %s", trace)

        # Decision Strategy Logic
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
            "confidence": confidence,
            "thoughts": thoughts_and_actions  # Preserving metadata
        }
