import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL environment variable not set.")
    exit(1)

engine = create_engine(DATABASE_URL)

def add_column_if_not_exists(connection, table_name, column_name, column_type, default_value=None):
    try:
        # Check if the column already exists
        result = connection.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name=\'{table_name}\' AND column_name=\'{column_name}\'"))
        if result.fetchone() is None:
            default_clause = f" DEFAULT \'{default_value}\'" if default_value is not None else ""
            if column_type == "TEXT" and default_value is None:
                default_clause = ""
            elif column_type == "VARCHAR(500)" and default_value is None:
                default_clause = ""

            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}{default_clause}"))
            connection.commit()
            print(f"Column \'{column_name}\' added to \'{table_name}\' table successfully.")
        else:
            print(f"Column \'{column_name}\' already exists in \'{table_name}\' table.")
    except Exception as e:
        print(f"An error occurred while adding column \'{column_name}\' to \'{table_name}\' table: {e}")

with engine.connect() as connection:
    add_column_if_not_exists(connection, "link", "rate_limiting_enabled", "BOOLEAN", False)
    add_column_if_not_exists(connection, "link", "dynamic_signature_enabled", "BOOLEAN", False)
    add_column_if_not_exists(connection, "link", "mx_verification_enabled", "BOOLEAN", False)
    add_column_if_not_exists(connection, "link", "preview_template_url", "VARCHAR(500)", None)
    add_column_if_not_exists(connection, "link", "allowed_countries", "TEXT", None)
    add_column_if_not_exists(connection, "link", "blocked_countries", "TEXT", None)
    add_column_if_not_exists(connection, "link", "allowed_regions", "TEXT", None)
    add_column_if_not_exists(connection, "link", "blocked_regions", "TEXT", None)
    add_column_if_not_exists(connection, "link", "allowed_cities", "TEXT", None)
    add_column_if_not_exists(connection, "link", "blocked_cities", "TEXT", None)

