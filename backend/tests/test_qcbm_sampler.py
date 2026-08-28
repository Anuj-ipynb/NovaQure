import pytest
import numpy as np
import os
import tempfile

from backend.sampling.qcbm_sampler import QCBMSampler


def test_sample_output_length():
    """Output should have the same length as the input vector."""
    sampler = QCBMSampler()
    input_vec = [0.1] * 128
    output = sampler.sample(input_vec)
    assert len(output) == len(input_vec)


def test_sample_output_type():
    """Output should be a list of floats."""
    sampler = QCBMSampler()
    output = sampler.sample([0.5] * 16)
    assert isinstance(output, list)
    assert all(isinstance(x, float) for x in output)


def test_sample_produces_different_output():
    """Quantum perturbation should change the vector (not return identity)."""
    sampler = QCBMSampler()
    input_vec = [0.3] * 8
    output = sampler.sample(input_vec)
    assert output != input_vec


def test_sample_output_normalized():
    """Output vector should be L2-normalized."""
    sampler = QCBMSampler()
    output = sampler.sample([1.0] * 128)
    norm = np.linalg.norm(output)
    assert abs(norm - 1.0) < 1e-6, f"Output norm is {norm}, expected 1.0"


def test_sample_handles_non_multiple_of_8():
    """Should handle input lengths that are not multiples of 8."""
    sampler = QCBMSampler()
    output = sampler.sample([0.2] * 13)
    assert len(output) == 13


def test_save_load_weights():
    """Save and load should preserve the exact weight values."""
    sampler = QCBMSampler()
    sampler.weights = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])

    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test_weights.npy")
        sampler.save_weights(path)

        sampler2 = QCBMSampler()
        sampler2.load_weights(path)
        np.testing.assert_array_almost_equal(sampler.weights, sampler2.weights)
        assert sampler2._trained is True


def test_load_nonexistent_weights():
    """Loading from a missing path should not crash."""
    sampler = QCBMSampler()
    original_weights = sampler.weights.copy()
    sampler.load_weights("nonexistent_path_xyz.npy")
    np.testing.assert_array_equal(sampler.weights, original_weights)
