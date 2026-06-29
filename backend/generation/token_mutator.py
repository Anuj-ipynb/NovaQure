from __future__ import annotations

import random

import selfies as sf

from backend.generation.base_mutator import (
    BaseMutator,
)


REPLACEMENT_TOKENS = (
    "[C]",
    "[O]",
    "[N]",
    "[F]",
    "[=C]",
)


class TokenMutator(BaseMutator):
    """
    Performs token replacement on a SELFIES string.

    This operator replaces an existing token with
    another chemically valid atom/bond token.
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

        index = random.randrange(
            len(tokens)
        )

        tokens[index] = random.choice(
            REPLACEMENT_TOKENS
        )

        return "".join(tokens)