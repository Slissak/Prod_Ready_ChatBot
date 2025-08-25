#!/usr/bin/env python3
"""
Test script to verify that the system properly handles multiple role mentions.
"""

import requests
import json

def test_multiple_roles():
    """Test that the system asks for clarification when multiple roles are mentioned."""
    session_id = "test_multiple_roles"
    
    # Test 1: Mention multiple roles
    test_data_1 = {
        "session_id": session_id,
        "user_message": "I'm interested in Data Analyst and Python Developer"
    }
    
    print("=== Test 1: Multiple Roles Mentioned ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_1,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
    
    # Test 2: Choose one role after clarification
    test_data_2 = {
        "session_id": session_id,
        "user_message": "Data Analyst"
    }
    
    print("\n=== Test 2: Choose Single Role ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_2,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"Response: {result.get('bot_response', 'No response')[:100]}...")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
    
    # Test 3: Try to mention multiple roles again
    test_data_3 = {
        "session_id": session_id,
        "user_message": "Actually, I'm also interested in ML Engineer and SQL Developer"
    }
    
    print("\n=== Test 3: Multiple Roles Again ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_3,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    print("=== Multiple Roles Test ===")
    test_multiple_roles()
