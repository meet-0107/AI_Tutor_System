@echo off
title AI Tutor System Launcher
echo ==========================================
echo   Starting Generative AI Tutor System...
echo ==========================================

:: Start the FastAPI backend server in a separate cmd window
start "AI Tutor Backend" cmd /k ".venv\Scripts\activate.bat && .venv\Scripts\python.exe -m uvicorn Week_2.main:app --host 127.0.0.1 --port 8000 --reload"

echo [Backend] Starting on http://localhost:8000...
echo [Frontend] Starting Streamlit UI...

:: Start the Streamlit frontend in the current cmd window using the virtual environment's executable
.venv\Scripts\streamlit.exe run Week_4\frontend\app.py

pause
