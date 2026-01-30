@echo off
echo.
echo ============================================
echo    SalesCoach - Lancement avec partage
echo ============================================
echo.
echo Lancement de PowerShell...
echo.

powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0lancer-avec-partage.ps1"

if errorlevel 1 (
    echo.
    echo ERREUR: Le script n'a pas pu se lancer
    echo.
    echo Solutions possibles:
    echo 1. Faites un clic droit sur ce fichier et "Executer en tant qu'administrateur"
    echo 2. Ou lancez directement: installer-cloudflare.ps1
    echo.
)

pause
