#!/usr/bin/env python3
"""
Apply All Comprehensive Fixes
==============================
This script applies all database migrations and verifies the setup
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from src.database import db
from src.main import app

def apply_database_migrations():
    """Apply comprehensive database migrations"""
    print("=" * 60)
    print("APPLYING DATABASE MIGRATIONS")
    print("=" * 60)
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return False
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Read migration SQL
        with open('database_migration_comprehensive.sql', 'r') as f:
            migration_sql = f.read()
        
        # Split by semicolons and execute each statement
        statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        with engine.connect() as conn:
            for stmt in statements:
                if stmt:
                    print(f"Executing: {stmt[:100]}...")
                    conn.execute(text(stmt))
                    conn.commit()
        
        print("✓ Database migrations applied successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error applying migrations: {e}")
        return False

def verify_tables():
    """Verify all required tables exist"""
    print("\n" + "=" * 60)
    print("VERIFYING DATABASE SCHEMA")
    print("=" * 60)
    
    required_tables = [
        'users', 'links', 'tracking_events', 'campaigns',
        'notifications', 'audit_logs', 'domains'
    ]
    
    with app.app_context():
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"Found {len(existing_tables)} tables")
            
            for table in required_tables:
                if table in existing_tables:
                    print(f"✓ Table '{table}' exists")
                else:
                    print(f"✗ Table '{table}' missing")
            
            return True
            
        except Exception as e:
            print(f"✗ Error verifying tables: {e}")
            return False

def verify_user_columns():
    """Verify user table has all required columns"""
    print("\n" + "=" * 60)
    print("VERIFYING USER TABLE COLUMNS")
    print("=" * 60)
    
    required_columns = [
        'avatar', 'profile_picture', 'reset_token', 'reset_token_expiry',
        'subscription_plan', 'subscription_status', 'subscription_end_date'
    ]
    
    with app.app_context():
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            for col in required_columns:
                if col in columns:
                    print(f"✓ Column 'users.{col}' exists")
                else:
                    print(f"✗ Column 'users.{col}' missing")
            
            return True
            
        except Exception as e:
            print(f"✗ Error verifying columns: {e}")
            return False

def main():
    """Main execution function"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "COMPREHENSIVE FIX APPLICATION" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # Apply migrations
    if not apply_database_migrations():
        print("\n⚠ Warning: Database migrations failed")
    
    # Verify setup
    verify_tables()
    verify_user_columns()
    
    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Test the frontend and backend locally")
    print("2. Verify all endpoints are working")
    print("3. Push to GitHub master branch")
    print("4. Deploy to Vercel with environment variables")

if __name__ == '__main__':
    main()
