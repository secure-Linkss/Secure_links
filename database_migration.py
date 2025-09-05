#!/usr/bin/env python3
"""
Database Migration Script for Secure Links Project
This script ensures all required database columns exist for the User model.
"""

import os
import psycopg2
from urllib.parse import urlparse
import sys

def migrate_database(database_url):
    """
    Migrate the database to ensure all required columns exist.
    """
    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        
        # Connect to the database
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password,
            sslmode='require'
        )
        
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # List of all required columns with their types
        required_columns = [
            ("role", "VARCHAR(20) DEFAULT 'member'"),
            ("settings", "TEXT"),
            ("last_login", "TIMESTAMP"),
            ("last_ip", "VARCHAR(45)"),
            ("login_count", "INTEGER DEFAULT 0"),
            ("failed_login_attempts", "INTEGER DEFAULT 0"),
            ("account_locked_until", "TIMESTAMP"),
            ("is_active", "BOOLEAN DEFAULT TRUE"),
            ("is_verified", "BOOLEAN DEFAULT FALSE"),
            ("plan_type", "VARCHAR(20) DEFAULT 'free'"),
            ("subscription_expiry", "TIMESTAMP"),
            ("daily_link_limit", "INTEGER DEFAULT 10"),
            ("links_used_today", "INTEGER DEFAULT 0"),
            ("last_reset_date", "DATE DEFAULT CURRENT_DATE"),
            ("telegram_bot_token", "VARCHAR(255)"),
            ("telegram_chat_id", "VARCHAR(100)"),
            ("telegram_enabled", "BOOLEAN DEFAULT FALSE")
        ]
        
        # Check and add missing columns
        for col_name, col_type in required_columns:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name=%s;
            """, (col_name,))
            
            if not cursor.fetchone():
                print(f"Adding missing '{col_name}' column...")
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
                conn.commit()
                print(f"Column '{col_name}' added successfully!")
            else:
                print(f"Column '{col_name}' already exists.")
        
        cursor.close()
        conn.close()
        print("Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        return False

if __name__ == "__main__":
    # Get database URL from environment or command line
    database_url = os.environ.get('DATABASE_URL')
    
    if len(sys.argv) > 1:
        database_url = sys.argv[1]
    
    if not database_url:
        print("Error: DATABASE_URL not provided")
        print("Usage: python3 database_migration.py [DATABASE_URL]")
        print("Or set DATABASE_URL environment variable")
        sys.exit(1)
    
    success = migrate_database(database_url)
    sys.exit(0 if success else 1)

