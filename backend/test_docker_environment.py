#!/usr/bin/env python3
"""
Docker environment variable test script.
Tests the Docker container with proper environment variable injection.
"""

import subprocess
import requests
import time
import json
import os
from typing import Dict, Any

def run_docker_command(cmd: str) -> tuple[int, str, str]:
    """Run a Docker command and return (return_code, stdout, stderr)."""
    print(f"🐳 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def build_docker_image(image_name: str = "chatbot-backend-test") -> bool:
    """Build the Docker image."""
    print("🔨 Building Docker image...")
    
    cmd = f"docker build -t {image_name} ."
    returncode, stdout, stderr = run_docker_command(cmd)
    
    if returncode == 0:
        print("✅ Docker image built successfully")
        return True
    else:
        print(f"❌ Docker build failed:")
        print(f"   STDOUT: {stdout}")
        print(f"   STDERR: {stderr}")
        return False

def run_docker_container(image_name: str, container_name: str, env_vars: Dict[str, str]) -> bool:
    """Run the Docker container with environment variables."""
    print("🚀 Starting Docker container...")
    
    # Build environment variable string
    env_string = " ".join([f"-e {k}={v}" for k, v in env_vars.items()])
    
    cmd = f"docker run -d --name {container_name} -p 8000:8000 {env_string} {image_name}"
    returncode, stdout, stderr = run_docker_command(cmd)
    
    if returncode == 0:
        print(f"✅ Docker container started: {stdout.strip()}")
        return True
    else:
        print(f"❌ Docker container start failed:")
        print(f"   STDOUT: {stdout}")
        print(f"   STDERR: {stderr}")
        return False

def stop_docker_container(container_name: str) -> bool:
    """Stop and remove the Docker container."""
    print(f"🛑 Stopping Docker container: {container_name}")
    
    # Stop container
    cmd_stop = f"docker stop {container_name}"
    returncode_stop, stdout_stop, stderr_stop = run_docker_command(cmd_stop)
    
    # Remove container
    cmd_rm = f"docker rm {container_name}"
    returncode_rm, stdout_rm, stderr_rm = run_docker_command(cmd_rm)
    
    if returncode_stop == 0 and returncode_rm == 0:
        print("✅ Docker container stopped and removed")
        return True
    else:
        print(f"⚠️  Container cleanup issues:")
        if returncode_stop != 0:
            print(f"   Stop error: {stderr_stop}")
        if returncode_rm != 0:
            print(f"   Remove error: {stderr_rm}")
        return False

def get_container_logs(container_name: str) -> str:
    """Get logs from the Docker container."""
    cmd = f"docker logs {container_name}"
    returncode, stdout, stderr = run_docker_command(cmd)
    
    if returncode == 0:
        return stdout
    else:
        return f"Error getting logs: {stderr}"

def wait_for_service(url: str, max_wait: int = 30) -> bool:
    """Wait for the service to be ready."""
    print(f"⏳ Waiting for service at {url}...")
    
    for i in range(max_wait):
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Service is ready after {i+1} seconds")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        if (i + 1) % 5 == 0:
            print(f"   Still waiting... ({i+1}/{max_wait}s)")
    
    print(f"❌ Service not ready after {max_wait} seconds")
    return False

def test_service_endpoints(base_url: str) -> Dict[str, Any]:
    """Test all service endpoints."""
    print(f"🧪 Testing service endpoints at {base_url}")
    
    results = {}
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            results['health'] = response.json()
            print("✅ Health endpoint: PASSED")
        else:
            results['health'] = {"error": f"HTTP {response.status_code}"}
            print(f"❌ Health endpoint: FAILED - HTTP {response.status_code}")
    except Exception as e:
        results['health'] = {"error": str(e)}
        print(f"❌ Health endpoint: FAILED - {str(e)}")
    
    # Test environment endpoint
    try:
        response = requests.get(f"{base_url}/env-test", timeout=10)
        if response.status_code == 200:
            results['environment'] = response.json()
            print("✅ Environment endpoint: PASSED")
        else:
            results['environment'] = {"error": f"HTTP {response.status_code}"}
            print(f"❌ Environment endpoint: FAILED - HTTP {response.status_code}")
    except Exception as e:
        results['environment'] = {"error": str(e)}
        print(f"❌ Environment endpoint: FAILED - {str(e)}")
    
    # Test chat endpoint
    try:
        test_data = {
            "session_id": "docker_test",
            "user_message": "Hi, testing Docker environment"
        }
        response = requests.post(
            f"{base_url}/chat",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            results['chat'] = response.json()
            print("✅ Chat endpoint: PASSED")
        else:
            results['chat'] = {"error": f"HTTP {response.status_code}"}
            print(f"❌ Chat endpoint: FAILED - HTTP {response.status_code}")
    except Exception as e:
        results['chat'] = {"error": str(e)}
        print(f"❌ Chat endpoint: FAILED - {str(e)}")
    
    return results

def main():
    """Main test function."""
    print("🐳 Docker Environment Variable Test")
    print("=" * 50)
    
    # Configuration
    image_name = "chatbot-backend-test"
    container_name = "chatbot-backend-test-container"
    base_url = "http://localhost:8000"
    
    # Get environment variables from .env file or environment
    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "PINECONE_INDEX_NAME": os.getenv("PINECONE_INDEX_NAME")
    }
    
    # Check if all environment variables are available
    missing_vars = [k for k, v in env_vars.items() if not v]
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("Please ensure all required environment variables are set.")
        return
    
    print("✅ All environment variables are available")
    
    try:
        # Step 1: Build Docker image
        if not build_docker_image(image_name):
            print("❌ Failed to build Docker image")
            return
        
        # Step 2: Run Docker container
        if not run_docker_container(image_name, container_name, env_vars):
            print("❌ Failed to start Docker container")
            return
        
        # Step 3: Wait for service to be ready
        if not wait_for_service(base_url):
            print("❌ Service failed to start")
            print("Container logs:")
            print(get_container_logs(container_name))
            return
        
        # Step 4: Test service endpoints
        results = test_service_endpoints(base_url)
        
        # Step 5: Print results summary
        print(f"\n📊 TEST RESULTS SUMMARY:")
        print(f"{'='*30}")
        
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
            print("🎉 ALL TESTS PASSED! Docker environment is properly configured.")
        else:
            print("⚠️  Some tests failed. Check the logs above for details.")
        
        # Step 6: Show container logs for debugging
        print(f"\n📋 CONTAINER LOGS:")
        print(f"{'='*30}")
        logs = get_container_logs(container_name)
        print(logs)
        
    except Exception as e:
        print(f"💥 Test failed with exception: {str(e)}")
    
    finally:
        # Cleanup: Stop and remove container
        stop_docker_container(container_name)

if __name__ == "__main__":
    main()
