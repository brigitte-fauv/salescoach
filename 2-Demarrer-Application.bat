@echo off
title SalesCoach - Demarrage

cd /d "%~dp0"

echo.
echo ============================================
echo    SalesCoach - Lancement
echo ============================================
echo.

REM Verifier que cloudflared est installe
if not exist cloudflared.exe (
    echo ERREUR: cloudflared.exe non trouve !
    echo.
    echo Lancez d'abord: 1-Installer-Cloudflare.bat
    echo.
    pause
    exit /b 1
)

echo [1/3] Demarrage du backend Python...
cd backend
start "SalesCoach Backend" cmd /k "python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"
cd ..

echo [2/3] Attente du demarrage... (10 secondes)
timeout /t 10 /nobreak

echo [3/3] Demarrage du frontend...
cd frontend
start "SalesCoach Frontend" cmd /k "npm run dev"
cd ..

echo.
echo Attente du demarrage complet... (5 secondes)
timeout /t 5 /nobreak

echo.
echo ============================================
echo    Lancement du tunnel Cloudflare
echo ============================================
echo.
echo IMPORTANT: 
echo - Une nouvelle fenetre va s'ouvrir
echo - Cherchez l'URL: https://xxxxx.trycloudflare.com
echo - Copiez cette URL et envoyez-la a vos collegues
echo.
pause

start "Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel --url http://localhost:5173"

echo.
echo ============================================
echo    Tout est lance !
echo ============================================
echo.
echo Vos collegues peuvent acceder a l'application via l'URL
echo affichee dans la fenetre Cloudflare Tunnel.
echo.
echo ATTENTION: Ne fermez aucune fenetre !
echo.
pause
