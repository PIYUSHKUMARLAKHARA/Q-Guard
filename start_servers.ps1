<#
.SYNOPSIS
    Q-Guard Full-Stack Quantum Dashboard Launcher
.DESCRIPTION
    Starts the FastAPI backend and Vite React frontend in separate PowerShell processes.
    Resolves all paths relative to the script location.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Q-Guard: Starting Full-Stack Quantum Dashboard" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Project Root: $ScriptDir" -ForegroundColor Gray
Write-Host ""

# 1. Check Python Virtual Environment
$PythonExe = $null
if (Test-Path "$ScriptDir\.venv\Scripts\python.exe") {
    $PythonExe = "$ScriptDir\.venv\Scripts\python.exe"
    Write-Host "[OK] Located virtual environment at .venv" -ForegroundColor Green
} elseif (Test-Path "$ScriptDir\.venv-1\Scripts\python.exe") {
    $PythonExe = "$ScriptDir\.venv-1\Scripts\python.exe"
    Write-Host "[OK] Located virtual environment at .venv-1" -ForegroundColor Green
} else {
    $SysPython = Get-Command python -ErrorAction SilentlyContinue
    if ($SysPython) {
        $PythonExe = "python"
        Write-Host "[WARN] Virtual environment (.venv) not found. Using system Python." -ForegroundColor Yellow
    } else {
        Write-Host "[ERROR] Python executable not found!" -ForegroundColor Red
        Write-Host "Please create a virtual environment:" -ForegroundColor Yellow
        Write-Host "  python -m venv .venv"
        Write-Host "  .\.venv\Scripts\pip install -r requirements.txt"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# 2. Check Backend Files
$BackendMain = "$ScriptDir\backend\app\main.py"
if (-not (Test-Path $BackendMain)) {
    Write-Host "[ERROR] Backend entrypoint not found at: $BackendMain" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# 3. Check Frontend Directory & package.json
$FrontendDir = "$ScriptDir\frontend"
$FrontendPkg = "$FrontendDir\package.json"
if (-not (Test-Path $FrontendPkg)) {
    Write-Host "[ERROR] Frontend package.json not found at: $FrontendPkg" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# 4. Check Frontend node_modules
if (-not (Test-Path "$FrontendDir\node_modules")) {
    Write-Host "[WARN] node_modules not found in $FrontendDir!" -ForegroundColor Yellow
    Write-Host "Please run 'npm install' inside $FrontendDir before starting the frontend." -ForegroundColor Yellow
    Write-Host ""
}

# 5. Check Ports
$port8000Used = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000Used) {
    Write-Host "[WARN] Port 8000 appears to be currently in use. FastAPI may conflict." -ForegroundColor Yellow
}
$port5173Used = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($port5173Used) {
    Write-Host "[WARN] Port 5173 appears to be in use. Vite may switch to port 5174." -ForegroundColor Yellow
}

# 6. Start Backend in separate window
Write-Host "Starting FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Green
$BackendCmd = "Set-Location '$ScriptDir'; & '$PythonExe' -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $BackendCmd

Start-Sleep -Seconds 3

# 7. Start Frontend in separate window
Write-Host "Starting React Frontend on http://localhost:5173 ..." -ForegroundColor Green
$FrontendCmd = "Set-Location '$FrontendDir'; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $FrontendCmd

Start-Sleep -Seconds 3

# 8. Open Browser
Write-Host "Opening browser..." -ForegroundColor Cyan
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Both servers launched." -ForegroundColor Green
Write-Host "  - Backend API: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  - API Docs:    http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "  - Frontend:    http://localhost:5173" -ForegroundColor White
Write-Host "Close the spawned terminal windows to stop the servers." -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
