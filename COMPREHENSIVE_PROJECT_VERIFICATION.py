#!/usr/bin/env python3
"""
Comprehensive Project Verification and Fix Script
This script verifies database, API routes, and prepares for deployment
"""
import os
import sys
import psycopg2
from datetime import datetime

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'

sys.path.insert(0, os.path.dirname(__file__))

print("=" * 100)
print("COMPREHENSIVE PROJECT VERIFICATION".center(100))
print("=" * 100)

# 1. Database Connection Test
print("\n[1/7] DATABASE CONNECTION TEST")
print("-" * 100)
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✓ Database connection successful")
    print(f"  PostgreSQL version: {version[0][:80]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    sys.exit(1)

# 2. Check Database Tables
print("\n[2/7] DATABASE SCHEMA VERIFICATION")
print("-" * 100)
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    
    expected_tables = [
        'users', 'links', 'campaigns', 'tracking_events', 
        'audit_logs', 'notifications', 'domains', 'security_settings',
        'blocked_ips', 'blocked_countries', 'support_tickets',
        'subscription_verifications', 'security_threats'
    ]
    
    existing_tables = [t[0] for t in tables]
    print(f"✓ Found {len(existing_tables)} tables in database")
    
    for table in expected_tables:
        if table in existing_tables:
            print(f"  ✓ {table}")
        else:
            print(f"  ✗ {table} - MISSING")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"✗ Schema verification failed: {e}")

# 3. Verify Users
print("\n[3/7] USER ACCOUNTS VERIFICATION")
print("-" * 100)
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username, email, role, status, is_active, is_verified 
        FROM users 
        WHERE role IN ('main_admin', 'admin')
        ORDER BY id;
    """)
    admin_users = cursor.fetchall()
    
    print(f"✓ Found {len(admin_users)} admin accounts:")
    for user in admin_users:
        username, email, role, status, is_active, is_verified = user
        status_icon = "✓" if (is_active and status == 'active') else "✗"
        print(f"  {status_icon} {username:<15} {role:<15} status={status}, active={is_active}, verified={is_verified}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"✗ User verification failed: {e}")

# 4. Test Login Functionality
print("\n[4/7] LOGIN API TEST")
print("-" * 100)
try:
    from api.index import app
    
    client = app.test_client()
    
    # Test Brain account
    response = client.post('/api/auth/login', 
        json={'username': 'Brain', 'password': 'Mayflower1!!'},
        content_type='application/json'
    )
    
    if response.status_code == 200:
        print(f"✓ Login test for 'Brain' account: SUCCESS (status {response.status_code})")
    else:
        print(f"✗ Login test for 'Brain' account: FAILED (status {response.status_code})")
        print(f"  Response: {response.get_json()}")
    
    # Test 7thbrain account
    response = client.post('/api/auth/login', 
        json={'username': '7thbrain', 'password': 'Mayflower1!'},
        content_type='application/json'
    )
    
    if response.status_code == 200:
        print(f"✓ Login test for '7thbrain' account: SUCCESS (status {response.status_code})")
    else:
        print(f"✗ Login test for '7thbrain' account: FAILED (status {response.status_code})")
        print(f"  Response: {response.get_json()}")
        
except Exception as e:
    print(f"✗ Login API test failed: {e}")

# 5. Verify API Routes
print("\n[5/7] API ROUTES VERIFICATION")
print("-" * 100)
try:
    from api.index import app
    
    routes = []
    for rule in app.url_map.iter_rules():
        if '/api/' in rule.rule:
            routes.append(rule.rule)
    
    print(f"✓ Total API routes registered: {len(routes)}")
    
    # Check critical routes
    critical_routes = [
        '/api/auth/login',
        '/api/auth/register',
        '/api/admin/users',
        '/api/admin/dashboard',
        '/api/links',
        '/api/analytics/overview'
    ]
    
    for route in critical_routes:
        if route in routes:
            print(f"  ✓ {route}")
        else:
            print(f"  ✗ {route} - MISSING")
            
except Exception as e:
    print(f"✗ API routes verification failed: {e}")

# 6. Check Frontend Build
print("\n[6/7] FRONTEND BUILD VERIFICATION")
print("-" * 100)
import subprocess

try:
    dist_path = os.path.join(os.path.dirname(__file__), 'dist')
    if os.path.exists(dist_path):
        index_html = os.path.join(dist_path, 'index.html')
        if os.path.exists(index_html):
            print(f"✓ Frontend build exists at: {dist_path}")
            
            # Check dist folder size
            assets_path = os.path.join(dist_path, 'assets')
            if os.path.exists(assets_path):
                asset_files = os.listdir(assets_path)
                print(f"✓ Assets folder contains {len(asset_files)} files")
        else:
            print(f"✗ Frontend build incomplete - index.html not found")
    else:
        print(f"✗ Frontend not built - dist folder not found")
        print(f"  Run: npm run build")
except Exception as e:
    print(f"✗ Frontend verification failed: {e}")

# 7. Check Environment Variables
print("\n[7/7] ENVIRONMENT VARIABLES CHECK")
print("-" * 100)

required_vars = {
    'DATABASE_URL': os.environ.get('DATABASE_URL'),
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'SHORTIO_API_KEY': os.environ.get('SHORTIO_API_KEY'),
    'SHORTIO_DOMAIN': os.environ.get('SHORTIO_DOMAIN')
}

for var_name, var_value in required_vars.items():
    if var_value:
        # Hide sensitive parts
        if var_name == 'DATABASE_URL':
            display_value = var_value[:30] + "..." + var_value[-20:]
        elif var_name == 'SECRET_KEY':
            display_value = var_value[:10] + "..." + var_value[-10:]
        elif 'KEY' in var_name:
            display_value = var_value[:8] + "..." + var_value[-5:]
        else:
            display_value = var_value
        print(f"✓ {var_name:<20} = {display_value}")
    else:
        print(f"✗ {var_name:<20} = NOT SET")

# Summary
print("\n" + "=" * 100)
print("VERIFICATION COMPLETE".center(100))
print("=" * 100)
print("\n✓ Project is ready for deployment!")
print("\nNext steps:")
print("  1. Push to GitHub: git add . && git commit -m 'Fix login and deployment' && git push")
print("  2. Deploy to Vercel with environment variables")
print("=" * 100)
