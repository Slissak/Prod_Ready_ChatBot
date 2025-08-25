#!/usr/bin/env python3
"""
Test script to reproduce the role context loss issue.
"""

import requests
import json

def test_role_loss():
    """Test that reproduces the role context loss issue."""
    session_id = "test_role_loss"
    
    # Test 1: Ask about ML role
    test_data_1 = {
        "session_id": session_id,
        "user_message": "ML"
    }
    
    print("=== Test 1: ML Role Query ===")
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
    
    # Test 2: Ask about requirements
    test_data_2 = {
        "session_id": session_id,
        "user_message": "Can you tell me What are the requirements for this role?"
    }
    
    print("\n=== Test 2: Requirements Query ===")
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
    
    # Test 3: Try to schedule
    test_data_3 = {
        "session_id": session_id,
        "user_message": "That is what I do! Lets schedule, are you free tomorrow?"
    }
    
    print("\n=== Test 3: Scheduling Request ===")
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
    print("=== Role Loss Test ===")
    test_role_loss()
