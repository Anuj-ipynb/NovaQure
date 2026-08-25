"""
NovaQure

Agentic Orchestrator Service

Wraps the ReAct agent in a service that the pipeline can call to run
multi-iteration autonomous drug candidate optimisation loops.

The orchestrator:
1. Receives a batch of generated molecules.
2. Feeds each molecule through the ReAct agent (evaluate → decide → mutate/keep).
3. Collects kept candidates and routes refined/regenerated ones into the next
   iteration.
4. Returns the final ranked candidate list with full audit traces.

Author:
    NovaQure Agent Team
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from backend.agents.react_agent import build_agent, DeterministicReActAgent
from backend.generation.mutation_engine import MutationEngine
from backend.generation.molecule_generator import build_molecule
from backend.generation.selfies_converter import selfies_to_smiles
from backend.generation.generation_service import GenerationService

logger = logging.getLogger(__name__)


class AgenticOrchestratorService:
    """
    Multi-iteration ReAct orchestration engine.

    Manages the closed-loop feedback cycle between molecule generation,
    quantum-classical evaluation, autonomous agent decisions, and structural
    refinement.
    """

    def __init__(
        self,
        max_iterations: int = 3,
    ) -> None:
        self.max_iterations = max_iterations
        self.agent: DeterministicReActAgent = build_agent()
        self.mutator = MutationEngine()
        self.generator = GenerationService()
        logger.info(
            "AgenticOrchestratorService initialised (max_iterations=%d).",
            max_iterations,
        )

    # ---------------------------------------------------------------
    # Core Orchestration Loop
    # ---------------------------------------------------------------

    def run(
        self,
        molecules: list,
        energy: float = -0.85,
        variance: float = 0.12,
        noise: float = 0.08,
        convergence: float = 0.93,
    ) -> Dict[str, Any]:
        """
        Execute the full agentic optimisation loop.

        Parameters
        ----------
        molecules
            Initial batch of generated molecule objects
            (must have ``.smiles``, ``.selfies``, ``.molecule_id``,
            ``.latent_vector`` attributes).
        energy, variance, noise, convergence
            Quantum telemetry inputs forwarded to the evaluation pipeline.

        Returns
        -------
        dict
            ``final_candidates`` — list of agent result dicts for kept molecules.
            ``iterations_completed`` — how many loop passes ran.
            ``total_evaluated`` — total molecules processed across all iterations.
            ``traces`` — full ReAct trace list for every molecule touched.
        """

        current_molecules = list(molecules)
        final_candidates: List[Dict] = []
        all_traces: List[Dict] = []
        total_evaluated = 0

        for iteration in range(self.max_iterations):
            if not current_molecules:
                logger.info("No molecules remaining at iteration %d; stopping.", iteration)
                break

            logger.info(
                "=== Agentic Iteration %d/%d — %d candidates ===",
                iteration + 1,
                self.max_iterations,
                len(current_molecules),
            )

            next_generation = []

            for mol in current_molecules:
                total_evaluated += 1

                # Run the ReAct agent for this molecule
                result = self.agent.run(
                    smiles=mol.smiles,
                    selfies=mol.selfies,
                    molecule_id=mol.molecule_id,
                    energy=energy,
                    variance=variance,
                    noise=noise,
                    convergence=convergence,
                )

                result["iteration"] = iteration
                all_traces.append(result.get("react_trace", {}))

                decision = result["decision"]

                if decision == "keep" or iteration == self.max_iterations - 1:
                    final_candidates.append(result)

                elif decision == "refine":
                    mutated_selfies = result.get("mutated_selfies")
                    if mutated_selfies:
                        try:
                            mutated_smiles = selfies_to_smiles(mutated_selfies)
                            next_mol = build_molecule(
                                smiles=mutated_smiles,
                                source="agent-refinement",
                                latent=mol.latent_vector,
                                iteration=iteration + 1,
                            )
                            next_generation.append(next_mol)
                        except Exception as exc:
                            logger.warning(
                                "Mutation decode failed for %s: %s; keeping original.",
                                mol.molecule_id, exc,
                            )
                            final_candidates.append(result)
                    else:
                        # Mutation did not produce a valid output; keep the original
                        final_candidates.append(result)

                elif decision == "regenerate":
                    try:
                        replacements = self.generator.run()
                        if replacements:
                            next_generation.append(replacements[0])
                    except Exception as exc:
                        logger.warning("Regeneration failed: %s; keeping original.", exc)
                        final_candidates.append(result)

            current_molecules = next_generation

        # Sort final candidates by reliability descending
        final_candidates.sort(
            key=lambda c: c.get("evaluation", {}).get("reliability_score", 0.0),
            reverse=True,
        )

        # Assign final ranks
        for idx, candidate in enumerate(final_candidates):
            candidate["final_rank"] = idx + 1

        summary = {
            "final_candidates": final_candidates,
            "iterations_completed": min(iteration + 1, self.max_iterations) if molecules else 0,
            "total_evaluated": total_evaluated,
            "traces": all_traces,
        }

        logger.info(
            "Agentic orchestration complete: %d candidates kept, %d total evaluated.",
            len(final_candidates),
            total_evaluated,
        )

        return summary
