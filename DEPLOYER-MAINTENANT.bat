@echo off
chcp 65001 >nul
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🚀 DÉPLOIEMENT AUTOMATIQUE - BRIGITTE
echo ═══════════════════════════════════════════════════════════════
echo.
echo 👤 Compte GitHub : brigitte-fauv
echo 📧 Email : brigitte@arkange.io
echo 📦 Dépôt : https://github.com/brigitte-fauv/salescoach
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo ⚠️  AVANT DE CONTINUER :
echo.
echo    Avez-vous créé le dépôt sur GitHub ?
echo    https://github.com/new
echo.
echo    Nom du dépôt : salescoach
echo    Type : Public
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🔍 Vérification de Git...
echo ═══════════════════════════════════════════════════════════════
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git n'est pas installé !
    echo.
    echo 📥 Options :
    echo    1. Git pour Windows : https://git-scm.com/download/win
    echo    2. GitHub Desktop : https://desktop.github.com/
    echo.
    echo Installez l'un des deux et relancez ce script.
    echo.
    pause
    exit /b 1
)

echo ✅ Git est installé
git --version
echo.

echo ═══════════════════════════════════════════════════════════════
echo 👤 Configuration de votre identité Git...
echo ═══════════════════════════════════════════════════════════════
echo.

git config user.name "brigitte-fauv"
git config user.email "brigitte@arkange.io"

echo ✅ Identité configurée :
echo    Nom : brigitte-fauv
echo    Email : brigitte@arkange.io
echo.

echo ═══════════════════════════════════════════════════════════════
echo 📦 Initialisation du dépôt Git...
echo ═══════════════════════════════════════════════════════════════
echo.

if exist ".git" (
    echo ℹ️  Dépôt Git déjà initialisé
) else (
    git init
    if errorlevel 1 (
        echo ❌ Erreur lors de l'initialisation
        pause
        exit /b 1
    )
    echo ✅ Dépôt Git initialisé
)
echo.

echo ═══════════════════════════════════════════════════════════════
echo 📝 Ajout des fichiers au commit...
echo ═══════════════════════════════════════════════════════════════
echo.

git add .
if errorlevel 1 (
    echo ❌ Erreur lors de l'ajout des fichiers
    pause
    exit /b 1
)

echo ✅ Tous les fichiers ont été ajoutés
echo.

echo ═══════════════════════════════════════════════════════════════
echo 💾 Création du commit...
echo ═══════════════════════════════════════════════════════════════
echo.

git commit -m "Déploiement SalesCoach sur Render.com"
if errorlevel 1 (
    echo ℹ️  Aucun changement à commiter ou commit déjà fait
)
echo.

echo ═══════════════════════════════════════════════════════════════
echo 🌿 Configuration de la branche main...
echo ═══════════════════════════════════════════════════════════════
echo.

git branch -M main
echo ✅ Branche principale configurée
echo.

echo ═══════════════════════════════════════════════════════════════
echo 🔗 Liaison avec GitHub...
echo ═══════════════════════════════════════════════════════════════
echo.

git remote remove origin 2>nul
git remote add origin https://github.com/brigitte-fauv/salescoach.git

echo ✅ Dépôt lié à : https://github.com/brigitte-fauv/salescoach
echo.

echo ═══════════════════════════════════════════════════════════════
echo 🚀 Envoi du code vers GitHub...
echo ═══════════════════════════════════════════════════════════════
echo.
echo ⚠️  Git va vous demander de vous authentifier :
echo    - Nom d'utilisateur : brigitte-fauv
echo    - Mot de passe : votre mot de passe GitHub
echo      (ou Personal Access Token si 2FA activé)
echo.
echo Si une fenêtre s'ouvre, entrez vos identifiants GitHub.
echo.
pause
echo.

git push -u origin main
if errorlevel 1 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ❌ ERREUR lors de l'envoi vers GitHub
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo 💡 Causes possibles :
    echo.
    echo 1. Le dépôt n'existe pas sur GitHub
    echo    → Créez-le sur : https://github.com/new
    echo    → Nom : salescoach
    echo.
    echo 2. Problème d'authentification
    echo    → Vérifiez votre nom d'utilisateur et mot de passe
    echo    → Si 2FA activé, utilisez un Personal Access Token :
    echo      https://github.com/settings/tokens
    echo.
    echo 3. Le dépôt existe déjà avec du contenu
    echo    → Utilisez : git pull origin main --allow-unrelated-histories
    echo    → Puis relancez ce script
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo ✅ SUCCÈS ! Code envoyé sur GitHub
echo ═══════════════════════════════════════════════════════════════
echo.
echo Votre code est maintenant disponible sur :
echo https://github.com/brigitte-fauv/salescoach
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🎯 PROCHAINE ÉTAPE : RENDER.COM
echo ═══════════════════════════════════════════════════════════════
echo.
echo 1. Allez sur : https://render.com
echo.
echo 2. Cliquez "Get Started for Free"
echo.
echo 3. Choisissez "Sign in with GitHub"
echo    (Utilisez votre compte : brigitte-fauv)
echo.
echo 4. Autorisez Render à accéder à vos dépôts
echo.
echo 5. Dans le dashboard :
echo    - Cliquez "New +" (en haut à droite)
echo    - Sélectionnez "Blueprint"
echo    - Trouvez "salescoach"
echo    - Cliquez "Connect"
echo    - Cliquez "Apply"
echo.
echo 6. ⚠️  IMPORTANT : Ajoutez GEMINI_API_KEY
echo    - Cliquez sur "salescoach-backend"
echo    - Environment → GEMINI_API_KEY → Edit
echo    - Collez votre clé (depuis backend\.env)
echo    - Save Changes
echo.
echo 7. Attendez 5-10 minutes (déploiement automatique)
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎉 Votre application sera accessible sur :
echo    https://salescoach-frontend.onrender.com
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📋 Pour plus de détails, consultez :
echo    INSTRUCTIONS-BRIGITTE.txt
echo.
echo ═══════════════════════════════════════════════════════════════
pause
