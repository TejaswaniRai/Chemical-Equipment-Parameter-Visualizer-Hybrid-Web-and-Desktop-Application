#!/usr/bin/env python3
"""
Test script to verify user-specific dataset filtering
"""

import requests
import sys

API_BASE_URL = 'http://localhost:8000/api'

def create_test_user(username, password):
    """Create a test user and return token"""
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/register/',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Created user: {username}")
            return data['token']
        elif response.status_code == 400 and 'already exists' in response.json().get('error', ''):
            # User exists, try login
            response = requests.post(
                f'{API_BASE_URL}/auth/login/',
                json={'username': username, 'password': password}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Logged in existing user: {username}")
                return data['token']
        
        print(f"❌ Failed to create/login user: {response.text}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_datasets(token, username):
    """Get datasets for a user"""
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f'{API_BASE_URL}/datasets/', headers=headers)
        
        if response.status_code == 200:
            datasets = response.json()
            print(f"\n📊 Datasets for {username}: {len(datasets)}")
            for ds in datasets:
                print(f"  📁 {ds['name']}")
                print(f"     Uploaded: {ds['uploaded_at']}")
                print(f"     User: {ds.get('uploaded_by_username', 'N/A')}")
            return datasets
        else:
            print(f"❌ Failed to get datasets: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    """Test user isolation"""
    print("=" * 60)
    print("USER ISOLATION TEST")
    print("=" * 60)
    print("This test verifies that each user only sees their own datasets\n")
    
    # Check backend
    try:
        requests.get(f'{API_BASE_URL}/', timeout=2)
        print("✅ Backend is running\n")
    except:
        print("❌ Backend not running! Start it with: python manage.py runserver")
        sys.exit(1)
    
    # Create/login two test users
    print("Creating test users...")
    token1 = create_test_user('testuser1', 'testpass123')
    token2 = create_test_user('testuser2', 'testpass456')
    
    if not token1 or not token2:
        print("\n❌ Failed to create test users")
        sys.exit(1)
    
    # Get datasets for each user
    print("\n" + "=" * 60)
    print("FETCHING DATASETS FOR EACH USER")
    print("=" * 60)
    
    datasets1 = get_datasets(token1, 'testuser1')
    datasets2 = get_datasets(token2, 'testuser2')
    
    # Verify isolation
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    
    # Check if user1's datasets mention user1
    user1_ok = True
    for ds in datasets1:
        uploaded_by = ds.get('uploaded_by_username', '')
        if uploaded_by and uploaded_by != 'testuser1':
            print(f"❌ FAIL: User1 sees dataset from {uploaded_by}")
            user1_ok = False
    
    if user1_ok:
        print("✅ PASS: testuser1 only sees their own datasets")
    
    # Check if user2's datasets mention user2
    user2_ok = True
    for ds in datasets2:
        uploaded_by = ds.get('uploaded_by_username', '')
        if uploaded_by and uploaded_by != 'testuser2':
            print(f"❌ FAIL: User2 sees dataset from {uploaded_by}")
            user2_ok = False
    
    if user2_ok:
        print("✅ PASS: testuser2 only sees their own datasets")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if user1_ok and user2_ok:
        print("🎉 SUCCESS: User isolation working correctly!")
        print("\nEach user only sees their own datasets.")
        print("Upload some files with different users to see them separated.")
    else:
        print("⚠️  WARNING: User isolation may not be working correctly")
        print("Check backend views.py - datasets should be filtered by user")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == '__main__':
    main()
