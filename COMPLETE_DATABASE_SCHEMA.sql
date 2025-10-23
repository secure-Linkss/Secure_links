-- Complete Database Schema for Brain Link Tracker
-- Created: October 23, 2025
-- This file contains ALL tables needed for the application

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================================
-- USERS TABLE - Core user accounts
-- ================================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'member' CHECK (role IN ('main_admin', 'admin', 'member')),
    plan_type VARCHAR(50) DEFAULT 'free' CHECK (plan_type IN ('free', 'pro', 'enterprise')),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    subscription_status VARCHAR(50),
    subscription_start_date TIMESTAMP,
    subscription_end_date TIMESTAMP,
    phone VARCHAR(20),
    country VARCHAR(100),
    telegram_chat_id VARCHAR(255),
    telegram_enabled BOOLEAN DEFAULT false,
    two_factor_enabled BOOLEAN DEFAULT false,
    two_factor_secret VARCHAR(255),
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    failed_login_attempts INTEGER DEFAULT 0,
    last_failed_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_stripe_customer ON users(stripe_customer_id);

-- ================================================================
-- CAMPAIGNS TABLE - Marketing campaigns
-- ================================================================
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'archived')),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    budget DECIMAL(10, 2),
    total_clicks INTEGER DEFAULT 0,
    total_conversions INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5, 2) DEFAULT 0,
    revenue DECIMAL(10, 2) DEFAULT 0,
    cost_per_click DECIMAL(10, 4),
    roi DECIMAL(10, 2),
    tags TEXT[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_campaigns_user ON campaigns(user_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);

-- ================================================================
-- LINKS TABLE - Tracking links
-- ================================================================
CREATE TABLE IF NOT EXISTS links (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE SET NULL,
    original_url TEXT NOT NULL,
    short_code VARCHAR(50) UNIQUE NOT NULL,
    short_url TEXT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    tags TEXT[],
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP,
    click_limit INTEGER,
    click_count INTEGER DEFAULT 0,
    unique_clicks INTEGER DEFAULT 0,
    last_clicked_at TIMESTAMP,
    qr_code_url TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_links_user ON links(user_id);
CREATE INDEX IF NOT EXISTS idx_links_campaign ON links(campaign_id);
CREATE INDEX IF NOT EXISTS idx_links_short_code ON links(short_code);
CREATE INDEX IF NOT EXISTS idx_links_created_at ON links(created_at);

-- ================================================================
-- TRACKING_EVENTS TABLE - Click tracking data
-- ================================================================
CREATE TABLE IF NOT EXISTS tracking_events (
    id SERIAL PRIMARY KEY,
    link_id INTEGER REFERENCES links(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referer TEXT,
    country VARCHAR(100),
    country_code VARCHAR(10),
    city VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    device_type VARCHAR(50),
    device_brand VARCHAR(100),
    device_model VARCHAR(100),
    os VARCHAR(100),
    os_version VARCHAR(50),
    browser VARCHAR(100),
    browser_version VARCHAR(50),
    is_mobile BOOLEAN DEFAULT false,
    is_bot BOOLEAN DEFAULT false,
    is_unique BOOLEAN DEFAULT false,
    conversion_value DECIMAL(10, 2),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tracking_events_link ON tracking_events(link_id);
CREATE INDEX IF NOT EXISTS idx_tracking_events_user ON tracking_events(user_id);
CREATE INDEX IF NOT EXISTS idx_tracking_events_created_at ON tracking_events(created_at);
CREATE INDEX IF NOT EXISTS idx_tracking_events_country ON tracking_events(country);

-- ================================================================
-- NOTIFICATIONS TABLE - User notifications
-- ================================================================
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'info' CHECK (type IN ('info', 'success', 'warning', 'error')),
    priority VARCHAR(50) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    action_url TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

-- ================================================================
-- AUDIT_LOGS TABLE - Admin activity tracking
-- ================================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    target_type VARCHAR(100),
    target_id INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_actor ON audit_logs(actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_target ON audit_logs(target_type, target_id);

-- ================================================================
-- SECURITY_THREATS TABLE - Security monitoring
-- ================================================================
CREATE TABLE IF NOT EXISTS security_threats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    threat_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'resolved', 'false_positive')),
    ip_address VARCHAR(45),
    user_agent TEXT,
    description TEXT,
    resolution_notes TEXT,
    resolved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_security_threats_user ON security_threats(user_id);
CREATE INDEX IF NOT EXISTS idx_security_threats_status ON security_threats(status);
CREATE INDEX IF NOT EXISTS idx_security_threats_severity ON security_threats(severity);

-- ================================================================
-- BLOCKED_IPS TABLE - IP blocking
-- ================================================================
CREATE TABLE IF NOT EXISTS blocked_ips (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL UNIQUE,
    reason TEXT,
    blocked_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP,
    unblocked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_blocked_ips_address ON blocked_ips(ip_address);
CREATE INDEX IF NOT EXISTS idx_blocked_ips_active ON blocked_ips(is_active);

-- ================================================================
-- BLOCKED_COUNTRIES TABLE - Country blocking
-- ================================================================
CREATE TABLE IF NOT EXISTS blocked_countries (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(10) NOT NULL UNIQUE,
    country_name VARCHAR(100) NOT NULL,
    reason TEXT,
    blocked_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT true,
    unblocked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_blocked_countries_code ON blocked_countries(country_code);
CREATE INDEX IF NOT EXISTS idx_blocked_countries_active ON blocked_countries(is_active);

-- ================================================================
-- SUPPORT_TICKETS TABLE - Support system
-- ================================================================
CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'waiting_response', 'resolved', 'closed')),
    priority VARCHAR(50) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    category VARCHAR(100),
    tags TEXT[],
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_support_tickets_user ON support_tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_support_tickets_assigned ON support_tickets(assigned_to);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);

-- ================================================================
-- SUPPORT_TICKET_COMMENTS TABLE - Ticket replies
-- ================================================================
CREATE TABLE IF NOT EXISTS support_ticket_comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES support_tickets(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT false,
    attachments JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_ticket_comments_ticket ON support_ticket_comments(ticket_id);
CREATE INDEX IF NOT EXISTS idx_ticket_comments_user ON support_ticket_comments(user_id);

-- ================================================================
-- SUBSCRIPTION_VERIFICATIONS TABLE - Payment tracking
-- ================================================================
CREATE TABLE IF NOT EXISTS subscription_verifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    payment_method VARCHAR(50) NOT NULL CHECK (payment_method IN ('stripe', 'crypto')),
    plan_type VARCHAR(50) NOT NULL CHECK (plan_type IN ('pro', 'enterprise')),
    amount DECIMAL(10, 2),
    currency VARCHAR(10) DEFAULT 'USD',
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'rejected')),
    crypto_currency VARCHAR(20),
    crypto_tx_hash VARCHAR(255),
    crypto_wallet_address VARCHAR(255),
    payment_screenshot_url TEXT,
    stripe_payment_intent_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    confirmed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    confirmed_at TIMESTAMP,
    rejection_reason TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_subscription_verifications_user ON subscription_verifications(user_id);
CREATE INDEX IF NOT EXISTS idx_subscription_verifications_status ON subscription_verifications(status);

-- ================================================================
-- DOMAINS TABLE - Custom domain management
-- ================================================================
CREATE TABLE IF NOT EXISTS domains (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    domain_name VARCHAR(255) NOT NULL UNIQUE,
    is_verified BOOLEAN DEFAULT false,
    verification_token VARCHAR(255),
    dns_status VARCHAR(50) DEFAULT 'pending',
    ssl_status VARCHAR(50) DEFAULT 'pending',
    is_active BOOLEAN DEFAULT true,
    last_checked_at TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_domains_user ON domains(user_id);
CREATE INDEX IF NOT EXISTS idx_domains_name ON domains(domain_name);

-- ================================================================
-- SECURITY_SETTINGS TABLE - Security configuration
-- ================================================================
CREATE TABLE IF NOT EXISTS security_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    two_factor_enabled BOOLEAN DEFAULT false,
    two_factor_method VARCHAR(50) DEFAULT 'app',
    ip_whitelist TEXT[],
    login_alerts_enabled BOOLEAN DEFAULT true,
    session_timeout_minutes INTEGER DEFAULT 60,
    allowed_devices JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_security_settings_user ON security_settings(user_id);

-- ================================================================
-- ADMIN_SETTINGS TABLE - System configuration
-- ================================================================
CREATE TABLE IF NOT EXISTS admin_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    setting_type VARCHAR(50) DEFAULT 'string',
    description TEXT,
    is_public BOOLEAN DEFAULT false,
    updated_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_admin_settings_key ON admin_settings(setting_key);

-- ================================================================
-- PAYMENT_HISTORY TABLE - Payment records
-- ================================================================
CREATE TABLE IF NOT EXISTS payment_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    status VARCHAR(50) NOT NULL,
    plan_type VARCHAR(50),
    stripe_payment_intent_id VARCHAR(255),
    stripe_invoice_id VARCHAR(255),
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payment_history_user ON payment_history(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_history_created_at ON payment_history(created_at);

-- ================================================================
-- CRYPTO_WALLET_ADDRESSES TABLE - Admin crypto wallets
-- ================================================================
CREATE TABLE IF NOT EXISTS crypto_wallet_addresses (
    id SERIAL PRIMARY KEY,
    cryptocurrency VARCHAR(20) NOT NULL UNIQUE,
    wallet_address VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    updated_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================
-- BROADCAST_MESSAGES TABLE - Global messages
-- ================================================================
CREATE TABLE IF NOT EXISTS broadcast_messages (
    id SERIAL PRIMARY KEY,
    sent_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'info',
    priority VARCHAR(50) DEFAULT 'medium',
    recipient_count INTEGER DEFAULT 0,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_broadcast_messages_sent_by ON broadcast_messages(sent_by);
CREATE INDEX IF NOT EXISTS idx_broadcast_messages_sent_at ON broadcast_messages(sent_at);

-- ================================================================
-- INSERT DEFAULT DATA
-- ================================================================

-- Insert crypto wallet placeholders
INSERT INTO crypto_wallet_addresses (cryptocurrency, wallet_address, is_active) VALUES
('BTC', 'Configure in Admin Panel', false),
('ETH', 'Configure in Admin Panel', false),
('LTC', 'Configure in Admin Panel', false),
('USDT', 'Configure in Admin Panel', false)
ON CONFLICT (cryptocurrency) DO NOTHING;

-- Insert default admin settings
INSERT INTO admin_settings (setting_key, setting_value, setting_type, description, is_public) VALUES
('site_name', 'Brain Link Tracker', 'string', 'Application name', true),
('maintenance_mode', 'false', 'boolean', 'Maintenance mode status', false),
('max_links_per_user', '1000', 'integer', 'Maximum links per user', false),
('session_timeout', '3600', 'integer', 'Session timeout in seconds', false)
ON CONFLICT (setting_key) DO NOTHING;

-- ================================================================
-- TRIGGERS FOR UPDATED_AT
-- ================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
DO $$
DECLARE
    t text;
BEGIN
    FOR t IN
        SELECT table_name
        FROM information_schema.columns
        WHERE column_name = 'updated_at'
        AND table_schema = 'public'
    LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS update_%I_updated_at ON %I', t, t);
        EXECUTE format('
            CREATE TRIGGER update_%I_updated_at
            BEFORE UPDATE ON %I
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column()', t, t);
    END LOOP;
END;
$$;

-- ================================================================
-- DATABASE VIEWS FOR REPORTING
-- ================================================================

-- User statistics view
CREATE OR REPLACE VIEW user_statistics AS
SELECT
    u.id,
    u.username,
    u.email,
    u.role,
    u.plan_type,
    COUNT(DISTINCT l.id) as total_links,
    COUNT(DISTINCT c.id) as total_campaigns,
    COUNT(DISTINCT te.id) as total_clicks,
    u.created_at as user_since
FROM users u
LEFT JOIN links l ON u.id = l.user_id
LEFT JOIN campaigns c ON u.id = c.user_id
LEFT JOIN tracking_events te ON l.id = te.link_id
GROUP BY u.id;

-- Campaign performance view
CREATE OR REPLACE VIEW campaign_performance AS
SELECT
    c.id,
    c.name,
    c.user_id,
    c.status,
    COUNT(DISTINCT l.id) as link_count,
    SUM(l.click_count) as total_clicks,
    c.budget,
    c.revenue,
    c.roi,
    c.created_at
FROM campaigns c
LEFT JOIN links l ON c.id = l.campaign_id
GROUP BY c.id;

-- Security dashboard view
CREATE OR REPLACE VIEW security_dashboard AS
SELECT
    COUNT(*) FILTER (WHERE status = 'active') as active_threats,
    COUNT(*) FILTER (WHERE status = 'resolved') as resolved_threats,
    COUNT(*) FILTER (WHERE severity = 'critical') as critical_threats,
    COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '24 hours') as threats_today,
    (SELECT COUNT(*) FROM blocked_ips WHERE is_active = true) as blocked_ips_count,
    (SELECT COUNT(*) FROM blocked_countries WHERE is_active = true) as blocked_countries_count
FROM security_threats;

-- ================================================================
-- COMPLETION MESSAGE
-- ================================================================

DO $$
BEGIN
    RAISE NOTICE '=================================================================';
    RAISE NOTICE 'Brain Link Tracker - Complete Database Schema';
    RAISE NOTICE 'All tables, indexes, triggers, and views created successfully!';
    RAISE NOTICE '=================================================================';
END $$;
