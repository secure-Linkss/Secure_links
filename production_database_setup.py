#!/usr/bin/env python3
"""
Production Database Setup Script for Brain Link Tracker
This script ensures all database tables are properly created with correct schema
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.database import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import all models to ensure they're registered
from src.models.user import User
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from src.models.campaign import Campaign
from src.models.audit_log import AuditLog
from src.models.notification import Notification
from src.models.domain import Domain
from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
from src.models.security_threat import SecurityThreat
from src.models.security_threat_db import SecurityThreat as SecurityThreatDB
from src.models.support_ticket import SupportTicket
from src.models.support_ticket_db import SupportTicket as SupportTicketDB
from src.models.subscription_verification import SubscriptionVerification
from src.models.subscription_verification_db import SubscriptionVerification as SubscriptionVerificationDB

def create_production_database():
    """Create production database with all tables"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure database
    database_url = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb')
    
    if database_url and 'postgresql' in database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"✅ Using PostgreSQL: {database_url.split('@')[1].split('/')[0]}")
    else:
        # Fallback to SQLite for development
        os.makedirs('src/database', exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///src/database/app.db'
        print("⚠️  Using SQLite fallback")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE')
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        print("🗄️  Creating all database tables...")
        
        # Create all tables (only creates missing ones)
        print("🔨 Creating missing tables...")
        db.create_all()
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"📊 Created {len(tables)} tables:")
        for table in sorted(tables):
            columns = inspector.get_columns(table)
            print(f"  ✅ {table} ({len(columns)} columns)")
        
        # Create admin users
        print("👤 Creating admin users...")
        
        # Create main admin "Brain"
        if not User.query.filter_by(username="Brain").first():
            admin_user = User(
                username="Brain", 
                email="admin@brainlinktracker.com",
                role="main_admin",
                status="active",
                is_active=True,
                is_verified=True,
                plan_type="enterprise"
            )
            admin_user.set_password("Mayflower1!!")
            db.session.add(admin_user)
            print("  ✅ Created admin user: Brain")
        
        # Create secondary admin "7thbrain"
        if not User.query.filter_by(username="7thbrain").first():
            admin_user2 = User(
                username="7thbrain", 
                email="admin2@brainlinktracker.com",
                role="admin",
                status="active",
                is_active=True,
                is_verified=True,
                plan_type="pro"
            )
            admin_user2.set_password("Mayflower1!")
            db.session.add(admin_user2)
            print("  ✅ Created admin user: 7thbrain")
        
        # Create demo user
        if not User.query.filter_by(username="demo").first():
            demo_user = User(
                username="demo", 
                email="demo@brainlinktracker.com",
                role="member",
                status="active",
                is_active=True,
                is_verified=True,
                plan_type="free"
            )
            demo_user.set_password("demo123")
            db.session.add(demo_user)
            print("  ✅ Created demo user: demo")
        
        # Create sample data for testing
        print("📝 Creating sample data...")
        
        # Sample domain
        if not Domain.query.filter_by(domain="secure-links.short.gy").first():
            domain = Domain(
                domain="secure-links.short.gy",
                is_active=True,
                is_default=True,
                ssl_enabled=True,
                created_by=1
            )
            db.session.add(domain)
            print("  ✅ Created sample domain")
        
        # Sample campaign
        admin_user = User.query.filter_by(username="Brain").first()
        if admin_user and not Campaign.query.filter_by(name="Sample Campaign").first():
            campaign = Campaign(
                name="Sample Campaign",
                description="A sample campaign for testing",
                owner_id=admin_user.id,
                status="active"
            )
            db.session.add(campaign)
            print("  ✅ Created sample campaign")
        
        # Sample security settings
        if admin_user and not SecuritySettings.query.filter_by(user_id=admin_user.id).first():
            security_settings = SecuritySettings(
                user_id=admin_user.id,
                enable_2fa=False,
                login_notifications=True,
                suspicious_activity_alerts=True,
                password_expiry_days=90
            )
            db.session.add(security_settings)
            print("  ✅ Created sample security settings")
        
        # Commit all changes
        db.session.commit()
        
        # Final verification
        print("\n🔍 Final Database Verification:")
        
        # Check user count
        user_count = User.query.count()
        print(f"  👥 Users: {user_count}")
        
        # Check admin users
        admins = User.query.filter(User.role.in_(['admin', 'main_admin'])).all()
        print(f"  🔐 Admin users: {len(admins)}")
        for admin in admins:
            print(f"    - {admin.username} ({admin.role}) - Status: {admin.status}")
        
        # Check other tables
        link_count = Link.query.count()
        campaign_count = Campaign.query.count()
        domain_count = Domain.query.count()
        
        print(f"  🔗 Links: {link_count}")
        print(f"  📁 Campaigns: {campaign_count}")
        print(f"  🌐 Domains: {domain_count}")
        
        print("\n🎉 Database setup completed successfully!")
        print("🚀 Application is ready for production deployment!")
        
        return True

if __name__ == "__main__":
    print("🚀 Brain Link Tracker - Production Database Setup")
    print("=" * 50)
    
    try:
        success = create_production_database()
        if success:
            print("\n✅ SUCCESS: Database is ready!")
            sys.exit(0)
        else:
            print("\n❌ FAILED: Database setup failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)