
-- Comprehensive Database Schema Fix
-- This script ensures all required tables and columns exist

-- User table enhancements
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_tier VARCHAR(50) DEFAULT 'free';
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_expires_at TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS login_count INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS api_key VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
ALTER TABLE users ADD COLUMN IF NOT EXISTS country VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS timezone VARCHAR(100);

-- Links table enhancements
ALTER TABLE links ADD COLUMN IF NOT EXISTS qr_code_url VARCHAR(500);
ALTER TABLE links ADD COLUMN IF NOT EXISTS password VARCHAR(255);
ALTER TABLE links ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP;
ALTER TABLE links ADD COLUMN IF NOT EXISTS max_clicks INTEGER;
ALTER TABLE links ADD COLUMN IF NOT EXISTS tags TEXT;
ALTER TABLE links ADD COLUMN IF NOT EXISTS custom_domain_id INTEGER;
ALTER TABLE links ADD COLUMN IF NOT EXISTS utm_source VARCHAR(255);
ALTER TABLE links ADD COLUMN IF NOT EXISTS utm_medium VARCHAR(255);
ALTER TABLE links ADD COLUMN IF NOT EXISTS utm_campaign VARCHAR(255);

-- Campaigns table enhancements
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS budget DECIMAL(10,2);
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS spent DECIMAL(10,2) DEFAULT 0;
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS target_audience TEXT;
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS conversion_goal VARCHAR(100);
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS start_date TIMESTAMP;
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS end_date TIMESTAMP;

-- Tracking events table enhancements
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS country VARCHAR(100);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS city VARCHAR(100);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS device_type VARCHAR(50);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS browser VARCHAR(100);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS os VARCHAR(100);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS referrer_domain VARCHAR(255);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS session_id VARCHAR(255);
ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS conversion_value DECIMAL(10,2);

-- Audit logs table enhancements
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45);
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS user_agent TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS request_method VARCHAR(10);
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS request_url VARCHAR(500);
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS response_status INTEGER;

-- Security settings table enhancements
ALTER TABLE security_settings ADD COLUMN IF NOT EXISTS max_login_attempts INTEGER DEFAULT 5;
ALTER TABLE security_settings ADD COLUMN IF NOT EXISTS lockout_duration INTEGER DEFAULT 900;
ALTER TABLE security_settings ADD COLUMN IF NOT EXISTS password_min_length INTEGER DEFAULT 8;
ALTER TABLE security_settings ADD COLUMN IF NOT EXISTS require_2fa BOOLEAN DEFAULT FALSE;
ALTER TABLE security_settings ADD COLUMN IF NOT EXISTS allowed_countries TEXT;
ALTER TABLE security_settings ADD COLUMN IF NOT EXISTS blocked_user_agents TEXT;

-- Notifications table enhancements
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS notification_type VARCHAR(50) DEFAULT 'info';
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 1;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS action_url VARCHAR(500);
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS metadata JSON;

-- Domains table enhancements
ALTER TABLE domains ADD COLUMN IF NOT EXISTS ssl_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE domains ADD COLUMN IF NOT EXISTS ssl_expires_at TIMESTAMP;
ALTER TABLE domains ADD COLUMN IF NOT EXISTS dns_records JSON;
ALTER TABLE domains ADD COLUMN IF NOT EXISTS verification_token VARCHAR(255);
ALTER TABLE domains ADD COLUMN IF NOT EXISTS last_verified_at TIMESTAMP;

-- Support tickets table enhancements
ALTER TABLE support_tickets ADD COLUMN IF NOT EXISTS attachment_url VARCHAR(500);
ALTER TABLE support_tickets ADD COLUMN IF NOT EXISTS estimated_resolution TIMESTAMP;
ALTER TABLE support_tickets ADD COLUMN IF NOT EXISTS satisfaction_rating INTEGER;
ALTER TABLE support_tickets ADD COLUMN IF NOT EXISTS resolution_notes TEXT;
ALTER TABLE support_tickets ADD COLUMN IF NOT EXISTS escalated_at TIMESTAMP;

-- Create missing indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id);
CREATE INDEX IF NOT EXISTS idx_links_short_code ON links(short_code);
CREATE INDEX IF NOT EXISTS idx_links_created_at ON links(created_at);
CREATE INDEX IF NOT EXISTS idx_tracking_events_link_id ON tracking_events(link_id);
CREATE INDEX IF NOT EXISTS idx_tracking_events_timestamp ON tracking_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);

-- Create missing tables if they don't exist
CREATE TABLE IF NOT EXISTS payment_methods (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_payment_method_id VARCHAR(255) NOT NULL,
    card_last4 VARCHAR(4),
    card_brand VARCHAR(50),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscription_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_tier VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    stripe_subscription_id VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_usage (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    response_status INTEGER,
    response_time_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS link_analytics (
    id SERIAL PRIMARY KEY,
    link_id INTEGER NOT NULL REFERENCES links(id) ON DELETE CASCADE,
    date_recorded DATE NOT NULL,
    clicks INTEGER DEFAULT 0,
    unique_clicks INTEGER DEFAULT 0,
    top_country VARCHAR(100),
    top_referrer VARCHAR(255),
    conversion_rate DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(link_id, date_recorded)
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2) NOT NULL,
    metric_unit VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default system settings if not exists
INSERT INTO security_settings (id, user_id, enable_2fa, block_suspicious_ips, enable_rate_limiting, max_login_attempts, lockout_duration)
SELECT 1, 1, FALSE, TRUE, TRUE, 5, 900
WHERE NOT EXISTS (SELECT 1 FROM security_settings WHERE id = 1);
