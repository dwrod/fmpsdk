# fmpsdk Development Guide

## Overview

This is a **forked and customized** Python SDK for the [Financial Modeling Prep (FMP) API](https://financialmodelingprep.com). The original SDK was created by Dax Mickelson; this fork is maintained by David Rodriguez with substantial modifications for LLM integration and GenAI.Financial use cases.

**Key Differences from Original:**
- Default output format changed from JSON to **Markdown tables** (LLM-friendly)
- Added data compression utilities for efficient LLM consumption
- Custom `sec_filings_data()` function that fetches and parses actual SEC filing content
- MCP (Model Context Protocol) server integration
- Precision control for numeric values

## Project Structure

```
fmpsdk/
├── __init__.py          # Root package (re-exports fmpsdk/)
├── fmpsdk/              # Main SDK package
│   ├── __init__.py      # Exports 159 public functions
│   ├── url_methods.py   # Core HTTP methods (__return_json_v3, __return_json_v4)
│   ├── settings.py      # Constants (BASE_URLs, valid values, filenames)
│   ├── data_compression.py  # Output formatting (TSV, Markdown, JSON)
│   │
│   ├── # Financial Data Modules
│   ├── financial_statements.py   # Income, balance sheet, cash flow, SEC filings
│   ├── company_profile.py        # Company info, executives, metrics
│   ├── company_valuation.py      # Ratings, peers, analysts, ESG
│   ├── financial_growth_ratios.py # Growth metrics, ratios
│   ├── valuation_metrics.py      # DCF, market cap
│   │
│   ├── # Market Data Modules
│   ├── quote.py                  # Real-time quotes, forex, crypto
│   ├── stock_time_series.py      # Historical prices, dividends, splits
│   ├── stock_market.py           # Gainers, losers, sectors
│   ├── market_indexes.py         # S&P 500, NASDAQ, Dow Jones constituents
│   ├── technical_indicators.py   # SMA, EMA, RSI, etc.
│   │
│   ├── # Alternative Data Modules
│   ├── news.py                   # Stock news, press releases
│   ├── calendar_data.py          # Earnings, dividends, IPO calendars
│   ├── insider_trading.py        # Insider transactions
│   ├── institutional_fund.py     # 13F filings, ETF holdings
│   ├── senate.py                 # Senate trading disclosures
│   ├── social_sentiment.py       # Social media sentiment
│   │
│   ├── # Reference Data Modules
│   ├── available_data.py         # Symbol lists, exchanges, sectors
│   ├── search_functions.py       # Ticker/company search
│   └── ...
│
├── fmpsdk_mcp_server.py  # MCP server for Claude Desktop
├── example_usage.py      # Usage examples
├── pyproject.toml        # Poetry config (Python 3.12+)
└── README.md
```

## Environment Variables

```bash
FMP_API_KEY=your_fmp_api_key        # Required - get from financialmodelingprep.com
SEC_USER_AGENT=your_email@domain    # Required for SEC filing downloads
```

## Code Patterns

### Function Signature Pattern

All public functions follow this pattern:

```python
def function_name(
    symbol: str,                           # Usually required
    period: str = "annual",                # "annual" or "quarter"
    limit: int = DEFAULT_LIMIT,            # Default is 10
    output: str = 'markdown',              # 'markdown', 'tsv', or 'json'
    precision: typing.Optional[int] = 5    # Decimal places (some functions)
) -> typing.Union[typing.List[typing.Dict], str]:
```

### Output Formats

```python
# Markdown (default) - best for LLM consumption
fmpsdk.income_statement('AAPL', output='markdown')
# Returns: "| date | revenue | netIncome | ... |\n|---|---|---| ..."

# JSON - best for programmatic access
fmpsdk.income_statement('AAPL', output='json')
# Returns: [{"date": "2024-09-28", "revenue": 391035000000, ...}, ...]

# TSV - compact tabular format
fmpsdk.income_statement('AAPL', output='tsv')
# Returns: "date\trevenue\tnetIncome\n2024-09-28\t391035000000\t..."
```

### API Version Routing

- **v3 API** (`__return_json_v3`): Most endpoints - financial statements, quotes, company data
- **v4 API** (`__return_json_v4`): Newer endpoints - batch transcripts, core info, outlook

### Error Handling

Functions return `None` on API errors (logged to console). Check return values:

```python
result = fmpsdk.company_profile('AAPL')
if result is None:
    # Handle error - check logs for details
```

## Key Functions for Case Studies

### Financial Statements
```python
fmpsdk.income_statement(symbol, period='annual', limit=10)
fmpsdk.balance_sheet_statement(symbol, period='annual', limit=10)
fmpsdk.cash_flow_statement(symbol, period='annual', limit=10)
```

### SEC Filings (Custom Enhancement)
```python
# Get filing metadata (links only)
fmpsdk.sec_filings(symbol, filing_type='10-K', limit=5)

# Get actual filing CONTENT as Markdown (LLM-ready)
fmpsdk.sec_filings_data(symbol, filing_type='10-K', limit=1)
# WARNING: Full 10-K content is VERY long (100k+ tokens)
```

### Earnings & Transcripts
```python
fmpsdk.earning_call_transcript(symbol, year=2024, quarter=1)
fmpsdk.batch_earning_call_transcript(symbol, year=2024)
fmpsdk.earning_call_transcripts_available_dates(symbol)
```

### Company Analysis
```python
fmpsdk.company_profile(symbol)          # Overview, CEO, sector, etc.
fmpsdk.key_metrics(symbol, period='annual', limit=10)
fmpsdk.financial_ratios(symbol, period='annual', limit=10)
fmpsdk.analyst_estimates(symbol)
fmpsdk.analyst_recommendation(symbol)
```

### News & Events
```python
fmpsdk.stock_news(symbol, limit=50)
fmpsdk.press_releases(symbol, limit=20)
fmpsdk.earning_calendar(from_date='2024-01-01', to_date='2024-12-31')
```

## Development Guidelines

### Before Every Commit

```bash
# Run local code review
/review-staged

# Fix any issues found
/fix-review
```

### Adding New Endpoints

1. Identify the FMP API endpoint and version (v3 or v4)
2. Add function to appropriate module (or create new module)
3. Follow the standard function signature pattern
4. Add to `__init__.py` imports and `__all__` list
5. Include docstring with `:param`, `:return`, `:example:`
6. Run `/review-staged` to verify

### Testing

```bash
# Run tests (when implemented)
cd src/fmpsdk
poetry run pytest

# Manual testing
poetry run python -c "import fmpsdk; print(fmpsdk.company_profile('AAPL'))"
```

### Linting

```bash
poetry run black fmpsdk/
poetry run isort fmpsdk/
poetry run flake8 fmpsdk/
poetry run mypy fmpsdk/
```

## Code Review

Local code review is configured via `.claude/` directory:

```
.claude/
├── agents/
│   └── code-reviewer.md    # Review rules and patterns
└── commands/
    ├── review-staged.md    # /review-staged command
    └── fix-review.md       # /fix-review command
```

### BLOCK-Level Checks (Must Fix)
1. Missing `API_KEY` usage from environment variable
2. Wrong API version (v3 vs v4) for endpoint
3. Missing `format_output()` call when function has `output` param
4. New public function not exported in `__init__.py`
5. Inconsistent function signature pattern
6. Missing type hints on public functions
7. File writes without context manager

### WARN-Level Checks (Should Fix)
1. Missing docstring
2. Missing `:example:` in docstring
3. Hardcoded limit instead of `DEFAULT_LIMIT`
4. Missing period validation (`__validate_period`)
5. Broad exception handling
6. Missing error logging

## Known Issues / TODO

1. **Rate Limiting**: No built-in rate limiting - FMP has limits based on plan
2. **Async Support**: All functions are synchronous (uses `requests`)
3. **Test Coverage**: Minimal test coverage
4. **Type Hints**: Partially implemented
5. **README Outdated**: States "synced as of 20210220" - many newer endpoints exist

## FMP API Reference

- Full API docs: https://site.financialmodelingprep.com/developer/docs
- 159+ endpoints currently implemented
- ~150+ additional endpoints available in FMP API not yet in SDK

## Git Submodule Note

This repository is included as a git submodule in the parent GenAI.Financial project at `src/fmpsdk/`. Changes should be committed to both the submodule and the parent repository.

```bash
# After making changes to fmpsdk
cd src/fmpsdk
git add . && git commit -m "feat: Description"
git push origin main

# Then in parent repo
cd ../..
git add src/fmpsdk
git commit -m "chore: Update fmpsdk submodule"
```
