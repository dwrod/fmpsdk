"""
FMP Endpoint Parameter Mapping for API Introspection.

This module defines how to call each FMP endpoint for field introspection.
Each endpoint is mapped to a parameter configuration that tells the
introspection script what arguments to pass.

GEN-127: Enables deterministic field inventory generation.

Parameter Types:
- symbol: Requires a stock ticker (e.g., 'AAPL')
- symbol_list: Requires a comma-separated list of tickers
- none: No required parameters
- date_range: Requires from_date and to_date
- date: Requires a single date parameter
- exchange: Requires an exchange code (e.g., 'NYSE')
- cik: Requires a CIK number
- transcript: Requires symbol + year + quarter
- technical: Requires symbol + period + statistics_type
- chart: Requires symbol + timeframe
- skip: Skip introspection (variable fields, text content, etc.)
"""

from typing import Any, Dict

# Sample data for introspection
SAMPLE_SYMBOL = "AAPL"
SAMPLE_SYMBOLS = "AAPL,MSFT,GOOGL"
SAMPLE_DATE = "2024-01-15"
SAMPLE_FROM_DATE = "2024-01-01"
SAMPLE_TO_DATE = "2024-03-31"
SAMPLE_EXCHANGE = "NYSE"
SAMPLE_CIK = "0000320193"  # Apple's CIK
SAMPLE_YEAR = 2024
SAMPLE_QUARTER = 1

ENDPOINT_PARAMS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # FINANCIAL STATEMENTS - Category 1: Symbol-only
    # =========================================================================
    "income_statement": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "balance_sheet_statement": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "cash_flow_statement": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "income_statement_as_reported": {
        "type": "skip",
        "reason": "Variable XBRL fields per company - not standardized",
    },
    "balance_sheet_statement_as_reported": {
        "type": "skip",
        "reason": "Variable XBRL fields per company - not standardized",
    },
    "cash_flow_statement_as_reported": {
        "type": "skip",
        "reason": "Variable XBRL fields per company - not standardized",
    },
    "financial_statement_full_as_reported": {
        "type": "skip",
        "reason": "Variable XBRL fields per company - not standardized",
    },
    "earnings_surprises": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "income_statement_ttm": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "balance_sheet_statement_ttm": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "cash_flow_statement_ttm": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "latest_financial_statements": {"type": "none"},
    # =========================================================================
    # EARNINGS & TRANSCRIPTS
    # =========================================================================
    "earning_call_transcript": {
        "type": "skip",
        "reason": "Returns text content, not structured fields",
    },
    "batch_earning_call_transcript": {
        "type": "skip",
        "reason": "Returns text content, not structured fields",
    },
    "earning_call_transcripts_available_dates": {
        "type": "symbol",
        "sample": SAMPLE_SYMBOL,
    },
    "earning_call_transcript_latest": {
        "type": "skip",
        "reason": "Returns text content, not structured fields",
    },
    # =========================================================================
    # SEC FILINGS
    # =========================================================================
    "sec_filings": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "sec_filings_data": {
        "type": "skip",
        "reason": "Returns Markdown text content, not structured fields",
    },
    # =========================================================================
    # COMPANY PROFILE & INFO
    # =========================================================================
    "company_profile": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "key_executives": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "company_core_information": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "company_outlook": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "enterprise_values": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "stock_peers": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "financial_score": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "owner_earnings": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "employee_count": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_employee_count": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "executive_compensation": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "compensation_benchmark": {"type": "year", "sample": SAMPLE_YEAR},
    "company_notes": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # KEY METRICS & RATIOS
    # =========================================================================
    "key_metrics": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "key_metrics_ttm": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "financial_ratios": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "financial_ratios_ttm": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # GROWTH METRICS
    # =========================================================================
    "financial_growth": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "income_statement_growth": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "balance_sheet_statement_growth": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "cash_flow_statement_growth": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # VALUATION
    # =========================================================================
    "discounted_cash_flow": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "advanced_discounted_cash_flow": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_daily_discounted_cash_flow": {
        "type": "symbol",
        "sample": SAMPLE_SYMBOL,
    },
    "market_capitalization": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_market_capitalization": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # RATINGS & ANALYSTS
    # =========================================================================
    "rating": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_rating": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "analyst_estimates": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "analyst_recommendation": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "stock_grade": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "upgrades_downgrades": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "upgrades_downgrades_consensus": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "upgrades_downgrades_by_company": {"type": "company", "sample": "Barclays"},
    "ratings_snapshot": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "grades_consensus": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # PRICE TARGETS
    # =========================================================================
    "price_targets": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "price_target_summary": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "price_target_consensus": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "price_target_by_analyst_name": {"type": "analyst_name", "sample": "Tim Anderson"},
    "price_target_by_company": {"type": "company", "sample": "Barclays"},
    "price_target_rss_feed": {"type": "none"},
    # =========================================================================
    # ESG
    # =========================================================================
    "esg_score": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # SEGMENTS
    # =========================================================================
    "sales_revenue_by_segments": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "revenue_geographic_segmentation": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # M&A
    # =========================================================================
    "search_mergers_acquisitions": {"type": "search_name", "sample": "Apple"},
    "mergers_acquisitions_rss_feed": {"type": "none"},
    # =========================================================================
    # NEWS
    # =========================================================================
    "stock_news": {"type": "none"},
    "general_news": {"type": "none"},
    "fmp_articles": {"type": "none"},
    "press_releases": {"type": "none"},
    "upgrades_downgrades_rss_feed": {"type": "none"},
    # =========================================================================
    # CALENDAR - Category 3: Date range
    # =========================================================================
    "earning_calendar": {
        "type": "date_range",
        "from": SAMPLE_FROM_DATE,
        "to": SAMPLE_TO_DATE,
    },
    "historical_earning_calendar": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "dividend_calendar": {
        "type": "date_range",
        "from": SAMPLE_FROM_DATE,
        "to": SAMPLE_TO_DATE,
    },
    "ipo_calendar": {
        "type": "date_range",
        "from": SAMPLE_FROM_DATE,
        "to": SAMPLE_TO_DATE,
    },
    "stock_split_calendar": {
        "type": "date_range",
        "from": SAMPLE_FROM_DATE,
        "to": SAMPLE_TO_DATE,
    },
    "economic_calendar": {
        "type": "date_range",
        "from": SAMPLE_FROM_DATE,
        "to": SAMPLE_TO_DATE,
    },
    # =========================================================================
    # QUOTES & MARKET DATA
    # =========================================================================
    "quote": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "quote_short": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_price_full": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_chart": {
        "type": "chart",
        "symbol": SAMPLE_SYMBOL,
        "timeframe": "1day",
        "from_date": SAMPLE_FROM_DATE,
        "to_date": SAMPLE_TO_DATE,
    },
    "multiple_company_prices": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "aftermarket_trade": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "aftermarket_quote": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # MARKET MOVERS - Category 2: No parameters
    # =========================================================================
    "actives": {"type": "none"},
    "gainers": {"type": "none"},
    "losers": {"type": "none"},
    "sectors_performance": {"type": "none"},
    "historical_sectors_performance": {
        "type": "date_range",
        "from": SAMPLE_FROM_DATE,
        "to": SAMPLE_TO_DATE,
    },
    "market_hours": {"type": "none"},
    "is_market_open": {"type": "none"},
    "industry_performance_snapshot": {"type": "none"},
    # =========================================================================
    # INDEXES - Category 2: No parameters
    # =========================================================================
    "indexes": {"type": "none"},
    "sp500_constituent": {"type": "none"},
    "historical_sp500_constituent": {"type": "none"},
    "nasdaq_constituent": {"type": "none"},
    "historical_nasdaq_constituent": {"type": "none"},
    "dowjones_constituent": {"type": "none"},
    "historical_dowjones_constituent": {"type": "none"},
    # =========================================================================
    # INSTITUTIONAL & OWNERSHIP
    # =========================================================================
    "institutional_holders": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "mutual_fund_holders": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "etf_holders": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "form_13f": {"type": "cik", "sample": SAMPLE_CIK},
    # =========================================================================
    # ETF DATA
    # =========================================================================
    "etf_sector_weightings": {"type": "symbol", "sample": "SPY"},
    "etf_country_weightings": {"type": "symbol", "sample": "VEU"},
    # =========================================================================
    # INSIDER TRADING
    # =========================================================================
    "insider_trading": {"type": "symbol_kwarg", "sample": SAMPLE_SYMBOL},
    "insider_trading_rss_feed": {"type": "none"},
    # =========================================================================
    # SENATE TRADING
    # =========================================================================
    "senate_trading_rss": {"type": "none"},
    "senate_trading_symbol": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "senate_disclosure_rss": {"type": "none"},
    "senate_disclosure_symbol": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # DIVIDENDS & SPLITS
    # =========================================================================
    "historical_stock_dividend": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_stock_split": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # SHARES FLOAT
    # =========================================================================
    "shares_float": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "historical_share_float": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # SOCIAL SENTIMENT
    # =========================================================================
    "historical_social_sentiment": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "trending_social_sentiment": {"type": "none"},
    "social_sentiment_changes": {"type": "none"},
    # =========================================================================
    # TECHNICAL INDICATORS - Category 5: Special parameters
    # =========================================================================
    "technical_indicators": {
        "type": "technical",
        "symbol": SAMPLE_SYMBOL,
        "period": 14,
        "statistics_type": "sma",
    },
    # =========================================================================
    # ECONOMICS
    # =========================================================================
    "treasury_rates": {"type": "none"},
    "economic_indicators": {"type": "indicator", "sample": "GDP"},
    "market_risk_premium": {"type": "none"},
    # =========================================================================
    # FOREX
    # =========================================================================
    "forex": {"type": "none"},
    "forex_list": {"type": "none"},
    "forex_quote": {"type": "symbol", "sample": "EURUSD"},
    "forex_historical": {
        "type": "forex_historical",
        "symbol": "EURUSD",
        "from_date": SAMPLE_FROM_DATE,
        "to_date": SAMPLE_TO_DATE,
    },
    # =========================================================================
    # CRYPTO
    # =========================================================================
    "cryptocurrency_quote": {"type": "symbol", "sample": "BTCUSD"},
    "cryptocurrencies_list": {"type": "none"},
    # =========================================================================
    # COMMODITIES
    # =========================================================================
    "commodity_price": {
        "type": "commodity",
        "symbol": "GCUSD",
        "from_date": SAMPLE_FROM_DATE,
        "to_date": SAMPLE_TO_DATE,
    },
    "commodities_list": {"type": "none"},
    # =========================================================================
    # STOCK SCREENER
    # =========================================================================
    "stock_screener": {
        "type": "screener",
        "market_cap_more_than": 1_000_000_000,
        "sector": "Technology",
        "limit": 10,
    },
    # =========================================================================
    # SEARCH
    # =========================================================================
    "search": {
        "type": "skip",
        "reason": "Returns string list, not dict - requires query parameter",
    },
    "search_ticker": {
        "type": "skip",
        "reason": "Returns string list, not dict - requires query parameter",
    },
    # =========================================================================
    # REFERENCE DATA - Category 2: No parameters
    # =========================================================================
    "symbols_list": {"type": "none"},
    "etf_list": {"type": "none"},
    "available_traded_list": {"type": "none"},
    "available_forex": {"type": "none"},
    "available_cryptocurrencies": {"type": "none"},
    "available_commodities": {"type": "none"},
    "available_etfs": {"type": "none"},
    "available_indexes": {"type": "none"},
    "available_sectors": {
        "type": "skip",
        "reason": "Returns simple string list, not structured dict fields",
    },
    "available_industries": {
        "type": "skip",
        "reason": "Returns simple string list, not structured dict fields",
    },
    "available_exchanges": {
        "type": "skip",
        "reason": "Returns simple string list, not structured dict fields",
    },
    "all_countries": {
        "type": "skip",
        "reason": "Returns simple string list, not structured dict fields",
    },
    "delisted_companies": {"type": "none"},
    "financial_statement_symbol_lists": {
        "type": "skip",
        "reason": "Returns simple string list of symbols, not structured dict fields",
    },
    "available_mutual_funds": {"type": "none"},
    "available_tsx": {"type": "none"},
    "available_euronext": {"type": "none"},
    "mutual_fund_list": {"type": "none"},
    "tsx_list": {"type": "none"},
    # =========================================================================
    # CIK MAPPING
    # =========================================================================
    "cik": {"type": "cik", "sample": SAMPLE_CIK},
    "cik_list": {"type": "none"},
    "cik_search": {"type": "search_name", "sample": "Apple"},
    "cusip": {"type": "cik", "sample": SAMPLE_CIK},
    "mapper_cik_name": {"type": "search_name", "sample": "Tim Cook"},
    "mapper_cik_company": {"type": "ticker", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # ALTERNATIVE DATA
    # =========================================================================
    "commitment_of_traders_report_list": {"type": "none"},
    "commitment_of_traders_report": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    "commitment_of_traders_report_analysis": {
        "type": "cot_analysis",
        "symbol": SAMPLE_SYMBOL,
        "from_date": SAMPLE_FROM_DATE,
        "to_date": SAMPLE_TO_DATE,
    },
    "fail_to_deliver": {"type": "symbol", "sample": SAMPLE_SYMBOL},
    # =========================================================================
    # SECTOR/INDUSTRY PE - Category 4: Date required
    # =========================================================================
    "sector_pe_ratio": {
        "type": "skip",
        "reason": "Returns empty for most dates - data availability varies",
    },
    "industry_pe_ratio": {
        "type": "skip",
        "reason": "Returns empty for most dates - data availability varies",
    },
    "batch_eod_prices": {
        "type": "skip",
        "reason": "Batch endpoint - requires specific setup",
    },
    # =========================================================================
    # SEC RSS
    # =========================================================================
    "sec_rss_feeds": {"type": "none"},
    # =========================================================================
    # EXCHANGE - Category 6: Exchange required
    # =========================================================================
    "exchange_realtime": {"type": "exchange", "sample": SAMPLE_EXCHANGE},
    "holidays_by_exchange": {"type": "exchange", "sample": SAMPLE_EXCHANGE},
    # =========================================================================
    # CROWDFUNDING
    # =========================================================================
    "crowdfunding_rss_feed": {"type": "none"},
    "crowdfunding_search": {"type": "search_name", "sample": "Tech"},
    "crowdfunding_by_cik": {"type": "cik", "sample": SAMPLE_CIK},
}


def get_endpoint_param_config(endpoint_name: str) -> Dict[str, Any] | None:
    """
    Get parameter configuration for an endpoint.

    :param endpoint_name: Name of the endpoint from FMP_REGISTRY.
    :return: Parameter config dict or None if not found.
    """
    return ENDPOINT_PARAMS.get(endpoint_name)


def get_introspectable_endpoints() -> list[str]:
    """
    Get list of endpoints that can be introspected (not skipped).

    :return: List of endpoint names that have deterministic field structures.
    """
    return [
        name
        for name, config in ENDPOINT_PARAMS.items()
        if config.get("type") != "skip"
    ]


def get_skipped_endpoints() -> Dict[str, str]:
    """
    Get endpoints that are skipped with their reasons.

    :return: Dict mapping endpoint name to skip reason.
    """
    return {
        name: config.get("reason", "No reason provided")
        for name, config in ENDPOINT_PARAMS.items()
        if config.get("type") == "skip"
    }
