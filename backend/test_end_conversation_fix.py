#!/usr/bin/env python3
"""
Test script to verify end conversation properly triggers session restart.
"""

import requests
import json

def test_end_conversation_fix():
    """Test that end conversation properly triggers session restart."""
    session_id = "test_end_conversation_fix"
    
    print("=== End Conversation Fix Test ===")
    
    # Test 1: Start a conversation
    test_data_1 = {
        "session_id": session_id,
        "user_message": "Hi, I'm interested in the Data Analyst position"
    }
    
    print("1. Starting conversation...")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_1,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result.get('bot_response', 'No response')[:100]}...")
            print(f"📝 New session required: {result.get('new_session_required', False)}")
        else:
            print(f"❌ Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return
    
    # Test 2: End conversation with "not interested"
    test_data_2 = {
        "session_id": session_id,
        "user_message": "Thanks, not interested any more bye"
    }
    
    print("\n2. Ending conversation with 'not interested'...")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_2,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result.get('bot_response', 'No response')}")
            print(f"📝 New session required: {result.get('new_session_required', False)}")
            logs = result.get('logs', [])
            print(f"📝 Logs: {logs}")
            
            if result.get('new_session_required'):
                print("✅ Session restart signal detected!")
            else:
                print("❌ Session restart signal NOT detected!")
        else:
            print(f"❌ Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return
    
    # Test 3: Try to continue with same session ID (should create new session)
    test_data_3 = {
        "session_id": session_id,
        "user_message": "Hi again"
    }
    
    print("\n3. Testing new session creation...")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_3,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result.get('bot_response', 'No response')[:100]}...")
            print(f"📝 New session required: {result.get('new_session_required', False)}")
            
            # Check if this looks like a fresh session
            if "Hello! I'm an AI career assistant" in result.get('bot_response', ''):
                print("✅ New session started successfully")
            else:
                print("❌ New session not started properly")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_end_conversation_fix()
