import pytest

from app.services.amde_service import AMDEService


@pytest.fixture
def amde():
    return AMDEService()


def _wrap(qed=0.8, affinity=0.7, reliability=0.8):
    """Create a molecule dict in the format AMDE expects."""
    return {
        "components": {
            "qed": qed,
            "affinity_score": affinity,
            "reliability_score": reliability,
            "reliability": reliability,
        }
    }


def test_keep_decision(amde):
    """All metrics passing thresholds → decision should be 'keep'."""
    result = amde.decide(_wrap(qed=0.8, affinity=0.7, reliability=0.8))
    assert result["decision"] == "keep"


def test_refine_on_low_qed(amde):
    """Low QED → decision should be 'refine'."""
    result = amde.decide(_wrap(qed=0.3, affinity=0.7, reliability=0.8))
    assert result["decision"] == "refine"


def test_refine_on_low_affinity(amde):
    """Low affinity → decision should be 'refine'."""
    result = amde.decide(_wrap(qed=0.8, affinity=0.2, reliability=0.8))
    assert result["decision"] == "refine"


def test_regenerate_on_low_reliability(amde):
    """Low reliability → decision should be 'regenerate'."""
    result = amde.decide(_wrap(qed=0.8, affinity=0.7, reliability=0.2))
    assert result["decision"] == "regenerate"


def test_confidence_calculation(amde):
    """Confidence should be the mean of assessment scores."""
    result = amde.decide(_wrap(qed=0.6, affinity=0.6, reliability=0.6))
    assert isinstance(result["confidence"], float)
    assert 0.0 <= result["confidence"] <= 1.0


def test_react_traces_present(amde):
    """The 'thoughts' key should contain reasoning traces."""
    result = amde.decide(_wrap())
    assert "thoughts" in result
    assert len(result["thoughts"]) >= 6  # at least 2 per assessment (thought + action)


def test_recommendation_present(amde):
    """A recommendation string should always be present."""
    result = amde.decide(_wrap())
    assert "recommendation" in result
    assert isinstance(result["recommendation"], str)
    assert len(result["recommendation"]) > 0
