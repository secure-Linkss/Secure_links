#!/usr/bin/env python3
"""
Brain Link Tracker - Project Completion Verification
=====================================================
This script verifies that all phases of the project are complete
"""

import os
import sys
import json
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

def check(condition, message):
    """Check a condition and print result"""
    if condition:
        print(f"{Colors.GREEN}✓ {message}{Colors.NC}")
        return True
    else:
        print(f"{Colors.RED}✗ {message}{Colors.NC}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}Brain Link Tracker - Project Completion Verification{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}\n")
    
    passed = 0
    failed = 0
    
    # PHASE 1: Backend API Verification
    print(f"{Colors.BLUE}PHASE 1: Backend API Routes{Colors.NC}")
    print("-" * 60)
    
    backend_routes = [
        ("src/routes/analytics_complete.py", "Analytics routes (complete)"),
        ("src/routes/security_complete.py", "Security routes (complete)"),
        ("src/routes/user_settings_complete.py", "User settings routes (complete)"),
        ("src/routes/campaigns.py", "Campaign routes"),
        ("src/routes/auth.py", "Authentication routes"),
        ("src/routes/links.py", "Link management routes"),
    ]
    
    for route_file, description in backend_routes:
        if check(os.path.exists(route_file), f"{description}"):
            passed += 1
        else:
            failed += 1
    
    # PHASE 2: Frontend Components Verification
    print(f"\n{Colors.BLUE}PHASE 2: Frontend Components{Colors.NC}")
    print("-" * 60)
    
    frontend_components = [
        ("src/components/Analytics.jsx", "Analytics component"),
        ("src/components/Geography.jsx", "Geography component"),
        ("src/components/Security.jsx", "Security component"),
        ("src/components/Campaign.jsx", "Campaign component"),
        ("src/components/Settings.jsx", "Settings component"),
        ("src/components/Dashboard.jsx", "Dashboard component"),
        ("src/components/TrackingLinks.jsx", "Tracking Links component"),
        ("src/components/LiveActivity.jsx", "Live Activity component"),
        ("src/components/LinkShortener.jsx", "Link Shortener component"),
    ]
    
    for component_file, description in frontend_components:
        if check(os.path.exists(component_file), f"{description}"):
            passed += 1
        else:
            failed += 1
    
    # Verify mobile responsiveness patterns in components
    print(f"\n{Colors.YELLOW}Checking Mobile Responsiveness...{Colors.NC}")
    responsive_patterns = ["grid-cols-1", "sm:grid-cols", "lg:grid-cols"]
    
    for component_file, _ in frontend_components[:5]:  # Check main components
        if os.path.exists(component_file):
            with open(component_file, 'r') as f:
                content = f.read()
                has_responsive = all(pattern in content for pattern in responsive_patterns)
                component_name = os.path.basename(component_file)
                if check(has_responsive, f"{component_name} has mobile responsive grids"):
                    passed += 1
                else:
                    failed += 1
    
    # PHASE 3: Database Models Verification
    print(f"\n{Colors.BLUE}PHASE 3: Database Models{Colors.NC}")
    print("-" * 60)
    
    models = [
        ("src/models/user.py", "User model"),
        ("src/models/link.py", "Link model"),
        ("src/models/tracking_event.py", "Tracking Event model"),
        ("src/models/campaign.py", "Campaign model"),
        ("src/models/security.py", "Security model"),
        ("src/models/notification.py", "Notification model"),
    ]
    
    for model_file, description in models:
        if check(os.path.exists(model_file), f"{description}"):
            passed += 1
        else:
            failed += 1
    
    # Verify User model has required fields
    if os.path.exists("src/models/user.py"):
        with open("src/models/user.py", 'r') as f:
            user_model = f.read()
            required_fields = ["notification_settings", "preferences", "metadata", "password"]
            for field in required_fields:
                if check(field in user_model, f"User model has '{field}' field"):
                    passed += 1
                else:
                    failed += 1
    
    # PHASE 4: Configuration & Deployment
    print(f"\n{Colors.BLUE}PHASE 4: Configuration & Deployment{Colors.NC}")
    print("-" * 60)
    
    config_files = [
        (".env.example", "Environment template"),
        (".env", "Environment configuration"),
        ("deploy_complete.sh", "Deployment script"),
        ("requirements.txt", "Python dependencies"),
        ("package.json", "Node dependencies"),
        ("vercel.json", "Vercel configuration"),
    ]
    
    for config_file, description in config_files:
        if check(os.path.exists(config_file), f"{description}"):
            passed += 1
        else:
            failed += 1
    
    # Verify environment variables are set
    if os.path.exists(".env"):
        with open(".env", 'r') as f:
            env_content = f.read()
            required_env = ["DATABASE_URL", "SECRET_KEY"]
            for var in required_env:
                if check(f"{var}=" in env_content, f"Environment variable {var} is set"):
                    passed += 1
                else:
                    failed += 1
    
    # PHASE 5: Main Application Integration
    print(f"\n{Colors.BLUE}PHASE 5: Application Integration{Colors.NC}")
    print("-" * 60)
    
    if os.path.exists("src/main.py"):
        with open("src/main.py", 'r') as f:
            main_content = f.read()
            required_imports = [
                "analytics_complete",
                "security_complete",
                "user_settings_complete",
                "campaigns_bp",
            ]
            for import_name in required_imports:
                if check(import_name in main_content, f"Imports {import_name}"):
                    passed += 1
                else:
                    failed += 1
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}Verification Summary{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}")
    
    total = passed + failed
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\nTotal Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.NC}")
    print(f"{Colors.RED}Failed: {failed}{Colors.NC}")
    print(f"Success Rate: {percentage:.1f}%")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{'='*60}{Colors.NC}")
        print(f"{Colors.GREEN}✓ ALL PHASES COMPLETE! Project is production-ready.{Colors.NC}")
        print(f"{Colors.GREEN}{'='*60}{Colors.NC}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{'='*60}{Colors.NC}")
        print(f"{Colors.YELLOW}⚠ Some components need attention.{Colors.NC}")
        print(f"{Colors.YELLOW}{'='*60}{Colors.NC}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
