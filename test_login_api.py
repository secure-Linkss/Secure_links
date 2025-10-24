#!/usr/bin/env python3
"""
Test login API functionality
"""
import os
import sys

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'

sys.path.insert(0, os.path.dirname(__file__))

from api.index import app
from src.models.user import User, db

# Create test client
client = app.test_client()

print("=" * 80)
print("TESTING LOGIN API")
print("=" * 80)

# Test login with admin account
print("\n1. Testing login with 'Brain' account...")
response = client.post('/api/auth/login', 
    json={
        'username': 'Brain',
        'password': 'Mayflower1!!'
    },
    content_type='application/json'
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.get_json()}")

# Test login with 7thbrain account
print("\n2. Testing login with '7thbrain' account...")
response = client.post('/api/auth/login', 
    json={
        'username': '7thbrain',
        'password': 'Mayflower1!'
    },
    content_type='application/json'
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.get_json()}")

# Test invalid credentials
print("\n3. Testing login with invalid credentials...")
response = client.post('/api/auth/login', 
    json={
        'username': 'invalid',
        'password': 'wrong'
    },
    content_type='application/json'
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.get_json()}")

# Check database users
print("\n4. Checking users in database...")
with app.app_context():
    users = User.query.filter(User.username.in_(['Brain', '7thbrain'])).all()
    for user in users:
        print(f"  - {user.username}: role={user.role}, status={user.status}, is_active={user.is_active}, is_verified={user.is_verified}")
        # Test password check
        pwd = 'Mayflower1!!' if user.username == 'Brain' else 'Mayflower1!'
        pwd_check = user.check_password(pwd)
        print(f"    Password check: {pwd_check}")

print("\n" + "=" * 80)
print("LOGIN API TEST COMPLETED")
print("=" * 80)
