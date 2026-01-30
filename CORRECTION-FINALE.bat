@echo off
chcp 65001 >nul
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔧 CORRECTION FINALE - AUTORISATION HOST RENDER
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ Correction effectuée :
echo    Ajout de "salescoach-frontend.onrender.com" 
echo    dans la liste des hosts autorisés
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

git config user.name "brigitte-fauv"
git config user.email "brigitte@arkange.io"

echo 📦 Ajout des fichiers...
git add .

echo.
echo 💾 Création du commit...
git commit -m "Fix: Ajout allowedHosts pour Render.com"

if errorlevel 1 (
    echo ⚠️  Aucun changement à commiter
)

echo.
echo 🚀 Envoi vers GitHub...
git push origin main

if errorlevel 1 (
    echo.
    echo ❌ ERREUR - Entrez vos identifiants GitHub
    echo    Username : brigitte-fauv
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo ✅✅✅ SUCCÈS ! CORRECTION ENVOYÉE ✅✅✅
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎯 MAINTENANT :
echo.
echo 1. Allez sur https://render.com
echo.
echo 2. Cliquez sur "salescoach-frontend"
echo.
echo 3. Attendez que "Deploying..." se termine (2-3 min)
echo.
echo 4. Quand vous voyez "Deploy live" ✅
echo.
echo 5. Ouvrez : https://salescoach-frontend.onrender.com
echo.
echo 6. ✅ ÇA DEVRAIT MARCHER ! 🎉
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
