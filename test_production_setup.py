#!/usr/bin/env python3
"""
Production Setup Verification Script
Tests database connection, environment variables, and basic functionality
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

def test_environment_variables():
    """Test that all required environment variables are set"""
    print("🔍 Testing Environment Variables...")
    
    # Load environment variables
    load_dotenv()
    
    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'SHORTIO_API_KEY', 
        'SHORTIO_DOMAIN'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"  ✅ {var}: {'*' * min(8, len(value))}...")
    
    if missing_vars:
        print(f"  ❌ Missing variables: {', '.join(missing_vars)}")
        return False
    
    print("  ✅ All required environment variables are set")
    return True

def test_database_connection():
    """Test database connectivity"""
    print("\n🔍 Testing Database Connection...")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("  ❌ DATABASE_URL not set")
        return False
    
    try:
        # Test connection
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"  ✅ Connected to PostgreSQL: {version[0][:50]}...")
        
        # Test if we can create tables (permissions check)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Test insert
        cursor.execute("INSERT INTO connection_test DEFAULT VALUES RETURNING id;")
        test_id = cursor.fetchone()[0]
        print(f"  ✅ Database write test successful (inserted record ID: {test_id})")
        
        # Clean up test table
        cursor.execute("DROP TABLE IF EXISTS connection_test;")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("  ✅ Database connection and permissions verified")
        return True
        
    except Exception as e:
        print(f"  ❌ Database connection failed: {str(e)}")
        return False

def test_shortio_api():
    """Test Short.io API connectivity"""
    print("\n🔍 Testing Short.io API...")
    
    api_key = os.getenv('SHORTIO_API_KEY')
    domain = os.getenv('SHORTIO_DOMAIN')
    
    if not api_key or not domain:
        print("  ⚠️  Short.io credentials not set - skipping API test")
        return True
    
    try:
        import requests
        
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json'
        }
        
        # Test API connectivity with domain info
        response = requests.get(
            f'https://api.short.io/links/expand?domain={domain}&path=test',
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 404]:  # 404 is expected for non-existent link
            print("  ✅ Short.io API accessible")
            return True
        else:
            print(f"  ⚠️  Short.io API returned status {response.status_code}")
            return True  # Don't fail deployment for API issues
            
    except Exception as e:
        print(f"  ⚠️  Short.io API test failed: {str(e)}")
        return True  # Don't fail deployment for API issues

def main():
    """Run all production setup tests"""
    print("🚀 Production Setup Verification")
    print("=" * 50)
    
    tests = [
        test_environment_variables,
        test_database_connection,
        test_shortio_api
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ❌ Test failed with exception: {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All tests passed! Production setup is ready.")
        return True
    else:
        failed_count = len([r for r in results if not r])
        print(f"❌ {failed_count} test(s) failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)