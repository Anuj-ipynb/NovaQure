from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class LatentVector:

    values: np.ndarray

    def normalize(self) -> "LatentVector":

        norm = np.linalg.norm(
            self.values
        )

        if norm > 0:
            self.values = (
                self.values / norm
            )

        return self

    def distance(
        self,
        other: "LatentVector"
    ) -> float:

        return float(
            np.linalg.norm(
                self.values - other.values
            )
        )

    def interpolate(
        self,
        other: "LatentVector",
        alpha: float
    ) -> "LatentVector":

        return LatentVector(
            (
                (1 - alpha)
                * self.values
                +
                alpha
                * other.values
            )
        )

    def perturb(
        self,
        sigma: float
    ) -> "LatentVector":

        noise = np.random.normal(
            0,
            sigma,
            self.values.shape
        )

        return LatentVector(
            self.values + noise
        ).normalize()

    def to_list(self):

        return (
            self.values
            .astype(float)
            .tolist()
        )
