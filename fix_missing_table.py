#!/usr/bin/env python3
"""
Fix missing database table: subscription_verification
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

def create_missing_table():
    """Create the missing subscription_verification table"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Create subscription_verification table if it doesn't exist
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS subscription_verification (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            subscription_type VARCHAR(50) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            verification_token VARCHAR(255) UNIQUE,
            payment_method VARCHAR(50),
            amount DECIMAL(10, 2),
            currency VARCHAR(3) DEFAULT 'USD',
            stripe_subscription_id VARCHAR(255),
            verified_at TIMESTAMP,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSONB DEFAULT '{}'::jsonb
        );
        
        CREATE INDEX IF NOT EXISTS idx_subscription_verification_user_id ON subscription_verification(user_id);
        CREATE INDEX IF NOT EXISTS idx_subscription_verification_status ON subscription_verification(status);
        CREATE INDEX IF NOT EXISTS idx_subscription_verification_token ON subscription_verification(verification_token);
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Successfully created subscription_verification table")
        
        # Insert some sample data
        sample_data_sql = """
        INSERT INTO subscription_verification (user_id, subscription_type, status, verification_token, payment_method, amount, currency) 
        VALUES 
            (1, 'premium', 'active', 'ver_token_001', 'stripe', 29.99, 'USD'),
            (2, 'pro', 'pending', 'ver_token_002', 'paypal', 49.99, 'USD')
        ON CONFLICT (verification_token) DO NOTHING;
        """
        
        cursor.execute(sample_data_sql)
        conn.commit()
        print("✅ Added sample subscription verification data")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating subscription_verification table: {str(e)}")
        return False

if __name__ == "__main__":
    create_missing_table()