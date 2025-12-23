@echo off
REM Script de test pour Windows
REM Lance la suite de tests de l'application

echo ========================================
echo   E-Commerce A/B Test Dashboard
echo   Suite de tests
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Installez Python depuis https://www.python.org/
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo Installation des dépendances...
pip install -q requests
echo.

REM Lancer les tests
echo Lancement des tests...
echo.
python run_tests.py

echo.
pause
