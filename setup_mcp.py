#!/usr/bin/env python3
"""
Setup script for the FMPSDK MCP Server

This script helps set up and test the MCP server configuration.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import mcp
        print("✅ MCP library found")
    except ImportError:
        print("❌ MCP library not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-mcp.txt"])
        print("✅ MCP library installed")
    
    try:
        # Try to import the fmpsdk from current directory
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import fmpsdk
        print(f"✅ FMPSDK found with {len(fmpsdk.__all__ if hasattr(fmpsdk, '__all__') else [])} functions")
    except ImportError as e:
        print(f"❌ FMPSDK not found: {e}")
        return False
    
    return True

def check_environment():
    """Check environment variables."""
    print("\n🔍 Checking environment variables...")
    
    fmp_key = os.getenv('FMP_API_KEY')
    if fmp_key:
        print(f"✅ FMP_API_KEY found (ending in ...{fmp_key[-4:]})")
    else:
        print("⚠️  FMP_API_KEY not set. You'll need this for API calls.")
    
    sec_agent = os.getenv('SEC_USER_AGENT')
    if sec_agent:
        print(f"✅ SEC_USER_AGENT found: {sec_agent}")
    else:
        print("⚠️  SEC_USER_AGENT not set. Recommended for SEC filing functions.")
    
    return bool(fmp_key)

def test_function_discovery():
    """Test that the server can discover functions."""
    print("\n🔍 Testing function discovery...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import fmpsdk
        
        functions = []
        if hasattr(fmpsdk, '__all__'):
            for func_name in fmpsdk.__all__:
                try:
                    func = getattr(fmpsdk, func_name)
                    if callable(func):
                        functions.append(func_name)
                except AttributeError:
                    pass
        
        print(f"✅ Discovered {len(functions)} callable functions")
        
        # Show some example functions by category
        categories = {
            "Company Data": [f for f in functions if any(keyword in f for keyword in ['company', 'profile', 'executive'])],
            "Financial Statements": [f for f in functions if any(keyword in f for keyword in ['income', 'balance', 'cash_flow'])],
            "Market Data": [f for f in functions if any(keyword in f for keyword in ['quote', 'price', 'market'])],
            "News & Analysis": [f for f in functions if any(keyword in f for keyword in ['news', 'analyst', 'rating'])],
        }
        
        for category, funcs in categories.items():
            if funcs:
                print(f"  📊 {category}: {len(funcs)} functions (e.g., {funcs[0]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error discovering functions: {e}")
        return False

def create_test_script():
    """Create a simple test script."""
    test_script = '''#!/usr/bin/env python3
"""
Simple test script for the FMPSDK MCP Server
"""

import asyncio
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_server():
    """Test basic server functionality."""
    try:
        from fmpsdk_mcp_server import FMPSDK_FUNCTIONS, handle_list_tools
        
        print(f"✅ Server module loaded successfully")
        print(f"📊 Found {len(FMPSDK_FUNCTIONS)} functions")
        
        # Test tool listing
        tools = await handle_list_tools()
        print(f"🔧 Generated {len(tools)} MCP tools")
        
        # Show some example tools
        for i, tool in enumerate(tools[:5]):
            print(f"  {i+1}. {tool.name}: {tool.description[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)
'''
    
    with open("test_mcp_server.py", "w") as f:
        f.write(test_script)
    
    print("\n📝 Created test_mcp_server.py")

def main():
    """Main setup function."""
    print("🚀 Setting up FMPSDK MCP Server")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        return False
    
    # Check environment
    env_ok = check_environment()
    
    # Test function discovery
    if not test_function_discovery():
        print("\n❌ Function discovery failed")
        return False
    
    # Create test script
    create_test_script()
    
    print("\n✅ Setup completed successfully!")
    
    if not env_ok:
        print("\n⚠️  Important: Set your FMP_API_KEY environment variable:")
        print("   export FMP_API_KEY='your_api_key_here'")
    
    print("\n📖 Next steps:")
    print("1. Test the server: python test_mcp_server.py")
    print("2. Run the server: python fmpsdk_mcp_server.py")
    print("3. Configure your MCP client with mcp_config.json")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 