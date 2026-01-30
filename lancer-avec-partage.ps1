# Script pour lancer SalesCoach et le rendre accessible via Cloudflare Tunnel

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "`n=== SalesCoach - Lancement avec partage public (Cloudflare) ===" -ForegroundColor Cyan
Write-Host ""

# Vérifier que cloudflared est installé
$cloudflaredPath = Join-Path $root "cloudflared.exe"
if (-not (Test-Path $cloudflaredPath)) {
    Write-Host "✗ cloudflared.exe non trouvé !" -ForegroundColor Red
    Write-Host ""
    Write-Host "INSTALLATION REQUISE:" -ForegroundColor Yellow
    Write-Host "Exécutez d'abord : .\installer-cloudflare.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Ou téléchargez manuellement :" -ForegroundColor Yellow
    Write-Host "1. Allez sur https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/" -ForegroundColor White
    Write-Host "2. Téléchargez la version Windows" -ForegroundColor White
    Write-Host "3. Renommez en 'cloudflared.exe' et placez dans : $root" -ForegroundColor White
    Write-Host ""
    Write-Host "Appuyez sur une touche pour lancer l'installation automatique..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    & "$root\installer-cloudflare.ps1"
    exit 0
}

Write-Host "✓ Cloudflare Tunnel trouvé" -ForegroundColor Green
Write-Host ""

# Lancer l'application normale (backend + frontend)
Write-Host "Lancement de l'application..." -ForegroundColor Yellow
$scriptPath = Join-Path $root "scripts\start-all.ps1"

# Lancer le script start-all.ps1 dans une nouvelle fenêtre
Start-Process powershell -ArgumentList "-NoExit", "-File", "`"$scriptPath`"" -WindowStyle Normal

Write-Host "✓ Application démarrée" -ForegroundColor Green
Write-Host ""
Write-Host "Attente du démarrage complet (15 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Lancer cloudflared pour le frontend (port 5173)
Write-Host ""
Write-Host "Création du tunnel public avec Cloudflare..." -ForegroundColor Yellow
Write-Host ""

# Lancer cloudflared dans une nouvelle fenêtre PowerShell avec couleurs
$cloudflaredCommand = @"
& '$cloudflaredPath' tunnel --url http://localhost:5173
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $cloudflaredCommand -WindowStyle Normal

Write-Host "✓ Tunnel Cloudflare lancé !" -ForegroundColor Green
Write-Host ""
Write-Host "=== INSTRUCTIONS ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Une fenêtre Cloudflare Tunnel s'est ouverte" -ForegroundColor White
Write-Host "2. Cherchez les lignes avec 'Your quick Tunnel has been created!' et une URL" -ForegroundColor White
Write-Host "3. L'URL ressemble à : https://xxxxx.trycloudflare.com" -ForegroundColor Green
Write-Host "4. Copiez cette URL et envoyez-la à vos collègues" -ForegroundColor White
Write-Host ""
Write-Host "✅ AVANTAGES Cloudflare :" -ForegroundColor Green
Write-Host "   - 100% gratuit, pas de limite" -ForegroundColor White
Write-Host "   - Serveurs européens (RGPD compliant)" -ForegroundColor White
Write-Host "   - Plus rapide et sécurisé" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANT :" -ForegroundColor Red
Write-Host "   - Cette URL est temporaire (expire à la fermeture)" -ForegroundColor Yellow
Write-Host "   - Ne fermez aucune des fenêtres ouvertes" -ForegroundColor Yellow
Write-Host "   - Vos collègues peuvent accéder depuis n'importe où" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer (mais laissez les autres fenêtres ouvertes)..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
