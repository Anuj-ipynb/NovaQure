import pytest

from backend.evaluation.nqre_service import NQREService


@pytest.fixture
def nqre():
    return NQREService()


def test_reliability_range(nqre):
    """Reliability score should be in [0, 100]."""
    result = nqre.evaluate(
        corrected_energy=-5.0, variance=0.3, noise_score=20.0, convergence=0.8
    )
    assert 0.0 <= result.reliability_score <= 100.0


def test_perfect_inputs_high_reliability(nqre):
    """Low variance + low noise + high convergence → high reliability."""
    result = nqre.evaluate(
        corrected_energy=-5.0, variance=0.0, noise_score=0.0, convergence=1.0
    )
    assert result.reliability_score >= 90.0


def test_bad_inputs_low_reliability(nqre):
    """High variance + high noise + low convergence → low reliability."""
    result = nqre.evaluate(
        corrected_energy=-5.0, variance=0.9, noise_score=90.0, convergence=0.05
    )
    assert result.reliability_score < 50.0


def test_confidence_bounded(nqre):
    """Confidence should be clamped to [0, 100]."""
    result = nqre.evaluate(
        corrected_energy=-5.0, variance=0.5, noise_score=50.0, convergence=0.5
    )
    assert 0.0 <= result.confidence_score <= 100.0


def test_negative_variance_raises(nqre):
    """Negative variance should raise ValueError."""
    with pytest.raises(ValueError):
        nqre.evaluate(
            corrected_energy=-5.0, variance=-0.1, noise_score=20.0, convergence=0.8
        )


def test_convergence_out_of_range_raises(nqre):
    """Convergence outside [0, 1] should raise ValueError."""
    with pytest.raises(ValueError):
        nqre.evaluate(
            corrected_energy=-5.0, variance=0.3, noise_score=20.0, convergence=1.5
        )


def test_health_check_passes(nqre):
    """Health check should pass with valid configuration."""
    assert nqre.health_check() is True
