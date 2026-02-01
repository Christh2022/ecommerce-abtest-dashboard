# Setup script for git hooks and security tools
# Run this script after cloning the repository

Write-Host "🔧 Configuration des outils de sécurité..." -ForegroundColor Cyan

# Check Python
Write-Host "`n Vérification de Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " Python détecté: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host " Python non trouvé. Installez Python 3.11+ depuis https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Install pre-commit
Write-Host "` Installation de pre-commit..." -ForegroundColor Yellow
pip install pre-commit detect-secrets 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host " pre-commit installé" -ForegroundColor Green
} else {
    Write-Host " Erreur lors de l'installation de pre-commit" -ForegroundColor Red
    exit 1
}

# Install pre-commit hooks
Write-Host "`n🎣 Installation des hooks Git..." -ForegroundColor Yellow
pre-commit install
if ($LASTEXITCODE -eq 0) {
    Write-Host " Hooks Git installés" -ForegroundColor Green
} else {
    Write-Host " Erreur lors de l'installation des hooks" -ForegroundColor Red
    exit 1
}

# Generate secrets baseline
Write-Host "`n Génération du baseline de détection de secrets..." -ForegroundColor Yellow
if (Test-Path ".secrets.baseline") {
    Write-Host "  Baseline existant trouvé, conservation..." -ForegroundColor Yellow
} else {
    detect-secrets scan --baseline .secrets.baseline
    if ($LASTEXITCODE -eq 0) {
        Write-Host " Baseline créé" -ForegroundColor Green
    } else {
        Write-Host "  Erreur lors de la création du baseline (non critique)" -ForegroundColor Yellow
    }
}

# Create .env if not exists
Write-Host "` Configuration de l'environnement..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  Fichier .env existant trouvé" -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host " Fichier .env créé depuis .env.example" -ForegroundColor Green
    Write-Host "  IMPORTANT: Éditez .env et changez les mots de passe!" -ForegroundColor Red
}

# Run pre-commit on all files
Write-Host "` Test des hooks sur tous les fichiers..." -ForegroundColor Yellow
Write-Host "   (Ceci peut prendre quelques minutes la première fois)" -ForegroundColor Gray
pre-commit run --all-files
if ($LASTEXITCODE -eq 0) {
    Write-Host " Tous les checks passent!" -ForegroundColor Green
} else {
    Write-Host "  Certains checks ont échoué. Vérifiez les messages ci-dessus." -ForegroundColor Yellow
    Write-Host "   Vous pouvez corriger les problèmes et relancer: pre-commit run --all-files" -ForegroundColor Gray
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host " Configuration terminée!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "` Prochaines étapes:" -ForegroundColor Yellow
Write-Host "   1. Éditez .env et changez tous les mots de passe" -ForegroundColor White
Write-Host "   2. Lisez docs/SECRETS_MANAGEMENT.md pour les bonnes pratiques" -ForegroundColor White
Write-Host "   3. Les hooks Git vont maintenant vérifier chaque commit" -ForegroundColor White
Write-Host "   4. Lancez l'application: docker-compose -f docker-compose.secure.yml up -d" -ForegroundColor White

Write-Host "`n Sécurité:" -ForegroundColor Yellow
Write-Host "   - Ne commitez JAMAIS le fichier .env" -ForegroundColor Red
Write-Host "   - Utilisez des mots de passe forts (>= 16 caractères)" -ForegroundColor White
Write-Host "   - Activez la 2FA sur GitHub" -ForegroundColor White

Write-Host "`n"
