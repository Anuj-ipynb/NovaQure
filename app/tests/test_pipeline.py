from app.services.optimization_pipeline import OptimizationPipeline
from app.services.ranking_service import MoleculeScore


def test_pipeline():
    molecules = [
        MoleculeScore("mol1", 0.7, 0.6, -8.0, 0.9),
        MoleculeScore("mol2", 0.5, 0.5, -5.0, 0.6),
        MoleculeScore("mol3", 0.8, 0.7, -6.0, 0.85),
    ]

    pipeline = OptimizationPipeline()
    history = pipeline.run(molecules, iterations=2)

    assert len(history) == 2
    assert "iteration" in history[0]
    assert "results" in history[0]
    