
import os
import sys

sys.path.insert(0, ".") # Add current directory to path

from src.main import app, db # Import app and db directly
from src.models.user import User
from src.models.link import Link

def seed_db_remote():
    with app.app_context():
        # Drop all tables and recreate them to ensure a clean state
        db.drop_all()
        db.create_all()

        # Check if user already exists
        user = User.query.filter_by(username="Brain").first()
        if not user:
            print("Creating default admin user 'Brain'...")
            # Create a user
            user = User(username="Brain", email="admin@brainlinktracker.com", role="admin")
            user.set_password("Mayflower1!!")
            db.session.add(user)
            db.session.commit()

            # Create a link
            link = Link(
                user_id=user.id,
                campaign_name="Test Campaign",
                target_url="https://www.example.com",
            )
            db.session.add(link)
            db.session.commit()

            print("Remote database seeded successfully!")
        else:
            print("User 'Brain' already exists. Skipping seeding.")

if __name__ == "__main__":
    # Get database URL from environment or command line
    database_url = os.environ.get('DATABASE_URL')
    
    if len(sys.argv) > 1:
        database_url = sys.argv[1]
    
    if not database_url:
        print("Error: DATABASE_URL not provided")
        print("Usage: python3 seed_remote_db.py [DATABASE_URL]")
        sys.exit(1)
        
    os.environ["DATABASE_URL"] = database_url
    seed_db_remote()

