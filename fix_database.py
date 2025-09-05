import os
import psycopg2
from urllib.parse import urlparse

# Database URL from environment
database_url = "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Parse the database URL
parsed = urlparse(database_url)

try:
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
    
    # Check if role column exists
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='users' AND column_name='role';
    """)
    
    role_exists = cursor.fetchone()
    
    if not role_exists:
        print("Adding missing 'role' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'member';")
        conn.commit()
        print("Role column added successfully!")
    else:
        print("Role column already exists.")
    
    # Check and add other missing columns if needed
    missing_columns = [
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
    
    for col_name, col_type in missing_columns:
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='{col_name}';
        """)
        
        if not cursor.fetchone():
            print(f"Adding missing '{col_name}' column...")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
            conn.commit()
            print(f"Column '{col_name}' added successfully!")
    
    cursor.close()
    conn.close()
    print("Database migration completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
