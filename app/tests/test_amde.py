from app.services.amde_service import AMDEService


def test_amde():
    service = AMDEService()

    sample_input = {
        "molecule_id": "mol1",
        "components": {
            "qed": 0.6,
            "sa": 0.5,
            "affinity_score": 0.3,
            "reliability": 0.8
        }
    }

    result = service.decide(sample_input)

    assert "decision" in result
    assert "reason" in result
    assert "confidence" in result
    