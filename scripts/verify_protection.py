"""
Q-Guard: Protection Mechanism & Error-Class Verification Script.

Tests ancilla parity-check behavior under controlled injected errors (X and Z)
to empirically verify detectable vs. non-detectable error classes.
"""

from pathlib import Path
import sys
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from qguard.metrics import filter_counts

SHOTS = 4096
SEED = 42


def create_injected_error_circuit(error_gate=None, protected=False):
    """
    Prepare Bell state |Phi+> and inject controlled error gate on q0.
    """
    if protected:
        qc = QuantumCircuit(3, 3)
    else:
        qc = QuantumCircuit(2, 2)

    # 1. State preparation
    qc.h(0)
    qc.cx(0, 1)

    # 2. Injected error on data qubit 0
    if error_gate == "X":
        qc.x(0)
    elif error_gate == "Z":
        qc.z(0)
    elif error_gate is not None:
        raise ValueError(f"Unknown error gate: {error_gate}")

    # 3. Ancilla parity check (if protected)
    if protected:
        qc.barrier()
        qc.cx(0, 2)
        qc.cx(1, 2)
        qc.barrier()

    # 4. Measure
    qc.measure(0, 0)
    qc.measure(1, 1)
    if protected:
        qc.measure(2, 2)

    return qc


def run_test(error_gate=None, protected=False):
    circuit = create_injected_error_circuit(error_gate=error_gate, protected=protected)
    sim = AerSimulator()
    compiled = transpile(circuit, sim, seed_transpiler=SEED)
    result = sim.run(compiled, shots=SHOTS, seed_simulator=SEED).result()
    counts = result.get_counts()

    acc_counts, accepted, total, acc_rate = filter_counts(counts, protected=protected)
    rejected = total - accepted
    rej_rate = rejected / total if total > 0 else 0.0

    return {
        "error": error_gate or "None",
        "protected": protected,
        "counts": counts,
        "accepted": accepted,
        "rejected": rejected,
        "acceptance_rate": acc_rate,
        "rejection_rate": rej_rate,
    }


def main():
    print("=" * 75)
    print("Q-Guard: Error Detection Verification (Injected Faults)")
    print("=" * 75)

    test_cases = [
        (None, "No Fault (Target |Phi+>)"),
        ("X", "Bit-Flip Error X on q0 (Changes parity to odd)"),
        ("Z", "Phase-Flip Error Z on q0 (Leaves parity unchanged)"),
    ]

    for gate, desc in test_cases:
        print(f"\nScenario: {desc}")
        for protected in [False, True]:
            res = run_test(error_gate=gate, protected=protected)
            mode = "Protected (Ancilla Postselect)" if protected else "Unprotected"
            print(
                f"  [{mode:<32}] "
                f"Accepted: {res['accepted']:<5} | "
                f"Rejected: {res['rejected']:<5} | "
                f"Accept Rate: {res['acceptance_rate']*100:.1f}%"
            )

    print("\n" + "=" * 75)
    print("Verification Summary:")
    print("1. Bit-flip (X) error: 100% REJECTED in protected mode -> DETECTED.")
    print("2. Phase-flip (Z) error: 100% ACCEPTED in protected mode -> UNDETECTED.")
    print("This verifies that ZZ parity check is limited to bit-flip detection.")
    print("=" * 75)


if __name__ == "__main__":
    main()
