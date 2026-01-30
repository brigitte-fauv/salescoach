@echo off
chcp 65001 >nul
echo.
echo ================================================
echo    📤 POUSSER LE CODE SUR GITHUB
echo ================================================
echo.
echo Ce script va préparer votre code pour Render.com
echo.
echo ⚠️  AVANT DE CONTINUER :
echo.
echo 1. Créez un compte sur https://github.com/signup
echo 2. Créez un nouveau dépôt nommé "salescoach"
echo 3. Copiez l'URL du dépôt (exemple : https://github.com/VOTRE-NOM/salescoach.git)
echo.
echo ================================================
echo.

echo ℹ️  Votre compte GitHub : brigitte-fauv
echo ℹ️  Email : brigitte@arkange.io
echo.
echo 📋 URL de votre dépôt devrait être :
echo    https://github.com/brigitte-fauv/salescoach.git
echo.

set /p "confirm=Est-ce correct ? (O/n) : "

if /i "%confirm%"=="n" (
    set /p "url=Entrez l'URL correcte : "
) else (
    set "url=https://github.com/brigitte-fauv/salescoach.git"
)

if "%url%"=="" (
    echo.
    echo ❌ ERREUR : Vous devez fournir une URL
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo 📋 Vérification de Git...
echo ================================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git n'est pas installé !
    echo.
    echo 📥 Téléchargez Git ici :
    echo https://git-scm.com/download/win
    echo.
    echo Ou utilisez GitHub Desktop :
    echo https://desktop.github.com/
    echo.
    pause
    exit /b 1
)

echo ✅ Git est installé !
echo.
echo ================================================
echo 📦 Initialisation du dépôt...
echo ================================================
echo.

git init
if errorlevel 1 (
    echo ❌ Erreur lors de l'initialisation
    pause
    exit /b 1
)

echo ✅ Dépôt initialisé
echo.
echo ================================================
echo 👤 Configuration Git...
echo ================================================
echo.

git config user.email "brigitte@arkange.io" 2>nul
git config user.name "brigitte-fauv" 2>nul
echo ✅ Configuration utilisateur définie
echo.
echo ================================================
echo 📝 Ajout des fichiers...
echo ================================================
echo.

git add .
if errorlevel 1 (
    echo ❌ Erreur lors de l'ajout des fichiers
    pause
    exit /b 1
)

echo ✅ Fichiers ajoutés
echo.
echo ================================================
echo 💾 Création du commit...
echo ================================================
echo.

git commit -m "Déploiement initial SalesCoach pour Render.com"
if errorlevel 1 (
    echo ⚠️  Aucun changement à commiter ou erreur
    echo.
)

echo.
echo ================================================
echo 🌿 Configuration de la branche principale...
echo ================================================
echo.

git branch -M main
echo ✅ Branche configurée
echo.
echo ================================================
echo 🔗 Liaison avec GitHub...
echo ================================================
echo.

git remote add origin %url% 2>nul
if errorlevel 1 (
    echo ℹ️  Remote déjà existant, mise à jour...
    git remote set-url origin %url%
)

echo ✅ Lié à GitHub
echo.
echo ================================================
echo 🚀 Envoi du code vers GitHub...
echo ================================================
echo.

git push -u origin main
if errorlevel 1 (
    echo.
    echo ❌ ERREUR lors de l'envoi
    echo.
    echo 💡 Solutions possibles :
    echo 1. Vérifiez que l'URL est correcte
    echo 2. Vérifiez votre connexion internet
    echo 3. Authentifiez-vous si demandé
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo ✅ SUCCÈS !
echo ================================================
echo.
echo Votre code est maintenant sur GitHub !
echo.
echo 🎯 PROCHAINE ÉTAPE :
echo.
echo 1. Allez sur https://render.com
echo 2. Connectez-vous avec GitHub
echo 3. Cliquez "New +" → "Blueprint"
echo 4. Sélectionnez votre dépôt "salescoach"
echo 5. Cliquez "Apply"
echo 6. Ajoutez votre GEMINI_API_KEY dans le backend
echo.
echo Votre app sera accessible sur :
echo https://salescoach-frontend.onrender.com
echo.
echo ================================================
pause
