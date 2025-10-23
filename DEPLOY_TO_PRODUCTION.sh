#!/bin/bash

# Brain Link Tracker - Production Deployment Script
# October 21, 2025

set -e  # Exit on any error

echo "=========================================="
echo "BRAIN LINK TRACKER - DEPLOYMENT SCRIPT"
echo "=========================================="

# Colors for output
GREEN='\033[0.32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Environment Variables (will be set on Vercel)
# export SECRET_KEY="your_secret_key_here"
# These variables will be set on Vercel
# export DATABASE_URL="your_database_url_here"
# export SHORTIO_API_KEY="your_api_key_here"
# export SHORTIO_DOMAIN="your_domain_here"

echo ""
echo "=== Step 1: Verify Build ==="
python3 BUILD_VERIFICATION.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build verification failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build verification passed${NC}"

echo ""
echo "=== Step 2: Configure Git ==="
git config --global user.email "admin@brainlinktracker.com"
git config --global user.name "Brain Link Tracker"
echo -e "${GREEN}✅ Git configured${NC}"

echo ""
echo "=== Step 3: Add All Changes ==="
git add .
echo -e "${GREEN}✅ All changes staged${NC}"

echo ""
echo "=== Step 4: Commit Changes ==="
COMMIT_MESSAGE="Production Fix: Resolved SQLAlchemy metadata conflict and database schema issues - $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MESSAGE" || echo -e "${YELLOW}⚠️  No changes to commit${NC}"
echo -e "${GREEN}✅ Changes committed${NC}"

echo ""
echo "=== Step 5: Push to GitHub ==="
echo "Repository: https://github.com/secure-Linkss/bol.new"
echo "Branch: main"

# Set up GitHub authentication (use your own token)
# GITHUB_TOKEN="your_github_token_here"
# git remote set-url origin "https://${GITHUB_TOKEN}@github.com/secure-Linkss/bol.new.git"

git push origin main --force
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully pushed to GitHub${NC}"
else
    echo -e "${RED}❌ Failed to push to GitHub${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ DEPLOYMENT PREPARATION COMPLETE!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Go to Vercel Dashboard: https://vercel.com/dashboard"
echo "2. Import the GitHub repository: secure-Linkss/bol.new"
echo "3. Configure Environment Variables:"
echo "   - SECRET_KEY=${SECRET_KEY}"
echo "   - DATABASE_URL=${DATABASE_URL}"
echo "   - SHORTIO_API_KEY=${SHORTIO_API_KEY}"
echo "   - SHORTIO_DOMAIN=${SHORTIO_DOMAIN}"
echo "4. Deploy the project"
echo "5. Run database migration:"
echo "   python3 migrate_database_production.py"
echo ""
echo "Login Credentials:"
echo "  Username: Brain"
echo "  Password: Mayflower1!!"
echo ""
echo "  Username: 7thbrain"
echo "  Password: Mayflower1!"
echo "=========================================="

# Create environment variables file for Vercel
cat > .env.production <<EOF
SECRET_KEY=ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE
DATABASE_URL=postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-a-de4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
SHORTIO_API_KEY=sk_DbGGlUHPN7Z9VotL
SHORTIO_DOMAIN=Secure-links.short.gy
EOF

echo ""
echo "✅ Environment variables file created: .env.production"
echo "This file contains all required environment variables for Vercel"
