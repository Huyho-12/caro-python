# Helper script to run the interactive GUI test locally (Windows PowerShell)
# Usage:
# 1) Open PowerShell in the project root (D:\caro-python-main)
# 2) Run: .\run_gui_local.ps1
# If your PowerShell execution policy prevents running scripts, run:
#    powershell -ExecutionPolicy Bypass -File .\run_gui_local.ps1

Push-Location $PSScriptRoot
try {
    Write-Host "Running GUI smoke test: run_ai_smoketest.py" -ForegroundColor Green
    python .\run_ai_smoketest.py
} finally {
    Pop-Location
}
