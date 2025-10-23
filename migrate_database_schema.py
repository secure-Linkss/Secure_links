#!/usr/bin/env python3
"""
Database Migration Script for Production
Adds missing columns to existing tables
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_database():
    """Apply database migrations to add missing columns"""
    print("🔧 Starting Database Migration...")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not set")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # List of migrations to apply
        migrations = [
            # Add missing columns to users table
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar VARCHAR(500);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(500);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expiry TIMESTAMP;",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_plan VARCHAR(50);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_end_date TIMESTAMP;",
            
            # Update existing columns defaults if needed
            "ALTER TABLE users ALTER COLUMN role SET DEFAULT 'member';",
            "ALTER TABLE users ALTER COLUMN status SET DEFAULT 'pending';",
            "ALTER TABLE users ALTER COLUMN login_count SET DEFAULT 0;",
            "ALTER TABLE users ALTER COLUMN failed_login_attempts SET DEFAULT 0;",
            "ALTER TABLE users ALTER COLUMN is_active SET DEFAULT true;",
            "ALTER TABLE users ALTER COLUMN is_verified SET DEFAULT false;",
            "ALTER TABLE users ALTER COLUMN plan_type SET DEFAULT 'free';",
            "ALTER TABLE users ALTER COLUMN daily_link_limit SET DEFAULT 10;",
            "ALTER TABLE users ALTER COLUMN links_used_today SET DEFAULT 0;",
            "ALTER TABLE users ALTER COLUMN telegram_enabled SET DEFAULT false;",
        ]
        
        print("  Applying migrations...")
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"    ✅ {migration[:50]}...")
            except Exception as e:
                print(f"    ⚠️  {migration[:50]}... - {str(e)}")
        
        # Commit changes
        conn.commit()
        
        # Verify table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print(f"  ✅ Users table now has {len(columns)} columns:")
        for col_name, data_type, nullable, default in columns:
            nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
            default_str = f"DEFAULT {default}" if default else ""
            print(f"    - {col_name}: {data_type} {nullable_str} {default_str}")
        
        cursor.close()
        conn.close()
        
        print("🎉 Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    if not success:
        exit(1)