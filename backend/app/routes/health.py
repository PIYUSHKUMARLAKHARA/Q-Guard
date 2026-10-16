"""Health check API route."""

from fastapi import APIRouter
import qiskit
import qiskit_aer
from ..schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/api/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """Return API health status and quantum runtime versions."""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        qiskit_version=qiskit.__version__,
        aer_version=qiskit_aer.__version__,
        environment="simulation-nisq",
    )
