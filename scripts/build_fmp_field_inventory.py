#!/usr/bin/env python3
"""
Build deterministic FMP endpoint field inventory via API introspection.

GEN-127: This script calls each FMP endpoint and captures the actual field
names returned, creating a deterministic inventory for LLM schema planning.

Usage:
    cd src/fmpsdk
    poetry run python scripts/build_fmp_field_inventory.py

    # Or with specific endpoints:
    poetry run python scripts/build_fmp_field_inventory.py --endpoints income_statement,quote

    # Dry run (show what would be introspected):
    poetry run python scripts/build_fmp_field_inventory.py --dry-run

Output:
    fmpsdk/fmp_endpoint_fields.py

Requirements:
    - FMP_API_KEY environment variable set
    - Valid FMP API subscription
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import fmpsdk
from fmpsdk.fmp_registry import FMP_REGISTRY
from fmpsdk.endpoint_params import (
    ENDPOINT_PARAMS,
    get_introspectable_endpoints,
    get_skipped_endpoints,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Rate limiting - FMP has API limits
REQUEST_DELAY = 1.5  # seconds between API calls

# Output file path
OUTPUT_PATH = Path(__file__).parent.parent / "fmpsdk" / "fmp_endpoint_fields.py"


def extract_fields(data: Any, max_depth: int = 2) -> Set[str]:
    """
    Extract field names from API response.

    Handles various response formats:
    - List of dicts (most common)
    - Single dict
    - Nested structures (flattened to top level)

    :param data: API response data.
    :param max_depth: Maximum nesting depth to extract.
    :return: Set of field names.
    """
    if not data:
        return set()

    fields = set()

    # Handle list of dicts (most common FMP pattern)
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            # Extract from first item (all items have same structure)
            fields = _extract_dict_fields(data[0], max_depth)
        return fields

    # Handle single dict
    if isinstance(data, dict):
        fields = _extract_dict_fields(data, max_depth)
        return fields

    return fields


def _extract_dict_fields(d: dict, depth: int, prefix: str = "") -> Set[str]:
    """
    Recursively extract field names from a dict.

    :param d: Dictionary to extract from.
    :param depth: Remaining depth to traverse.
    :param prefix: Prefix for nested field names.
    :return: Set of field names.
    """
    fields = set()

    for key, value in d.items():
        field_name = f"{prefix}{key}" if prefix else key
        fields.add(field_name)

        # Only go one level deep for nested structures
        # This avoids over-complicating the field inventory
        if depth > 1 and isinstance(value, dict):
            nested = _extract_dict_fields(value, depth - 1, f"{field_name}.")
            fields.update(nested)

    return fields


def introspect_endpoint(endpoint_name: str) -> Optional[Set[str]]:
    """
    Call an endpoint and extract its field names.

    :param endpoint_name: Name of the endpoint from FMP_REGISTRY.
    :return: Set of field names, or None if introspection failed.
    """
    registry_entry = FMP_REGISTRY.get(endpoint_name)
    if not registry_entry:
        logger.warning(f"Endpoint not in registry: {endpoint_name}")
        return None

    param_config = ENDPOINT_PARAMS.get(endpoint_name)
    if not param_config:
        logger.warning(f"No param config for {endpoint_name}, skipping")
        return None

    if param_config.get("type") == "skip":
        reason = param_config.get("reason", "No reason")
        logger.info(f"Skipping {endpoint_name}: {reason}")
        return None

    func_name = registry_entry.function
    func = getattr(fmpsdk, func_name, None)
    if not func:
        logger.warning(f"Function not found in fmpsdk: {func_name}")
        return None

    try:
        result = _call_endpoint(func, func_name, param_config)

        if result is None:
            logger.warning(f"[EMPTY] {endpoint_name}: API returned None")
            return None

        fields = extract_fields(result)
        if fields:
            logger.info(f"[OK] {endpoint_name}: {len(fields)} fields")
            return fields
        else:
            logger.warning(f"[EMPTY] {endpoint_name}: No fields extracted")
            return None

    except Exception as e:
        logger.error(f"[ERROR] {endpoint_name}: {e}")
        return None


def _get_supported_kwargs(func: callable) -> set:
    """
    Get the set of keyword arguments a function supports.

    :param func: The function to inspect.
    :return: Set of supported parameter names.
    """
    import inspect

    try:
        sig = inspect.signature(func)
        return set(sig.parameters.keys())
    except (ValueError, TypeError):
        return set()


def _call_endpoint(func: callable, func_name: str, param_config: dict) -> Any:
    """
    Call an FMP endpoint with appropriate parameters.

    :param func: The fmpsdk function to call.
    :param func_name: Function name (for logging).
    :param param_config: Parameter configuration from ENDPOINT_PARAMS.
    :return: API response data.
    """
    param_type = param_config.get("type")

    # Get supported kwargs for this function
    supported = _get_supported_kwargs(func)

    # Build kwargs based on what the function supports
    kwargs = {}
    if "output" in supported:
        kwargs["output"] = "json"

    if param_type == "symbol":
        if "limit" in supported:
            kwargs["limit"] = 1
        return func(param_config["sample"], **kwargs)

    elif param_type == "symbol_kwarg":
        # Some functions take symbol as kwarg
        if "limit" in supported:
            kwargs["limit"] = 1
        return func(symbol=param_config["sample"], **kwargs)

    elif param_type == "none":
        return func(**kwargs) if kwargs else func()

    elif param_type == "date_range":
        return func(
            from_date=param_config["from"],
            to_date=param_config["to"],
            **kwargs,
        )

    elif param_type == "date":
        return func(param_config["sample"], **kwargs)

    elif param_type == "exchange":
        return func(param_config["sample"], **kwargs)

    elif param_type == "cik":
        return func(param_config["sample"], **kwargs)

    elif param_type == "year":
        return func(param_config["sample"], **kwargs)

    elif param_type == "indicator":
        return func(param_config["sample"], **kwargs)

    elif param_type == "technical":
        return func(
            param_config["symbol"],
            period=param_config["period"],
            statistics_type=param_config["statistics_type"],
            **kwargs,
        )

    elif param_type == "chart":
        return func(
            param_config["symbol"],
            param_config["timeframe"],
            from_date=param_config.get("from_date"),
            to_date=param_config.get("to_date"),
            **kwargs,
        )

    elif param_type == "forex_historical":
        return func(
            param_config["symbol"],
            from_date=param_config["from_date"],
            to_date=param_config["to_date"],
            **kwargs,
        )

    elif param_type == "commodity":
        return func(
            param_config["symbol"],
            from_date=param_config["from_date"],
            to_date=param_config["to_date"],
            **kwargs,
        )

    elif param_type == "screener":
        # Stock screener has its own specific signature
        return func(
            market_cap_more_than=param_config.get("market_cap_more_than"),
            sector=param_config.get("sector"),
            limit=param_config.get("limit", 10),
        )

    elif param_type == "cot_analysis":
        return func(
            param_config["symbol"],
            from_date=param_config["from_date"],
            to_date=param_config["to_date"],
            **kwargs,
        )

    elif param_type == "company":
        # Functions that take company name (e.g., upgrades_downgrades_by_company)
        return func(param_config["sample"], **kwargs)

    elif param_type == "analyst_name":
        # Functions that take analyst name
        return func(param_config["sample"], **kwargs)

    elif param_type == "search_name":
        # Functions that search by name
        return func(param_config["sample"], **kwargs)

    elif param_type == "ticker":
        # Functions that take ticker explicitly
        return func(param_config["sample"], **kwargs)

    else:
        logger.warning(f"Unknown param type: {param_type} for {func_name}")
        return None


def build_inventory(
    endpoints: Optional[List[str]] = None,
    delay: float = REQUEST_DELAY,
) -> Dict[str, List[str]]:
    """
    Build complete field inventory for all (or specified) endpoints.

    :param endpoints: Optional list of specific endpoints to introspect.
    :param delay: Delay between API calls for rate limiting.
    :return: Dict mapping endpoint names to sorted list of field names.
    """
    inventory: Dict[str, List[str]] = {}

    # Determine which endpoints to process
    if endpoints:
        to_process = [e for e in endpoints if e in ENDPOINT_PARAMS]
    else:
        to_process = get_introspectable_endpoints()

    total = len(to_process)
    logger.info(f"Starting introspection of {total} endpoints...")

    for i, endpoint_name in enumerate(to_process, 1):
        logger.info(f"[{i}/{total}] Processing: {endpoint_name}")

        fields = introspect_endpoint(endpoint_name)
        if fields:
            inventory[endpoint_name] = sorted(list(fields))

        # Rate limiting between calls
        if i < total:
            time.sleep(delay)

    return inventory


def write_inventory(inventory: Dict[str, List[str]], output_path: Path) -> None:
    """
    Write inventory as a Python module.

    :param inventory: Field inventory dict.
    :param output_path: Output file path.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    total_fields = sum(len(fields) for fields in inventory.values())

    content = f'''"""
FMP Endpoint Field Inventory.

Auto-generated via API introspection. DO NOT EDIT MANUALLY.

GEN-127: This module provides deterministic field listings for each FMP endpoint,
enabling the schema planning LLM to know exactly what data is available.

Generated: {timestamp}
Total endpoints: {len(inventory)}
Total field mappings: {total_fields}

Usage:
    from fmpsdk.fmp_endpoint_fields import FMP_ENDPOINT_FIELDS

    # Get fields for an endpoint
    fields = FMP_ENDPOINT_FIELDS.get("income_statement", [])

    # Check if a field exists
    "revenue" in FMP_ENDPOINT_FIELDS.get("income_statement", [])
"""

from typing import Dict, List

FMP_ENDPOINT_FIELDS: Dict[str, List[str]] = {json.dumps(inventory, indent=2, sort_keys=True)}
'''

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)

    logger.info(f"Wrote {len(inventory)} endpoints to {output_path}")


def print_summary(inventory: Dict[str, List[str]]) -> None:
    """Print introspection summary."""
    total_endpoints = len(ENDPOINT_PARAMS)
    introspected = len(inventory)
    skipped = len(get_skipped_endpoints())
    failed = total_endpoints - introspected - skipped

    total_fields = sum(len(fields) for fields in inventory.values())

    print("\n" + "=" * 60)
    print("FMP FIELD INVENTORY SUMMARY")
    print("=" * 60)
    print(f"Total endpoints in registry:  {total_endpoints}")
    print(f"Successfully introspected:    {introspected}")
    print(f"Skipped (variable/text):      {skipped}")
    print(f"Failed:                       {failed}")
    print(f"Coverage:                     {introspected/total_endpoints*100:.1f}%")
    print(f"Total field mappings:         {total_fields}")
    print("=" * 60)

    if skipped:
        print("\nSkipped endpoints (variable fields or text content):")
        for name, reason in sorted(get_skipped_endpoints().items()):
            print(f"  - {name}: {reason}")

    # Show top 10 endpoints by field count
    print("\nTop 10 endpoints by field count:")
    sorted_by_count = sorted(
        inventory.items(), key=lambda x: len(x[1]), reverse=True
    )[:10]
    for name, fields in sorted_by_count:
        print(f"  {name}: {len(fields)} fields")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build FMP endpoint field inventory via API introspection"
    )
    parser.add_argument(
        "--endpoints",
        type=str,
        help="Comma-separated list of specific endpoints to introspect",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=REQUEST_DELAY,
        help=f"Delay between API calls (default: {REQUEST_DELAY}s)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(OUTPUT_PATH),
        help=f"Output file path (default: {OUTPUT_PATH})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be introspected without making API calls",
    )

    args = parser.parse_args()

    # Check for API key
    if not os.environ.get("FMP_API_KEY"):
        logger.error("FMP_API_KEY environment variable not set")
        sys.exit(1)

    # Parse endpoints if specified
    endpoints = None
    if args.endpoints:
        endpoints = [e.strip() for e in args.endpoints.split(",")]

    # Dry run mode
    if args.dry_run:
        to_process = endpoints or get_introspectable_endpoints()
        print(f"\nDry run - would introspect {len(to_process)} endpoints:")
        for ep in sorted(to_process):
            config = ENDPOINT_PARAMS.get(ep, {})
            print(f"  {ep}: {config.get('type', 'unknown')}")

        print(f"\nSkipped endpoints ({len(get_skipped_endpoints())}):")
        for name, reason in sorted(get_skipped_endpoints().items()):
            print(f"  {name}: {reason}")
        return

    # Build inventory
    inventory = build_inventory(endpoints=endpoints, delay=args.delay)

    # Write output
    output_path = Path(args.output)
    write_inventory(inventory, output_path)

    # Print summary
    print_summary(inventory)


if __name__ == "__main__":
    main()
