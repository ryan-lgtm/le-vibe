$ErrorActionPreference = "Continue"
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama) { exit 1 }
try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -UseBasicParsing -TimeoutSec 2
    if ($r.StatusCode -eq 200) { exit 0 }
} catch {}
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
