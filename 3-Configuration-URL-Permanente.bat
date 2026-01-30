@echo off
title Configuration Cloudflare Tunnel Permanent

cd /d "%~dp0"

echo.
echo ============================================
echo    Cloudflare Tunnel - Configuration Simplifiee
echo ============================================
echo.
echo IMPORTANT: Cette methode NE NECESSITE PAS de domaine !
echo.
echo PREREQUIS:
echo - Compte Cloudflare gratuit (https://dash.cloudflare.com/sign-up)
echo.
echo Appuyez sur une touche pour continuer...
pause >nul

echo.
echo [Etape 1/3] Connexion a votre compte Cloudflare...
echo.
echo Une page web va s'ouvrir pour vous connecter.
echo Connectez-vous avec votre compte Cloudflare.
echo.
pause

cloudflared.exe tunnel login

if errorlevel 1 (
    echo.
    echo ERREUR: Connexion echouee
    echo Verifiez que vous avez un compte Cloudflare.
    echo Creez-en un sur: https://dash.cloudflare.com/sign-up
    pause
    exit /b 1
)

echo.
echo Connexion reussie !
echo.

echo.
echo [Etape 2/3] Creation du tunnel permanent...
echo.
set /p TUNNEL_NAME="Entrez un nom pour votre tunnel (ex: salescoach): "

cloudflared.exe tunnel create %TUNNEL_NAME%

if errorlevel 1 (
    echo.
    echo ERREUR: Creation du tunnel echouee
    echo Le tunnel existe peut-etre deja ?
    echo.
    echo Liste des tunnels existants:
    cloudflared.exe tunnel list
    echo.
    echo Si votre tunnel existe deja, passez a l'etape suivante.
    pause
)

echo.
echo [Etape 3/3] Recuperation de l'ID du tunnel...
echo.

REM Lister les tunnels pour obtenir l'ID
echo Voici vos tunnels:
echo.
cloudflared.exe tunnel list

echo.
echo Notez l'ID du tunnel (colonne ID, format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
set /p TUNNEL_ID="Entrez l'ID du tunnel: "

echo.
echo Creation du fichier de configuration...
(
echo tunnel: %TUNNEL_ID%
echo credentials-file: %USERPROFILE%\.cloudflared\%TUNNEL_ID%.json
echo.
echo ingress:
echo   - service: http://localhost:5173
) > config.yml

echo.
echo ============================================
echo    Configuration terminee !
echo ============================================
echo.
echo Fichier config.yml cree avec succes !
echo.
echo Pour demarrer le tunnel permanent:
echo 1. Lancez: 2-Demarrer-Application.bat
echo 2. Puis lancez: 4-Demarrer-Tunnel-Permanent.bat
echo.
echo Le tunnel generera une URL permanente au demarrage.
echo.
pause
