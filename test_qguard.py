import unittest

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from qguard.circuits import make_bell_measurement_circuit
from qguard.metrics import bell_fidelity, fidelity_from_correlations
from qguard.experiments import correlation_from_counts


class TestQGuardCircuits(unittest.TestCase):

    def test_ideal_circuit_creation(self):
        for observable in ("XX", "YY", "ZZ"):
            circuit = make_bell_measurement_circuit(
                observable,
                protected=False,
            )

            self.assertIsInstance(circuit, QuantumCircuit)
            self.assertEqual(circuit.num_qubits, 2)
            self.assertEqual(circuit.num_clbits, 2)

    def test_protected_circuit_creation(self):
        for observable in ("XX", "YY", "ZZ"):
            circuit = make_bell_measurement_circuit(
                observable,
                protected=True,
            )

            self.assertEqual(circuit.num_qubits, 3)
            self.assertEqual(circuit.num_clbits, 3)

    def test_invalid_observable(self):
        with self.assertRaises(ValueError):
            make_bell_measurement_circuit("XY")

    def test_ideal_bell_fidelity(self):
        fidelity = bell_fidelity(
            xx=1.0,
            yy=-1.0,
            zz=1.0,
        )

        self.assertAlmostEqual(fidelity, 1.0)

    def test_zero_correlations_fidelity(self):
        fidelity = fidelity_from_correlations(
            {
                "XX": 0.0,
                "YY": 0.0,
                "ZZ": 0.0,
            }
        )

        self.assertAlmostEqual(fidelity, 0.25)

    def test_fidelity_is_clipped(self):
        self.assertEqual(
            bell_fidelity(10.0, -10.0, 10.0),
            1.0,
        )

        self.assertEqual(
            bell_fidelity(-10.0, 10.0, -10.0),
            0.0,
        )

    def test_ideal_xx_measurement(self):
        circuit = make_bell_measurement_circuit(
            "XX",
            protected=False,
        )

        simulator = AerSimulator()

        compiled = transpile(
            circuit,
            simulator,
            seed_transpiler=42,
        )

        result = simulator.run(
            compiled,
            shots=1024,
            seed_simulator=42,
        ).result()

        counts = result.get_counts()

        # For |Phi+>, XX outcomes should have equal bits.
        self.assertEqual(set(counts.keys()), {"00", "11"})

    def test_protected_ancilla_accepts_ideal_state(self):
        circuit = make_bell_measurement_circuit(
            "ZZ",
            protected=True,
        )

        simulator = AerSimulator()

        compiled = transpile(
            circuit,
            simulator,
            seed_transpiler=42,
        )

        result = simulator.run(
            compiled,
            shots=1024,
            seed_simulator=42,
        ).result()

        counts = result.get_counts()

        # Classical bit order is c2c1c0.
        # Ancilla is c2 and should be zero for the ideal state.
        self.assertTrue(
            all(key.replace(" ", "")[0] == "0" for key in counts)
        )

        
    def test_protected_postselection_rejects_all_shots(self):
        counts = {
            "100": 50,
            "111": 50,
        }

        with self.assertRaises(ValueError):
            correlation_from_counts(
                counts,
                protected=True,
            )

    def test_protected_postselection_accepts_ancilla_zero(self):
        counts = {
            "000": 30,
            "011": 20,
            "100": 40,
            "111": 10,
        }

        correlation, accepted, total = correlation_from_counts(
            counts,
            protected=True,
        )

        self.assertEqual(accepted, 50)
        self.assertEqual(total, 100)
        self.assertAlmostEqual(correlation, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)