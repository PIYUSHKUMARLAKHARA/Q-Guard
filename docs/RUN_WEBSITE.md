# Q-Guard: Full-Stack Website Running Guide

This guide provides step-by-step instructions to run the **Q-Guard** full-stack quantum dashboard locally on Windows (PowerShell or Git Bash) or Linux/macOS.

---

## 1. Prerequisites
- **Python:** 3.12 (or 3.11+)
- **Node.js:** v18+ (tested with v24.19.0)
- **npm:** v9+ (tested with 11.17.0)

---

## 2. Fast Launch (Development Mode)

Open **two terminal windows**:

### Terminal 1: Backend API (FastAPI)
```powershell
# Navigate to project root
cd C:\Users\dlakh\Downloads\Q-Guard\Q-Guard

# Activate Python virtual environment
.\.venv\Scripts\activate
# (On Git Bash: source .venv/Scripts/activate)

# Start FastAPI server on port 8000
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Backend will be live at:
- **API Base:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`
- **Health Check:** `http://127.0.0.1:8000/api/health`

---

### Terminal 2: Frontend Dashboard (React + Vite)
```powershell
# Navigate to frontend folder
cd C:\Users\dlakh\Downloads\Q-Guard\Q-Guard\frontend

# Install dependencies (if not already installed)
npm install

# Start Vite development server
npm run dev
```
Frontend will be live at:
- **Dashboard URL:** `http://localhost:5173`

The Vite dev server automatically proxies all `/api` requests to `http://127.0.0.1:8000`.

---

## 3. Alternative: Single-Server Production Mode

FastAPI is pre-configured to serve the compiled frontend production build directly from `/ui`:

1. Build the frontend (one time):
   ```powershell
   cd frontend
   npm run build
   cd ..
   ```
2. Start the backend:
   ```powershell
   python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
   ```
3. Open in browser:
   - **Compiled UI:** `http://127.0.0.1:8000/ui/`
   - **API Docs:** `http://127.0.0.1:8000/docs`

---

## 4. One-Click Windows Launch Script
You can also run the provided launcher script:
```powershell
.\start_servers.bat
```
This opens the backend and frontend concurrently in two separate terminal windows.

---

## 5. How to Run Experiments from the Website
1. Open `http://localhost:5173` in your browser.
2. Navigate to **Run Experiment** in the sidebar.
3. Choose your target **Processor Topology** (`2016-Inspired`, `Contemporary`, or `Hyperbolic-Inspired`).
4. Select the **Simulation Condition** (`Ideal`, `Noisy Baseline`, or `Noisy + Protection`).
5. Set your desired **Shot Count** (e.g., 4096) and deterministic **Seed** (e.g., 42).
6. Click **Run Experiment**. The real Qiskit simulation will run in the background.
7. Inspect the estimated Fidelity, 95% Confidence Interval, Entanglement Threshold decision ($F - 2\sigma_F > 0.5$), and Pauli correlation chart.
8. Click **Download CSV** from the navbar to export your raw results.

---

## 6. Running Automated Tests
```powershell
# Run all 66 unit and API tests
python -m unittest discover -v
```

---

## 7. Stopping the Servers
- Press `Ctrl + C` in both terminal windows to gracefully terminate FastAPI and the Vite dev server.
