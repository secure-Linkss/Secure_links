import psycopg2
import os

# The URL you provided seems to be a psql command format, not a connection string
# Let's parse it correctly
raw_url = "psql 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Extract the actual connection string
if "psql" in raw_url:
    # Remove psql and quotes
    conn_str = raw_url.replace("psql", "").strip().strip("'").strip('"')
    print(f"Cleaned connection string: {conn_str}")
    
    # Test connection
    try:
        conn = psycopg2.connect(conn_str)
        print("✓ Connection successful!")
        conn.close()
    except Exception as e:
        print(f"✗ Connection failed: {e}")
