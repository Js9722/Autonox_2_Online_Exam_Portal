#!/usr/bin/env python3
"""
Test script for authentication endpoints
Run this to verify signup and login functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    print("🧪 Testing Registration...")
    
    registration_data = {
        "email": "test@example.com",
        "password": "Test123456",
        "full_name": "Test User",
        "phone": "+1234567890",
        "experience_level": "junior",
        "applied_role": "software_engineer",
        "skills": ["JavaScript", "Python", "React", "Node.js"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=registration_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Registration successful!")
            print(f"   Token: {data['access_token'][:50]}...")
            print(f"   User ID: {data['user_data']['id']}")
            print(f"   Role: {data['user_data']['role']}")
            return data['access_token']
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_login():
    """Test user login"""
    print("\n🧪 Testing Login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "Test123456"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=login_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"   Token: {data['access_token'][:50]}...")
            print(f"   User ID: {data['user_data']['id']}")
            print(f"   Role: {data['user_data']['role']}")
            return data['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_get_user(token):
    """Test getting user info"""
    print("\n🧪 Testing Get User Info...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/auth/me",
            params={"token": token}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Get user info successful!")
            print(f"   User: {data['full_name']} ({data['email']})")
            print(f"   Role: {data['role']}")
            if data.get('candidate'):
                print(f"   Candidate ID: {data['candidate']['id']}")
                print(f"   Experience Level: {data['candidate']['experience_level']}")
            return True
        else:
            print(f"❌ Get user info failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Get user info error: {e}")
        return False

def main():
    """Run all authentication tests"""
    print("🚀 Starting Authentication Tests")
    print("=" * 50)
    
    # Test registration
    token = test_registration()
    
    if token:
        # Test get user info
        test_get_user(token)
        
        # Test login
        login_token = test_login()
        
        if login_token:
            # Test get user info with login token
            test_get_user(login_token)
    
    print("\n" + "=" * 50)
    print("🏁 Authentication Tests Complete")

if __name__ == "__main__":
    main()
