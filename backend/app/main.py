"""
Q-Guard FastAPI Application Entrypoint.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routes import health, experiments

app = FastAPI(
    title="Q-Guard Quantum API",
    description="Backend API connecting frontend dashboard to Q-Guard Qiskit simulation engine.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

import os

# Configure Cross-Origin Resource Sharing (CORS)
cors_env = os.getenv("CORS_ORIGINS", "")
if cors_env.strip():
    origins = [orig.strip() for orig in cors_env.split(",") if orig.strip()]
else:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(health.router)
app.include_router(experiments.router)


@app.get("/")
def root():
    return {
        "project": "Q-Guard — Quantum Error Detection and Protection Optimizer",
        "status": "online",
        "api_docs": "/docs",
        "endpoints": [
            "/api/health",
            "/api/processors",
            "/api/experiments",
            "/api/results/summary",
            "/api/results/export",
        ],
    }


from pathlib import Path
from fastapi.staticfiles import StaticFiles

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
frontend_dist = REPO_ROOT / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/ui", StaticFiles(directory=str(frontend_dist), html=True), name="ui")

