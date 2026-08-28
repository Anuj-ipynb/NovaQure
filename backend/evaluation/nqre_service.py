"""
NovaQure

NovaQure Reliability Evaluation (NQRE) Service

Evaluates the overall operational reliability and confidence bounds of 
corrected quantum execution outputs.

Responsibilities
----------------
- Normalize varying variance, noise_score, and convergence data
- Generate deterministic reliability indices weighted across features (weights sum to 1.0)
- Guard against invalid or corrupted system physical states
- Return type-safe validation models matching NovaQure conventions

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging

from backend.configs.nqre_config import (
    EPSILON,
    MIN_VARIANCE,
    MAX_VARIANCE,
    MIN_NOISE_SCORE,
    MAX_NOISE_SCORE,
    MIN_CONVERGENCE,
    MAX_CONVERGENCE,
    VARIANCE_WEIGHT,
    NOISE_WEIGHT,
    CONVERGENCE_WEIGHT,
)
from backend.evaluation.nqre_models import NQREResult

logger = logging.getLogger(__name__)


class NQREService:
    """
    NovaQure Reliability Evaluation engine wrapper.
    """

    def __init__(self) -> None:
        # Mathematical verification guard to ensure scaled bounds cannot overflow 100%
        weight_sum = VARIANCE_WEIGHT + NOISE_WEIGHT + CONVERGENCE_WEIGHT
        if abs(weight_sum - 1.0) > 1e-5:
            logger.error("NQRE configuration weights do not sum to 1.0 (Sum: %.4f). Scores will be skewed.", weight_sum)

    # ---------------------------------------------------------
    # Normalization Helper
    # ---------------------------------------------------------

    def _normalize(
        self,
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        """
        Normalize an incoming raw metric into [0.0, 1.0].
        """
        if maximum <= minimum:
            raise ValueError(
                f"Invalid normalization range specified. Min: {minimum}, Max: {maximum}"
            )

        normalized = (value - minimum) / (maximum - minimum + EPSILON)
        return max(0.0, min(1.0, normalized))

    # ---------------------------------------------------------
    # Feature Normalizations
    # ---------------------------------------------------------

    def normalize_variance(self, variance: float) -> float:
        """
        Normalize quantum variance against configured bounds.
        """
        return self._normalize(variance, MIN_VARIANCE, MAX_VARIANCE)

    def normalize_noise_score(self, noise_score: float) -> float:
        """
        Normalize incoming AQKC noise scores against configured bounds.
        """
        return self._normalize(noise_score, MIN_NOISE_SCORE, MAX_NOISE_SCORE)

    def normalize_convergence(self, convergence: float) -> float:
        """
        Normalize quantum wave-function convergence against configured bounds.
        """
        return self._normalize(convergence, MIN_CONVERGENCE, MAX_CONVERGENCE)

    # ---------------------------------------------------------
    # Reliability Score
    # ---------------------------------------------------------

    def compute_reliability(
        self,
        variance: float,
        noise_score: float,
        convergence: float,
    ) -> float:
        """
        Compute the reliability score.

        Lower variance and noise improve reliability,
        while higher convergence increases reliability.

        Returns
        -------
        float
            Reliability score in the range [0.0, 100.0].
        """
        normalized_variance = self.normalize_variance(variance)
        normalized_noise = self.normalize_noise_score(noise_score)
        normalized_convergence = self.normalize_convergence(convergence)

        # Invert variance and noise (lower is better), track convergence directly (higher is better)
        reliability = (
            VARIANCE_WEIGHT * (1.0 - normalized_variance)
            + NOISE_WEIGHT * (1.0 - normalized_noise)
            + CONVERGENCE_WEIGHT * normalized_convergence
        )

        reliability_scaled = reliability * 100.0
        logger.info("Reliability score: %.3f", reliability_scaled)
        return reliability_scaled

    # ---------------------------------------------------------
    # Confidence Score
    # ---------------------------------------------------------

    def compute_confidence(self, reliability_score: float) -> float:
        """
        Compute confidence score derived directly from the reliability parameters.

        Returns
        -------
        float
            Confidence score bound to the range [0.0, 100.0].
        """
        confidence = max(0.0, min(100.0, reliability_score))
        logger.info("Confidence score: %.3f", confidence)
        return confidence

    # ---------------------------------------------------------
    # Public Evaluation API
    # ---------------------------------------------------------

    def evaluate(
        self,
        corrected_energy: float,
        variance: float,
        noise_score: float,
        convergence: float,
    ) -> NQREResult:
        """
        Evaluate the reliability of corrected quantum outputs.

        Parameters
        ----------
        corrected_energy : float
            AQKC-corrected quantum energy. Reserved for future reliability extensions.
            Currently not included in the scoring function because absolute molecular 
            energies vary naturally and are not directly comparable indicator vectors.
        variance : float
            Quantum variance payload (must be non-negative).
        noise_score : float
            AQKC scaled noise rating (must be non-negative).
        convergence : float
            Quantum convergence ratio (must be bounded between 0.0 and 1.0).

        Returns
        -------
        NQREResult
            Type-safe validation model carrying confidence metrics.
        """
        # Explicit Boundary Guard Checks
        if variance < 0.0:
            raise ValueError(f"Quantum variance cannot be negative. Received: {variance}")
        if noise_score < 0.0:
            raise ValueError(f"Noise score cannot be negative. Received: {noise_score}")
        if not (0.0 <= convergence <= 1.0):
            raise ValueError(f"Convergence ratio must sit between 0.0 and 1.0. Received: {convergence}")

        # Explicitly swallow parameter to clear linter warnings for unread variables
        _ = corrected_energy

        reliability = self.compute_reliability(
            variance=variance,
            noise_score=noise_score,
            convergence=convergence,
        )

        confidence = self.compute_confidence(reliability)

        logger.info("NQRE evaluation completed successfully.")
        return NQREResult(
            reliability_score=reliability,
            confidence_score=confidence,
        )

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self) -> bool:
        """
        Verify the NQRE mathematical mapping environment is fully operational.
        """
        try:
            self.normalize_variance((MIN_VARIANCE + MAX_VARIANCE) / 2.0)
            self.normalize_noise_score((MIN_NOISE_SCORE + MAX_NOISE_SCORE) / 2.0)
            self.normalize_convergence((MIN_CONVERGENCE + MAX_CONVERGENCE) / 2.0)
            return True
        except Exception as exc:
            logger.exception("NQRE Service configuration check caught structural anomaly: %s", exc)
            return False

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self) -> "NQREService":
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> bool:
        # Returning False explicitly avoids suppression to let exceptions ripple up
        return False