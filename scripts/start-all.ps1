# SalesCoach - Lance backend + frontend
# Execute dans PowerShell : .\scripts\start-all.ps1
# Au premier run : installe les deps (pip + npm). Necessite Internet.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"

Write-Host "=== SalesCoach - Install et lancement ===" -ForegroundColor Cyan

# 1. Backend
$venv = Join-Path $backend ".venv"
$pythonExe = Join-Path $venv "Scripts\python.exe"
$pip = Join-Path $venv "Scripts\pip.exe"
$useVenv = $false

if ((Test-Path $venv) -and (Test-Path $pip)) {
    $useVenv = $true
} elseif (Test-Path $venv) {
    Write-Host "Venv sans pip. Suppression et utilisation du Python systeme." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venv -ErrorAction SilentlyContinue
}

if (-not $useVenv) {
    $pythonExe = "python"
    $pip = "python -m pip"
}

$hasDeps = $false
if ($useVenv) {
    $fastapiMarker = Join-Path $venv "Lib\site-packages\fastapi"
    if (Test-Path $fastapiMarker) { $hasDeps = $true }
} else {
    $hasDeps = $false
}
if (-not $hasDeps) {
    Write-Host "Install des deps Python..." -ForegroundColor Yellow
    Push-Location $backend
    if ($useVenv) { & $pip install -r requirements.txt -q } else { python -m pip install -r requirements.txt -q }
    if ($LASTEXITCODE -ne 0) { Pop-Location; Write-Host "Erreur pip. Verifie ton acces Internet." -ForegroundColor Red; exit 1 }
    Pop-Location
}

if (-not (Test-Path (Join-Path $backend ".env"))) {
    Copy-Item (Join-Path $backend ".env.example") (Join-Path $backend ".env")
    Write-Host "Fichier .env cree. Edite backend\.env et ajoute OPENAI_API_KEY (ou ANTHROPIC_API_KEY)." -ForegroundColor Yellow
}

# 2. Frontend
if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    Write-Host "Install des deps npm..." -ForegroundColor Yellow
    Push-Location $frontend
    npm install
    if ($LASTEXITCODE -ne 0) { Pop-Location; Write-Host "Erreur npm. Verifie ton acces Internet." -ForegroundColor Red; exit 1 }
    Pop-Location
}

# 3. Lancer backend avec --reload pour auto-recharge
Write-Host "Lancement du backend (port 8000) avec auto-reload..." -ForegroundColor Green
$uvicornArgs = @("-m", "uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000")
if ($useVenv) {
    Start-Process -FilePath $pythonExe -ArgumentList $uvicornArgs -WorkingDirectory $backend -WindowStyle Normal
} else {
    Start-Process -FilePath "python" -ArgumentList $uvicornArgs -WorkingDirectory $backend -WindowStyle Normal
}
Start-Sleep -Seconds 2

# 4. Lancer frontend
Write-Host "Lancement du frontend (port 5173)..." -ForegroundColor Green
Write-Host "Ouvre http://localhost:5173 dans ton navigateur. Ctrl+C pour arreter le frontend." -ForegroundColor Cyan
Push-Location $frontend
npm run dev
Pop-Location
