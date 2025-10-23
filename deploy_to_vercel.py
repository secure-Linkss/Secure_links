#!/usr/bin/env python3
"""
Vercel Deployment Script for Brain Link Tracker
Deploys the application to Vercel with proper environment variables
"""

import requests
import json
import time

# Vercel Configuration
VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"
PROJECT_NAME = "bol-new"
GITHUB_REPO = "secure-Linkss/bol.new"

# Environment Variables
ENV_VARS = {
    "DATABASE_URL": "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require",
    "SECRET_KEY": "ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE",
    "SHORTIO_API_KEY": "sk_DbGGlUHPN7Z9VotL",
    "SHORTIO_DOMAIN": "Secure-links.short.gy"
}

HEADERS = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
    "Content-Type": "application/json"
}

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def get_or_create_project():
    """Get existing project or create new one"""
    print_section("CHECKING VERCEL PROJECT")
    
    # Check if project exists
    response = requests.get(
        "https://api.vercel.com/v9/projects",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        projects = response.json().get("projects", [])
        for project in projects:
            if project["name"] == PROJECT_NAME:
                print(f"✓ Found existing project: {PROJECT_NAME}")
                print(f"  Project ID: {project['id']}")
                return project
        
        # Project doesn't exist, create it
        print(f"Project '{PROJECT_NAME}' not found, creating...")
        return create_project()
    else:
        print(f"✗ Error checking projects: {response.text}")
        return None

def create_project():
    """Create new Vercel project"""
    print("\n📦 Creating new Vercel project...")
    
    payload = {
        "name": PROJECT_NAME,
        "framework": "vite",
        "gitRepository": {
            "type": "github",
            "repo": GITHUB_REPO
        }
    }
    
    response = requests.post(
        "https://api.vercel.com/v10/projects",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code in [200, 201]:
        project = response.json()
        print(f"✓ Project created: {project['name']}")
        print(f"  Project ID: {project['id']}")
        return project
    else:
        print(f"✗ Error creating project: {response.text}")
        return None

def set_environment_variables(project_id):
    """Set environment variables for the project"""
    print_section("SETTING ENVIRONMENT VARIABLES")
    
    for key, value in ENV_VARS.items():
        print(f"\nSetting {key}...")
        
        # Check if env var exists
        response = requests.get(
            f"https://api.vercel.com/v9/projects/{project_id}/env",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            existing_envs = response.json().get("envs", [])
            env_exists = any(env["key"] == key for env in existing_envs)
            
            if env_exists:
                # Delete existing env var
                for env in existing_envs:
                    if env["key"] == key:
                        delete_response = requests.delete(
                            f"https://api.vercel.com/v9/projects/{project_id}/env/{env['id']}",
                            headers=HEADERS
                        )
                        if delete_response.status_code == 200:
                            print(f"  ✓ Deleted existing {key}")
                        break
        
        # Create new env var
        payload = {
            "key": key,
            "value": value,
            "type": "encrypted",
            "target": ["production", "preview", "development"]
        }
        
        response = requests.post(
            f"https://api.vercel.com/v10/projects/{project_id}/env",
            headers=HEADERS,
            json=payload
        )
        
        if response.status_code in [200, 201]:
            print(f"  ✓ {key} set successfully")
        else:
            print(f"  ✗ Error setting {key}: {response.text}")

def trigger_deployment(project_id):
    """Trigger a new deployment"""
    print_section("TRIGGERING DEPLOYMENT")
    
    print("\n🚀 Deploying to Vercel...")
    
    # Trigger deployment by creating a new deployment
    payload = {
        "name": PROJECT_NAME,
        "gitSource": {
            "type": "github",
            "repo": GITHUB_REPO,
            "ref": "master"
        }
    }
    
    response = requests.post(
        "https://api.vercel.com/v13/deployments",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code in [200, 201]:
        deployment = response.json()
        deployment_id = deployment.get("id")
        deployment_url = deployment.get("url")
        
        print(f"✓ Deployment triggered successfully!")
        print(f"  Deployment ID: {deployment_id}")
        print(f"  URL: https://{deployment_url}")
        
        # Wait for deployment to complete
        print("\n⏳ Waiting for deployment to complete...")
        return wait_for_deployment(deployment_id)
    else:
        print(f"✗ Error triggering deployment: {response.text}")
        return None

def wait_for_deployment(deployment_id):
    """Wait for deployment to complete"""
    max_attempts = 60  # 5 minutes
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.get(
            f"https://api.vercel.com/v13/deployments/{deployment_id}",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            deployment = response.json()
            state = deployment.get("readyState")
            
            if state == "READY":
                print(f"\n✓ Deployment complete!")
                print(f"  URL: https://{deployment.get('url')}")
                return deployment
            elif state in ["ERROR", "CANCELED"]:
                print(f"\n✗ Deployment failed: {state}")
                return None
            else:
                print(f"  Status: {state} ({attempt + 1}/{max_attempts})")
                time.sleep(5)
                attempt += 1
        else:
            print(f"✗ Error checking deployment status: {response.text}")
            return None
    
    print("\n⏰ Deployment timeout - check Vercel dashboard for status")
    return None

def main():
    """Main deployment function"""
    print("\n" + "="*80)
    print("  BRAIN LINK TRACKER - VERCEL DEPLOYMENT")
    print("="*80)
    
    # Step 1: Get or create project
    project = get_or_create_project()
    if not project:
        print("\n✗ Failed to get/create project")
        return
    
    project_id = project["id"]
    
    # Step 2: Set environment variables
    set_environment_variables(project_id)
    
    # Step 3: Trigger deployment
    deployment = trigger_deployment(project_id)
    
    if deployment:
        print("\n" + "="*80)
        print("  ✅ DEPLOYMENT SUCCESSFUL!")
        print("="*80)
        print(f"\n🌐 Your application is live at:")
        print(f"   https://{deployment.get('url')}")
        print("\n📋 Test the application:")
        print("   1. Navigate to the URL above")
        print("   2. Login with: Brain / Mayflower1!!")
        print("   3. Verify all admin panel tabs load correctly")
        print("   4. Test creating a link")
        print("="*80 + "\n")
    else:
        print("\n" + "="*80)
        print("  ⚠️ DEPLOYMENT STATUS UNKNOWN")
        print("="*80)
        print("\nPlease check Vercel dashboard for deployment status")
        print("="*80 + "\n")

if __name__ == "__main__":
    main()
