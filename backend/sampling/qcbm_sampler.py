from __future__ import annotations

import logging
import os
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

logger = logging.getLogger(__name__)


class QCBMSampler(
    BaseSampler
):
    """
    QCBM latent sampler powered by PennyLane.

    Uses an 8-qubit parameterized quantum circuit to perform quantum-inspired
    perturbation and sampling in the latent space.

    The circuit parameters can be trained via ``train()`` to match a target
    latent distribution, or left at their defaults for deterministic sampling.
    """

    DEFAULT_WEIGHTS_PATH = "models/qcbm_weights.npy"

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
        # Default weights (used if no trained checkpoint is loaded)
        self.weights = np.array([np.pi / 4] * self.num_qubits)
        self._trained = False

        # Auto-load trained weights if available
        if os.path.exists(self.DEFAULT_WEIGHTS_PATH):
            self.load_weights(self.DEFAULT_WEIGHTS_PATH)

    # -----------------------------------------------------------------
    # Training
    # -----------------------------------------------------------------

    def train(
        self,
        target_vectors: np.ndarray,
        epochs: int = 100,
        lr: float = 0.1,
    ) -> list[float]:
        """Train circuit parameters to match a target latent distribution.

        Uses Maximum Mean Discrepancy (MMD) with RBF kernel as the loss
        function, optimised via PennyLane's AdamOptimizer.

        Parameters
        ----------
        target_vectors : np.ndarray
            Array of shape ``(N, D)`` containing latent vectors from the
            encoder.  Only the first ``num_qubits`` dimensions of each
            vector are used per chunk.
        epochs : int
            Number of optimisation steps.
        lr : float
            Learning rate for Adam.

        Returns
        -------
        list[float]
            Loss values per epoch.
        """
        # Prepare target chunks (take first num_qubits dims, clip to [-1,1])
        targets = np.array(target_vectors, dtype=float)
        if targets.ndim == 1:
            targets = targets.reshape(1, -1)
        # Use first num_qubits columns
        target_chunks = np.clip(targets[:, :self.num_qubits], -1.0, 1.0)

        # Trainable parameters
        params = np.array(self.weights, requires_grad=True)
        opt = qml.AdamOptimizer(stepsize=lr)

        def rbf_kernel(x, y, sigma=1.0):
            """Radial basis function kernel."""
            diff = x - y
            return np.exp(-np.dot(diff, diff) / (2.0 * sigma ** 2))

        def mmd_loss(weights):
            """Maximum Mean Discrepancy between circuit outputs and targets."""
            # Sample circuit outputs for a subset of targets
            n_samples = min(len(target_chunks), 32)
            indices = np.random.choice(len(target_chunks), n_samples, replace=False)

            circuit_outputs = []
            for idx in indices:
                inputs = target_chunks[idx] * np.pi
                out = np.array(self.circuit(inputs, weights))
                circuit_outputs.append(out)

            # Compute MMD components
            loss = 0.0
            for i in range(n_samples):
                for j in range(n_samples):
                    loss += rbf_kernel(circuit_outputs[i], circuit_outputs[j])
                    loss += rbf_kernel(target_chunks[indices[i]], target_chunks[indices[j]])
                    loss -= 2.0 * rbf_kernel(circuit_outputs[i], target_chunks[indices[j]])
            loss = loss / (n_samples ** 2)
            return loss

        losses = []
        for epoch in range(epochs):
            params, loss_val = opt.step_and_cost(mmd_loss, params)
            losses.append(float(loss_val))
            if (epoch + 1) % 10 == 0 or epoch == 0:
                logger.info("QCBM train epoch %d/%d — MMD loss: %.6f", epoch + 1, epochs, float(loss_val))

        self.weights = np.array(params, requires_grad=False)
        self._trained = True
        logger.info("QCBM training complete. Final loss: %.6f", losses[-1])
        return losses

    # -----------------------------------------------------------------
    # Weight persistence
    # -----------------------------------------------------------------

    def save_weights(self, path: str | None = None) -> str:
        """Save trained circuit parameters to a .npy file."""
        path = path or self.DEFAULT_WEIGHTS_PATH
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        np.save(path, self.weights)
        logger.info("QCBM weights saved to %s", path)
        return path

    def load_weights(self, path: str | None = None) -> None:
        """Load circuit parameters from a .npy file."""
        path = path or self.DEFAULT_WEIGHTS_PATH
        if not os.path.exists(path):
            logger.warning("QCBM weights file not found: %s", path)
            return
        self.weights = np.load(path)
        self._trained = True
        logger.info("QCBM weights loaded from %s", path)

    # -----------------------------------------------------------------
    # Sampling (unchanged API)
    # -----------------------------------------------------------------

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
