"""Tests for experiment pipeline and circuit execution."""

import unittest
from qguard.experiments import (
    build_coupling_map,
    compile_circuit,
    run_single_experiment,
    correlation_from_counts,
)
from qguard.circuits import make_bell_measurement_circuit


class TestExperiments(unittest.TestCase):

    def setUp(self):
        self.processor = {
            "name": "TestProcessor",
            "id": "test_processor",
            "qubits": 4,
            "port_qubits": [0, 1],
            "ancilla_qubit": 2,
            "edges": [[0, 1], [1, 2], [2, 3]],
            "single_qubit_depolarizing": 0.001,
            "two_qubit_depolarizing": 0.015,
            "readout_error": 0.01,
        }

    def test_coupling_map_construction(self):
        cmap = build_coupling_map(self.processor)
        self.assertIsNotNone(cmap)
        # Bidirectional: 3 undirected edges -> 6 directed edges
        self.assertEqual(len(cmap.get_edges()), 6)

    def test_compile_circuit(self):
        qc = make_bell_measurement_circuit("XX", protected=False)
        compiled = compile_circuit(qc, self.processor, seed=42)
        self.assertGreater(compiled.depth(), 0)

    def test_run_single_experiment_ideal(self):
        res = run_single_experiment(
            processor=self.processor,
            experiment_name="Ideal",
            noisy=False,
            protected=False,
            shots=512,
            seed=42,
        )
        self.assertAlmostEqual(res["fidelity_estimate"], 1.0, places=3)
        self.assertTrue(res["threshold_passed"])
        self.assertEqual(res["acceptance_rate"], 1.0)
        self.assertEqual(res["discarded_shots_avg"], 0)

    def test_run_single_experiment_noisy(self):
        res = run_single_experiment(
            processor=self.processor,
            experiment_name="Noisy",
            noisy=True,
            protected=False,
            shots=512,
            seed=42,
        )
        self.assertGreater(res["fidelity_estimate"], 0.5)
        self.assertLess(res["fidelity_estimate"], 1.0)
        self.assertTrue(res["threshold_passed"])

    def test_run_single_experiment_protected(self):
        res = run_single_experiment(
            processor=self.processor,
            experiment_name="Noisy + Protection",
            noisy=True,
            protected=True,
            shots=512,
            seed=42,
        )
        self.assertGreater(res["fidelity_estimate"], 0.5)
        self.assertGreaterEqual(res["acceptance_rate"], 0.5)
        self.assertGreater(res["average_circuit_depth"], 4.0)

    def test_correlation_from_counts_compat(self):
        counts = {"00": 300, "11": 300}
        corr, acc, tot = correlation_from_counts(counts, protected=False)
        self.assertAlmostEqual(corr, 1.0)
        self.assertEqual(acc, 600)
        self.assertEqual(tot, 600)


if __name__ == "__main__":
    unittest.main()
