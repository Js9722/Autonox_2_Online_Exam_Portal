#!/usr/bin/env python3
"""
Test script to verify login functionality works
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration_and_login():
    """Test complete registration and login flow"""
    print("🧪 Testing Registration and Login Flow...")
    
    # Step 1: Register a user
    registration_data = {
        "email": "logintest@example.com",
        "password": "password123",
        "full_name": "Login Test User",
        "phone": "+1234567890",
        "experience_level": "junior",
        "applied_role": "software_engineer",
        "skills": ["JavaScript", "Python", "React"]
    }
    
    try:
        print("📝 Registering user...")
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=registration_data)
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            reg_data = response.json()
            print(f"   Token: {reg_data['access_token'][:50]}...")
            print(f"   User ID: {reg_data['user_data']['id']}")
            print(f"   Role: {reg_data['user_data']['role']}")
            print(f"   Candidate ID: {reg_data['user_data'].get('candidate_id')}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Step 2: Login with the same user
    login_data = {
        "email": "logintest@example.com",
        "password": "password123"
    }
    
    try:
        print("\n🔐 Testing login...")
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        
        if response.status_code == 200:
            print("✅ Login successful!")
            login_data = response.json()
            print(f"   Token: {login_data['access_token'][:50]}...")
            print(f"   User ID: {login_data['user_data']['id']}")
            print(f"   Role: {login_data['user_data']['role']}")
            
            # Step 3: Test getting user info with token
            token = login_data['access_token']
            headers = {"Authorization": f"Bearer {token}"}
            
            print("\n👤 Testing user info endpoint...")
            user_response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
            
            if user_response.status_code == 200:
                user_info = user_response.json()
                print("✅ User info retrieved successfully!")
                print(f"   User: {user_info['full_name']} ({user_info['email']})")
                print(f"   Role: {user_info['role']}")
                if user_info.get('candidate'):
                    print(f"   Candidate: {user_info['candidate']['full_name']}")
                    print(f"   Skills: {user_info['candidate']['extracted_skills']}")
                return True
            else:
                print(f"❌ User info failed: {user_response.status_code}")
                print(f"   Error: {user_response.text}")
                return False
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def test_demo_login():
    """Test with demo credentials"""
    print("\n🧪 Testing Demo Login...")
    
    # First create demo user if it doesn't exist
    demo_data = {
        "email": "demo@example.com",
        "password": "password123",
        "full_name": "Demo User",
        "phone": "+1234567890",
        "experience_level": "mid",
        "applied_role": "full_stack_developer",
        "skills": ["React", "Node.js", "Python", "AWS"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=demo_data)
        if response.status_code == 200:
            print("✅ Demo user created/exists")
        else:
            print("ℹ️ Demo user might already exist")
    except:
        pass
    
    # Try login
    login_data = {
        "email": "demo@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Demo login successful!")
            data = response.json()
            print(f"   Token: {data['access_token'][:50]}...")
            print(f"   User: {data['user_data']['full_name']}")
            return True
        else:
            print(f"❌ Demo login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Demo login error: {e}")
        return False

def main():
    """Run all login tests"""
    print("🚀 Starting Login Functionality Tests")
    print("=" * 50)
    
    # Test backend health first
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print("❌ Backend is not healthy")
            return
    except:
        print("❌ Cannot connect to backend")
        print("   Make sure backend is running on http://localhost:8000")
        return
    
    # Run tests
    test1_passed = test_registration_and_login()
    test2_passed = test_demo_login()
    
    print("\n" + "=" * 50)
    if test1_passed and test2_passed:
        print("🎉 All login tests passed!")
        print("\n🔗 Frontend Login Credentials:")
        print("   Email: demo@example.com")
        print("   Password: password123")
        print("   Email: logintest@example.com")
        print("   Password: password123")
    else:
        print("❌ Some tests failed")
    
    print("\n📱 Frontend Access:")
    print("   Start frontend: cd frontend && npm start")
    print("   Login page: http://localhost:3000/login")
    print("   Registration: http://localhost:3000/register")

if __name__ == "__main__":
    main()
