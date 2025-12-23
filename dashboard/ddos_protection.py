"""
Protection Anti-DDoS pour Flask/Dash
Implémente rate limiting et détection d'abus
"""

from flask import request, jsonify
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
import time

class RateLimiter:
    """Rate limiter simple en mémoire"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.blocked_ips = {}
        
    def is_rate_limited(self, ip, max_requests=100, window_seconds=60):
        """
        Vérifie si une IP dépasse le rate limit
        
        Args:
            ip: Adresse IP
            max_requests: Nombre max de requêtes
            window_seconds: Fenêtre de temps en secondes
        """
        now = datetime.now()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Nettoyer les anciennes requêtes
        self.requests[ip] = [
            req_time for req_time in self.requests[ip]
            if req_time > window_start
        ]
        
        # Vérifier si bloqué
        if ip in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]
        
        # Vérifier le nombre de requêtes
        if len(self.requests[ip]) >= max_requests:
            # Bloquer pour 5 minutes
            self.blocked_ips[ip] = datetime.now() + timedelta(minutes=5)
            return True
        
        # Enregistrer la requête
        self.requests[ip].append(now)
        return False
    
    def get_stats(self, ip):
        """Obtenir les statistiques pour une IP"""
        now = datetime.now()
        window_start = now - timedelta(seconds=60)
        
        recent_requests = [
            req_time for req_time in self.requests[ip]
            if req_time > window_start
        ]
        
        return {
            'ip': ip,
            'requests_last_minute': len(recent_requests),
            'is_blocked': ip in self.blocked_ips,
            'blocked_until': self.blocked_ips.get(ip)
        }

# Instance globale
rate_limiter = RateLimiter()

def rate_limit(max_requests=100, window_seconds=60):
    """
    Décorateur pour ajouter le rate limiting à une route
    
    Usage:
        @app.route('/api/data')
        @rate_limit(max_requests=50, window_seconds=60)
        def api_data():
            return jsonify({'data': 'value'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            
            if rate_limiter.is_rate_limited(ip, max_requests, window_seconds):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Maximum {max_requests} per {window_seconds}s',
                    'retry_after': 300
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def setup_ddos_protection(app):
    """
    Configure la protection DDoS sur l'application Flask
    
    Args:
        app: Instance Flask/Dash server
    """
    
    @app.before_request
    def check_rate_limit():
        """Vérifie le rate limit avant chaque requête"""
        ip = request.remote_addr
        
        # Exclure certaines routes du rate limiting
        excluded_paths = ['/health', '/_dash-', '/assets/']
        if any(request.path.startswith(path) for path in excluded_paths):
            return None
        
        # Rate limit agressif pour les routes sensibles
        sensitive_paths = ['/login', '/api/']
        if any(request.path.startswith(path) for path in sensitive_paths):
            if rate_limiter.is_rate_limited(ip, max_requests=20, window_seconds=60):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': 'Too many requests to sensitive endpoint',
                }), 429
        
        # Rate limit général
        if rate_limiter.is_rate_limited(ip, max_requests=200, window_seconds=60):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests',
            }), 429
        
        return None
    
    @app.route('/api/rate-limit-status')
    def rate_limit_status():
        """Endpoint pour vérifier son statut de rate limit"""
        ip = request.remote_addr
        stats = rate_limiter.get_stats(ip)
        return jsonify(stats)
    
    print("✅ Protection DDoS activée")
    print("   - Rate limiting: 200 req/min (général)")
    print("   - Rate limiting: 20 req/min (endpoints sensibles)")
    print("   - Blocage automatique: 5 minutes")

# Exemple d'utilisation dans app.py:
"""
from ddos_protection import setup_ddos_protection, rate_limit

# Dans l'initialisation de l'app
setup_ddos_protection(server)

# Pour des routes spécifiques
@server.route('/api/expensive-operation')
@rate_limit(max_requests=10, window_seconds=60)
def expensive_operation():
    return jsonify({'status': 'ok'})
"""
