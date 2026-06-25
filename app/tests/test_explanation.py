from app.services.explanation_service import ExplanationService


def test_explanation():
    service = ExplanationService()

    sample_input = {
        "molecule_id": "mol1",
        "final_score": 85,
        "components": {
            "qed": 0.8,
            "sa": 0.6,
            "affinity_score": 0.75,
            "reliability": 0.9
        }
    }

    result = service.generate(sample_input)

    assert "reason" in result
    assert "score_breakdown" in result
    