#!/usr/bin/env python3
"""
Add missing columns to existing database tables
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import psycopg2
from psycopg2 import sql

def add_missing_columns():
    """Add missing columns to the users table"""
    
    # Database connection
    database_url = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb')
    
    print("🔧 Adding missing columns to database...")
    print(f"📡 Connecting to: {database_url.split('@')[1].split('/')[0]}")
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # List of columns that should exist in users table
        users_columns = [
            ('notification_settings', 'TEXT'),
            ('preferences', 'TEXT'),
            ('user_metadata', 'TEXT')
        ]
        
        for column_name, column_type in users_columns:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name=%s;
            """, (column_name,))
            
            if not cursor.fetchone():
                print(f"➕ Adding {column_name} column to users table...")
                cursor.execute(f"""
                    ALTER TABLE users 
                    ADD COLUMN {column_name} {column_type};
                """)
                print(f"✅ Added {column_name} column")
            else:
                print(f"✅ {column_name} column already exists")
        
        # List of columns that should exist in audit_logs table
        audit_logs_columns = [
            ('details', 'TEXT'),
            ('ip_address', 'VARCHAR(45)'),
            ('user_agent', 'TEXT')
        ]
        
        for column_name, column_type in audit_logs_columns:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='audit_logs' AND column_name=%s;
            """, (column_name,))
            
            if not cursor.fetchone():
                print(f"➕ Adding {column_name} column to audit_logs table...")
                cursor.execute(f"""
                    ALTER TABLE audit_logs 
                    ADD COLUMN {column_name} {column_type};
                """)
                print(f"✅ Added {column_name} column")
            else:
                print(f"✅ {column_name} column already exists")
        
        # Commit changes
        conn.commit()
        
        print("🎉 Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return True

if __name__ == "__main__":
    print("🚀 Brain Link Tracker - Database Column Migration")
    print("=" * 50)
    
    success = add_missing_columns()
    
    if success:
        print("\n✅ SUCCESS: Database migration completed!")
        sys.exit(0)
    else:
        print("\n❌ FAILED: Database migration failed!")
        sys.exit(1)