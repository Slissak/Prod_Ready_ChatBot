#!/usr/bin/env python3
"""
Comprehensive test script to verify the RAG system is working properly.
This script tests different types of queries to ensure the backend responds appropriately.
"""

import requests
import json

def test_specific_question():
    """Test with a specific question about the Data Analyst position."""
    test_data = {
        "session_id": "test_session_specific",
        "user_message": "What are the requirements for the Data Analyst position?"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Specific Question Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

def test_general_inquiry():
    """Test with a general inquiry about the Data Analyst position."""
    test_data = {
        "session_id": "test_session_general",
        "user_message": "Tell me about the Data Analyst role"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nGeneral Inquiry Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

def test_scheduling_request():
    """Test scheduling functionality."""
    test_data = {
        "session_id": "test_session_scheduling",
        "user_message": "I'd like to schedule an interview for the Data Analyst position"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nScheduling Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot Response: {result.get('bot_response', 'No response')}")
            print(f"Logs: {result.get('logs', [])}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

def test_end_conversation():
    """Test conversation ending."""
    test_data = {
        "session_id": "test_session_end",
        "user_message": "Thank you, that's all I need"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nEnd Conversation Test:")
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
    print("=== Comprehensive Backend Test ===")
    test_specific_question()
    test_general_inquiry()
    test_scheduling_request()
    test_end_conversation()
