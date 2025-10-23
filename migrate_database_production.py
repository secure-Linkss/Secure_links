#!/usr/bin/env python3
"""
Production Database Migration Script
Properly handles database schema updates for PostgreSQL (Neon)
"""

import os
import sys
import psycopg2
from psycopg2 import sql

def get_db_connection():
    """Get PostgreSQL database connection"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        return None
    
    try:
        # Parse the database URL
        conn = psycopg2.connect(database_url)
        print("✅ Connected to database successfully!")
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

def column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = %s AND column_name = %s
        );
    """, (table_name, column_name))
    return cursor.fetchone()[0]

def add_column_if_not_exists(cursor, table_name, column_name, column_definition):
    """Add a column if it doesn't exist"""
    if not column_exists(cursor, table_name, column_name):
        try:
            cursor.execute(sql.SQL("""
                ALTER TABLE {} ADD COLUMN {} {}
            """).format(
                sql.Identifier(table_name),
                sql.Identifier(column_name),
                sql.SQL(column_definition)
            ))
            print(f"  ✅ Added column: {table_name}.{column_name}")
            return True
        except Exception as e:
            print(f"  ⚠️  Column {table_name}.{column_name} may already exist: {e}")
            return False
    else:
        print(f"  ℹ️  Column {table_name}.{column_name} already exists")
        return True

def migrate_database():
    """Run database migration"""
    print("\n" + "=" * 60)
    print("BRAIN LINK TRACKER - DATABASE MIGRATION")
    print("=" * 60 + "\n")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        print("=== Migrating users table ===")
        
        # Add missing columns to users table
        add_column_if_not_exists(cursor, 'users', 'settings', 'TEXT')
        add_column_if_not_exists(cursor, 'users', 'notification_settings', 'TEXT')
        add_column_if_not_exists(cursor, 'users', 'preferences', 'TEXT')
        add_column_if_not_exists(cursor, 'users', 'user_metadata', 'TEXT')
        add_column_if_not_exists(cursor, 'users', 'role', "VARCHAR(20) DEFAULT 'member'")
        add_column_if_not_exists(cursor, 'users', 'status', "VARCHAR(20) DEFAULT 'pending'")
        add_column_if_not_exists(cursor, 'users', 'last_login', 'TIMESTAMP')
        add_column_if_not_exists(cursor, 'users', 'last_ip', 'VARCHAR(45)')
        add_column_if_not_exists(cursor, 'users', 'login_count', 'INTEGER DEFAULT 0')
        add_column_if_not_exists(cursor, 'users', 'failed_login_attempts', 'INTEGER DEFAULT 0')
        add_column_if_not_exists(cursor, 'users', 'account_locked_until', 'TIMESTAMP')
        add_column_if_not_exists(cursor, 'users', 'is_active', 'BOOLEAN DEFAULT TRUE')
        add_column_if_not_exists(cursor, 'users', 'is_verified', 'BOOLEAN DEFAULT FALSE')
        add_column_if_not_exists(cursor, 'users', 'plan_type', "VARCHAR(20) DEFAULT 'free'")
        add_column_if_not_exists(cursor, 'users', 'subscription_expiry', 'TIMESTAMP')
        add_column_if_not_exists(cursor, 'users', 'daily_link_limit', 'INTEGER DEFAULT 10')
        add_column_if_not_exists(cursor, 'users', 'links_used_today', 'INTEGER DEFAULT 0')
        add_column_if_not_exists(cursor, 'users', 'last_reset_date', 'DATE DEFAULT CURRENT_DATE')
        add_column_if_not_exists(cursor, 'users', 'telegram_bot_token', 'VARCHAR(255)')
        add_column_if_not_exists(cursor, 'users', 'telegram_chat_id', 'VARCHAR(100)')
        add_column_if_not_exists(cursor, 'users', 'telegram_enabled', 'BOOLEAN DEFAULT FALSE')
        
        # Update admin users to active status
        print("\n=== Updating admin users ===")
        cursor.execute("""
            UPDATE users 
            SET status = 'active', is_active = TRUE, is_verified = TRUE 
            WHERE username IN ('Brain', '7thbrain')
        """)
        print("✅ Updated admin users to active status")
        
        # Commit changes
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        conn.rollback()
        conn.close()
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
