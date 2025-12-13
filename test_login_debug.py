#!/usr/bin/env python3
"""Debug authentication"""

import json
from werkzeug.security import check_password_hash

# Load users.json
with open('dashboard/users.json', 'r') as f:
    users = json.load(f)

print("=" * 60)
print("TESTING AUTHENTICATION")
print("=" * 60)

# Test admin user
admin = users.get('admin')
if admin:
    print(f"\n✓ Admin user found")
    print(f"  Username: {admin['username']}")
    print(f"  Password hash (first 80 chars): {admin['password'][:80]}...")
    
    # Test password
    test_password = 'admin123'
    result = check_password_hash(admin['password'], test_password)
    print(f"\n  Testing password '{test_password}': {'✓ VALID' if result else '✗ INVALID'}")
    
    # Try other common passwords
    for pwd in ['admin', 'Admin123', 'ADMIN123']:
        result = check_password_hash(admin['password'], pwd)
        if result:
            print(f"  Testing password '{pwd}': ✓ VALID")
else:
    print("\n✗ Admin user NOT found in users.json")

print("\n" + "=" * 60)
