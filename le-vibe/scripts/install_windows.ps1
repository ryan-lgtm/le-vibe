#Requires -Version 5.0
$ErrorActionPreference = "Stop"
if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install -e --id Ollama.Ollama --accept-package-agreements --accept-source-agreements
} else {
    Write-Error "winget not found. Install Ollama from https://ollama.com/download/windows"
    exit 1
}
