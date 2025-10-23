-- Comprehensive Database Migration for Brain Link Tracker
-- This script adds all missing columns to existing tables

-- Add missing columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar VARCHAR(500);
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(500);
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expiry TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_plan VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(50) DEFAULT 'active';
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_end_date TIMESTAMP;

-- Ensure all tracking_event fields exist
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_click_id VARCHAR(255);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_stage VARCHAR(50);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_processing_time FLOAT;
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_security_violation VARCHAR(100);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_final_url TEXT;
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_error TEXT;
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS quantum_security_score INTEGER;
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS is_verified_human BOOLEAN DEFAULT FALSE;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_tracking_events_user_id ON tracking_events(link_id);
CREATE INDEX IF NOT EXISTS idx_tracking_events_timestamp ON tracking_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_tracking_events_status ON tracking_events(status);
CREATE INDEX IF NOT EXISTS idx_tracking_events_lat_lng ON tracking_events(latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id);
CREATE INDEX IF NOT EXISTS idx_links_campaign_name ON links(campaign_name);
CREATE INDEX IF NOT EXISTS idx_campaigns_owner_id ON campaigns(owner_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(user_id, read);

-- Grant permissions (if needed for PostgreSQL)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO neondb_owner;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO neondb_owner;
