@echo off
REM FinCrime Loan Risk Assessment System - One-Click Startup
REM This launches both backend and frontend automatically

echo.
echo ==========================================
echo 🏦 Starting FinCrime Loan Risk System
echo ==========================================
echo.

REM Run PowerShell script
powershell -ExecutionPolicy Bypass -File start_system.ps1

REM If PowerShell fails, use fallback batch script
if errorlevel 1 (
    echo.
    echo PowerShell script failed, using fallback method...
    echo.
    call start_complete.bat
)
