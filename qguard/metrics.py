"""
Q-Guard: Quantum Metrics and Statistical Analysis Module.

Provides expectation value calculation, Bell-state fidelity estimation,
rigorous statistical uncertainty propagation, and threshold verification.
"""

import math
from typing import Any, Dict, Tuple


def filter_counts(
    counts: Dict[str, int],
    protected: bool = False,
) -> Tuple[Dict[str, int], int, int, float]:
    """
    Parse measurement counts and perform postselection filtering.

    Parameters:
        counts: Dictionary of bitstring to count.
        protected: If True, postselect on ancilla bit == '0' (c2 in c2c1c0).

    Returns:
        (accepted_counts, accepted_shots, total_shots, acceptance_rate)
    """
    total_shots = sum(counts.values())
    if total_shots == 0:
        return {}, 0, 0, 0.0

    accepted_counts: Dict[str, int] = {}
    accepted_shots = 0
    expected_bits = 3 if protected else 2

    for raw_key, num in counts.items():
        bits = raw_key.replace(" ", "")
        if len(bits) != expected_bits or any(b not in "01" for b in bits):
            raise ValueError(
                f"Invalid measurement bitstring '{raw_key}'. Expected {expected_bits} bits."
            )

        if protected:
            ancilla_bit = bits[0]
            if ancilla_bit != "0":
                continue  # Discard rejected shot
            data_bits = bits[1:]
        else:
            data_bits = bits

        accepted_counts[data_bits] = accepted_counts.get(data_bits, 0) + num
        accepted_shots += num

    acceptance_rate = accepted_shots / total_shots if total_shots > 0 else 0.0
    return accepted_counts, accepted_shots, total_shots, acceptance_rate


def expectation_from_counts(counts: Dict[str, int], observable: str) -> float:
    """
    Calculate two-qubit Pauli correlation from 2-bit measurement counts.
    Even parity ('00', '11') -> +1
    Odd parity ('01', '10') -> -1
    """
    if observable not in {"XX", "YY", "ZZ"}:
        raise ValueError(f"Invalid observable: '{observable}'. Must be 'XX', 'YY', or 'ZZ'")

    total = sum(counts.values())
    if total == 0:
        raise ValueError("Cannot calculate expectation from zero measurement counts.")

    weighted_sum = 0
    for bitstring, count in counts.items():
        bits = bitstring.replace(" ", "")
        if len(bits) != 2 or any(b not in "01" for b in bits):
            raise ValueError(f"Expected exactly 2 measured data bits, got: '{bitstring}'")

        parity = 1 if bits[0] == bits[1] else -1
        weighted_sum += parity * count

    return weighted_sum / total


def observable_uncertainty(counts: Dict[str, int], observable: str) -> float:
    """
    Calculate the statistical standard error of the mean correlation.
    For eigenvalue outcomes in {-1, +1}, Var(M) = 1 - <M>^2.
    Standard error sigma_M = sqrt(Var(M) / N).
    """
    total = sum(counts.values())
    if total <= 1:
        return 0.0

    exp = expectation_from_counts(counts, observable)
    variance = max(0.0, 1.0 - (exp ** 2))
    return math.sqrt(variance / total)


def bell_fidelity(xx: float, yy: float, zz: float) -> float:
    """
    Calculate Bell-state fidelity with target |Phi+> = (|00> + |11>) / sqrt(2).
    F = (1 + <XX> - <YY> + <ZZ>) / 4
    Clipped to [0.0, 1.0].
    """
    fidelity = (1.0 + xx - yy + zz) / 4.0
    return max(0.0, min(1.0, fidelity))


def fidelity_uncertainty(sigma_xx: float, sigma_yy: float, sigma_zz: float) -> float:
    """
    Propagate independent observable uncertainties to Bell-state fidelity.
    sigma_F = (1/4) * sqrt(sigma_xx^2 + sigma_yy^2 + sigma_zz^2)
    """
    sum_sq = (sigma_xx ** 2) + (sigma_yy ** 2) + (sigma_zz ** 2)
    return 0.25 * math.sqrt(sum_sq)


def fidelity_from_correlations(correlations: Dict[str, float]) -> float:
    """
    Helper for backward compatibility: calculate Bell fidelity from correlation map.
    """
    required = {"XX", "YY", "ZZ"}
    missing = required - correlations.keys()
    if missing:
        raise ValueError(f"Missing required correlations: {sorted(missing)}")

    return bell_fidelity(
        correlations["XX"],
        correlations["YY"],
        correlations["ZZ"],
    )


def evaluate_threshold(fidelity: float, uncertainty: float, threshold: float = 0.5) -> Dict[str, Any]:
    """
    Evaluate the statistical entanglement decision criterion:
    F - 2 * sigma_F > threshold

    Returns:
        Dictionary with criterion results and confidence margin.
    """
    f_minus_2sigma = fidelity - (2.0 * uncertainty)
    margin = f_minus_2sigma - threshold
    passed = bool(f_minus_2sigma > threshold)

    return {
        "threshold": threshold,
        "fidelity": fidelity,
        "uncertainty": uncertainty,
        "f_minus_2sigma": round(f_minus_2sigma, 5),
        "margin": round(margin, 5),
        "passed": passed,
    }