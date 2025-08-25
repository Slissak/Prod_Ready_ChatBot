#!/usr/bin/env python3
"""
Simple test script to debug the backend without the frontend.
This script will help you test the chat endpoint directly.
"""

import requests
import json

def test_backend():
    """Test the backend chat endpoint."""
    
    # Test data
    test_data = {
        "session_id": "test_session_123",
        "user_message": "Hello, I'm interested in the Data Analyst position."
    }
    
    try:
        # Make request to the backend
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the backend server.")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"ERROR: {str(e)}")

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Health Check Status: {response.status_code}")
        print(f"Health Check Response: {response.json()}")
    except Exception as e:
        print(f"Health Check Error: {str(e)}")

if __name__ == "__main__":
    print("=== Backend Test Script ===")
    print("1. Testing health check...")
    test_health_check()
    print("\n2. Testing chat endpoint...")
    test_backend()
