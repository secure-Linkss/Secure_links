# Secure Links - Deployment Guide

## Overview
This document provides comprehensive instructions for deploying the Secure Links application to Vercel and troubleshooting common issues.

## Prerequisites
- Node.js 18+ and npm/pnpm installed
- Python 3.9+ installed
- Vercel CLI installed (`npm i -g vercel`)
- GitHub account with repository access

## Environment Variables

### Required Environment Variables
Set these in Vercel Dashboard → Settings → Environment Variables:

```bash
# Database Configuration (Required)
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require

# Application Secret Key (Required)
SECRET_KEY=your-secret-key-here

# Short.io Integration (Optional)
SHORTIO_API_KEY=your-shortio-api-key
SHORTIO_DOMAIN=your-domain.short.gy

# Flask Environment
FLASK_ENV=production

# Node Environment
NODE_ENV=production
```

**Important:** Remove the `env` section from `vercel.json` before deployment to avoid exposing secrets.

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/secure-Linkss/Secure_links.git
cd Secure_links
```

### 2. Install Dependencies
```bash
# Install frontend dependencies
npm install
# or
pnpm install

# Install backend dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create .env File
```bash
cp .env.example .env
# Edit .env with your actual values
```

### 4. Build Frontend
```bash
npm run build
```

### 5. Run Locally with Vercel Dev
```bash
vercel dev
```

## Deployment to Vercel

### 1. Link to Vercel Project
```bash
vercel link
```

### 2. Set Environment Variables
```bash
# Set production environment variables
vercel env add DATABASE_URL production
vercel env add SECRET_KEY production
vercel env add SHORTIO_API_KEY production
vercel env add SHORTIO_DOMAIN production
vercel env add FLASK_ENV production
vercel env add NODE_ENV production
```

Or set them manually in Vercel Dashboard → Settings → Environment Variables.

### 3. Deploy to Production
```bash
vercel --prod
```

## Architecture

### Frontend (React + Vite)
- Built to `dist/` directory
- Served as static files by Vercel
- Routes handled by React Router

### Backend (Flask + Python)
- API routes in `api/` directory
- Serverless functions on Vercel
- PostgreSQL database (Neon)

### Routing Configuration
The `vercel.json` file configures:
- `/api/*` routes to Python serverless functions
- All other routes serve the React app

## Common Issues and Fixes

### Issue 1: Create Link Button Not Working

**Symptoms:**
- Clicking "Create Link" does nothing
- No network request in browser DevTools
- Console errors about authentication

**Fixes:**
1. Check if user is logged in (session cookie present)
2. Verify `credentials: 'include'` is set in fetch requests
3. Check browser console for JavaScript errors
4. Verify API endpoint is `/api/links/create` or `/api/links` (POST)

### Issue 2: 401 Authentication Required

**Symptoms:**
- API returns 401 status
- Error message: "Authentication required"

**Fixes:**
1. Ensure user is logged in
2. Check session cookie is being sent
3. Verify CORS is configured with `supports_credentials=True`
4. Add `credentials: 'include'` to all fetch requests

### Issue 3: 404 API Route Not Found

**Symptoms:**
- API returns 404 status
- Network tab shows request to `/api/links/create` or `/api/links`

**Fixes:**
1. Verify `vercel.json` routing configuration
2. Check that `api/index.py` exists
3. Ensure Flask blueprints are registered correctly
4. Rebuild and redeploy: `vercel --prod`

### Issue 4: 500 Internal Server Error

**Symptoms:**
- API returns 500 status
- Generic error message

**Fixes:**
1. Check Vercel function logs for stack traces
2. Verify DATABASE_URL is set correctly
3. Ensure database schema is up to date
4. Check for missing environment variables
5. Review Python error logs in Vercel dashboard

### Issue 5: Database Connection Errors

**Symptoms:**
- Error: "DATABASE_URL not set"
- Connection timeout errors
- SSL/TLS errors

**Fixes:**
1. Verify DATABASE_URL is set in Vercel environment variables
2. Ensure connection string includes `?sslmode=require`
3. Check database is accessible from Vercel's network
4. Verify database credentials are correct
5. Check database connection limits

### Issue 6: CORS Errors

**Symptoms:**
- Browser console shows CORS policy errors
- Preflight OPTIONS requests failing

**Fixes:**
1. Verify `Flask-Cors` is installed
2. Check `CORS(app, supports_credentials=True)` is set
3. Ensure OPTIONS method is handled in routes
4. Add `credentials: 'include'` to fetch requests

### Issue 7: Static Files Not Loading

**Symptoms:**
- Blank page after deployment
- 404 errors for JS/CSS files
- Assets not found

**Fixes:**
1. Run `npm run build` before deployment
2. Verify `dist/` directory exists and contains files
3. Check `vercel.json` routes configuration
4. Ensure `api/index.py` points to correct static folder
5. Redeploy: `vercel --prod`

## Debugging Tips

### 1. Check Vercel Function Logs
```bash
vercel logs
```

### 2. Test API Endpoints Locally
```bash
# Start local development server
vercel dev

# Test create link endpoint
curl -X POST http://localhost:3000/api/links \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{"target_url":"https://example.com","campaign_name":"Test"}'
```

### 3. Browser DevTools
- Open Network tab
- Click "Create Link" button
- Check request URL, method, headers, and payload
- Review response status and body
- Check Console tab for JavaScript errors

### 4. Verify Environment Variables
```bash
vercel env ls
```

### 5. Check Build Output
```bash
# Build frontend
npm run build

# Verify dist/ directory
ls -la dist/
```

## Production Checklist

Before deploying to production:

- [ ] Remove hardcoded secrets from code
- [ ] Set all environment variables in Vercel
- [ ] Remove `env` section from `vercel.json`
- [ ] Run `npm run build` to generate production assets
- [ ] Test all API endpoints locally with `vercel dev`
- [ ] Verify database migrations are applied
- [ ] Test authentication flow
- [ ] Test link creation with all domain types
- [ ] Verify tracking links work correctly
- [ ] Check analytics data is being recorded
- [ ] Test on multiple browsers
- [ ] Enable production error monitoring (Sentry, etc.)

## Security Best Practices

1. **Never commit secrets to Git**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use strong SECRET_KEY**
   - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

3. **Enable HTTPS only**
   - Vercel provides HTTPS by default

4. **Validate user input**
   - Sanitize URLs
   - Validate email addresses
   - Check for SQL injection

5. **Rate limiting**
   - Enable rate limiting for API endpoints
   - Prevent abuse of link creation

## Support

For issues not covered in this guide:
- Check Vercel documentation: https://vercel.com/docs
- Review Flask documentation: https://flask.palletsprojects.com/
- Check application logs in Vercel dashboard
- Review GitHub issues: https://github.com/secure-Linkss/Secure_links/issues

## Version History

- **v1.1** - Fixed create link functionality, improved error handling
- **v1.0** - Initial deployment

