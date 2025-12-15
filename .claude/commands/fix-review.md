# Fix Review Issues Command

Automatically fix issues found by `/review-staged`.

**Goal:** Quickly resolve common issues identified during code review.

## Process

### Step 1: Re-run Review

First, identify current issues:
```bash
/review-staged
```

### Step 2: Auto-fixable Issues

For each BLOCK issue, apply the fix:

#### Missing format_output
Add the format_output wrapper:
```python
# Before
return result

# After
return format_output(result, output)
```

#### Missing __init__.py Export
Add import and __all__ entry:
```python
# In fmpsdk/__init__.py, add:
from .module_name import function_name

# In __all__ list, add:
"function_name",
```

#### Missing Type Hints
Add standard type hints:
```python
# Before
def my_function(symbol, period="annual", limit=10):

# After
def my_function(
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
```

#### Hardcoded Limit
Replace with constant:
```python
# Before
limit: int = 10

# After
limit: int = DEFAULT_LIMIT
```

#### Missing Period Validation
Add validation call:
```python
# Before
query_vars = {"period": period}

# After
query_vars = {"period": __validate_period(period)}
```

### Step 3: Manual Fixes Required

Some issues require manual intervention:

- **Wrong API version**: Verify against FMP API docs which version to use
- **Missing docstring**: Write meaningful documentation
- **Broad exception handling**: Determine specific exceptions to catch

### Step 4: Verify Fixes

After applying fixes:
```bash
/review-staged
```

Confirm all BLOCK issues are resolved.

## Usage

```bash
# Run after /review-staged shows issues
/fix-review

# Or fix specific file
/fix-review fmpsdk/financial_statements.py
```

## Quick Fix Templates

### Standard Function Template
```python
def function_name(
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Brief description of what this function does.

    :param symbol: Company ticker (e.g., 'AAPL').
    :param period: 'quarter' or 'annual'. Default is 'annual'.
    :param limit: Number of records to retrieve. Default is DEFAULT_LIMIT.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: Data in the specified format.
    :example: function_name('AAPL', period='quarter', limit=5)
    """
    path = f"endpoint-path/{symbol}"
    query_vars = {
        "apikey": API_KEY,
        "period": __validate_period(period),
        "limit": limit,
    }
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)
```

### Required Imports for New Modules
```python
import typing
import os

from .settings import DEFAULT_LIMIT
from .url_methods import (
    __return_json_v3,
    __return_json_v4,
    __validate_period,
)
from .data_compression import format_output

API_KEY = os.getenv('FMP_API_KEY')
```
