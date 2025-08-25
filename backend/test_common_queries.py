#!/usr/bin/env python3
"""
Test script to verify that the router handles common queries correctly.
"""

import requests
import json

def test_introduction():
    """Test when user introduces themselves."""
    test_data = {
        "session_id": "test_intro",
        "user_message": "Hi my name is Sivan"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Introduction Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

def test_position_inquiry():
    """Test when user asks about open positions."""
    test_data = {
        "session_id": "test_positions",
        "user_message": "what are the current open positions?"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nPosition Inquiry Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

def test_role_mention():
    """Test when user mentions a specific role."""
    test_data = {
        "session_id": "test_role",
        "user_message": "Data analyst"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nRole Mention Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    print("=== Common Queries Test ===")
    test_introduction()
    test_position_inquiry()
    test_role_mention()
