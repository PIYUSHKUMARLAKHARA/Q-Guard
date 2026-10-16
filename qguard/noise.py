"""
Q-Guard: Physical Noise Modeling Module.

Constructs realistic Qiskit Aer NoiseModel instances based on
processor configuration (depolarizing and readout error channels).
"""

from typing import Any, Dict, List
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    ReadoutError,
)


STANDARD_1Q_GATES: List[str] = [
    "id", "x", "y", "z", "h", "s", "sdg", "t", "tdg", "sx", "rz"
]


def build_noise_model(processor: Dict[str, Any]) -> NoiseModel:
    r"""
    Build a Qiskit Aer NoiseModel for a given processor specification.

    Assumptions & Architecture:
    1. Single-Qubit Depolarizing:
       Uniform depolarizing channel applied to standard single-qubit gates.
       Channel: E(rho) = (1 - p1) rho + (p1 / 3) sum_{P in {X, Y, Z}} P rho P
    2. Two-Qubit Depolarizing:
       Depolarizing channel applied to CNOT ('cx') operations.
       Channel: E(rho) = (1 - p2) rho + (p2 / 15) sum_{P in {I, X, Y, Z}^2 \ {II}} P rho P
    3. Readout Errors:
       Symmetric classical bit-flip probability matrix applied at measurement:
       [[1 - pr, pr], [pr, 1 - pr]]
    4. Edge / Gate Specificity:
       If edge-specific errors are supplied under 'edge_errors', they take precedence;
       otherwise uniform all-qubit errors are applied.
    """
    noise_model = NoiseModel()

    p1 = float(processor.get("single_qubit_depolarizing", 0.0))
    p2 = float(processor.get("two_qubit_depolarizing", 0.0))
    pr = float(processor.get("readout_error", 0.0))

    # Validate probabilities
    for label, val in [("p1", p1), ("p2", p2), ("pr", pr)]:
        if not 0.0 <= val <= 1.0:
            raise ValueError(f"Error rate '{label}' must be in range [0, 1], got {val}")

    # 1-Qubit depolarizing
    if p1 > 0:
        err1 = depolarizing_error(p1, 1)
        noise_model.add_all_qubit_quantum_error(err1, STANDARD_1Q_GATES)

    # 2-Qubit depolarizing (check if edge-specific is provided)
    edge_errors = processor.get("edge_errors", None)
    if edge_errors and isinstance(edge_errors, dict):
        for edge_str, err_rate in edge_errors.items():
            rate = float(err_rate)
            if rate > 0:
                q0, q1 = map(int, edge_str.split("-"))
                err2 = depolarizing_error(rate, 2)
                noise_model.add_quantum_error(err2, "cx", [q0, q1])
                noise_model.add_quantum_error(err2, "cx", [q1, q0])
    elif p2 > 0:
        err2 = depolarizing_error(p2, 2)
        noise_model.add_all_qubit_quantum_error(err2, ["cx"])

    # Readout errors
    if pr > 0:
        readout_matrix = [
            [1.0 - pr, pr],
            [pr, 1.0 - pr],
        ]
        ro_err = ReadoutError(readout_matrix)
        noise_model.add_all_qubit_readout_error(ro_err)

    return noise_model
