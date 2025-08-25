#!/usr/bin/env python3
"""
Test script to verify that the role_id is correctly passed to scheduling tools.
"""

import requests
import json

def test_role_id_fix():
    """Test that role_id is correctly passed to scheduling tools."""
    session_id = "test_role_id_fix"
    
    # Test 1: Set role to SQL Developer
    test_data_1 = {
        "session_id": session_id,
        "user_message": "SQL Developer"
    }
    
    print("=== Test 1: Set Role to SQL Developer ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_1,
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
    
    # Test 2: Try to schedule
    test_data_2 = {
        "session_id": session_id,
        "user_message": "Let's schedule an interview"
    }
    
    print("\n=== Test 2: Schedule Interview ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_2,
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
    
    # Test 3: Provide time preference
    test_data_3 = {
        "session_id": session_id,
        "user_message": "Morning"
    }
    
    print("\n=== Test 3: Provide Time Preference ===")
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
    print("=== Role ID Fix Test ===")
    test_role_id_fix()
