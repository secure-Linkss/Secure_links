# 🚀 Brain Link Tracker - Deployment Guide

## Quick Deployment to Vercel

### Prerequisites
- GitHub repository: https://github.com/secure-Linkss/bol.new
- Vercel account
- Environment variables ready

---

## Step 1: Connect Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import from GitHub: `secure-Linkss/bol.new`
4. Select the repository

---

## Step 2: Configure Environment Variables

In the Vercel project settings, add these environment variables:

### Required Variables

```bash
SECRET_KEY=ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE
DATABASE_URL=postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SHORTIO_API_KEY=sk_DbGGlUHPN7Z9VotL
SHORTIO_DOMAIN=Secure-links.short.gy
FLASK_ENV=production
NODE_ENV=production
```

### How to Add Variables in Vercel:
1. Go to Project Settings
2. Click "Environment Variables"
3. Add each variable:
   - Name: `SECRET_KEY`
   - Value: `ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE`
   - Environment: Production, Preview, Development
4. Repeat for all variables

---

## Step 3: Build Configuration

Vercel should auto-detect the configuration from `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/t/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/q/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/dist/$1"
    }
  ]
}
```

### Manual Configuration (if needed):
- **Framework Preset**: Other
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

---

## Step 4: Deploy

1. Click "Deploy"
2. Wait for build to complete (2-3 minutes)
3. Vercel will provide a deployment URL

---

## Step 5: Verify Deployment

### Check These Endpoints:

1. **Homepage**: `https://your-deployment.vercel.app/`
   - Should load the login page

2. **API Health**: `https://your-deployment.vercel.app/api/health`
   - Should return status

3. **Static Assets**: Check if CSS and JS load correctly

### Test Login:
- Username: `Brain`
- Password: `Mayflower1!!`

Or:
- Username: `7thbrain`
- Password: `Mayflower1!`

---

## Step 6: Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Wait for SSL certificate provisioning

---

## Database Verification

The PostgreSQL database is hosted on Neon:
- **Host**: `ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech`
- **Database**: `neondb`
- **SSL**: Required

### Tables Created Automatically:
- `users`
- `links`
- `tracking_events`
- `campaigns`
- `audit_logs`
- `security_settings`
- `blocked_ips`
- `blocked_countries`
- `notifications`
- `domains`
- And more...

### Default Admin Users:
1. **Main Admin**
   - Username: `Brain`
   - Email: `admin@brainlinktracker.com`
   - Password: `Mayflower1!!`
   - Role: `main_admin`

2. **Admin**
   - Username: `7thbrain`
   - Email: `admin2@brainlinktracker.com`
   - Password: `Mayflower1!`
   - Role: `admin`

---

## Troubleshooting

### Build Fails
- Check environment variables are set
- Verify all dependencies in `package.json`
- Check Python dependencies in `requirements.txt`

### 500 Server Error
- Check DATABASE_URL is correct
- Verify database is accessible
- Check application logs in Vercel

### Frontend Not Loading
- Verify build command ran successfully
- Check `dist` folder was created
- Verify static file routing in `vercel.json`

### API Routes Not Working
- Check `/api/` prefix in routes
- Verify Flask app is starting
- Check Python runtime is correct

---

## Monitoring

### Vercel Dashboard
- **Deployments**: View all deployments
- **Analytics**: Track usage
- **Logs**: View runtime logs
- **Insights**: Performance metrics

### Database Monitoring
1. Go to [Neon Dashboard](https://console.neon.tech/)
2. Select your project
3. Monitor:
   - Connection count
   - Query performance
   - Storage usage

---

## Maintenance

### Update Deployment
```bash
git push origin master
```
Vercel automatically deploys on push to master.

### Rollback Deployment
1. Go to Vercel Dashboard
2. Select previous deployment
3. Click "Promote to Production"

### Update Environment Variables
1. Go to Project Settings → Environment Variables
2. Edit or add variables
3. Redeploy to apply changes

---

## Security Checklist

- ✅ Environment variables set correctly
- ✅ Database SSL enabled
- ✅ SECRET_KEY is strong and random
- ✅ Admin passwords are secure
- ✅ API routes are authenticated
- ✅ CORS configured properly
- ✅ Session cookies are secure

---

## Performance Optimization

### Frontend
- ✅ Vite build optimization enabled
- ✅ CSS purging active
- ✅ Components lazy-loaded where appropriate
- ✅ Images optimized

### Backend
- ✅ Database query optimization
- ✅ Connection pooling enabled
- ✅ Efficient data filtering
- ✅ Caching where appropriate

---

## Support Resources

### Documentation
- [Vercel Docs](https://vercel.com/docs)
- [Flask Docs](https://flask.palletsprojects.com/)
- [React Docs](https://react.dev/)
- [Neon Docs](https://neon.tech/docs)

### Repository
- **GitHub**: https://github.com/secure-Linkss/bol.new
- **Issues**: Report bugs via GitHub Issues

---

## Post-Deployment Checklist

- [ ] Deployment successful
- [ ] All pages load correctly
- [ ] Login works
- [ ] Dashboard displays data
- [ ] Analytics loads
- [ ] Geography tab works
- [ ] Security tab functional
- [ ] Campaign management operational
- [ ] Settings save correctly
- [ ] Export features work
- [ ] Mobile responsive on all pages
- [ ] No console errors
- [ ] Database connection stable
- [ ] Environment variables set
- [ ] Custom domain configured (if applicable)

---

## Quick Commands

### Local Development
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

### Git Commands
```bash
# Pull latest changes
git pull origin master

# Push changes (triggers deployment)
git push origin master

# View commit history
git log --oneline
```

---

## 🎉 Success!

Your Brain Link Tracker is now deployed and ready to use!

**Live URL**: Check your Vercel dashboard for the deployment URL

---

*Last Updated: October 21, 2025*
*Version: 1.0.0*
