"""Q-Guard quantum error-detection experiment package."""

from .circuits import make_bell_measurement_circuit, inspect_circuit_metrics
from .metrics import (
    bell_fidelity,
    expectation_from_counts,
    filter_counts,
    observable_uncertainty,
    fidelity_uncertainty,
    evaluate_threshold,
    fidelity_from_correlations,
)
from .noise import build_noise_model
from .simulator import build_simulator
from .validation import validate_processor_config, validate_topology
from .experiments import run_experiments, run_single_experiment, load_config

__all__ = [
    "make_bell_measurement_circuit",
    "inspect_circuit_metrics",
    "bell_fidelity",
    "expectation_from_counts",
    "filter_counts",
    "observable_uncertainty",
    "fidelity_uncertainty",
    "evaluate_threshold",
    "fidelity_from_correlations",
    "build_noise_model",
    "build_simulator",
    "validate_processor_config",
    "validate_topology",
    "run_experiments",
    "run_single_experiment",
    "load_config",
]
