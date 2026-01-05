# FinCrime Loan Risk Assessment System - Complete Startup Script
# This script starts both backend and frontend, then opens the browser

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🏦 Loan Approval Risk Analysis System" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if port is in use
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue -InformationLevel Quiet
    return $connection
}

# Check if backend is already running
Write-Host "[1/5] Checking if backend is already running..." -ForegroundColor Yellow
if (Test-Port 5000) {
    Write-Host "✅ Backend already running on port 5000" -ForegroundColor Green
} else {
    Write-Host "🚀 Starting Backend Server..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; ..\venv\Scripts\Activate.ps1; python app.py" -WindowStyle Normal
    Write-Host "✅ Backend server starting..." -ForegroundColor Green
}

# Wait for backend to be ready
Write-Host ""
Write-Host "[2/5] Waiting for backend to initialize..." -ForegroundColor Yellow
$maxAttempts = 15
$attempt = 0
$backendReady = $false

while ($attempt -lt $maxAttempts -and -not $backendReady) {
    Start-Sleep -Seconds 1
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Host "✅ Backend is ready!" -ForegroundColor Green
        }
    } catch {
        $attempt++
        Write-Host "." -NoNewline
    }
}

if (-not $backendReady) {
    Write-Host ""
    Write-Host "⚠️  Backend taking longer than expected. Please check the Backend Server window." -ForegroundColor Yellow
}

# Check if frontend is already running
Write-Host ""
Write-Host "[3/5] Checking if frontend is already running..." -ForegroundColor Yellow
if (Test-Port 8000) {
    Write-Host "✅ Frontend already running on port 8000" -ForegroundColor Green
} else {
    Write-Host "🚀 Starting Frontend Server..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; Write-Host '🌐 Frontend Server Running on http://localhost:8000' -ForegroundColor Green; Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow; python -m http.server 8000" -WindowStyle Normal
    Write-Host "✅ Frontend server starting..." -ForegroundColor Green
}

# Wait for frontend to be ready
Write-Host ""
Write-Host "[4/5] Waiting for frontend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Open browser
Write-Host ""
Write-Host "[5/5] Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8000"

# Display summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ System Started Successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Frontend:  http://localhost:8000" -ForegroundColor White
Write-Host "🔧 Backend:   http://localhost:5000" -ForegroundColor White
Write-Host "📊 Health:    http://localhost:5000/health" -ForegroundColor White
Write-Host ""
Write-Host "📂 Two windows opened:" -ForegroundColor Yellow
Write-Host "   1. Backend Server (Flask API)" -ForegroundColor White
Write-Host "   2. Frontend Server (HTTP Server)" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop the system:" -ForegroundColor Yellow
Write-Host "   - Close both PowerShell windows" -ForegroundColor White
Write-Host "   - Or press Ctrl+C in each window" -ForegroundColor White
Write-Host ""
Write-Host "🧪 Ready to test! Fill out the form and click 'Assess Risk'" -ForegroundColor Green
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
