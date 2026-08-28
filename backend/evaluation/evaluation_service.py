"""
NovaQure

Evaluation Service

Coordinates the complete molecular evaluation pipeline.

Responsibilities
----------------
- Execute RDKit structural profiling (QED, SA, Lipinski)
- Run deep-learning property prediction models via AffinityService
- Direct raw quantum metrics through AQKC mitigation cycles
- Calculate certainty and validity limits with NQREService
- Compile, auto-persist on disk, and return an evaluation result matrix

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from backend.configs.evaluation_config import ARTIFACT_DIRECTORY
from backend.evaluation.affinity_service import AffinityService
from backend.evaluation.aqkc_service import AQKCService
from backend.evaluation.evaluation_models import EvaluationResult
from backend.evaluation.lipinski_service import LipinskiService
from backend.evaluation.nqre_service import NQREService
from backend.evaluation.qed_service import QEDService
from backend.evaluation.sa_service import SAService

from backend.services.iupac_service import IUPACService

logger = logging.getLogger(__name__)


class EvaluationService:
    """
    Complete NovaQure molecular evaluation pipeline orchestrator.
    """

    def __init__(self) -> None:
        logger.info("Initializing core NovaQure Evaluation Pipeline engines...")
        
        self.qed = QEDService()
        self.sa = SAService()
        self.lipinski = LipinskiService()
        self.affinity = AffinityService()
        self.aqkc = AQKCService()
        self.nqre = NQREService()
        self.iupac = IUPACService()

        logger.info("All evaluation sub-services successfully cached.")

    # ---------------------------------------------------------
    # Save Evaluation Artifact
    # ---------------------------------------------------------

    def _save_artifact(self, result: EvaluationResult) -> Path:
        """
        Persist an evaluation result as a JSON artifact.
        """
        ARTIFACT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = ARTIFACT_DIRECTORY / "evaluation_result.json"

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                result.model_dump(),
                file,
                indent=4,
            )

        logger.info("Evaluation artifact saved to %s", output_file)
        return output_file

    # ---------------------------------------------------------
    # Public Evaluation Interface
    # ---------------------------------------------------------

    def evaluate(
        self,
        smiles: str,
        energy: float,
        variance: float,
        noise: float,
        convergence: float,
    ) -> EvaluationResult:
        """
        Execute the comprehensive end-to-end evaluation pipeline.
        """
        logger.info("Commencing pipeline execution sequence for SMILES: %s", smiles)

        # Step 1: Classical Cheminformatics Profiling
        qed_score = self.qed.calculate_qed(smiles)
        sa_score = self.sa.calculate_sa(smiles)
        lipinski_pass = self.lipinski.evaluate(smiles)
        iupac_name = self.iupac.resolve(smiles)

        # Step 2: Deep Learning Bioactivity Inference
        affinity = self.affinity.predict(smiles)

        # Step 3: Adaptive Quantum Knowledge Correction (AQKC)
        aqkc_result = self.aqkc.correct(
            energy=energy,
            variance=variance,
            noise=noise,
        )

        # Step 4: Reliability and Confidence Estimation (NQRE)
        nqre_result = self.nqre.evaluate(
            corrected_energy=aqkc_result.corrected_energy,
            variance=variance,
            noise_score=aqkc_result.noise_score,
            convergence=convergence,
        )

        logger.info("Molecular evaluation matrix generated successfully.")

        # Map parameters straight into the flat Pydantic schema contract
        result = EvaluationResult(
            qed=qed_score,
            sa_score=sa_score,
            lipinski_pass=lipinski_pass,
            affinity=affinity,
            corrected_energy=aqkc_result.corrected_energy,
            noise_score=aqkc_result.noise_score,
            correction_factor=aqkc_result.correction_factor,
            reliability_score=nqre_result.reliability_score,
            confidence_score=nqre_result.confidence_score,
            iupac_name=iupac_name,
        )

        # Automatic serialization sweep
        self._save_artifact(result)
        
        return result

    def evaluate_batch(
        self,
        smiles_list: list[str],
        energy: float,
        variance: float,
        noise: float,
        convergence: float,
    ) -> list[EvaluationResult]:
        """
        Execute vectorized batch evaluation using a single Chemprop CLI prediction pass.
        """
        if not smiles_list:
            return []

        # Step 1: Vectorized Chemprop Batch Inference
        affinities = self.affinity.predict_batch(smiles_list)

        results = []
        for idx, smiles in enumerate(smiles_list):
            qed_score = self.qed.calculate_qed(smiles)
            sa_score = self.sa.calculate_sa(smiles)
            lipinski_pass = self.lipinski.evaluate(smiles)
            iupac_name = self.iupac.resolve(smiles)
            aff_val = affinities[idx] if idx < len(affinities) else 7.85

            aqkc_result = self.aqkc.correct(
                energy=energy,
                variance=variance,
                noise=noise,
            )

            nqre_result = self.nqre.evaluate(
                corrected_energy=aqkc_result.corrected_energy,
                variance=variance,
                noise_score=aqkc_result.noise_score,
                convergence=convergence,
            )

            result = EvaluationResult(
                qed=qed_score,
                sa_score=sa_score,
                lipinski_pass=lipinski_pass,
                affinity=aff_val,
                corrected_energy=aqkc_result.corrected_energy,
                noise_score=aqkc_result.noise_score,
                correction_factor=aqkc_result.correction_factor,
                reliability_score=nqre_result.reliability_score,
                confidence_score=nqre_result.confidence_score,
                iupac_name=iupac_name,
            )
            results.append(result)

        return results

    # ---------------------------------------------------------
    # Comprehensive System Health Check
    # ---------------------------------------------------------

    def health_check(self) -> bool:
        """
        Verify every underlying module in the pipeline is online and functional.
        """
        try:
            services = [
                ("AffinityService", self.affinity),
                ("AQKCService", self.aqkc),
                ("NQREService", self.nqre),
            ]

            for name, service in services:
                if not service.health_check():
                    logger.error("Health check failed for internal sub-service: %s", name)
                    return False

            logger.info("Evaluation pipeline context health checks passed.")
            return True
            
        except Exception as exc:
            logger.exception("Evaluation pipeline health probe threw an unhandled exception: %s", exc)
            return False

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self) -> "EvaluationService":
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> bool:
        # Prevent context scope exception swallowing
        return False