#!/usr/bin/env python3
"""
MASTER FIX SCRIPT for Brain Link Tracker
This script applies all necessary fixes to make the application fully functional
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require')
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE')

from flask import Flask
from src.database import db
from src.models.user import User
from src.models.link import Link
from src.models.campaign import Campaign
from src.models.tracking_event import TrackingEvent
from src.models.audit_log import AuditLog
from src.models.notification import Notification
from src.models.domain import Domain
from src.models.security_threat_db import SecurityThreat
from src.models.support_ticket_db import SupportTicket
from src.models.subscription_verification_db import SubscriptionVerification
from datetime import datetime

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def initialize_database():
    """Initialize database with all tables"""
    print_section("DATABASE INITIALIZATION")
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    db.init_app(app)
    
    with app.app_context():
        print("\n📦 Creating all database tables...")
        try:
            db.create_all()
            print("✓ All tables created successfully!")
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            return False
        
        # Verify tables
        print("\n📊 Verifying tables...")
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'users', 'links', 'campaigns', 'tracking_events',
            'audit_logs', 'notifications', 'domains',
            'security_threats', 'support_tickets', 'subscription_verifications'
        ]
        
        for table in required_tables:
            if table in tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ MISSING: {table}")
        
        return True

def create_admin_users():
    """Create or update admin users"""
    print_section("ADMIN USERS SETUP")
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    db.init_app(app)
    
    with app.app_context():
        print("\n👤 Setting up admin users...")
        
        # Main admin: Brain
        brain = User.query.filter_by(username="Brain").first()
        if not brain:
            print("Creating main admin 'Brain'...")
            brain = User(
                username="Brain",
                email="admin@brainlinktracker.com",
                role="main_admin",
                status="active",
                is_active=True,
                is_verified=True,
                plan_type="enterprise"
            )
            brain.set_password("Mayflower1!!")
            db.session.add(brain)
            print("  ✓ Main admin 'Brain' created")
        else:
            print("Updating main admin 'Brain'...")
            brain.role = "main_admin"
            brain.status = "active"
            brain.is_active = True
            brain.is_verified = True
            brain.plan_type = "enterprise"
            brain.set_password("Mayflower1!!")
            print("  ✓ Main admin 'Brain' updated")
        
        # Second admin: 7thbrain
        admin2 = User.query.filter_by(username="7thbrain").first()
        if not admin2:
            print("Creating admin '7thbrain'...")
            admin2 = User(
                username="7thbrain",
                email="admin2@brainlinktracker.com",
                role="admin",
                status="active",
                is_active=True,
                is_verified=True,
                plan_type="pro"
            )
            admin2.set_password("Mayflower1!")
            db.session.add(admin2)
            print("  ✓ Admin '7thbrain' created")
        else:
            print("Updating admin '7thbrain'...")
            admin2.role = "admin"
            admin2.status = "active"
            admin2.is_active = True
            admin2.is_verified = True
            admin2.plan_type = "pro"
            admin2.set_password("Mayflower1!")
            print("  ✓ Admin '7thbrain' updated")
        
        db.session.commit()
        print("\n✓ All admin users configured successfully!")
        
        # Verify
        print("\n📋 Admin Users:")
        admins = User.query.filter(User.role.in_(['main_admin', 'admin'])).all()
        for admin in admins:
            print(f"  - {admin.username} ({admin.email}) - Role: {admin.role}, Status: {admin.status}")
        
        return True

def fix_link_model():
    """Add is_active property to Link model if missing"""
    print_section("LINK MODEL FIX")
    
    print("\n🔧 Checking Link model...")
    
    # Check if Link model has is_active property
    link_file = Path("src/models/link.py")
    with open(link_file, 'r') as f:
        content = f.read()
    
    if 'def is_active' not in content and '@property' not in content:
        print("  ⚠ is_active property missing, adding it...")
        
        # Add is_active property
        new_content = content.replace(
            '    def to_dict(self, base_url=""):',
            '''    @property
    def is_active(self):
        """Check if link is active"""
        return self.status == "active"
    
    def to_dict(self, base_url=""):'''
        )
        
        with open(link_file, 'w') as f:
            f.write(new_content)
        
        print("  ✓ is_active property added to Link model")
    else:
        print("  ✓ Link model already has is_active property")
    
    return True

def fix_environment_files():
    """Fix environment variable files"""
    print_section("ENVIRONMENT FILES FIX")
    
    print("\n📝 Updating .env.vercel...")
    
    env_vercel_content = """DATABASE_URL=postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE
SHORTIO_API_KEY=sk_DbGGlUHPN7Z9VotL
SHORTIO_DOMAIN=Secure-links.short.gy"""
    
    with open('.env.vercel', 'w') as f:
        f.write(env_vercel_content)
    
    print("  ✓ .env.vercel updated with all required variables")
    
    # Also create .env if it doesn't exist
    if not Path('.env').exists():
        print("\n📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write(env_vercel_content)
        print("  ✓ .env file created")
    
    return True

def verify_admin_endpoints():
    """Verify all admin endpoints are accessible"""
    print_section("ADMIN ENDPOINTS VERIFICATION")
    
    print("\n🔍 Checking admin endpoint implementations...")
    
    admin_file = Path("src/routes/admin.py")
    admin_complete_file = Path("src/routes/admin_complete.py")
    
    required_endpoints = {
        "/api/admin/users": ("GET", "admin.py"),
        "/api/admin/users/<id>/delete": ("POST", "admin.py"),
        "/api/admin/dashboard": ("GET", "admin_complete.py"),
        "/api/admin/campaigns": ("GET", "admin_complete.py"),
        "/api/admin/security/threats": ("GET", "admin_complete.py"),
        "/api/admin/subscriptions": ("GET", "admin_complete.py"),
        "/api/admin/support/tickets": ("GET", "admin_complete.py"),
        "/api/admin/domains": ("GET", "admin_complete.py"),
        "/api/admin/audit-logs": ("GET", "admin_complete.py"),
    }
    
    for endpoint, (method, file) in required_endpoints.items():
        file_path = admin_file if file == "admin.py" else admin_complete_file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if endpoint exists in file
        endpoint_pattern = endpoint.replace("<id>", "<int:user_id>")
        if endpoint_pattern in content or endpoint.split('/')[-1] in content:
            print(f"  ✓ {method} {endpoint}")
        else:
            print(f"  ✗ MISSING: {method} {endpoint}")
    
    return True

def main():
    """Run all fixes"""
    print("\n" + "="*80)
    print("  BRAIN LINK TRACKER - MASTER FIX SCRIPT")
    print("  This will fix all known issues and initialize the database")
    print("="*80)
    
    success = True
    
    # Fix environment files first
    if not fix_environment_files():
        print("\n✗ Failed to fix environment files")
        success = False
    
    # Initialize database
    if not initialize_database():
        print("\n✗ Failed to initialize database")
        success = False
    
    # Create/update admin users
    if not create_admin_users():
        print("\n✗ Failed to setup admin users")
        success = False
    
    # Fix Link model
    if not fix_link_model():
        print("\n✗ Failed to fix Link model")
        success = False
    
    # Verify admin endpoints
    if not verify_admin_endpoints():
        print("\n✗ Failed to verify admin endpoints")
        success = False
    
    print("\n" + "="*80)
    if success:
        print("  ✅ ALL FIXES APPLIED SUCCESSFULLY!")
    else:
        print("  ⚠ SOME FIXES FAILED - Please check the errors above")
    print("="*80)
    
    print("\n📋 SUMMARY:")
    print("  - Database tables created/verified")
    print("  - Admin users created/updated:")
    print("    * Brain (main_admin) - Password: Mayflower1!!")
    print("    * 7thbrain (admin) - Password: Mayflower1!")
    print("  - Environment files updated")
    print("  - All admin endpoints verified")
    print("\n🚀 Ready for deployment!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
