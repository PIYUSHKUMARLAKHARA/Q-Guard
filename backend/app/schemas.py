"""Pydantic request and response schemas for Q-Guard API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProcessorSummary(BaseModel):
    id: str
    name: str
    qubits: int
    port_qubits: List[int]
    ancilla_qubit: int
    single_qubit_depolarizing: float
    two_qubit_depolarizing: float
    readout_error: float
    is_connected: bool
    edges_count: int
    edges: List[List[int]]
    note: str


class ExperimentRunRequest(BaseModel):
    processor_id: str = Field(..., description="Target processor ID (e.g., 'contemporary')")
    experiment_type: str = Field(
        "Noisy + Protection",
        description="Experiment case: 'Ideal', 'Noisy', or 'Noisy + Protection'",
    )
    shots: int = Field(4096, ge=100, le=20000, description="Shot count per observable")
    seed: int = Field(42, ge=0, description="Deterministic pseudo-random seed")
    observable: Optional[str] = Field(
        "ALL",
        description="'ALL' for complete Bell fidelity (XX, YY, ZZ) or specific observable",
    )


class ExperimentResultResponse(BaseModel):
    id: str = "exp-001"
    processor: str
    processor_id: str
    experiment: str
    fidelity_estimate: float
    fidelity_uncertainty: float
    f_minus_2sigma: float
    threshold_passed: bool
    threshold_margin: float
    XX: float
    YY: float
    ZZ: float
    sigma_XX: float
    sigma_YY: float
    sigma_ZZ: float
    accepted_shots_avg: int
    total_shots_avg: int
    discarded_shots_avg: int
    acceptance_rate: float
    shots_per_observable: int
    average_circuit_depth: float
    average_one_qubit_gates: float
    average_two_qubit_gates: float
    average_swap_count: float
    physical_qubits: int
    noisy: bool
    protected: bool
    timestamp: str = "2026-10-15 00:00:00"
    note: str = ""


class ProtectionComparisonItem(BaseModel):
    processor: str
    noisy_fidelity: float
    protected_fidelity: float
    fidelity_change: float
    acceptance_rate: float
    discarded_shots_avg: int
    extra_two_qubit_gates: float
    extra_circuit_depth: float
    threshold_passed: bool
    fidelity_improved: bool


class SummaryResponse(BaseModel):
    total_experiments: int
    processors_count: int
    processors: List[str]
    experiments: List[ExperimentResultResponse]
    protection_analysis: List[ProtectionComparisonItem]


class HealthResponse(BaseModel):
    status: str
    version: str
    qiskit_version: str
    aer_version: str
    environment: str
