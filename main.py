"""
Q-Guard: Main Entrypoint for Basic Track Experiments.
"""

from qguard.experiments import run_experiments


def main():
    print("=" * 75)
    print("Q-Guard — Quantum Error Detection and Protection Optimizer")
    print("Hackathon Basic Track Execution Pipeline")
    print("NOTE: Processor parameters are illustrative placeholders.")
    print("Replace them with official organizer PDF values before final submission.")
    print("=" * 75)

    results = run_experiments()

    display_cols = [
        "processor",
        "experiment",
        "fidelity_estimate",
        "fidelity_uncertainty",
        "f_minus_2sigma",
        "threshold_passed",
        "XX",
        "YY",
        "ZZ",
        "accepted_shots_avg",
        "acceptance_rate",
    ]

    print("\n" + "=" * 75)
    print("Summary of Results:")
    print("=" * 75)
    print(results[display_cols].to_string(index=False))
    print("\nOutputs generated in 'outputs/':")
    print("  - experiment_results.csv & results.csv")
    print("  - summary_results.csv & protection_analysis.csv")
    print("  - geometry_analysis.csv")
    print("  - fidelity_comparison.png & acceptance_rate.png")
    print("  - circuit_overhead.png & processor_comparison.png")
    print("  - final_report.md")


if __name__ == "__main__":
    main()
