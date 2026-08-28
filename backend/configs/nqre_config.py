"""
NovaQure

NQRE Configuration

Configuration values for the NovaQure Reliability
Evaluation (NQRE) algorithm.

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

MIN_CONVERGENCE: float = 0.0
MAX_CONVERGENCE: float = 1.0

MIN_VARIANCE: float = 0.0
MAX_VARIANCE: float = 1.0

MIN_NOISE_SCORE: float = 0.0
MAX_NOISE_SCORE: float = 100.0

# ==========================================================
# Reliability Weights
# (Must sum to 1.0)
# ==========================================================

VARIANCE_WEIGHT: float = 0.40
NOISE_WEIGHT: float = 0.30
CONVERGENCE_WEIGHT: float = 0.30