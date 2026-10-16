"""
Q-Guard: Quantum Circuit Construction Module.

Constructs Bell-state preparation circuits, Pauli basis rotations
(XX, YY, ZZ), and ancilla-assisted parity-check detection circuits.
"""

from typing import Any, Dict, Sequence
from qiskit import QuantumCircuit


def make_bell_measurement_circuit(
    observable: str,
    protected: bool = False,
    port_qubits: Sequence[int] = (0, 1),
    ancilla_qubit: int = 2,
) -> QuantumCircuit:
    """
    Create a Bell-state preparation and measurement circuit.

    Data qubits:
        port_qubits[0], port_qubits[1] (default: q0, q1)
    Optional ancilla:
        ancilla_qubit (default: q2)

    Supported Observables:
        'XX', 'YY', 'ZZ'

    Protection Scheme:
        The protected circuit performs an ancilla-based ZZ parity check
        (CNOT from q0 -> qa, CNOT from q1 -> qa) followed by measurement.
        This provides detection for bit-flip (X) and bit-phase (Y) errors,
        but does NOT detect phase-flip (Z) errors as Z commutes with ZZ.
        This is an educational postselection mechanism, NOT a complete
        quantum error-correction code (QECC).
    """
    if observable not in {"XX", "YY", "ZZ"}:
        raise ValueError(
            f"Invalid observable: '{observable}'. Must be one of: 'XX', 'YY', 'ZZ'"
        )

    q0, q1 = port_qubits[0], port_qubits[1]

    if protected:
        qa = ancilla_qubit
        total_qubits = max(q0, q1, qa) + 1
        qc = QuantumCircuit(total_qubits, 3)
    else:
        total_qubits = max(q0, q1) + 1
        qc = QuantumCircuit(total_qubits, 2)

    # Step 1: Prepare Bell state |Phi+> = (|00> + |11>) / sqrt(2)
    qc.h(q0)
    qc.cx(q0, q1)

    # Step 2: Ancilla-assisted ZZ parity measurement (if protected)
    if protected:
        qc.barrier()
        qc.cx(q0, qa)
        qc.cx(q1, qa)
        qc.barrier()

    # Step 3: Measurement basis rotation
    if observable == "XX":
        qc.h(q0)
        qc.h(q1)
    elif observable == "YY":
        qc.sdg(q0)
        qc.h(q0)
        qc.sdg(q1)
        qc.h(q1)
    elif observable == "ZZ":
        pass  # Standard computational basis

    qc.barrier()

    # Step 4: Measure data qubits into classical bits 0 and 1
    qc.measure(q0, 0)
    qc.measure(q1, 1)

    # Step 5: Measure ancilla into classical bit 2 (if protected)
    if protected:
        qc.measure(qa, 2)

    return qc


def inspect_circuit_metrics(circuit: QuantumCircuit) -> Dict[str, Any]:
    """
    Extract physical execution metrics from a transpiled or uncompiled circuit.
    """
    depth = circuit.depth()
    one_qubit_count = 0
    two_qubit_count = 0
    swap_count = 0
    gate_counts: Dict[str, int] = {}
    active_qubits = set()

    for instruction in circuit.data:
        op = instruction.operation
        name = op.name

        if name in {"barrier", "measure"}:
            continue

        gate_counts[name] = gate_counts.get(name, 0) + 1

        for q in instruction.qubits:
            active_qubits.add(circuit.find_bit(q).index)

        num_q = op.num_qubits
        if num_q == 1:
            one_qubit_count += 1
        elif num_q == 2:
            two_qubit_count += 1
            if name == "swap":
                swap_count += 1

    return {
        "depth": depth,
        "one_qubit_gates": one_qubit_count,
        "two_qubit_gates": two_qubit_count,
        "swap_gates": swap_count,
        "total_operations": sum(gate_counts.values()),
        "active_qubits": len(active_qubits),
        "gate_breakdown": gate_counts,
    }