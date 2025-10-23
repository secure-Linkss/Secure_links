#!/usr/bin/env python3
"""
Production Database Initialization Script
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from api.index import app, db
    from src.models.user import User
    
    print("🔧 Initializing Production Database...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("  ✅ Database tables created successfully")
        
        # Verify tables exist
        from sqlalchemy import text
        result = db.session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"  ✅ Created {len(tables)} tables: {sorted(tables)}")
        
        # Check if admin users exist (they should be created automatically by the app)
        admin_users = User.query.filter(User.role.in_(['main_admin', 'admin'])).all()
        print(f"  ✅ Found {len(admin_users)} admin users")
        
        for user in admin_users:
            print(f"    - {user.username} ({user.role}) - Status: {user.status}")
        
        print("🎉 Database initialization completed successfully!")
        
except Exception as e:
    print(f"❌ Database initialization failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)