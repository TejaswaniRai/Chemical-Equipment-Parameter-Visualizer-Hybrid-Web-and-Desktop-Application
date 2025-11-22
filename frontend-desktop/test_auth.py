#!/usr/bin/env python3
"""
Test script to verify authentication is working correctly
Run this to check if login/register endpoints are properly secured
"""

import requests
import sys

API_BASE_URL = 'http://localhost:8000/api'

def test_backend_connection():
    """Test if backend is running"""
    print("=" * 60)
    print("Testing Backend Connection...")
    print("=" * 60)
    
    try:
        response = requests.get(f'{API_BASE_URL}/', timeout=2)
        print("✅ Backend is running!")
        return True
    except Exception as e:
        print(f"❌ Backend not running: {e}")
        print("\nPlease start the backend with: python manage.py runserver")
        return False

def test_invalid_login():
    """Test that invalid credentials are rejected"""
    print("\n" + "=" * 60)
    print("Test 1: Invalid Login (should FAIL)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/login/',
            json={'username': 'nonexistent_user_12345', 'password': 'wrongpassword'}
        )
        
        if response.status_code == 401:
            print("✅ PASS: Invalid credentials correctly rejected")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_register_new_user():
    """Test user registration"""
    print("\n" + "=" * 60)
    print("Test 2: Register New User (should SUCCEED)")
    print("=" * 60)
    
    import random
    test_username = f"testuser_{random.randint(1000, 9999)}"
    test_password = "testpass123"
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/register/',
            json={'username': test_username, 'password': test_password}
        )
        
        if response.status_code == 201:
            data = response.json()
            if 'token' in data and 'username' in data:
                print(f"✅ PASS: User '{test_username}' registered successfully")
                print(f"   Token: {data['token'][:20]}...")
                return True, test_username, test_password
            else:
                print("❌ FAIL: Registration succeeded but response missing data")
                return False, None, None
        else:
            print(f"❌ FAIL: Expected 201, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None, None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, None, None

def test_valid_login(username, password):
    """Test that valid credentials work"""
    print("\n" + "=" * 60)
    print("Test 3: Valid Login (should SUCCEED)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/login/',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data and 'username' in data:
                print(f"✅ PASS: Login successful for '{username}'")
                print(f"   Token: {data['token'][:20]}...")
                return True
            else:
                print("❌ FAIL: Login succeeded but response missing data")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_duplicate_registration(username, password):
    """Test that duplicate usernames are rejected"""
    print("\n" + "=" * 60)
    print("Test 4: Duplicate Registration (should FAIL)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/register/',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 400:
            error = response.json().get('error', '')
            if 'already exists' in error.lower():
                print(f"✅ PASS: Duplicate username correctly rejected")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"⚠️  WARNING: Got 400 but different error: {error}")
                return True
        else:
            print(f"❌ FAIL: Expected 400, got {response.status_code}")
            print(f"   Duplicate registration should be rejected!")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_missing_credentials():
    """Test that missing credentials are rejected"""
    print("\n" + "=" * 60)
    print("Test 5: Missing Credentials (should FAIL)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/login/',
            json={'username': '', 'password': ''}
        )
        
        if response.status_code == 400:
            print("✅ PASS: Empty credentials correctly rejected")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ FAIL: Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all authentication tests"""
    print("\n" + "=" * 60)
    print("AUTHENTICATION SECURITY TEST SUITE")
    print("=" * 60)
    print("This will verify that:")
    print("1. Invalid credentials are rejected")
    print("2. Registration creates new users")
    print("3. Valid login works for registered users")
    print("4. Duplicate usernames are prevented")
    print("5. Missing credentials are rejected")
    print("=" * 60 + "\n")
    
    # Check backend
    if not test_backend_connection():
        sys.exit(1)
    
    results = []
    
    # Test 1: Invalid login
    results.append(("Invalid Login", test_invalid_login()))
    
    # Test 2: Register new user
    success, username, password = test_register_new_user()
    results.append(("New Registration", success))
    
    if success and username and password:
        # Test 3: Valid login
        results.append(("Valid Login", test_valid_login(username, password)))
        
        # Test 4: Duplicate registration
        results.append(("Duplicate Prevention", test_duplicate_registration(username, password)))
    else:
        print("\n⚠️  Skipping tests 3-4 due to registration failure")
        results.append(("Valid Login", False))
        results.append(("Duplicate Prevention", False))
    
    # Test 5: Missing credentials
    results.append(("Missing Credentials", test_missing_credentials()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Authentication is properly secured.")
    else:
        print("⚠️  Some tests failed. Authentication may have issues.")
    
    print("=" * 60 + "\n")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
