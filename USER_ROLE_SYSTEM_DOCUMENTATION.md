# User Role System Documentation

## Overview
This document provides a comprehensive guide to the three-tier user role system implemented in the Brain Link Tracker SaaS application.

## Role Hierarchy

### 1. Main Admin (Superuser)
- **Role Value:** `main_admin`
- **Access Level:** Full system access
- **Capabilities:** All features across the entire platform
- **Tab Access:** All 12 tabs (Tabs 1-11 + exclusive Main Admin tabs)

### 2. Admin
- **Role Value:** `admin`
- **Access Level:** Administrative access with some restrictions
- **Capabilities:** Most administrative features except Main Admin exclusives
- **Tab Access:** 11 tabs (Tabs 1-11, excluding Main Admin-only tabs)

### 3. Member (User)
- **Role Value:** `member`
- **Access Level:** Standard user access
- **Capabilities:** Core application features
- **Tab Access:** 11 tabs (Tabs 1-11, no Admin Panel access)

---

## Tab Structure (11 Main Tabs)

### Tabs 1-11: Available to All Users

1. **Dashboard** (Badge: 1)
   - Path: `/dashboard`
   - Icon: LayoutDashboard
   - Description: Overview of user activity and metrics

2. **Tracking Links** (Badge: 2)
   - Path: `/tracking-links`
   - Icon: Link2
   - Description: Manage and monitor tracking links

3. **Live Activity** (Badge: 3)
   - Path: `/live-activity`
   - Icon: Activity
   - Description: Real-time activity monitoring

4. **Campaign** (Badge: 4)
   - Path: `/campaign`
   - Icon: Target
   - Description: Campaign management and tracking

5. **Analytics** (Badge: 5)
   - Path: `/analytics`
   - Icon: BarChart3
   - Description: Detailed analytics and reporting

6. **Geography** (Badge: 6)
   - Path: `/geography`
   - Icon: Globe
   - Description: Geographic data visualization

7. **Security** (Badge: 7)
   - Path: `/security`
   - Icon: Shield
   - Description: Security monitoring and settings

8. **Settings** (Badge: 8)
   - Path: `/settings`
   - Icon: Settings
   - Description: User account and application settings

9. **Link Shortener** (Badge: 9)
   - Path: `/link-shortener`
   - Icon: Scissors
   - Description: URL shortening service

10. **Notifications** (Badge: 10 or dynamic count)
    - Path: `/notifications`
    - Icon: Bell
    - Description: System notifications and alerts

11. **Admin Panel** (Badge: 11)
    - Path: `/admin-panel`
    - Icon: User
    - Description: Administrative control panel
    - **Access:** Admin and Main Admin only

---

## Admin Panel Internal Tabs

The Admin Panel (Tab 11) contains multiple sub-tabs with varying access levels:

### Standard Admin Tabs (Admin + Main Admin Access)

1. **Dashboard**
   - Overview statistics for all system entities
   - Real-time metrics: users, campaigns, links, clicks

2. **Users**
   - User management
   - Create, read, update, delete users
   - View user details and activity

3. **Campaigns**
   - Campaign management and monitoring
   - View campaign statistics and associated links
   - Live data from Campaign table and campaign_name fields

4. **Security**
   - Security threat monitoring
   - View and resolve security incidents
   - Access security threat database

5. **Subscriptions**
   - Subscription management
   - View and modify user subscription plans
   - Extend subscription periods

6. **Support**
   - Support ticket system
   - View, assign, and resolve tickets
   - Customer support management

7. **Settings**
   - Domain management
   - System configuration
   - General administrative settings

8. **Pending Users** (NEW)
   - Review user registration requests
   - Approve or reject pending users
   - **Access:** Admin and Main Admin only

9. **Global Broadcaster** (NEW)
   - Send system-wide messages to all users
   - Create broadcast notifications
   - Set message priority and type
   - **Access:** Admin and Main Admin only

### Main Admin Exclusive Tabs

10. **Audit** (Main Admin Only)
    - Complete audit log access
    - Export audit logs to CSV
    - View all administrative actions

11. **Crypto Payments** (NEW - Main Admin Only)
    - Cryptocurrency payment integration
    - Configure Bitcoin, Ethereum, USDT gateways
    - Manage payment processors
    - **Access:** Main Admin only

12. **Telegram Integration** (NEW - Main Admin Only)
    - Configure Telegram bot integrations
    - Notification Bot for system alerts
    - Support Bot for customer inquiries
    - **Access:** Main Admin only

---

## Role-Based Access Control Implementation

### Frontend (React)

#### Layout Component (`src/components/Layout.jsx`)
- Displays navigation menu items
- Shows Admin Panel only for `admin` and `main_admin` roles
- Badge numbers correctly reflect tab positions (1-11)

```jsx
{user && (user.role === "admin" || user.role === "main_admin") && (
  <Route path="/admin-panel" element={<AdminPanelComplete />} />
)}
```

#### Admin Panel Component (`src/components/AdminPanelComplete.jsx`)
- Retrieves user role from localStorage
- Conditional rendering based on role:
  - `isMainAdmin`: Checks if role is `main_admin`
  - `isAdmin`: Checks if role is `admin` or `main_admin`
- Tabs dynamically shown/hidden based on permissions

```jsx
const isMainAdmin = currentUser?.role === 'main_admin';
const isAdmin = currentUser?.role === 'admin' || currentUser?.role === 'main_admin';

{isMainAdmin && (
  <TabsTrigger value="crypto">Crypto Payments</TabsTrigger>
)}
```

### Backend (Flask/Python)

#### Decorators (`src/routes/admin_complete.py`, `src/routes/admin.py`)

**Admin Required Decorator:**
```python
@admin_required
def admin_function(current_user):
    # Requires role = 'admin' or 'main_admin'
```

**Main Admin Required Decorator:**
```python
@main_admin_required
def main_admin_function(current_user):
    # Requires role = 'main_admin' only
```

#### User Model (`src/models/user.py`)
```python
role = db.Column(db.String(20), default='member')  # member, admin, main_admin
status = db.Column(db.String(20), default='pending')  # pending, active, suspended, expired
```

---

## Database Schema

### Users Table
| Column | Type | Default | Description |
|--------|------|---------|-------------|
| `id` | Integer | Auto | Primary key |
| `username` | String(80) | - | Unique username |
| `email` | String(120) | - | Unique email |
| `password_hash` | String(255) | - | Hashed password |
| `role` | String(20) | `'member'` | User role (member/admin/main_admin) |
| `status` | String(20) | `'pending'` | Account status (pending/active/suspended/expired) |
| `is_active` | Boolean | `True` | Account active flag |
| `is_verified` | Boolean | `False` | Email verification status |
| `plan_type` | String(20) | `'free'` | Subscription plan (free/pro/enterprise) |
| `created_at` | DateTime | `utcnow()` | Account creation timestamp |

### Supporting Tables
- **Notifications** - User notifications and alerts
- **Audit Logs** - Administrative action tracking
- **Support Tickets** - Customer support system
- **Security Threats** - Security monitoring database
- **Campaigns** - Marketing campaign data
- **Links** - Tracking link management
- **Domains** - Custom domain configuration
- **Tracking Events** - Click and interaction tracking

---

## User Registration Flow

1. **Registration**
   - New user registers via `/api/auth/register`
   - User created with `role='member'` and `status='pending'`
   - `is_active=False` until approved

2. **Admin Approval** (NEW)
   - Admin views pending users in **Pending Users** tab
   - Admin can approve or reject registration
   - Upon approval: `status='active'`, `is_active=True`

3. **Login**
   - User logs in via `/api/auth/login`
   - System checks:
     - Password validity
     - Status is not `pending`, `suspended`, or `expired`
     - `is_active` is `True`
   - JWT token generated for session

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info
- `GET /api/auth/validate` - Validate JWT token

### Admin Endpoints (Admin + Main Admin)
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/users` - List all users
- `POST /api/admin/users` - Create new user
- `GET /api/admin/campaigns` - List all campaigns
- `GET /api/admin/security/threats` - Security threats
- `GET /api/admin/subscriptions` - User subscriptions
- `GET /api/admin/support/tickets` - Support tickets
- `GET /api/admin/domains` - Domain management

### Main Admin Exclusive Endpoints
- `GET /api/admin/audit-logs` - Audit log access (Main Admin only)
- `GET /api/admin/audit-logs/export` - Export audit logs (Main Admin only)
- `POST /api/admin/system/delete-all` - Delete all system data (Main Admin only)

---

## Security Features

### Authentication
- JWT token-based authentication
- Token expiration: 30 days
- Session management via localStorage
- Automatic token validation on app load

### Authorization
- Role-based access control (RBAC)
- Decorator-based endpoint protection
- Frontend conditional rendering
- Backend permission validation

### Audit Logging
- All admin actions logged
- Actor tracking (user who performed action)
- Action details and timestamps
- IP address and user agent recording

### Account Security
- Failed login attempt tracking
- Account locking mechanism
- Password hashing (Werkzeug)
- Status-based access control

---

## Frontend State Management

### User Context
- Stored in `localStorage` as `user` JSON object
- Retrieved on app initialization
- Contains: id, username, email, role, status, plan_type

### Token Management
- Stored in `localStorage` as `token`
- Included in Authorization header for API requests
- Format: `Bearer <token>`
- Validated on page reload

### Role Checks
```javascript
const currentUser = JSON.parse(localStorage.getItem('user'));
const isMainAdmin = currentUser?.role === 'main_admin';
const isAdmin = currentUser?.role === 'admin' || currentUser?.role === 'main_admin';
const isMember = currentUser?.role === 'member';
```

---

## Best Practices

### For Administrators

1. **User Management**
   - Review pending users regularly
   - Verify user information before approval
   - Monitor user activity via audit logs

2. **Security**
   - Review security threats regularly
   - Resolve incidents promptly
   - Monitor failed login attempts

3. **Communication**
   - Use Global Broadcaster for system-wide announcements
   - Maintain Telegram bot configurations
   - Respond to support tickets promptly

### For Main Admins

1. **System Administration**
   - Regular audit log reviews
   - Backup critical data before system operations
   - Configure payment gateways carefully
   - Test Telegram integrations thoroughly

2. **Access Control**
   - Grant admin privileges judiciously
   - Review admin actions via audit logs
   - Maintain separation of duties

---

## Troubleshooting

### User Cannot Login
- Check `status` field: must be `'active'`
- Check `is_active` field: must be `True`
- Verify password is correct
- Check for account lock (`account_locked_until`)

### Admin Cannot Access Certain Tabs
- Verify user role in database
- Check JWT token validity
- Ensure frontend retrieves correct user data
- Clear localStorage and re-login

### Pending Users Not Showing
- Ensure users have `status='pending'`
- Check admin has proper role (`admin` or `main_admin`)
- Verify `/api/admin/users` endpoint returns all users

---

## Summary

The Brain Link Tracker SaaS application implements a robust three-tier role system:

- **11 Core Tabs (1-11)**: Accessible by all users (Members see 10, Admins see 11)
- **Admin Panel (Tab 11)**: Contains 12 internal administrative tabs
- **Role-Based Access**: Main Admin (12 admin tabs), Admin (9 admin tabs), Member (no admin access)
- **New Features Added**:
  - Pending Users approval system
  - Global Broadcaster for system-wide messaging
  - Crypto Payment Integration (Main Admin only)
  - Telegram Bot Integration (Main Admin only)

All role checks are enforced on both frontend (conditional rendering) and backend (decorators), ensuring security and proper access control throughout the application.
