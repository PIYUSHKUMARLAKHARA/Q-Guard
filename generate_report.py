import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT_DIR / "outputs"

RESULTS_PATH = OUTPUT_DIR / "results.csv"
GEOMETRY_PATH = OUTPUT_DIR / "geometry_analysis.csv"


def load_results():
    if not RESULTS_PATH.exists():
        raise FileNotFoundError(
            "results.csv not found. Run python main.py first."
        )

    df = pd.read_csv(RESULTS_PATH)

    required_columns = {
        "processor",
        "experiment",
        "fidelity_estimate",
        "acceptance_rate",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns in results.csv: {missing}"
        )

    if df.empty:
        raise ValueError("results.csv is empty")

    return df


def validate_results(df):
    print("\n--- Result Validation ---")

    print("Total experiment rows:", len(df))
    print("Processors:", df["processor"].nunique())
    print("Experiments:", df["experiment"].nunique())

    print("\nRows per processor:")

    print(
        df.groupby("processor")["experiment"]
        .count()
        .to_string()
    )

    if not df["fidelity_estimate"].between(0, 1).all():
        raise ValueError(
            "Fidelity estimates must be between 0 and 1."
        )

    if not df["acceptance_rate"].between(0, 1).all():
        raise ValueError(
            "Acceptance rates must be between 0 and 1."
        )

    print("\nFidelity and acceptance-rate ranges are valid.")


def create_fidelity_plot(df):
    pivot = df.pivot(
        index="processor",
        columns="experiment",
        values="fidelity_estimate",
    )

    ax = pivot.plot(
        kind="bar",
        figsize=(11, 6),
        ylim=(0, 1.05),
    )

    ax.set_title("Q-Guard: Fidelity Comparison")
    ax.set_xlabel("Processor")
    ax.set_ylabel("Estimated Bell-State Fidelity")
    ax.legend(title="Experiment")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()

    path = OUTPUT_DIR / "final_fidelity_comparison.png"

    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Saved:", path)


def create_acceptance_plot(df):
    pivot = df.pivot(
        index="processor",
        columns="experiment",
        values="acceptance_rate",
    )

    ax = pivot.plot(
        kind="bar",
        figsize=(11, 6),
        ylim=(0, 1.05),
    )

    ax.set_title("Q-Guard: Acceptance Rate Comparison")
    ax.set_xlabel("Processor")
    ax.set_ylabel("Acceptance Rate")
    ax.legend(title="Experiment")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()

    path = OUTPUT_DIR / "final_acceptance_comparison.png"

    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Saved:", path)


def create_summary_report(df):
    summary = df.pivot(
        index="processor",
        columns="experiment",
        values="fidelity_estimate",
    )

    required = {"Noisy", "Noisy + Protection"}

    if required.issubset(summary.columns):
        summary["protection_fidelity_change"] = (
            summary["Noisy + Protection"] - summary["Noisy"]
        )

    output_path = OUTPUT_DIR / "final_summary.csv"

    summary.to_csv(output_path)

    print("\n--- Final Fidelity Summary ---")
    print(summary.to_string())

    print("\nSaved:", output_path)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_results()

    validate_results(df)

    create_fidelity_plot(df)
    create_acceptance_plot(df)
    create_summary_report(df)

    print("\nQ-Guard report generation completed.")


if __name__ == "__main__":
    main()