#!/usr/bin/env python3
"""
Attack Metrics Exporter for Prometheus
Exposes security attack metrics for Grafana alerting
"""

from prometheus_client import start_http_server, Counter, Gauge, Info, Histogram
import time
import os
from datetime import datetime

# Port for Prometheus exporter
EXPORTER_PORT = int(os.getenv('ATTACK_EXPORTER_PORT', '9092'))

# ============================================================================
# ATTACK DETECTION COUNTERS
# ============================================================================

# Injection Attacks
sql_injection_attempts = Counter(
    'security_sql_injection_attempts_total',
    'Total SQL injection attempts detected',
    ['severity', 'payload_type']
)

nosql_injection_attempts = Counter(
    'security_nosql_injection_attempts_total',
    'Total NoSQL injection attempts detected',
    ['severity']
)

command_injection_attempts = Counter(
    'security_command_injection_attempts_total',
    'Total command injection attempts detected',
    ['severity', 'command_type']
)

ldap_injection_attempts = Counter(
    'security_ldap_injection_attempts_total',
    'Total LDAP injection attempts detected',
    ['severity']
)

xpath_injection_attempts = Counter(
    'security_xpath_injection_attempts_total',
    'Total XPath injection attempts detected',
    ['severity']
)

# Data Exposure
sensitive_data_exposure = Counter(
    'security_sensitive_data_exposure_total',
    'Sensitive data exposure incidents',
    ['data_type', 'severity']
)

information_disclosure = Counter(
    'security_information_disclosure_total',
    'Information disclosure incidents',
    ['disclosure_type', 'severity']
)

# Data Manipulation
parameter_tampering = Counter(
    'security_parameter_tampering_total',
    'Parameter tampering attempts',
    ['parameter', 'severity']
)

mass_assignment = Counter(
    'security_mass_assignment_total',
    'Mass assignment attempts',
    ['severity']
)

race_condition = Counter(
    'security_race_condition_total',
    'Race condition exploitation attempts',
    ['severity']
)

business_logic_abuse = Counter(
    'security_business_logic_abuse_total',
    'Business logic abuse attempts',
    ['abuse_type', 'severity']
)

# File Attacks
file_upload_vulnerability = Counter(
    'security_file_upload_attempts_total',
    'Malicious file upload attempts',
    ['file_type', 'severity']
)

path_traversal = Counter(
    'security_path_traversal_attempts_total',
    'Path traversal attempts',
    ['severity']
)

local_file_inclusion = Counter(
    'security_lfi_attempts_total',
    'Local file inclusion attempts',
    ['severity']
)

remote_file_inclusion = Counter(
    'security_rfi_attempts_total',
    'Remote file inclusion attempts',
    ['severity']
)

# Serialization Attacks
insecure_deserialization = Counter(
    'security_deserialization_attempts_total',
    'Insecure deserialization attempts',
    ['severity']
)

# Advanced Attacks
blind_sql_injection = Counter(
    'security_blind_sql_injection_total',
    'Blind SQL injection attempts',
    ['injection_type', 'severity']
)

second_order_injection = Counter(
    'security_second_order_injection_total',
    'Second-order injection attempts',
    ['severity']
)

polyglot_injection = Counter(
    'security_polyglot_injection_total',
    'Polyglot injection attempts',
    ['severity']
)

# API Attacks
excessive_data_exposure_api = Counter(
    'security_api_data_exposure_total',
    'API excessive data exposure',
    ['endpoint', 'severity']
)

bola_attack = Counter(
    'security_bola_attempts_total',
    'BOLA (Broken Object Level Authorization) attempts',
    ['resource', 'severity']
)

graphql_abuse = Counter(
    'security_graphql_abuse_total',
    'GraphQL abuse attempts',
    ['abuse_type', 'severity']
)

# Supply Chain
dependency_vulnerability = Counter(
    'security_dependency_exposure_total',
    'Vulnerable dependencies exposed',
    ['severity']
)

# Low & Slow Attacks
slow_exfiltration = Counter(
    'security_slow_exfiltration_total',
    'Slow data exfiltration attempts',
    ['severity']
)

rate_limit_bypass = Counter(
    'security_rate_limit_bypass_total',
    'Rate limiting bypass attempts',
    ['bypass_method', 'severity']
)

# Persistence Attacks
webshell_upload = Counter(
    'security_webshell_upload_total',
    'Webshell upload attempts',
    ['webshell_type', 'severity']
)

backdoor_creation = Counter(
    'security_backdoor_attempts_total',
    'Backdoor creation attempts',
    ['backdoor_type', 'severity']
)

# Data Exfiltration
dns_exfiltration = Counter(
    'security_dns_exfiltration_total',
    'DNS exfiltration attempts',
    ['severity']
)

api_exfiltration = Counter(
    'security_api_exfiltration_total',
    'Data exfiltration via legitimate API',
    ['endpoint', 'severity']
)

# Attack Chaining
attack_chain = Counter(
    'security_attack_chain_total',
    'Attack chaining detected',
    ['chain_type', 'severity']
)

# ============================================================================
# ATTACK METRICS GAUGES
# ============================================================================

total_attacks_last_hour = Gauge(
    'security_total_attacks_last_hour',
    'Total attacks in the last hour'
)

critical_vulnerabilities = Gauge(
    'security_critical_vulnerabilities_found',
    'Number of critical vulnerabilities found'
)

high_vulnerabilities = Gauge(
    'security_high_vulnerabilities_found',
    'Number of high severity vulnerabilities found'
)

data_exfiltrated_bytes = Gauge(
    'security_data_exfiltrated_bytes',
    'Total bytes of data exfiltrated'
)

active_attack_sources = Gauge(
    'security_active_attack_sources',
    'Number of active attack sources/IPs'
)

# ============================================================================
# ATTACK INFO
# ============================================================================

last_attack_info = Info(
    'security_last_attack',
    'Information about the last detected attack'
)

# ============================================================================
# ATTACK TIMING HISTOGRAM
# ============================================================================

attack_duration = Histogram(
    'security_attack_duration_seconds',
    'Duration of security attacks',
    ['attack_type']
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def record_attack(attack_type: str, severity: str, **labels):
    """Record an attack in the appropriate metric"""
    
    attack_metrics = {
        'sql_injection': sql_injection_attempts,
        'nosql_injection': nosql_injection_attempts,
        'command_injection': command_injection_attempts,
        'ldap_injection': ldap_injection_attempts,
        'xpath_injection': xpath_injection_attempts,
        'sensitive_data_exposure': sensitive_data_exposure,
        'information_disclosure': information_disclosure,
        'parameter_tampering': parameter_tampering,
        'mass_assignment': mass_assignment,
        'race_condition': race_condition,
        'business_logic_abuse': business_logic_abuse,
        'file_upload': file_upload_vulnerability,
        'path_traversal': path_traversal,
        'lfi': local_file_inclusion,
        'rfi': remote_file_inclusion,
        'deserialization': insecure_deserialization,
        'blind_sql': blind_sql_injection,
        'second_order_injection': second_order_injection,
        'polyglot_injection': polyglot_injection,
        'api_data_exposure': excessive_data_exposure_api,
        'bola': bola_attack,
        'graphql_abuse': graphql_abuse,
        'dependency_vuln': dependency_vulnerability,
        'slow_exfiltration': slow_exfiltration,
        'rate_limit_bypass': rate_limit_bypass,
        'webshell': webshell_upload,
        'backdoor': backdoor_creation,
        'dns_exfiltration': dns_exfiltration,
        'api_exfiltration': api_exfiltration,
        'attack_chain': attack_chain,
    }
    
    metric = attack_metrics.get(attack_type)
    if metric:
        # Build label dict
        label_dict = {'severity': severity}
        label_dict.update(labels)
        
        # Increment counter
        metric.labels(**label_dict).inc()
        
        # Update last attack info
        last_attack_info.info({
            'type': attack_type,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        })

def update_vulnerability_counts(critical: int, high: int):
    """Update vulnerability count gauges"""
    critical_vulnerabilities.set(critical)
    high_vulnerabilities.set(high)

def update_exfiltrated_data(bytes_count: int):
    """Update exfiltrated data gauge"""
    data_exfiltrated_bytes.set(bytes_count)

if __name__ == '__main__':
    # Start Prometheus exporter server
    start_http_server(EXPORTER_PORT)
    print(f"Attack Metrics Exporter started on port {EXPORTER_PORT}")
    
    # Keep the server running
    while True:
        time.sleep(60)
