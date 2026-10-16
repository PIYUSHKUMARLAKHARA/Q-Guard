"""
Q-Guard Experiment Service.

Coordinates experiment execution with qguard quantum simulation engine,
manages result history, and provides analytical summaries.
"""

import asyncio
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional
import uuid
import pandas as pd

# Add repository root to Python path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from qguard.experiments import (
    load_config,
    run_single_experiment,
    run_experiments,
)
from qguard.validation import validate_topology

CONFIG_PATH = REPO_ROOT / "config" / "processors.json"
OUTPUT_DIR = REPO_ROOT / "outputs"
RESULTS_CSV = OUTPUT_DIR / "experiment_results.csv"
PROTECTION_CSV = OUTPUT_DIR / "protection_analysis.csv"

# Global lock to prevent concurrent Qiskit simulations from colliding
_EXPERIMENT_LOCK = asyncio.Lock()


class ExperimentService:
    @staticmethod
    def get_processors() -> List[Dict[str, Any]]:
        """Retrieve all configured processor topologies and physical specs."""
        config = load_config(str(CONFIG_PATH))
        processors_data = []

        for proc in config.get("processors", []):
            qubits = int(proc["qubits"])
            edges = proc.get("edges", [])
            topo = validate_topology(qubits, edges)

            processors_data.append({
                "id": proc.get("id", proc["name"].lower().replace(" ", "_")),
                "name": proc["name"],
                "qubits": qubits,
                "port_qubits": proc.get("port_qubits", [0, 1]),
                "ancilla_qubit": proc.get("ancilla_qubit", 2),
                "single_qubit_depolarizing": float(proc.get("single_qubit_depolarizing", 0.0)),
                "two_qubit_depolarizing": float(proc.get("two_qubit_depolarizing", 0.0)),
                "readout_error": float(proc.get("readout_error", 0.0)),
                "is_connected": topo["is_connected"],
                "edges_count": topo["edges_count"],
                "edges": edges,
                "note": proc.get("note", config.get("note", "Illustrative placeholder")),
            })
        return processors_data

    @staticmethod
    def get_processor_by_id(processor_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific processor configuration by ID."""
        processors = ExperimentService.get_processors()
        for p in processors:
            if p["id"].lower() == processor_id.lower():
                return p
        return None

    @staticmethod
    def get_results_history() -> List[Dict[str, Any]]:
        """Load experiment history from outputs/experiment_results.csv or results.csv."""
        target_csv = RESULTS_CSV if RESULTS_CSV.exists() else (OUTPUT_DIR / "results.csv")
        if not target_csv.exists():
            return []

        try:
            df = pd.read_csv(target_csv)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Ensure id column exists and has no NaN
            if "id" not in df.columns:
                df["id"] = [f"exp-{i+1:03d}" for i in range(len(df))]
            else:
                df["id"] = df["id"].apply(
                    lambda v: f"exp-{uuid.uuid4().hex[:6]}"
                    if (pd.isna(v) or str(v).lower() == "nan" or not str(v).strip())
                    else str(v)
                )

            # Ensure timestamp column exists and has no NaN
            if "timestamp" not in df.columns:
                df["timestamp"] = now_str
            else:
                df["timestamp"] = df["timestamp"].apply(
                    lambda v: now_str
                    if (pd.isna(v) or str(v).lower() == "nan" or not str(v).strip())
                    else str(v)
                )

            # Fill remaining NaNs for safety
            df["note"] = df["note"].fillna("").astype(str) if "note" in df.columns else ""
            df = df.fillna(0.0)

            records = df.to_dict(orient="records")
            for idx, r in enumerate(records):
                if not isinstance(r.get("id"), str) or str(r.get("id")).lower() == "nan":
                    r["id"] = f"exp-{idx+1:03d}"
                if not isinstance(r.get("timestamp"), str) or str(r.get("timestamp")).lower() == "nan":
                    r["timestamp"] = now_str

            return records
        except Exception:
            return []

    @staticmethod
    async def run_single(
        processor_id: str,
        experiment_type: str,
        shots: int,
        seed: int,
        observable: str = "ALL",
    ) -> Dict[str, Any]:
        """Run a single experiment through Q-Guard Qiskit engine with concurrency lock."""
        proc = ExperimentService.get_processor_by_id(processor_id)
        if not proc:
            raise ValueError(f"Unknown processor ID '{processor_id}'. Available: {[p['id'] for p in ExperimentService.get_processors()]}")

        # Map experiment type to boolean flags
        exp_type_clean = experiment_type.strip()
        if exp_type_clean == "Ideal":
            noisy = False
            protected = False
        elif exp_type_clean == "Noisy":
            noisy = True
            protected = False
        elif exp_type_clean in {"Noisy + Protection", "Protected"}:
            noisy = True
            protected = True
            exp_type_clean = "Noisy + Protection"
        else:
            raise ValueError(f"Invalid experiment_type '{experiment_type}'. Must be 'Ideal', 'Noisy', or 'Noisy + Protection'")

        async with _EXPERIMENT_LOCK:
            # Run in thread pool to avoid blocking asyncio event loop
            record = await asyncio.to_thread(
                run_single_experiment,
                processor=proc,
                experiment_name=exp_type_clean,
                noisy=noisy,
                protected=protected,
                shots=shots,
                seed=seed,
            )

            record["id"] = f"run-{uuid.uuid4().hex[:8]}"
            record["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Persist to experiment_results.csv
            ExperimentService._append_result(record)
            return record

    @staticmethod
    async def run_all() -> List[Dict[str, Any]]:
        """Run the full 3x3 matrix across all processors and cases."""
        async with _EXPERIMENT_LOCK:
            df = await asyncio.to_thread(
                run_experiments,
                config_path=str(CONFIG_PATH),
                output_dir=str(OUTPUT_DIR),
            )
            records = df.to_dict(orient="records")
            for idx, r in enumerate(records):
                r["id"] = f"batch-{idx+1:03d}"
                r["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return records

    @staticmethod
    def get_summary() -> Dict[str, Any]:
        """Retrieve executive summary including protection trade-offs."""
        history = ExperimentService.get_results_history()
        processors = [p["name"] for p in ExperimentService.get_processors()]

        protection_analysis = []
        if PROTECTION_CSV.exists():
            try:
                p_df = pd.read_csv(PROTECTION_CSV)
                protection_analysis = p_df.to_dict(orient="records")
            except Exception:
                protection_analysis = []

        return {
            "total_experiments": len(history),
            "processors_count": len(processors),
            "processors": processors,
            "experiments": history,
            "protection_analysis": protection_analysis,
        }

    @staticmethod
    def get_csv_export_path() -> Optional[Path]:
        """Get path to the latest results CSV."""
        if RESULTS_CSV.exists():
            return RESULTS_CSV
        alt = OUTPUT_DIR / "results.csv"
        if alt.exists():
            return alt
        return None

    @staticmethod
    def _append_result(record: Dict[str, Any]):
        """Append a newly executed experiment record to results CSV."""
        target_csv = RESULTS_CSV
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        new_row = pd.DataFrame([record])
        if target_csv.exists():
            try:
                existing_df = pd.read_csv(target_csv)
                updated_df = pd.concat([existing_df, new_row], ignore_index=True)
                updated_df.to_csv(target_csv, index=False)
                # Also keep results.csv in sync
                updated_df.to_csv(OUTPUT_DIR / "results.csv", index=False)
            except Exception:
                new_row.to_csv(target_csv, index=False)
        else:
            new_row.to_csv(target_csv, index=False)
            new_row.to_csv(OUTPUT_DIR / "results.csv", index=False)
