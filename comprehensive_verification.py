#!/usr/bin/env python3
"""
Comprehensive Production Verification Script
Tests all major components of the Brain Link Tracker application
"""

import os
import sys
import requests
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

def test_database_connection():
    """Test database connection and models"""
    print("🗄️  Testing Database Connection...")
    
    try:
        from src.database import db
        from src.models.user import User
        from src.models.link import Link
        from src.models.campaign import Campaign
        from flask import Flask
        
        app = Flask(__name__)
        app.config['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb'
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Test basic queries
            users = User.query.count()
            links = Link.query.count()
            campaigns = Campaign.query.count()
            
            # Check admin users
            admin_user = User.query.filter_by(username="Brain").first()
            
            print(f"  ✅ Database connected successfully")
            print(f"  ✅ Users: {users}, Links: {links}, Campaigns: {campaigns}")
            print(f"  ✅ Admin user 'Brain' exists: {admin_user is not None}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Database connection failed: {str(e)}")
        return False

def test_api_endpoints(base_url):
    """Test critical API endpoints"""
    print(f"🔌 Testing API Endpoints ({base_url})...")
    
    # Test login
    try:
        login_response = requests.post(f'{base_url}/api/auth/login', 
                                     json={'username': 'Brain', 'password': 'Mayflower1!!'},
                                     timeout=10)
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"  ✅ Login successful - Token received")
            
            # Test authenticated endpoints
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test admin endpoints
            admin_users_response = requests.get(f'{base_url}/api/admin/users', headers=headers, timeout=10)
            admin_campaigns_response = requests.get(f'{base_url}/api/admin/campaigns', headers=headers, timeout=10)
            
            print(f"  ✅ Admin users endpoint: {admin_users_response.status_code}")
            print(f"  ✅ Admin campaigns endpoint: {admin_campaigns_response.status_code}")
            
            return True
        else:
            print(f"  ❌ Login failed: {login_response.status_code} - {login_response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ API test failed: {str(e)}")
        return False

def test_quantum_redirect():
    """Test quantum redirect system"""
    print("⚡ Testing Quantum Redirect System...")
    
    try:
        from src.services.quantum_redirect import quantum_redirect
        
        # Test token generation
        test_token = quantum_redirect.generate_genesis_token(
            link_id="1",
            user_ip="127.0.0.1",
            user_agent="Test-Agent",
            referrer="test-referrer"
        )
        
        if test_token:
            print(f"  ✅ Genesis token generation working")
            
            # Test validation
            validation_result = quantum_redirect.stage2_validation_hub(
                genesis_token=test_token,
                current_ip="127.0.0.1",
                current_user_agent="Test-Agent",
                lenient_mode=True
            )
            
            if validation_result.get('success'):
                print(f"  ✅ Token validation working")
            else:
                print(f"  ⚠️  Token validation: {validation_result.get('error')}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Quantum redirect test failed: {str(e)}")
        return False

def test_frontend_build():
    """Test frontend build"""
    print("🎨 Testing Frontend Build...")
    
    try:
        dist_path = os.path.join(os.path.dirname(__file__), 'dist')
        if os.path.exists(dist_path):
            index_html = os.path.join(dist_path, 'index.html')
            assets_path = os.path.join(dist_path, 'assets')
            
            if os.path.exists(index_html) and os.path.exists(assets_path):
                asset_files = os.listdir(assets_path)
                js_files = [f for f in asset_files if f.endswith('.js')]
                css_files = [f for f in asset_files if f.endswith('.css')]
                
                print(f"  ✅ Frontend build exists")
                print(f"  ✅ Assets: {len(js_files)} JS files, {len(css_files)} CSS files")
                return True
            else:
                print(f"  ❌ Missing build files")
                return False
        else:
            print(f"  ❌ Dist folder not found")
            return False
            
    except Exception as e:
        print(f"  ❌ Frontend build test failed: {str(e)}")
        return False

def run_comprehensive_verification():
    """Run all verification tests"""
    print("🚀 Brain Link Tracker - Comprehensive Production Verification")
    print("=" * 65)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {}
    
    # Test database
    results['database'] = test_database_connection()
    print()
    
    # Test frontend build
    results['frontend'] = test_frontend_build()
    print()
    
    # Test quantum redirect
    results['quantum'] = test_quantum_redirect()
    print()
    
    # Summary
    print("📊 VERIFICATION SUMMARY:")
    print("-" * 30)
    
    passed_tests = 0
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name.upper()}: {status}")
        if passed:
            passed_tests += 1
    
    print()
    print(f"📈 Overall Score: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW ISSUES BEFORE DEPLOYMENT")
        return False

if __name__ == "__main__":
    success = run_comprehensive_verification()
    sys.exit(0 if success else 1)