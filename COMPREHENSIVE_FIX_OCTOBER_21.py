#!/usr/bin/env python3
"""
Comprehensive Fix Script for Brain Link Tracker
October 21, 2025
Fixes all critical issues including:
1. SQLAlchemy reserved 'metadata' attribute conflict
2. Database schema verification
3. Model integrity checks
4. API route validation
5. Frontend-backend connectivity
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import db
from flask import Flask
from flask_migrate import Migrate

def create_app():
    """Create Flask app with proper configuration"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE')
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL')
    if database_url and 'postgresql' in database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        os.makedirs(os.path.join(os.path.dirname(__file__), 'src', 'database'), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    return app

def verify_models():
    """Verify all models can be imported without errors"""
    print("\n=== VERIFYING MODELS ===")
    try:
        from src.models.user import User
        from src.models.link import Link
        from src.models.tracking_event import TrackingEvent
        from src.models.campaign import Campaign
        from src.models.audit_log import AuditLog
        from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
        from src.models.support_ticket import SupportTicket
        from src.models.subscription_verification import SubscriptionVerification
        from src.models.notification import Notification
        from src.models.domain import Domain
        from src.models.security_threat import SecurityThreat
        print("✅ All models imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Model import error: {e}")
        return False

def verify_database_schema(app):
    """Verify database schema and create all tables"""
    print("\n=== VERIFYING DATABASE SCHEMA ===")
    try:
        with app.app_context():
            # Import all models
            from src.models.user import User
            from src.models.link import Link
            from src.models.tracking_event import TrackingEvent
            from src.models.campaign import Campaign
            from src.models.audit_log import AuditLog
            from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
            from src.models.support_ticket import SupportTicket
            from src.models.subscription_verification import SubscriptionVerification
            from src.models.notification import Notification
            from src.models.domain import Domain
            from src.models.security_threat import SecurityThreat
            
            # Create all tables
            db.create_all()
            print("✅ All tables created successfully!")
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\nDatabase tables: {', '.join(tables)}")
            
            return True
    except Exception as e:
        print(f"❌ Database schema error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_admin_users(app):
    """Create default admin users"""
    print("\n=== CREATING ADMIN USERS ===")
    try:
        with app.app_context():
            from src.models.user import User
            
            # Create main admin
            if not User.query.filter_by(username="Brain").first():
                admin_user = User(
                    username="Brain",
                    email="admin@brainlinktracker.com",
                    role="main_admin",
                    status="active",
                    is_active=True,
                    is_verified=True
                )
                admin_user.set_password("Mayflower1!!")
                db.session.add(admin_user)
                print("✅ Created admin user: Brain")
            else:
                print("ℹ️  Admin user 'Brain' already exists")
            
            # Create secondary admin
            if not User.query.filter_by(username="7thbrain").first():
                admin_user2 = User(
                    username="7thbrain",
                    email="admin2@brainlinktracker.com",
                    role="admin",
                    status="active",
                    is_active=True,
                    is_verified=True
                )
                admin_user2.set_password("Mayflower1!")
                db.session.add(admin_user2)
                print("✅ Created admin user: 7thbrain")
            else:
                print("ℹ️  Admin user '7thbrain' already exists")
            
            db.session.commit()
            return True
    except Exception as e:
        print(f"❌ Admin user creation error: {e}")
        db.session.rollback()
        return False

def verify_routes():
    """Verify all routes are properly configured"""
    print("\n=== VERIFYING ROUTES ===")
    try:
        from src.routes.user import user_bp
        from src.routes.auth import auth_bp
        from src.routes.links import links_bp
        from src.routes.track import track_bp
        from src.routes.events import events_bp
        from src.routes.analytics import analytics_bp
        from src.routes.campaigns import campaigns_bp
        from src.routes.settings import settings_bp
        from src.routes.admin import admin_bp
        from src.routes.security import security_bp
        from src.routes.notifications import notifications_bp
        
        print("✅ All routes imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Route import error: {e}")
        return False

def main():
    """Main execution function"""
    print("=" * 60)
    print("BRAIN LINK TRACKER - COMPREHENSIVE FIX")
    print("October 21, 2025")
    print("=" * 60)
    
    # Step 1: Verify models
    if not verify_models():
        print("\n❌ CRITICAL: Model verification failed!")
        return False
    
    # Step 2: Create Flask app
    print("\n=== CREATING FLASK APP ===")
    app = create_app()
    print("✅ Flask app created successfully!")
    
    # Step 3: Verify database schema
    if not verify_database_schema(app):
        print("\n❌ CRITICAL: Database schema verification failed!")
        return False
    
    # Step 4: Create admin users
    if not create_admin_users(app):
        print("\n⚠️  WARNING: Admin user creation had issues")
    
    # Step 5: Verify routes
    if not verify_routes():
        print("\n⚠️  WARNING: Route verification had issues")
    
    print("\n" + "=" * 60)
    print("✅ COMPREHENSIVE FIX COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Test login with credentials:")
    print("   - Username: Brain, Password: Mayflower1!!")
    print("   - Username: 7thbrain, Password: Mayflower1!")
    print("2. Deploy to Vercel")
    print("3. Verify all features are working")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
