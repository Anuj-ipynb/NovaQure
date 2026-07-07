"""
NovaQure

AQKC Configuration

Configuration values for the
Adaptive Quantum Knowledge Correction (AQKC) algorithm.

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

# ==========================================================
# Numerical Stability
# ==========================================================

EPSILON: float = 1e-8

# ==========================================================
# Normalization Ranges
# ==========================================================

MIN_VARIANCE: float = 0.0
MAX_VARIANCE: float = 1.0

MIN_NOISE: float = 0.0
MAX_NOISE: float = 1.0

# ==========================================================
# AQKC Weights
# ==========================================================

ENERGY_WEIGHT: float = 0.60
VARIANCE_WEIGHT: float = 0.25
NOISE_WEIGHT: float = 0.15

# ==========================================================
# Correction Constraints
# ==========================================================

MAX_CORRECTION_FACTOR: float = 0.20

# ==========================================================
# Noise Score Scaling
# ==========================================================

NOISE_SCORE_SCALE: float = 100.0