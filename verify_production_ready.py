#!/usr/bin/env python3
"""
Production Readiness Verification Script
=========================================
Verifies all components, routes, and database tables for production deployment
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def check_database_models():
    """Verify all database models are properly defined"""
    print("\n" + "="*60)
    print("CHECKING DATABASE MODELS")
    print("="*60)
    
    try:
        from src.models.user import User, db
        from src.models.link import Link
        from src.models.tracking_event import TrackingEvent
        from src.models.campaign import Campaign
        from src.models.audit_log import AuditLog
        from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
        from src.models.support_ticket import SupportTicket
        from src.models.subscription_verification import SubscriptionVerification
        from src.models.notification import Notification
        from src.models.domain import Domain
        from src.models.security_threat import SecurityThreat
        
        models = [
            ('User', User),
            ('Link', Link),
            ('TrackingEvent', TrackingEvent),
            ('Campaign', Campaign),
            ('AuditLog', AuditLog),
            ('SecuritySettings', SecuritySettings),
            ('BlockedIP', BlockedIP),
            ('BlockedCountry', BlockedCountry),
            ('SupportTicket', SupportTicket),
            ('SubscriptionVerification', SubscriptionVerification),
            ('Notification', Notification),
            ('Domain', Domain),
            ('SecurityThreat', SecurityThreat)
        ]
        
        print(f"✅ All {len(models)} database models imported successfully:")
        for name, model in models:
            print(f"   - {name}: {model.__tablename__}")
        
        return True
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False

def check_api_routes():
    """Verify all API routes are properly registered"""
    print("\n" + "="*60)
    print("CHECKING API ROUTES")
    print("="*60)
    
    try:
        from api.index import app
        
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append((rule.rule, ','.join(rule.methods - {'HEAD', 'OPTIONS'})))
        
        # Group routes by prefix
        api_routes = [r for r in routes if r[0].startswith('/api/')]
        track_routes = [r for r in routes if r[0].startswith(('/t/', '/p/', '/q/', '/track'))]
        other_routes = [r for r in routes if r not in api_routes and r not in track_routes]
        
        print(f"✅ Total routes registered: {len(routes)}")
        print(f"\n📍 API Routes ({len(api_routes)}):")
        for route, methods in sorted(api_routes)[:15]:
            print(f"   {methods:15} {route}")
        if len(api_routes) > 15:
            print(f"   ... and {len(api_routes) - 15} more")
        
        print(f"\n📍 Tracking Routes ({len(track_routes)}):")
        for route, methods in sorted(track_routes):
            print(f"   {methods:15} {route}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking routes: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_country_flags():
    """Verify country flags utility is working"""
    print("\n" + "="*60)
    print("CHECKING COUNTRY FLAGS")
    print("="*60)
    
    try:
        from src.utils.country_flags import COUNTRY_FLAGS, get_country_flag, get_country_count
        
        total_countries = get_country_count()
        print(f"✅ Country flags loaded: {total_countries} countries")
        
        # Test some key countries
        test_countries = [
            "United States", "United Kingdom", "Canada", "Germany", "France",
            "Australia", "India", "Brazil", "Japan", "China", "Russia",
            "Mexico", "South Africa", "Nigeria", "Singapore"
        ]
        
        print("\n   Sample flags:")
        for country in test_countries[:10]:
            flag = get_country_flag(country)
            print(f"   {flag} {country}")
        
        # Test fallback
        unknown_flag = get_country_flag("NonExistentCountry")
        print(f"\n   Fallback for unknown: {unknown_flag} (should be 🌍)")
        
        return True
    except Exception as e:
        print(f"❌ Error checking country flags: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_frontend_components():
    """Check frontend components exist"""
    print("\n" + "="*60)
    print("CHECKING FRONTEND COMPONENTS")
    print("="*60)
    
    component_dir = os.path.join(os.path.dirname(__file__), 'src', 'components')
    
    if not os.path.exists(component_dir):
        print("❌ Components directory not found")
        return False
    
    # Key components
    key_components = [
        'Dashboard.jsx',
        'Analytics.jsx',
        'Geography.jsx',
        'TrackingLinks.jsx',
        'Campaign.jsx',
        'Security.jsx',
        'Settings.jsx',
        'LiveActivity.jsx',
        'Notifications.jsx',
        'AdminPanel.jsx',
        'LoginPage.jsx'
    ]
    
    ui_dir = os.path.join(component_dir, 'ui')
    ui_components = len([f for f in os.listdir(ui_dir) if f.endswith('.jsx')]) if os.path.exists(ui_dir) else 0
    
    missing = []
    found = []
    
    for component in key_components:
        path = os.path.join(component_dir, component)
        if os.path.exists(path):
            found.append(component)
        else:
            missing.append(component)
    
    print(f"✅ Key components: {len(found)}/{len(key_components)} found")
    for comp in found:
        print(f"   ✓ {comp}")
    
    if missing:
        print(f"\n❌ Missing components:")
        for comp in missing:
            print(f"   ✗ {comp}")
    
    print(f"\n✅ UI components (shadcn/ui): {ui_components} components")
    
    return len(missing) == 0

def check_config_files():
    """Check configuration files"""
    print("\n" + "="*60)
    print("CHECKING CONFIGURATION FILES")
    print("="*60)
    
    root = os.path.dirname(__file__)
    
    config_files = {
        'package.json': 'Frontend dependencies',
        'package-lock.json': 'Dependency lock file (npm)',
        'vercel.json': 'Vercel deployment config',
        '.env.production': 'Production environment template',
        'requirements.txt': 'Python dependencies',
        'vite.config.js': 'Vite build configuration',
        'tailwind.config.js': 'Tailwind CSS config',
        'api/index.py': 'Vercel serverless function entry'
    }
    
    all_good = True
    for file, description in config_files.items():
        path = os.path.join(root, file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"   ✓ {file:25} ({description}) - {size} bytes")
        else:
            print(f"   ✗ {file:25} ({description}) - MISSING")
            all_good = False
    
    # Check that pnpm-lock.yaml is NOT present
    pnpm_lock = os.path.join(root, 'pnpm-lock.yaml')
    if os.path.exists(pnpm_lock):
        print(f"\n   ⚠️  pnpm-lock.yaml exists - should be removed for npm compatibility")
        all_good = False
    else:
        print(f"\n   ✓ pnpm-lock.yaml correctly removed (using npm)")
    
    return all_good

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("BRAIN LINK TRACKER - PRODUCTION READINESS CHECK")
    print("="*60)
    
    checks = [
        ("Configuration Files", check_config_files),
        ("Frontend Components", check_frontend_components),
        ("Country Flags Utility", check_country_flags),
        ("Database Models", check_database_models),
        ("API Routes", check_api_routes),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n❌ Error running {check_name}: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, passed_check in results.items():
        status = "✅ PASS" if passed_check else "❌ FAIL"
        print(f"{status:10} {check_name}")
    
    print("\n" + "="*60)
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED - READY FOR PRODUCTION DEPLOYMENT!")
        print("="*60)
        return 0
    else:
        print("\n⚠️  SOME CHECKS FAILED - REVIEW ERRORS ABOVE")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
