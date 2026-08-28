import pytest

from app.services.ranking_service import RankingService, MoleculeScore


@pytest.fixture
def ranker():
    return RankingService()


def _make_score(mol_id="mol_1", qed=0.7, sa=3.0, affinity=-7.0, reliability=80.0):
    return MoleculeScore(
        molecule_id=mol_id, qed=qed, sa=sa, affinity=affinity, reliability=reliability
    )


def test_rank_ordering(ranker):
    """Molecules should be sorted descending by final_score."""
    mols = [
        _make_score("mol_a", qed=0.3, sa=5.0, affinity=-3.0, reliability=40.0),
        _make_score("mol_b", qed=0.9, sa=1.5, affinity=-9.0, reliability=95.0),
    ]
    ranked = ranker.rank(mols)
    assert ranked[0]["rank"] == 1
    assert ranked[0]["final_score"] >= ranked[1]["final_score"]


def test_sa_inversion(ranker):
    """Lower SA (easier synthesis) should yield a higher score contribution."""
    easy = ranker.compute_score(_make_score(sa=1.0))
    hard = ranker.compute_score(_make_score(sa=10.0))
    assert easy["final_score"] > hard["final_score"]


def test_affinity_normalization(ranker):
    """Affinity of -10 should normalize to 1.0, 0 to 0.0."""
    assert ranker.normalize_affinity(-10.0) == 1.0
    assert ranker.normalize_affinity(0.0) == 0.0


def test_single_molecule(ranker):
    """Ranking should work with a single molecule."""
    ranked = ranker.rank([_make_score()])
    assert len(ranked) == 1
    assert ranked[0]["rank"] == 1


def test_reliability_normalization(ranker):
    """Reliability > 1 should be divided by 100."""
    score = ranker.compute_score(_make_score(reliability=85.0))
    assert score["components"]["reliability"] == 0.85


def test_score_components_present(ranker):
    """Result should contain all expected component keys."""
    score = ranker.compute_score(_make_score())
    assert "qed" in score["components"]
    assert "sa" in score["components"]
    assert "affinity_score" in score["components"]
    assert "reliability" in score["components"]
