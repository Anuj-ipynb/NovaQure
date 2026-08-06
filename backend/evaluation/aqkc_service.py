"""
NovaQure

Adaptive Quantum Knowledge Correction (AQKC)

Corrects noisy quantum outputs before reliability evaluation.

Responsibilities
----------------
- Validate telemetry bounds (variance, noise) strictly before normalization execution
- Normalize metrics safely within target configuration profiles
- Dynamically scale corrections without iterative structural passes
- Map outputs to type-safe Pydantic data schemas

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging

from backend.configs.aqkc_config import (
    EPSILON,
    MIN_VARIANCE,
    MAX_VARIANCE,
    MIN_NOISE,
    MAX_NOISE,
    ENERGY_WEIGHT,
    VARIANCE_WEIGHT,
    NOISE_WEIGHT,
    MAX_CORRECTION_FACTOR,
    NOISE_SCORE_SCALE,
)
from backend.evaluation.aqkc_models import AQKCResult

logger = logging.getLogger(__name__)


class AQKCService:
    """
    Adaptive Quantum Knowledge Correction service.
    """

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
        Normalize an incoming raw telemetry metric into [0.0, 1.0].
        """
        if maximum <= minimum:
            raise ValueError(
                f"Invalid normalization range specified. Min: {minimum}, Max: {maximum}"
            )

        normalized = (value - minimum) / (maximum - minimum + EPSILON)
        return max(0.0, min(1.0, normalized))

    # ---------------------------------------------------------
    # Variance
    # ---------------------------------------------------------

    def normalize_variance(self, variance: float) -> float:
        """
        Normalize raw quantum variance against configured bounds.
        """
        return self._normalize(
            variance,
            MIN_VARIANCE,
            MAX_VARIANCE,
        )

    # ---------------------------------------------------------
    # Noise
    # ---------------------------------------------------------

    def normalize_noise(self, noise: float) -> float:
        """
        Normalize raw quantum noise measurements against configured bounds.
        """
        return self._normalize(
            noise,
            MIN_NOISE,
            MAX_NOISE,
        )

    # ---------------------------------------------------------
    # Correction Factor
    # ---------------------------------------------------------

    def compute_correction(self, variance: float, noise: float) -> float:
        """
        Compute the AQKC correction factor.

        Higher variance and noise increase the magnitude of the 
        correction factor applied to the base energy.
        """
        normalized_variance = self.normalize_variance(variance)
        normalized_noise = self.normalize_noise(noise)

        correction = (
            VARIANCE_WEIGHT * normalized_variance +
            NOISE_WEIGHT * normalized_noise
        )

        correction = min(correction, MAX_CORRECTION_FACTOR)
        logger.info("Correction factor calculated: %.6f", correction)
        return correction

    # ---------------------------------------------------------
    # Correct Energy
    # ---------------------------------------------------------

    def compute_corrected_energy(self, energy: float, correction_factor: float) -> float:
        """
        Compute corrected quantum energy using Zero-Noise Richardson Extrapolation (ZNE).
        Extrapolates energy to lambda = 0 using simulated scales lambda = 1 and lambda = 2.
        """
        # Baseline noise (lambda = 1)
        e_1 = energy
        # Scaled noise (lambda = 2) - simulated using the correction factor
        e_2 = energy * (1.0 + ENERGY_WEIGHT * correction_factor)
        
        # Richardson Extrapolation formula: E(0) = 2*E(1) - E(2)
        corrected_energy = 2.0 * e_1 - e_2
        logger.info("ZNE Richardson Extrapolation corrected quantum energy: %.6f", corrected_energy)
        return corrected_energy


    # ---------------------------------------------------------
    # Noise Score
    # ---------------------------------------------------------

    def compute_noise_score(self, noise: float) -> float:
        """
        Convert raw normalized noise into an interpretable bounded rating scale.
        Lower values represent cleaner quantum outputs.
        """
        normalized_noise = self.normalize_noise(noise)
        score = normalized_noise * NOISE_SCORE_SCALE
        
        logger.info("Calculated noise score: %.3f", score)
        return score

    # ---------------------------------------------------------
    # Public Correction API
    # ---------------------------------------------------------

    def correct(
        self,
        energy: float,
        variance: float,
        noise: float,
    ) -> AQKCResult:
        """
        Apply full AQKC correction pipeline to raw quantum simulation inputs.

        Parameters
        ----------
        energy : float
            Raw uncorrected quantum molecular energy.
        variance : float
            Raw quantum variance (must be non-negative).
        noise : float
            Raw quantum noise payload (must be non-negative).

        Returns
        -------
        AQKCResult
            Type-safe validation model containing corrected evaluation metrics.
        """
        # Explicit Physical Boundary Checks
        if variance < 0.0:
            raise ValueError(f"Quantum variance cannot be negative. Received: {variance}")
        if noise < 0.0:
            raise ValueError(f"Quantum noise cannot be negative. Received: {noise}")

        # Execute functional evaluation pass
        correction_factor = self.compute_correction(variance, noise)
        corrected_energy = self.compute_corrected_energy(energy, correction_factor)
        noise_score = self.compute_noise_score(noise)

        logger.info("AQKC mitigation cycle completed successfully.")
        
        return AQKCResult(
            corrected_energy=corrected_energy,
            noise_score=noise_score,
            correction_factor=correction_factor,
        )

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self) -> bool:
        """
        Verify the mathematical static configuration states are operational by running 
        a lightweight internal tracking evaluation.
        """
        try:
            mid_variance = (MIN_VARIANCE + MAX_VARIANCE) / 2.0
            mid_noise = (MIN_NOISE + MAX_NOISE) / 2.0
            
            self.normalize_variance(mid_variance)
            self.normalize_noise(mid_noise)
            return True
        except Exception as exc:
            logger.critical("AQKC Service Health Check failed configuration validation: %s", exc)
            return False

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self) -> "AQKCService":
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> bool:
        # Returning False ensures runtime exceptions bubble out cleanly
        return False