import pandas as pd
from pathlib import Path

output_dir = Path("outputs")
csv_path = output_dir / "multi_seed_validation.csv"

if not csv_path.exists():
    from scripts.validate_seeds import run_multi_seed_validation
    run_multi_seed_validation()

# Load multi-seed experiment results
df = pd.read_csv(csv_path)

# Separate noisy and protected results
noisy = df[df["experiment"] == "Noisy"].copy()
protected = df[df["experiment"] == "Noisy + Protection"].copy()

comparison = noisy.merge(
    protected,
    on="processor",
    suffixes=("_noisy", "_protected")
)

comparison["fidelity_change"] = (
    comparison["mean_fidelity_protected"]
    - comparison["mean_fidelity_noisy"]
)

comparison["acceptance_loss"] = (
    comparison["mean_acceptance_rate_noisy"]
    - comparison["mean_acceptance_rate_protected"]
)

comparison["fidelity_improved"] = (
    comparison["fidelity_change"] > 0
)

columns = [
    "processor",
    "mean_fidelity_noisy",
    "std_fidelity_noisy",
    "mean_fidelity_protected",
    "std_fidelity_protected",
    "fidelity_change",
    "mean_acceptance_rate_protected",
    "acceptance_loss",
    "fidelity_improved",
]

report = comparison[columns].sort_values("processor")

report.to_csv(
    output_dir / "final_multi_seed_report.csv",
    index=False
)

print("\n=== Q-Guard Final Multi-Seed Report ===")
print(report.round(5).to_string(index=False))
print("\nSaved: outputs/final_multi_seed_report.csv")
