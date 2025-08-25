#!/usr/bin/env python3
"""
Test script to verify that the RAG system properly handles role mentions.
"""

import requests
import json

def test_role_mention():
    """Test when user just mentions a role without asking a specific question."""
    test_data = {
        "session_id": "test_role_mention",
        "user_message": "Data analyst"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Role Mention Test:")
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
    print("=== Role Mention Test ===")
    test_role_mention()
