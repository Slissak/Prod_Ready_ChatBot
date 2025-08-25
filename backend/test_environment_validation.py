#!/usr/bin/env python3
"""
Comprehensive environment variable validation test script.
Tests all deployment scenarios: local .env, local Docker, and Azure container.
"""

import requests
import json
import time
import os
from typing import Dict, Any

def test_health_endpoint(base_url: str) -> Dict[str, Any]:
    """Test the health endpoint."""
    print(f"🏥 Testing health endpoint at {base_url}/health...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {result.get('status')}")
            print(f"   Environment variables:")
            for var, present in result.get('environment_variables', {}).items():
                status = "✅ Present" if present else "❌ Missing"
                print(f"     {var}: {status}")
            return result
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return {"error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {str(e)}")
        return {"error": str(e)}

def test_environment_endpoint(base_url: str) -> Dict[str, Any]:
    """Test the environment test endpoint."""
    print(f"🔍 Testing environment endpoint at {base_url}/env-test...")
    
    try:
        response = requests.get(f"{base_url}/env-test", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Environment test passed!")
            print(f"   All variables present: {result.get('all_variables_present')}")
            print(f"   Environment: {result.get('environment_status', {}).get('environment')}")
            return result
        else:
            print(f"❌ Environment test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return {"error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Environment test error: {str(e)}")
        return {"error": str(e)}

def test_chat_endpoint(base_url: str) -> Dict[str, Any]:
    """Test the chat endpoint with a simple message."""
    print(f"💬 Testing chat endpoint at {base_url}/chat...")
    
    test_data = {
        "session_id": "test_env_validation",
        "user_message": "Hi, I'm testing the environment setup"
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat test passed!")
            print(f"   Response: {result.get('bot_response', 'No response')[:100]}...")
            return result
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return {"error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat test error: {str(e)}")
        return {"error": str(e)}

def test_root_endpoint(base_url: str) -> Dict[str, Any]:
    """Test the root endpoint."""
    print(f"📡 Testing root endpoint at {base_url}/...")
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Root endpoint test passed!")
            print(f"   Status: {result.get('status')}")
            print(f"   Version: {result.get('version')}")
            return result
        else:
            print(f"❌ Root endpoint test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return {"error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint error: {str(e)}")
        return {"error": str(e)}

def run_comprehensive_test(base_url: str, test_name: str):
    """Run all tests for a given deployment scenario."""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name.upper()} TEST")
    print(f"{'='*60}")
    print(f"Testing against: {base_url}")
    
    results = {}
    
    # Test 1: Root endpoint
    results['root'] = test_root_endpoint(base_url)
    
    # Test 2: Health endpoint
    results['health'] = test_health_endpoint(base_url)
    
    # Test 3: Environment endpoint
    results['environment'] = test_environment_endpoint(base_url)
    
    # Test 4: Chat endpoint
    results['chat'] = test_chat_endpoint(base_url)
    
    # Summary
    print(f"\n📊 {test_name.upper()} TEST SUMMARY:")
    print(f"{'='*40}")
    
    success_count = 0
    total_tests = len(results)
    
    for test_name, result in results.items():
        if 'error' not in result:
            print(f"✅ {test_name}: PASSED")
            success_count += 1
        else:
            print(f"❌ {test_name}: FAILED - {result.get('error')}")
    
    print(f"\n🎯 Overall: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED! Environment is properly configured.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
    
    return results

def main():
    """Main test function."""
    print("🚀 Environment Variable Validation Test Suite")
    print("=" * 60)
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Local Development (.env file)",
            "url": "http://localhost:8000"
        },
        {
            "name": "Local Docker Container",
            "url": "http://localhost:8000"  # Same port, different container
        },
        {
            "name": "Azure Container Instance",
            "url": "http://your-azure-container-ip:8000"  # Replace with actual Azure URL
        }
    ]
    
    all_results = {}
    
    for scenario in test_scenarios:
        print(f"\n🔍 Testing {scenario['name']}...")
        
        # Skip Azure test if URL is placeholder
        if "your-azure-container-ip" in scenario['url']:
            print("⏭️  Skipping Azure test (URL not configured)")
            continue
            
        try:
            results = run_comprehensive_test(scenario['url'], scenario['name'])
            all_results[scenario['name']] = results
        except Exception as e:
            print(f"💥 Error testing {scenario['name']}: {str(e)}")
            all_results[scenario['name']] = {"error": str(e)}
    
    # Final summary
    print(f"\n{'='*60}")
    print("🎯 FINAL SUMMARY")
    print(f"{'='*60}")
    
    for scenario_name, results in all_results.items():
        if "error" in results:
            print(f"❌ {scenario_name}: FAILED - {results['error']}")
        else:
            success_count = sum(1 for result in results.values() if 'error' not in result)
            total_count = len(results)
            print(f"✅ {scenario_name}: {success_count}/{total_count} tests passed")

if __name__ == "__main__":
    main()
