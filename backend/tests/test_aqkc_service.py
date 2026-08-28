import pytest

from backend.evaluation.aqkc_service import AQKCService
from backend.configs.aqkc_config import MAX_CORRECTION_FACTOR


@pytest.fixture
def aqkc():
    return AQKCService()


def test_correction_factor_bounds(aqkc):
    """Correction factor should never exceed MAX_CORRECTION_FACTOR."""
    factor = aqkc.compute_correction(variance=1.0, noise=1.0)
    assert factor <= MAX_CORRECTION_FACTOR


def test_correction_factor_nonnegative(aqkc):
    """Correction factor should be non-negative for non-negative inputs."""
    factor = aqkc.compute_correction(variance=0.0, noise=0.0)
    assert factor >= 0.0


def test_zne_corrects_energy(aqkc):
    """Corrected energy should differ from raw energy when correction > 0."""
    result = aqkc.correct(energy=-5.0, variance=0.5, noise=0.3)
    assert result.corrected_energy != -5.0


def test_corrected_energy_differs_from_raw(aqkc):
    """ZNE correction should produce a different energy than the raw input."""
    result = aqkc.correct(energy=-5.0, variance=0.5, noise=0.3)
    # E(2) = E(1) * (1 + w*c) — for negative E, E(2) is more negative
    # E(0) = 2*E(1) - E(2) — so corrected is less negative (closer to zero)
    assert result.corrected_energy != -5.0
    assert result.corrected_energy > -5.0  # ZNE pushes toward zero for negative energies


def test_noise_score_range(aqkc):
    """Noise score should be within [0, NOISE_SCORE_SCALE]."""
    result = aqkc.correct(energy=-3.0, variance=0.2, noise=0.5)
    assert 0.0 <= result.noise_score <= 100.0


def test_negative_variance_raises(aqkc):
    """Negative variance should raise ValueError."""
    with pytest.raises(ValueError, match="negative"):
        aqkc.correct(energy=-5.0, variance=-0.1, noise=0.3)


def test_negative_noise_raises(aqkc):
    """Negative noise should raise ValueError."""
    with pytest.raises(ValueError, match="negative"):
        aqkc.correct(energy=-5.0, variance=0.3, noise=-0.1)


def test_health_check_passes(aqkc):
    """Health check should pass with valid configuration."""
    assert aqkc.health_check() is True
