"""Tests for physical noise modeling and simulator builder."""

import unittest
from qiskit_aer.noise import NoiseModel
from qguard.noise import build_noise_model
from qguard.simulator import build_simulator


class TestNoise(unittest.TestCase):

    def setUp(self):
        self.processor = {
            "name": "TestProcessor",
            "qubits": 5,
            "edges": [[0, 1], [1, 2], [2, 3], [3, 4]],
            "single_qubit_depolarizing": 0.001,
            "two_qubit_depolarizing": 0.015,
            "readout_error": 0.02,
        }

    def test_build_noise_model(self):
        model = build_noise_model(self.processor)
        self.assertIsInstance(model, NoiseModel)

    def test_invalid_error_rates_raise(self):
        bad_proc = dict(self.processor, single_qubit_depolarizing=1.5)
        with self.assertRaises(ValueError):
            build_noise_model(bad_proc)

        bad_proc2 = dict(self.processor, two_qubit_depolarizing=-0.05)
        with self.assertRaises(ValueError):
            build_noise_model(bad_proc2)

    def test_zero_noise_model(self):
        zero_proc = dict(
            self.processor,
            single_qubit_depolarizing=0.0,
            two_qubit_depolarizing=0.0,
            readout_error=0.0,
        )
        model = build_noise_model(zero_proc)
        self.assertIsInstance(model, NoiseModel)

    def test_build_simulator_ideal_vs_noisy(self):
        sim_ideal = build_simulator(self.processor, noisy=False)
        self.assertIsNotNone(sim_ideal)

        sim_noisy = build_simulator(self.processor, noisy=True)
        self.assertIsNotNone(sim_noisy)

    def test_edge_specific_noise(self):
        edge_proc = dict(
            self.processor,
            edge_errors={"0-1": 0.02, "1-2": 0.03}
        )
        model = build_noise_model(edge_proc)
        self.assertIsInstance(model, NoiseModel)


if __name__ == "__main__":
    unittest.main()
