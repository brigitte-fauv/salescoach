@echo off
title Installation Cloudflare Tunnel

echo.
echo ============================================
echo    Etape 1: Installation Cloudflare
echo ============================================
echo.
echo Telechargement de cloudflared.exe...
echo.

cd /d "%~dp0"

if exist cloudflared.exe (
    echo Cloudflared deja installe !
    cloudflared.exe --version
    echo.
    echo Installation OK !
    goto :end
)

echo Telechargement en cours depuis GitHub...
curl -L "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -o cloudflared.exe

if not exist cloudflared.exe (
    echo.
    echo ERREUR: Telechargement echoue
    echo.
    echo Solution manuelle:
    echo 1. Allez sur: https://github.com/cloudflare/cloudflared/releases/latest
    echo 2. Telechargez: cloudflared-windows-amd64.exe
    echo 3. Placez-le dans: %~dp0
    echo 4. Renommez-le en: cloudflared.exe
    echo.
    goto :end
)

echo.
echo ============================================
echo    Installation reussie !
echo ============================================
echo.
cloudflared.exe --version
echo.
echo Maintenant, lancez: 2-Demarrer-Application.bat
echo.

:end
pause
