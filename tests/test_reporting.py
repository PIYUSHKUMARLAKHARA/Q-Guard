"""Tests for report generation and visualization functions."""

import tempfile
import unittest
from pathlib import Path
import pandas as pd

from qguard.reporting import (
    generate_summary_csv,
    generate_protection_analysis_csv,
    generate_visualizations,
    generate_final_markdown_report,
)


class TestReporting(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.out_dir = Path(self.temp_dir.name)

        # Mock experiment results dataframe
        self.mock_df = pd.DataFrame([
            {
                "processor": "ProcA",
                "experiment": "Ideal",
                "fidelity_estimate": 1.0,
                "fidelity_uncertainty": 0.0,
                "f_minus_2sigma": 1.0,
                "threshold_passed": True,
                "acceptance_rate": 1.0,
                "discarded_shots_avg": 0,
                "average_circuit_depth": 4.0,
                "average_two_qubit_gates": 1.0,
                "protected": False,
            },
            {
                "processor": "ProcA",
                "experiment": "Noisy",
                "fidelity_estimate": 0.94,
                "fidelity_uncertainty": 0.003,
                "f_minus_2sigma": 0.934,
                "threshold_passed": True,
                "acceptance_rate": 1.0,
                "discarded_shots_avg": 0,
                "average_circuit_depth": 4.0,
                "average_two_qubit_gates": 1.0,
                "protected": False,
            },
            {
                "processor": "ProcA",
                "experiment": "Noisy + Protection",
                "fidelity_estimate": 0.91,
                "fidelity_uncertainty": 0.004,
                "f_minus_2sigma": 0.902,
                "threshold_passed": True,
                "acceptance_rate": 0.92,
                "discarded_shots_avg": 320,
                "average_circuit_depth": 9.0,
                "average_two_qubit_gates": 6.0,
                "protected": True,
            },
        ])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_summary_csv_generation(self):
        summary_path = self.out_dir / "summary.csv"
        df_summary = generate_summary_csv(self.mock_df, summary_path)
        self.assertTrue(summary_path.exists())
        self.assertIn("fidelity_change", df_summary.columns)

    def test_protection_analysis_csv_generation(self):
        analysis_path = self.out_dir / "analysis.csv"
        df_analysis = generate_protection_analysis_csv(self.mock_df, analysis_path)
        self.assertTrue(analysis_path.exists())
        self.assertIn("extra_two_qubit_gates", df_analysis.columns)
        self.assertAlmostEqual(df_analysis.loc["ProcA", "fidelity_change"], -0.03)

    def test_markdown_report_generation(self):
        report_path = self.out_dir / "final_report.md"
        generate_final_markdown_report(self.mock_df, report_path)
        self.assertTrue(report_path.exists())
        content = report_path.read_text(encoding="utf-8")
        self.assertIn("Q-Guard: Final Experimental Report", content)
        self.assertIn("ProcA", content)

    def test_visualizations_generation(self):
        plots = generate_visualizations(self.mock_df, self.out_dir)
        self.assertGreaterEqual(len(plots), 3)
        for p in plots:
            self.assertTrue(p.exists())
            self.assertGreater(p.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
