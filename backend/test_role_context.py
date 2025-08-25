#!/usr/bin/env python3
"""
Test script to verify that role context is maintained properly across conversations.
"""

import requests
import json

def test_role_context_maintenance():
    """Test that role context is maintained when switching between roles."""
    session_id = "test_role_context"
    
    # Test 1: Ask about Data Analyst
    test_data_1 = {
        "session_id": session_id,
        "user_message": "Tell me about the Data Analyst position"
    }
    
    print("=== Test 1: Data Analyst Query ===")
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
    
    # Test 2: Ask about Senior SQL Developer
    test_data_2 = {
        "session_id": session_id,
        "user_message": "Now tell me about the Senior SQL Developer role"
    }
    
    print("\n=== Test 2: Senior SQL Developer Query ===")
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
    
    # Test 3: Try to schedule for Senior SQL Developer
    test_data_3 = {
        "session_id": session_id,
        "user_message": "I'd like to schedule an interview for the Senior SQL Developer position"
    }
    
    print("\n=== Test 3: Scheduling for Senior SQL Developer ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_3,
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

if __name__ == "__main__":
    print("=== Role Context Maintenance Test ===")
    test_role_context_maintenance()
