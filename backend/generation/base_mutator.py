from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseMutator(ABC):

    @abstractmethod
    def mutate(
        self,
        selfies_string: str,
    ) -> str:
        """
        Apply a mutation to a SELFIES string.
        """
        raise NotImplementedError
