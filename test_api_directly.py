#!/usr/bin/env python3
"""
Direct API Test - Start server and test basic functionality
"""

import os
import sys
import subprocess
import time
import requests
import json

# Set environment variables
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

def test_basic_api():
    """Test basic API functionality"""
    print("🚀 Starting API functionality test...")
    
    # Start server in background
    server_process = subprocess.Popen(
        [sys.executable, '-c', '''
import os
import sys
sys.path.insert(0, ".")
from api.index import app
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
        '''],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(8)
    
    try:
        base_url = "http://localhost:5000"
        
        # Test 1: Health check
        print("🔍 Testing health check...")
        try:
            response = requests.get(f"{base_url}/api/auth/validate", timeout=5)
            print(f"✅ Health check: {response.status_code} (Expected 401/403)")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            
        # Test 2: Login
        print("🔐 Testing login...")
        try:
            login_data = {
                "username": "Brain",
                "password": "Mayflower1!!"
            }
            response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=10)
            print(f"✅ Login test: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('token')
                print(f"✅ Got authentication token: {token[:20]}...")
                
                # Test 3: Authenticated request
                print("🔑 Testing authenticated request...")
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(f"{base_url}/api/admin/dashboard-stats", headers=headers, timeout=10)
                print(f"✅ Dashboard stats: {response.status_code}")
                
                if response.status_code == 200:
                    stats = response.json()
                    print(f"✅ Dashboard data keys: {list(stats.keys())}")
                    
        except Exception as e:
            print(f"❌ Login test failed: {e}")
            
        print("✅ API functionality test completed")
        
    finally:
        # Stop server
        server_process.terminate()
        server_process.wait()
        print("🛑 Server stopped")

if __name__ == "__main__":
    test_basic_api()