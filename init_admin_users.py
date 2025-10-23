#!/usr/bin/env python3
"""
Initialize admin users in the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import db
from src.models.user import User
from datetime import datetime, date
from werkzeug.security import generate_password_hash

def init_admin_users():
    """Initialize the admin users in the database"""
    
    # Check if main admin already exists
    main_admin = User.query.filter_by(username='Brain').first()
    if not main_admin:
        # Create main admin user
        main_admin = User(
            username='Brain',
            email='admin@brainlinktracker.com',
            password_hash=generate_password_hash('Mayflower1!!'),
            role='main_admin',
            status='active',
            is_active=True,
            is_verified=True,
            plan_type='enterprise',
            daily_link_limit=10000,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow(),
            login_count=1
        )
        db.session.add(main_admin)
        print("✅ Created main admin user: Brain")
    else:
        print("✅ Main admin user already exists: Brain")
    
    # Check if regular admin already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Create regular admin user
        admin_user = User(
            username='admin',
            email='admin2@brainlinktracker.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            status='active',
            is_active=True,
            is_verified=True,
            plan_type='pro',
            daily_link_limit=1000,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow(),
            login_count=1
        )
        db.session.add(admin_user)
        print("✅ Created admin user: admin")
    else:
        print("✅ Admin user already exists: admin")
    
    # Commit changes
    try:
        db.session.commit()
        print("✅ Database updated successfully!")
        
        # Verify users were created
        all_users = User.query.all()
        print(f"\n📊 Total users in database: {len(all_users)}")
        for user in all_users:
            print(f"   - {user.username} ({user.role}) - {user.email}")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error updating database: {e}")

if __name__ == "__main__":
    # Import Flask app to get database context
    from api.index import app
    
    with app.app_context():
        print("🚀 Initializing admin users...")
        init_admin_users()
