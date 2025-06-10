#!/usr/bin/env python3
"""
Example usage of the FMPSDK MCP Server

This script demonstrates how to test and use various functions
from the fmpsdk through the MCP server interface.
"""

import asyncio
import os
import sys
from typing import Any, Dict

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def demonstrate_functions():
    """Demonstrate various fmpsdk functions through the MCP server."""
    try:
        from fmpsdk_mcp_server import FMPSDK_FUNCTIONS, handle_call_tool
        
        print("🚀 FMPSDK MCP Server Function Demonstration")
        print("=" * 60)
        
        # Check if API key is available
        api_key = os.getenv('FMP_API_KEY')
        if not api_key:
            print("⚠️  Warning: FMP_API_KEY not set. Using demo mode...")
            demo_mode = True
        else:
            print(f"✅ Using API key ending in: ...{api_key[-4:]}")
            demo_mode = False
        
        print(f"📊 Available functions: {len(FMPSDK_FUNCTIONS)}")
        print()
        
        # Demonstrate different categories of functions
        test_cases = [
            {
                "name": "Company Profile",
                "tool": "fmp_company_profile",
                "args": {"symbol": "AAPL", "output": "markdown"},
                "description": "Get Apple's company profile"
            },
            {
                "name": "Search Function",
                "tool": "fmp_search",
                "args": {"query": "Apple", "limit": 5},
                "description": "Search for Apple-related securities"
            },
            {
                "name": "Available Symbols",
                "tool": "fmp_symbols_list",
                "args": {"output": "markdown"},
                "description": "Get list of available stock symbols"
            },
            {
                "name": "Market Quote",
                "tool": "fmp_quote",
                "args": {"symbol": "AAPL", "output": "markdown"},
                "description": "Get real-time quote for Apple"
            },
            {
                "name": "Economic Calendar",
                "tool": "fmp_economic_calendar",
                "args": {"from_date": "2024-01-01", "to_date": "2024-01-31", "output": "markdown"},
                "description": "Get economic events for January 2024"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{i}. Testing {test_case['name']}")
            print(f"   Description: {test_case['description']}")
            print(f"   Tool: {test_case['tool']}")
            print(f"   Arguments: {test_case['args']}")
            
            if demo_mode and test_case['tool'] in ['fmp_company_profile', 'fmp_quote']:
                print("   📋 Result: [Skipped - requires API key]")
            else:
                try:
                    result = await handle_call_tool(test_case['tool'], test_case['args'])
                    if result and len(result) > 0:
                        response = result[0].text
                        # Truncate long responses
                        if len(response) > 300:
                            response = response[:300] + "... [truncated]"
                        print(f"   📋 Result: {response}")
                    else:
                        print("   📋 Result: No data returned")
                except Exception as e:
                    print(f"   ❌ Error: {str(e)}")
            
            print()
        
        # Show function categories
        print("📚 Function Categories:")
        print("-" * 30)
        
        categories = {}
        for func_name in FMPSDK_FUNCTIONS.keys():
            # Categorize functions based on name patterns
            if any(keyword in func_name for keyword in ['company', 'profile', 'executive']):
                category = "Company Information"
            elif any(keyword in func_name for keyword in ['income', 'balance', 'cash_flow', 'financial']):
                category = "Financial Statements"
            elif any(keyword in func_name for keyword in ['quote', 'price', 'market', 'forex']):
                category = "Market Data"
            elif any(keyword in func_name for keyword in ['news', 'analyst', 'rating', 'estimate']):
                category = "News & Analysis"
            elif any(keyword in func_name for keyword in ['calendar', 'earning', 'ipo', 'economic']):
                category = "Calendar Events"
            elif any(keyword in func_name for keyword in ['sec', 'filing']):
                category = "SEC Filings"
            elif any(keyword in func_name for keyword in ['search', 'list', 'available']):
                category = "Data Discovery"
            else:
                category = "Other"
            
            if category not in categories:
                categories[category] = []
            categories[category].append(func_name)
        
        for category, functions in sorted(categories.items()):
            print(f"  📂 {category}: {len(functions)} functions")
            # Show a few examples
            examples = functions[:3]
            for func in examples:
                print(f"     • fmp_{func}")
            if len(functions) > 3:
                print(f"     ... and {len(functions) - 3} more")
            print()
        
        print("✅ Demonstration completed!")
        
        if demo_mode:
            print("\n💡 Tip: Set your FMP_API_KEY environment variable to test API-dependent functions:")
            print("   export FMP_API_KEY='your_api_key_here'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        return False

async def list_all_tools():
    """List all available tools with their descriptions."""
    try:
        from fmpsdk_mcp_server import handle_list_tools
        
        print("\n🔧 All Available MCP Tools:")
        print("=" * 60)
        
        tools = await handle_list_tools()
        
        for i, tool in enumerate(tools, 1):
            print(f"{i:3d}. {tool.name}")
            if tool.description:
                # Truncate long descriptions
                desc = tool.description[:100] + "..." if len(tool.description) > 100 else tool.description
                print(f"      {desc}")
            
            # Show required parameters
            schema = tool.inputSchema
            if schema and "properties" in schema:
                required = schema.get("required", [])
                if required:
                    print(f"      Required: {', '.join(required)}")
            print()
        
        print(f"Total: {len(tools)} tools available")
        return True
        
    except Exception as e:
        print(f"❌ Error listing tools: {e}")
        return False

async def main():
    """Main demonstration function."""
    print("🎯 FMPSDK MCP Server Demonstration")
    print("This script shows how your fmpsdk functions work through the MCP server.")
    print()
    
    # Run demonstrations
    success1 = await demonstrate_functions()
    success2 = await list_all_tools()
    
    if success1 and success2:
        print("\n🎉 All demonstrations completed successfully!")
        print("\nNext steps:")
        print("1. Start the MCP server: python fmpsdk_mcp_server.py")
        print("2. Configure your MCP client (e.g., Claude Desktop)")
        print("3. Start using the financial data tools in your client!")
    else:
        print("\n⚠️  Some demonstrations failed. Check the error messages above.")
    
    return success1 and success2

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 