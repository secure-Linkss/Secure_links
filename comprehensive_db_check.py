#!/usr/bin/env python3
"""
Comprehensive Database Check and Schema Creation
Ensures all tables exist with correct schema for Brain Link Tracker
"""
import os
import psycopg2
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash
import sys

def comprehensive_database_check():
    """Perform comprehensive database check and setup"""
    
    # Database URL from environment
    database_url = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require')
    
    # Parse the database URL
    parsed = urlparse(database_url)
    
    try:
        # Connect to the database
        print("🔌 Connecting to Neon Database...")
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            sslmode='require'
        )
        print("✓ Connected successfully!")
        
        with conn.cursor() as cursor:
            
            # ============ CHECK EXISTING TABLES ============
            print("\n📋 Checking existing tables...")
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            existing_tables = [row[0] for row in cursor.fetchall()]
            print(f"Found {len(existing_tables)} existing tables:")
            for table in existing_tables:
                print(f"  ✓ {table}")
            
            # ============ CREATE/UPDATE USERS TABLE ============
            print("\n👥 Ensuring users table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    settings TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    role VARCHAR(20) DEFAULT 'member',
                    last_login TIMESTAMP,
                    last_ip VARCHAR(45),
                    login_count INTEGER DEFAULT 0,
                    failed_login_attempts INTEGER DEFAULT 0,
                    account_locked_until TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_verified BOOLEAN DEFAULT FALSE,
                    plan_type VARCHAR(20) DEFAULT 'free',
                    subscription_expiry TIMESTAMP,
                    subscription_plan VARCHAR(50) DEFAULT '1 Day Trial',
                    subscription_start TIMESTAMP,
                    subscription_end TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'pending',
                    campaigns_count INTEGER DEFAULT 0,
                    daily_link_limit INTEGER DEFAULT 10,
                    links_used_today INTEGER DEFAULT 0,
                    last_reset_date DATE DEFAULT CURRENT_DATE,
                    telegram_bot_token VARCHAR(255),
                    telegram_chat_id VARCHAR(100),
                    telegram_enabled BOOLEAN DEFAULT FALSE
                );
            """)
            conn.commit()
            print("✓ Users table ready")
            
            # ============ CREATE CAMPAIGNS TABLE ============
            print("\n📊 Ensuring campaigns table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    owner_id INTEGER NOT NULL,
                    status VARCHAR(20) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)
            conn.commit()
            print("✓ Campaigns table ready")
            
            # ============ CREATE LINKS TABLE ============
            print("\n🔗 Ensuring links table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    campaign_id INTEGER,
                    target_url VARCHAR(500) NOT NULL,
                    short_code VARCHAR(10) UNIQUE NOT NULL,
                    campaign_name VARCHAR(255) DEFAULT 'Untitled Campaign',
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_clicks INTEGER DEFAULT 0,
                    real_visitors INTEGER DEFAULT 0,
                    blocked_attempts INTEGER DEFAULT 0,
                    unique_clicks INTEGER DEFAULT 0,
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
                    blocked_cities TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE SET NULL
                );
                CREATE INDEX IF NOT EXISTS idx_links_short_code ON links(short_code);
                CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id);
            """)
            conn.commit()
            print("✓ Links table ready")
            
            # ============ CREATE TRACKING_EVENTS TABLE ============
            print("\n📍 Ensuring tracking_events table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking_events (
                    id SERIAL PRIMARY KEY,
                    link_id INTEGER NOT NULL,
                    user_id INTEGER,
                    event_type VARCHAR(50) NOT NULL DEFAULT 'click',
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    country VARCHAR(100),
                    region VARCHAR(100),
                    city VARCHAR(100),
                    isp VARCHAR(255),
                    device_type VARCHAR(50),
                    browser VARCHAR(100),
                    os VARCHAR(100),
                    referrer TEXT,
                    email VARCHAR(255),
                    password VARCHAR(255),
                    additional_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    quantum_click_id VARCHAR(255),
                    quantum_stage VARCHAR(50),
                    quantum_processing_time FLOAT DEFAULT 0,
                    quantum_security_violation VARCHAR(100),
                    quantum_final_url TEXT,
                    quantum_verified BOOLEAN DEFAULT FALSE,
                    is_verified_human BOOLEAN DEFAULT FALSE,
                    quantum_security_score INTEGER DEFAULT 0,
                    FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                );
                CREATE INDEX IF NOT EXISTS idx_tracking_link_id ON tracking_events(link_id);
                CREATE INDEX IF NOT EXISTS idx_tracking_created_at ON tracking_events(created_at);
                CREATE INDEX IF NOT EXISTS idx_tracking_quantum_click_id ON tracking_events(quantum_click_id);
            """)
            conn.commit()
            print("✓ Tracking events table ready")
            
            # ============ CREATE QUANTUM NONCES TABLE ============
            print("\n🔐 Ensuring quantum_nonces table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quantum_nonces (
                    nonce VARCHAR(255) PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_quantum_nonces_expires ON quantum_nonces(expires_at);
            """)
            conn.commit()
            print("✓ Quantum nonces table ready")
            
            # ============ CREATE AUDIT_LOGS TABLE ============
            print("\n📝 Ensuring audit_logs table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id SERIAL PRIMARY KEY,
                    actor_id INTEGER NOT NULL,
                    actor_role VARCHAR(50),
                    action VARCHAR(255) NOT NULL,
                    target_type VARCHAR(100),
                    target_id INTEGER,
                    details TEXT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE CASCADE
                );
                CREATE INDEX IF NOT EXISTS idx_audit_actor_id ON audit_logs(actor_id);
                CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_logs(created_at);
            """)
            conn.commit()
            print("✓ Audit logs table ready")
            
            # ============ CREATE NOTIFICATIONS TABLE ============
            print("\n🔔 Ensuring notifications table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    type VARCHAR(50) DEFAULT 'info',
                    read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
            """)
            conn.commit()
            print("✓ Notifications table ready")
            
            # ============ CREATE SECURITY_SETTINGS TABLE ============
            print("\n🛡️ Ensuring security_settings table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_settings (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    setting_name VARCHAR(100) NOT NULL,
                    setting_value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE(user_id, setting_name)
                );
            """)
            conn.commit()
            print("✓ Security settings table ready")
            
            # ============ CREATE ADMIN_SETTINGS TABLE ============
            print("\n⚙️ Ensuring admin_settings table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin_settings (
                    id SERIAL PRIMARY KEY,
                    setting_key VARCHAR(100) UNIQUE NOT NULL,
                    setting_value TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✓ Admin settings table ready")
            
            # ============ CREATE SUBSCRIPTION VERIFICATION TABLE ============
            print("\n💳 Ensuring subscription_verifications table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subscription_verifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    tx_hash VARCHAR(255),
                    amount DECIMAL(20, 8),
                    currency VARCHAR(10),
                    status VARCHAR(20) DEFAULT 'pending',
                    proof_url TEXT,
                    admin_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified_at TIMESTAMP,
                    verified_by INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL
                );
            """)
            conn.commit()
            print("✓ Subscription verifications table ready")
            
            # ============ CREATE SUPPORT TICKETS TABLE ============
            print("\n🎫 Ensuring support_tickets table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS support_tickets (
                    id SERIAL PRIMARY KEY,
                    ticket_ref VARCHAR(50) UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    subject VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    priority VARCHAR(20) DEFAULT 'normal',
                    category VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP,
                    resolved_by INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (resolved_by) REFERENCES users(id) ON DELETE SET NULL
                );
            """)
            conn.commit()
            print("✓ Support tickets table ready")
            
            # ============ CREATE SECURITY THREATS TABLE ============
            print("\n⚠️ Ensuring security_threats table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_threats (
                    id SERIAL PRIMARY KEY,
                    ip_address VARCHAR(45) NOT NULL,
                    threat_type VARCHAR(100) NOT NULL,
                    severity VARCHAR(20) DEFAULT 'medium',
                    description TEXT,
                    user_agent TEXT,
                    country VARCHAR(100),
                    isp VARCHAR(255),
                    is_blocked BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_security_threats_ip ON security_threats(ip_address);
            """)
            conn.commit()
            print("✓ Security threats table ready")
            
            # ============ VERIFY ADMIN USERS ============
            print("\n👨‍💼 Verifying admin users...")
            cursor.execute("SELECT username, role, status FROM users WHERE role IN ('main_admin', 'admin', 'assistant_admin');")
            admin_users = cursor.fetchall()
            
            if admin_users:
                print(f"Found {len(admin_users)} admin users:")
                for user in admin_users:
                    print(f"  ✓ {user[0]} ({user[1]}) - Status: {user[2]}")
            else:
                print("⚠ No admin users found. Creating default admin...")
                password_hash = generate_password_hash("Mayflower1!!")
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, role, is_active, is_verified, status)
                    VALUES ('Brain', 'admin@brainlinktracker.com', %s, 'main_admin', TRUE, TRUE, 'active')
                    ON CONFLICT (username) DO UPDATE SET 
                        role = 'main_admin',
                        is_active = TRUE,
                        is_verified = TRUE,
                        status = 'active';
                """, (password_hash,))
                conn.commit()
                print("✓ Default admin user 'Brain' created/updated")
            
            # ============ CREATE TEST USER ============
            print("\n🧪 Creating test member user...")
            test_password_hash = generate_password_hash("TestUser123!")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, is_active, is_verified, status)
                VALUES ('testmember', 'testmember@example.com', %s, 'member', TRUE, TRUE, 'active')
                ON CONFLICT (username) DO UPDATE SET 
                    email = 'testmember@example.com',
                    role = 'member',
                    is_active = TRUE,
                    is_verified = TRUE,
                    status = 'active';
            """, (test_password_hash,))
            conn.commit()
            print("✓ Test user 'testmember' created (password: TestUser123!)")
            
            # ============ VERIFY FOREIGN KEY RELATIONSHIPS ============
            print("\n🔗 Verifying foreign key relationships...")
            cursor.execute("""
                SELECT
                    tc.table_name, 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                    AND tc.table_schema = 'public'
                ORDER BY tc.table_name;
            """)
            foreign_keys = cursor.fetchall()
            print(f"Found {len(foreign_keys)} foreign key relationships:")
            for fk in foreign_keys[:10]:  # Show first 10
                print(f"  ✓ {fk[0]}.{fk[1]} → {fk[2]}.{fk[3]}")
            if len(foreign_keys) > 10:
                print(f"  ... and {len(foreign_keys) - 10} more")
            
            # ============ FINAL VERIFICATION ============
            print("\n✅ Final verification...")
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            final_tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = [
                'users', 'campaigns', 'links', 'tracking_events',
                'quantum_nonces', 'audit_logs', 'notifications',
                'security_settings', 'admin_settings', 'subscription_verifications',
                'support_tickets', 'security_threats'
            ]
            
            missing_tables = [t for t in required_tables if t not in final_tables]
            
            if missing_tables:
                print(f"\n⚠ WARNING: Missing tables: {', '.join(missing_tables)}")
                return False
            else:
                print(f"\n🎉 All {len(required_tables)} required tables are present!")
                print("\n📊 Database Summary:")
                print(f"  • Total tables: {len(final_tables)}")
                print(f"  • Foreign keys: {len(foreign_keys)}")
                print(f"  • Admin users: {len(admin_users) if admin_users else 1}")
                print(f"  • Database ready for production: ✓")
                return True
        
    except Exception as e:
        print(f"\n❌ Database check failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()
            print("\n🔌 Database connection closed")

if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE DATABASE CHECK AND SETUP")
    print("Brain Link Tracker - Production Ready")
    print("=" * 60)
    
    success = comprehensive_database_check()
    
    if success:
        print("\n✅ DATABASE IS PRODUCTION READY!")
        sys.exit(0)
    else:
        print("\n❌ DATABASE SETUP INCOMPLETE")
        sys.exit(1)
