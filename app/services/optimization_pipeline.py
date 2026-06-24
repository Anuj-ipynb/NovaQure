from typing import List
from app.services.ranking_service import RankingService, MoleculeScore
from app.services.explanation_service import ExplanationService
from app.services.amde_service import AMDEService
from app.services.optimization_history import OptimizationHistory
import random
import json


class OptimizationPipeline:
    """
    Orchestrates the full optimization loop:
    Ranking -> Explanation -> Decision (AMDE) -> Refinement/Regeneration -> Repeat
    """

    def __init__(self):
        # Initialize all core components
        self.ranker = RankingService()
        self.explainer = ExplanationService()
        self.amde = AMDEService()
        self.history_manager = OptimizationHistory()

    def simulate_refinement(self, molecule: dict) -> dict:
        """
        Slightly improves molecule properties to simulate refinement.
        """
        molecule["components"]["affinity_score"] += random.uniform(0.01, 0.05)
        molecule["components"]["qed"] += random.uniform(0.01, 0.03)
        return molecule

    def simulate_regeneration(self, molecule: dict) -> dict:
        """
        Replaces molecule properties with new random values to simulate regeneration.
        """
        molecule["components"]["affinity_score"] = random.uniform(0.3, 0.9)
        molecule["components"]["qed"] = random.uniform(0.4, 0.9)
        return molecule

    def run(self, molecules: List[MoleculeScore], iterations: int = 3):
        """
        Runs the full optimization loop for a given number of iterations.

        Args:
            molecules: Initial list of MoleculeScore objects
            iterations: Number of optimization cycles

        Returns:
            List of iteration-wise optimization results
        """

        # Reset history for a fresh run
        self.history_manager = OptimizationHistory()

        current = molecules

        for i in range(iterations):
            # Step 1: Rank molecules
            ranked = self.ranker.rank(current)

            # Store decisions for traceability
            decisions_log = []

            for mol in ranked:
                # Step 2: Generate explanation
                explanation = self.explainer.generate(mol)

                # Step 3: Get decision from AMDE
                decision = self.amde.decide(mol)

                # Attach explanation and decision to molecule
                mol["explanation"] = explanation
                mol["decision"] = decision

                # Log decision for iteration-level trace
                decisions_log.append({
                    "molecule_id": mol["molecule_id"],
                    "decision": decision["decision"],
                    "reason": decision["reason"],
                    "confidence": decision["confidence"]
                })

                # Step 4: Apply action based on decision
                if decision["decision"] == "refine":
                    self.simulate_refinement(mol)

                elif decision["decision"] == "regenerate":
                    self.simulate_regeneration(mol)

            # Step 5: Store iteration results
            iteration_data = {
                "iteration": i + 1,
                "results": ranked,
                "decisions": decisions_log
            }

            self.history_manager.log(iteration_data)

            # Step 6: Prepare input for next iteration
            current = [
                MoleculeScore(
                    molecule_id=m["molecule_id"],
                    qed=m["components"]["qed"],
                    sa=m["components"]["sa"],
                    affinity=-m["components"]["affinity_score"] * 10,
                    reliability=m["components"]["reliability"]
                )
                for m in ranked
            ]

        # Save results to file for downstream usage (e.g., platform/UI)
        with open("rankings.json", "w") as f:
            json.dump(self.history_manager.get_history(), f, indent=2)

        return self.history_manager.get_history()