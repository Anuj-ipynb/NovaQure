from __future__ import annotations

import random

import selfies as sf

from backend.generation.base_mutator import (
    BaseMutator,
)


INSERTION_TOKENS = (
    "[C]",
    "[O]",
    "[N]",
    "[F]",
    "[=C]",
)


class TokenInsertionMutator(BaseMutator):
    """
    Inserts a chemically valid SELFIES token
    at a random position.
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

        insert_index = random.randint(
            0,
            len(tokens)
        )

        token = random.choice(
            INSERTION_TOKENS
        )

        tokens.insert(
            insert_index,
            token,
        )

        return "".join(tokens)