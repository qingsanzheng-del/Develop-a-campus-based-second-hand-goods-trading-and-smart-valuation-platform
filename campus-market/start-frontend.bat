@echo off
chcp 65001 >nul
cd /d "%~dp0frontend"
echo ============================================
echo  Starting Frontend (Vite + Vue)...
echo  Keep this window open while using the app.
echo  When ready, open: http://localhost:5173
echo ============================================
call npm run dev
pause
