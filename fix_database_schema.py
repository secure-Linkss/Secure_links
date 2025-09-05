#!/usr/bin/env python3
"""
Database schema fix script to resolve foreign key constraints and table issues
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL')
    if database_url and 'postgresql' in database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        os.makedirs(os.path.join(os.path.dirname(__file__), 'src', 'database'), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE')
    
    db.init_app(app)
    return app

def fix_database_schema():
    app = create_app()
    
    with app.app_context():
        print("Starting database schema fix...")
        
        try:
            # Try to create all tables (this will handle missing tables)
            print("Creating/updating database tables...")
            db.create_all()
            
            # Verify admin user exists
            print("Checking admin user...")
            admin_user = User.query.filter_by(username="Brain").first()
            if not admin_user:
                print("Creating default admin user...")
                admin_user = User(username="Brain", email="admin@brainlinktracker.com", role="admin")
                admin_user.set_password("Mayflower1!!")
                db.session.add(admin_user)
                db.session.commit()
                print("Default admin user 'Brain' created successfully.")
            else:
                print("Admin user already exists.")
            
            # Test link creation to verify schema is working
            print("Testing link creation...")
            test_link = Link(
                user_id=admin_user.id,
                target_url="https://test.example.com",
                short_code="test123",
                campaign_name="Test Campaign"
            )
            db.session.add(test_link)
            db.session.commit()
            
            # Clean up test link
            db.session.delete(test_link)
            db.session.commit()
            
            print("Database schema fix completed successfully!")
            print("Link creation test passed!")
            
        except Exception as e:
            print(f"Error during schema fix: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    fix_database_schema()

