"""Tests for configuration, topology, and routing validation."""

import unittest
from qguard.validation import (
    validate_topology,
    validate_processor_config,
    calculate_shortest_distance,
)


class TestValidation(unittest.TestCase):

    def test_valid_topology(self):
        topo = validate_topology(qubits=4, edges=[[0, 1], [1, 2], [2, 3]])
        self.assertTrue(topo["is_connected"])
        self.assertEqual(topo["connected_components"], 1)
        self.assertEqual(topo["edges_count"], 3)
        self.assertAlmostEqual(topo["average_degree"], 1.5)

    def test_disconnected_topology(self):
        topo = validate_topology(qubits=4, edges=[[0, 1], [2, 3]])
        self.assertFalse(topo["is_connected"])
        self.assertEqual(topo["connected_components"], 2)

    def test_self_loop_raises(self):
        with self.assertRaises(ValueError):
            validate_topology(qubits=3, edges=[[0, 0], [0, 1]])

    def test_out_of_bounds_edge_raises(self):
        with self.assertRaises(ValueError):
            validate_topology(qubits=3, edges=[[0, 3]])

    def test_insufficient_qubits_raises(self):
        with self.assertRaises(ValueError):
            validate_topology(qubits=1, edges=[])

    def test_validate_processor_config(self):
        valid_config = {
            "shots": 1024,
            "seed": 42,
            "processors": [
                {
                    "name": "TestProc",
                    "qubits": 4,
                    "port_qubits": [0, 1],
                    "ancilla_qubit": 2,
                    "edges": [[0, 1], [1, 2], [2, 3]],
                    "single_qubit_depolarizing": 0.001,
                    "two_qubit_depolarizing": 0.01,
                    "readout_error": 0.01,
                }
            ],
        }
        res = validate_processor_config(valid_config)
        self.assertEqual(res["shots"], 1024)

    def test_ancilla_overlap_raises(self):
        bad_config = {
            "processors": [
                {
                    "name": "BadProc",
                    "qubits": 3,
                    "port_qubits": [0, 1],
                    "ancilla_qubit": 1,  # overlaps with port qubit!
                    "edges": [[0, 1], [1, 2]],
                }
            ]
        }
        with self.assertRaises(ValueError):
            validate_processor_config(bad_config)

    def test_shortest_distance(self):
        proc = {"qubits": 4, "edges": [[0, 1], [1, 2], [2, 3]]}
        self.assertEqual(calculate_shortest_distance(proc, 0, 1), 1)
        self.assertEqual(calculate_shortest_distance(proc, 0, 2), 2)
        self.assertEqual(calculate_shortest_distance(proc, 0, 3), 3)
        self.assertEqual(calculate_shortest_distance(proc, 2, 2), 0)


if __name__ == "__main__":
    unittest.main()
