"""Automated tests for FastAPI Backend endpoints."""

import sys
from pathlib import Path
import unittest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app


class TestBackendAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("Q-Guard", data["project"])

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("qiskit_version", data)

    def test_get_processors(self):
        response = self.client.get("/api/processors")
        self.assertEqual(response.status_code, 200)
        processors = response.json()
        self.assertGreaterEqual(len(processors), 3)
        names = [p["name"] for p in processors]
        self.assertIn("2016-Inspired", names)
        self.assertIn("Contemporary", names)
        self.assertIn("Hyperbolic-Inspired", names)

    def test_get_processor_by_id(self):
        response = self.client.get("/api/processors/contemporary")
        self.assertEqual(response.status_code, 200)
        proc = response.json()
        self.assertEqual(proc["name"], "Contemporary")
        self.assertEqual(proc["qubits"], 7)

    def test_get_processor_not_found(self):
        response = self.client.get("/api/processors/unknown_chip")
        self.assertEqual(response.status_code, 404)

    def test_get_experiments(self):
        response = self.client.get("/api/experiments")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_summary(self):
        response = self.client.get("/api/results/summary")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_experiments", data)
        self.assertIn("processors", data)

    def test_csv_export(self):
        response = self.client.get("/api/results/export")
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertIn("text/csv", response.headers.get("content-type", ""))

    def test_run_experiment_simulation(self):
        # Run small real experiment through API
        payload = {
            "processor_id": "contemporary",
            "experiment_type": "Ideal",
            "shots": 256,
            "seed": 42,
            "observable": "ALL",
        }
        response = self.client.post("/api/experiments", json=payload)
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertAlmostEqual(res["fidelity_estimate"], 1.0, places=2)
        self.assertTrue(res["threshold_passed"])
        self.assertEqual(res["processor"], "Contemporary")

    def test_run_experiment_invalid_processor(self):
        payload = {
            "processor_id": "nonexistent_chip",
            "experiment_type": "Ideal",
            "shots": 256,
            "seed": 42,
        }
        response = self.client.post("/api/experiments", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_run_experiment_invalid_shots(self):
        payload = {
            "processor_id": "contemporary",
            "experiment_type": "Ideal",
            "shots": 10,  # below minimum (100)
            "seed": 42,
        }
        response = self.client.post("/api/experiments", json=payload)
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
