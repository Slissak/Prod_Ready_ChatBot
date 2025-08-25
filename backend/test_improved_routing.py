#!/usr/bin/env python3
"""
Test script to verify the improved routing logic.
"""

import requests
import json

def test_improved_routing():
    """Test that the routing logic works correctly with the new end_conversation criteria."""
    session_id = "test_improved_routing"
    
    # Test 1: Introduction (should go to RAG, not end_conversation)
    test_data_1 = {
        "session_id": session_id,
        "user_message": "Hi, I'm John"
    }
    
    print("=== Test 1: Introduction (Should Route to RAG) ===")
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
    
    # Test 2: Ask about positions (should go to RAG, not end_conversation)
    test_data_2 = {
        "session_id": session_id,
        "user_message": "What positions are available?"
    }
    
    print("\n=== Test 2: Position Inquiry (Should Route to RAG) ===")
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
    
    # Test 3: Sign-off phrase (should go to end_conversation)
    test_data_3 = {
        "session_id": session_id,
        "user_message": "Thank you, that's all"
    }
    
    print("\n=== Test 3: Sign-off (Should Route to End Conversation) ===")
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
    
    # Test 4: Not interested (should go to end_conversation)
    test_data_4 = {
        "session_id": session_id,
        "user_message": "I'm not interested in any of these roles"
    }
    
    print("\n=== Test 4: Not Interested (Should Route to End Conversation) ===")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_4,
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
    print("=== Improved Routing Test ===")
    test_improved_routing()
