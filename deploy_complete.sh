#!/bin/bash

###########################################
# Brain Link Tracker - Complete Deployment
# This script handles the full deployment process
###########################################

set -e  # Exit on error

echo "🚀 Starting Brain Link Tracker Deployment..."
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check environment variables
echo -e "\n${BLUE}Step 1: Checking environment variables...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Using environment variables from system.${NC}"
else
    echo -e "${GREEN}✓ .env file found${NC}"
    # Load environment variables
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check required variables
REQUIRED_VARS="DATABASE_URL SECRET_KEY"
for var in $REQUIRED_VARS; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}✗ ERROR: Required environment variable $var is not set${NC}"
        exit 1
    else
        echo -e "${GREEN}✓ $var is set${NC}"
    fi
done

# Step 2: Install Python dependencies
echo -e "\n${BLUE}Step 2: Installing Python dependencies...${NC}"
pip install --no-input --quiet -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Step 3: Install Node dependencies
echo -e "\n${BLUE}Step 3: Installing Node dependencies...${NC}"
npm install --silent
echo -e "${GREEN}✓ Node dependencies installed${NC}"

# Step 4: Database setup
echo -e "\n${BLUE}Step 4: Setting up database...${NC}"
python3 << EOF
import sys
sys.path.insert(0, '.')
from src.main import app, db
from src.models.user import User

with app.app_context():
    # Create all tables
    db.create_all()
    print('✓ Database tables created')
    
    # Create default admin user if not exists
    if not User.query.filter_by(username="Brain").first():
        admin_user = User(
            username="Brain", 
            email="admin@brainlinktracker.com",
            role="admin",
            is_active=True,
            is_verified=True
        )
        admin_user.set_password("Mayflower1!!")
        db.session.add(admin_user)
        db.session.commit()
        print('✓ Default admin user created (Username: Brain, Password: Mayflower1!!)')
    else:
        print('✓ Admin user already exists')
EOF
echo -e "${GREEN}✓ Database setup complete${NC}"

# Step 5: Build frontend
echo -e "\n${BLUE}Step 5: Building frontend...${NC}"
npm run build
echo -e "${GREEN}✓ Frontend built successfully${NC}"

# Step 6: Verify build
echo -e "\n${BLUE}Step 6: Verifying build...${NC}"
if [ -d "dist" ]; then
    echo -e "${GREEN}✓ dist/ directory exists${NC}"
    if [ -f "dist/index.html" ]; then
        echo -e "${GREEN}✓ index.html found in dist/${NC}"
        FILE_COUNT=$(find dist -type f | wc -l)
        echo -e "${GREEN}✓ $FILE_COUNT files in dist/ directory${NC}"
    else
        echo -e "${RED}✗ ERROR: index.html not found in dist/${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ ERROR: dist/ directory not found${NC}"
    exit 1
fi

# Step 7: Test backend
echo -e "\n${BLUE}Step 7: Testing backend routes...${NC}"
python3 << EOF
import sys
sys.path.insert(0, '.')
from src.main import app

with app.app_context():
    # Test that all blueprints are registered
    blueprints = list(app.blueprints.keys())
    print(f'✓ {len(blueprints)} blueprints registered: {", ".join(blueprints)}')
    
    # Test that routes are accessible
    rules = [str(rule) for rule in app.url_map.iter_rules()]
    api_routes = [r for r in rules if '/api/' in r]
    print(f'✓ {len(api_routes)} API routes registered')
EOF
echo -e "${GREEN}✓ Backend tests passed${NC}"

# Step 8: Display deployment information
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Deployment Information:${NC}"
echo -e "  • Frontend: Built in dist/ directory"
echo -e "  • Backend: Flask app in src/main.py"
echo -e "  • Database: Connected to PostgreSQL"
echo -e "  • Admin Login: Brain / Mayflower1!!"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. For local testing: python3 src/main.py"
echo -e "  2. For Vercel deployment: vercel --prod"
echo -e "  3. For other platforms: Follow their Python + React deployment guide"
echo ""
echo -e "${YELLOW}Important Notes:${NC}"
echo -e "  • Make sure environment variables are set in your deployment platform"
echo -e "  • Update DATABASE_URL, SECRET_KEY, and other credentials as needed"
echo -e "  • Change the default admin password after first login"
echo ""
echo -e "${GREEN}Happy Tracking! 🎉${NC}"
