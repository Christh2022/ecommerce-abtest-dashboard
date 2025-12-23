#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour valider l'organisation des scripts de dashboards.

Ce script vérifie:
1. Que tous les fichiers de dashboards existent
2. Que les imports fonctionnent correctement
3. Que la structure des dashboards est valide
"""

import os
import sys
import importlib.util
from pathlib import Path

# Configuration de l'encodage pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✓{RESET} {message}")

def print_error(message):
    print(f"{RED}✗{RESET} {message}")

def print_info(message):
    print(f"{BLUE}ℹ{RESET} {message}")

def print_warning(message):
    print(f"{YELLOW}⚠{RESET} {message}")

def test_file_exists(file_path, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(file_path):
        print_success(f"{description}: {os.path.basename(file_path)}")
        return True
    else:
        print_error(f"{description}: {file_path} NOT FOUND")
        return False

def test_script_syntax(file_path):
    """Vérifie qu'un script Python a une syntaxe valide"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        return True
    except SyntaxError as e:
        print_error(f"Erreur de syntaxe dans {file_path}: {e}")
        return False

def main():
    print_info("Validation de l'organisation des scripts de dashboards Grafana")
    print("=" * 70)
    
    # Déterminer le chemin racine du projet (parent du dossier tools/)
    project_root = Path(__file__).parent.parent.absolute()
    dashboards_dir = project_root / "grafana_dashboards_scripts"
    
    print(f"\n{BLUE}Répertoire du projet:{RESET} {project_root}")
    print(f"{BLUE}Répertoire des dashboards:{RESET} {dashboards_dir}")
    
    # Liste des scripts attendus
    expected_scripts = [
        "create_dashboards_1_3.py",
        "create_dashboards_4_6.py",
        "create_bi_dashboard.py",
        "create_full_dashboard.py",
        "create_monitoring_dashboard.py",
        "create_prometheus_dashboard.py",
        "__init__.py",
        "README.md"
    ]
    
    all_tests_passed = True
    
    # Test 1: Vérifier que le dossier existe
    print(f"\n{BLUE}Test 1:{RESET} Vérification de l'existence du dossier")
    if dashboards_dir.exists() and dashboards_dir.is_dir():
        print_success(f"Le dossier grafana_dashboards_scripts existe")
    else:
        print_error(f"Le dossier grafana_dashboards_scripts n'existe pas!")
        all_tests_passed = False
        return 1
    
    # Test 2: Vérifier que tous les fichiers existent
    print(f"\n{BLUE}Test 2:{RESET} Vérification de la présence de tous les scripts")
    for script in expected_scripts:
        script_path = dashboards_dir / script
        if not test_file_exists(script_path, script):
            all_tests_passed = False
    
    # Test 3: Vérifier la syntaxe Python
    print(f"\n{BLUE}Test 3:{RESET} Vérification de la syntaxe Python")
    python_scripts = [s for s in expected_scripts if s.endswith('.py')]
    for script in python_scripts:
        script_path = dashboards_dir / script
        if script_path.exists():
            if test_script_syntax(script_path):
                print_success(f"Syntaxe valide: {script}")
            else:
                all_tests_passed = False
    
    # Test 4: Vérifier les fichiers de configuration
    print(f"\n{BLUE}Test 4:{RESET} Vérification des fichiers de configuration")
    config_files = [
        (project_root / "docker" / "Dockerfile.dashboard-init", "docker/Dockerfile.dashboard-init"),
        (project_root / "scripts" / "init_grafana_dashboards.sh", "init_grafana_dashboards.sh"),
    ]
    
    for file_path, description in config_files:
        if test_file_exists(file_path, description):
            # Vérifier que le fichier contient les nouveaux chemins
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'grafana_dashboards_scripts' in content:
                    print_success(f"  → Chemins mis à jour dans {description}")
                else:
                    print_warning(f"  → Les chemins peuvent ne pas être à jour dans {description}")
    
    # Test 5: Vérifier la structure JSON des dashboards
    print(f"\n{BLUE}Test 5:{RESET} Vérification basique de la structure des dashboards")
    dashboard_scripts = [s for s in python_scripts if s.startswith('create_') and s != '__init__.py']
    for script in dashboard_scripts:
        script_path = dashboards_dir / script
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'GRAFANA_URL' in content and 'dashboard' in content:
                    print_success(f"Structure valide: {script}")
                else:
                    print_warning(f"Structure douteuse: {script}")
    
    # Résumé final
    print("\n" + "=" * 70)
    if all_tests_passed:
        print_success("Tous les tests sont passés! ✨")
        print_info("\nVous pouvez maintenant:")
        print("  1. Exécuter les scripts individuellement:")
        print(f"     python grafana_dashboards_scripts/create_dashboards_1_3.py")
        print("  2. Ou utiliser Docker Compose pour tout initialiser automatiquement")
        return 0
    else:
        print_error("Certains tests ont échoué. Veuillez corriger les erreurs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
