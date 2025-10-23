#!/usr/bin/env python3
"""
MASTER COMPREHENSIVE FIX SCRIPT
Fixes all critical issues identified in the project audit
"""

import os
import sys
import psycopg2
from datetime import datetime

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-a4e4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')

def execute_sql(sql, params=None):
    """Execute SQL with proper error handling"""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        
        conn.commit()
        print(f"✓ SQL executed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def fix_user_model_schema():
    """Add missing profile fields to User table"""
    print("\n" + "=" * 80)
    print("1. FIXING USER MODEL SCHEMA")
    print("=" * 80)
    
    alterations = [
        # Avatar/Profile Picture
        """
        ALTER TABLE "user" 
        ADD COLUMN IF NOT EXISTS avatar VARCHAR(500),
        ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(500);
        """,
        
        # Subscription fields
        """
        ALTER TABLE "user" 
        ADD COLUMN IF NOT EXISTS subscription_plan VARCHAR(50) DEFAULT 'free',
        ADD COLUMN IF NOT EXISTS subscription_end_date TIMESTAMP,
        ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) DEFAULT 'active';
        """,
        
        # Password reset fields
        """
        ALTER TABLE "user" 
        ADD COLUMN IF NOT EXISTS reset_token VARCHAR(200),
        ADD COLUMN IF NOT EXISTS reset_token_expiry TIMESTAMP;
        """
    ]
    
    for sql in alterations:
        execute_sql(sql)
    
    print("✓ User model schema updated")

def create_profile_settings_table():
    """Create a dedicated profile settings table"""
    print("\n" + "=" * 80)
    print("2. CREATING PROFILE SETTINGS TABLE")
    print("=" * 80)
    
    sql = """
    CREATE TABLE IF NOT EXISTS profile_settings (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL UNIQUE,
        bio TEXT,
        phone VARCHAR(20),
        company VARCHAR(100),
        website VARCHAR(200),
        timezone VARCHAR(50) DEFAULT 'UTC',
        language VARCHAR(10) DEFAULT 'en',
        email_notifications BOOLEAN DEFAULT true,
        push_notifications BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
    );
    """
    
    execute_sql(sql)
    print("✓ Profile settings table created")

def fix_campaign_stats():
    """Add stats columns to campaigns if missing"""
    print("\n" + "=" * 80)
    print("3. FIXING CAMPAIGN STATS SCHEMA")
    print("=" * 80)
    
    sql = """
    ALTER TABLE campaign 
    ADD COLUMN IF NOT EXISTS clicks INTEGER DEFAULT 0,
    ADD COLUMN IF NOT EXISTS visitors INTEGER DEFAULT 0,
    ADD COLUMN IF NOT EXISTS conversions INTEGER DEFAULT 0,
    ADD COLUMN IF NOT EXISTS conversion_rate DECIMAL(5,2) DEFAULT 0.0;
    """
    
    execute_sql(sql)
    print("✓ Campaign stats schema updated")

def create_geography_data_table():
    """Create table for geography/atlas map data"""
    print("\n" + "=" * 80)
    print("4. CREATING GEOGRAPHY DATA TABLE")
    print("=" * 80)
    
    sql = """
    CREATE TABLE IF NOT EXISTS geography_data (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        country VARCHAR(100),
        country_code VARCHAR(10),
        city VARCHAR(100),
        latitude DECIMAL(10, 7),
        longitude DECIMAL(10, 7),
        clicks INTEGER DEFAULT 0,
        visitors INTEGER DEFAULT 0,
        last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
    );
    
    CREATE INDEX IF NOT EXISTS idx_geography_user ON geography_data(user_id);
    CREATE INDEX IF NOT EXISTS idx_geography_country ON geography_data(country_code);
    """
    
    execute_sql(sql)
    print("✓ Geography data table created")

def update_campaign_stats_from_tracking():
    """Update campaign statistics from tracking events"""
    print("\n" + "=" * 80)
    print("5. UPDATING CAMPAIGN STATISTICS")
    print("=" * 80)
    
    sql = """
    WITH campaign_stats AS (
        SELECT 
            c.id as campaign_id,
            COUNT(DISTINCT te.id) as total_clicks,
            COUNT(DISTINCT te.ip_address) as unique_visitors,
            0 as conversions
        FROM campaign c
        LEFT JOIN link l ON l.campaign = c.name
        LEFT JOIN tracking_event te ON te.link_id = l.id
        GROUP BY c.id
    )
    UPDATE campaign c
    SET 
        clicks = COALESCE(cs.total_clicks, 0),
        visitors = COALESCE(cs.unique_visitors, 0),
        conversions = COALESCE(cs.conversions, 0),
        conversion_rate = CASE 
            WHEN COALESCE(cs.total_clicks, 0) > 0 
            THEN (COALESCE(cs.conversions, 0)::DECIMAL / cs.total_clicks * 100)
            ELSE 0 
        END
    FROM campaign_stats cs
    WHERE c.id = cs.campaign_id;
    """
    
    execute_sql(sql)
    print("✓ Campaign statistics updated from tracking data")

def populate_geography_data():
    """Populate geography data from tracking events"""
    print("\n" + "=" * 80)
    print("6. POPULATING GEOGRAPHY DATA")
    print("=" * 80)
    
    sql = """
    INSERT INTO geography_data (user_id, country, country_code, city, latitude, longitude, clicks, visitors, last_visit)
    SELECT 
        l.user_id,
        te.country,
        te.country_code,
        te.city,
        te.latitude,
        te.longitude,
        COUNT(*) as clicks,
        COUNT(DISTINCT te.ip_address) as visitors,
        MAX(te.timestamp) as last_visit
    FROM tracking_event te
    JOIN link l ON l.id = te.link_id
    WHERE te.country IS NOT NULL
    GROUP BY l.user_id, te.country, te.country_code, te.city, te.latitude, te.longitude
    ON CONFLICT DO NOTHING;
    """
    
    execute_sql(sql)
    print("✓ Geography data populated from tracking events")

def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("MASTER COMPREHENSIVE FIX SCRIPT")
    print("Starting at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)
    
    try:
        # Step 1: Fix User Model
        fix_user_model_schema()
        
        # Step 2: Create Profile Settings Table
        create_profile_settings_table()
        
        # Step 3: Fix Campaign Stats
        fix_campaign_stats()
        
        # Step 4: Create Geography Data Table
        create_geography_data_table()
        
        # Step 5: Update Campaign Stats
        update_campaign_stats_from_tracking()
        
        # Step 6: Populate Geography Data
        populate_geography_data()
        
        print("\n" + "=" * 80)
        print("✓ ALL DATABASE FIXES COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
