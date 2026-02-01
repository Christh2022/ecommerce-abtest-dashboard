#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de redirection pour exécuter tous les dashboards Grafana
Ce fichier redirige vers le script principal dans scripts/utils/
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

# Importer et exécuter le script principal
from scripts.utils.run_all_dashboards import main

if __name__ == "__main__":
    main()
