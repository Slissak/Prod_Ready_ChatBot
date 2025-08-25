#!/usr/bin/env python3
"""
Simple test script to verify frontend configuration works.
"""

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_config_import():
    """Test if config module can be imported."""
    try:
        from config import config
        print("✅ Config module imported successfully")
        print(f"   Environment: {config.environment}")
        print(f"   Backend URL: {config.backend_url}")
        print(f"   Debug: {config.debug}")
        return True
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False

def test_backend_config_import():
    """Test if backend config can be imported."""
    try:
        from backend.app.config import JOB_ROLE_MAPPING
        print("✅ Backend config imported successfully")
        print(f"   Job roles: {list(JOB_ROLE_MAPPING.keys())}")
        return True
    except Exception as e:
        print(f"❌ Backend config import failed: {e}")
        return False

def test_secrets_file():
    """Test if secrets file exists and is readable."""
    secrets_path = ".streamlit/secrets.toml"
    if os.path.exists(secrets_path):
        print(f"✅ Secrets file exists: {secrets_path}")
        try:
            with open(secrets_path, 'r') as f:
                content = f.read()
                print(f"   Content: {content.strip()}")
            return True
        except Exception as e:
            print(f"❌ Secrets file read failed: {e}")
            return False
    else:
        print(f"❌ Secrets file not found: {secrets_path}")
        return False

def main():
    """Run all tests."""
    print("🧪 Frontend Configuration Test")
    print("=" * 40)
    
    tests = [
        test_config_import,
        test_backend_config_import,
        test_secrets_file
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"📊 Test Results: {success_count}/{total_count} passed")
    
    if success_count == total_count:
        print("🎉 All tests passed! Frontend should work correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return success_count == total_count

if __name__ == "__main__":
    main()
