#!/usr/bin/env python3
"""
Test rapide du rate limiting - envoie 250 requêtes pour déclencher le blocage
Limite: 200 req/min -> devrait bloquer après 200 requêtes
"""

import requests
import time
from datetime import datetime

TARGET = "http://localhost:8050/"
TOTAL_REQUESTS = 250
DELAY = 0.1  # 100ms entre les requêtes = 600 req/min théorique

print("🛡️  TEST DE RATE LIMITING")
print("=" * 50)
print(f"Target: {TARGET}")
print(f"Requêtes: {TOTAL_REQUESTS}")
print(f"Délai entre requêtes: {DELAY}s")
print(f"Limite attendue: 200 req/min → blocage après ~200 req")
print()

success_count = 0
blocked_count = 0
error_count = 0
blocked_started = False

print("[*] Début du test...\n")
start_time = time.time()

for i in range(1, TOTAL_REQUESTS + 1):
    try:
        response = requests.get(TARGET, timeout=5)
        
        if response.status_code == 429:
            blocked_count += 1
            if not blocked_started:
                blocked_started = True
                print(f"\n🚫 RATE LIMIT ACTIVÉ après {i-1} requêtes!")
                print(f"   Temps écoulé: {time.time() - start_time:.1f}s\n")
        elif response.status_code in [200, 302]:
            success_count += 1
        else:
            error_count += 1
            
        # Afficher progression toutes les 25 requêtes
        if i % 25 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed * 60
            status = "OK" if success_count == i else "BLOCKED" if blocked_count > 0 else "ERROR"
            print(f"[{i:3d}/{TOTAL_REQUESTS}] ✅ {success_count:3d} | 🚫 {blocked_count:3d} | ❌ {error_count:3d} | {rate:.0f} req/min | {status}")
            
        time.sleep(DELAY)
        
    except requests.exceptions.RequestException as e:
        error_count += 1
        if i % 50 == 0:
            print(f"[ERROR] Requête {i}: {str(e)[:50]}")

elapsed_time = time.time() - start_time
avg_rate = TOTAL_REQUESTS / elapsed_time * 60

print("\n" + "=" * 50)
print("📊 RÉSULTATS DU TEST")
print("=" * 50)
print(f"✅ Succès:       {success_count:3d} ({success_count/TOTAL_REQUESTS*100:.1f}%)")
print(f"🚫 Bloquées:     {blocked_count:3d} ({blocked_count/TOTAL_REQUESTS*100:.1f}%)")
print(f"❌ Erreurs:      {error_count:3d} ({error_count/TOTAL_REQUESTS*100:.1f}%)")
print(f"⏱️  Temps total:  {elapsed_time:.1f}s")
print(f"📈 Taux moyen:   {avg_rate:.0f} req/min")
print()

if blocked_count > 0:
    print("✅ PROTECTION DDOS FONCTIONNELLE!")
    print(f"   Le rate limiting a bloqué {blocked_count} requêtes")
else:
    print("⚠️  AUCUN BLOCAGE DÉTECTÉ")
    print("   Vérifiez que la protection DDoS est activée")

print("=" * 50)
