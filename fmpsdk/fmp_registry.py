"""
FMP Endpoint Registry for LLM-powered data source selection.

This module provides a comprehensive registry of all FMP (Financial Modeling Prep)
endpoints available in the fmpsdk package. Each endpoint is documented with
LLM-friendly descriptions, parameters, use cases, and return types.

Usage:
    from fmpsdk.fmp_registry import FMP_REGISTRY, get_registry_for_llm, get_endpoints_by_category

    # Get all endpoints in a category
    financials = get_endpoints_by_category('financials')

    # Get LLM-friendly formatted context
    context = get_registry_for_llm()
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class FMPEndpoint:
    """Registry entry for an FMP endpoint."""

    name: str  # Canonical name (e.g., "income_statement")
    function: str  # fmpsdk function name
    description: str  # LLM-friendly description
    category: str  # Category for grouping
    parameters: Dict[str, Any]  # Available params with types and defaults
    example_use_cases: List[str]  # When to use this endpoint
    returns: str  # Description of return data structure
    notes: Optional[str] = None  # Any caveats or special handling


# =============================================================================
# FMP ENDPOINT REGISTRY
# =============================================================================

FMP_REGISTRY: Dict[str, FMPEndpoint] = {
    # =========================================================================
    # FINANCIAL STATEMENTS
    # =========================================================================
    "income_statement": FMPEndpoint(
        name="income_statement",
        function="income_statement",
        description="Annual or quarterly income statement data including revenue, expenses, and net income. Shows profitability trends over time.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True, "description": "Stock ticker (e.g., 'AAPL')"},
            "period": {"type": "str", "required": False, "default": "annual", "options": ["annual", "quarter"]},
            "limit": {"type": "int", "required": False, "default": 10, "description": "Number of periods to retrieve"},
            "output": {"type": "str", "required": False, "default": "markdown", "options": ["markdown", "json", "tsv"]},
        },
        example_use_cases=[
            "Revenue trend analysis over multiple years",
            "Profitability assessment and margin analysis",
            "Year-over-year growth comparison",
            "Cost structure analysis",
        ],
        returns="List of income statements with date, revenue, grossProfit, operatingIncome, netIncome, eps, etc.",
    ),
    "balance_sheet_statement": FMPEndpoint(
        name="balance_sheet_statement",
        function="balance_sheet_statement",
        description="Annual or quarterly balance sheet data including assets, liabilities, and equity. Shows financial position at specific points in time.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True, "description": "Stock ticker or CIK"},
            "period": {"type": "str", "required": False, "default": "annual", "options": ["annual", "quarter"]},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Asset composition analysis",
            "Debt level assessment",
            "Working capital analysis",
            "Shareholder equity trends",
        ],
        returns="List of balance sheets with totalAssets, totalLiabilities, totalEquity, cash, inventory, etc.",
    ),
    "cash_flow_statement": FMPEndpoint(
        name="cash_flow_statement",
        function="cash_flow_statement",
        description="Annual or quarterly cash flow statement showing operating, investing, and financing activities. Reveals actual cash generation and usage.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True, "description": "Stock ticker or CIK"},
            "period": {"type": "str", "required": False, "default": "annual", "options": ["annual", "quarter"]},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Free cash flow analysis",
            "Capital expenditure trends",
            "Dividend sustainability assessment",
            "Cash conversion analysis",
        ],
        returns="List of cash flow statements with operatingCashFlow, investingCashFlow, financingCashFlow, freeCashFlow, etc.",
    ),
    "income_statement_as_reported": FMPEndpoint(
        name="income_statement_as_reported",
        function="income_statement_as_reported",
        description="Income statement exactly as reported in SEC filings, without standardization. Useful for detailed analysis matching company-specific terminology.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Detailed SEC filing analysis",
            "Company-specific line item research",
            "Audit and compliance checks",
        ],
        returns="As-reported income statement data with original SEC filing field names.",
    ),
    "balance_sheet_statement_as_reported": FMPEndpoint(
        name="balance_sheet_statement_as_reported",
        function="balance_sheet_statement_as_reported",
        description="Balance sheet exactly as reported in SEC filings, without standardization.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Detailed SEC filing analysis",
            "Company-specific asset/liability categorization",
        ],
        returns="As-reported balance sheet data with original SEC filing field names.",
    ),
    "cash_flow_statement_as_reported": FMPEndpoint(
        name="cash_flow_statement_as_reported",
        function="cash_flow_statement_as_reported",
        description="Cash flow statement exactly as reported in SEC filings, without standardization.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Detailed SEC filing analysis",
            "Company-specific cash flow categorization",
        ],
        returns="As-reported cash flow statement data with original SEC filing field names.",
    ),
    "financial_statement_full_as_reported": FMPEndpoint(
        name="financial_statement_full_as_reported",
        function="financial_statement_full_as_reported",
        description="Complete financial statements as reported in SEC filings, combining income, balance sheet, and cash flow.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Comprehensive SEC filing analysis",
            "Full financial picture from original filings",
        ],
        returns="Complete as-reported financial statement data.",
    ),
    "earnings_surprises": FMPEndpoint(
        name="earnings_surprises",
        function="earnings_surprises",
        description="Historical earnings surprises showing actual vs estimated EPS. Reveals how often a company beats or misses expectations.",
        category="financials",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Earnings beat/miss pattern analysis",
            "Management guidance accuracy assessment",
            "Earnings quality evaluation",
        ],
        returns="List of earnings surprises with date, actualEarningResult, estimatedEarning, surprise percentage.",
    ),
    # =========================================================================
    # EARNINGS & TRANSCRIPTS
    # =========================================================================
    "earning_call_transcript": FMPEndpoint(
        name="earning_call_transcript",
        function="earning_call_transcript",
        description="Full text transcript of earnings call for a specific quarter. Contains management commentary, guidance, and Q&A with analysts.",
        category="earnings",
        parameters={
            "symbol": {"type": "str", "required": True},
            "year": {"type": "int", "required": True, "description": "Year (e.g., 2024)"},
            "quarter": {"type": "int", "required": True, "description": "Quarter (1-4)"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Management sentiment analysis",
            "Strategic initiative tracking",
            "Guidance and outlook extraction",
            "Competitive intelligence from Q&A",
        ],
        returns="Earnings call transcript text with date, symbol, quarter, year, and content.",
        notes="Transcripts can be very long (10k+ words). Consider token limits.",
    ),
    "batch_earning_call_transcript": FMPEndpoint(
        name="batch_earning_call_transcript",
        function="batch_earning_call_transcript",
        description="All earnings call transcripts for a company in a given year. Efficient for annual analysis.",
        category="earnings",
        parameters={
            "symbol": {"type": "str", "required": True},
            "year": {"type": "int", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Full year management commentary analysis",
            "Quarterly guidance evolution tracking",
            "Annual narrative analysis",
        ],
        returns="Multiple earnings call transcripts for all quarters in the year.",
        notes="Very large data return - may hit token limits.",
    ),
    "earning_call_transcripts_available_dates": FMPEndpoint(
        name="earning_call_transcripts_available_dates",
        function="earning_call_transcripts_available_dates",
        description="List of available earnings call transcript dates for a company. Use to discover which transcripts are available.",
        category="earnings",
        parameters={
            "symbol": {"type": "str", "required": True},
        },
        example_use_cases=[
            "Discover available transcript dates before fetching",
            "Plan transcript analysis scope",
        ],
        returns="List of [quarter, year] pairs with available transcripts.",
    ),
    # =========================================================================
    # SEC FILINGS
    # =========================================================================
    "sec_filings": FMPEndpoint(
        name="sec_filings",
        function="sec_filings",
        description="SEC filing metadata and links (10-K, 10-Q, 8-K, etc.). Returns filing dates, types, and URLs but NOT the actual content.",
        category="sec",
        parameters={
            "symbol": {"type": "str", "required": True},
            "filing_type": {"type": "str", "required": False, "default": "", "options": ["10-K", "10-Q", "8-K", "DEF 14A", "S-1", "etc"]},
            "limit": {"type": "int", "required": False, "default": 10},
        },
        example_use_cases=[
            "Find SEC filing links for further analysis",
            "Track filing history and timing",
            "Identify recent 8-K events",
        ],
        returns="List of filings with type, fillingDate, acceptedDate, cik, link, finalLink.",
    ),
    "sec_filings_data": FMPEndpoint(
        name="sec_filings_data",
        function="sec_filings_data",
        description="Full text content of SEC filings rendered as Markdown. Fetches and parses actual filing content from SEC EDGAR.",
        category="sec",
        parameters={
            "symbol": {"type": "str", "required": True},
            "filing_type": {"type": "str", "required": False, "default": "10-K", "options": ["10-K", "10-Q", "8-K"]},
            "limit": {"type": "int", "required": False, "default": 1},
        },
        example_use_cases=[
            "Deep 10-K analysis for risk factors, business description",
            "8-K event analysis for material events",
            "Historical 10-K trend analysis",
        ],
        returns="Full Markdown-formatted SEC filing content.",
        notes="WARNING: Full 10-K content is VERY long (100k+ tokens). Limit to 1-2 filings max.",
    ),
    # =========================================================================
    # COMPANY PROFILE & INFO
    # =========================================================================
    "company_profile": FMPEndpoint(
        name="company_profile",
        function="company_profile",
        description="Comprehensive company overview including price, market cap, sector, industry, CEO, description, headquarters, website, and key statistics.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Company overview and background research",
            "Sector and industry classification",
            "Market cap and basic statistics",
            "Company description for reports",
        ],
        returns="Company profile with symbol, price, beta, mktCap, description, sector, industry, ceo, website, etc.",
    ),
    "key_executives": FMPEndpoint(
        name="key_executives",
        function="key_executives",
        description="Key executives data from SEC filings including names, titles, and compensation.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Management team analysis",
            "Executive compensation research",
            "Corporate governance assessment",
        ],
        returns="List of executives with name, title, pay, currencyPay, etc.",
    ),
    "company_core_information": FMPEndpoint(
        name="company_core_information",
        function="company_core_information",
        description="Core company information including CIK, exchange, SIC code, and state of incorporation.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Regulatory and compliance research",
            "Company registration details",
        ],
        returns="Core info with cik, exchange, sicCode, sicDescription, stateOfIncorporation, etc.",
    ),
    "company_outlook": FMPEndpoint(
        name="company_outlook",
        function="company_outlook",
        description="Comprehensive company outlook combining profile, metrics, ratios, and stock data in one call.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Quick comprehensive company snapshot",
            "All-in-one company analysis",
        ],
        returns="Combined data including profile, metrics, ratios, stock data, insider transactions, and more.",
    ),
    "enterprise_values": FMPEndpoint(
        name="enterprise_values",
        function="enterprise_values",
        description="Enterprise value data including market cap, debt, and cash. Shows total company value for M&A analysis.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "M&A valuation analysis",
            "EV/EBITDA calculations",
            "Capital structure analysis",
        ],
        returns="Enterprise value data with date, symbol, enterpriseValue, numberOfShares, addTotalDebt, minusCashAndEquivalents.",
    ),
    # =========================================================================
    # KEY METRICS & RATIOS
    # =========================================================================
    "key_metrics": FMPEndpoint(
        name="key_metrics",
        function="key_metrics",
        description="Key financial metrics including revenue per share, PE ratio, debt to equity, ROE, and more.",
        category="metrics",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Valuation metrics analysis",
            "Profitability metrics tracking",
            "Leverage and efficiency ratios",
        ],
        returns="Key metrics with revenuePerShare, netIncomePerShare, peRatio, debtToEquity, returnOnEquity, etc.",
    ),
    "key_metrics_ttm": FMPEndpoint(
        name="key_metrics_ttm",
        function="key_metrics_ttm",
        description="Trailing twelve months (TTM) key metrics for most recent performance snapshot.",
        category="metrics",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Current valuation metrics",
            "Real-time performance snapshot",
        ],
        returns="TTM key metrics data.",
    ),
    "financial_ratios": FMPEndpoint(
        name="financial_ratios",
        function="financial_ratios",
        description="Comprehensive financial ratios including liquidity, profitability, debt, and efficiency ratios.",
        category="metrics",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Comprehensive ratio analysis",
            "Peer comparison",
            "Credit analysis",
            "Investment screening",
        ],
        returns="Financial ratios including currentRatio, quickRatio, grossProfitMargin, returnOnAssets, debtRatio, etc.",
    ),
    "financial_ratios_ttm": FMPEndpoint(
        name="financial_ratios_ttm",
        function="financial_ratios_ttm",
        description="Trailing twelve months financial ratios for current performance.",
        category="metrics",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Current ratio analysis",
            "Real-time performance assessment",
        ],
        returns="TTM financial ratios data.",
    ),
    # =========================================================================
    # GROWTH METRICS
    # =========================================================================
    "financial_growth": FMPEndpoint(
        name="financial_growth",
        function="financial_growth",
        description="Financial growth metrics showing year-over-year or quarter-over-quarter growth rates.",
        category="growth",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Growth trend analysis",
            "Historical growth rate tracking",
            "Growth consistency assessment",
        ],
        returns="Growth metrics with revenueGrowth, netIncomeGrowth, epsgrowth, etc.",
    ),
    "income_statement_growth": FMPEndpoint(
        name="income_statement_growth",
        function="income_statement_growth",
        description="Income statement growth metrics showing revenue and profit growth trends.",
        category="growth",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Revenue growth analysis",
            "Profit margin trend analysis",
        ],
        returns="Income statement growth data.",
    ),
    "balance_sheet_statement_growth": FMPEndpoint(
        name="balance_sheet_statement_growth",
        function="balance_sheet_statement_growth",
        description="Balance sheet growth metrics showing asset and liability growth trends.",
        category="growth",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Asset growth analysis",
            "Debt growth tracking",
        ],
        returns="Balance sheet growth data.",
    ),
    "cash_flow_statement_growth": FMPEndpoint(
        name="cash_flow_statement_growth",
        function="cash_flow_statement_growth",
        description="Cash flow growth metrics showing operating, investing, and financing cash flow trends.",
        category="growth",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "precision": {"type": "int", "required": False, "default": 5},
        },
        example_use_cases=[
            "Cash flow growth analysis",
            "Free cash flow trend tracking",
        ],
        returns="Cash flow growth data.",
    ),
    # =========================================================================
    # VALUATION
    # =========================================================================
    "discounted_cash_flow": FMPEndpoint(
        name="discounted_cash_flow",
        function="discounted_cash_flow",
        description="DCF valuation estimating intrinsic value based on projected future cash flows.",
        category="valuation",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Intrinsic value estimation",
            "Under/overvaluation assessment",
            "Value investing screening",
        ],
        returns="DCF data with date, symbol, dcf (intrinsic value), stockPrice.",
    ),
    "advanced_discounted_cash_flow": FMPEndpoint(
        name="advanced_discounted_cash_flow",
        function="advanced_discounted_cash_flow",
        description="Advanced DCF model with detailed assumptions and projections.",
        category="valuation",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Detailed intrinsic value analysis",
            "DCF sensitivity analysis",
        ],
        returns="Advanced DCF data with detailed projections and assumptions.",
    ),
    "historical_daily_discounted_cash_flow": FMPEndpoint(
        name="historical_daily_discounted_cash_flow",
        function="historical_daily_discounted_cash_flow",
        description="Daily historical DCF values showing intrinsic value evolution over time.",
        category="valuation",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Historical valuation trends",
            "Valuation gap analysis over time",
        ],
        returns="Historical DCF values with date, symbol, dcf, stockPrice.",
    ),
    "market_capitalization": FMPEndpoint(
        name="market_capitalization",
        function="market_capitalization",
        description="Current market capitalization of a company.",
        category="valuation",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Company size classification",
            "Market value assessment",
        ],
        returns="Market cap data with date, symbol, marketCap.",
    ),
    "historical_market_capitalization": FMPEndpoint(
        name="historical_market_capitalization",
        function="historical_market_capitalization",
        description="Historical market capitalization showing company value over time.",
        category="valuation",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Market cap growth analysis",
            "Historical size tracking",
        ],
        returns="Historical market cap data.",
    ),
    # =========================================================================
    # RATINGS & ANALYSTS
    # =========================================================================
    "rating": FMPEndpoint(
        name="rating",
        function="rating",
        description="FMP's proprietary rating based on financial analysis including DCF, ratios, and intrinsic value.",
        category="analysts",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Quick investment rating lookup",
            "Automated screening based on ratings",
        ],
        returns="Rating data with symbol, date, rating, ratingScore, ratingRecommendation, etc.",
    ),
    "historical_rating": FMPEndpoint(
        name="historical_rating",
        function="historical_rating",
        description="Historical ratings showing how FMP's assessment has changed over time.",
        category="analysts",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 100},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Rating trend analysis",
            "Historical sentiment tracking",
        ],
        returns="Historical rating data.",
    ),
    "analyst_estimates": FMPEndpoint(
        name="analyst_estimates",
        function="analyst_estimates",
        description="Wall Street analyst estimates for future earnings, revenue, and EPS.",
        category="analysts",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "annual"},
            "limit": {"type": "int", "required": False, "default": 100},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Forward earnings expectations",
            "Revenue forecast analysis",
            "Consensus estimate tracking",
        ],
        returns="Analyst estimates with estimatedRevenueAvg, estimatedEpsAvg, numberOfAnalysts, etc.",
        notes="Estimates are not always accurate - use for guidance only.",
    ),
    "analyst_recommendation": FMPEndpoint(
        name="analyst_recommendation",
        function="analyst_recommendation",
        description="Analyst buy/sell/hold recommendations with analyst firm details.",
        category="analysts",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Analyst sentiment analysis",
            "Recommendation consensus tracking",
            "Analyst coverage assessment",
        ],
        returns="Analyst recommendations with analystName, analystCompany, recommendationKey, etc.",
    ),
    "stock_grade": FMPEndpoint(
        name="stock_grade",
        function="stock_grade",
        description="Stock grades from hedge funds, investment firms, and analysts.",
        category="analysts",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 50},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Professional investor assessment",
            "Grade change tracking",
        ],
        returns="Stock grades with gradingCompany, newGrade, previousGrade, action, etc.",
    ),
    "upgrades_downgrades": FMPEndpoint(
        name="upgrades_downgrades",
        function="upgrades_downgrades",
        description="Stock upgrades and downgrades from analysts.",
        category="analysts",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Rating change tracking",
            "Analyst sentiment shifts",
        ],
        returns="Upgrade/downgrade data with publishedDate, newGrade, previousGrade, gradingCompany.",
    ),
    "upgrades_downgrades_consensus": FMPEndpoint(
        name="upgrades_downgrades_consensus",
        function="upgrades_downgrades_consensus",
        description="Consensus rating across all analysts for a stock.",
        category="analysts",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Overall analyst sentiment",
            "Consensus view assessment",
        ],
        returns="Consensus data with symbol, strongBuy, buy, hold, sell, strongSell, consensus.",
    ),
    "upgrades_downgrades_by_company": FMPEndpoint(
        name="upgrades_downgrades_by_company",
        function="upgrades_downgrades_by_company",
        description="All upgrades and downgrades issued by a specific analyst firm.",
        category="analysts",
        parameters={
            "company": {"type": "str", "required": True, "description": "Analyst firm name (e.g., 'Morgan Stanley')"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Track specific analyst firm recommendations",
            "Firm-level research aggregation",
        ],
        returns="All ratings from the specified analyst firm.",
    ),
    # =========================================================================
    # PRICE TARGETS
    # =========================================================================
    "price_targets": FMPEndpoint(
        name="price_targets",
        function="price_targets",
        description="Analyst price targets for a company's stock.",
        category="price_targets",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Price target analysis",
            "Upside/downside potential assessment",
        ],
        returns="Price targets with analystName, analystCompany, priceTarget, publishedDate.",
    ),
    "price_target_summary": FMPEndpoint(
        name="price_target_summary",
        function="price_target_summary",
        description="Summary of price targets including average, high, low, and number of analysts.",
        category="price_targets",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Quick price target overview",
            "Analyst consensus target",
        ],
        returns="Summary with lastMonth, lastQuarter, high, low, average, median, numberOfAnalysts.",
    ),
    "price_target_consensus": FMPEndpoint(
        name="price_target_consensus",
        function="price_target_consensus",
        description="Consensus price target averaging all analyst targets.",
        category="price_targets",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Consensus price expectation",
            "Overall market target",
        ],
        returns="Consensus price target data.",
    ),
    "price_target_by_analyst_name": FMPEndpoint(
        name="price_target_by_analyst_name",
        function="price_target_by_analyst_name",
        description="Price targets from a specific analyst across different stocks.",
        category="price_targets",
        parameters={
            "name": {"type": "str", "required": True, "description": "Analyst name"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Track specific analyst coverage",
            "Analyst performance tracking",
        ],
        returns="Price targets from the specified analyst.",
    ),
    "price_target_by_company": FMPEndpoint(
        name="price_target_by_company",
        function="price_target_by_company",
        description="Price targets from a specific analyst firm.",
        category="price_targets",
        parameters={
            "company": {"type": "str", "required": True, "description": "Analyst firm (e.g., 'Barclays')"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Firm-level price targets",
            "Institutional research tracking",
        ],
        returns="Price targets from the specified firm.",
    ),
    "price_target_rss_feed": FMPEndpoint(
        name="price_target_rss_feed",
        function="price_target_rss_feed",
        description="RSS feed of latest price target updates across all stocks.",
        category="price_targets",
        parameters={
            "page": {"type": "int", "required": False, "default": 0},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Real-time price target monitoring",
            "Latest analyst actions",
        ],
        returns="Recent price target updates.",
    ),
    # =========================================================================
    # ESG
    # =========================================================================
    "esg_score": FMPEndpoint(
        name="esg_score",
        function="esg_score",
        description="Environmental, Social, and Governance (ESG) scores with breakdown by E, S, and G components.",
        category="esg",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Sustainability analysis",
            "ESG screening",
            "Socially responsible investing research",
            "Renewable energy company assessment",
        ],
        returns="ESG data with environmentalScore, socialScore, governanceScore, ESGScore, etc.",
    ),
    # =========================================================================
    # COMPANY VALUATION EXTRAS
    # =========================================================================
    "stock_peers": FMPEndpoint(
        name="stock_peers",
        function="stock_peers",
        description="Similar companies trading on the same exchange, in the same sector, with similar market cap.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Competitor identification",
            "Peer comparison analysis",
            "Industry benchmarking",
        ],
        returns="List of peer symbols.",
    ),
    "financial_score": FMPEndpoint(
        name="financial_score",
        function="financial_score",
        description="Financial health score assessing company performance.",
        category="metrics",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Financial health assessment",
            "Quick screening metric",
        ],
        returns="Financial score data.",
    ),
    "owner_earnings": FMPEndpoint(
        name="owner_earnings",
        function="owner_earnings",
        description="Owner earnings calculation (Buffett's preferred metric) showing true cash available to shareholders.",
        category="metrics",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Value investing analysis",
            "True earnings power assessment",
        ],
        returns="Owner earnings data.",
    ),
    # =========================================================================
    # SEGMENTS
    # =========================================================================
    "sales_revenue_by_segments": FMPEndpoint(
        name="sales_revenue_by_segments",
        function="sales_revenue_by_segments",
        description="Revenue breakdown by business segments (product lines, services, etc.).",
        category="segments",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "quarter"},
            "limit": {"type": "int", "required": False, "default": None},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Business segment analysis",
            "Product line performance tracking",
            "Diversification assessment",
        ],
        returns="Revenue by segment with date and segment-specific revenue values.",
    ),
    "revenue_geographic_segmentation": FMPEndpoint(
        name="revenue_geographic_segmentation",
        function="revenue_geographic_segmentation",
        description="Revenue breakdown by geographic region showing global market presence.",
        category="segments",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "str", "required": False, "default": "quarter"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Geographic exposure analysis",
            "International expansion tracking",
            "Regional performance comparison",
        ],
        returns="Revenue by geography with date and region-specific revenue values.",
    ),
    # =========================================================================
    # EMPLOYEE & COMPENSATION
    # =========================================================================
    "employee_count": FMPEndpoint(
        name="employee_count",
        function="employee_count",
        description="Current number of employees at a company.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Company size assessment",
            "Workforce analysis",
        ],
        returns="Employee count data.",
    ),
    "historical_employee_count": FMPEndpoint(
        name="historical_employee_count",
        function="historical_employee_count",
        description="Historical employee count showing workforce growth or decline over time.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Workforce growth analysis",
            "Operational scaling assessment",
        ],
        returns="Historical employee count data.",
    ),
    "executive_compensation": FMPEndpoint(
        name="executive_compensation",
        function="executive_compensation",
        description="Executive compensation data from proxy filings.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Executive pay analysis",
            "Compensation benchmarking",
            "Corporate governance assessment",
        ],
        returns="Executive compensation with name, title, salary, bonus, stockAwards, etc.",
    ),
    "compensation_benchmark": FMPEndpoint(
        name="compensation_benchmark",
        function="compensation_benchmark",
        description="Executive compensation benchmarks for a specific year.",
        category="company",
        parameters={
            "year": {"type": "int", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Industry compensation comparison",
            "Pay benchmarking",
        ],
        returns="Compensation benchmark data.",
    ),
    "company_notes": FMPEndpoint(
        name="company_notes",
        function="company_notes",
        description="Company notes and additional information.",
        category="company",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Additional company context",
            "Notes and observations",
        ],
        returns="Company notes data.",
    ),
    # =========================================================================
    # M&A
    # =========================================================================
    "search_mergers_acquisitions": FMPEndpoint(
        name="search_mergers_acquisitions",
        function="search_mergers_acquisitions",
        description="Search for M&A deals by company name.",
        category="corporate_actions",
        parameters={
            "name": {"type": "str", "required": True, "description": "Company name to search"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "M&A activity research",
            "Deal history lookup",
            "Strategic transaction analysis",
        ],
        returns="M&A deal data.",
    ),
    "mergers_acquisitions_rss_feed": FMPEndpoint(
        name="mergers_acquisitions_rss_feed",
        function="mergers_acquisitions_rss_feed",
        description="RSS feed of latest M&A news and announcements.",
        category="news",
        parameters={
            "page": {"type": "int", "required": False, "default": 0},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Real-time M&A monitoring",
            "Deal flow tracking",
        ],
        returns="Latest M&A news.",
    ),
    # =========================================================================
    # NEWS
    # =========================================================================
    "stock_news": FMPEndpoint(
        name="stock_news",
        function="stock_news",
        description="Stock-specific news articles from various sources.",
        category="news",
        parameters={
            "tickers": {"type": "str or list", "required": False, "description": "Stock symbol(s)"},
            "limit": {"type": "int", "required": False, "default": 25},
            "page": {"type": "int", "required": False, "default": 0},
            "from_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Company-specific news tracking",
            "Event-driven analysis",
            "Sentiment research",
        ],
        returns="News articles with title, publishedDate, site, url, text snippet.",
    ),
    "general_news": FMPEndpoint(
        name="general_news",
        function="general_news",
        description="General financial and market news from various sources.",
        category="news",
        parameters={
            "pages": {"type": "int", "required": False, "default": 20},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Market news overview",
            "General financial coverage",
        ],
        returns="General news articles.",
    ),
    "fmp_articles": FMPEndpoint(
        name="fmp_articles",
        function="fmp_articles",
        description="Articles published by Financial Modeling Prep.",
        category="news",
        parameters={
            "page": {"type": "int", "required": False, "default": 0},
            "size": {"type": "int", "required": False, "default": 25},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "FMP analysis and research",
            "Educational content",
        ],
        returns="FMP articles with title, date, content.",
    ),
    "press_releases": FMPEndpoint(
        name="press_releases",
        function="press_releases",
        description="Company press releases with official announcements.",
        category="news",
        parameters={
            "symbol": {"type": "str", "required": False, "description": "Stock symbol (optional)"},
            "limit": {"type": "int", "required": False, "default": 10},
            "page": {"type": "int", "required": False, "default": 0},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Official company announcements",
            "Corporate communications tracking",
            "Event detection",
        ],
        returns="Press releases with title, date, text.",
    ),
    "upgrades_downgrades_rss_feed": FMPEndpoint(
        name="upgrades_downgrades_rss_feed",
        function="upgrades_downgrades_rss_feed",
        description="RSS feed of latest analyst upgrades and downgrades.",
        category="news",
        parameters={
            "page": {"type": "int", "required": False, "default": 0},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Real-time rating changes",
            "Analyst action monitoring",
        ],
        returns="Latest upgrades/downgrades.",
    ),
    # =========================================================================
    # CALENDAR
    # =========================================================================
    "earning_calendar": FMPEndpoint(
        name="earning_calendar",
        function="earning_calendar",
        description="Earnings announcement calendar showing upcoming and past earnings dates.",
        category="calendar",
        parameters={
            "from_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "estimate_required": {"type": "bool", "required": False, "default": True},
            "revenue_minimum": {"type": "float", "required": False, "default": 1000000000},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Earnings season tracking",
            "Upcoming earnings dates",
            "Event planning",
        ],
        returns="Earnings calendar with date, symbol, eps, epsEstimated, revenue, revenueEstimated.",
    ),
    "historical_earning_calendar": FMPEndpoint(
        name="historical_earning_calendar",
        function="historical_earning_calendar",
        description="Historical and upcoming earnings dates for a specific company.",
        category="calendar",
        parameters={
            "symbol": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Company-specific earnings history",
            "Earnings pattern analysis",
        ],
        returns="Historical earnings calendar data.",
    ),
    "dividend_calendar": FMPEndpoint(
        name="dividend_calendar",
        function="dividend_calendar",
        description="Dividend payment calendar showing upcoming dividend dates.",
        category="calendar",
        parameters={
            "from_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": False, "description": "YYYY-MM-DD (max 3 months)"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Dividend income planning",
            "Ex-dividend date tracking",
        ],
        returns="Dividend calendar with date, symbol, dividend, recordDate, paymentDate.",
        notes="Maximum 3-month date range.",
    ),
    "ipo_calendar": FMPEndpoint(
        name="ipo_calendar",
        function="ipo_calendar",
        description="IPO calendar showing upcoming and recent initial public offerings.",
        category="calendar",
        parameters={
            "from_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "IPO tracking",
            "New listing research",
        ],
        returns="IPO calendar with date, symbol, exchange, name, ipoPrice, priceRange.",
    ),
    "stock_split_calendar": FMPEndpoint(
        name="stock_split_calendar",
        function="stock_split_calendar",
        description="Stock split calendar showing upcoming splits.",
        category="calendar",
        parameters={
            "from_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Split event tracking",
            "Corporate action monitoring",
        ],
        returns="Stock split calendar with date, symbol, numerator, denominator.",
    ),
    "economic_calendar": FMPEndpoint(
        name="economic_calendar",
        function="economic_calendar",
        description="Economic events calendar with GDP, CPI, employment data releases.",
        category="calendar",
        parameters={
            "from_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
            "impact_filter": {"type": "str or list", "required": False, "default": ["High"], "options": ["Low", "Medium", "High"]},
            "country_filter": {"type": "str or list", "required": False},
            "currency_filter": {"type": "str or list", "required": False},
        },
        example_use_cases=[
            "Macro event tracking",
            "Economic data releases",
            "Market-moving event planning",
        ],
        returns="Economic calendar with date, event, country, actual, previous, estimate, impact.",
    ),
    # =========================================================================
    # QUOTES & MARKET DATA
    # =========================================================================
    "quote": FMPEndpoint(
        name="quote",
        function="quote",
        description="Real-time full quote with bid/ask, volume, price, and daily statistics.",
        category="market",
        parameters={
            "symbol": {"type": "str or list", "required": True, "description": "Stock symbol(s)"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Real-time price lookup",
            "Current market data",
            "Trading decisions",
        ],
        returns="Full quote with price, change, changesPercentage, dayLow, dayHigh, volume, avgVolume, etc.",
    ),
    "quote_short": FMPEndpoint(
        name="quote_short",
        function="quote_short",
        description="Simplified real-time quote with just price, change, and volume.",
        category="market",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Quick price check",
            "Simple market snapshot",
        ],
        returns="Short quote with symbol, price, volume.",
    ),
    "historical_price_full": FMPEndpoint(
        name="historical_price_full",
        function="historical_price_full",
        description="Daily historical OHLCV price data for up to 5 years.",
        category="market",
        parameters={
            "symbol": {"type": "str or list", "required": True},
            "from_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Historical price analysis",
            "Trend analysis",
            "Backtesting",
            "Chart data",
        ],
        returns="Historical prices with date, open, high, low, close, volume, change, changePercent.",
    ),
    "historical_chart": FMPEndpoint(
        name="historical_chart",
        function="historical_chart",
        description="Intraday and daily historical price data with various timeframes.",
        category="market",
        parameters={
            "symbol": {"type": "str", "required": True},
            "timeframe": {"type": "str", "required": True, "options": ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]},
            "from_date": {"type": "str", "required": True, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": True, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Intraday analysis",
            "Short-term trading",
            "Technical analysis",
        ],
        returns="Historical chart data with date, open, high, low, close, volume.",
    ),
    "multiple_company_prices": FMPEndpoint(
        name="multiple_company_prices",
        function="multiple_company_prices",
        description="Real-time prices for multiple companies in a single request.",
        category="market",
        parameters={
            "symbols": {"type": "str or list", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Portfolio monitoring",
            "Batch price lookup",
            "Watchlist updates",
        ],
        returns="Prices for multiple symbols.",
    ),
    # =========================================================================
    # MARKET MOVERS
    # =========================================================================
    "actives": FMPEndpoint(
        name="actives",
        function="actives",
        description="Most actively traded stocks by volume.",
        category="market",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Market activity monitoring",
            "High volume stock discovery",
            "Liquidity analysis",
        ],
        returns="Active stocks with symbol, name, change, price, changesPercentage, volume.",
    ),
    "gainers": FMPEndpoint(
        name="gainers",
        function="gainers",
        description="Stocks with the biggest gains today.",
        category="market",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Daily winners tracking",
            "Momentum stock discovery",
        ],
        returns="Top gaining stocks with symbol, name, change, price, changesPercentage.",
    ),
    "losers": FMPEndpoint(
        name="losers",
        function="losers",
        description="Stocks with the biggest losses today.",
        category="market",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Daily losers tracking",
            "Sell-off monitoring",
            "Potential recovery plays",
        ],
        returns="Top losing stocks with symbol, name, change, price, changesPercentage.",
    ),
    "sectors_performance": FMPEndpoint(
        name="sectors_performance",
        function="sectors_performance",
        description="Current performance by sector.",
        category="market",
        parameters={
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Sector rotation analysis",
            "Market breadth assessment",
        ],
        returns="Sector performance with sector name and changesPercentage.",
    ),
    "historical_sectors_performance": FMPEndpoint(
        name="historical_sectors_performance",
        function="historical_sectors_performance",
        description="Historical sector performance over time.",
        category="market",
        parameters={
            "from_date": {"type": "str", "required": True, "description": "YYYY-MM-DD"},
            "to_date": {"type": "str", "required": True, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Sector trend analysis",
            "Historical rotation patterns",
        ],
        returns="Historical sector performance data.",
    ),
    "market_hours": FMPEndpoint(
        name="market_hours",
        function="market_hours",
        description="Market hours information for exchanges.",
        category="market",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Trading schedule lookup",
            "Market timing",
        ],
        returns="Market hours data.",
    ),
    "is_market_open": FMPEndpoint(
        name="is_market_open",
        function="is_market_open",
        description="Check if a market/exchange is currently open.",
        category="market",
        parameters={
            "exchange": {"type": "str", "required": False, "default": "NASDAQ"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Market status check",
            "Trading availability",
        ],
        returns="Market open/closed status.",
    ),
    # =========================================================================
    # INDEXES
    # =========================================================================
    "indexes": FMPEndpoint(
        name="indexes",
        function="indexes",
        description="Major market indexes (S&P 500, Dow Jones, NASDAQ, etc.).",
        category="indexes",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Market benchmark tracking",
            "Index performance comparison",
        ],
        returns="Index data with symbol, name, price, change, changesPercentage.",
    ),
    "sp500_constituent": FMPEndpoint(
        name="sp500_constituent",
        function="sp500_constituent",
        description="Current S&P 500 constituents list.",
        category="indexes",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "S&P 500 stock list",
            "Index composition analysis",
        ],
        returns="S&P 500 constituents with symbol, name, sector, subSector.",
    ),
    "historical_sp500_constituent": FMPEndpoint(
        name="historical_sp500_constituent",
        function="historical_sp500_constituent",
        description="Historical S&P 500 additions and removals.",
        category="indexes",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Index changes tracking",
            "Historical composition",
        ],
        returns="Historical S&P 500 changes.",
    ),
    "nasdaq_constituent": FMPEndpoint(
        name="nasdaq_constituent",
        function="nasdaq_constituent",
        description="Current NASDAQ 100 constituents list.",
        category="indexes",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "NASDAQ 100 stock list",
            "Tech index composition",
        ],
        returns="NASDAQ constituents with symbol, name, sector.",
    ),
    "historical_nasdaq_constituent": FMPEndpoint(
        name="historical_nasdaq_constituent",
        function="historical_nasdaq_constituent",
        description="Historical NASDAQ additions and removals.",
        category="indexes",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "NASDAQ changes tracking",
        ],
        returns="Historical NASDAQ changes.",
    ),
    "dowjones_constituent": FMPEndpoint(
        name="dowjones_constituent",
        function="dowjones_constituent",
        description="Current Dow Jones Industrial Average constituents.",
        category="indexes",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "DJIA stock list",
            "Blue chip analysis",
        ],
        returns="Dow Jones constituents.",
    ),
    "historical_dowjones_constituent": FMPEndpoint(
        name="historical_dowjones_constituent",
        function="historical_dowjones_constituent",
        description="Historical Dow Jones additions and removals.",
        category="indexes",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "DJIA changes tracking",
        ],
        returns="Historical Dow Jones changes.",
    ),
    # =========================================================================
    # INSTITUTIONAL & OWNERSHIP
    # =========================================================================
    "institutional_holders": FMPEndpoint(
        name="institutional_holders",
        function="institutional_holders",
        description="Major institutional investors holding a stock.",
        category="ownership",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Institutional ownership analysis",
            "Smart money tracking",
            "Ownership concentration",
        ],
        returns="Institutional holders with holder name, shares, dateReported, change, changePercentage.",
    ),
    "mutual_fund_holders": FMPEndpoint(
        name="mutual_fund_holders",
        function="mutual_fund_holders",
        description="Mutual funds holding a stock.",
        category="ownership",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Mutual fund ownership tracking",
            "Fund flow analysis",
        ],
        returns="Mutual fund holders data.",
    ),
    "etf_holders": FMPEndpoint(
        name="etf_holders",
        function="etf_holders",
        description="ETFs holding a specific stock.",
        category="ownership",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "ETF exposure analysis",
            "Passive ownership tracking",
        ],
        returns="ETF holders data.",
    ),
    "form_13f": FMPEndpoint(
        name="form_13f",
        function="form_13f",
        description="Form 13F filings showing institutional holdings over $100M AUM.",
        category="ownership",
        parameters={
            "cik_id": {"type": "str", "required": True, "description": "CIK of institution"},
            "date": {"type": "str", "required": False, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Institutional portfolio analysis",
            "Hedge fund tracking",
        ],
        returns="13F holdings with cusip, symbol, shares, value.",
    ),
    # =========================================================================
    # ETF DATA
    # =========================================================================
    "etf_sector_weightings": FMPEndpoint(
        name="etf_sector_weightings",
        function="etf_sector_weightings",
        description="Sector weightings for an ETF.",
        category="etf",
        parameters={
            "symbol": {"type": "str", "required": True, "description": "ETF symbol"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "ETF sector exposure analysis",
            "Portfolio diversification assessment",
        ],
        returns="Sector weightings with sector and weightPercentage.",
    ),
    "etf_country_weightings": FMPEndpoint(
        name="etf_country_weightings",
        function="etf_country_weightings",
        description="Country/geographic weightings for an ETF.",
        category="etf",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Geographic exposure analysis",
            "International diversification",
        ],
        returns="Country weightings data.",
    ),
    # =========================================================================
    # INSIDER TRADING
    # =========================================================================
    "insider_trading": FMPEndpoint(
        name="insider_trading",
        function="insider_trading",
        description="Insider trading transactions (Form 4 filings).",
        category="ownership",
        parameters={
            "symbol": {"type": "str", "required": False},
            "reporting_cik": {"type": "int", "required": False},
            "company_cik": {"type": "int", "required": False},
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Insider sentiment analysis",
            "Executive trading patterns",
            "Insider buying/selling signals",
        ],
        returns="Insider trades with reportingName, transactionType, securitiesTransacted, price.",
        notes="Provide only ONE of: symbol, reporting_cik, or company_cik.",
    ),
    "insider_trading_rss_feed": FMPEndpoint(
        name="insider_trading_rss_feed",
        function="insider_trading_rss_feed",
        description="Real-time RSS feed of insider trading activity.",
        category="ownership",
        parameters={
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Real-time insider activity monitoring",
            "Breaking insider trades",
        ],
        returns="Latest insider trades.",
    ),
    # =========================================================================
    # SENATE TRADING
    # =========================================================================
    "senate_trading_rss": FMPEndpoint(
        name="senate_trading_rss",
        function="senate_trading_rss",
        description="RSS feed of Senate member stock trades.",
        category="ownership",
        parameters={
            "page": {"type": "int", "required": False, "default": 0},
        },
        example_use_cases=[
            "Congressional trading tracking",
            "Political insider trading",
        ],
        returns="Senate trading data.",
    ),
    "senate_trading_symbol": FMPEndpoint(
        name="senate_trading_symbol",
        function="senate_trading_symbol",
        description="Senate trades filtered by stock symbol.",
        category="ownership",
        parameters={
            "symbol": {"type": "str", "required": True},
        },
        example_use_cases=[
            "Congressional trades in specific stocks",
        ],
        returns="Senate trades for the symbol.",
    ),
    "senate_disclosure_rss": FMPEndpoint(
        name="senate_disclosure_rss",
        function="senate_disclosure_rss",
        description="RSS feed of Senate financial disclosures.",
        category="ownership",
        parameters={
            "page": {"type": "int", "required": False, "default": 0},
        },
        example_use_cases=[
            "Senate disclosure monitoring",
        ],
        returns="Senate disclosure data.",
    ),
    "senate_disclosure_symbol": FMPEndpoint(
        name="senate_disclosure_symbol",
        function="senate_disclosure_symbol",
        description="Senate disclosures filtered by stock symbol.",
        category="ownership",
        parameters={
            "symbol": {"type": "str", "required": True},
        },
        example_use_cases=[
            "Senate holdings in specific stocks",
        ],
        returns="Senate disclosures for the symbol.",
    ),
    # =========================================================================
    # DIVIDENDS & SPLITS
    # =========================================================================
    "historical_stock_dividend": FMPEndpoint(
        name="historical_stock_dividend",
        function="historical_stock_dividend",
        description="Historical dividend payments for a company.",
        category="dividends",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Dividend history analysis",
            "Dividend growth tracking",
            "Income investing research",
        ],
        returns="Historical dividends with date, label, adjDividend, dividend.",
    ),
    "historical_stock_split": FMPEndpoint(
        name="historical_stock_split",
        function="historical_stock_split",
        description="Historical stock splits for a company.",
        category="corporate_actions",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Split history analysis",
            "Price adjustment research",
        ],
        returns="Historical splits with date, label, numerator, denominator.",
    ),
    # =========================================================================
    # SHARES FLOAT
    # =========================================================================
    "shares_float": FMPEndpoint(
        name="shares_float",
        function="shares_float",
        description="Shares float - publicly traded shares available for trading.",
        category="market",
        parameters={
            "symbol": {"type": "str", "required": True},
            "all": {"type": "bool", "required": False, "default": False},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Float analysis",
            "Short squeeze potential",
            "Liquidity assessment",
        ],
        returns="Shares float with symbol, date, freeFloat, floatShares, outstandingShares.",
    ),
    "historical_share_float": FMPEndpoint(
        name="historical_share_float",
        function="historical_share_float",
        description="Historical shares float data over time.",
        category="market",
        parameters={
            "symbol": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Float changes over time",
            "Dilution tracking",
        ],
        returns="Historical float data.",
    ),
    # =========================================================================
    # SOCIAL SENTIMENT
    # =========================================================================
    "historical_social_sentiment": FMPEndpoint(
        name="historical_social_sentiment",
        function="historical_social_sentiment",
        description="Historical social media sentiment for a stock.",
        category="sentiment",
        parameters={
            "symbol": {"type": "str", "required": True},
            "page": {"type": "int", "required": False, "default": 0},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Social sentiment trends",
            "Retail investor sentiment",
        ],
        returns="Social sentiment data with date and sentiment metrics.",
    ),
    "trending_social_sentiment": FMPEndpoint(
        name="trending_social_sentiment",
        function="trending_social_sentiment",
        description="Currently trending stocks by social sentiment.",
        category="sentiment",
        parameters={
            "sentiment_type": {"type": "str", "required": False, "default": "bullish", "options": ["bullish", "bearish"]},
            "source": {"type": "str", "required": False, "default": "stocktwits", "options": ["stocktwits", "twitter"]},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Trending stock discovery",
            "Social momentum tracking",
        ],
        returns="Trending stocks by sentiment.",
    ),
    "social_sentiment_changes": FMPEndpoint(
        name="social_sentiment_changes",
        function="social_sentiment_changes",
        description="Changes in social sentiment over time.",
        category="sentiment",
        parameters={
            "sentiment_type": {"type": "str", "required": False, "default": "bullish"},
            "source": {"type": "str", "required": False, "default": "stocktwits"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Sentiment shift detection",
            "Momentum changes",
        ],
        returns="Sentiment change data.",
    ),
    # =========================================================================
    # TECHNICAL INDICATORS
    # =========================================================================
    "technical_indicators": FMPEndpoint(
        name="technical_indicators",
        function="technical_indicators",
        description="Technical indicators (SMA, EMA, RSI, MACD, etc.).",
        category="technical",
        parameters={
            "symbol": {"type": "str", "required": True},
            "period": {"type": "int", "required": False, "default": 10},
            "statistics_type": {"type": "str", "required": False, "default": "sma", "options": ["sma", "ema", "wma", "dema", "tema", "williams", "rsi", "adx", "standardDeviation"]},
            "time_delta": {"type": "str", "required": False, "default": "1day", "options": ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Technical analysis",
            "Trading signals",
            "Trend identification",
        ],
        returns="Technical indicator values with date and indicator value.",
    ),
    # =========================================================================
    # ECONOMICS
    # =========================================================================
    "treasury_rates": FMPEndpoint(
        name="treasury_rates",
        function="treasury_rates",
        description="US Treasury rates across all maturities.",
        category="economics",
        parameters={
            "from_date": {"type": "str", "required": False},
            "to_date": {"type": "str", "required": False},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Interest rate analysis",
            "Yield curve research",
            "Risk-free rate lookup",
        ],
        returns="Treasury rates with date and rates for various maturities.",
    ),
    "economic_indicators": FMPEndpoint(
        name="economic_indicators",
        function="economic_indicators",
        description="Economic indicators (GDP, CPI, unemployment, etc.).",
        category="economics",
        parameters={
            "name": {"type": "str", "required": True, "description": "Indicator name (GDP, CPI, unemploymentRate, etc.)"},
            "from_date": {"type": "str", "required": False},
            "to_date": {"type": "str", "required": False},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Macro economic analysis",
            "GDP tracking",
            "Inflation monitoring",
        ],
        returns="Economic indicator values with date and value.",
    ),
    "market_risk_premium": FMPEndpoint(
        name="market_risk_premium",
        function="market_risk_premium",
        description="Market risk premium by country for CAPM calculations.",
        category="economics",
        parameters={
            "country": {"type": "str", "required": False},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "CAPM calculations",
            "Cost of equity estimation",
        ],
        returns="Market risk premium data.",
    ),
    # =========================================================================
    # FOREX
    # =========================================================================
    "forex": FMPEndpoint(
        name="forex",
        function="forex",
        description="Real-time forex prices for all currency pairs.",
        category="forex",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Currency rate lookup",
            "FX market overview",
        ],
        returns="Forex prices with ticker, bid, ask, changes.",
    ),
    "forex_list": FMPEndpoint(
        name="forex_list",
        function="forex_list",
        description="Full quote list for all forex currency pairs.",
        category="forex",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Complete FX market data",
        ],
        returns="Full forex quotes.",
    ),
    "forex_quote": FMPEndpoint(
        name="forex_quote",
        function="forex_quote",
        description="Full quote for a specific forex pair.",
        category="forex",
        parameters={
            "symbol": {"type": "str", "required": True, "description": "Currency pair (e.g., 'EURUSD')"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Specific currency pair quote",
        ],
        returns="Forex quote data.",
    ),
    "forex_historical": FMPEndpoint(
        name="forex_historical",
        function="forex_historical",
        description="Historical forex data for a currency pair.",
        category="forex",
        parameters={
            "symbol": {"type": "str", "required": True},
            "from_date": {"type": "str", "required": True},
            "to_date": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Historical FX analysis",
            "Currency trend research",
        ],
        returns="Historical forex prices.",
    ),
    # =========================================================================
    # CRYPTO
    # =========================================================================
    "cryptocurrency_quote": FMPEndpoint(
        name="cryptocurrency_quote",
        function="cryptocurrency_quote",
        description="Real-time cryptocurrency quote.",
        category="crypto",
        parameters={
            "symbol": {"type": "str", "required": True, "description": "Crypto pair (e.g., 'BTCUSD')"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Crypto price lookup",
            "Bitcoin/Ethereum quotes",
        ],
        returns="Cryptocurrency quote data.",
    ),
    "cryptocurrencies_list": FMPEndpoint(
        name="cryptocurrencies_list",
        function="cryptocurrencies_list",
        description="Full quotes for all cryptocurrencies.",
        category="crypto",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Full crypto market overview",
        ],
        returns="All cryptocurrency quotes.",
    ),
    # =========================================================================
    # COMMODITIES
    # =========================================================================
    "commodity_price": FMPEndpoint(
        name="commodity_price",
        function="commodity_price",
        description="Historical commodity price data.",
        category="commodities",
        parameters={
            "symbol": {"type": "str", "required": True, "description": "Commodity symbol (e.g., 'ZGUSD')"},
            "from_date": {"type": "str", "required": False},
            "to_date": {"type": "str", "required": False},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Commodity price analysis",
            "Gold/oil/silver prices",
        ],
        returns="Commodity price data.",
    ),
    "commodities_list": FMPEndpoint(
        name="commodities_list",
        function="commodities_list",
        description="Full quotes for all commodities.",
        category="commodities",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Commodities market overview",
        ],
        returns="All commodity quotes.",
    ),
    # =========================================================================
    # STOCK SCREENER
    # =========================================================================
    "stock_screener": FMPEndpoint(
        name="stock_screener",
        function="stock_screener",
        description="Screen stocks based on financial criteria (market cap, beta, dividend, etc.).",
        category="screener",
        parameters={
            "market_cap_more_than": {"type": "float", "required": False},
            "market_cap_lower_than": {"type": "float", "required": False},
            "beta_more_than": {"type": "float", "required": False},
            "beta_lower_than": {"type": "float", "required": False},
            "volume_more_than": {"type": "float", "required": False},
            "volume_lower_than": {"type": "float", "required": False},
            "dividend_more_than": {"type": "float", "required": False},
            "dividend_lower_than": {"type": "float", "required": False},
            "price_more_than": {"type": "float", "required": False},
            "price_lower_than": {"type": "float", "required": False},
            "is_etf": {"type": "bool", "required": False},
            "is_fund": {"type": "bool", "required": False},
            "is_actively_trading": {"type": "bool", "required": False},
            "sector": {"type": "str", "required": False},
            "industry": {"type": "str", "required": False},
            "country": {"type": "str", "required": False},
            "exchange": {"type": "str or list", "required": False},
            "limit": {"type": "int", "required": False, "default": 10},
        },
        example_use_cases=[
            "Investment screening",
            "Stock discovery by criteria",
            "Sector-specific searches",
        ],
        returns="Screened stocks with symbol, companyName, marketCap, sector, etc.",
    ),
    # =========================================================================
    # SEARCH
    # =========================================================================
    "search": FMPEndpoint(
        name="search",
        function="search",
        description="Search for stocks, ETFs, and financial instruments by name or ticker.",
        category="search",
        parameters={
            "query": {"type": "str", "required": False, "description": "Search query"},
            "limit": {"type": "int", "required": False, "default": 10},
            "exchange": {"type": "str", "required": False},
        },
        example_use_cases=[
            "Find stock by name",
            "Ticker lookup",
        ],
        returns="Search results with symbol, name, currency, stockExchange.",
    ),
    "search_ticker": FMPEndpoint(
        name="search_ticker",
        function="search_ticker",
        description="Search specifically for ticker symbols.",
        category="search",
        parameters={
            "query": {"type": "str", "required": False},
            "limit": {"type": "int", "required": False, "default": 10},
            "exchange": {"type": "str", "required": False},
        },
        example_use_cases=[
            "Ticker symbol lookup",
        ],
        returns="Ticker search results.",
    ),
    # =========================================================================
    # REFERENCE DATA
    # =========================================================================
    "symbols_list": FMPEndpoint(
        name="symbols_list",
        function="symbols_list",
        description="Full list of all available stock symbols.",
        category="reference",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Complete stock universe",
        ],
        returns="All stock symbols.",
    ),
    "etf_list": FMPEndpoint(
        name="etf_list",
        function="etf_list",
        description="Full list of all available ETFs.",
        category="reference",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "ETF universe",
        ],
        returns="All ETF symbols.",
    ),
    "available_traded_list": FMPEndpoint(
        name="available_traded_list",
        function="available_traded_list",
        description="List of all tradable symbols.",
        category="reference",
        parameters={},
        example_use_cases=[
            "Tradable securities list",
        ],
        returns="All tradable symbols.",
    ),
    "available_forex": FMPEndpoint(
        name="available_forex",
        function="available_forex",
        description="List of available forex currency pairs.",
        category="reference",
        parameters={},
        example_use_cases=[
            "FX pair availability",
        ],
        returns="Available forex pairs.",
    ),
    "available_cryptocurrencies": FMPEndpoint(
        name="available_cryptocurrencies",
        function="available_cryptocurrencies",
        description="List of available cryptocurrencies.",
        category="reference",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Crypto availability",
        ],
        returns="Available cryptocurrencies.",
    ),
    "available_commodities": FMPEndpoint(
        name="available_commodities",
        function="available_commodities",
        description="List of available commodities.",
        category="reference",
        parameters={},
        example_use_cases=[
            "Commodity availability",
        ],
        returns="Available commodities.",
    ),
    "available_etfs": FMPEndpoint(
        name="available_etfs",
        function="available_etfs",
        description="List of available ETFs.",
        category="reference",
        parameters={},
        example_use_cases=[
            "ETF availability",
        ],
        returns="Available ETFs.",
    ),
    "available_indexes": FMPEndpoint(
        name="available_indexes",
        function="available_indexes",
        description="List of available market indexes.",
        category="reference",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Index availability",
        ],
        returns="Available indexes.",
    ),
    "available_sectors": FMPEndpoint(
        name="available_sectors",
        function="available_sectors",
        description="List of available market sectors.",
        category="reference",
        parameters={},
        example_use_cases=[
            "Sector list for screening",
        ],
        returns="Available sectors.",
    ),
    "available_industries": FMPEndpoint(
        name="available_industries",
        function="available_industries",
        description="List of available industries.",
        category="reference",
        parameters={},
        example_use_cases=[
            "Industry list for screening",
        ],
        returns="Available industries.",
    ),
    "available_exchanges": FMPEndpoint(
        name="available_exchanges",
        function="available_exchanges",
        description="List of available stock exchanges.",
        category="reference",
        parameters={},
        example_use_cases=[
            "Exchange list",
        ],
        returns="Available exchanges.",
    ),
    "all_countries": FMPEndpoint(
        name="all_countries",
        function="all_countries",
        description="List of all countries with market data.",
        category="reference",
        parameters={},
        example_use_cases=[
            "Country availability",
        ],
        returns="All countries.",
    ),
    "delisted_companies": FMPEndpoint(
        name="delisted_companies",
        function="delisted_companies",
        description="List of delisted companies.",
        category="reference",
        parameters={
            "limit": {"type": "int", "required": False, "default": 10},
        },
        example_use_cases=[
            "Historical delisting tracking",
        ],
        returns="Delisted companies.",
    ),
    "financial_statement_symbol_lists": FMPEndpoint(
        name="financial_statement_symbol_lists",
        function="financial_statement_symbol_lists",
        description="Symbols with available financial statements.",
        category="reference",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Find companies with financials",
        ],
        returns="Symbols with financial statements.",
    ),
    # =========================================================================
    # CIK MAPPING
    # =========================================================================
    "cik": FMPEndpoint(
        name="cik",
        function="cik",
        description="Get company name by CIK.",
        category="reference",
        parameters={
            "cik_id": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "CIK to company lookup",
        ],
        returns="Company name for CIK.",
    ),
    "cik_list": FMPEndpoint(
        name="cik_list",
        function="cik_list",
        description="Full list of CIK numbers.",
        category="reference",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "CIK database",
        ],
        returns="CIK list.",
    ),
    "cik_search": FMPEndpoint(
        name="cik_search",
        function="cik_search",
        description="Search for CIK by company name.",
        category="reference",
        parameters={
            "name": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Find CIK by name",
        ],
        returns="CIK search results.",
    ),
    "cusip": FMPEndpoint(
        name="cusip",
        function="cusip",
        description="CUSIP mapper for CIK.",
        category="reference",
        parameters={
            "cik_id": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "CUSIP lookup",
        ],
        returns="CUSIP data.",
    ),
    "mapper_cik_name": FMPEndpoint(
        name="mapper_cik_name",
        function="mapper_cik_name",
        description="Map CIK to insider names.",
        category="reference",
        parameters={
            "name": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Find CIK for insider",
        ],
        returns="CIK mapping.",
    ),
    "mapper_cik_company": FMPEndpoint(
        name="mapper_cik_company",
        function="mapper_cik_company",
        description="Map ticker to company CIK.",
        category="reference",
        parameters={
            "ticker": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Find CIK for ticker",
        ],
        returns="Company CIK.",
    ),
    # =========================================================================
    # ALTERNATIVE DATA
    # =========================================================================
    "commitment_of_traders_report_list": FMPEndpoint(
        name="commitment_of_traders_report_list",
        function="commitment_of_traders_report_list",
        description="List of available COT report symbols.",
        category="alternative",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "COT report availability",
        ],
        returns="COT symbols.",
    ),
    "commitment_of_traders_report": FMPEndpoint(
        name="commitment_of_traders_report",
        function="commitment_of_traders_report",
        description="CFTC Commitment of Traders report data.",
        category="alternative",
        parameters={
            "symbol": {"type": "str", "required": True},
            "from_date": {"type": "str", "required": False},
            "to_date": {"type": "str", "required": False},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Futures positioning analysis",
            "Speculator vs hedger activity",
        ],
        returns="COT report data.",
    ),
    "commitment_of_traders_report_analysis": FMPEndpoint(
        name="commitment_of_traders_report_analysis",
        function="commitment_of_traders_report_analysis",
        description="Analysis of COT report data.",
        category="alternative",
        parameters={
            "symbol": {"type": "str", "required": True},
            "from_date": {"type": "str", "required": True},
            "to_date": {"type": "str", "required": True},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "COT trend analysis",
        ],
        returns="COT analysis data.",
    ),
    "fail_to_deliver": FMPEndpoint(
        name="fail_to_deliver",
        function="fail_to_deliver",
        description="Fail-to-deliver data showing settlement failures.",
        category="alternative",
        parameters={
            "symbol": {"type": "str", "required": True},
            "page": {"type": "int", "required": False, "default": 0},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Short selling analysis",
            "Settlement issues tracking",
        ],
        returns="FTD data.",
    ),
    "sector_pe_ratio": FMPEndpoint(
        name="sector_pe_ratio",
        function="sector_pe_ratio",
        description="Sector-level P/E ratios.",
        category="valuation",
        parameters={
            "date": {"type": "str", "required": True, "description": "YYYY-MM-DD"},
            "exchange": {"type": "str", "required": False, "default": "NYSE"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Sector valuation comparison",
        ],
        returns="Sector PE ratios.",
    ),
    "industry_pe_ratio": FMPEndpoint(
        name="industry_pe_ratio",
        function="industry_pe_ratio",
        description="Industry-level P/E ratios.",
        category="valuation",
        parameters={
            "date": {"type": "str", "required": True, "description": "YYYY-MM-DD"},
            "exchange": {"type": "str", "required": False, "default": "NYSE"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Industry valuation comparison",
        ],
        returns="Industry PE ratios.",
    ),
    "batch_eod_prices": FMPEndpoint(
        name="batch_eod_prices",
        function="batch_eod_prices",
        description="End of day prices for all stocks on a specific date.",
        category="market",
        parameters={
            "date": {"type": "str", "required": True, "description": "YYYY-MM-DD"},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Historical EOD snapshot",
            "Bulk price data",
        ],
        returns="All EOD prices for the date.",
    ),
    "sec_rss_feeds": FMPEndpoint(
        name="sec_rss_feeds",
        function="sec_rss_feeds",
        description="SEC RSS feed of latest filings.",
        category="sec",
        parameters={
            "limit": {"type": "int", "required": False, "default": 10},
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=[
            "Latest SEC filings",
            "Real-time filing monitoring",
        ],
        returns="Latest SEC filings.",
    ),
    "exchange_realtime": FMPEndpoint(
        name="exchange_realtime",
        function="exchange_realtime",
        description="Real-time quotes for all stocks on an exchange.",
        category="market",
        parameters={
            "exchange": {"type": "str", "required": True, "description": "Exchange symbol"},
        },
        example_use_cases=[
            "Exchange-wide real-time data",
        ],
        returns="Real-time quotes for exchange.",
    ),
    # =========================================================================
    # CROWDFUNDING
    # =========================================================================
    "crowdfunding_rss_feed": FMPEndpoint(
        name="crowdfunding_rss_feed",
        function="crowdfunding_rss_feed",
        description="RSS feed of crowdfunding campaigns.",
        category="alternative",
        parameters={
            "page": {"type": "int", "required": False, "default": 0},
        },
        example_use_cases=[
            "Crowdfunding monitoring",
        ],
        returns="Crowdfunding campaigns.",
    ),
    "crowdfunding_search": FMPEndpoint(
        name="crowdfunding_search",
        function="crowdfunding_search",
        description="Search crowdfunding campaigns by name.",
        category="alternative",
        parameters={
            "name": {"type": "str", "required": True},
        },
        example_use_cases=[
            "Find specific crowdfunding campaigns",
        ],
        returns="Matching crowdfunding campaigns.",
    ),
    "crowdfunding_by_cik": FMPEndpoint(
        name="crowdfunding_by_cik",
        function="crowdfunding_by_cik",
        description="Crowdfunding campaigns by company CIK.",
        category="alternative",
        parameters={
            "cik": {"type": "str", "required": True},
        },
        example_use_cases=[
            "Company-specific crowdfunding",
        ],
        returns="Crowdfunding campaigns for CIK.",
    ),
    # Additional reference data
    "available_mutual_funds": FMPEndpoint(
        name="available_mutual_funds",
        function="available_mutual_funds",
        description="List of available mutual funds.",
        category="reference",
        parameters={},
        example_use_cases=["Mutual fund availability"],
        returns="Available mutual funds.",
    ),
    "available_tsx": FMPEndpoint(
        name="available_tsx",
        function="available_tsx",
        description="List of available TSX symbols.",
        category="reference",
        parameters={},
        example_use_cases=["TSX availability"],
        returns="Available TSX symbols.",
    ),
    "available_euronext": FMPEndpoint(
        name="available_euronext",
        function="available_euronext",
        description="List of available Euronext stocks.",
        category="reference",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=["Euronext availability"],
        returns="Available Euronext stocks.",
    ),
    "mutual_fund_list": FMPEndpoint(
        name="mutual_fund_list",
        function="mutual_fund_list",
        description="Full quotes for all mutual funds.",
        category="market",
        parameters={
            "output": {"type": "str", "required": False, "default": "markdown"},
        },
        example_use_cases=["Mutual fund quotes"],
        returns="All mutual fund quotes.",
    ),
    "tsx_list": FMPEndpoint(
        name="tsx_list",
        function="tsx_list",
        description="TSX stocks data.",
        category="market",
        parameters={},
        example_use_cases=["TSX market data"],
        returns="TSX stocks data.",
    ),
}


# =============================================================================
# CATEGORY DEFINITIONS
# =============================================================================

CATEGORIES = {
    "financials": "Core financial statements (income, balance sheet, cash flow)",
    "earnings": "Earnings calls, transcripts, and surprises",
    "sec": "SEC filings and regulatory documents",
    "company": "Company profile, executives, and corporate information",
    "metrics": "Key financial metrics and ratios",
    "growth": "Financial growth metrics",
    "valuation": "Valuation metrics (DCF, market cap, PE ratios)",
    "analysts": "Analyst ratings, estimates, and recommendations",
    "price_targets": "Analyst price targets",
    "esg": "Environmental, Social, and Governance scores",
    "segments": "Business and geographic segment data",
    "corporate_actions": "M&A, splits, and other corporate actions",
    "news": "News, press releases, and RSS feeds",
    "calendar": "Earnings, dividend, IPO, and economic calendars",
    "market": "Real-time market data, quotes, and movers",
    "indexes": "Market indexes and constituents",
    "ownership": "Institutional ownership, insider trading, 13F filings",
    "etf": "ETF-specific data (holdings, weightings)",
    "dividends": "Dividend history and payments",
    "sentiment": "Social sentiment data",
    "technical": "Technical indicators",
    "economics": "Economic indicators and treasury rates",
    "forex": "Foreign exchange data",
    "crypto": "Cryptocurrency data",
    "commodities": "Commodity prices",
    "screener": "Stock screening tools",
    "search": "Search functionality",
    "reference": "Reference data (symbol lists, exchanges, etc.)",
    "alternative": "Alternative data (COT, crowdfunding, FTD)",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_endpoints_by_category(category: str) -> List[FMPEndpoint]:
    """Get all endpoints in a specific category.

    Args:
        category: Category name (e.g., 'financials', 'sec', 'news')

    Returns:
        List of FMPEndpoint objects in the category
    """
    return [ep for ep in FMP_REGISTRY.values() if ep.category == category]


def get_all_categories() -> List[str]:
    """Get all available categories.

    Returns:
        List of category names
    """
    return list(CATEGORIES.keys())


def get_registry_for_llm(
    categories: Optional[List[str]] = None,
    include_parameters: bool = True,
    include_use_cases: bool = True,
) -> str:
    """Format registry as context for LLM schema generation.

    Groups endpoints by category with descriptions and use cases.
    Designed to be token-efficient while providing comprehensive information.

    Args:
        categories: Optional list of categories to include. If None, includes all.
        include_parameters: Whether to include parameter details
        include_use_cases: Whether to include example use cases

    Returns:
        Formatted string suitable for LLM context
    """
    lines = ["# AVAILABLE FMP DATA SOURCES", ""]

    # Filter categories if specified
    cats_to_include = categories if categories else list(CATEGORIES.keys())

    for cat in cats_to_include:
        if cat not in CATEGORIES:
            continue

        endpoints = get_endpoints_by_category(cat)
        if not endpoints:
            continue

        # Category header
        lines.append(f"## {cat.upper().replace('_', ' ')}")
        lines.append(f"_{CATEGORIES[cat]}_")
        lines.append("")

        for ep in endpoints:
            # Endpoint name and description
            lines.append(f"### {ep.name}")
            lines.append(f"**Function:** `fmpsdk.{ep.function}()`")
            lines.append(f"**Description:** {ep.description}")

            # Parameters
            if include_parameters and ep.parameters:
                params_str = []
                for param, details in ep.parameters.items():
                    if isinstance(details, dict):
                        req = "required" if details.get("required") else "optional"
                        default = f", default={details.get('default')}" if "default" in details else ""
                        options = f", options={details.get('options')}" if "options" in details else ""
                        params_str.append(f"  - `{param}` ({details.get('type', 'any')}, {req}{default}{options})")
                    else:
                        params_str.append(f"  - `{param}`: {details}")
                if params_str:
                    lines.append("**Parameters:**")
                    lines.extend(params_str)

            # Use cases
            if include_use_cases and ep.example_use_cases:
                lines.append("**Use when:**")
                for uc in ep.example_use_cases[:3]:  # Limit to 3 use cases
                    lines.append(f"  - {uc}")

            # Returns
            lines.append(f"**Returns:** {ep.returns}")

            # Notes
            if ep.notes:
                lines.append(f"**Note:** {ep.notes}")

            lines.append("")

    return "\n".join(lines)


def get_compact_registry_for_llm() -> str:
    """Get a compact version of the registry for token-limited contexts.

    Returns:
        Compact formatted string
    """
    lines = ["# FMP DATA SOURCES (Compact)", ""]

    for cat, desc in CATEGORIES.items():
        endpoints = get_endpoints_by_category(cat)
        if not endpoints:
            continue

        lines.append(f"## {cat.upper()}: {desc}")
        for ep in endpoints:
            params = ", ".join(ep.parameters.keys()) if ep.parameters else "none"
            lines.append(f"- **{ep.name}**({params}): {ep.description[:100]}...")
        lines.append("")

    return "\n".join(lines)


def search_endpoints(query: str) -> List[FMPEndpoint]:
    """Search endpoints by keyword.

    Args:
        query: Search query

    Returns:
        List of matching FMPEndpoint objects
    """
    query_lower = query.lower()
    results = []

    for ep in FMP_REGISTRY.values():
        if (
            query_lower in ep.name.lower()
            or query_lower in ep.description.lower()
            or query_lower in ep.category.lower()
            or any(query_lower in uc.lower() for uc in ep.example_use_cases)
        ):
            results.append(ep)

    return results
