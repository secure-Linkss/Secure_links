#!/usr/bin/env python3
"""
Comprehensive Project Audit Script
Identifies all issues mentioned by the user and creates a fix plan
"""

import os
import json
import re
from pathlib import Path

def audit_results():
    """Store audit findings"""
    return {
        "critical_issues": [],
        "api_routes": [],
        "models": [],
        "components": [],
        "missing_implementations": [],
        "data_fetching_issues": []
    }

def scan_api_routes():
    """Scan all API routes"""
    routes_dir = Path("src/routes")
    routes = []
    
    for file in routes_dir.glob("*.py"):
        with open(file, 'r') as f:
            content = f.read()
            # Find all route decorators
            route_matches = re.findall(r'@[\w_]+\.route\([\'"]([^\'"]+)[\'"]', content)
            routes.extend([(file.name, route) for route in route_matches])
    
    return routes

def scan_models():
    """Scan all database models"""
    models_dir = Path("src/models")
    models = []
    
    for file in models_dir.glob("*.py"):
        if file.name != "__init__.py":
            with open(file, 'r') as f:
                content = f.read()
                # Find class definitions
                class_matches = re.findall(r'class (\w+)\(', content)
                models.extend([(file.name, cls) for cls in class_matches])
    
    return models

def scan_components():
    """Scan all React components"""
    components_dir = Path("src/components")
    components = []
    
    for file in components_dir.glob("*.jsx"):
        components.append(file.name)
    
    return components

def check_user_model():
    """Check if User model has profile fields"""
    user_model_path = Path("src/models/user.py")
    
    with open(user_model_path, 'r') as f:
        content = f.read()
    
    required_fields = ['avatar', 'profile_picture', 'subscription_end_date', 'subscription_plan']
    missing_fields = []
    
    for field in required_fields:
        if field not in content:
            missing_fields.append(field)
    
    return missing_fields

def check_campaign_routes():
    """Check campaign routes for live data issues"""
    campaigns_route_path = Path("src/routes/campaigns.py")
    
    with open(campaigns_route_path, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check if it has proper stats calculation
    if 'clicks' not in content or 'conversions' not in content:
        issues.append("Campaign stats calculation missing")
    
    # Check for regenerate endpoint
    if 'regenerate' not in content:
        issues.append("Link regeneration endpoint missing")
    
    return issues

def check_geography_component():
    """Check if Geography uses heat map or atlas map"""
    geography_path = Path("src/components/Geography.jsx")
    
    with open(geography_path, 'r') as f:
        content = f.read()
    
    if 'heat' in content.lower():
        return "Uses heat map - needs atlas map implementation"
    
    return None

def main():
    print("=" * 80)
    print("COMPREHENSIVE PROJECT AUDIT")
    print("=" * 80)
    print()
    
    # 1. API Routes
    print("1. API ROUTES AUDIT")
    print("-" * 80)
    routes = scan_api_routes()
    print(f"Found {len(routes)} API routes")
    for file, route in routes[:10]:  # Show first 10
        print(f"  - {file}: {route}")
    print()
    
    # 2. Models
    print("2. DATABASE MODELS AUDIT")
    print("-" * 80)
    models = scan_models()
    print(f"Found {len(models)} models")
    for file, model in models:
        print(f"  - {file}: {model}")
    print()
    
    # 3. Components
    print("3. REACT COMPONENTS AUDIT")
    print("-" * 80)
    components = scan_components()
    print(f"Found {len(components)} components")
    for comp in components:
        print(f"  - {comp}")
    print()
    
    # 4. User Model Profile Fields
    print("4. USER MODEL PROFILE FIELDS CHECK")
    print("-" * 80)
    missing_user_fields = check_user_model()
    if missing_user_fields:
        print("Missing fields in User model:")
        for field in missing_user_fields:
            print(f"  - {field}")
    else:
        print("All profile fields present")
    print()
    
    # 5. Campaign Routes Issues
    print("5. CAMPAIGN ROUTES CHECK")
    print("-" * 80)
    campaign_issues = check_campaign_routes()
    if campaign_issues:
        print("Issues found:")
        for issue in campaign_issues:
            print(f"  - {issue}")
    else:
        print("No issues found")
    print()
    
    # 6. Geography Component
    print("6. GEOGRAPHY COMPONENT CHECK")
    print("-" * 80)
    geo_issue = check_geography_component()
    if geo_issue:
        print(f"Issue: {geo_issue}")
    else:
        print("No issues found")
    print()
    
    # 7. Critical Issues Summary
    print("=" * 80)
    print("CRITICAL ISSUES SUMMARY")
    print("=" * 80)
    
    issues = [
        "1. Profile icon not fully implemented (avatar, password reset, logout, subscription)",
        "2. Campaign management showing sample data instead of live data",
        "3. Link regeneration failing",
        "4. Heat map not working - needs atlas map",
        "5. Auto-create campaign from tracking link not working",
        "6. Notification timestamps showing incorrectly",
        "7. Dashboard metric design inconsistency",
        "8. Page reload stability issues",
        "9. Many components not fetching live data (graphs, charts, metrics)",
    ]
    
    for issue in issues:
        print(f"  {issue}")
    
    print()
    print("=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    os.chdir('/home/user/brain-link-tracker')
    main()
