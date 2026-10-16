"""Tests for quantum circuit construction and basis rotations."""

import unittest
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from qguard.circuits import make_bell_measurement_circuit, inspect_circuit_metrics


class TestCircuits(unittest.TestCase):

    def test_circuit_dimensions(self):
        for obs in ("XX", "YY", "ZZ"):
            qc_unprot = make_bell_measurement_circuit(obs, protected=False)
            self.assertEqual(qc_unprot.num_qubits, 2)
            self.assertEqual(qc_unprot.num_clbits, 2)

            qc_prot = make_bell_measurement_circuit(obs, protected=True)
            self.assertEqual(qc_prot.num_qubits, 3)
            self.assertEqual(qc_prot.num_clbits, 3)

    def test_custom_ports(self):
        qc = make_bell_measurement_circuit("ZZ", protected=True, port_qubits=(1, 3), ancilla_qubit=4)
        self.assertEqual(qc.num_qubits, 5)
        self.assertEqual(qc.num_clbits, 3)

    def test_invalid_observable_raises(self):
        with self.assertRaises(ValueError):
            make_bell_measurement_circuit("XZ")
        with self.assertRaises(ValueError):
            make_bell_measurement_circuit("INVALID")

    def test_circuit_metrics_inspection(self):
        qc = make_bell_measurement_circuit("XX", protected=True)
        metrics = inspect_circuit_metrics(qc)
        self.assertIn("depth", metrics)
        self.assertIn("one_qubit_gates", metrics)
        self.assertIn("two_qubit_gates", metrics)
        self.assertIn("swap_gates", metrics)
        self.assertGreaterEqual(metrics["depth"], 1)
        self.assertGreaterEqual(metrics["two_qubit_gates"], 3)  # 1 prep CX + 2 parity CX

    def test_ideal_state_correlations(self):
        sim = AerSimulator()
        # Test XX: outcomes should be 00 or 11
        qc_xx = make_bell_measurement_circuit("XX", protected=False)
        counts_xx = sim.run(transpile(qc_xx, sim), shots=500, seed_simulator=42).result().get_counts()
        self.assertTrue(all(k in {"00", "11"} for k in counts_xx.keys()))

        # Test YY: outcomes should be 01 or 10 (correlation -1)
        qc_yy = make_bell_measurement_circuit("YY", protected=False)
        counts_yy = sim.run(transpile(qc_yy, sim), shots=500, seed_simulator=42).result().get_counts()
        self.assertTrue(all(k in {"01", "10"} for k in counts_yy.keys()))

        # Test ZZ: outcomes should be 00 or 11 (correlation +1)
        qc_zz = make_bell_measurement_circuit("ZZ", protected=False)
        counts_zz = sim.run(transpile(qc_zz, sim), shots=500, seed_simulator=42).result().get_counts()
        self.assertTrue(all(k in {"00", "11"} for k in counts_zz.keys()))


if __name__ == "__main__":
    unittest.main()
