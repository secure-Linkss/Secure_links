import os
from src.main import app
from flask_migrate import upgrade

# Set the DATABASE_URL environment variable for the app context
os.environ['DATABASE_URL'] = "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

with app.app_context():
    # This will run the latest migration, creating all tables if they don't exist
    print("Attempting to run database migration (upgrade)...")
    try:
        upgrade()
        print("Database migration successful. All necessary tables should now exist.")
    except Exception as e:
        print(f"Database migration failed: {e}")

