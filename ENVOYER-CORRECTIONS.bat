@echo off
chcp 65001 >nul
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    ✅ ENVOI DES CORRECTIONS SUR GITHUB
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🔧 Corrections effectuées :
echo    1. Ajout configuration preview dans vite.config.ts
echo    2. Autorisation de l'hôte Render.com
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

git config user.name "brigitte-fauv" 2>nul
git config user.email "brigitte@arkange.io" 2>nul

echo 📦 Ajout des fichiers modifiés...
git add frontend/vite.config.ts frontend/package.json frontend/src/components/Checklist.tsx

echo.
echo 💾 Création du commit...
git commit -m "Fix: Configuration Vite preview + correction TypeScript"

if errorlevel 1 (
    echo.
    echo ⚠️  Aucun changement à commiter ou déjà fait
    echo.
)

echo.
echo 🚀 Envoi vers GitHub...
git push origin main

if errorlevel 1 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ❌ ERREUR lors de l'envoi
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo 💡 Entrez vos identifiants GitHub :
    echo    Username : brigitte-fauv
    echo    Password : votre mot de passe GitHub
    echo.
    echo Si vous avez la 2FA activée, utilisez un Personal Access Token
    echo https://github.com/settings/tokens
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo ✅ SUCCÈS ! Corrections envoyées
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎯 QUE FAIRE MAINTENANT ?
echo.
echo 1. Allez sur https://render.com
echo.
echo 2. Vous verrez "Deploying..." sur salescoach-frontend
echo.
echo 3. Attendez 2-3 minutes que le déploiement se termine
echo.
echo 4. Quand vous voyez "Deploy live" avec une coche verte ✅
echo.
echo 5. Votre application sera accessible sur :
echo    👉 https://salescoach-frontend.onrender.com
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
