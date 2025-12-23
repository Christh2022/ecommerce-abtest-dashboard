@echo off
REM Script d'installation du système d'authentification (Windows)
REM Usage: install_auth.bat

echo ================================================
echo Installation du systeme d'authentification
echo ================================================
echo.

cd /d "%~dp0"

echo Installation des dependances Python...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo [OK] Dependances installees avec succes
) else (
    echo [ERREUR] Erreur lors de l'installation des dependances
    exit /b 1
)

echo.
echo Verification du module d'authentification...
python -c "from auth import AuthManager; print('[OK] Module auth charge avec succes')"

if %ERRORLEVEL% EQU 0 (
    echo [OK] Module d'authentification operationnel
) else (
    echo [ERREUR] Erreur lors du chargement du module d'authentification
    exit /b 1
)

echo.
echo ================================================
echo Installation terminee avec succes!
echo ================================================
echo.
echo Pour demarrer le dashboard:
echo   cd dashboard
echo   python app.py
echo.
echo Comptes par defaut:
echo   Admin: admin / admin123
echo   User:  user / user123
echo.
echo Documentation: dashboard\AUTH_README.md
echo ================================================
pause
