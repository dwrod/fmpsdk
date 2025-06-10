# FMPSDK MCP Server

This is a Model Context Protocol (MCP) server that exposes all functions from your Financial Modeling Prep SDK (`fmpsdk`) as MCP tools. This allows you to use your comprehensive financial data SDK with any MCP-compatible client.

## Features

- 🔍 **Automatic Function Discovery**: Automatically discovers and exposes all 156+ functions from your fmpsdk
- 📊 **Comprehensive Coverage**: Includes functions for:
  - Company profiles and financial statements
  - Market data and quotes
  - News and analyst recommendations
  - Technical indicators
  - SEC filings
  - Economic data
  - And much more!
- 🛡️ **Type Safety**: Automatic parameter type inference and validation
- 📝 **Rich Documentation**: Function descriptions and parameter details from docstrings
- ⚡ **High Performance**: Efficient async operation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-mcp.txt
```

### 2. Set Environment Variables

You'll need a Financial Modeling Prep API key:

```bash
export FMP_API_KEY="your_fmp_api_key_here"
export SEC_USER_AGENT="YourName your.email@example.com"  # Optional but recommended for SEC filings
```

### 3. Run Setup and Test

```bash
python setup_mcp.py
python test_mcp_server.py
```

### 4. Start the MCP Server

```bash
python fmpsdk_mcp_server.py
```

## Available Functions

The server exposes all functions from your fmpsdk with the prefix `fmp_`. Here are some examples organized by category:

### Company Information
- `fmp_company_profile` - Get comprehensive company profile
- `fmp_key_executives` - Get key executive information
- `fmp_company_outlook` - Get company outlook and forecasts

### Financial Statements
- `fmp_income_statement` - Get income statement data
- `fmp_balance_sheet_statement` - Get balance sheet data
- `fmp_cash_flow_statement` - Get cash flow statement data

### Market Data
- `fmp_quote` - Get real-time stock quotes
- `fmp_historical_price_full` - Get historical price data
- `fmp_forex` - Get forex rates

### Analysis & Ratings
- `fmp_analyst_estimates` - Get analyst estimates
- `fmp_rating` - Get company ratings
- `fmp_esg_score` - Get ESG scores

### News & Events
- `fmp_stock_news` - Get stock-specific news
- `fmp_earning_calendar` - Get earnings calendar
- `fmp_economic_calendar` - Get economic events

### SEC Filings
- `fmp_sec_filings` - Get SEC filing links
- `fmp_sec_filings_data` - Get full SEC filing content

And many more! Each function includes:
- Detailed descriptions from the original docstrings
- Parameter specifications with types and defaults
- Usage examples

## Configuration for MCP Clients

### Claude Desktop

Add this to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "fmpsdk": {
      "command": "python",
      "args": ["/path/to/your/fmpsdk_mcp_server.py"],
      "env": {
        "FMP_API_KEY": "your_api_key_here",
        "SEC_USER_AGENT": "YourName your.email@example.com"
      }
    }
  }
}
```

### Other MCP Clients

Use the provided `mcp_config.json` as a starting point and adapt it for your specific MCP client.

## Usage Examples

Once connected to an MCP client, you can use the tools like this:

### Get Company Profile
```
Use the fmp_company_profile tool with symbol "AAPL" to get Apple's company profile
```

### Get Financial Statements
```
Use the fmp_income_statement tool with symbol "AAPL", period "quarter", and limit 4 to get Apple's quarterly income statements
```

### Search for Companies
```
Use the fmp_search tool with query "Tesla" to find Tesla-related securities
```

### Get Market Data
```
Use the fmp_quote tool with symbol "AAPL" to get Apple's current stock quote
```

## Function Categories

The server organizes your fmpsdk functions into these categories:

1. **Available Data** (18 functions)
   - Symbol lists, available instruments, country data

2. **Company Profile** (7 functions)
   - Company information, executives, core data

3. **Company Valuation** (18 functions)
   - Ratings, estimates, ESG scores, peer analysis

4. **Financial Statements** (12 functions)
   - Income statements, balance sheets, cash flow, SEC filings

5. **Financial Growth & Ratios** (6 functions)
   - Growth metrics, financial ratios, trend analysis

6. **Market Data & Quotes** (15 functions)
   - Real-time quotes, historical data, forex, commodities

7. **News & Events** (7 functions)
   - Financial news, press releases, RSS feeds

8. **Calendar Data** (6 functions)
   - Earnings calendar, IPO calendar, economic events

9. **Analysis & Recommendations** (6 functions)
   - Price targets, analyst recommendations

10. **Institutional Data** (11 functions)
    - Institutional holdings, Form 13F, ETF data

11. **Market Indexes** (6 functions)
    - S&P 500, NASDAQ, Dow Jones constituents

12. **Alternative Data** (8 functions)
    - COT reports, insider trading, social sentiment

And more!

## Error Handling

The server includes comprehensive error handling:
- Parameter validation
- API rate limiting awareness
- Detailed error messages
- Graceful fallbacks

## Logging

The server logs important events and errors. You can adjust the logging level by modifying the `logging.basicConfig(level=logging.INFO)` line in the server file.

## Development

### Adding New Functions

If you add new functions to your fmpsdk, they will be automatically discovered and exposed by the MCP server. Just restart the server to pick up the changes.

### Customizing Function Behavior

You can modify the `get_function_signature_and_docs()` function to customize how function metadata is extracted and presented.

### Testing

Run the test script to verify everything is working:

```bash
python test_mcp_server.py
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're running the server from the directory containing your fmpsdk
2. **API Key Issues**: Ensure your FMP_API_KEY environment variable is set correctly
3. **Function Not Found**: Check that the function exists in your fmpsdk's `__all__` list

### Getting Help

- Check the server logs for detailed error messages
- Verify your API key has sufficient permissions
- Ensure all dependencies are installed correctly

## License

This MCP server respects the same license as your original fmpsdk package.

---

**Attribution**: Data provided by Financial Modeling Prep 