from __future__ import annotations

import numpy as np
import pennylane as qml

from backend.generation.generation_config import (
    GenerationConfig
)

from backend.generation.latent_space import (
    LatentVector
)

from backend.sampling.base_sampler import (
    BaseSampler
)


class QCBMSampler(
    BaseSampler
):
    """
    QCBM latent sampler powered by PennyLane.

    Uses an 8-qubit parameterized quantum circuit to perform quantum-inspired
    perturbation and sampling in the latent space.
    """

    def __init__(self):
        # Create an 8-qubit quantum simulator device
        self.num_qubits = 8
        self.dev = qml.device("default.qubit", wires=self.num_qubits)

        # Define the QNode
        @qml.qnode(self.dev)
        def _circuit(inputs, weights):
            # Encode inputs into RY rotations
            for i in range(self.num_qubits):
                qml.RY(inputs[i], wires=i)
            # Entangle qubits
            for i in range(self.num_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
            qml.CNOT(wires=[self.num_qubits - 1, 0])
            # Apply parameterized weights
            for i in range(self.num_qubits):
                qml.RX(weights[i], wires=i)
            return [qml.expval(qml.PauliZ(i)) for i in range(self.num_qubits)]

        self.circuit = _circuit
        # Static weights for deterministic quantum sampling
        self.weights = np.array([np.pi / 4] * self.num_qubits)

    def sample(
        self,
        latent_vector: list[float]
    ) -> list[float]:

        arr = np.array(latent_vector, dtype=float)
        # Ensure we can reshape to (N, 8). If length is not a multiple of 8, pad with zeros
        original_length = len(arr)
        pad_size = (self.num_qubits - (original_length % self.num_qubits)) % self.num_qubits
        if pad_size > 0:
            arr = np.pad(arr, (0, pad_size), mode='constant')

        chunks = arr.reshape(-1, self.num_qubits)
        samples = []

        # Run 5 quantum perturbation steps to generate diversity
        for step in range(5):
            perturbed_chunks = []
            for chunk in chunks:
                # scale inputs to avoid angle saturation, map chunk to [-pi, pi]
                inputs = np.clip(chunk, -1.0, 1.0) * np.pi
                # Execute the quantum circuit to get expectation values
                quantum_noise = np.array(self.circuit(inputs, self.weights))
                # Perturb the original chunk using the quantum expectation values
                perturbed_chunk = chunk + GenerationConfig.LATENT_NOISE_STD * quantum_noise
                perturbed_chunks.append(perturbed_chunk)
            
            flat_perturbed = np.concatenate(perturbed_chunks)[:original_length]
            samples.append(flat_perturbed)

        mean_vector = np.mean(
            samples,
            axis=0
        )

        return (
            LatentVector(
                mean_vector
            )
            .normalize()
            .to_list()
        )

