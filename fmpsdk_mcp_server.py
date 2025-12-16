#!/usr/bin/env python3
"""
Financial Modeling Prep (FMP) MCP Server

This server exposes all functions from the fmpsdk package as MCP tools,
providing comprehensive access to financial data APIs.
"""

import asyncio
import inspect
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Add the current directory to the path to import fmpsdk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import fmpsdk
except ImportError as e:
    logging.error(f"Failed to import fmpsdk: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fmpsdk-mcp-server")

# Initialize the MCP server
server = Server("fmpsdk")

def get_function_signature_and_docs(func) -> Dict[str, Any]:
    """Extract function signature, parameters, and documentation."""
    try:
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or ""
        
        # Parse parameters
        parameters = {}
        for name, param in sig.parameters.items():
            param_info = {
                "type": "string",  # Default type
                "required": param.default == inspect.Parameter.empty
            }
            
            # Try to infer type from annotation
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == str:
                    param_info["type"] = "string"
                elif param.annotation == int:
                    param_info["type"] = "integer"
                elif param.annotation == float:
                    param_info["type"] = "number"
                elif param.annotation == bool:
                    param_info["type"] = "boolean"
                elif hasattr(param.annotation, "__origin__"):
                    # Handle Union types (like Optional)
                    if param.annotation.__origin__ == Union:
                        args = param.annotation.__args__
                        if len(args) == 2 and type(None) in args:
                            # This is Optional[T]
                            non_none_type = next(arg for arg in args if arg != type(None))
                            if non_none_type == str:
                                param_info["type"] = "string"
                            elif non_none_type == int:
                                param_info["type"] = "integer"
                            elif non_none_type == float:
                                param_info["type"] = "number"
                            elif non_none_type == bool:
                                param_info["type"] = "boolean"
                        elif str in args or list in args:
                            param_info["type"] = "string"
            
            # Set default value if available
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
                param_info["required"] = False
            
            parameters[name] = param_info
        
        return {
            "parameters": parameters,
            "description": doc,
            "function": func
        }
    except Exception as e:
        logger.error(f"Error analyzing function {func.__name__}: {e}")
        return {
            "parameters": {},
            "description": f"Function: {func.__name__}",
            "function": func
        }

def discover_fmpsdk_functions() -> Dict[str, Dict[str, Any]]:
    """
    Discover all available functions in the fmpsdk package.

    GEN-91: Uses FMP_REGISTRY as source of truth with whitelist validation.
    This ensures only curated API endpoints are exposed, not helper functions.
    """
    functions = {}

    # GEN-91: Use FMP_REGISTRY for curated endpoint discovery
    try:
        from fmpsdk import FMP_REGISTRY
        # Auto-generate whitelist from registry
        allowed_functions = frozenset(ep.function for ep in FMP_REGISTRY.values())

        for endpoint_name, endpoint in FMP_REGISTRY.items():
            func_name = endpoint.function

            # Whitelist validation (defense-in-depth)
            if func_name not in allowed_functions:
                logger.warning(f"Function {func_name} not in whitelist, skipping")
                continue

            try:
                func = getattr(fmpsdk, func_name, None)
                if func is None or not callable(func):
                    logger.warning(f"Function {func_name} not found or not callable")
                    continue

                # GEN-92: Extract parameters from function signatures (source of truth)
                # Use registry for description only
                sig_info = get_function_signature_and_docs(func)
                func_info = {
                    "parameters": sig_info["parameters"],  # From function signature
                    "description": endpoint.description,   # From registry (curated)
                    "function": func,
                }
                functions[func_name] = func_info
                logger.info(f"Discovered function: {func_name}")
            except Exception as e:
                logger.error(f"Error processing function {func_name}: {e}")

    except ImportError:
        logger.warning("FMP_REGISTRY not available, falling back to __all__")
        # Fallback to original behavior if registry not available
        if hasattr(fmpsdk, '__all__'):
            for func_name in fmpsdk.__all__:
                try:
                    func = getattr(fmpsdk, func_name)
                    if callable(func):
                        func_info = get_function_signature_and_docs(func)
                        functions[func_name] = func_info
                        logger.info(f"Discovered function: {func_name}")
                except AttributeError:
                    logger.warning(f"Function {func_name} not found in fmpsdk")
                except Exception as e:
                    logger.error(f"Error processing function {func_name}: {e}")

    logger.info(f"Discovered {len(functions)} functions from fmpsdk")
    return functions

# Discover all available functions
FMPSDK_FUNCTIONS = discover_fmpsdk_functions()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available FMP SDK tools."""
    tools = []
    
    for func_name, func_info in FMPSDK_FUNCTIONS.items():
        # Create the tool schema
        properties = {}
        required = []
        
        for param_name, param_info in func_info["parameters"].items():
            properties[param_name] = {
                "type": param_info["type"],
                "description": f"Parameter: {param_name}"
            }
            if "default" in param_info:
                properties[param_name]["default"] = param_info["default"]
            if param_info.get("required", False):
                required.append(param_name)
        
        tool = types.Tool(
            name=f"fmp_{func_name}",
            description=func_info["description"][:500] + "..." if len(func_info["description"]) > 500 else func_info["description"],
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": required
            }
        )
        tools.append(tool)
    
    return tools

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    """Handle tool calls to FMP SDK functions."""
    if not name.startswith("fmp_"):
        raise ValueError(f"Unknown tool: {name}")
    
    func_name = name[4:]  # Remove "fmp_" prefix
    
    if func_name not in FMPSDK_FUNCTIONS:
        raise ValueError(f"Unknown FMP function: {func_name}")
    
    func_info = FMPSDK_FUNCTIONS[func_name]
    func = func_info["function"]
    
    try:
        # Prepare arguments
        kwargs = {}
        if arguments:
            for key, value in arguments.items():
                if key in func_info["parameters"]:
                    kwargs[key] = value
        
        # Call the function
        logger.info(f"Calling {func_name} with arguments: {kwargs}")
        result = func(**kwargs)
        
        # Format the result
        if result is None:
            response = "No data returned"
        elif isinstance(result, str):
            response = result
        elif isinstance(result, (list, dict)):
            # Convert to string representation
            if isinstance(result, list) and len(result) > 100:
                response = f"Returned {len(result)} items. First 5 items:\n" + str(result[:5])
            else:
                response = str(result)
        else:
            response = str(result)
        
        return [types.TextContent(type="text", text=response)]
        
    except Exception as e:
        error_msg = f"Error calling {func_name}: {str(e)}"
        logger.error(error_msg)
        return [types.TextContent(type="text", text=error_msg)]

async def main():
    """Main entry point for the MCP server."""
    # Check for required environment variables
    if not os.getenv('FMP_API_KEY'):
        logger.warning("FMP_API_KEY environment variable not set. Some functions may fail.")
    
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fmpsdk",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 