@echo off
title AI Tutor System Launcher
echo ==========================================
echo   Starting Generative AI Tutor System...
echo ==========================================

:: Stop any existing backend on port 8000
echo Cleaning up any stale backend servers running on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)

:: Stop any existing frontend on port 8501
echo Cleaning up any stale frontend servers running on port 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo Starting fresh servers...

:: Start the FastAPI backend server in a separate cmd window
start "AI Tutor Backend" cmd /k ".venv\Scripts\activate.bat && .venv\Scripts\python.exe -m uvicorn Week_2.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir Week_2 --reload-dir Week_3"

echo [Backend] Starting on http://localhost:8000...
echo [Frontend] Starting Streamlit UI...

:: Start the Streamlit frontend in the current cmd window using the virtual environment's executable
call .venv\Scripts\activate.bat
streamlit run Week_4\frontend\app.py

pause

