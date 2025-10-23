#!/usr/bin/env python3
"""
PRODUCTION VERIFICATION SCRIPT
Comprehensive verification of Brain Link Tracker for production deployment
"""
import os
import sys
import subprocess
import json
from pathlib import Path

class ProductionVerifier:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues = []
        self.successes = []
        
    def log_success(self, message):
        self.successes.append(f"✓ {message}")
        print(f"✓ {message}")
        
    def log_issue(self, message):
        self.issues.append(f"✗ {message}")
        print(f"✗ {message}")
        
    def check_python_syntax(self):
        """Check all Python files for syntax errors"""
        print("\n" + "="*60)
        print("CHECKING PYTHON SYNTAX")
        print("="*60)
        
        python_files = list(self.project_root.rglob("*.py"))
        error_count = 0
        
        for py_file in python_files:
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                self.log_issue(f"Syntax error in {py_file}: {e}")
                error_count += 1
                
        if error_count == 0:
            self.log_success(f"All {len(python_files)} Python files have valid syntax")
        else:
            self.log_issue(f"{error_count} Python files have syntax errors")
            
    def check_mock_data(self):
        """Check for mock/sample data in code"""
        print("\n" + "="*60)
        print("CHECKING FOR MOCK/SAMPLE DATA")
        print("="*60)
        
        mock_patterns = [
            'mock_data', 'sample_data', 'fake_data', 'dummy_data',
            'MOCK_', 'SAMPLE_', 'FAKE_', 'DUMMY_',
            'test_data =', 'mock =', 'sample =',
            'example.com/test', 'example.org'
        ]
        
        found_mocks = []
        
        # Check Python files
        for py_file in self.project_root.rglob("*.py"):
            if 'node_modules' in str(py_file) or '.git' in str(py_file) or 'test' in str(py_file).lower():
                continue
                
            with open(py_file, 'r') as f:
                content = f.read()
                for pattern in mock_patterns:
                    if pattern.lower() in content.lower():
                        found_mocks.append(f"{py_file}: Contains '{pattern}'")
                        
        # Check JS/JSX files
        for js_file in list(self.project_root.rglob("*.js")) + list(self.project_root.rglob("*.jsx")):
            if 'node_modules' in str(js_file) or '.git' in str(js_file) or 'test' in str(js_file).lower():
                continue
                
            with open(js_file, 'r') as f:
                content = f.read()
                for pattern in mock_patterns:
                    if pattern.lower() in content.lower():
                        found_mocks.append(f"{js_file}: Contains '{pattern}'")
        
        if found_mocks:
            self.log_issue(f"Found {len(found_mocks)} potential mock data references")
            for mock in found_mocks[:10]:  # Show first 10
                print(f"    {mock}")
            if len(found_mocks) > 10:
                print(f"    ... and {len(found_mocks) - 10} more")
        else:
            self.log_success("No obvious mock data patterns found")
            
    def check_redis_dependencies(self):
        """Check for Redis dependencies that should be removed"""
        print("\n" + "="*60)
        print("CHECKING FOR REDIS DEPENDENCIES")
        print("="*60)
        
        redis_found = []
        
        for py_file in self.project_root.rglob("*.py"):
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
                
            with open(py_file, 'r') as f:
                content = f.read()
                if 'import redis' in content and 'quantum_redirect.py' not in str(py_file):
                    redis_found.append(str(py_file))
                    
        # Check requirements.txt
        req_file = self.project_root / 'requirements.txt'
        if req_file.exists():
            with open(req_file, 'r') as f:
                if 'redis' in f.read().lower():
                    redis_found.append('requirements.txt')
                    
        if redis_found:
            self.log_issue(f"Redis dependencies found in {len(redis_found)} files")
            for rf in redis_found:
                print(f"    {rf}")
        else:
            self.log_success("No unwanted Redis dependencies found")
            
    def check_api_endpoints(self):
        """Check if all required API endpoints are defined"""
        print("\n" + "="*60)
        print("CHECKING API ENDPOINTS")
        print("="*60)
        
        required_endpoints = [
            '/api/admin/users',
            '/api/admin/campaigns',
            '/api/admin/dashboard',
            '/api/admin/security',
            '/api/links',
            '/api/analytics',
            '/q/'  # Quantum redirect
        ]
        
        # Scan route files
        route_files = list((self.project_root / 'src' / 'routes').glob("*.py"))
        all_routes = []
        
        for route_file in route_files:
            with open(route_file, 'r') as f:
                content = f.read()
                # Find @bp.route decorators
                import re
                routes = re.findall(r'@\w+\.route\(["\']([^"\']+)["\']', content)
                all_routes.extend(routes)
                
        missing_endpoints = []
        for endpoint in required_endpoints:
            found = any(endpoint in route for route in all_routes)
            if not found:
                missing_endpoints.append(endpoint)
                
        if missing_endpoints:
            self.log_issue(f"Missing {len(missing_endpoints)} required endpoints")
            for ep in missing_endpoints:
                print(f"    {ep}")
        else:
            self.log_success(f"All {len(required_endpoints)} required endpoints defined")
            
    def check_frontend_build(self):
        """Check if frontend can build"""
        print("\n" + "="*60)
        print("CHECKING FRONTEND BUILD")
        print("="*60)
        
        package_json = self.project_root / 'package.json'
        if not package_json.exists():
            self.log_issue("package.json not found")
            return
            
        self.log_success("package.json exists")
        
        # Check for common issues
        with open(package_json, 'r') as f:
            pkg = json.load(f)
            
        if 'build' not in pkg.get('scripts', {}):
            self.log_issue("No build script defined in package.json")
        else:
            self.log_success("Build script defined")
            
        # Check if node_modules exists
        node_modules = self.project_root / 'node_modules'
        if not node_modules.exists():
            self.log_issue("node_modules not found - run npm install")
        else:
            self.log_success("node_modules exists")
            
    def check_environment_config(self):
        """Check environment configuration"""
        print("\n" + "="*60)
        print("CHECKING ENVIRONMENT CONFIGURATION")
        print("="*60)
        
        env_file = self.project_root / '.env'
        required_vars = [
            'SECRET_KEY',
            'DATABASE_URL',
            'SHORTIO_API_KEY',
            'SHORTIO_DOMAIN'
        ]
        
        if not env_file.exists():
            self.log_issue(".env file not found")
            return
            
        with open(env_file, 'r') as f:
            env_content = f.read()
            
        missing_vars = []
        for var in required_vars:
            if var not in env_content:
                missing_vars.append(var)
                
        if missing_vars:
            self.log_issue(f"Missing environment variables: {', '.join(missing_vars)}")
        else:
            self.log_success(f"All {len(required_vars)} required environment variables present")
            
        # Check for placeholder values
        if 'your_secret_key' in env_content.lower() or 'placeholder' in env_content.lower():
            self.log_issue("Placeholder values found in .env")
        else:
            self.log_success("No placeholder values in .env")
            
    def check_vercel_config(self):
        """Check Vercel deployment configuration"""
        print("\n" + "="*60)
        print("CHECKING VERCEL CONFIGURATION")
        print("="*60)
        
        vercel_json = self.project_root / 'vercel.json'
        if not vercel_json.exists():
            self.log_issue("vercel.json not found")
            return
            
        with open(vercel_json, 'r') as f:
            try:
                config = json.load(f)
                self.log_success("vercel.json is valid JSON")
                
                if 'builds' in config:
                    self.log_success("Build configuration present")
                else:
                    self.log_issue("No builds configuration in vercel.json")
                    
                if 'routes' in config or 'rewrites' in config:
                    self.log_success("Routing configuration present")
                else:
                    self.log_issue("No routing configuration in vercel.json")
                    
            except json.JSONDecodeError:
                self.log_issue("vercel.json is invalid JSON")
                
    def generate_report(self):
        """Generate final verification report"""
        print("\n" + "="*60)
        print("VERIFICATION REPORT")
        print("="*60)
        
        print(f"\n✅ SUCCESSES: {len(self.successes)}")
        for success in self.successes:
            print(f"  {success}")
            
        print(f"\n❌ ISSUES: {len(self.issues)}")
        for issue in self.issues:
            print(f"  {issue}")
            
        print("\n" + "="*60)
        if len(self.issues) == 0:
            print("🎉 PROJECT IS PRODUCTION READY!")
            print("="*60)
            return True
        else:
            print(f"⚠️  {len(self.issues)} ISSUES NEED ATTENTION")
            print("="*60)
            return False
            
    def run_all_checks(self):
        """Run all verification checks"""
        print("\n" + "="*60)
        print("BRAIN LINK TRACKER - PRODUCTION VERIFICATION")
        print("="*60)
        
        self.check_python_syntax()
        self.check_mock_data()
        self.check_redis_dependencies()
        self.check_api_endpoints()
        self.check_environment_config()
        self.check_vercel_config()
        self.check_frontend_build()
        
        return self.generate_report()

if __name__ == "__main__":
    verifier = ProductionVerifier()
    success = verifier.run_all_checks()
    sys.exit(0 if success else 1)
