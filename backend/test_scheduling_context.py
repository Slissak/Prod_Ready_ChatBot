#!/usr/bin/env python3
"""
Test script to verify that role context is maintained during scheduling conversations.
"""

import requests
import json

def test_scheduling_context():
    """Test that role context is maintained during scheduling."""
    session_id = "test_scheduling_context"
    
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
    
    # Test 2: Request scheduling
    test_data_2 = {
        "session_id": session_id,
        "user_message": "Great, can we schedule an interview?"
    }
    
    print("\n=== Test 2: Scheduling Request ===")
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
    
    # Test 3: Provide time preference
    test_data_3 = {
        "session_id": session_id,
        "user_message": "can you do in 3 days afternoon?"
    }
    
    print("\n=== Test 3: Time Preference ===")
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
    
    # Test 4: Confirm specific time
    test_data_4 = {
        "session_id": session_id,
        "user_message": "I can come at 15:00"
    }
    
    print("\n=== Test 4: Confirm Specific Time ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_4,
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
    print("=== Scheduling Context Test ===")
    test_scheduling_context()
