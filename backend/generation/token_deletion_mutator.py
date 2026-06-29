from __future__ import annotations

import random

import selfies as sf

from backend.generation.base_mutator import BaseMutator


class TokenDeletionMutator(BaseMutator):
    """
    Removes one token from a SELFIES sequence.

    At least one token is always preserved.
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

        if len(tokens) <= 1:
            return selfies_string

        delete_index = random.randrange(
            len(tokens)
        )

        del tokens[
            delete_index
        ]

        return "".join(tokens)
