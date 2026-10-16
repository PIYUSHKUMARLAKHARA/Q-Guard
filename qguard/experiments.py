"""
Q-Guard: Experiment Pipeline Module.

Executes quantum experiments across ideal, noisy, and protected configurations,
recording comprehensive fidelity, uncertainty, and physical resource metrics.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd

from qiskit import transpile
from qiskit.transpiler import CouplingMap

from .circuits import make_bell_measurement_circuit, inspect_circuit_metrics
from .metrics import (
    filter_counts,
    expectation_from_counts,
    observable_uncertainty,
    bell_fidelity,
    fidelity_uncertainty,
    evaluate_threshold,
)
from .simulator import build_simulator
from .validation import (
    validate_processor_config,
    validate_topology,
    calculate_shortest_distance,
)
from .reporting import (
    generate_summary_csv,
    generate_protection_analysis_csv,
    generate_visualizations,
    generate_final_markdown_report,
)

OBSERVABLES = ("XX", "YY", "ZZ")
DEFAULT_BASIS_GATES = [
    "id", "x", "y", "z", "h", "s", "sdg", "t", "tdg", "sx", "cx"
]


def correlation_from_counts(counts: Dict[str, int], protected: bool = False) -> Tuple[float, int, int]:
    """
    Calculate parity correlation from measurement counts (for backward compatibility).
    """
    total = sum(counts.values())
    if total == 0:
        raise ValueError("The simulator returned no measurement shots.")

    acc_counts, accepted, total_shots, acc_rate = filter_counts(counts, protected=protected)
    if accepted == 0:
        raise ValueError(
            "No shots passed ancilla postselection. Cannot calculate a valid conditional correlation."
        )

    corr = expectation_from_counts(acc_counts, "ZZ")
    return corr, accepted, total_shots



def load_config(path: str = "config/processors.json") -> Dict[str, Any]:
    """Load and validate processor configuration JSON file."""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    # Perform structural and physical constraint validation
    validate_processor_config(config)
    return config


def build_coupling_map(processor: Dict[str, Any]) -> Optional[CouplingMap]:
    """Build a bidirectional Qiskit CouplingMap from processor coupling edges."""
    edges = processor.get("edges", [])
    if not edges:
        return None

    directed = []
    for edge in edges:
        u, v = int(edge[0]), int(edge[1])
        directed.append([u, v])
        directed.append([v, u])

    return CouplingMap(couplinglist=directed)


def compile_circuit(circuit, processor: Dict[str, Any], seed: int = 42):
    """
    Transpile circuit to processor coupling topology and supported basis gates.
    """
    coupling_map = build_coupling_map(processor)
    basis_gates = processor.get("basis_gates", DEFAULT_BASIS_GATES)

    compiled = transpile(
        circuit,
        coupling_map=coupling_map,
        basis_gates=basis_gates,
        optimization_level=1,
        seed_transpiler=seed,
    )
    return compiled


def run_single_experiment(
    processor: Dict[str, Any],
    experiment_name: str,
    noisy: bool,
    protected: bool,
    shots: int,
    seed: int,
) -> Dict[str, Any]:
    """
    Execute three-basis Bell state measurements (XX, YY, ZZ) for a single experiment case.
    """
    correlations: Dict[str, float] = {}
    uncertainties: Dict[str, float] = {}
    accepted_shots_list: List[int] = []
    total_shots_list: List[int] = []
    depths: List[int] = []
    one_q_counts: List[int] = []
    two_q_counts: List[int] = []
    swap_counts: List[int] = []

    port_qubits = processor.get("port_qubits", [0, 1])
    ancilla_qubit = processor.get("ancilla_qubit", 2)

    for idx, observable in enumerate(OBSERVABLES):
        current_seed = seed + idx

        # Step 1: Create circuit
        circuit = make_bell_measurement_circuit(
            observable=observable,
            protected=protected,
            port_qubits=port_qubits,
            ancilla_qubit=ancilla_qubit,
        )

        # Step 2: Transpile to processor topology
        compiled = compile_circuit(circuit, processor, seed=current_seed)
        metrics = inspect_circuit_metrics(compiled)

        depths.append(metrics["depth"])
        one_q_counts.append(metrics["one_qubit_gates"])
        two_q_counts.append(metrics["two_qubit_gates"])
        swap_counts.append(metrics["swap_gates"])

        # Step 3: Run simulation
        simulator = build_simulator(processor, noisy=noisy, seed=current_seed)
        result = simulator.run(compiled, shots=shots, seed_simulator=current_seed).result()
        counts = result.get_counts(compiled)

        # Step 4: Postselection filter
        acc_counts, acc_shots, tot_shots, acc_rate = filter_counts(counts, protected=protected)

        accepted_shots_list.append(acc_shots)
        total_shots_list.append(tot_shots)

        if acc_shots == 0:
            correlations[observable] = 0.0
            uncertainties[observable] = 1.0
        else:
            correlations[observable] = expectation_from_counts(acc_counts, observable)
            uncertainties[observable] = observable_uncertainty(acc_counts, observable)

    # Step 5: Fidelity and Uncertainty
    fidelity = bell_fidelity(correlations["XX"], correlations["YY"], correlations["ZZ"])
    sigma_f = fidelity_uncertainty(
        uncertainties["XX"], uncertainties["YY"], uncertainties["ZZ"]
    )
    thresh = evaluate_threshold(fidelity, sigma_f, threshold=0.5)

    total_meas = sum(total_shots_list)
    acc_meas = sum(accepted_shots_list)
    overall_acc_rate = (acc_meas / total_meas) if total_meas > 0 else 0.0
    discarded_avg = round((total_meas - acc_meas) / len(OBSERVABLES))

    return {
        "processor": processor.get("name", "Unknown"),
        "processor_id": processor.get("id", "unknown"),
        "experiment": experiment_name,
        "fidelity_estimate": round(fidelity, 5),
        "fidelity_uncertainty": round(sigma_f, 5),
        "f_minus_2sigma": thresh["f_minus_2sigma"],
        "threshold_passed": thresh["passed"],
        "threshold_margin": thresh["margin"],
        "XX": round(correlations["XX"], 5),
        "YY": round(correlations["YY"], 5),
        "ZZ": round(correlations["ZZ"], 5),
        "sigma_XX": round(uncertainties["XX"], 5),
        "sigma_YY": round(uncertainties["YY"], 5),
        "sigma_ZZ": round(uncertainties["ZZ"], 5),
        "accepted_shots_avg": round(acc_meas / len(OBSERVABLES)),
        "total_shots_avg": round(total_meas / len(OBSERVABLES)),
        "discarded_shots_avg": discarded_avg,
        "acceptance_rate": round(overall_acc_rate, 5),
        "shots_per_observable": shots,
        "average_circuit_depth": round(sum(depths) / len(depths), 2),
        "average_one_qubit_gates": round(sum(one_q_counts) / len(one_q_counts), 2),
        "average_two_qubit_gates": round(sum(two_q_counts) / len(two_q_counts), 2),
        "average_swap_count": round(sum(swap_counts) / len(swap_counts), 2),
        "physical_qubits": int(processor.get("qubits", 0)),
        "noisy": noisy,
        "protected": protected,
        "note": "Illustrative processor profile; validate with official challenge parameters when provided.",
    }


def run_experiments(
    config_path: str = "config/processors.json",
    output_dir: str = "outputs",
) -> pd.DataFrame:
    """Execute full experimental matrix across all configured processors."""
    config = load_config(config_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    shots = int(config.get("shots", 4096))
    base_seed = int(config.get("seed", 42))

    experiment_cases = [
        ("Ideal", False, False),
        ("Noisy", True, False),
        ("Noisy + Protection", True, True),
    ]

    records = []

    for proc_idx, processor in enumerate(config["processors"]):
        name = processor.get("name", "Unknown")
        print(f"\nProcessor: {name}")

        for case_idx, (exp_name, noisy, protected) in enumerate(experiment_cases):
            print(f"  Running {exp_name}...")
            seed = base_seed + (proc_idx * 1000) + (case_idx * 100)

            record = run_single_experiment(
                processor=processor,
                experiment_name=exp_name,
                noisy=noisy,
                protected=protected,
                shots=shots,
                seed=seed,
            )
            records.append(record)
            print(
                f"    Fidelity: {record['fidelity_estimate']:.5f} "
                f"(±{2*record['fidelity_uncertainty']:.5f}) | "
                f"Threshold: {'PASS' if record['threshold_passed'] else 'FAIL'}"
            )

    df = pd.DataFrame(records)

    # 1. Save detailed experiment results
    df.to_csv(out_dir / "experiment_results.csv", index=False)
    # Save results.csv for backward compatibility
    df.to_csv(out_dir / "results.csv", index=False)

    # 2. Generate summary tables
    generate_summary_csv(df, out_dir / "summary_results.csv")
    generate_summary_csv(df, out_dir / "final_summary.csv")  # backward compatibility
    generate_protection_analysis_csv(df, out_dir / "protection_analysis.csv")

    # 3. Generate geometry analysis
    geo_records = []
    for proc in config["processors"]:
        topo = validate_topology(int(proc["qubits"]), proc.get("edges", []))
        geo_records.append({
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
    pd.DataFrame(geo_records).to_csv(out_dir / "geometry_analysis.csv", index=False)

    # 4. Generate visual plots
    generate_visualizations(df, out_dir)

    # 5. Generate final Markdown report
    generate_final_markdown_report(df, out_dir / "final_report.md")

    print(f"\nAll outputs successfully saved to: {out_dir.resolve()}")
    return df
