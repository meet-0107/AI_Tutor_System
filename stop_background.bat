@echo off
title AI Tutor System - Stop Background Servers
echo ==================================================
echo   Stopping Generative AI Tutor Background Servers...
echo ==================================================

:: Stop the FastAPI backend listening on port 8000
echo Stopping Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a
)

:: Stop the Streamlit frontend listening on port 8501
echo Stopping Frontend (Port 8501)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a
)

echo ==================================================
echo   Background servers stopped successfully!
echo ==================================================
pause
