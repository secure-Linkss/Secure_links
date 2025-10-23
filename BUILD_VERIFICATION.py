#!/usr/bin/env python3
"""
Build Verification Script for Brain Link Tracker
Tests all critical components before deployment
"""

import os
import sys
import json

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"  ✅ {description}")
        return True
    else:
        print(f"  ❌ MISSING: {description} ({filepath})")
        return False

def check_python_imports():
    """Check if all Python modules can be imported"""
    print("\n=== Checking Python Imports ===")
    errors = []
    
    modules_to_check = [
        ('flask', 'Flask'),
        ('flask_cors', 'CORS'),
        ('flask_sqlalchemy', 'SQLAlchemy'),
        ('flask_migrate', 'Migrate'),
        ('werkzeug.security', 'generate_password_hash'),
        ('jwt', 'JWT'),
        ('requests', 'Requests'),
        ('psycopg2', 'PostgreSQL Driver')
    ]
    
    for module_name, display_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"  ✅ {display_name}")
        except ImportError as e:
            print(f"  ❌ {display_name}: {e}")
            errors.append(display_name)
    
    return len(errors) == 0

def check_models():
    """Check if all models can be imported"""
    print("\n=== Checking Models ===")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from src.models.user import User
        print("  ✅ User model")
        
        from src.models.link import Link
        print("  ✅ Link model")
        
        from src.models.tracking_event import TrackingEvent
        print("  ✅ TrackingEvent model")
        
        from src.models.campaign import Campaign
        print("  ✅ Campaign model")
        
        from src.models.audit_log import AuditLog
        print("  ✅ AuditLog model")
        
        from src.models.notification import Notification
        print("  ✅ Notification model")
        
        from src.models.domain import Domain
        print("  ✅ Domain model")
        
        from src.models.security_threat import SecurityThreat
        print("  ✅ SecurityThreat model")
        
        return True
    except Exception as e:
        print(f"  ❌ Model import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_routes():
    """Check if all routes can be imported"""
    print("\n=== Checking Routes ===")
    
    try:
        from src.routes.auth import auth_bp
        print("  ✅ Auth routes")
        
        from src.routes.links import links_bp
        print("  ✅ Links routes")
        
        from src.routes.analytics import analytics_bp
        print("  ✅ Analytics routes")
        
        from src.routes.campaigns import campaigns_bp
        print("  ✅ Campaigns routes")
        
        from src.routes.admin import admin_bp
        print("  ✅ Admin routes")
        
        from src.routes.security import security_bp
        print("  ✅ Security routes")
        
        from src.routes.shorten import shorten_bp
        print("  ✅ Shorten routes")
        
        from src.routes.notifications import notifications_bp
        print("  ✅ Notifications routes")
        
        from src.routes.track import track_bp
        print("  ✅ Track routes")
        
        return True
    except Exception as e:
        print(f"  ❌ Route import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_frontend_components():
    """Check if frontend files exist"""
    print("\n=== Checking Frontend Components ===")
    
    components = [
        'src/components/LoginPage.jsx',
        'src/components/Dashboard.jsx',
        'src/components/TrackingLinks.jsx',
        'src/components/Campaign.jsx',
        'src/components/CampaignManagement.jsx',
        'src/components/Analytics.jsx',
        'src/components/AdminPanel.jsx',
        'src/components/AdminPanelComplete.jsx',
        'src/components/Security.jsx',
        'src/components/Settings.jsx',
        'src/components/LiveActivity.jsx',
        'src/components/Notifications.jsx',
        'src/components/CreateLinkModal.jsx',
        'src/components/LinkShortener.jsx',
        'src/components/InteractiveMap.jsx',
        'src/App.jsx',
        'src/main.jsx'
    ]
    
    all_exist = True
    for component in components:
        if not check_file_exists(component, component):
            all_exist = False
    
    return all_exist

def check_config_files():
    """Check if configuration files exist"""
    print("\n=== Checking Configuration Files ===")
    
    config_files = [
        ('vercel.json', 'Vercel configuration'),
        ('package.json', 'Package configuration'),
        ('requirements.txt', 'Python requirements'),
        ('vite.config.js', 'Vite configuration'),
        ('tailwind.config.js', 'Tailwind configuration'),
        ('api/index.py', 'API entry point')
    ]
    
    all_exist = True
    for filepath, description in config_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_env_variables():
    """Check environment variables"""
    print("\n=== Checking Environment Variables ===")
    
    required_vars = [
        ('SECRET_KEY', False),
        ('DATABASE_URL', False),
        ('SHORTIO_API_KEY', True),
        ('SHORTIO_DOMAIN', True)
    ]
    
    all_set = True
    for var_name, is_optional in required_vars:
        if os.environ.get(var_name):
            print(f"  ✅ {var_name} is set")
        else:
            if is_optional:
                print(f"  ⚠️  {var_name} is not set (optional)")
            else:
                print(f"  ❌ {var_name} is not set (REQUIRED)")
                all_set = False
    
    return all_set

def check_api_index():
    """Check API index.py for correct configuration"""
    print("\n=== Checking API Configuration ===")
    
    with open('api/index.py', 'r') as f:
        content = f.read()
        
        checks = [
            ('from src.models.user import db, User', 'User model import'),
            ('from src.routes.auth import auth_bp', 'Auth routes import'),
            ('from src.routes.links import links_bp', 'Links routes import'),
            ('app.register_blueprint(auth_bp', 'Auth blueprint registration'),
            ('app.register_blueprint(links_bp', 'Links blueprint registration'),
            ('db.init_app(app)', 'Database initialization'),
            ('db.create_all()', 'Table creation')
        ]
        
        all_passed = True
        for check_str, description in checks:
            if check_str in content:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ MISSING: {description}")
                all_passed = False
        
        return all_passed

def main():
    """Main execution function"""
    print("=" * 60)
    print("BRAIN LINK TRACKER - BUILD VERIFICATION")
    print("=" * 60)
    
    results = []
    
    # Check Python imports
    results.append(("Python Imports", check_python_imports()))
    
    # Check models
    results.append(("Models", check_models()))
    
    # Check routes
    results.append(("Routes", check_routes()))
    
    # Check frontend components
    results.append(("Frontend Components", check_frontend_components()))
    
    # Check config files
    results.append(("Configuration Files", check_config_files()))
    
    # Check environment variables (informational only)
    check_env_variables()
    
    # Check API configuration
    results.append(("API Configuration", check_api_index()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("BUILD VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("✅ ALL CHECKS PASSED - READY FOR BUILD")
        return True
    else:
        print("❌ SOME CHECKS FAILED - PLEASE FIX ISSUES")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
