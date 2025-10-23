#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from api.index import app
from src.models.user import User, db
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from datetime import datetime, timedelta
import random

def populate_test_data():
    with app.app_context():
        # Sample data for testing
        countries = ['United States', 'United Kingdom', 'Canada', 'Germany', 'France', 'Australia']
        cities = ['New York', 'London', 'Toronto', 'Berlin', 'Paris', 'Sydney']
        devices = ['desktop', 'mobile', 'tablet']
        browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
        os_list = ['Windows', 'macOS', 'Linux', 'iOS', 'Android']

        print('Creating sample tracking events for testing...')

        # Get the first user and their links
        user = User.query.first()
        if user:
            print(f'Found user: {user.username}')
            
            # Create some sample links if none exist
            if Link.query.filter_by(user_id=user.id).count() == 0:
                print('Creating sample links...')
                sample_links = [
                    Link(
                        user_id=user.id,
                        target_url='https://example.com',
                        campaign_name='Sample Campaign 1',
                        short_code='abc123'
                    ),
                    Link(
                        user_id=user.id,
                        target_url='https://test.com',
                        campaign_name='Sample Campaign 2',
                        short_code='def456'
                    ),
                    Link(
                        user_id=user.id,
                        target_url='https://demo.com',
                        campaign_name='Sample Campaign 3',
                        short_code='ghi789'
                    )
                ]
                for link in sample_links:
                    db.session.add(link)
                db.session.commit()
                print('Created 3 sample links')
            
            links = Link.query.filter_by(user_id=user.id).all()
            if links:
                print(f'Found {len(links)} links')
                
                # Create sample tracking events
                for i in range(100):  # Create 100 sample events
                    link = random.choice(links)
                    event = TrackingEvent(
                        link_id=link.id,
                        ip_address=f'192.168.{random.randint(1, 255)}.{random.randint(1, 254)}',
                        user_agent=f'{random.choice(browsers)}/100.0 (compatible)',
                        country=random.choice(countries),
                        city=random.choice(cities),
                        device_type=random.choice(devices),
                        browser=random.choice(browsers),
                        os=random.choice(os_list),
                        is_bot=random.choice([True, False]),
                        captured_email=random.choice([True, False]) if random.random() > 0.7 else False,
                        timestamp=datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
                    )
                    db.session.add(event)
                
                db.session.commit()
                print(f'Created 100 sample tracking events for testing')
                
                # Print some statistics
                total_events = TrackingEvent.query.count()
                total_links = Link.query.count()
                total_users = User.query.count()
                
                print(f'\nDatabase Statistics:')
                print(f'Total Users: {total_users}')
                print(f'Total Links: {total_links}')
                print(f'Total Events: {total_events}')
                
            else:
                print('No links found for user')
        else:
            print('No users found')

if __name__ == '__main__':
    populate_test_data()
