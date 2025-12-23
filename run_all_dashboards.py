#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour exécuter tous les scripts de création de dashboards dans l'ordre.

Usage:
    python run_all_dashboards.py

Variables d'environnement:
    GRAFANA_URL      - URL de Grafana (défaut: http://localhost:3000)
    GRAFANA_USER     - Utilisateur Grafana (défaut: admin)
    GRAFANA_PASSWORD - Mot de passe Grafana (défaut: admin123)
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(message):
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{message}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")

def print_success(message):
    print(f"{GREEN}✓{RESET} {message}")

def print_error(message):
    print(f"{RED}✗{RESET} {message}")

def print_info(message):
    print(f"{BLUE}→{RESET} {message}")

def run_script(script_path, description):
    """Exécute un script Python et retourne True si succès"""
    print_info(f"Exécution: {description}")
    print(f"  Script: {script_path.name}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print_success(f"Succès: {description}")
            if "created successfully" in result.stdout or "créé avec succès" in result.stdout:
                print(f"  {result.stdout.strip()}")
            return True
        else:
            print_error(f"Échec: {description}")
            if result.stderr:
                print(f"  Erreur: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print_error(f"Timeout: {description} (>30s)")
        return False
    except Exception as e:
        print_error(f"Exception: {description}")
        print(f"  {str(e)}")
        return False

def main():
    print_header("🚀 Création Automatique de Tous les Dashboards Grafana")
    
    # Configuration
    grafana_url = os.getenv('GRAFANA_URL', 'http://localhost:3000')
    grafana_user = os.getenv('GRAFANA_USER', 'admin')
    
    print(f"{BLUE}Configuration:{RESET}")
    print(f"  Grafana URL: {grafana_url}")
    print(f"  Utilisateur: {grafana_user}")
    print()
    
    # Répertoire des scripts
    project_root = Path(__file__).parent.absolute()
    dashboards_dir = project_root / "grafana_dashboards_scripts"
    
    if not dashboards_dir.exists():
        print_error(f"Le dossier {dashboards_dir} n'existe pas!")
        return 1
    
    # Liste des scripts à exécuter dans l'ordre
    scripts_to_run = [
        ("create_dashboards_1_3.py", "Dashboards 1-3 (Funnel, Segmentation, Products)"),
        ("create_dashboards_4_6.py", "Dashboards 4-6 (Cohorts, Real-Time, Predictive)"),
        ("create_bi_dashboard.py", "Business Intelligence Dashboard"),
        ("create_full_dashboard.py", "E-Commerce A/B Test Analytics Dashboard"),
        ("create_monitoring_dashboard.py", "Monitoring Dashboard"),
        ("create_prometheus_dashboard.py", "Prometheus Dashboard"),
    ]
    
    # Statistiques
    total = len(scripts_to_run)
    success_count = 0
    failed_scripts = []
    
    # Exécution des scripts
    for i, (script_name, description) in enumerate(scripts_to_run, 1):
        print(f"\n{BOLD}[{i}/{total}]{RESET} {description}")
        print("-" * 70)
        
        script_path = dashboards_dir / script_name
        
        if not script_path.exists():
            print_error(f"Script introuvable: {script_name}")
            failed_scripts.append((script_name, "Fichier introuvable"))
            continue
        
        if run_script(script_path, description):
            success_count += 1
            time.sleep(2)  # Pause entre les scripts
        else:
            failed_scripts.append((script_name, "Erreur d'exécution"))
    
    # Résumé final
    print_header("📊 Résumé de l'Exécution")
    
    print(f"Total: {total} scripts")
    print_success(f"Succès: {success_count}/{total}")
    
    if failed_scripts:
        print_error(f"Échecs: {len(failed_scripts)}/{total}")
        print("\n" + YELLOW + "Scripts en échec:" + RESET)
        for script_name, reason in failed_scripts:
            print(f"  • {script_name}: {reason}")
    
    print(f"\n{BLUE}🌐 Accédez à Grafana:{RESET} {grafana_url}")
    print(f"   Utilisateur: {grafana_user}")
    print()
    
    # Code de retour
    if success_count == total:
        print_success("✨ Tous les dashboards ont été créés avec succès!")
        return 0
    elif success_count > 0:
        print(f"{YELLOW}⚠{RESET}  Certains dashboards ont échoué mais d'autres ont été créés.")
        return 1
    else:
        print_error("Aucun dashboard n'a pu être créé. Vérifiez la configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
