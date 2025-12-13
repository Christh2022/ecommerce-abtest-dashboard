"""
Utility script to generate password hashes for users.json
Usage: python generate_password_hash.py
"""

from werkzeug.security import generate_password_hash
import sys


def main():
    print("=" * 60)
    print("Password Hash Generator for E-Commerce Dashboard")
    print("=" * 60)
    print()
    
    while True:
        # Get password from user
        password = input("Enter password to hash (or 'quit' to exit): ").strip()
        
        if password.lower() == 'quit':
            print("\nGoodbye!")
            break
        
        if not password:
            print("⚠️  Password cannot be empty!\n")
            continue
        
        # Generate hash
        hashed = generate_password_hash(password)
        
        print(f"\n✅ Password hash generated:")
        print(f"   {hashed}")
        print(f"\n📋 Copy this hash to users.json in the 'password' field")
        print("-" * 60)
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
