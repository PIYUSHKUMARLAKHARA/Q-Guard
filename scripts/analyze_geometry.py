"""
Q-Guard: Processor Topology and Geometry Analysis Script.

Analyzes coupling graph connectivity, vertex degrees, and physical error rates.
"""

import json
from pathlib import Path
import sys
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from qguard.validation import validate_topology

CONFIG_PATH = ROOT_DIR / "config" / "processors.json"
OUTPUT_PATH = ROOT_DIR / "outputs" / "geometry_analysis.csv"


def main():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration not found: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = json.load(f)

    processors = config.get("processors", [])
    if not processors:
        raise ValueError("No processors found in processors.json")

    results = []
    for proc in processors:
        qubits = int(proc["qubits"])
        edges = proc.get("edges", [])
        topo = validate_topology(qubits, edges)

        results.append({
            "processor": proc["name"],
            "qubits": topo["qubits"],
            "edges": topo["edges_count"],
            "average_degree": round(topo["average_degree"], 5),
            "maximum_degree": topo["maximum_degree"],
            "connected_components": topo["connected_components"],
            "is_connected": topo["is_connected"],
            "single_qubit_depolarizing": proc.get("single_qubit_depolarizing", 0.0),
            "two_qubit_depolarizing": proc.get("two_qubit_depolarizing", 0.0),
            "readout_error": proc.get("readout_error", 0.0),
        })

    df = pd.DataFrame(results)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n" + "=" * 75)
    print("Q-Guard: Processor Geometry & Topology Analysis")
    print("=" * 75)
    print(df.to_string(index=False))
    print(f"\nSaved geometry analysis to: {OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    main()
