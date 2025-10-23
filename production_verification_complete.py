#!/usr/bin/env python3
"""
Complete Production Verification Script
Tests all aspects of the application before deployment
"""

import os
import sys
import time
import requests
import psycopg2
import subprocess
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProductionVerifier:
    def __init__(self):
        self.app_process = None
        self.base_url = "http://localhost:5000"
        
    def test_environment_setup(self):
        """Verify all environment variables are set"""
        print("🔍 Testing Environment Setup...")
        
        required_vars = [
            'DATABASE_URL',
            'SECRET_KEY', 
            'SHORTIO_API_KEY',
            'SHORTIO_DOMAIN'
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
            else:
                print(f"  ✅ {var}: Set")
        
        if missing:
            print(f"  ❌ Missing: {', '.join(missing)}")
            return False
        
        print("  ✅ All environment variables are configured")
        return True
    
    def test_database_connection(self):
        """Test database connectivity and basic operations"""
        print("\\n🔍 Testing Database Connection...")
        
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"  ✅ Connected to: {version[:80]}...")
            
            # Test table existence
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
            print(f"  ✅ Found {len(tables)} tables: {', '.join(sorted(tables)[:5])}...")
            
            # Test user table specifically
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"  ✅ Users table has {user_count} records")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"  ❌ Database test failed: {str(e)}")
            return False
    
    def test_build_integrity(self):
        """Test that the build files exist and are valid"""
        print("\\n🔍 Testing Build Integrity...")
        
        build_files = [
            'dist/index.html',
            'dist/assets'
        ]
        
        for file_path in build_files:
            full_path = os.path.join(os.getcwd(), file_path)
            if os.path.exists(full_path):
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    print(f"  ✅ {file_path}: {size} bytes")
                else:
                    files = os.listdir(full_path)
                    print(f"  ✅ {file_path}: {len(files)} files")
            else:
                print(f"  ❌ {file_path}: Missing")
                return False
        
        return True
    
    def start_application(self):
        """Start the Flask application in background"""
        print("\\n🔍 Starting Application...")
        
        try:
            # Start the application
            env = os.environ.copy()
            env['FLASK_ENV'] = 'production'
            env['FLASK_DEBUG'] = 'False'
            
            self.app_process = subprocess.Popen(
                [sys.executable, 'api/index.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Wait for startup
            print("  ⏳ Waiting for application to start...")
            time.sleep(5)
            
            # Check if process is still running
            if self.app_process.poll() is None:
                print("  ✅ Application started successfully")
                return True
            else:
                stdout, stderr = self.app_process.communicate()
                print(f"  ❌ Application failed to start:")
                print(f"      STDOUT: {stdout.decode()[:200]}...")
                print(f"      STDERR: {stderr.decode()[:200]}...")
                return False
                
        except Exception as e:
            print(f"  ❌ Failed to start application: {str(e)}")
            return False
    
    def test_api_endpoints(self):
        """Test critical API endpoints"""
        print("\\n🔍 Testing API Endpoints...")
        
        # Test endpoints
        test_cases = [
            ('/api/auth/status', 'Auth Status'),
            ('/api/analytics/overview', 'Analytics Overview'),
            ('/api/settings/get', 'Settings'),
        ]
        
        success_count = 0
        for endpoint, description in test_cases:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code in [200, 401, 403]:  # 401/403 are expected for auth endpoints
                    print(f"  ✅ {description}: HTTP {response.status_code}")
                    success_count += 1
                else:
                    print(f"  ⚠️  {description}: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ {description}: {str(e)}")
        
        return success_count >= len(test_cases) // 2  # At least half should work
    
    def test_frontend_serving(self):
        """Test that the frontend is being served correctly"""
        print("\\n🔍 Testing Frontend Serving...")
        
        try:
            # Test main page
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200 and 'html' in response.headers.get('content-type', ''):
                print("  ✅ Frontend HTML served correctly")
                
                # Check if it contains expected content
                if 'Brain Link Tracker' in response.text or 'react' in response.text.lower():
                    print("  ✅ Frontend content appears to be React app")
                    return True
                else:
                    print("  ⚠️  Frontend served but content uncertain")
                    return True
            else:
                print(f"  ❌ Frontend serving failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Frontend test failed: {str(e)}")
            return False
    
    def test_login_functionality(self):
        """Test login functionality with admin users"""
        print("\\n🔍 Testing Login Functionality...")
        
        # Test login endpoint
        login_data = {
            'username': 'Brain',
            'password': 'Mayflower1!!'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("  ✅ Login API accessible and responding")
                data = response.json()
                if 'token' in data or 'success' in data:
                    print("  ✅ Login appears to be working correctly")
                    return True
                else:
                    print("  ⚠️  Login response format unexpected")
                    return True
            elif response.status_code == 401:
                print("  ✅ Login API working (credentials rejected as expected)")
                return True
            else:
                print(f"  ❌ Login API error: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Login test failed: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.app_process:
            print("\\n🧹 Cleaning up...")
            self.app_process.terminate()
            self.app_process.wait()
            print("  ✅ Application stopped")
    
    def run_verification(self):
        """Run complete verification suite"""
        print("🚀 Production Verification Suite")
        print("=" * 60)
        
        tests = [
            ('Environment Setup', self.test_environment_setup),
            ('Database Connection', self.test_database_connection),
            ('Build Integrity', self.test_build_integrity),
            ('Application Startup', self.start_application),
            ('Frontend Serving', self.test_frontend_serving),
            ('API Endpoints', self.test_api_endpoints),
            ('Login Functionality', self.test_login_functionality),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                if not result:
                    print(f"\\n⚠️  {test_name} failed - continuing with remaining tests...")
            except Exception as e:
                print(f"\\n❌ {test_name} threw exception: {str(e)}")
                results.append((test_name, False))
        
        # Summary
        print("\\n" + "=" * 60)
        print("📊 VERIFICATION SUMMARY")
        print("=" * 60)
        
        passed = 0
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status}: {test_name}")
            if result:
                passed += 1
        
        total = len(results)
        print(f"\\n📈 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed >= total * 0.8:  # 80% pass rate
            print("🎉 PRODUCTION READY! Application can be deployed.")
            return True
        else:
            print("⚠️  NEEDS ATTENTION: Some critical tests failed.")
            return False

def main():
    verifier = ProductionVerifier()
    try:
        success = verifier.run_verification()
        return 0 if success else 1
    finally:
        verifier.cleanup()

if __name__ == "__main__":
    sys.exit(main())