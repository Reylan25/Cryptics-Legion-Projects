# Smart Expense Tracker - Auto Port Management Script
# This script finds and kills any process using port 8551, then runs the app

param(
    [string]$Mode = "desktop",  # "desktop" or "android"
    [int]$Port = 8551
)

Write-Host "🚀 Smart Expense Tracker Launcher" -ForegroundColor Cyan
Write-Host "=================================`n" -ForegroundColor Cyan

# Function to kill port
function Kill-Port {
    param([int]$PortNum)
    
    $process = netstat -ano | Select-String ":$PortNum" | Select-Object -First 1
    
    if ($process) {
        $pid = ($process -split '\s+')[-1]
        Write-Host "⚠️  Port $PortNum is in use (PID: $pid)" -ForegroundColor Yellow
        Write-Host "🔨 Killing process..." -ForegroundColor Yellow
        taskkill /PID $pid /F | Out-Null
        Start-Sleep -Seconds 1
        Write-Host "✓ Port freed" -ForegroundColor Green
    } else {
        Write-Host "✓ Port $PortNum is available" -ForegroundColor Green
    }
}

# Kill the port
Kill-Port -PortNum $Port

Write-Host "`n"

# Run based on mode
if ($Mode -eq "android") {
    Write-Host "📱 Launching for Android..." -ForegroundColor Cyan
    python src/main.py --target android
} else {
    Write-Host "🖥️  Launching for Desktop..." -ForegroundColor Cyan
    python src/main.py
}
