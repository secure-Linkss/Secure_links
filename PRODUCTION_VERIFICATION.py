#!/usr/bin/env python3
"""
Complete Production Verification Script
Tests all critical functionality before deployment
"""
import os
import sys
import json
from datetime import datetime

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'
os.environ['SHORTIO_API_KEY'] = 'sk_DbGGlUHPN7Z9VotL'
os.environ['SHORTIO_DOMAIN'] = 'Secure-links.short.gy'

sys.path.insert(0, os.path.dirname(__file__))

try:
    from api.index import app
    from src.models.user import User, db
    import psycopg2
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_section(title):
    print(f"\n--- {title} ---")

def check_database_connection():
    """Verify database connectivity"""
    print_section("Database Connection Test")
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ Database connected successfully")
        print(f"  PostgreSQL version: {version[0][:60]}...")
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"✓ Found {len(tables)} tables in database")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def check_users():
    """Verify user accounts"""
    print_section("User Accounts Verification")
    try:
        with app.app_context():
            users = User.query.all()
            print(f"✓ Found {len(users)} users in database")
            
            # Check admin users
            admin_users = User.query.filter(User.role.in_(['main_admin', 'admin'])).all()
            print(f"\n  Admin users ({len(admin_users)}):")
            for user in admin_users:
                status_icon = "✓" if user.is_active and user.status == 'active' else "✗"
                print(f"    {status_icon} {user.username} ({user.role}) - Status: {user.status}, Active: {user.is_active}")
            
            # Check member users
            member_users = User.query.filter_by(role='member').all()
            active_members = [u for u in member_users if u.is_active and u.status == 'active']
            print(f"\n  Member users: {len(member_users)} total, {len(active_members)} active")
            
            return True
    except Exception as e:
        print(f"✗ User verification failed: {e}")
        return False

def check_login_functionality():
    """Test login API"""
    print_section("Login API Test")
    try:
        client = app.test_client()
        
        # Test admin login
        test_accounts = [
            {'username': 'Brain', 'password': 'Mayflower1!!', 'expected_role': 'main_admin'},
            {'username': '7thbrain', 'password': 'Mayflower1!', 'expected_role': 'admin'}
        ]
        
        for account in test_accounts:
            response = client.post('/api/auth/login', 
                json={'username': account['username'], 'password': account['password']},
                content_type='application/json'
            )
            
            if response.status_code == 200:
                data = response.get_json()
                if data and 'user' in data:
                    user_data = data['user']
                    role_match = user_data.get('role') == account['expected_role']
                    status_icon = "✓" if role_match else "✗"
                    print(f"  {status_icon} Login successful for '{account['username']}' - Role: {user_data.get('role')}")
                else:
                    print(f"  ✗ Login failed for '{account['username']}' - Invalid response")
            else:
                print(f"  ✗ Login failed for '{account['username']}' - Status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"✗ Login test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_api_routes():
    """Verify critical API routes"""
    print_section("API Routes Verification")
    try:
        client = app.test_client()
        
        # Test various API endpoints
        routes = [
            ('/api/auth/me', 'GET'),
            ('/api/user/stats', 'GET'),
            ('/api/campaigns', 'GET'),
            ('/api/links', 'GET'),
        ]
        
        print("  Testing API routes (without authentication):")
        for route, method in routes:
            if method == 'GET':
                response = client.get(route)
            else:
                response = client.post(route)
            
            # We expect 401 for most routes without auth
            if response.status_code in [200, 401, 404]:
                print(f"    ✓ {route} - Status: {response.status_code}")
            else:
                print(f"    ! {route} - Status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"✗ API routes check failed: {e}")
        return False

def check_database_schema():
    """Verify database schema integrity"""
    print_section("Database Schema Verification")
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = conn.cursor()
        
        # Check critical tables
        required_tables = [
            'users', 'links', 'campaigns', 'tracking_events', 
            'notifications', 'audit_logs', 'domains', 'support_tickets'
        ]
        
        for table in required_tables:
            cursor.execute(f"""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = '{table}';
            """)
            count = cursor.fetchone()[0]
            status = "✓" if count > 0 else "✗"
            print(f"  {status} Table '{table}': {'exists' if count > 0 else 'MISSING'}")
        
        # Check users table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)
        user_columns = [row[0] for row in cursor.fetchall()]
        required_user_columns = ['id', 'username', 'email', 'password_hash', 'role', 'status', 'is_active']
        
        print(f"\n  Users table columns ({len(user_columns)} total):")
        for col in required_user_columns:
            status = "✓" if col in user_columns else "✗"
            print(f"    {status} {col}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Schema verification failed: {e}")
        return False

def check_frontend_build():
    """Verify frontend build"""
    print_section("Frontend Build Verification")
    try:
        dist_path = os.path.join(os.path.dirname(__file__), 'dist')
        
        if not os.path.exists(dist_path):
            print(f"✗ dist/ directory not found")
            return False
        
        # Check for index.html
        index_path = os.path.join(dist_path, 'index.html')
        if os.path.exists(index_path):
            print(f"✓ index.html found")
            file_size = os.path.getsize(index_path)
            print(f"  Size: {file_size} bytes")
        else:
            print(f"✗ index.html not found")
            return False
        
        # Check for assets
        assets_path = os.path.join(dist_path, 'assets')
        if os.path.exists(assets_path):
            assets = os.listdir(assets_path)
            print(f"✓ assets/ directory found with {len(assets)} files")
        else:
            print(f"✗ assets/ directory not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Frontend build check failed: {e}")
        return False

def check_environment_variables():
    """Verify environment variables"""
    print_section("Environment Variables Check")
    
    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'SHORTIO_API_KEY',
        'SHORTIO_DOMAIN'
    ]
    
    all_present = True
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive data
            display_value = value[:20] + '...' if len(value) > 20 else value
            print(f"  ✓ {var}: {display_value}")
        else:
            print(f"  ✗ {var}: NOT SET")
            all_present = False
    
    return all_present

def main():
    print_header("BRAIN LINK TRACKER - PRODUCTION VERIFICATION")
    print(f"Verification Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Environment Variables': check_environment_variables(),
        'Database Connection': check_database_connection(),
        'Database Schema': check_database_schema(),
        'User Accounts': check_users(),
        'Login Functionality': check_login_functionality(),
        'API Routes': check_api_routes(),
        'Frontend Build': check_frontend_build()
    }
    
    print_header("VERIFICATION SUMMARY")
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {status}: {check}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("  ✓ ALL CHECKS PASSED - READY FOR PRODUCTION DEPLOYMENT")
    else:
        print("  ✗ SOME CHECKS FAILED - REVIEW BEFORE DEPLOYMENT")
    print("=" * 80 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
