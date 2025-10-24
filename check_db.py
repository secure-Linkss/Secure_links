import psycopg2

db_url = "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
    tables = cur.fetchall()
    
    print(f"✅ Database connected! Found {len(tables)} tables:\n")
    for t in tables:
        print(f"  - {t[0]}")
    
    # Check if key tables exist
    table_names = [t[0] for t in tables]
    required_tables = ['users', 'links', 'campaigns', 'tracking_events', 'notifications']
    
    print("\n📋 Required tables check:")
    for table in required_tables:
        if table in table_names:
            print(f"  ✅ {table}")
        else:
            print(f"  ❌ {table} - MISSING")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
