@echo off
echo ==========================================
echo Starting FinCrime Loan Risk System
echo ==========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting backend server...
cd backend
python app.py
