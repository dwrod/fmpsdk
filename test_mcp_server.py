#!/usr/bin/env python3
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
