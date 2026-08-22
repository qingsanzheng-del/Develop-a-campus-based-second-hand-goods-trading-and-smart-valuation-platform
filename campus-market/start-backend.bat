@echo off
chcp 65001 >nul
cd /d "%~dp0backend"
echo ============================================
echo  Starting Backend (FastAPI)...
echo  Keep this window open while using the app.
echo  Success = you see "Uvicorn running on ..."
echo ============================================
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
