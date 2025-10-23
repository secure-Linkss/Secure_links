"""
Comprehensive Database Schema Check and Setup
Ensures all required tables exist and are properly configured for production
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Set environment variables
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require'
os.environ['SHORTIO_API_KEY'] = 'sk_DbGGlUHPN7Z9VotL'
os.environ['SHORTIO_DOMAIN'] = 'Secure-links.short.gy'

def get_db_connection():
    """Get database connection"""
    db_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(db_url)

def check_table_exists(cursor, table_name):
    """Check if a table exists in the database"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
    """, (table_name,))
    return cursor.fetchone()[0]

def get_table_columns(cursor, table_name):
    """Get all columns for a table"""
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    return cursor.fetchall()

def add_column_if_not_exists(cursor, table_name, column_name, column_def):
    """Add a column to a table if it doesn't exist"""
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s AND column_name = %s;
    """, (table_name, column_name))
    
    if not cursor.fetchone():
        print(f"  Adding column '{column_name}' to table '{table_name}'...")
        cursor.execute(sql.SQL("ALTER TABLE {} ADD COLUMN {}").format(
            sql.Identifier(table_name),
            sql.SQL(column_def)
        ))
        return True
    return False

def create_table_if_not_exists(cursor, table_name, create_statement):
    """Create a table if it doesn't exist"""
    if not check_table_exists(cursor, table_name):
        print(f"Creating table '{table_name}'...")
        cursor.execute(create_statement)
        return True
    return False

def verify_and_fix_database():
    """Main function to verify and fix database schema"""
    print("=" * 80)
    print("BRAIN LINK TRACKER - DATABASE VERIFICATION & SETUP")
    print("=" * 80)
    print()
    
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✓ Connected to database successfully")
        print()
        
        # Track changes
        tables_created = []
        columns_added = []
        tables_verified = []
        
        # =================================================================
        # 1. USERS TABLE - Core user management
        # =================================================================
        print("Checking USERS table...")
        users_created = create_table_if_not_exists(cursor, 'users', """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                settings TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                role VARCHAR(20) DEFAULT 'member',
                status VARCHAR(20) DEFAULT 'pending',
                last_login TIMESTAMP,
                last_ip VARCHAR(45),
                login_count INTEGER DEFAULT 0,
                failed_login_attempts INTEGER DEFAULT 0,
                account_locked_until TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                plan_type VARCHAR(20) DEFAULT 'free',
                subscription_expiry TIMESTAMP,
                daily_link_limit INTEGER DEFAULT 10,
                links_used_today INTEGER DEFAULT 0,
                last_reset_date DATE DEFAULT CURRENT_DATE,
                telegram_bot_token VARCHAR(255),
                telegram_chat_id VARCHAR(100),
                telegram_enabled BOOLEAN DEFAULT FALSE
            );
        """)
        
        if users_created:
            tables_created.append('users')
        else:
            # Verify and add missing columns
            required_columns = [
                ('role', "VARCHAR(20) DEFAULT 'member'"),
                ('status', "VARCHAR(20) DEFAULT 'pending'"),
                ('last_login', 'TIMESTAMP'),
                ('last_ip', 'VARCHAR(45)'),
                ('login_count', 'INTEGER DEFAULT 0'),
                ('failed_login_attempts', 'INTEGER DEFAULT 0'),
                ('account_locked_until', 'TIMESTAMP'),
                ('is_active', 'BOOLEAN DEFAULT TRUE'),
                ('is_verified', 'BOOLEAN DEFAULT FALSE'),
                ('plan_type', "VARCHAR(20) DEFAULT 'free'"),
                ('subscription_expiry', 'TIMESTAMP'),
                ('daily_link_limit', 'INTEGER DEFAULT 10'),
                ('links_used_today', 'INTEGER DEFAULT 0'),
                ('last_reset_date', 'DATE DEFAULT CURRENT_DATE'),
                ('telegram_bot_token', 'VARCHAR(255)'),
                ('telegram_chat_id', 'VARCHAR(100)'),
                ('telegram_enabled', 'BOOLEAN DEFAULT FALSE'),
            ]
            
            for col_name, col_def in required_columns:
                if add_column_if_not_exists(cursor, 'users', col_name, col_def):
                    columns_added.append(f'users.{col_name}')
            
            tables_verified.append('users')
        
        # =================================================================
        # 2. LINK TABLE - Link tracking and management
        # =================================================================
        print("Checking LINK table...")
        link_created = create_table_if_not_exists(cursor, 'link', """
            CREATE TABLE link (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                target_url VARCHAR(500) NOT NULL,
                short_code VARCHAR(10) UNIQUE NOT NULL,
                campaign_name VARCHAR(255) DEFAULT 'Untitled Campaign',
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_clicks INTEGER DEFAULT 0,
                real_visitors INTEGER DEFAULT 0,
                blocked_attempts INTEGER DEFAULT 0,
                capture_email BOOLEAN DEFAULT FALSE,
                capture_password BOOLEAN DEFAULT FALSE,
                bot_blocking_enabled BOOLEAN DEFAULT FALSE,
                geo_targeting_enabled BOOLEAN DEFAULT FALSE,
                geo_targeting_type VARCHAR(20) DEFAULT 'allow',
                rate_limiting_enabled BOOLEAN DEFAULT FALSE,
                dynamic_signature_enabled BOOLEAN DEFAULT FALSE,
                mx_verification_enabled BOOLEAN DEFAULT FALSE,
                preview_template_url VARCHAR(500),
                allowed_countries TEXT,
                blocked_countries TEXT,
                allowed_regions TEXT,
                blocked_regions TEXT,
                allowed_cities TEXT,
                blocked_cities TEXT
            );
        """)
        
        if link_created:
            tables_created.append('link')
            # Create index on short_code for fast lookups
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_link_short_code ON link(short_code);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_link_user_id ON link(user_id);")
        else:
            tables_verified.append('link')
        
        # =================================================================
        # 3. TRACKING_EVENT TABLE - Click tracking and analytics
        # =================================================================
        print("Checking TRACKING_EVENT table...")
        tracking_created = create_table_if_not_exists(cursor, 'tracking_event', """
            CREATE TABLE tracking_event (
                id SERIAL PRIMARY KEY,
                link_id INTEGER NOT NULL REFERENCES link(id) ON DELETE CASCADE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                user_agent TEXT,
                country VARCHAR(100),
                region VARCHAR(100),
                city VARCHAR(100),
                zip_code VARCHAR(20),
                isp VARCHAR(255),
                organization VARCHAR(255),
                as_number VARCHAR(50),
                timezone VARCHAR(50),
                latitude FLOAT,
                longitude FLOAT,
                device_type VARCHAR(50),
                browser VARCHAR(100),
                browser_version VARCHAR(50),
                os VARCHAR(100),
                os_version VARCHAR(50),
                captured_email VARCHAR(255),
                captured_password VARCHAR(255),
                status VARCHAR(50),
                blocked_reason VARCHAR(255),
                unique_id VARCHAR(255),
                email_opened BOOLEAN DEFAULT FALSE,
                redirected BOOLEAN DEFAULT FALSE,
                on_page BOOLEAN DEFAULT FALSE,
                is_bot BOOLEAN DEFAULT FALSE,
                referrer TEXT,
                session_duration INTEGER,
                page_views INTEGER DEFAULT 1,
                threat_score INTEGER DEFAULT 0,
                bot_type VARCHAR(100),
                quantum_enabled BOOLEAN DEFAULT FALSE,
                quantum_click_id VARCHAR(255),
                quantum_stage VARCHAR(50),
                quantum_processing_time FLOAT,
                quantum_security_violation VARCHAR(100),
                quantum_verified BOOLEAN DEFAULT FALSE,
                quantum_final_url TEXT,
                quantum_error TEXT,
                quantum_security_score INTEGER,
                is_verified_human BOOLEAN DEFAULT FALSE
            );
        """)
        
        if tracking_created:
            tables_created.append('tracking_event')
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tracking_link_id ON tracking_event(link_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tracking_timestamp ON tracking_event(timestamp);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tracking_country ON tracking_event(country);")
        else:
            tables_verified.append('tracking_event')
        
        # =================================================================
        # 4. CAMPAIGNS TABLE
        # =================================================================
        print("Checking CAMPAIGNS table...")
        campaigns_created = create_table_if_not_exists(cursor, 'campaigns', """
            CREATE TABLE campaigns (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                description TEXT,
                owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        if campaigns_created:
            tables_created.append('campaigns')
        else:
            tables_verified.append('campaigns')
        
        # =================================================================
        # 5. NOTIFICATION TABLE
        # =================================================================
        print("Checking NOTIFICATION table...")
        notification_created = create_table_if_not_exists(cursor, 'notification', """
            CREATE TABLE notification (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                type VARCHAR(50) DEFAULT 'info',
                read BOOLEAN DEFAULT FALSE,
                priority VARCHAR(50) DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        if notification_created:
            tables_created.append('notification')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_notification_user_id ON notification(user_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_notification_read ON notification(read);")
        else:
            tables_verified.append('notification')
        
        # =================================================================
        # 6. AUDIT_LOG TABLE
        # =================================================================
        print("Checking AUDIT_LOG table...")
        audit_created = create_table_if_not_exists(cursor, 'audit_log', """
            CREATE TABLE audit_log (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                action VARCHAR(255) NOT NULL,
                details TEXT,
                ip_address VARCHAR(45),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        if audit_created:
            tables_created.append('audit_log')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_log(user_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_log(created_at);")
        else:
            tables_verified.append('audit_log')
        
        # =================================================================
        # 7. SECURITY SETTINGS TABLE
        # =================================================================
        print("Checking SECURITY_SETTINGS table...")
        security_settings_created = create_table_if_not_exists(cursor, 'security_settings', """
            CREATE TABLE security_settings (
                id SERIAL PRIMARY KEY,
                user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
                two_factor_enabled BOOLEAN DEFAULT FALSE,
                ip_whitelist TEXT,
                session_timeout INTEGER DEFAULT 3600,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        if security_settings_created:
            tables_created.append('security_settings')
        else:
            tables_verified.append('security_settings')
        
        # =================================================================
        # 8. BLOCKED_IP TABLE
        # =================================================================
        print("Checking BLOCKED_IP table...")
        blocked_ip_created = create_table_if_not_exists(cursor, 'blocked_ip', """
            CREATE TABLE blocked_ip (
                id SERIAL PRIMARY KEY,
                ip_address VARCHAR(45) UNIQUE NOT NULL,
                reason TEXT,
                blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blocked_by INTEGER REFERENCES users(id) ON DELETE SET NULL
            );
        """)
        
        if blocked_ip_created:
            tables_created.append('blocked_ip')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_blocked_ip_address ON blocked_ip(ip_address);")
        else:
            tables_verified.append('blocked_ip')
        
        # =================================================================
        # 9. BLOCKED_COUNTRY TABLE
        # =================================================================
        print("Checking BLOCKED_COUNTRY table...")
        blocked_country_created = create_table_if_not_exists(cursor, 'blocked_country', """
            CREATE TABLE blocked_country (
                id SERIAL PRIMARY KEY,
                country_code VARCHAR(2) UNIQUE NOT NULL,
                country_name VARCHAR(100) NOT NULL,
                reason TEXT,
                blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blocked_by INTEGER REFERENCES users(id) ON DELETE SET NULL
            );
        """)
        
        if blocked_country_created:
            tables_created.append('blocked_country')
        else:
            tables_verified.append('blocked_country')
        
        # =================================================================
        # 10. SUPPORT_TICKET TABLE
        # =================================================================
        print("Checking SUPPORT_TICKET table...")
        support_ticket_created = create_table_if_not_exists(cursor, 'support_ticket', """
            CREATE TABLE support_ticket (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                subject VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'open',
                priority VARCHAR(50) DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                resolved_by INTEGER REFERENCES users(id) ON DELETE SET NULL
            );
        """)
        
        if support_ticket_created:
            tables_created.append('support_ticket')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_support_ticket_user_id ON support_ticket(user_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_support_ticket_status ON support_ticket(status);")
        else:
            tables_verified.append('support_ticket')
        
        # =================================================================
        # 11. SUBSCRIPTION_VERIFICATION TABLE
        # =================================================================
        print("Checking SUBSCRIPTION_VERIFICATION table...")
        sub_verification_created = create_table_if_not_exists(cursor, 'subscription_verification', """
            CREATE TABLE subscription_verification (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                verification_code VARCHAR(100) UNIQUE NOT NULL,
                plan_type VARCHAR(20) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified_at TIMESTAMP,
                expires_at TIMESTAMP
            );
        """)
        
        if sub_verification_created:
            tables_created.append('subscription_verification')
        else:
            tables_verified.append('subscription_verification')
        
        # =================================================================
        # SUMMARY REPORT
        # =================================================================
        print()
        print("=" * 80)
        print("DATABASE VERIFICATION COMPLETE")
        print("=" * 80)
        print()
        
        if tables_created:
            print(f"✓ {len(tables_created)} NEW TABLES CREATED:")
            for table in tables_created:
                print(f"  - {table}")
            print()
        
        if columns_added:
            print(f"✓ {len(columns_added)} NEW COLUMNS ADDED:")
            for column in columns_added:
                print(f"  - {column}")
            print()
        
        if tables_verified:
            print(f"✓ {len(tables_verified)} TABLES VERIFIED (Already Exist):")
            for table in tables_verified:
                print(f"  - {table}")
            print()
        
        # Get table counts
        print("=" * 80)
        print("DATABASE STATISTICS")
        print("=" * 80)
        print()
        
        tables_to_check = ['users', 'link', 'tracking_event', 'campaigns', 'notification', 
                          'audit_log', 'security_settings', 'blocked_ip', 'blocked_country',
                          'support_ticket', 'subscription_verification']
        
        for table in tables_to_check:
            if check_table_exists(cursor, table):
                cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table)))
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} rows")
        
        print()
        print("=" * 80)
        print("✓ DATABASE IS READY FOR PRODUCTION")
        print("=" * 80)
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify_and_fix_database()
    sys.exit(0 if success else 1)
