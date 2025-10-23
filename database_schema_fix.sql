-- Fix Brain Link Tracker Database Schema
-- This script adds missing columns to existing tables

-- Add missing columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS notification_settings TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS preferences TEXT;

-- Ensure all required columns exist in users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS settings TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS user_metadata TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'member';
ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending';
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_ip VARCHAR(45);
ALTER TABLE users ADD COLUMN IF NOT EXISTS login_count INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS account_locked_until TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS plan_type VARCHAR(20) DEFAULT 'free';
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_expiry TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS daily_link_limit INTEGER DEFAULT 10;
ALTER TABLE users ADD COLUMN IF NOT EXISTS links_used_today INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_reset_date DATE DEFAULT CURRENT_DATE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS telegram_bot_token VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS telegram_chat_id VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS telegram_enabled BOOLEAN DEFAULT FALSE;

-- Update admin users to active status
UPDATE users SET status = 'active', is_active = TRUE, is_verified = TRUE 
WHERE username IN ('Brain', '7thbrain');
