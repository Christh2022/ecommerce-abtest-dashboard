#!/usr/bin/env python3
"""
Audit des headers de sécurité HTTP
Vérifie la présence des headers de sécurité recommandés
"""

import requests

TARGET_URL = 'http://localhost:8050'

REQUIRED_SECURITY_HEADERS = {
    'Strict-Transport-Security': {
        'description': 'Force HTTPS (HSTS)',
        'severity': 'HIGH',
        'recommended': 'max-age=31536000; includeSubDomains'
    },
    'X-Frame-Options': {
        'description': 'Protection contre Clickjacking',
        'severity': 'HIGH',
        'recommended': 'DENY ou SAMEORIGIN'
    },
    'X-Content-Type-Options': {
        'description': 'Empêche MIME sniffing',
        'severity': 'MEDIUM',
        'recommended': 'nosniff'
    },
    'X-XSS-Protection': {
        'description': 'Protection XSS du navigateur',
        'severity': 'MEDIUM',
        'recommended': '1; mode=block'
    },
    'Content-Security-Policy': {
        'description': 'Politique de sécurité du contenu (CSP)',
        'severity': 'HIGH',
        'recommended': "default-src 'self'"
    },
    'Referrer-Policy': {
        'description': 'Contrôle les informations de référence',
        'severity': 'LOW',
        'recommended': 'no-referrer ou strict-origin-when-cross-origin'
    },
    'Permissions-Policy': {
        'description': 'Contrôle des permissions du navigateur',
        'severity': 'LOW',
        'recommended': 'geolocation=(), microphone=(), camera=()'
    }
}

def check_security_headers():
    """Vérifie les headers de sécurité"""
    print("="*70)
    print("🔍 AUDIT DES HEADERS DE SÉCURITÉ HTTP")
    print("="*70)
    print(f"Target: {TARGET_URL}")
    print()
    
    try:
        response = requests.get(TARGET_URL, allow_redirects=False, timeout=5)
        headers = response.headers
        
        print(f"Status Code: {response.status_code}")
        print()
        print("-"*70)
        print("Headers présents:")
        print("-"*70)
        
        for header, value in headers.items():
            print(f"  {header}: {value}")
        
        print()
        print("="*70)
        print("📊 ANALYSE DES HEADERS DE SÉCURITÉ")
        print("="*70)
        print()
        
        vulnerabilities = []
        
        for header_name, info in REQUIRED_SECURITY_HEADERS.items():
            present = header_name in headers or header_name.lower() in [h.lower() for h in headers.keys()]
            
            severity_emoji = {
                'HIGH': '🔴',
                'MEDIUM': '🟠',
                'LOW': '🟡'
            }
            
            emoji = severity_emoji.get(info['severity'], '⚪')
            
            if present:
                header_value = headers.get(header_name, headers.get(header_name.lower(), ''))
                print(f"✅ {emoji} {header_name}")
                print(f"   Valeur: {header_value}")
            else:
                print(f"❌ {emoji} {header_name} - MANQUANT")
                print(f"   {info['description']}")
                print(f"   Recommandé: {info['recommended']}")
                vulnerabilities.append({
                    'header': header_name,
                    'severity': info['severity'],
                    'description': info['description']
                })
            print()
        
        print("="*70)
        print("📋 RÉSUMÉ")
        print("="*70)
        print()
        
        if vulnerabilities:
            print(f"🔴 {len(vulnerabilities)} headers de sécurité manquants")
            print()
            
            by_severity = {}
            for vuln in vulnerabilities:
                sev = vuln['severity']
                by_severity[sev] = by_severity.get(sev, 0) + 1
            
            if 'HIGH' in by_severity:
                print(f"  🔴 HIGH: {by_severity['HIGH']}")
            if 'MEDIUM' in by_severity:
                print(f"  🟠 MEDIUM: {by_severity['MEDIUM']}")
            if 'LOW' in by_severity:
                print(f"  🟡 LOW: {by_severity['LOW']}")
            
            print()
            print("Vulnérabilités détectées:")
            for vuln in vulnerabilities:
                print(f"  • {vuln['header']} ({vuln['severity']}): {vuln['description']}")
            
            print()
            print("="*70)
            print("⚠️  IMPACT DES VULNÉRABILITÉS")
            print("="*70)
            print()
            print("Sans headers de sécurité, l'application est vulnérable à:")
            print()
            print("  🔴 Clickjacking (X-Frame-Options manquant)")
            print("     → Un attaquant peut embarquer votre site dans une iframe")
            print("     → Vol de clics, phishing")
            print()
            print("  🔴 XSS (Content-Security-Policy manquant)")
            print("     → Scripts malicieux peuvent s'exécuter")
            print("     → Vol de cookies, session hijacking")
            print()
            print("  🟠 MIME Confusion (X-Content-Type-Options manquant)")
            print("     → Upload de fichiers malicieux exécutables")
            print()
            print("CVSS Score estimé: 7.5 (HIGH)")
            
        else:
            print("✅ Tous les headers de sécurité sont présents!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")

if __name__ == '__main__':
    check_security_headers()
