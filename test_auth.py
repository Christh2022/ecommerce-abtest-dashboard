#!/usr/bin/env python3
"""Test authentication with users.json"""

from werkzeug.security import check_password_hash
import json

# Load users
with open('dashboard/users.json', 'r') as f:
    users = json.load(f)

# Test admin password
admin_hash = users['admin']['password']
print(f"Testing admin password...")
print(f"Hash: {admin_hash[:80]}...")
result = check_password_hash(admin_hash, 'admin123')
print(f"✅ Password 'admin123' is {'VALID' if result else 'INVALID'}")
print()

# Test user password (if needed)
print("Note: To test login, go to http://127.0.0.1:8050/login")
print("Username: admin")
print("Password: admin123")
