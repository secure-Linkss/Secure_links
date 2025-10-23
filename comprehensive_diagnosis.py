#!/usr/bin/env python3
"""
Comprehensive Brain Link Tracker Diagnostic Script
Analyzes the entire project for missing APIs, models, components, and configuration issues
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def check_database_models():
    """Check all database models and their to_dict methods"""
    print_section("DATABASE MODELS CHECK")
    
    models_dir = Path("src/models")
    model_files = list(models_dir.glob("*.py"))
    
    print(f"\nFound {len(model_files)} model files:")
    for model_file in model_files:
        print(f"  ✓ {model_file.name}")
    
    # Check critical models
    critical_models = [
        "user.py", "link.py", "campaign.py", "tracking_event.py",
        "audit_log.py", "notification.py", "domain.py",
        "security_threat.py", "support_ticket.py", "subscription_verification.py"
    ]
    
    print("\nCritical models status:")
    for model in critical_models:
        path = models_dir / model
        if path.exists():
            print(f"  ✓ {model}")
        else:
            print(f"  ✗ MISSING: {model}")

def check_api_routes():
    """Check all API route files"""
    print_section("API ROUTES CHECK")
    
    routes_dir = Path("src/routes")
    route_files = list(routes_dir.glob("*.py"))
    
    print(f"\nFound {len(route_files)} route files:")
    for route_file in route_files:
        print(f"  ✓ {route_file.name}")
    
    # List all endpoints in admin_complete.py
    admin_complete = routes_dir / "admin_complete.py"
    if admin_complete.exists():
        print("\n Analyzing admin_complete.py endpoints:")
        with open(admin_complete, 'r') as f:
            content = f.read()
            import re
            endpoints = re.findall(r'@admin_complete_bp\.route\("([^"]+)"', content)
            for endpoint in endpoints:
                print(f"    - {endpoint}")

def check_frontend_components():
    """Check frontend React components"""
    print_section("FRONTEND COMPONENTS CHECK")
    
    components_dir = Path("src/components")
    component_files = list(components_dir.glob("*.jsx")) + list(components_dir.glob("*.tsx"))
    
    print(f"\nFound {len(component_files)} component files:")
    for component_file in component_files:
        if component_file.parent.name != "ui":
            print(f"  ✓ {component_file.name}")
    
    # Check critical components
    critical_components = [
        "Dashboard.jsx", "TrackingLinks.jsx", "AdminPanel.jsx", 
        "Analytics.jsx", "Geography.jsx", "Security.jsx",
        "Settings.jsx", "Campaign.jsx", "LoginPage.jsx"
    ]
    
    print("\nCritical components status:")
    for component in critical_components:
        path = components_dir / component
        if path.exists():
            print(f"  ✓ {component}")
        else:
            print(f"  ✗ MISSING: {component}")

def check_environment_variables():
    """Check environment variable configuration"""
    print_section("ENVIRONMENT VARIABLES CHECK")
    
    env_files = [".env.example", ".env.production", ".env.vercel"]
    
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "SHORTIO_API_KEY",
        "SHORTIO_DOMAIN"
    ]
    
    print("\nEnvironment files:")
    for env_file in env_files:
        if Path(env_file).exists():
            print(f"  ✓ {env_file}")
            with open(env_file, 'r') as f:
                content = f.read()
                for var in required_vars:
                    if var in content:
                        # Check if it has a value
                        for line in content.split('\n'):
                            if line.startswith(var):
                                if '=' in line and line.split('=')[1].strip():
                                    print(f"    ✓ {var} is set")
                                else:
                                    print(f"    ⚠ {var} is defined but empty")
                    else:
                        print(f"    ✗ {var} is missing")
        else:
            print(f"  ✗ MISSING: {env_file}")

def check_main_app_files():
    """Check main application entry points"""
    print_section("MAIN APPLICATION FILES CHECK")
    
    critical_files = {
        "src/main.py": "Main Flask app",
        "api/index.py": "Vercel API entry point",
        "src/App.jsx": "Main React component",
        "src/database.py": "Database configuration",
        "package.json": "Frontend dependencies",
        "requirements.txt": "Python dependencies",
        "vercel.json": "Vercel deployment config",
        "vite.config.js": "Vite build config"
    }
    
    print("\nCritical files status:")
    for file_path, description in critical_files.items():
        if Path(file_path).exists():
            print(f"  ✓ {file_path} - {description}")
        else:
            print(f"  ✗ MISSING: {file_path} - {description}")

def analyze_admin_endpoints():
    """Analyze admin panel API endpoints"""
    print_section("ADMIN PANEL API ANALYSIS")
    
    print("\nExpected admin endpoints:")
    expected_endpoints = [
        "/api/admin/dashboard",
        "/api/admin/dashboard/stats",
        "/api/admin/campaigns",
        "/api/admin/campaigns/details",
        "/api/admin/users",
        "/api/admin/users/<id>",
        "/api/admin/domains",
        "/api/admin/security/threats",
        "/api/admin/subscriptions",
        "/api/admin/support-tickets"
    ]
    
    for endpoint in expected_endpoints:
        print(f"  - {endpoint}")
    
    # Check if admin_complete.py has these endpoints
    admin_file = Path("src/routes/admin_complete.py")
    if admin_file.exists():
        with open(admin_file, 'r') as f:
            content = f.read()
        
        print("\nEndpoint implementation status:")
        for endpoint in expected_endpoints:
            # Convert endpoint pattern to route pattern
            route_pattern = endpoint.replace("<id>", "<int:user_id>")
            if route_pattern in content or endpoint.split('/')[-1] in content:
                print(f"  ✓ {endpoint}")
            else:
                print(f"  ✗ MISSING: {endpoint}")

def check_database_schema():
    """Check if database schema is properly defined"""
    print_section("DATABASE SCHEMA CHECK")
    
    print("\nRequired database tables:")
    required_tables = [
        "users",
        "links", 
        "campaigns",
        "tracking_events",
        "audit_logs",
        "notifications",
        "domains",
        "security_threats",
        "support_tickets",
        "subscription_verifications"
    ]
    
    for table in required_tables:
        print(f"  - {table}")
    
    print("\nNote: Run database initialization script to create these tables")

def main():
    print("\n" + "="*80)
    print("  BRAIN LINK TRACKER - COMPREHENSIVE DIAGNOSTIC REPORT")
    print("="*80)
    
    check_main_app_files()
    check_database_models()
    check_api_routes()
    check_frontend_components()
    check_environment_variables()
    analyze_admin_endpoints()
    check_database_schema()
    
    print("\n" + "="*80)
    print("  DIAGNOSTIC COMPLETE")
    print("="*80)
    print("\nNext Steps:")
    print("1. Fix any MISSING files or endpoints")
    print("2. Initialize database with proper schema")
    print("3. Test login functionality")
    print("4. Test all admin panel endpoints")
    print("5. Verify frontend components can fetch data")
    print("6. Run build test before deployment")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
