@echo off
echo =====================================================
echo  VIBE SPACIEE - Starting Backend Server
echo =====================================================
cd /d "%~dp0backend"

if not exist ".venv\Scripts\uvicorn.exe" (
    echo ERROR: Virtual environment not found.
    echo Please run: python -m venv .venv  then  pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo  Server starting at: http://127.0.0.1:8001
echo  Open your browser to: http://127.0.0.1:8001
echo  Press CTRL+C to stop.
echo.
.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8001 --reload
pause
