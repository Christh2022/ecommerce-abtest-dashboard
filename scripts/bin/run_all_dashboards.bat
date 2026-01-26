@echo off
REM Script batch pour exécuter tous les scripts de création de dashboards
REM Usage: run_all_dashboards.bat

echo ========================================
echo Creation de tous les dashboards Grafana
echo ========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.x et reessayer
    pause
    exit /b 1
)

REM Exécuter le script Python
python run_all_dashboards.py

REM Capturer le code de retour
if errorlevel 1 (
    echo.
    echo [ERREUR] Certains dashboards n'ont pas pu etre crees
    echo Verifiez que Grafana est accessible et que les credentials sont corrects
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCES] Tous les dashboards ont ete crees avec succes!
    pause
    exit /b 0
)
