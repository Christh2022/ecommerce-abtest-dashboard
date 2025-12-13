#!/usr/bin/env python3
"""Import Security Logs Dashboard to Grafana"""
import json
import requests

# Read dashboard
with open('grafana/dashboards/security-logs.json', 'r', encoding='utf-8') as f:
    dashboard_json = f.read()
    # Clean any potential control characters
    dashboard_json = ''.join(char for char in dashboard_json if ord(char) >= 32 or char in '\n\r\t')
    dashboard = json.loads(dashboard_json)

# Prepare payload
payload = {
    'dashboard': dashboard,
    'overwrite': True,
    'message': 'Imported Security & Application Logs Dashboard'
}

# Import to Grafana
response = requests.post(
    'http://localhost:3000/api/dashboards/db',
    json=payload,
    auth=('admin', 'admin123'),
    headers={'Content-Type': 'application/json'}
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"✅ Dashboard imported successfully!")
    print(f"   URL: http://localhost:3000{result.get('url', '/d/security-logs')}")
    print(f"   UID: {result.get('uid', 'security-logs')}")
else:
    print(f"❌ Error: {response.text}")
