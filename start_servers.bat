@echo off
setlocal enabledelayedexpansion

:: Resolve root directory relative to this script
cd /d "%~dp0"
set "ROOT_DIR=%cd%"

echo ======================================================================
echo Q-Guard: Quantum Error Detection and Protection Dashboard Launcher
echo ======================================================================
echo Project Root: %ROOT_DIR%
echo.

:: 1. Check Python Virtual Environment
set "PYTHON_EXE="
if exist "%ROOT_DIR%\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%ROOT_DIR%\.venv\Scripts\python.exe"
    echo [OK] Located virtual environment at .venv\
) else if exist "%ROOT_DIR%\.venv-1\Scripts\python.exe" (
    set "PYTHON_EXE=%ROOT_DIR%\.venv-1\Scripts\python.exe"
    echo [OK] Located virtual environment at .venv-1\
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=python"
        echo [WARN] Virtual environment (.venv) not found. Using system Python.
    ) else (
        echo [ERROR] Python not found! Please create a virtual environment (.venv) or install Python.
        echo Run: python -m venv .venv ^&^& .\.venv\Scripts\pip install -r requirements.txt
        pause
        exit /b 1
    )
)

:: 2. Check Backend Main Entrypoint
if not exist "%ROOT_DIR%\backend\app\main.py" (
    echo [ERROR] Backend entrypoint '%ROOT_DIR%\backend\app\main.py' not found!
    pause
    exit /b 1
)

:: 3. Check Frontend Directory and package.json
if not exist "%ROOT_DIR%\frontend\package.json" (
    echo [ERROR] Frontend package.json not found in '%ROOT_DIR%\frontend'!
    pause
    exit /b 1
)

:: 4. Check Frontend node_modules
if not exist "%ROOT_DIR%\frontend\node_modules" (
    echo [WARN] Frontend node_modules not detected!
    echo Please run 'npm install' inside the frontend directory before running the dashboard.
    echo Command: cd "%ROOT_DIR%\frontend" ^&^& npm install
    echo.
)

:: 5. Start Backend in separate window
echo Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Q-Guard Backend (FastAPI)" cmd /k "cd /d "%ROOT_DIR%" && "%PYTHON_EXE%" -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

:: 6. Start Frontend in separate window
echo Starting React/Vite Frontend on http://localhost:5173 ...
start "Q-Guard Frontend (Vite)" cmd /k "cd /d "%ROOT_DIR%\frontend" && npm run dev"

timeout /t 3 /nobreak >nul

:: 7. Open Browser
echo Opening browser at http://localhost:5173 ...
start http://localhost:5173

echo.
echo ======================================================================
echo Both servers are running.
echo   - Backend API: http://127.0.0.1:8000
echo   - API Docs:    http://127.0.0.1:8000/docs
echo   - Frontend:    http://localhost:5173
echo Close the opened terminal windows to stop the servers.
echo ======================================================================
