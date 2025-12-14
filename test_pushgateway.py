#!/usr/bin/env python3
"""
Test script pour vérifier l'envoi de métriques au Pushgateway
"""

from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
import time

# Configuration
PUSHGATEWAY_URL = "127.0.0.1:9091"

# Créer un registre
registry = CollectorRegistry()

# Créer des métriques de test
test_counter = Counter(
    'security_attacks_total',
    'Total security attacks performed',
    ['attack_type', 'severity', 'category'],
    registry=registry
)

print("🧪 Test d'envoi de métriques au Pushgateway...")
print(f"📡 URL: {PUSHGATEWAY_URL}")

# Simuler quelques attaques
attacks = [
    ('sql_injection', 'critical', 'injection'),
    ('xss', 'high', 'injection'),
    ('path_traversal', 'critical', 'file_attack'),
    ('command_injection', 'critical', 'injection'),
    ('parameter_tampering', 'high', 'data_manipulation'),
]

for attack_type, severity, category in attacks:
    # Incrémenter le compteur
    test_counter.labels(
        attack_type=attack_type,
        severity=severity,
        category=category
    ).inc()
    
    print(f"✅ Attack sent: {attack_type} ({severity})")
    
    # Envoyer au Pushgateway
    try:
        push_to_gateway(
            PUSHGATEWAY_URL,
            job='security_attacks',
            registry=registry
        )
        print(f"   ✓ Pushed to Pushgateway")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    time.sleep(1)

print("\n✅ Test terminé!")
print(f"\n📊 Vérifiez les métriques:")
print(f"   - Pushgateway: http://localhost:9091/metrics")
print(f"   - Prometheus: http://localhost:9090/graph")
print(f"   - Grafana: http://localhost:3000/d/security-attacks")
