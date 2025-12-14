@echo off
REM ========================================
REM Verification du systeme de detection
REM ========================================

echo.
echo ========================================
echo VERIFICATION DU SYSTEME
echo ========================================
echo.

REM 1. Services Docker
echo [1/6] Verification des services Docker...
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr ecommerce
echo.

REM 2. Pushgateway
echo [2/6] Test de connexion Pushgateway (port 9091)...
curl -s http://localhost:9091/metrics | findstr "security_attacks" >nul 2>&1
if errorlevel 1 (
    echo ❌ Pas de metriques security_attacks trouvees
    echo Executez d'abord: lancer_tests_securite.bat
) else (
    echo ✓ Metriques security_attacks trouvees!
)
echo.

REM 3. Prometheus
echo [3/6] Verification Prometheus...
docker logs ecommerce-prometheus 2>&1 | findstr "pushgateway" | findstr "up" >nul 2>&1
if errorlevel 1 (
    echo ⚠ Impossible de verifier le scraping de Pushgateway
) else (
    echo ✓ Prometheus scrape Pushgateway
)
echo.

REM 4. Grafana
echo [4/6] Test de connexion Grafana (port 3000)...
curl -s http://localhost:3000/api/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Grafana n'est pas accessible
) else (
    echo ✓ Grafana est accessible
)
echo.

REM 5. Compter les metriques
echo [5/6] Comptage des metriques dans Pushgateway...
curl -s http://localhost:9091/metrics | findstr /C:"security_attacks_total" | find /C "security_attacks_total{" >nul 2>&1
if errorlevel 1 (
    echo ⚠ Aucune metrique trouvee - Lancez les tests
) else (
    echo ✓ Metriques presentes
)
echo.

REM 6. Dernier rapport
echo [6/6] Dernier rapport genere...
dir /B /O-D security-reports\attack-results\*.json 2>nul | findstr /R "^security_test.*\.json$" >nul 2>&1
if errorlevel 1 (
    echo ⚠ Aucun rapport trouve
) else (
    echo ✓ Rapports disponibles dans security-reports/attack-results/
    for /F "delims=" %%i in ('dir /B /O-D security-reports\attack-results\*.json 2^>nul') do (
        echo   Dernier: %%i
        goto :done
    )
    :done
)
echo.

echo ========================================
echo RESUME
echo ========================================
echo.
echo Services a verifier:
echo - Grafana Dashboard: http://localhost:3000
echo - Alertes Grafana: http://localhost:3000/alerting/list
echo - Pushgateway: http://localhost:9091
echo.
echo Pour lancer les tests:
echo   lancer_tests_securite.bat
echo.
pause
