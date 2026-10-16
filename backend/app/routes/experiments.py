"""Experiment and Result API routes."""

from pathlib import Path
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import FileResponse

from ..schemas import (
    ExperimentResultResponse,
    ExperimentRunRequest,
    ProcessorSummary,
    SummaryResponse,
)
from ..services.experiment_service import ExperimentService

router = APIRouter(tags=["Experiments & Results"])


@router.get("/api/processors", response_model=List[ProcessorSummary])
def get_processors() -> List[ProcessorSummary]:
    """Retrieve all available processor configurations."""
    try:
        processors = ExperimentService.get_processors()
        return [ProcessorSummary(**p) for p in processors]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load processor configurations: {str(e)}",
        )


@router.get("/api/processors/{processor_id}", response_model=ProcessorSummary)
def get_processor(processor_id: str) -> ProcessorSummary:
    """Retrieve details for a specific processor by ID."""
    proc = ExperimentService.get_processor_by_id(processor_id)
    if not proc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Processor '{processor_id}' not found.",
        )
    return ProcessorSummary(**proc)


@router.get("/api/experiments", response_model=List[ExperimentResultResponse])
def get_experiments(limit: int = Query(50, ge=1, le=500)) -> List[ExperimentResultResponse]:
    """Retrieve history of executed experiments."""
    history = ExperimentService.get_results_history()
    # Return latest first
    reversed_history = list(reversed(history))[:limit]
    results = []
    for r in reversed_history:
        try:
            results.append(ExperimentResultResponse(**r))
        except Exception:
            # Fallback if any field needs default
            continue
    return results


@router.get("/api/experiments/{experiment_id}", response_model=ExperimentResultResponse)
def get_experiment_by_id(experiment_id: str) -> ExperimentResultResponse:
    """Retrieve a single experiment result by ID."""
    history = ExperimentService.get_results_history()
    for r in history:
        if str(r.get("id")) == experiment_id:
            return ExperimentResultResponse(**r)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Experiment '{experiment_id}' not found.",
    )


@router.post("/api/experiments", response_model=ExperimentResultResponse)
async def run_experiment(request: ExperimentRunRequest) -> ExperimentResultResponse:
    """
    Execute a real quantum experiment via Qiskit Aer simulation engine.
    """
    try:
        record = await ExperimentService.run_single(
            processor_id=request.processor_id,
            experiment_type=request.experiment_type,
            shots=request.shots,
            seed=request.seed,
            observable=request.observable or "ALL",
        )
        return ExperimentResultResponse(**record)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Experiment execution failed: {str(e)}",
        )


@router.post("/api/experiments/run-all", response_model=List[ExperimentResultResponse])
async def run_all_experiments() -> List[ExperimentResultResponse]:
    """
    Execute the full 3x3 matrix across all processors and noise conditions.
    """
    try:
        records = await ExperimentService.run_all()
        return [ExperimentResultResponse(**r) for r in records]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch execution failed: {str(e)}",
        )


@router.get("/api/results/summary", response_model=SummaryResponse)
def get_summary() -> SummaryResponse:
    """Retrieve statistical summary and protection comparisons."""
    try:
        summary_data = ExperimentService.get_summary()
        return SummaryResponse(**summary_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {str(e)}",
        )


@router.get("/api/results/export")
def export_results_csv():
    """Download the actual current experiment results as a CSV file."""
    path = ExperimentService.get_csv_export_path()
    if not path or not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No experiment results CSV found. Run an experiment first.",
        )
    return FileResponse(
        path=str(path),
        media_type="text/csv",
        filename="qguard_experiment_results.csv",
    )


@router.get("/api/results/plots/{plot_name}")
def get_plot_image(plot_name: str):
    """Serve a generated PNG chart from the outputs directory."""
    allowed_plots = {
        "fidelity_comparison.png",
        "acceptance_rate.png",
        "circuit_overhead.png",
        "processor_comparison.png",
        "final_fidelity_comparison.png",
        "final_acceptance_comparison.png",
    }
    if plot_name not in allowed_plots:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid plot name. Allowed: {sorted(allowed_plots)}",
        )

    # Use project root outputs
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    plot_path = repo_root / "outputs" / plot_name

    if not plot_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plot '{plot_name}' not generated yet. Run experiments first.",
        )
    return FileResponse(path=str(plot_path), media_type="image/png")
