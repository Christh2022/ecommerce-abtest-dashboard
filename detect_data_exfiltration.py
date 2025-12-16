#!/usr/bin/env python3
"""
Script de détection d'exfiltration de données
Analyse les logs, connexions réseau et accès aux données sensibles
"""

import subprocess
import json
from datetime import datetime, timedelta
import re

def check_suspicious_database_queries():
    """Vérifie les requêtes PostgreSQL suspectes (SELECT * massifs)"""
    print("\n=== 🗄️  Vérification des requêtes PostgreSQL suspectes ===")
    
    cmd = """docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -t -c "
        SELECT 
            query_start,
            usename,
            application_name,
            LEFT(query, 150) as query,
            state
        FROM pg_stat_activity 
        WHERE datname = 'ecommerce_db' 
            AND query NOT LIKE '%pg_stat_activity%'
            AND state != 'idle'
        ORDER BY query_start DESC
        LIMIT 20;
    " """
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(f"✅ Connexions actives trouvées:")
            print(result.stdout)
        else:
            print("✅ Aucune requête active suspecte")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def check_suspicious_network_connections():
    """Vérifie les connexions réseau sortantes suspectes depuis les containers"""
    print("\n=== 🌐 Vérification des connexions réseau sortantes ===")
    
    containers = ['ecommerce-dashboard', 'ecommerce-postgres']
    
    for container in containers:
        cmd = f"docker exec {container} sh -c 'netstat -an 2>/dev/null || ss -an 2>/dev/null || echo \"Tool not available\"'"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            established = [line for line in result.stdout.split('\n') if 'ESTABLISHED' in line or 'ESTAB' in line]
            
            if established:
                print(f"\n📡 {container} - Connexions établies: {len(established)}")
                # Filtrer uniquement les connexions externes (pas localhost/Docker)
                external = [conn for conn in established if not any(x in conn for x in ['127.0.0.1', '172.', '::1'])]
                if external:
                    print(f"⚠️  Connexions externes détectées:")
                    for conn in external[:5]:
                        print(f"   {conn.strip()}")
            else:
                print(f"✅ {container} - Aucune connexion suspecte")
        except Exception as e:
            print(f"❌ Erreur pour {container}: {e}")

def check_large_data_transfers():
    """Vérifie les transferts de données volumineux dans les logs"""
    print("\n=== 📊 Vérification des transferts de données volumineux ===")
    
    cmd = "docker logs ecommerce-dashboard --since 1h 2>&1 | grep -iE 'SELECT.*FROM|export|dump|download|transfer' | head -20"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            lines = result.stdout.split('\n')
            print(f"⚠️  {len(lines)} requêtes de récupération de données trouvées:")
            for line in lines[:10]:
                print(f"   {line.strip()}")
        else:
            print("✅ Aucun transfert volumineux détecté")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def check_failed_auth_attempts():
    """Détecte les tentatives d'authentification échouées (brute force)"""
    print("\n=== 🔐 Vérification des tentatives d'authentification échouées ===")
    
    cmd = "docker logs ecommerce-dashboard --since 1h 2>&1 | grep -iE 'login.*failed|authentication.*failed|unauthorized|invalid.*credentials' | wc -l"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        count = int(result.stdout.strip() or 0)
        
        if count > 10:
            print(f"🚨 ALERTE: {count} tentatives d'authentification échouées détectées!")
            # Montrer quelques exemples
            cmd2 = "docker logs ecommerce-dashboard --since 1h 2>&1 | grep -iE 'login.*failed|authentication.*failed' | tail -5"
            examples = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
            print("Exemples:")
            print(examples.stdout)
        elif count > 0:
            print(f"⚠️  {count} tentatives échouées (normal si tests en cours)")
        else:
            print("✅ Aucune tentative d'authentification échouée")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def check_sensitive_data_access():
    """Vérifie l'accès aux données sensibles (tables users, credentials, etc.)"""
    print("\n=== 🔒 Vérification des accès aux données sensibles ===")
    
    sensitive_tables = ['users', 'credentials', 'payment', 'credit_card']
    
    for table in sensitive_tables:
        cmd = f"docker logs ecommerce-postgres --since 1h 2>&1 | grep -i 'SELECT.*FROM.*{table}' | wc -l"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            count = int(result.stdout.strip() or 0)
            
            if count > 0:
                print(f"⚠️  Table '{table}': {count} accès détectés")
            else:
                print(f"✅ Table '{table}': Aucun accès")
        except Exception as e:
            print(f"❌ Erreur pour {table}: {e}")

def check_prometheus_attack_metrics():
    """Vérifie les métriques d'attaques dans Prometheus"""
    print("\n=== 📈 Métriques d'attaques (Prometheus) ===")
    
    queries = {
        "Injections SQL": "sum(security_attacks_total{attack_type=~'sql.*'})",
        "Exfiltration de données": "sum(security_attacks_total{attack_type=~'.*exfiltration.*|.*exposure.*'})",
        "Total attaques critiques": "sum(security_attacks_total{severity='critical'})",
    }
    
    for name, query in queries.items():
        cmd = f"curl -s 'http://localhost:9091/metrics' | grep -E 'security_attacks_total' | grep -v '^#'"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            
            if name == "Injections SQL":
                sql_attacks = [l for l in lines if 'sql_injection' in l]
                if sql_attacks:
                    print(f"🚨 {name}: {len(sql_attacks)} détectées")
                    for attack in sql_attacks[:3]:
                        match = re.search(r'} (\d+)', attack)
                        if match:
                            print(f"   → {match.group(1)} tentatives")
            elif name == "Exfiltration de données":
                exfil = [l for l in lines if any(x in l for x in ['exfiltration', 'exposure', 'leakage'])]
                if exfil:
                    print(f"⚠️  {name}: {len(exfil)} types détectés")
            elif name == "Total attaques critiques":
                critical = [l for l in lines if 'critical' in l]
                if critical:
                    total = sum(int(re.search(r'} (\d+)', l).group(1)) for l in critical if re.search(r'} (\d+)', l))
                    print(f"🔴 {name}: {total} attaques")
                    
        except Exception as e:
            print(f"❌ Erreur pour '{name}': {e}")

def generate_report():
    """Génère un rapport complet de sécurité"""
    print("\n" + "="*60)
    print("RAPPORT DE DETECTION D'EXFILTRATION DE DONNEES")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    check_failed_auth_attempts()
    check_suspicious_database_queries()
    check_large_data_transfers()
    check_sensitive_data_access()
    check_suspicious_network_connections()
    check_prometheus_attack_metrics()
    
    print("\n" + "="*60)
    print("RECOMMANDATIONS:")
    print("="*60)
    print("""
1. ✅ Vérifiez le dashboard Grafana: http://localhost:3000
2. ✅ Consultez les alertes actives: http://localhost:3000/alerting/list
3. ✅ Examinez les logs détaillés: docker logs ecommerce-dashboard -f
4. ✅ Vérifiez les fichiers exfiltrés: ls -lh security-reports/exfiltrated-data/
5. ✅ Analysez le rapport JSON: security-reports/attack-results/
    """)

if __name__ == "__main__":
    generate_report()
