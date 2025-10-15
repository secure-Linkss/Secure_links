'''
from src.main import create_app, db
from src.models.user import User
from src.models.link import Link

def seed_db():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Check if user already exists
        user = User.query.filter_by(username='Brain').first()
        if not user:
            # Create a user
            user = User(username='Brain', email='admin@brainlinktracker.com')
            user.set_password('Mayflower1!!')
            db.session.add(user)
            db.session.commit()

            # Create a link
            link = Link(
                user_id=user.id,
                name='Test Campaign',
                target_url='https://www.example.com',
            )
            db.session.add(link)
            db.session.commit()

            print('Database seeded!')
'''
