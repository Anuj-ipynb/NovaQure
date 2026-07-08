from app.services.ranking_service import RankingService, MoleculeScore


def test_ranking():
    molecules = [
        MoleculeScore("mol1", 0.7, 0.6, -8.0, 0.9),
        MoleculeScore("mol2", 0.5, 0.5, -5.0, 0.6),
        MoleculeScore("mol3", 0.8, 0.7, -6.0, 0.85),
    ]

    service = RankingService()
    ranked = service.rank(molecules)

    assert ranked[0]["rank"] == 1
    assert len(ranked) == 3
    