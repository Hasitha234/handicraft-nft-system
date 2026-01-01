# PowerShell script to start backend server
# Kills any existing process on port 8000 first

Write-Host "Checking for processes on port 8000..." -ForegroundColor Yellow

$port = 8000
$processes = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique

if ($processes) {
    Write-Host "Found processes using port $port: $processes" -ForegroundColor Yellow
    foreach ($pid in $processes) {
        Write-Host "Killing process $pid..." -ForegroundColor Yellow
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
    Write-Host "Port $port cleared!" -ForegroundColor Green
} else {
    Write-Host "Port $port is free!" -ForegroundColor Green
}

Write-Host "`nStarting backend server..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Gray

# Activate venv and start server
if (Test-Path "venv\Scripts\activate") {
    & "venv\Scripts\python.exe" run.py
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run: python -m venv venv" -ForegroundColor Yellow
}


