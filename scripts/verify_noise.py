"""
Q-Guard: Noise Model Verification Script.

Transpiles Bell-state circuits across XX, YY, ZZ observables and compares
ideal vs. noisy measurement counts and gate counts.
"""

import json
from pathlib import Path
import sys
from qiskit import transpile

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from qguard.circuits import make_bell_measurement_circuit
from qguard.simulator import build_simulator

CONFIG_PATH = ROOT_DIR / "config" / "processors.json"


def count_gates(circuit):
    counts = {}
    for instruction in circuit.data:
        name = instruction.operation.name
        counts[name] = counts.get(name, 0) + 1
    return counts


def run_verification():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = json.load(f)

    processor = config["processors"][0]
    shots = int(config.get("shots", 4096))
    seed = int(config.get("seed", 42))

    print("=" * 65)
    print("Q-Guard: Physical Noise Model Verification")
    print(f"Processor: {processor['name']} | Shots: {shots}")
    print("=" * 65)

    for observable in ("XX", "YY", "ZZ"):
        print(f"\nObservable: {observable}")
        circuit = make_bell_measurement_circuit(observable=observable, protected=False)
        compiled = transpile(
            circuit,
            basis_gates=["id", "x", "y", "z", "h", "s", "sdg", "t", "tdg", "sx", "cx"],
            optimization_level=0,
            seed_transpiler=seed,
        )
        print("Transpiled gates:", count_gates(compiled))

        for noisy in (False, True):
            sim = build_simulator(processor=processor, noisy=noisy, seed=seed)
            result = sim.run(compiled, shots=shots, seed_simulator=seed).result()
            counts = result.get_counts()
            total_shots = sum(counts.values())

            label = "Noisy" if noisy else "Ideal"
            print(f"  {label:<7} | Total: {total_shots} | Counts: {counts}")
            assert total_shots == shots, f"Expected {shots} shots, got {total_shots}"

    print("\n" + "=" * 65)
    print("Noise verification check passed.")
    print("=" * 65)


if __name__ == "__main__":
    run_verification()
