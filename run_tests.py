#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de tests pour le projet e-commerce A/B testing dashboard
"""

import sys
import os
import unittest
from pathlib import Path

# Ajouter le répertoire parent au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "dashboard"))

def run_tests():
    """Exécute tous les tests du projet"""
    
    # Configurer le loader de tests
    loader = unittest.TestLoader()
    
    # Chercher tous les tests dans le répertoire dashboard
    dashboard_tests = loader.discover('dashboard', pattern='test_*.py')
    
    # Chercher tous les tests dans le répertoire scripts
    scripts_tests = loader.discover('scripts', pattern='test_*.py')
    
    # Combiner les suites de tests
    suite = unittest.TestSuite([dashboard_tests, scripts_tests])
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retourner le code de sortie approprié
    return 0 if result.wasSuccessful() else 1

def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("🧪 Exécution des tests du projet")
    print("=" * 60)
    print()
    
    try:
        exit_code = run_tests()
        
        print()
        print("=" * 60)
        if exit_code == 0:
            print("✅ Tous les tests ont réussi!")
        else:
            print("❌ Certains tests ont échoué")
        print("=" * 60)
        
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
