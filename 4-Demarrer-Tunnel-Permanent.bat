@echo off
title Cloudflare Tunnel Permanent

cd /d "%~dp0"

echo.
echo ============================================
echo    Demarrage du Tunnel Permanent
echo ============================================
echo.

if not exist config.yml (
    echo ERREUR: Fichier config.yml non trouve !
    echo.
    echo Executez d'abord: 3-Configuration-URL-Permanente.bat
    echo.
    pause
    exit /b 1
)

echo Demarrage du tunnel avec la configuration permanente...
echo.

cloudflared.exe tunnel --config config.yml run

pause
