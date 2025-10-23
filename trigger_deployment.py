#!/usr/bin/env python3
"""
Trigger Vercel deployment via project redeploy
"""

import requests
import json
import time

VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"
PROJECT_ID = "prj_5TJgAWxpuy2bWpXHBYBuFHVNpRxA"

HEADERS = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
    "Content-Type": "application/json"
}

def get_latest_deployment():
    """Get the latest deployment"""
    print("\n📦 Getting latest deployment...")
    
    response = requests.get(
        f"https://api.vercel.com/v6/deployments?projectId={PROJECT_ID}&limit=1",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        data = response.json()
        deployments = data.get("deployments", [])
        if deployments:
            deployment = deployments[0]
            deployment_id = deployment.get('uid') or deployment.get('id')
            print(f"✓ Found latest deployment: {deployment_id}")
            print(f"  URL: {deployment.get('url')}")
            return deployment
        else:
            print("✗ No deployments found")
    else:
        print(f"✗ Error: {response.text}")
    
    return None

def redeploy(deployment_id):
    """Redeploy an existing deployment"""
    print(f"\n🚀 Triggering redeploy...")
    
    response = requests.post(
        f"https://api.vercel.com/v13/deployments/{deployment_id}/redeploy",
        headers=HEADERS
    )
    
    if response.status_code in [200, 201]:
        new_deployment = response.json()
        print(f"✓ Redeployment triggered!")
        print(f"  New Deployment ID: {new_deployment['id']}")
        print(f"  URL: https://{new_deployment.get('url')}")
        return new_deployment
    else:
        print(f"✗ Error: {response.text}")
        return None

def main():
    print("\n" + "="*80)
    print("  TRIGGERING VERCEL DEPLOYMENT")
    print("="*80)
    
    # Get latest deployment
    deployment = get_latest_deployment()
    
    if deployment:
        # Redeploy
        deployment_id = deployment.get('uid') or deployment.get('id')
        new_deployment = redeploy(deployment_id)
        
        if new_deployment:
            print("\n" + "="*80)
            print("  ✅ DEPLOYMENT TRIGGERED SUCCESSFULLY!")
            print("="*80)
            print(f"\n🌐 Application URL:")
            print(f"   https://{new_deployment.get('url')}")
            print("\n📝 Note: Deployment may take 2-5 minutes to complete")
            print("   Check status at: https://vercel.com/dashboard")
            print("\n🔑 Login Credentials:")
            print("   Username: Brain")
            print("   Password: Mayflower1!!")
            print("="*80 + "\n")
    else:
        print("\n✗ Could not find latest deployment")
        print("Please trigger deployment manually from Vercel dashboard")

if __name__ == "__main__":
    main()
