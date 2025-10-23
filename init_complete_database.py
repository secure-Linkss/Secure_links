#!/usr/bin/env python3
"""
Complete Database Initialization Script
Creates all necessary tables for the Brain Link Tracker application
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'

from src.main import app, db
from src.models.user import User
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from src.models.campaign import Campaign
from src.models.audit_log import AuditLog
from src.models.domain import Domain
from src.models.notification import Notification
from src.models.security_threat_db import SecurityThreat, IPBlocklist
from src.models.support_ticket_db import SupportTicket, SupportTicketComment
from src.models.subscription_verification_db import SubscriptionVerification, SubscriptionHistory
from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
from datetime import datetime, timedelta

def init_database():
    """Initialize the complete database schema"""
    print("🔄 Initializing complete database schema...")
    
    with app.app_context():
        # Drop all tables (careful in production!)
        print("⚠️  Dropping existing tables...")
        try:
            # Drop with CASCADE to handle dependencies
            with db.engine.connect() as conn:
                conn.execute(db.text("DROP SCHEMA public CASCADE;"))
                conn.execute(db.text("CREATE SCHEMA public;"))
                conn.commit()
        except Exception as e:
            print(f"⚠️  CASCADE drop failed, trying regular drop: {e}")
            db.drop_all()
        
        # Create all tables
        print("✅ Creating all tables...")
        db.create_all()
        
        # Create default admin user
        print("👤 Creating default admin user...")
        if not User.query.filter_by(username="Brain").first():
            admin_user = User(
                username="Brain",
                email="admin@brainlinktracker.com",
                role="main_admin",
                is_active=True,
                is_verified=True,
                plan_type="enterprise"
            )
            admin_user.set_password("Mayflower1!!")
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Default admin user 'Brain' created with ID: {admin_user.id}")
        
        # Create secondary admin user
        if not User.query.filter_by(username="admin").first():
            admin_user2 = User(
                username="admin",
                email="admin@example.com",
                role="admin",
                is_active=True,
                is_verified=True,
                plan_type="pro"
            )
            admin_user2.set_password("admin123")
            db.session.add(admin_user2)
            db.session.commit()
            print(f"✅ Secondary admin user 'admin' created with ID: {admin_user2.id}")
        
        # Create sample domain
        print("🌐 Creating sample domain...")
        if not Domain.query.filter_by(domain="secure-links.short.gy").first():
            sample_domain = Domain(
                domain="secure-links.short.gy",
                domain_type="shortio",
                description="Default Short.io domain for link shortening",
                is_active=True,
                is_verified=True,
                api_key="sk_DbGGlUHPN7Z9VotL",
                created_by=1  # Brain user
            )
            db.session.add(sample_domain)
            db.session.commit()
            print(f"✅ Sample domain created with ID: {sample_domain.id}")
        
        # Create sample campaign
        print("📊 Creating sample campaign...")
        if not Campaign.query.filter_by(name="Default Campaign").first():
            sample_campaign = Campaign(
                name="Default Campaign",
                description="Default campaign for new links",
                owner_id=1,  # Brain user
                status="active"
            )
            db.session.add(sample_campaign)
            db.session.commit()
            print(f"✅ Sample campaign created with ID: {sample_campaign.id}")
        
        # Create sample test link
        print("🔗 Creating sample test link...")
        if not Link.query.filter_by(short_code="test123").first():
            test_link = Link(
                user_id=1,  # Brain user
                target_url="https://example.com/test-destination",
                short_code="test123",
                campaign_name="Default Campaign",
                status="active"
            )
            db.session.add(test_link)
            db.session.commit()
            print(f"✅ Test link created with ID: {test_link.id}")
        
        # Create quantum redirect nonce table
        print("🔐 Creating quantum redirect nonce table...")
        try:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    CREATE TABLE IF NOT EXISTS quantum_nonces (
                        nonce VARCHAR(255) PRIMARY KEY,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL
                    );
                """))
                conn.execute(db.text("""
                    CREATE INDEX IF NOT EXISTS idx_quantum_nonces_expires 
                    ON quantum_nonces(expires_at);
                """))
                conn.commit()
            print("✅ Quantum nonce table created")
        except Exception as e:
            print(f"⚠️  Quantum nonce table creation: {e}")
        
        # Create sample security settings
        print("🛡️  Creating security settings...")
        if not SecuritySettings.query.first():
            security_settings = SecuritySettings(
                user_id=1,  # Brain user
                bot_protection=True,
                rate_limiting=True,
                geo_blocking=False,
                ip_blocking=True,
                vpn_detection=True,
                suspicious_activity_detection=True
            )
            db.session.add(security_settings)
            db.session.commit()
            print(f"✅ Security settings created with ID: {security_settings.id}")
        
        # Create sample member user
        print("👥 Creating sample member user...")
        if not User.query.filter_by(username="testuser").first():
            test_user = User(
                username="testuser",
                email="test@example.com",
                role="member",
                is_active=True,
                is_verified=True,
                plan_type="free"
            )
            test_user.set_password("test123")
            db.session.add(test_user)
            db.session.commit()
            print(f"✅ Test member user created with ID: {test_user.id}")
        
        # Create audit log entry
        print("📝 Creating initial audit log...")
        audit_log = AuditLog(
            actor_id=1,  # Brain user
            action="Database initialized",
            target_id=None,
            target_type="system"
        )
        db.session.add(audit_log)
        db.session.commit()
        print(f"✅ Audit log entry created with ID: {audit_log.id}")
        
        # Verify all tables exist
        print("\n🔍 Verifying database schema...")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        expected_tables = [
            'users', 'links', 'tracking_events', 'campaigns', 'audit_logs',
            'domains', 'notifications', 'security_threats', 'ip_blocklist',
            'support_tickets', 'support_ticket_comments', 'subscription_verifications',
            'subscription_history', 'security_settings', 'blocked_ips', 'blocked_countries'
        ]
        
        missing_tables = []
        for table in expected_tables:
            if table in tables:
                print(f"✅ {table}")
            else:
                missing_tables.append(table)
                print(f"❌ {table} - MISSING!")
        
        if missing_tables:
            print(f"\n⚠️  Missing tables: {', '.join(missing_tables)}")
        else:
            print("\n🎉 All expected tables are present!")
        
        print(f"\n📊 Database Statistics:")
        print(f"   Users: {User.query.count()}")
        print(f"   Links: {Link.query.count()}")
        print(f"   Campaigns: {Campaign.query.count()}")
        print(f"   Domains: {Domain.query.count()}")
        print(f"   Audit Logs: {AuditLog.query.count()}")
        
        print("\n🎯 Database initialization completed successfully!")
        print("\n🔑 Admin Credentials:")
        print("   Username: Brain")
        print("   Password: Mayflower1!!")
        print("   Email: admin@brainlinktracker.com")
        print("\n   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@example.com")
        
        return True

def verify_database_connection():
    """Verify database connection and schema"""
    print("🔗 Verifying database connection...")
    
    try:
        with app.app_context():
            # Test connection
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT 1")).fetchone()
            if result:
                print("✅ Database connection successful")
            
            # Check if main tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            if 'users' in tables:
                user_count = User.query.count()
                print(f"✅ Users table exists with {user_count} users")
            
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Brain Link Tracker - Complete Database Initialization")
    print("=" * 60)
    
    # Check if we should reset the database
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("⚠️  RESET MODE: This will delete all existing data!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Initialization cancelled")
            sys.exit(1)
    
    # Verify connection first
    if not verify_database_connection():
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Initialize database
    try:
        init_database()
        print("\n🎉 Database initialization completed successfully!")
        print("\n🌐 Application is ready to deploy!")
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)