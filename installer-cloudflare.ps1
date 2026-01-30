# Script pour télécharger et installer cloudflared

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "`n=== Installation Cloudflare Tunnel ===" -ForegroundColor Cyan
Write-Host ""

# URL de téléchargement de cloudflared pour Windows
$downloadUrl = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
$cloudflaredPath = Join-Path $root "cloudflared.exe"

if (Test-Path $cloudflaredPath) {
    Write-Host "✓ cloudflared déjà installé" -ForegroundColor Green
    Write-Host ""
    & $cloudflaredPath --version
    Write-Host ""
    Write-Host "Pour mettre à jour, supprimez cloudflared.exe et relancez ce script" -ForegroundColor Yellow
} else {
    Write-Host "Téléchargement de cloudflared..." -ForegroundColor Yellow
    Write-Host "Source: $downloadUrl" -ForegroundColor Gray
    Write-Host ""
    
    try {
        # Télécharger cloudflared
        Invoke-WebRequest -Uri $downloadUrl -OutFile $cloudflaredPath -UseBasicParsing
        
        Write-Host "✓ Téléchargement terminé !" -ForegroundColor Green
        Write-Host ""
        Write-Host "✓ cloudflared installé dans : $cloudflaredPath" -ForegroundColor Green
        Write-Host ""
        
        # Vérifier la version
        & $cloudflaredPath --version
        
    } catch {
        Write-Host "✗ Erreur lors du téléchargement" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host ""
        Write-Host "Téléchargement manuel :" -ForegroundColor Yellow
        Write-Host "1. Allez sur https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/" -ForegroundColor White
        Write-Host "2. Téléchargez la version Windows" -ForegroundColor White
        Write-Host "3. Renommez le fichier en 'cloudflared.exe'" -ForegroundColor White
        Write-Host "4. Placez-le dans : $root" -ForegroundColor White
        exit 1
    }
}

Write-Host ""
Write-Host "=== Installation terminée ===" -ForegroundColor Green
Write-Host ""
Write-Host "Pour partager votre application, lancez : .\Lancer-Partage.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
