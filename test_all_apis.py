#!/usr/bin/env python3
"""
Comprehensive API Testing Script
Tests all API endpoints to ensure they are working correctly
"""

import os
import sys
import requests
import json
import threading
import time
from urllib.parse import urljoin

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_USER_CREDENTIALS = {
    'username': 'Brain',
    'password': 'Mayflower1!!'
}

def start_api_server():
    """Start the API server in background"""
    import subprocess
    import signal
    
    os.chdir("/home/user/Secure_links")
    
    # Set environment variables
    env = os.environ.copy()
    env.update({
        'SECRET_KEY': 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE',
        'DATABASE_URL': 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
        'FLASK_ENV': 'development'
    })
    
    # Start server
    process = subprocess.Popen(['python3', 'api/index.py'], env=env)
    
    # Wait for server to start
    time.sleep(5)
    
    return process

def test_api_endpoint(endpoint, method='GET', data=None, headers=None):
    """Test a single API endpoint"""
    url = urljoin(BASE_URL, endpoint)
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        
        return {
            'endpoint': endpoint,
            'method': method,
            'status_code': response.status_code,
            'success': 200 <= response.status_code < 500,
            'response_size': len(response.content),
            'response_time': response.elapsed.total_seconds()
        }
        
    except Exception as e:
        return {
            'endpoint': endpoint,
            'method': method,
            'status_code': 0,
            'success': False,
            'error': str(e),
            'response_time': 0
        }

def test_authentication():
    """Test authentication endpoints"""
    print("🔐 Testing Authentication...")
    
    # Test login
    login_result = test_api_endpoint(
        '/api/auth/login',
        method='POST',
        data=TEST_USER_CREDENTIALS
    )
    
    print(f"  Login: {'✅' if login_result['success'] else '❌'} {login_result['status_code']}")
    
    return login_result

def test_core_endpoints():
    """Test core API endpoints"""
    endpoints = [
        # User endpoints
        ('/api/users', 'GET'),
        ('/api/profile', 'GET'),
        ('/api/user/profile', 'GET'),
        
        # Link endpoints
        ('/api/links', 'GET'),
        ('/api/links/create', 'POST'),
        
        # Campaign endpoints
        ('/api/campaigns', 'GET'),
        
        # Analytics endpoints
        ('/api/analytics/dashboard', 'GET'),
        ('/api/analytics/summary', 'GET'),
        ('/api/analytics/overview', 'GET'),
        
        # Admin endpoints
        ('/api/admin/dashboard', 'GET'),
        ('/api/admin/users', 'GET'),
        ('/api/admin/campaigns', 'GET'),
        ('/api/admin/audit-logs', 'GET'),
        
        # Notification endpoints
        ('/api/notifications', 'GET'),
        ('/api/notifications/count', 'GET'),
        
        # Settings endpoints
        ('/api/settings', 'GET'),
        
        # Domain endpoints
        ('/api/domains', 'GET'),
        
        # Event endpoints
        ('/api/events', 'GET'),
        
        # Security endpoints
        ('/api/security/settings', 'GET'),
        
        # Support endpoints
        ('/api/support/tickets', 'GET'),
        
        # Payment endpoints
        ('/api/payments/plans', 'GET'),
        ('/api/payments/subscription', 'GET'),
    ]
    
    print(f"\n📊 Testing {len(endpoints)} Core Endpoints...")
    
    results = []
    success_count = 0
    
    for endpoint, method in endpoints:
        result = test_api_endpoint(endpoint, method=method)
        results.append(result)
        
        if result['success']:
            success_count += 1
            print(f"  {'✅' if result['success'] else '❌'} {method} {endpoint} - {result['status_code']}")
        else:
            print(f"  {'✅' if result['success'] else '❌'} {method} {endpoint} - {result.get('status_code', 'ERROR')}")
    
    print(f"\n📈 Core Endpoints Results: {success_count}/{len(endpoints)} successful")
    return results

def test_parametrized_endpoints():
    """Test endpoints with parameters"""
    endpoints = [
        # Links with ID
        ('/api/links/1', 'GET'),
        ('/api/links/regenerate/1', 'POST'),
        
        # Campaigns with ID
        ('/api/campaigns/1', 'GET'),
        
        # Admin users with ID
        ('/api/admin/users/1', 'GET'),
        ('/api/admin/approve-user/1', 'POST'),
        
        # Notifications with ID
        ('/api/notifications/1', 'GET'),
        ('/api/notifications/1/read', 'POST'),
        
        # Events with ID
        ('/api/events/1', 'GET'),
        
        # Domains with ID
        ('/api/admin/domains/1', 'GET'),
    ]
    
    print(f"\n🔗 Testing {len(endpoints)} Parametrized Endpoints...")
    
    results = []
    success_count = 0
    
    for endpoint, method in endpoints:
        result = test_api_endpoint(endpoint, method=method)
        results.append(result)
        
        if result['success']:
            success_count += 1
            print(f"  {'✅' if result['success'] else '❌'} {method} {endpoint} - {result['status_code']}")
        else:
            print(f"  {'✅' if result['success'] else '❌'} {method} {endpoint} - {result.get('status_code', 'ERROR')}")
    
    print(f"\n📈 Parametrized Endpoints Results: {success_count}/{len(endpoints)} successful")
    return results

def test_data_creation():
    """Test creating data through APIs"""
    print("\n🆕 Testing Data Creation...")
    
    # Test creating a link
    link_data = {
        'url': 'https://example.com',
        'title': 'Test Link',
        'description': 'A test link for API verification'
    }
    
    create_link_result = test_api_endpoint(
        '/api/links/create',
        method='POST',
        data=link_data
    )
    
    print(f"  Create Link: {'✅' if create_link_result['success'] else '❌'} {create_link_result['status_code']}")
    
    # Test creating a campaign
    campaign_data = {
        'name': 'Test Campaign',
        'description': 'A test campaign for API verification'
    }
    
    create_campaign_result = test_api_endpoint(
        '/api/campaigns',
        method='POST',
        data=campaign_data
    )
    
    print(f"  Create Campaign: {'✅' if create_campaign_result['success'] else '❌'} {create_campaign_result['status_code']}")
    
    return [create_link_result, create_campaign_result]

def generate_test_report(all_results):
    """Generate comprehensive test report"""
    
    total_tests = len(all_results)
    successful_tests = sum(1 for result in all_results if result['success'])
    failed_tests = total_tests - successful_tests
    
    avg_response_time = sum(result.get('response_time', 0) for result in all_results) / total_tests if total_tests > 0 else 0
    
    report = {
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'failed_tests': failed_tests,
        'success_rate': (successful_tests / total_tests * 100) if total_tests > 0 else 0,
        'average_response_time': avg_response_time,
        'detailed_results': all_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save report
    with open('api_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return report

def main():
    """Main testing function"""
    print("🚀 Starting Comprehensive API Testing...")
    print("=" * 60)
    
    # Start API server
    print("🔄 Starting API server...")
    server_process = start_api_server()
    
    try:
        # Wait for server to be ready
        print("⏳ Waiting for server to start...")
        time.sleep(10)
        
        # Test server is running
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=5)
            print("✅ Server is running")
        except:
            print("⚠️ Server may not be fully ready, proceeding with tests...")
        
        all_results = []
        
        # Run authentication test
        auth_result = test_authentication()
        all_results.append(auth_result)
        
        # Run core endpoint tests
        core_results = test_core_endpoints()
        all_results.extend(core_results)
        
        # Run parametrized endpoint tests
        param_results = test_parametrized_endpoints()
        all_results.extend(param_results)
        
        # Run data creation tests
        creation_results = test_data_creation()
        all_results.extend(creation_results)
        
        # Generate report
        report = generate_test_report(all_results)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE API TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {report['total_tests']}")
        print(f"Successful: {report['successful_tests']} ✅")
        print(f"Failed: {report['failed_tests']} ❌")
        print(f"Success Rate: {report['success_rate']:.1f}%")
        print(f"Average Response Time: {report['average_response_time']:.3f}s")
        print(f"\n📝 Detailed report saved to: api_test_report.json")
        
        # Print failed tests
        if report['failed_tests'] > 0:
            print("\n❌ FAILED TESTS:")
            for result in all_results:
                if not result['success']:
                    print(f"  • {result['method']} {result['endpoint']} - {result.get('error', 'HTTP ' + str(result['status_code']))}")
        
        return report['success_rate'] > 80  # Consider 80%+ success rate as passing
        
    finally:
        # Stop server
        if server_process:
            server_process.terminate()
            print("\n🛑 API server stopped")

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ API Testing Completed Successfully!")
    else:
        print("\n❌ API Testing Failed - Check the report for details")
        sys.exit(1)