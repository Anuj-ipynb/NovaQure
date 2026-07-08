from __future__ import annotations

import random

import selfies as sf

from backend.generation.base_mutator import (
    BaseMutator,
)


BRANCH_TOKENS = (
    "[Branch1]",
)


class BranchMutator(BaseMutator):
    """
    Inserts a branch token into a SELFIES string.

    Branch mutations modify molecular topology
    rather than replacing existing atoms.
    """

    def mutate(
        self,
        selfies_string: str,
    ) -> str:

        tokens = list(
            sf.split_selfies(
                selfies_string
            )
        )

        if not tokens:
            return selfies_string

        index = random.randint(
            0,
            len(tokens)
        )

        tokens.insert(
            index,
            random.choice(
                BRANCH_TOKENS
            ),
        )

        return "".join(tokens)  