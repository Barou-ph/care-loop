$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    $Python = $VenvPython
} else {
    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonCommand) {
        throw "Python was not found. Install Python or create .venv first."
    }
    $Python = $PythonCommand.Source
}

# Local MVP defaults: API and desktop detector communicate over loopback.
$env:CARE_LOOP_API_URL = "http://127.0.0.1:8000"

$ApiReady = $false
try {
    $Health = Invoke-RestMethod -Uri "$($env:CARE_LOOP_API_URL)/health" -TimeoutSec 2
    $ApiReady = ($Health.status -eq "ok")
} catch {
    $ApiReady = $false
}

if (-not $ApiReady) {
    Write-Host "Starting CARE LOOP API..." -ForegroundColor Cyan
    Start-Process -FilePath $Python `
        -ArgumentList @("-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000") `
        -WorkingDirectory $ProjectRoot

    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 1
        try {
            $Health = Invoke-RestMethod -Uri "$($env:CARE_LOOP_API_URL)/health" -TimeoutSec 2
            if ($Health.status -eq "ok") {
                $ApiReady = $true
                break
            }
        } catch { }
    }
}

if (-not $ApiReady) {
    throw "CARE LOOP API did not start. Check whether port 8000 is already in use."
}

Write-Host "CARE LOOP API is ready at $($env:CARE_LOOP_API_URL)" -ForegroundColor Green
Start-Process "$($env:CARE_LOOP_API_URL)/"
Write-Host "Launching YOLO fall-detection desktop app..." -ForegroundColor Cyan
Write-Host "Close the desktop app normally when you finish testing." -ForegroundColor Yellow
& $Python "run.py"
