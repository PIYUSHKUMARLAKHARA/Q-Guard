"""
Q-Guard: Protection Analysis Script.

Compares noisy baseline with protected experiments to evaluate
fidelity gain/loss, gate overhead, and postselection trade-offs.
"""

from pathlib import Path
import sys
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from qguard.reporting import generate_protection_analysis_csv

RESULTS_CSV = ROOT_DIR / "outputs" / "results.csv"
OUTPUT_CSV = ROOT_DIR / "outputs" / "protection_analysis.csv"


def main():
    if not RESULTS_CSV.exists():
        alt_path = ROOT_DIR / "outputs" / "experiment_results.csv"
        if alt_path.exists():
            df = pd.read_csv(alt_path)
        else:
            raise FileNotFoundError(f"Results file not found. Run 'python main.py' first.")
    else:
        df = pd.read_csv(RESULTS_CSV)

    analysis = generate_protection_analysis_csv(df, OUTPUT_CSV)

    print("\n" + "=" * 75)
    print("Q-Guard: Protection Analysis (Noisy Baseline vs. Protected)")
    print("=" * 75)
    print(analysis.round(5).to_string())
    print(f"\nSaved analysis to: {OUTPUT_CSV}")
    return analysis


if __name__ == "__main__":
    main()
