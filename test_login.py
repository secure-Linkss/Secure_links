#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require'
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'

from flask import Flask
from src.database import db
from src.models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Test if user exists
    user = User.query.filter_by(username='Brain').first()
    if user:
        print(f'✓ User Brain found: {user.email}')
        print(f'  Status: {user.status}, Active: {user.is_active}, Role: {user.role}')
        # Test password
        if user.check_password('Mayflower1!!'):
            print('✓ Password is correct')
            token = user.generate_token()
            print(f'✓ Token generated: {token[:30]}...')
        else:
            print('✗ Password is incorrect - rehashing...')
            user.set_password('Mayflower1!!')
            db.session.commit()
            print('✓ Password reset and rehashed')
    else:
        print('✗ User Brain not found')
        
    print('\n📋 All users in database:')
    users = User.query.all()
    for u in users:
        print(f'  - {u.username} ({u.email}) - Status: {u.status}, Active: {u.is_active}, Role: {u.role}')
