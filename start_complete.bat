@echo off
echo ==========================================
echo 🏦 Loan Approval Risk Analysis System
echo ==========================================
echo.
echo Starting Backend and Frontend...
echo.

REM Start backend in a new window
echo [1/3] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && ..\venv\Scripts\activate && python app.py"

REM Wait for backend to start
echo [2/3] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend HTTP server in a new window
echo [3/3] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"

REM Wait a moment for frontend server to start
timeout /t 2 /nobreak >nul

REM Open browser
echo.
echo ✅ Opening browser...
start http://localhost:8000

echo.
echo ==========================================
echo ✅ System Started Successfully!
echo ==========================================
echo.
echo 🌐 Frontend: http://localhost:8000
echo 🔧 Backend:  http://localhost:5000
echo.
echo 📊 Two windows opened:
echo    1. Backend Server (Flask API)
echo    2. Frontend Server (HTTP Server)
echo.
echo 🛑 To stop: Close both terminal windows
echo    or press Ctrl+C in each window
echo.
echo ==========================================
echo.
pause
