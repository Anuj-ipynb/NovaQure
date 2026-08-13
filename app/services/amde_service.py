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

        # Step 4: Optional Live LLM Insight (Non-blocking fallback)
        llm_result = self._try_llm_reasoning(comp, decision, reason)
        if llm_result:
            model_name, rec_text = llm_result
            thoughts_and_actions.append(f"Thought (LLM Agent - {model_name}): {rec_text}")
            llm_recommendation = rec_text
        else:
            llm_recommendation = None

        return {
            "decision": decision,
            "reason": reason,
            "confidence": confidence,
            "recommendation": llm_recommendation or "Maintain structure and evaluate binding stability.",
            "thoughts": thoughts_and_actions  # Preserving metadata
        }

    def _try_llm_reasoning(self, comp: Dict, decision: str, reason: str) -> tuple[str, str] | None:
        """
        Queries the configured LLM provider (NVIDIA Nemotron API or local Ollama)
        for qualitative chemical optimization advice. Times out in 1.5s to ensure fast pipeline runs.
        """
        try:
            import urllib.request
            import json
            from backend.configs.llm_config import get_active_llm_info, NVIDIA_API_KEY

            info = get_active_llm_info()
            smiles = comp.get("smiles", "unknown structure")
            prompt = (
                f"As a medicinal chemist, give a 1-sentence recommendation for molecule '{smiles}'. "
                f"Current evaluation decision: {decision} due to {reason}."
            )

            if info["type"] == "nvidia":
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {NVIDIA_API_KEY}"
                }
                body = {
                    "model": info["model"],
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 60,
                    "temperature": 0.2
                }
                req = urllib.request.Request(
                    info["endpoint"],
                    data=json.dumps(body).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=1.5) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode("utf-8"))
                        text = data["choices"][0]["message"]["content"].strip()
                        return info["model"], text

            elif info["type"] == "ollama":
                headers = {"Content-Type": "application/json"}
                body = {"model": info["model"], "prompt": prompt, "stream": False}
                req = urllib.request.Request(
                    info["endpoint"],
                    data=json.dumps(body).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=1.5) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode("utf-8"))
                        text = data.get("response", "").strip()
                        return info["model"], text
        except Exception:
            # Silent fallback to deterministic execution engine when LLM endpoint is unreachable
            pass
        return None

