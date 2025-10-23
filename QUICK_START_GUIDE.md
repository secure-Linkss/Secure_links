# Brain Link Tracker - Quick Start Guide

## 🚀 Getting Started in 3 Minutes

### Prerequisites
- Node.js 18+ installed
- Python 3.9+ installed
- PostgreSQL database (Neon, Supabase, or local)

---

## ⚡ Quick Setup

### 1. Clone & Install (1 minute)

```bash
git clone https://github.com/secure-Linkss/bol.new.git
cd bol.new

# Install all dependencies
pip install -r requirements.txt
npm install
```

### 2. Configure Environment (30 seconds)

```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your values (already pre-filled for you)
# DATABASE_URL, SECRET_KEY, SHORTIO_API_KEY are already set
```

### 3. Deploy & Run (1 minute)

**Option A: Automated (Recommended)**
```bash
./deploy_complete.sh
```

**Option B: Manual**
```bash
# Initialize database
python3 -c "from src.main import app, db; app.app_context().push(); db.create_all()"

# Build frontend
npm run build

# Start server
python3 src/main.py
```

### 4. Access the Application

Open your browser: `http://localhost:5000`

**Default Login:**
- Username: `Brain`
- Password: `Mayflower1!!`

⚠️ Change password after first login!

---

## 🎯 Key Features Available

### 1. Dashboard
- Real-time analytics overview
- Performance metrics
- Quick stats

### 2. Tracking Links
- Create short tracking links
- Quantum redirect system
- Campaign association

### 3. Live Activity
- Real-time event monitoring
- Visitor tracking
- Bot detection

### 4. Analytics (NEW!)
- 7 compact metric cards
- Performance trend charts
- Device breakdown
- Geographic distribution
- Campaign performance

### 5. Geography (NEW!)
- Interactive world map
- Country heat mapping
- City-level tracking
- Top countries list

### 6. Security (NEW!)
- Threat monitoring
- IP activity logs
- Blocked IPs management
- Security event timeline

### 7. Campaign (NEW!)
- Create & manage campaigns
- Track performance
- Conversion analytics
- Status management

### 8. Settings (NEW!)
- Profile management
- Password change
- Notification preferences
- App preferences

### 9. Link Shortener
- Quick link creation
- Custom short codes
- URL shortening

### Admin Panel (Admin Only)
- User management
- System analytics
- Campaign overview
- Security settings

---

## 📱 Mobile Access

All components are fully responsive! Access from:
- Desktop browsers
- Tablets
- Mobile phones

---

## 🔐 Security Features

1. **User Data Isolation**
   - Each user sees only their own data
   - Admins see personal data in main tabs
   - System-wide data in admin sub-tabs

2. **Authentication**
   - JWT token-based
   - Secure session management
   - Password hashing with Werkzeug

3. **Threat Detection**
   - Bot detection
   - Suspicious activity monitoring
   - IP blocking

---

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "Database connection error"
Check `.env` file:
```bash
# Verify DATABASE_URL is correct
cat .env | grep DATABASE_URL
```

### Issue: "Port already in use"
```bash
# Use different port
FLASK_PORT=5001 python3 src/main.py
```

### Issue: "Frontend not loading"
```bash
# Rebuild frontend
npm run build
```

---

## 📊 Verification

Check if everything is working:

```bash
python3 verify_completion.py
```

Expected output: **42/42 tests passing (100%)**

---

## 🌐 Deployment to Vercel

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel --prod
```

### Step 4: Set Environment Variables
In Vercel Dashboard → Settings → Environment Variables:
- `DATABASE_URL`
- `SECRET_KEY`
- `SHORTIO_API_KEY`
- `SHORTIO_DOMAIN`

---

## 📚 API Endpoints

### Analytics
```
GET /api/analytics/overview?period=7
GET /api/analytics/geography?period=7
```

### Security
```
GET /api/security/logs?period=7
```

### User Settings
```
GET /api/user/settings
PUT /api/user/profile
PUT /api/user/password
PUT /api/user/notifications
```

### Campaigns
```
GET /api/campaigns
POST /api/campaigns
```

---

## 💡 Tips & Tricks

1. **Performance Optimization**
   - Use period=1 for last 24 hours (faster)
   - Use period=30 for monthly data

2. **Mobile Usage**
   - All charts are touch-friendly
   - Swipe to navigate on mobile
   - Pinch to zoom on maps

3. **Keyboard Shortcuts**
   - Refresh data: F5 or Ctrl+R
   - Navigate tabs: Arrow keys (when focused)

4. **Data Export**
   - Click "Export" button in Analytics, Geography, Security, Campaign
   - Downloads as CSV file

---

## 🎓 Learning Resources

### Documentation
- `COMPLETION_REPORT.md` - Full project documentation
- `README.md` - Project overview
- `.env.example` - Environment variables guide

### Code Structure
```
src/
├── components/        # Frontend React components
├── routes/           # Backend API routes
├── models/           # Database models
└── main.py           # Main Flask application
```

---

## 🆘 Support

### For Issues:
1. Run verification: `python3 verify_completion.py`
2. Check logs in console
3. Review `.env` configuration
4. Check database connection

### For Questions:
- Review `COMPLETION_REPORT.md`
- Check API documentation above
- Verify environment variables

---

## ✅ Checklist

Before going live:

- [ ] Environment variables configured
- [ ] Database initialized
- [ ] Admin password changed
- [ ] Frontend built
- [ ] Verification passing (42/42)
- [ ] Tested on desktop
- [ ] Tested on mobile
- [ ] SSL certificate configured (production)
- [ ] Backup strategy in place
- [ ] Monitoring setup (optional)

---

## 🎉 You're All Set!

Your Brain Link Tracker is now ready for production use!

**Next Steps:**
1. Login and change admin password
2. Create your first tracking link
3. Monitor real-time activity
4. Explore analytics and insights

**Happy Tracking!** 🚀

---

*Last Updated: October 21, 2025*
*Version: 2.0.0 - Quantum Intelligence Release*
