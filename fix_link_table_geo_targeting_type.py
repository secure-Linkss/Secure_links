import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL environment variable not set.")
    exit(1)

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    try:
        # Check if the column already exists to prevent errors on re-run
        result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name=\'link\' AND column_name=\'geo_targeting_type\'"))
        if result.fetchone() is None:
            connection.execute(text("ALTER TABLE link ADD COLUMN geo_targeting_type VARCHAR(20) DEFAULT \'allow\'"))
            connection.commit()
            print("Column \'geo_targeting_type\' added to \'link\' table successfully.")
        else:
            print("Column \'geo_targeting_type\' already exists in \'link\' table.")
    except Exception as e:
        print(f"An error occurred during link table migration: {e}")

