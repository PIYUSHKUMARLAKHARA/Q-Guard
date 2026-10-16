"""
Q-Guard: Simulator Construction Module.

Creates ideal and noisy Qiskit AerSimulator instances.
"""

from typing import Any, Dict
from qiskit_aer import AerSimulator
from .noise import build_noise_model


def build_simulator(
    processor: Dict[str, Any],
    noisy: bool = True,
    seed: int = 42,
) -> AerSimulator:
    """
    Create an ideal or noisy Qiskit Aer simulator instance.

    Parameters:
        processor: Dictionary of processor parameters.
        noisy: If True, builds and attaches the physical NoiseModel.
        seed: Random seed for simulator reproducibility.
    """
    if not noisy:
        return AerSimulator(seed_simulator=seed)

    noise_model = build_noise_model(processor)

    return AerSimulator(
        noise_model=noise_model,
        seed_simulator=seed,
    )