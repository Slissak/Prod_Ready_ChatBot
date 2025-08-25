#!/usr/bin/env python3
"""
Test script to verify session restart functionality.
"""

import requests
import json

def test_session_restart():
    """Test that sessions are properly cleaned up and restarted when conversation ends."""
    session_id = "test_session_restart"
    
    print("=== Session Restart Test ===")
    
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
            print(f"📝 Logs: {len(result.get('logs', []))} log entries")
        else:
            print(f"❌ Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return
    
    # Test 2: End the conversation
    test_data_2 = {
        "session_id": session_id,
        "user_message": "Thank you, that's all"
    }
    
    print("\n2. Ending conversation...")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_2,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result.get('bot_response', 'No response')}")
            logs = result.get('logs', [])
            print(f"📝 Logs: {logs}")
            
            # Check if session cleanup was logged
            cleanup_logged = any("Session" in log and "cleaned up" in log for log in logs)
            new_session_required = result.get("new_session_required", False)
            
            if cleanup_logged and new_session_required:
                print("✅ Session cleanup detected and new session required")
            elif cleanup_logged:
                print("✅ Session cleanup detected in logs")
            elif new_session_required:
                print("✅ New session required flag set")
            else:
                print("❌ Session cleanup not detected")
        else:
            print(f"❌ Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return
    
    # Test 3: Try to continue with same session (should create new session)
    test_data_3 = {
        "session_id": session_id,
        "user_message": "Hi again, I have another question"
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
            logs = result.get('logs', [])
            print(f"📝 Logs: {logs}")
            
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
    test_session_restart()
