#!/bin/bash

# Deployment Script with Environment Variables
# ==============================================

set -e

echo "=========================================="
echo "  BRAIN LINK TRACKER DEPLOYMENT"
echo "=========================================="
echo ""

# Environment Variables
export SECRET_KEY="ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE"
export DATABASE_URL="postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-a4de4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
export SHORTIO_API_KEY="sk_DbGGlUHPN7Z9VotL"
export SHORTIO_DOMAIN="Secure-links.short.gy"

echo "✓ Environment variables set"
echo ""

# Apply database migrations
echo "Applying database migrations..."
python3 apply_all_fixes.py

echo ""
echo "=========================================="
echo "  READY FOR DEPLOYMENT"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Commit changes: git add . && git commit -m 'Apply comprehensive fixes'"
echo "2. Push to GitHub: git push origin master"
echo "3. Deploy to Vercel (auto-deployment should trigger)"
echo ""
echo "Manual Vercel deployment (if needed):"
echo "  vercel --prod"
echo ""
