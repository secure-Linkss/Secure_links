#!/usr/bin/env python3
"""
Comprehensive Audit Script for Secure Links Project
This script performs a complete audit of:
1. Frontend build status
2. Backend API routes
3. Database connectivity and schema
4. Live data fetching capabilities
5. Component functionality
6. Missing implementations
"""

import os
import sys
import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import subprocess
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ComprehensiveAudit:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.database_url = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
        self.results = {
            'frontend_build': False,
            'backend_running': False,
            'database_connected': False,
            'api_routes_tested': [],
            'missing_implementations': [],
            'database_tables': [],
            'live_data_issues': [],
            'component_issues': [],
            'recommendations': []
        }
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test_frontend_build(self):
        """Test if frontend builds successfully"""
        self.log("Testing frontend build...")
        try:
            result = subprocess.run(['npm', 'run', 'build'], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.results['frontend_build'] = True
                self.log("✅ Frontend builds successfully")
                return True
            else:
                self.log(f"❌ Frontend build failed: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Frontend build test failed: {str(e)}", "ERROR")
            return False
            
    def test_database_connection(self):
        """Test database connectivity and inspect schema"""
        self.log("Testing database connection...")
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Test basic connectivity
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            self.log(f"✅ Database connected: {version['version'][:50]}...")
            
            # Get all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = [row['table_name'] for row in cursor.fetchall()]
            self.results['database_tables'] = tables
            self.log(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
            
            # Check for required tables
            required_tables = [
                'users', 'links', 'campaigns', 'tracking_events', 
                'audit_logs', 'security_threats', 'support_tickets',
                'notifications', 'domains', 'subscription_verification'
            ]
            
            missing_tables = [table for table in required_tables if table not in tables]
            if missing_tables:
                self.results['missing_implementations'].extend(
                    [f"Missing database table: {table}" for table in missing_tables]
                )
                self.log(f"⚠️  Missing tables: {', '.join(missing_tables)}", "WARNING")
            
            self.results['database_connected'] = True
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            self.log(f"❌ Database connection failed: {str(e)}", "ERROR")
            return False
            
    def test_api_routes(self):
        """Test critical API routes"""
        self.log("Testing API routes...")
        
        # Test routes that should be accessible without authentication
        public_routes = [
            {'path': '/api/auth/validate', 'method': 'GET', 'expected_status': [401, 403]},
        ]
        
        # Test routes that require authentication (expect 401)
        protected_routes = [
            {'path': '/api/admin/dashboard-stats', 'method': 'GET', 'expected_status': [401]},
            {'path': '/api/admin/users', 'method': 'GET', 'expected_status': [401]},
            {'path': '/api/admin/campaigns', 'method': 'GET', 'expected_status': [401]},
            {'path': '/api/analytics/overview', 'method': 'GET', 'expected_status': [401]},
            {'path': '/api/links', 'method': 'GET', 'expected_status': [401]},
            {'path': '/api/campaigns', 'method': 'GET', 'expected_status': [401]},
        ]
        
        all_routes = public_routes + protected_routes
        
        for route_info in all_routes:
            try:
                url = f"{self.base_url}{route_info['path']}"
                if route_info['method'].upper() == 'GET':
                    response = requests.get(url, timeout=5)
                elif route_info['method'].upper() == 'POST':
                    response = requests.post(url, timeout=5)
                
                if response.status_code in route_info['expected_status']:
                    self.log(f"✅ {route_info['path']} - Status: {response.status_code}")
                    self.results['api_routes_tested'].append({
                        'path': route_info['path'],
                        'status': response.status_code,
                        'success': True
                    })
                else:
                    self.log(f"⚠️  {route_info['path']} - Expected: {route_info['expected_status']}, Got: {response.status_code}", "WARNING")
                    self.results['api_routes_tested'].append({
                        'path': route_info['path'],
                        'status': response.status_code,
                        'success': False
                    })
                    
            except requests.exceptions.ConnectionError:
                self.log(f"❌ {route_info['path']} - Connection failed (server not running?)", "ERROR")
                self.results['api_routes_tested'].append({
                    'path': route_info['path'],
                    'status': 'connection_failed',
                    'success': False
                })
            except Exception as e:
                self.log(f"❌ {route_info['path']} - Error: {str(e)}", "ERROR")
                self.results['api_routes_tested'].append({
                    'path': route_info['path'],
                    'status': f'error: {str(e)}',
                    'success': False
                })
                
    def check_component_implementations(self):
        """Check for missing component implementations"""
        self.log("Checking component implementations...")
        
        component_files = [
            'src/components/Dashboard.jsx',
            'src/components/AdminPanelComplete.jsx',
            'src/components/Analytics.jsx',
            'src/components/Campaign.jsx',
            'src/components/TrackingLinks.jsx',
            'src/components/Geography.jsx',
            'src/components/Security.jsx',
            'src/components/Settings.jsx',
            'src/components/Profile.jsx',
            'src/components/NotificationSystem.jsx'
        ]
        
        for component_file in component_files:
            if os.path.exists(component_file):
                # Check if component has live data fetching
                with open(component_file, 'r') as f:
                    content = f.read()
                    
                # Check for fetch calls
                if 'fetch(' in content or 'axios.' in content:
                    self.log(f"✅ {component_file} - Has API calls")
                else:
                    self.log(f"⚠️  {component_file} - No API calls found", "WARNING")
                    self.results['component_issues'].append(f"{component_file} - No live data fetching")
                
                # Check for hardcoded data
                if 'mockData' in content or 'sampleData' in content or 'dummyData' in content:
                    self.log(f"⚠️  {component_file} - Contains mock/dummy data", "WARNING")
                    self.results['live_data_issues'].append(f"{component_file} - Contains hardcoded data")
                    
            else:
                self.log(f"❌ {component_file} - File not found", "ERROR")
                self.results['missing_implementations'].append(f"Missing component: {component_file}")
                
    def check_vercel_deployment_readiness(self):
        """Check if project is ready for Vercel deployment"""
        self.log("Checking Vercel deployment readiness...")
        
        required_files = [
            ('vercel.json', 'Vercel configuration'),
            ('package.json', 'Package configuration'),
            ('dist/index.html', 'Built frontend'),
            ('api/index.py', 'Backend entry point')
        ]
        
        for file_path, description in required_files:
            if os.path.exists(file_path):
                self.log(f"✅ {description} - {file_path}")
            else:
                self.log(f"❌ {description} - {file_path} missing", "ERROR")
                self.results['missing_implementations'].append(f"Missing {description}: {file_path}")
                
    def check_database_data_population(self):
        """Check if database tables have live data"""
        self.log("Checking database data population...")
        
        if not self.results['database_connected']:
            self.log("❌ Cannot check data population - database not connected", "ERROR")
            return
            
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Check data in key tables
            tables_to_check = [
                ('users', 'User accounts'),
                ('links', 'Shortened links'),
                ('campaigns', 'Marketing campaigns'),
                ('tracking_events', 'Click tracking data')
            ]
            
            for table_name, description in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name};")
                    result = cursor.fetchone()
                    count = result['count']
                    
                    if count > 0:
                        self.log(f"✅ {description} - {count} records")
                    else:
                        self.log(f"⚠️  {description} - No data", "WARNING")
                        self.results['live_data_issues'].append(f"{table_name} table is empty")
                        
                except psycopg2.Error as e:
                    self.log(f"❌ {description} - Table check failed: {str(e)}", "ERROR")
                    
            cursor.close()
            conn.close()
            
        except Exception as e:
            self.log(f"❌ Database data check failed: {str(e)}", "ERROR")
            
    def generate_recommendations(self):
        """Generate recommendations based on audit results"""
        self.log("Generating recommendations...")
        
        recommendations = []
        
        if not self.results['frontend_build']:
            recommendations.append("Fix frontend build issues before deployment")
            
        if not self.results['database_connected']:
            recommendations.append("Fix database connection issues")
            
        if self.results['missing_implementations']:
            recommendations.append("Implement missing components and database tables")
            
        if self.results['live_data_issues']:
            recommendations.append("Replace hardcoded data with live API calls")
            recommendations.append("Populate database tables with initial data")
            
        if self.results['component_issues']:
            recommendations.append("Add live data fetching to components without API calls")
            
        # API-specific recommendations
        failed_routes = [route for route in self.results['api_routes_tested'] if not route['success']]
        if failed_routes:
            recommendations.append("Fix failed API routes for full functionality")
            
        self.results['recommendations'] = recommendations
        
        for rec in recommendations:
            self.log(f"💡 RECOMMENDATION: {rec}")
            
    def run_comprehensive_audit(self):
        """Run the complete audit"""
        self.log("="*60)
        self.log("STARTING COMPREHENSIVE PROJECT AUDIT")
        self.log("="*60)
        
        # Test frontend build
        self.test_frontend_build()
        
        # Test database
        self.test_database_connection()
        
        # Test API routes (requires backend to be running)
        try:
            # Quick check if backend is running
            response = requests.get(f"{self.base_url}/api/auth/validate", timeout=2)
            self.results['backend_running'] = True
            self.log("✅ Backend is running")
            self.test_api_routes()
        except requests.exceptions.ConnectionError:
            self.log("⚠️  Backend not running - skipping API tests", "WARNING")
            self.results['backend_running'] = False
            
        # Check components
        self.check_component_implementations()
        
        # Check Vercel readiness
        self.check_vercel_deployment_readiness()
        
        # Check database data
        self.check_database_data_population()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Print summary
        self.print_audit_summary()
        
        return self.results
        
    def print_audit_summary(self):
        """Print a comprehensive audit summary"""
        self.log("="*60)
        self.log("AUDIT SUMMARY")
        self.log("="*60)
        
        # Overall status
        issues_count = (
            len(self.results['missing_implementations']) +
            len(self.results['live_data_issues']) +
            len(self.results['component_issues']) +
            len([r for r in self.results['api_routes_tested'] if not r['success']])
        )
        
        if issues_count == 0:
            self.log("🎉 PROJECT STATUS: EXCELLENT - Ready for production!")
        elif issues_count <= 5:
            self.log("⚠️  PROJECT STATUS: GOOD - Minor issues to address")
        else:
            self.log("❌ PROJECT STATUS: NEEDS WORK - Multiple issues found")
            
        # Component status
        self.log(f"\n📊 COMPONENT STATUS:")
        self.log(f"   Frontend Build: {'✅ PASS' if self.results['frontend_build'] else '❌ FAIL'}")
        self.log(f"   Backend Running: {'✅ PASS' if self.results['backend_running'] else '⚠️  NOT RUNNING'}")
        self.log(f"   Database Connected: {'✅ PASS' if self.results['database_connected'] else '❌ FAIL'}")
        
        # API Routes
        successful_routes = len([r for r in self.results['api_routes_tested'] if r['success']])
        total_routes = len(self.results['api_routes_tested'])
        self.log(f"   API Routes: {successful_routes}/{total_routes} working")
        
        # Issues summary
        if self.results['missing_implementations']:
            self.log(f"\n❌ MISSING IMPLEMENTATIONS ({len(self.results['missing_implementations'])}):")
            for issue in self.results['missing_implementations'][:5]:  # Show first 5
                self.log(f"   - {issue}")
                
        if self.results['live_data_issues']:
            self.log(f"\n⚠️  LIVE DATA ISSUES ({len(self.results['live_data_issues'])}):")
            for issue in self.results['live_data_issues'][:5]:  # Show first 5
                self.log(f"   - {issue}")
                
        if self.results['component_issues']:
            self.log(f"\n🔧 COMPONENT ISSUES ({len(self.results['component_issues'])}):")
            for issue in self.results['component_issues'][:5]:  # Show first 5
                self.log(f"   - {issue}")
                
        # Recommendations
        if self.results['recommendations']:
            self.log(f"\n💡 TOP RECOMMENDATIONS:")
            for rec in self.results['recommendations'][:3]:  # Show first 3
                self.log(f"   - {rec}")
                
        self.log("="*60)


if __name__ == "__main__":
    audit = ComprehensiveAudit()
    results = audit.run_comprehensive_audit()
    
    # Save results to file
    with open('audit_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"\nDetailed results saved to: audit_results.json")