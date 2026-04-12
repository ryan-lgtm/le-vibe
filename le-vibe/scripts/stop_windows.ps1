$ErrorActionPreference = "SilentlyContinue"
Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Stopped ollama processes (if any)."
