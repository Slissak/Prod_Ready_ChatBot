#!/usr/bin/env python3
"""
Test script to verify that role state is managed in a single place.
"""

import requests
import json

def test_single_role_state():
    """Test that role state is managed only by the router."""
    session_id = "test_single_role_state"
    
    # Test 1: Set role to ML Engineer
    test_data_1 = {
        "session_id": session_id,
        "user_message": "ML"
    }
    
    print("=== Test 1: Set Role to ML Engineer ===")
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
    
    # Test 2: Ask about requirements (should maintain ML role)
    test_data_2 = {
        "session_id": session_id,
        "user_message": "What are the requirements?"
    }
    
    print("\n=== Test 2: Ask Requirements (Maintain ML Role) ===")
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
    
    # Test 3: Try to schedule (should maintain ML role)
    test_data_3 = {
        "session_id": session_id,
        "user_message": "Let's schedule an interview"
    }
    
    print("\n=== Test 3: Schedule Interview (Maintain ML Role) ===")
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
    print("=== Single Role State Test ===")
    test_single_role_state()
