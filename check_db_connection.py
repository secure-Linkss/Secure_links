import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Use the provided URL directly
DATABASE_URL = "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

if not DATABASE_URL:
    print("Error: DATABASE_URL is not set.")
    exit(1)

print(f"Attempting to connect to: {DATABASE_URL.split('@')[-1]}")

try:
    # Create a SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Attempt to connect and execute a simple query
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("Database connection successful.")
        print(f"PostgreSQL Version: {result.scalar()}")
    
    # Check if the database contains the 'user' table (a core table)
    with engine.connect() as connection:
        # Note: PostgreSQL table names are typically lowercase.
        result = connection.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user');"))
        if result.scalar():
            print("Core 'user' table found. Database schema is likely initialized.")
        else:
            print("Warning: Core 'user' table NOT found. Schema initialization may be required.")

except Exception as e:
    print(f"Database connection failed: {e}")
    exit(1)

