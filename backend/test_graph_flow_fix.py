#!/usr/bin/env python3
"""
Test script to verify the graph flow is working correctly.
"""

import requests
import json

def test_graph_flow_fix():
    """Test that the graph flow works correctly for normal conversations and end conversations."""
    session_id = "test_graph_flow_fix"
    
    print("=== Graph Flow Fix Test ===")
    
    # Test 1: Normal conversation - should NOT end
    test_data_1 = {
        "session_id": session_id,
        "user_message": "Hi, I'm interested in the Data Analyst position"
    }
    
    print("1. Testing normal conversation...")
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
            
            if not result.get('new_session_required'):
                print("✅ Normal conversation - no session restart (correct)")
            else:
                print("❌ Normal conversation triggered session restart (wrong)")
        else:
            print(f"❌ Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return
    
    # Test 2: Ask a question - should NOT end
    test_data_2 = {
        "session_id": session_id,
        "user_message": "What are the requirements?"
    }
    
    print("\n2. Testing question (should continue conversation)...")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_2,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result.get('bot_response', 'No response')[:100]}...")
            print(f"📝 New session required: {result.get('new_session_required', False)}")
            
            if not result.get('new_session_required'):
                print("✅ Question handled - no session restart (correct)")
            else:
                print("❌ Question triggered session restart (wrong)")
        else:
            print(f"❌ Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return
    
    # Test 3: End conversation - SHOULD end
    test_data_3 = {
        "session_id": session_id,
        "user_message": "Thank you, that's all"
    }
    
    print("\n3. Testing end conversation...")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data_3,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result.get('bot_response', 'No response')}")
            print(f"📝 New session required: {result.get('new_session_required', False)}")
            
            if result.get('new_session_required'):
                print("✅ End conversation - session restart triggered (correct)")
            else:
                print("❌ End conversation - no session restart (wrong)")
        else:
            print(f"❌ Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return

if __name__ == "__main__":
    test_graph_flow_fix()
