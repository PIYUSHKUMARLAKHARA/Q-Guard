"""
Q-Guard: Multi-Seed Statistical Validation Script.

Executes multiple independent random seeds for each processor profile and
experimental condition to evaluate simulation stability and variance.
"""

import csv
from pathlib import Path
import statistics
import sys

# Ensure root directory is on Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from qguard.experiments import load_config, run_single_experiment


def run_multi_seed_validation(
    config_path: Path = ROOT_DIR / "config" / "processors.json",
    output_path: Path = ROOT_DIR / "outputs" / "multi_seed_validation.csv",
    num_seeds: int = 10,
):
    config = load_config(str(config_path))
    shots = int(config.get("shots", 4096))
    base_seed = int(config.get("seed", 42))

    seed_offsets = list(range(num_seeds))
    records = []

    print("\n" + "=" * 80)
    print(f"Q-Guard: Multi-Seed Statistical Validation ({num_seeds} seeds/condition)")
    print("=" * 80)

    for processor in config["processors"]:
        processor_name = processor.get("name", "Unknown")

        for experiment_name, noisy, protected in [
            ("Noisy", True, False),
            ("Noisy + Protection", True, True),
        ]:
            fidelities = []
            acceptance_rates = []
            f_minus_2sigmas = []

            for offset in seed_offsets:
                seed = base_seed + (offset * 13)

                result = run_single_experiment(
                    processor=processor,
                    experiment_name=experiment_name,
                    noisy=noisy,
                    protected=protected,
                    shots=shots,
                    seed=seed,
                )

                fidelities.append(float(result["fidelity_estimate"]))
                acceptance_rates.append(float(result["acceptance_rate"]))
                f_minus_2sigmas.append(float(result["f_minus_2sigma"]))

            mean_fid = statistics.mean(fidelities)
            std_fid = statistics.stdev(fidelities) if len(fidelities) > 1 else 0.0
            mean_acc = statistics.mean(acceptance_rates)
            std_acc = statistics.stdev(acceptance_rates) if len(acceptance_rates) > 1 else 0.0

            record = {
                "processor": processor_name,
                "experiment": experiment_name,
                "runs": len(seed_offsets),
                "shots_per_observable": shots,
                "mean_fidelity": round(mean_fid, 5),
                "std_fidelity": round(std_fid, 5),
                "mean_acceptance_rate": round(mean_acc, 5),
                "std_acceptance_rate": round(std_acc, 5),
                "mean_f_minus_2sigma": round(statistics.mean(f_minus_2sigmas), 5),
                "all_passed_threshold": all(f > 0.5 for f in f_minus_2sigmas),
            }
            records.append(record)

            print(
                f"{processor_name:<20} | {experiment_name:<20} | "
                f"F: {mean_fid:.5f} (SD: {std_fid:.5f}) | "
                f"Acc: {mean_acc*100:.1f}% | "
                f"Threshold: {'PASS' if record['all_passed_threshold'] else 'FAIL'}"
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"\nSaved multi-seed validation results to: {output_path}")
    return records


if __name__ == "__main__":
    run_multi_seed_validation()
