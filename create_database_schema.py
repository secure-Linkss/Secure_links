"""
Database Schema Creation and Validation Script
Ensures all tables are created and properly configured
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from src.database import db
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
# Import the DB variants
try:
    from src.models.security_threat_db import SecurityThreat as SecurityThreatDB
except ImportError:
    SecurityThreatDB = None

try:
    from src.models.support_ticket_db import SupportTicket as SupportTicketDB
except ImportError:
    SupportTicketDB = None

try:
    from src.models.subscription_verification_db import SubscriptionVerification as SubscriptionVerificationDB
except ImportError:
    SubscriptionVerificationDB = None

from flask import Flask

def create_app():
    """Create Flask app for database operations"""
    app = Flask(__name__)
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL')
    if database_url and 'postgresql' in database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"✓ Using PostgreSQL database")
    else:
        # Development - SQLite
        os.makedirs('src/database', exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///src/database/app.db'
        print(f"✓ Using SQLite database (development mode)")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    db.init_app(app)
    return app

def validate_models():
    """Validate all models are properly defined"""
    models = [
        ('User', User),
        ('Link', Link),
        ('TrackingEvent', TrackingEvent),
        ('Campaign', Campaign),
        ('AuditLog', AuditLog),
        ('SecuritySettings', SecuritySettings),
        ('BlockedIP', BlockedIP),
        ('BlockedCountry', BlockedCountry),
        ('SupportTicket', SupportTicket),
        ('SubscriptionVerification', SubscriptionVerification),
        ('Notification', Notification),
        ('Domain', Domain),
        ('SecurityThreat', SecurityThreat),
    ]
    
    print("\n=== Model Validation ===")
    for name, model in models:
        print(f"✓ {name} model loaded")
    
    if SecurityThreatDB:
        print(f"✓ SecurityThreatDB model loaded")
    if SupportTicketDB:
        print(f"✓ SupportTicketDB model loaded")
    if SubscriptionVerificationDB:
        print(f"✓ SubscriptionVerificationDB model loaded")
    
    return True

def create_tables(app):
    """Create all database tables"""
    with app.app_context():
        print("\n=== Creating Database Tables ===")
        
        try:
            # Create all tables
            db.create_all()
            print("✓ All tables created successfully")
            
            # Get table names
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n=== Database Tables ({len(tables)}) ===")
            for table in sorted(tables):
                columns = inspector.get_columns(table)
                print(f"\n✓ Table: {table}")
                print(f"  Columns ({len(columns)}):")
                for col in columns:
                    col_type = str(col['type'])
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    default = f", DEFAULT: {col['default']}" if col.get('default') else ""
                    print(f"    - {col['name']}: {col_type} {nullable}{default}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            import traceback
            traceback.print_exc()
            return False

def create_default_data(app):
    """Create default admin users and essential data"""
    with app.app_context():
        print("\n=== Creating Default Data ===")
        
        try:
            # Create default main admin
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
                print("✓ Created main admin user: Brain")
            else:
                print("✓ Main admin 'Brain' already exists")
            
            # Create default admin
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
                print("✓ Created admin user: 7thbrain")
            else:
                print("✓ Admin '7thbrain' already exists")
            
            db.session.commit()
            print("✓ Default data created successfully")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error creating default data: {e}")
            import traceback
            traceback.print_exc()
            return False

def verify_schema(app):
    """Verify the database schema is correct"""
    with app.app_context():
        print("\n=== Schema Verification ===")
        
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = [
                'users', 'links', 'tracking_events', 'campaigns',
                'audit_logs', 'security_settings', 'blocked_ips', 'blocked_countries',
                'support_tickets', 'subscription_verifications', 'notifications',
                'domains', 'security_threats'
            ]
            
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                print(f"✗ Missing tables: {', '.join(missing_tables)}")
                return False
            else:
                print(f"✓ All {len(required_tables)} required tables exist")
                return True
                
        except Exception as e:
            print(f"✗ Error verifying schema: {e}")
            return False

def main():
    """Main execution function"""
    print("=" * 50)
    print("Brain Link Tracker - Database Schema Setup")
    print("=" * 50)
    
    # Validate models
    if not validate_models():
        print("\n✗ Model validation failed")
        return False
    
    # Create Flask app
    app = create_app()
    
    # Create tables
    if not create_tables(app):
        print("\n✗ Table creation failed")
        return False
    
    # Create default data
    if not create_default_data(app):
        print("\n✗ Default data creation failed")
        return False
    
    # Verify schema
    if not verify_schema(app):
        print("\n✗ Schema verification failed")
        return False
    
    print("\n" + "=" * 50)
    print("✓ Database schema setup completed successfully!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
