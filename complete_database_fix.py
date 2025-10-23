"""
COMPLETE DATABASE FIX SCRIPT
Ensures all tables, columns, and relationships are properly set up
"""

import os
import sys
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
from sqlalchemy import inspect, text
from flask import Flask

def create_app():
    """Create Flask app with database configuration"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE')
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL')
    if database_url and 'postgresql' in database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"✓ Using PostgreSQL database")
    else:
        db_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
        print(f"✓ Using SQLite database at: {db_path}")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    return app

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def add_missing_columns():
    """Add any missing columns to existing tables"""
    migrations = []
    
    # Check Link model for required columns
    if check_table_exists('links'):
        # Ensure clicks is named total_clicks
        if not check_column_exists('links', 'total_clicks') and check_column_exists('links', 'clicks'):
            migrations.append("ALTER TABLE links RENAME COLUMN clicks TO total_clicks")
            print("⚠ Need to rename 'clicks' to 'total_clicks' in links table")
        
        # Ensure target_url exists
        if not check_column_exists('links', 'target_url'):
            migrations.append("ALTER TABLE links ADD COLUMN target_url VARCHAR(500)")
            print("⚠ Need to add 'target_url' column to links table")
    
    # Check TrackingEvent model for quantum fields
    if check_table_exists('tracking_events'):
        quantum_fields = [
            ('quantum_enabled', 'BOOLEAN DEFAULT FALSE'),
            ('quantum_click_id', 'VARCHAR(255)'),
            ('quantum_stage', 'VARCHAR(50)'),
            ('quantum_processing_time', 'FLOAT'),
            ('quantum_security_violation', 'VARCHAR(100)'),
            ('quantum_verified', 'BOOLEAN DEFAULT FALSE'),
            ('quantum_final_url', 'TEXT'),
            ('quantum_error', 'TEXT'),
            ('quantum_security_score', 'INTEGER'),
            ('is_verified_human', 'BOOLEAN DEFAULT FALSE')
        ]
        
        for field_name, field_type in quantum_fields:
            if not check_column_exists('tracking_events', field_name):
                migrations.append(f"ALTER TABLE tracking_events ADD COLUMN {field_name} {field_type}")
                print(f"⚠ Need to add '{field_name}' column to tracking_events table")
    
    return migrations

def run_migrations(migrations):
    """Execute SQL migrations"""
    if not migrations:
        print("✓ No migrations needed - all columns exist")
        return True
    
    print(f"\n{'='*60}")
    print(f"RUNNING {len(migrations)} DATABASE MIGRATIONS")
    print(f"{'='*60}\n")
    
    try:
        for migration in migrations:
            print(f"Executing: {migration}")
            db.session.execute(text(migration))
        
        db.session.commit()
        print("\n✓ All migrations completed successfully!")
        return True
    
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        db.session.rollback()
        return False

def verify_schema():
    """Verify all tables and essential columns exist"""
    print(f"\n{'='*60}")
    print("VERIFYING DATABASE SCHEMA")
    print(f"{'='*60}\n")
    
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    required_tables = {
        'users': ['id', 'username', 'email', 'password_hash', 'role'],
        'links': ['id', 'user_id', 'target_url', 'short_code', 'total_clicks'],
        'tracking_events': ['id', 'link_id', 'timestamp', 'ip_address', 'country', 'city'],
        'campaigns': ['id', 'user_id', 'name', 'status'],
        'security_settings': ['id', 'user_id', 'bot_protection'],
        'notifications': ['id', 'user_id', 'title', 'message'],
    }
    
    all_good = True
    
    for table_name, required_columns in required_tables.items():
        if table_name in tables:
            print(f"✓ Table '{table_name}' exists")
            columns = [col['name'] for col in inspector.get_columns(table_name)]
            
            for col in required_columns:
                if col in columns:
                    print(f"  ✓ Column '{col}' exists")
                else:
                    print(f"  ✗ Column '{col}' MISSING")
                    all_good = False
        else:
            print(f"✗ Table '{table_name}' MISSING")
            all_good = False
    
    return all_good

def main():
    """Main execution function"""
    print(f"\n{'='*60}")
    print("COMPLETE DATABASE FIX SCRIPT")
    print(f"{'='*60}\n")
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating all tables from models...")
        db.create_all()
        print("✓ Tables created/verified\n")
        
        # Check for missing columns
        migrations = add_missing_columns()
        
        # Run migrations if needed
        if migrations:
            if not run_migrations(migrations):
                print("\n✗ FAILED - Database migration errors occurred")
                return False
        
        # Verify final schema
        if verify_schema():
            print(f"\n{'='*60}")
            print("✓ DATABASE SCHEMA VERIFICATION PASSED")
            print(f"{'='*60}\n")
            return True
        else:
            print(f"\n{'='*60}")
            print("✗ DATABASE SCHEMA VERIFICATION FAILED")
            print(f"{'='*60}\n")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
