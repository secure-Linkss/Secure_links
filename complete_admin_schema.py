#!/usr/bin/env python3
"""
Complete Admin Panel Database Schema
Adds missing tables for full admin panel functionality
"""
import psycopg2
from urllib.parse import urlparse
import os

def complete_admin_schema():
    database_url = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require'
    parsed = urlparse(database_url)
    
    try:
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            sslmode='require'
        )
        
        with conn.cursor() as cursor:
            print("🔧 Completing Admin Panel Database Schema...\n")
            
            # 1. Create support_tickets table
            print("1. Creating support_tickets table...")
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
            print("✅ support_tickets table created\n")
            
            # 2. Create ticket_messages table
            print("2. Creating ticket_messages table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ticket_messages (
                    id SERIAL PRIMARY KEY,
                    ticket_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticket_id) REFERENCES support_tickets(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)
            conn.commit()
            print("✅ ticket_messages table created\n")
            
            # 3. Create subscription_verifications table
            print("3. Creating subscription_verifications table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subscription_verifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    plan_type VARCHAR(50) NOT NULL,
                    amount DECIMAL(10, 2),
                    currency VARCHAR(10) DEFAULT 'USD',
                    tx_hash VARCHAR(255),
                    payment_method VARCHAR(50),
                    proof_url TEXT,
                    proof_screenshot TEXT,
                    status VARCHAR(20) DEFAULT 'pending',
                    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified_at TIMESTAMP,
                    verified_by INTEGER,
                    rejection_reason TEXT,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL
                );
            """)
            conn.commit()
            print("✅ subscription_verifications table created\n")
            
            # 4. Create security_threats table
            print("4. Creating security_threats table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_threats (
                    id SERIAL PRIMARY KEY,
                    link_id INTEGER,
                    email VARCHAR(255),
                    ip_address VARCHAR(45) NOT NULL,
                    country VARCHAR(100),
                    city VARCHAR(100),
                    isp VARCHAR(255),
                    user_agent TEXT,
                    threat_type VARCHAR(50) NOT NULL,
                    threat_level VARCHAR(20) DEFAULT 'medium',
                    threat_score INTEGER DEFAULT 0,
                    flag_reason TEXT,
                    is_blocked BOOLEAN DEFAULT FALSE,
                    is_whitelisted BOOLEAN DEFAULT FALSE,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    occurrence_count INTEGER DEFAULT 1,
                    additional_data TEXT,
                    FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE SET NULL
                );
            """)
            conn.commit()
            print("✅ security_threats table created\n")
            
            # 5. Create admin_settings table for payment configuration
            print("5. Creating admin_settings table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin_settings (
                    id SERIAL PRIMARY KEY,
                    setting_key VARCHAR(100) UNIQUE NOT NULL,
                    setting_value TEXT,
                    setting_type VARCHAR(50) DEFAULT 'string',
                    description TEXT,
                    is_public BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_by INTEGER,
                    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
                );
            """)
            conn.commit()
            print("✅ admin_settings table created\n")
            
            # 6. Insert default admin settings
            print("6. Inserting default admin settings...")
            cursor.execute("""
                INSERT INTO admin_settings (setting_key, setting_value, setting_type, description, is_public)
                VALUES 
                    ('btc_wallet_address', '', 'string', 'Bitcoin wallet address for payments', TRUE),
                    ('usdt_wallet_address', '', 'string', 'USDT wallet address for payments', TRUE),
                    ('eth_wallet_address', '', 'string', 'Ethereum wallet address for payments', TRUE),
                    ('payment_instructions', 'Please send payment and provide transaction hash for verification.', 'text', 'Payment instructions for users', TRUE),
                    ('subscription_notification_days', '7,3,1', 'string', 'Days before expiry to send notifications', FALSE),
                    ('max_login_attempts', '5', 'number', 'Maximum failed login attempts before lock', FALSE),
                    ('account_lock_duration', '30', 'number', 'Account lock duration in minutes', FALSE),
                    ('enable_2fa', 'false', 'boolean', 'Enable two-factor authentication', FALSE),
                    ('enable_email_notifications', 'true', 'boolean', 'Enable email notifications', FALSE)
                ON CONFLICT (setting_key) DO NOTHING;
            """)
            conn.commit()
            print("✅ Default admin settings inserted\n")
            
            # 7. Add indexes for performance
            print("7. Adding database indexes...")
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_support_tickets_user_id ON support_tickets(user_id);
                CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);
                CREATE INDEX IF NOT EXISTS idx_ticket_messages_ticket_id ON ticket_messages(ticket_id);
                CREATE INDEX IF NOT EXISTS idx_subscription_verifications_user_id ON subscription_verifications(user_id);
                CREATE INDEX IF NOT EXISTS idx_subscription_verifications_status ON subscription_verifications(status);
                CREATE INDEX IF NOT EXISTS idx_security_threats_ip_address ON security_threats(ip_address);
                CREATE INDEX IF NOT EXISTS idx_security_threats_link_id ON security_threats(link_id);
                CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_id ON audit_logs(actor_id);
                CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
            """)
            conn.commit()
            print("✅ Indexes created\n")
            
            # 8. Verify all tables exist
            print("8. Verifying admin panel tables...")
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN (
                    'users', 'campaigns', 'links', 'tracking_events',
                    'audit_logs', 'support_tickets', 'ticket_messages',
                    'subscription_verifications', 'security_threats', 'admin_settings'
                )
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            required_tables = [
                'admin_settings', 'audit_logs', 'campaigns', 'links',
                'security_threats', 'subscription_verifications', 'support_tickets',
                'ticket_messages', 'tracking_events', 'users'
            ]
            
            existing_tables = [t[0] for t in tables]
            
            print("Required tables status:")
            for table in required_tables:
                if table in existing_tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} (MISSING)")
            
            print(f"\n✅ Admin panel schema complete! ({len(existing_tables)}/{len(required_tables)} tables)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error completing schema: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ADMIN PANEL DATABASE SCHEMA COMPLETION")
    print("=" * 60 + "\n")
    
    success = complete_admin_schema()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ SCHEMA COMPLETION SUCCESSFUL")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ SCHEMA COMPLETION FAILED")
        print("=" * 60)
