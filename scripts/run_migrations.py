#!/usr/bin/env python3
"""
Database Migration Runner
Executes SQL migrations in order and tracks migration history
"""

import os
import sys
import time
from pathlib import Path
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'ecommerce_db'),
    'user': os.getenv('POSTGRES_USER', 'dashuser'),
    'password': os.getenv('POSTGRES_PASSWORD', 'dashpass'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

MIGRATIONS_DIR = Path(__file__).parent / 'migrations'


def get_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"❌ Error connecting to database: {e}")
        sys.exit(1)


def ensure_migrations_table(conn):
    """Ensure the schema_migrations table exists"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id SERIAL PRIMARY KEY,
            version VARCHAR(20) NOT NULL UNIQUE,
            description TEXT,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            execution_time_ms INTEGER
        );
    """)
    conn.commit()
    cursor.close()
    print("✅ Migrations tracking table ready")


def get_applied_migrations(conn):
    """Get list of already applied migrations"""
    cursor = conn.cursor()
    cursor.execute("SELECT version FROM schema_migrations ORDER BY version;")
    applied = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return applied


def get_pending_migrations(applied_migrations):
    """Get list of migration files that haven't been applied"""
    if not MIGRATIONS_DIR.exists():
        print(f"❌ Migrations directory not found: {MIGRATIONS_DIR}")
        return []
    
    all_migrations = sorted([
        f for f in MIGRATIONS_DIR.glob('*.sql')
        if f.name[0].isdigit()
    ])
    
    pending = []
    for migration_file in all_migrations:
        version = migration_file.stem.split('_')[0]
        if version not in applied_migrations:
            pending.append((version, migration_file))
    
    return pending


def execute_migration(conn, version, migration_file):
    """Execute a single migration file"""
    print(f"\n📝 Applying migration {version}: {migration_file.name}")
    
    try:
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        start_time = time.time()
        cursor = conn.cursor()
        
        # Execute the migration
        cursor.execute(sql_content)
        
        execution_time = int((time.time() - start_time) * 1000)
        
        # Record the migration (if not already recorded by the migration itself)
        cursor.execute("""
            INSERT INTO schema_migrations (version, description, execution_time_ms)
            VALUES (%s, %s, %s)
            ON CONFLICT (version) 
            DO UPDATE SET execution_time_ms = EXCLUDED.execution_time_ms;
        """, (version, migration_file.name, execution_time))
        
        conn.commit()
        cursor.close()
        
        print(f"✅ Migration {version} applied successfully ({execution_time}ms)")
        return True
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error applying migration {version}: {e}")
        return False
    except Exception as e:
        conn.rollback()
        print(f"❌ Unexpected error: {e}")
        return False


def show_migration_status(conn):
    """Display current migration status"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT version, description, applied_at, execution_time_ms
        FROM schema_migrations
        ORDER BY version;
    """)
    
    migrations = cursor.fetchall()
    cursor.close()
    
    if not migrations:
        print("\n📊 No migrations applied yet")
        return
    
    print("\n📊 Applied Migrations:")
    print("-" * 80)
    for version, description, applied_at, exec_time in migrations:
        print(f"  {version} | {description or 'N/A'}")
        print(f"         Applied: {applied_at} | Time: {exec_time or 0}ms")
    print("-" * 80)


def run_migrations(dry_run=False):
    """Main function to run all pending migrations"""
    print("=" * 80)
    print("🚀 Database Migration Runner")
    print("=" * 80)
    
    # Connect to database
    print(f"\n🔌 Connecting to database: {DB_CONFIG['dbname']}@{DB_CONFIG['host']}")
    conn = get_connection()
    
    # Ensure migrations table exists
    ensure_migrations_table(conn)
    
    # Get migration status
    applied_migrations = get_applied_migrations(conn)
    print(f"✅ Found {len(applied_migrations)} applied migration(s)")
    
    pending_migrations = get_pending_migrations(applied_migrations)
    print(f"📋 Found {len(pending_migrations)} pending migration(s)")
    
    if not pending_migrations:
        print("\n✨ Database is up to date!")
        show_migration_status(conn)
        conn.close()
        return
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made")
        print("\nPending migrations:")
        for version, migration_file in pending_migrations:
            print(f"  - {version}: {migration_file.name}")
        conn.close()
        return
    
    # Apply pending migrations
    print(f"\n🔄 Applying {len(pending_migrations)} migration(s)...")
    
    success_count = 0
    for version, migration_file in pending_migrations:
        if execute_migration(conn, version, migration_file):
            success_count += 1
        else:
            print(f"\n❌ Migration failed. Stopping here.")
            break
    
    # Show final status
    print(f"\n✅ Successfully applied {success_count}/{len(pending_migrations)} migration(s)")
    show_migration_status(conn)
    
    conn.close()
    print("\n" + "=" * 80)


def rollback_migration(version):
    """Rollback a specific migration (placeholder for future implementation)"""
    print(f"⚠️  Rollback functionality not yet implemented for version {version}")
    print("Please manually revert changes if needed")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database migration runner')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show pending migrations without applying them')
    parser.add_argument('--status', action='store_true',
                       help='Show current migration status')
    parser.add_argument('--rollback', type=str, metavar='VERSION',
                       help='Rollback a specific migration version')
    
    args = parser.parse_args()
    
    if args.status:
        conn = get_connection()
        ensure_migrations_table(conn)
        show_migration_status(conn)
        conn.close()
    elif args.rollback:
        rollback_migration(args.rollback)
    else:
        run_migrations(dry_run=args.dry_run)
