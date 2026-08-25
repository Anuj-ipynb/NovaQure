"""
NovaQure

ReAct Agent — LangChain Tool Definitions

Defines LangChain-compatible tools that the ReAct agent can invoke during
its autonomous reasoning loop.  Each tool wraps an existing NovaQure
service so that the agent has access to the full evaluation and refinement
pipeline without duplicating logic.

Tools
-----
- EvaluateMolecule : computes QED, SA, Lipinski, VQE energy, NQRE reliability
- MutateMolecule  : applies SELFIES-level structural mutations
- RankCandidates  : ranks a batch of scored molecules
- ExplainMolecule : generates plain-language XAI summaries

Author:
    NovaQure Agent Team
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from langchain_core.tools import Tool

from backend.evaluation.evaluation_service import EvaluationService
from backend.generation.mutation_engine import MutationEngine
from backend.generation.selfies_converter import selfies_to_smiles
from app.services.ranking_service import RankingService, MoleculeScore
from app.services.explanation_service import ExplanationService

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Shared singleton instances (created once, re-used across tool calls)
# ------------------------------------------------------------------

_evaluator = None
_mutator = None
_ranker = None
_explainer = None


def _get_evaluator() -> EvaluationService:
    global _evaluator
    if _evaluator is None:
        _evaluator = EvaluationService()
    return _evaluator


def _get_mutator() -> MutationEngine:
    global _mutator
    if _mutator is None:
        _mutator = MutationEngine()
    return _mutator


def _get_ranker() -> RankingService:
    global _ranker
    if _ranker is None:
        _ranker = RankingService()
    return _ranker


def _get_explainer() -> ExplanationService:
    global _explainer
    if _explainer is None:
        _explainer = ExplanationService()
    return _explainer


# ------------------------------------------------------------------
# Tool: EvaluateMolecule
# ------------------------------------------------------------------

def _evaluate_molecule(input_str: str) -> str:
    """
    Evaluate a molecule given its SMILES string and quantum telemetry.

    Expected JSON input::

        {
            "smiles": "CCO",
            "energy": -0.85,
            "variance": 0.12,
            "noise": 0.08,
            "convergence": 0.93
        }

    Returns a JSON string with QED, SA, Lipinski, affinity,
    corrected energy, noise score, reliability, and confidence.
    """
    try:
        params = json.loads(input_str)
        result = _get_evaluator().evaluate(
            smiles=params["smiles"],
            energy=params.get("energy", -0.85),
            variance=params.get("variance", 0.12),
            noise=params.get("noise", 0.08),
            convergence=params.get("convergence", 0.93),
        )
        return json.dumps(result.model_dump(), indent=2)
    except Exception as exc:
        logger.error("[EvaluateMolecule] %s", exc)
        return json.dumps({"error": str(exc)})


# ------------------------------------------------------------------
# Tool: MutateMolecule
# ------------------------------------------------------------------

def _mutate_molecule(input_str: str) -> str:
    """
    Apply a structural mutation to a SELFIES molecule.

    Expected JSON input::

        {
            "selfies": "[C][C][O]",
            "strategy": "replacement"   // optional
        }

    Returns the mutated SELFIES string and its decoded SMILES.
    """
    try:
        params = json.loads(input_str)
        selfies_string = params["selfies"]
        strategy = params.get("strategy")
        mutated_selfies = _get_mutator().mutate(selfies_string, strategy=strategy)
        mutated_smiles = selfies_to_smiles(mutated_selfies)
        return json.dumps({
            "mutated_selfies": mutated_selfies,
            "mutated_smiles": mutated_smiles,
        })
    except Exception as exc:
        logger.error("[MutateMolecule] %s", exc)
        return json.dumps({"error": str(exc)})


# ------------------------------------------------------------------
# Tool: RankCandidates
# ------------------------------------------------------------------

def _rank_candidates(input_str: str) -> str:
    """
    Rank a list of scored molecules.

    Expected JSON input — an array of objects::

        [
            {
                "molecule_id": "...",
                "qed": 0.7,
                "sa": 2.3,
                "affinity": -6.1,
                "reliability": 78.5
            }
        ]

    Returns a JSON array sorted by final_score descending with ranks.
    """
    try:
        items = json.loads(input_str)
        scores = [
            MoleculeScore(
                molecule_id=item["molecule_id"],
                qed=item["qed"],
                sa=item["sa"],
                affinity=item["affinity"],
                reliability=item["reliability"],
            )
            for item in items
        ]
        ranked = _get_ranker().rank(scores)
        return json.dumps(ranked, indent=2)
    except Exception as exc:
        logger.error("[RankCandidates] %s", exc)
        return json.dumps({"error": str(exc)})


# ------------------------------------------------------------------
# Tool: ExplainMolecule
# ------------------------------------------------------------------

def _explain_molecule(input_str: str) -> str:
    """
    Generate a plain-language explanation for a scored molecule.

    Expected JSON input::

        {
            "components": {
                "qed": 0.7,
                "affinity_score": 0.6,
                "reliability_score": 0.8
            }
        }
    """
    try:
        molecule_data = json.loads(input_str)
        explanation = _get_explainer().generate(molecule_data)
        return json.dumps(explanation, indent=2)
    except Exception as exc:
        logger.error("[ExplainMolecule] %s", exc)
        return json.dumps({"error": str(exc)})


# ------------------------------------------------------------------
# Public API — build the list of LangChain tools
# ------------------------------------------------------------------

def build_react_tools() -> List[Tool]:
    """
    Construct and return the full set of LangChain Tools
    available to the NovaQure ReAct agent.
    """

    evaluate_tool = Tool(
        name="EvaluateMolecule",
        func=_evaluate_molecule,
        description=(
            "Evaluate a molecule. Input must be a JSON string with keys: "
            "'smiles' (str), 'energy' (float), 'variance' (float), "
            "'noise' (float), 'convergence' (float). Returns JSON with "
            "QED, SA, Lipinski, affinity, corrected energy, noise score, "
            "reliability, and confidence."
        ),
    )

    mutate_tool = Tool(
        name="MutateMolecule",
        func=_mutate_molecule,
        description=(
            "Mutate a molecule for structural refinement. Input must be a "
            "JSON string with key 'selfies' (str) and optional 'strategy' "
            "(str: 'replacement', 'insertion', 'deletion', 'branch'). "
            "Returns JSON with mutated_selfies and mutated_smiles."
        ),
    )

    rank_tool = Tool(
        name="RankCandidates",
        func=_rank_candidates,
        description=(
            "Rank a batch of molecules by composite score. Input must be "
            "a JSON array of objects with keys: 'molecule_id', 'qed', "
            "'sa', 'affinity', 'reliability'. Returns JSON array sorted "
            "by final_score with assigned ranks."
        ),
    )

    explain_tool = Tool(
        name="ExplainMolecule",
        func=_explain_molecule,
        description=(
            "Generate a plain-language explanation for a scored molecule. "
            "Input must be a JSON string with a 'components' dict containing "
            "'qed', 'affinity_score', 'reliability_score'."
        ),
    )

    return [evaluate_tool, mutate_tool, rank_tool, explain_tool]
