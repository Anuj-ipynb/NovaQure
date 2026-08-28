from __future__ import annotations

import random

from backend.generation.generation_config import (
    GenerationConfig,
)

from backend.generation.token_mutator import (
    TokenMutator,
)

from backend.generation.token_insertion_mutator import (
    TokenInsertionMutator,
)

from backend.generation.token_deletion_mutator import (
    TokenDeletionMutator,
)

from backend.generation.branch_mutator import (
    BranchMutator,
)


class MutationEngine:

    def __init__(self) -> None:

        self._mutators = {
            "replacement": TokenMutator(),
            "insertion": TokenInsertionMutator(),
            "deletion": TokenDeletionMutator(),
            "branch": BranchMutator(),
        }

    def register_mutator(
        self,
        name: str,
        mutator,
    ) -> None:

        self._mutators[name] = mutator

    def mutate(
        self,
        selfies_string: str,
        strategy: str | None = None,
    ) -> str:

        if strategy is None:

            names = list(
                GenerationConfig
                .MUTATION_WEIGHTS
                .keys()
            )

            weights = list(
                GenerationConfig
                .MUTATION_WEIGHTS
                .values()
            )

            strategy = random.choices(
                names,
                weights=weights,
                k=1,
            )[0]

        if strategy not in self._mutators:

            raise ValueError(
                f"Unknown mutation strategy: {strategy}"
            )

        return self._mutators[
            strategy
        ].mutate(
            selfies_string
        )

    def available_mutators(
        self,
    ) -> list[str]:

        return sorted(
            self._mutators.keys()
        )