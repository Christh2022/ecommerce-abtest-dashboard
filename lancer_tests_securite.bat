@echo off
REM ========================================
REM Script de test des attaques de securite
REM Usage: Double-cliquer sur ce fichier
REM ========================================

echo.
echo ========================================
echo TEST DES ATTAQUES DE SECURITE
echo ========================================
echo.

REM Verifier que les services Docker sont en cours d'execution
echo [1/4] Verification des services Docker...
docker ps | findstr ecommerce-pushgateway >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Les services Docker ne sont pas en cours d'execution
    echo Lancez d'abord: docker-compose -f docker-compose.secure.yml up -d
    pause
    exit /b 1
)
echo ✓ Services Docker: OK
echo.

REM Verifier que Pushgateway est accessible
echo [2/4] Verification de Pushgateway...
curl -s http://localhost:9091/metrics >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Pushgateway n'est pas accessible sur le port 9091
    pause
    exit /b 1
)
echo ✓ Pushgateway: OK
echo.

REM Lancer les tests de securite
echo [3/4] Lancement des tests de securite...
echo.
python test_security_simple.py --target http://localhost:8050
if errorlevel 1 (
    echo.
    echo ERREUR: Les tests ont echoue
    pause
    exit /b 1
)
echo.

REM Afficher les resultats
echo [4/4] Tests termines avec succes!
echo.
echo ========================================
echo PROCHAINES ETAPES:
echo ========================================
echo.
echo 1. Ouvrez Grafana: http://localhost:3000
echo 2. Allez dans "Dashboards" ^> "Security Attacks Dashboard"
echo 3. Attendez 10-15 secondes pour voir les donnees
echo 4. Verifiez les alertes: http://localhost:3000/alerting/list
echo.
echo Les rapports sont sauvegardes dans:
echo security-reports/attack-results/
echo.
pause
