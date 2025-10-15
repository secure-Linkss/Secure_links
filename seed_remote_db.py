
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
    # Set the DATABASE_URL environment variable for the script
    os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    seed_db_remote()

