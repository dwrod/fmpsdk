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
    """Registry entry for an FMP endpoint.

    GEN-92: Parameters are now extracted from function signatures at runtime.
    GEN-93: Added example field for LLM-friendly function call examples.
    """

    name: str  # Canonical name (e.g., "income_statement")
    function: str  # fmpsdk function name
    description: str  # LLM-friendly description
    category: str  # Category for grouping
    example_use_cases: List[str]  # When to use this endpoint
    returns: str  # Description of return data structure
    example: Optional[str] = None  # Example function call for LLM
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
        example_use_cases=[
            "Revenue trend analysis over multiple years",
            "Profitability assessment and margin analysis",
            "Year-over-year growth comparison",
            "Cost structure analysis",
        ],
        returns="List of income statements with date, revenue, grossProfit, operatingIncome, netIncome, eps, etc.",
        example="income_statement('AAPL', period='annual', limit=5)",
    ),
    "balance_sheet_statement": FMPEndpoint(
        name="balance_sheet_statement",
        function="balance_sheet_statement",
        description="Annual or quarterly balance sheet data including assets, liabilities, and equity. Shows financial position at specific points in time.",
        category="financials",
        example_use_cases=[
            "Asset composition analysis",
            "Debt level assessment",
            "Working capital analysis",
            "Shareholder equity trends",
        ],
        returns="List of balance sheets with totalAssets, totalLiabilities, totalEquity, cash, inventory, etc.",
        example="balance_sheet_statement('MSFT', period='quarter', limit=8)",
    ),
    "cash_flow_statement": FMPEndpoint(
        name="cash_flow_statement",
        function="cash_flow_statement",
        description="Annual or quarterly cash flow statement showing operating, investing, and financing activities. Reveals actual cash generation and usage.",
        category="financials",
        example_use_cases=[
            "Free cash flow analysis",
            "Capital expenditure trends",
            "Dividend sustainability assessment",
            "Cash conversion analysis",
        ],
        returns="List of cash flow statements with operatingCashFlow, investingCashFlow, financingCashFlow, freeCashFlow, etc.",
        example="cash_flow_statement('GOOGL', period='annual', limit=5)",
    ),
    "income_statement_as_reported": FMPEndpoint(
        name="income_statement_as_reported",
        function="income_statement_as_reported",
        description="Income statement exactly as reported in SEC filings, without standardization. Useful for detailed analysis matching company-specific terminology.",
        category="financials",
        example_use_cases=[
            "Detailed SEC filing analysis",
            "Company-specific line item research",
            "Audit and compliance checks",
        ],
        returns="As-reported income statement data with original SEC filing field names.",
        example="income_statement_as_reported('TSLA', period='annual', limit=3)",
    ),
    "balance_sheet_statement_as_reported": FMPEndpoint(
        name="balance_sheet_statement_as_reported",
        function="balance_sheet_statement_as_reported",
        description="Balance sheet exactly as reported in SEC filings, without standardization.",
        category="financials",
        example_use_cases=[
            "Detailed SEC filing analysis",
            "Company-specific asset/liability categorization",
        ],
        returns="As-reported balance sheet data with original SEC filing field names.",
        example="balance_sheet_statement_as_reported('AMZN', period='annual', limit=3)",
    ),
    "cash_flow_statement_as_reported": FMPEndpoint(
        name="cash_flow_statement_as_reported",
        function="cash_flow_statement_as_reported",
        description="Cash flow statement exactly as reported in SEC filings, without standardization.",
        category="financials",
        example_use_cases=[
            "Detailed SEC filing analysis",
            "Company-specific cash flow categorization",
        ],
        returns="As-reported cash flow statement data with original SEC filing field names.",
        example="cash_flow_statement_as_reported('META', period='annual', limit=3)",
    ),
    "financial_statement_full_as_reported": FMPEndpoint(
        name="financial_statement_full_as_reported",
        function="financial_statement_full_as_reported",
        description="Complete financial statements as reported in SEC filings, combining income, balance sheet, and cash flow.",
        category="financials",
        example_use_cases=[
            "Comprehensive SEC filing analysis",
            "Full financial picture from original filings",
        ],
        returns="Complete as-reported financial statement data.",
        example="financial_statement_full_as_reported('NVDA', period='annual')",
    ),
    "earnings_surprises": FMPEndpoint(
        name="earnings_surprises",
        function="earnings_surprises",
        description="Historical earnings surprises showing actual vs estimated EPS. Reveals how often a company beats or misses expectations.",
        category="financials",
        example_use_cases=[
            "Earnings beat/miss pattern analysis",
            "Management guidance accuracy assessment",
            "Earnings quality evaluation",
        ],
        returns="List of earnings surprises with date, actualEarningResult, estimatedEarning, surprise percentage.",
        example="earnings_surprises('AAPL')",
    ),
    # =========================================================================
    # EARNINGS & TRANSCRIPTS
    # =========================================================================
    "earning_call_transcript": FMPEndpoint(
        name="earning_call_transcript",
        function="earning_call_transcript",
        description="Full text transcript of earnings call for a specific quarter. Contains management commentary, guidance, and Q&A with analysts.",
        category="earnings",
        example_use_cases=[
            "Management sentiment analysis",
            "Strategic initiative tracking",
            "Guidance and outlook extraction",
            "Competitive intelligence from Q&A",
        ],
        returns="Earnings call transcript text with date, symbol, quarter, year, and content.",
        example="earning_call_transcript('AAPL', year=2024, quarter=1)",
        notes="Transcripts can be very long (10k+ words). Consider token limits.",
    ),
    "batch_earning_call_transcript": FMPEndpoint(
        name="batch_earning_call_transcript",
        function="batch_earning_call_transcript",
        description="All earnings call transcripts for a company in a given year. Efficient for annual analysis.",
        category="earnings",
        example_use_cases=[
            "Full year management commentary analysis",
            "Quarterly guidance evolution tracking",
            "Annual narrative analysis",
        ],
        returns="Multiple earnings call transcripts for all quarters in the year.",
        example="batch_earning_call_transcript('MSFT', year=2024)",
        notes="Very large data return - may hit token limits.",
    ),
    "earning_call_transcripts_available_dates": FMPEndpoint(
        name="earning_call_transcripts_available_dates",
        function="earning_call_transcripts_available_dates",
        description="List of available earnings call transcript dates for a company. Use to discover which transcripts are available.",
        category="earnings",
        example_use_cases=[
            "Discover available transcript dates before fetching",
            "Plan transcript analysis scope",
        ],
        returns="List of [quarter, year] pairs with available transcripts.",
        example="earning_call_transcripts_available_dates('GOOGL')",
    ),
    # =========================================================================
    # SEC FILINGS
    # =========================================================================
    "sec_filings": FMPEndpoint(
        name="sec_filings",
        function="sec_filings",
        description="SEC filing metadata and links (10-K, 10-Q, 8-K, etc.). Returns filing dates, types, and URLs but NOT the actual content.",
        category="sec",
        example_use_cases=[
            "Find SEC filing links for further analysis",
            "Track filing history and timing",
            "Identify recent 8-K events",
        ],
        returns="List of filings with type, fillingDate, acceptedDate, cik, link, finalLink.",
        example="sec_filings('AAPL', filing_type='10-K', limit=5)",
    ),
    "sec_filings_data": FMPEndpoint(
        name="sec_filings_data",
        function="sec_filings_data",
        description="Full text content of SEC filings rendered as Markdown. Fetches and parses actual filing content from SEC EDGAR.",
        category="sec",
        example_use_cases=[
            "Deep 10-K analysis for risk factors, business description",
            "8-K event analysis for material events",
            "Historical 10-K trend analysis",
        ],
        returns="Full Markdown-formatted SEC filing content.",
        example="sec_filings_data('TSLA', filing_type='10-K', limit=1)",
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
        example_use_cases=[
            "Company overview and background research",
            "Sector and industry classification",
            "Market cap and basic statistics",
            "Company description for reports",
        ],
        returns="Company profile with symbol, price, beta, mktCap, description, sector, industry, ceo, website, etc.",
        example="company_profile('AAPL')",
    ),
    "key_executives": FMPEndpoint(
        name="key_executives",
        function="key_executives",
        description="Key executives data from SEC filings including names, titles, and compensation.",
        category="company",
        example_use_cases=[
            "Management team analysis",
            "Executive compensation research",
            "Corporate governance assessment",
        ],
        returns="List of executives with name, title, pay, currencyPay, etc.",
        example="key_executives('MSFT')",
    ),
    "company_core_information": FMPEndpoint(
        name="company_core_information",
        function="company_core_information",
        description="Core company information including CIK, exchange, SIC code, and state of incorporation.",
        category="company",
        example_use_cases=[
            "Regulatory and compliance research",
            "Company registration details",
        ],
        returns="Core info with cik, exchange, sicCode, sicDescription, stateOfIncorporation, etc.",
        example="company_core_information('GOOGL')",
    ),
    "company_outlook": FMPEndpoint(
        name="company_outlook",
        function="company_outlook",
        description="Comprehensive company outlook combining profile, metrics, ratios, and stock data in one call.",
        category="company",
        example_use_cases=[
            "Quick comprehensive company snapshot",
            "All-in-one company analysis",
        ],
        returns="Combined data including profile, metrics, ratios, stock data, insider transactions, and more.",
        example="company_outlook('AMZN')",
    ),
    "enterprise_values": FMPEndpoint(
        name="enterprise_values",
        function="enterprise_values",
        description="Enterprise value data including market cap, debt, and cash. Shows total company value for M&A analysis.",
        category="company",
        example_use_cases=[
            "M&A valuation analysis",
            "EV/EBITDA calculations",
            "Capital structure analysis",
        ],
        returns="Enterprise value data with date, symbol, enterpriseValue, numberOfShares, addTotalDebt, minusCashAndEquivalents.",
        example="enterprise_values('META', period='annual', limit=5)",
    ),
    # =========================================================================
    # KEY METRICS & RATIOS
    # =========================================================================
    "key_metrics": FMPEndpoint(
        name="key_metrics",
        function="key_metrics",
        description="Key financial metrics including revenue per share, PE ratio, debt to equity, ROE, and more.",
        category="metrics",
        example_use_cases=[
            "Valuation metrics analysis",
            "Profitability metrics tracking",
            "Leverage and efficiency ratios",
        ],
        returns="Key metrics with revenuePerShare, netIncomePerShare, peRatio, debtToEquity, returnOnEquity, etc.",
        example="key_metrics('AAPL', period='annual', limit=5)",
    ),
    "key_metrics_ttm": FMPEndpoint(
        name="key_metrics_ttm",
        function="key_metrics_ttm",
        description="Trailing twelve months (TTM) key metrics for most recent performance snapshot.",
        category="metrics",
        example_use_cases=[
            "Current valuation metrics",
            "Real-time performance snapshot",
        ],
        returns="TTM key metrics data.",
        example="key_metrics_ttm('MSFT')",
    ),
    "financial_ratios": FMPEndpoint(
        name="financial_ratios",
        function="financial_ratios",
        description="Comprehensive financial ratios including liquidity, profitability, debt, and efficiency ratios.",
        category="metrics",
        example_use_cases=[
            "Comprehensive ratio analysis",
            "Peer comparison",
            "Credit analysis",
            "Investment screening",
        ],
        returns="Financial ratios including currentRatio, quickRatio, grossProfitMargin, returnOnAssets, debtRatio, etc.",
        example="financial_ratios('GOOGL', period='annual', limit=5)",
    ),
    "financial_ratios_ttm": FMPEndpoint(
        name="financial_ratios_ttm",
        function="financial_ratios_ttm",
        description="Trailing twelve months financial ratios for current performance.",
        category="metrics",
        example_use_cases=[
            "Current ratio analysis",
            "Real-time performance assessment",
        ],
        returns="TTM financial ratios data.",
        example="financial_ratios_ttm('AMZN')",
    ),
    # =========================================================================
    # GROWTH METRICS
    # =========================================================================
    "financial_growth": FMPEndpoint(
        name="financial_growth",
        function="financial_growth",
        description="Financial growth metrics showing year-over-year or quarter-over-quarter growth rates.",
        category="growth",
        example_use_cases=[
            "Growth trend analysis",
            "Historical growth rate tracking",
            "Growth consistency assessment",
        ],
        returns="Growth metrics with revenueGrowth, netIncomeGrowth, epsgrowth, etc.",
        example="financial_growth('NVDA', period='annual', limit=5)",
    ),
    "income_statement_growth": FMPEndpoint(
        name="income_statement_growth",
        function="income_statement_growth",
        description="Income statement growth metrics showing revenue and profit growth trends.",
        category="growth",
        example_use_cases=[
            "Revenue growth analysis",
            "Profit margin trend analysis",
        ],
        returns="Income statement growth data.",
        example="income_statement_growth('TSLA', limit=5)",
    ),
    "balance_sheet_statement_growth": FMPEndpoint(
        name="balance_sheet_statement_growth",
        function="balance_sheet_statement_growth",
        description="Balance sheet growth metrics showing asset and liability growth trends.",
        category="growth",
        example_use_cases=[
            "Asset growth analysis",
            "Debt growth tracking",
        ],
        returns="Balance sheet growth data.",
        example="balance_sheet_statement_growth('JPM', limit=5)",
    ),
    "cash_flow_statement_growth": FMPEndpoint(
        name="cash_flow_statement_growth",
        function="cash_flow_statement_growth",
        description="Cash flow growth metrics showing operating, investing, and financing cash flow trends.",
        category="growth",
        example_use_cases=[
            "Cash flow growth analysis",
            "Free cash flow trend tracking",
        ],
        returns="Cash flow growth data.",
        example="cash_flow_statement_growth('V', limit=5)",
    ),
    # =========================================================================
    # VALUATION
    # =========================================================================
    "discounted_cash_flow": FMPEndpoint(
        name="discounted_cash_flow",
        function="discounted_cash_flow",
        description="DCF valuation estimating intrinsic value based on projected future cash flows.",
        category="valuation",
        example_use_cases=[
            "Intrinsic value estimation",
            "Under/overvaluation assessment",
            "Value investing screening",
        ],
        returns="DCF data with date, symbol, dcf (intrinsic value), stockPrice.",
        example="discounted_cash_flow('AAPL')",
    ),
    "advanced_discounted_cash_flow": FMPEndpoint(
        name="advanced_discounted_cash_flow",
        function="advanced_discounted_cash_flow",
        description="Advanced DCF model with detailed assumptions and projections.",
        category="valuation",
        example_use_cases=[
            "Detailed intrinsic value analysis",
            "DCF sensitivity analysis",
        ],
        returns="Advanced DCF data with detailed projections and assumptions.",
        example="advanced_discounted_cash_flow('MSFT')",
    ),
    "historical_daily_discounted_cash_flow": FMPEndpoint(
        name="historical_daily_discounted_cash_flow",
        function="historical_daily_discounted_cash_flow",
        description="Daily historical DCF values showing intrinsic value evolution over time.",
        category="valuation",
        example_use_cases=[
            "Historical valuation trends",
            "Valuation gap analysis over time",
        ],
        returns="Historical DCF values with date, symbol, dcf, stockPrice.",
        example="historical_daily_discounted_cash_flow('GOOGL', limit=30)",
    ),
    "market_capitalization": FMPEndpoint(
        name="market_capitalization",
        function="market_capitalization",
        description="Current market capitalization of a company.",
        category="valuation",
        example_use_cases=[
            "Company size classification",
            "Market value assessment",
        ],
        returns="Market cap data with date, symbol, marketCap.",
        example="market_capitalization('AMZN')",
    ),
    "historical_market_capitalization": FMPEndpoint(
        name="historical_market_capitalization",
        function="historical_market_capitalization",
        description="Historical market capitalization showing company value over time.",
        category="valuation",
        example_use_cases=[
            "Market cap growth analysis",
            "Historical size tracking",
        ],
        returns="Historical market cap data.",
        example="historical_market_capitalization('META', limit=100)",
    ),
    # =========================================================================
    # RATINGS & ANALYSTS
    # =========================================================================
    "rating": FMPEndpoint(
        name="rating",
        function="rating",
        description="FMP's proprietary rating based on financial analysis including DCF, ratios, and intrinsic value.",
        category="analysts",
        example_use_cases=[
            "Quick investment rating lookup",
            "Automated screening based on ratings",
        ],
        returns="Rating data with symbol, date, rating, ratingScore, ratingRecommendation, etc.",
        example="rating('AAPL')",
    ),
    "historical_rating": FMPEndpoint(
        name="historical_rating",
        function="historical_rating",
        description="Historical ratings showing how FMP's assessment has changed over time.",
        category="analysts",
        example_use_cases=[
            "Rating trend analysis",
            "Historical sentiment tracking",
        ],
        returns="Historical rating data.",
        example="historical_rating('MSFT', limit=50)",
    ),
    "analyst_estimates": FMPEndpoint(
        name="analyst_estimates",
        function="analyst_estimates",
        description="Wall Street analyst estimates for future earnings, revenue, and EPS.",
        category="analysts",
        example_use_cases=[
            "Forward earnings expectations",
            "Revenue forecast analysis",
            "Consensus estimate tracking",
        ],
        returns="Analyst estimates with estimatedRevenueAvg, estimatedEpsAvg, numberOfAnalysts, etc.",
        example="analyst_estimates('GOOGL', period='annual', limit=4)",
        notes="Estimates are not always accurate - use for guidance only.",
    ),
    "analyst_recommendation": FMPEndpoint(
        name="analyst_recommendation",
        function="analyst_recommendation",
        description="Analyst buy/sell/hold recommendations with analyst firm details.",
        category="analysts",
        example_use_cases=[
            "Analyst sentiment analysis",
            "Recommendation consensus tracking",
            "Analyst coverage assessment",
        ],
        returns="Analyst recommendations with analystName, analystCompany, recommendationKey, etc.",
        example="analyst_recommendation('AMZN')",
    ),
    "stock_grade": FMPEndpoint(
        name="stock_grade",
        function="stock_grade",
        description="Stock grades from hedge funds, investment firms, and analysts.",
        category="analysts",
        example_use_cases=[
            "Professional investor assessment",
            "Grade change tracking",
        ],
        returns="Stock grades with gradingCompany, newGrade, previousGrade, action, etc.",
        example="stock_grade('META', limit=20)",
    ),
    "upgrades_downgrades": FMPEndpoint(
        name="upgrades_downgrades",
        function="upgrades_downgrades",
        description="Stock upgrades and downgrades from analysts.",
        category="analysts",
        example_use_cases=[
            "Rating change tracking",
            "Analyst sentiment shifts",
        ],
        returns="Upgrade/downgrade data with publishedDate, newGrade, previousGrade, gradingCompany.",
        example="upgrades_downgrades('NVDA')",
    ),
    "upgrades_downgrades_consensus": FMPEndpoint(
        name="upgrades_downgrades_consensus",
        function="upgrades_downgrades_consensus",
        description="Consensus rating across all analysts for a stock.",
        category="analysts",
        example_use_cases=[
            "Overall analyst sentiment",
            "Consensus view assessment",
        ],
        returns="Consensus data with symbol, strongBuy, buy, hold, sell, strongSell, consensus.",
        example="upgrades_downgrades_consensus('AAPL')",),
    "upgrades_downgrades_by_company": FMPEndpoint(
        name="upgrades_downgrades_by_company",
        function="upgrades_downgrades_by_company",
        description="All upgrades and downgrades issued by a specific analyst firm.",
        category="analysts",
        example_use_cases=[
            "Track specific analyst firm recommendations",
            "Firm-level research aggregation",
        ],
        returns="All ratings from the specified analyst firm.",
        example="upgrades_downgrades_by_company()",),
    # =========================================================================
    # PRICE TARGETS
    # =========================================================================
    "price_targets": FMPEndpoint(
        name="price_targets",
        function="price_targets",
        description="Analyst price targets for a company's stock.",
        category="price_targets",
        example_use_cases=[
            "Price target analysis",
            "Upside/downside potential assessment",
        ],
        returns="Price targets with analystName, analystCompany, priceTarget, publishedDate.",
        example="price_targets('MSFT')",),
    "price_target_summary": FMPEndpoint(
        name="price_target_summary",
        function="price_target_summary",
        description="Summary of price targets including average, high, low, and number of analysts.",
        category="price_targets",
        example_use_cases=[
            "Quick price target overview",
            "Analyst consensus target",
        ],
        returns="Summary with lastMonth, lastQuarter, high, low, average, median, numberOfAnalysts.",
        example="price_target_summary('GOOGL')",),
    "price_target_consensus": FMPEndpoint(
        name="price_target_consensus",
        function="price_target_consensus",
        description="Consensus price target averaging all analyst targets.",
        category="price_targets",
        example_use_cases=[
            "Consensus price expectation",
            "Overall market target",
        ],
        returns="Consensus price target data.",
        example="price_target_consensus('AMZN')",),
    "price_target_by_analyst_name": FMPEndpoint(
        name="price_target_by_analyst_name",
        function="price_target_by_analyst_name",
        description="Price targets from a specific analyst across different stocks.",
        category="price_targets",
        example_use_cases=[
            "Track specific analyst coverage",
            "Analyst performance tracking",
        ],
        returns="Price targets from the specified analyst.",
        example="price_target_by_analyst_name()",),
    "price_target_by_company": FMPEndpoint(
        name="price_target_by_company",
        function="price_target_by_company",
        description="Price targets from a specific analyst firm.",
        category="price_targets",
        example_use_cases=[
            "Firm-level price targets",
            "Institutional research tracking",
        ],
        returns="Price targets from the specified firm.",
        example="price_target_by_company()",),
    "price_target_rss_feed": FMPEndpoint(
        name="price_target_rss_feed",
        function="price_target_rss_feed",
        description="RSS feed of latest price target updates across all stocks.",
        category="price_targets",
        example_use_cases=[
            "Real-time price target monitoring",
            "Latest analyst actions",
        ],
        returns="Recent price target updates.",
        example="price_target_rss_feed()",),
    # =========================================================================
    # ESG
    # =========================================================================
    "esg_score": FMPEndpoint(
        name="esg_score",
        function="esg_score",
        description="Environmental, Social, and Governance (ESG) scores with breakdown by E, S, and G components.",
        category="esg",
        example_use_cases=[
            "Sustainability analysis",
            "ESG screening",
            "Socially responsible investing research",
            "Renewable energy company assessment",
        ],
        returns="ESG data with environmentalScore, socialScore, governanceScore, ESGScore, etc.",
        example="esg_score('MSFT')",
    ),
    # =========================================================================
    # COMPANY VALUATION EXTRAS
    # =========================================================================
    "stock_peers": FMPEndpoint(
        name="stock_peers",
        function="stock_peers",
        description="Similar companies trading on the same exchange, in the same sector, with similar market cap.",
        category="company",
        example_use_cases=[
            "Competitor identification",
            "Peer comparison analysis",
            "Industry benchmarking",
        ],
        returns="List of peer symbols.",
        example="stock_peers('NVDA')",),
    "financial_score": FMPEndpoint(
        name="financial_score",
        function="financial_score",
        description="Financial health score assessing company performance.",
        category="metrics",
        example_use_cases=[
            "Financial health assessment",
            "Quick screening metric",
        ],
        returns="Financial score data.",
        example="financial_score('TSLA')",),
    "owner_earnings": FMPEndpoint(
        name="owner_earnings",
        function="owner_earnings",
        description="Owner earnings calculation (Buffett's preferred metric) showing true cash available to shareholders.",
        category="metrics",
        example_use_cases=[
            "Value investing analysis",
            "True earnings power assessment",
        ],
        returns="Owner earnings data.",
        example="owner_earnings('BRK-B')",
    ),
    # =========================================================================
    # SEGMENTS
    # =========================================================================
    "sales_revenue_by_segments": FMPEndpoint(
        name="sales_revenue_by_segments",
        function="sales_revenue_by_segments",
        description="Segment revenue: revenue breakdown by business segments, product lines, services. Use for segment-level revenue analysis.",
        category="segments",
        example_use_cases=[
            "Segment revenue analysis",
            "Revenue by segment breakdown",
            "Product line revenue tracking",
        ],
        returns="Revenue by segment with date and segment-specific revenue values.",
        example="sales_revenue_by_segments('V', limit=5)",),
    "revenue_geographic_segmentation": FMPEndpoint(
        name="revenue_geographic_segmentation",
        function="revenue_geographic_segmentation",
        description="Geographic revenue: revenue by region/country. Shows global market presence and regional sales breakdown.",
        category="segments",
        example_use_cases=[
            "Geographic exposure analysis",
            "International expansion tracking",
            "Regional performance comparison",
        ],
        returns="Revenue by geography with date and region-specific revenue values.",
        example="revenue_geographic_segmentation('JNJ')",),
    # =========================================================================
    # EMPLOYEE & COMPENSATION
    # =========================================================================
    "employee_count": FMPEndpoint(
        name="employee_count",
        function="employee_count",
        description="Current number of employees at a company.",
        category="company",
        example_use_cases=[
            "Company size assessment",
            "Workforce analysis",
        ],
        returns="Employee count data.",
        example="employee_count('UNH')",),
    "historical_employee_count": FMPEndpoint(
        name="historical_employee_count",
        function="historical_employee_count",
        description="Historical employee count showing workforce growth or decline over time.",
        category="company",
        example_use_cases=[
            "Workforce growth analysis",
            "Operational scaling assessment",
        ],
        returns="Historical employee count data.",
        example="historical_employee_count('HD')",),
    "executive_compensation": FMPEndpoint(
        name="executive_compensation",
        function="executive_compensation",
        description="Executive compensation data from proxy filings.",
        category="company",
        example_use_cases=[
            "Executive pay analysis",
            "Compensation benchmarking",
            "Corporate governance assessment",
        ],
        returns="Executive compensation with name, title, salary, bonus, stockAwards, etc.",
        example="executive_compensation('AAPL')",),
    "compensation_benchmark": FMPEndpoint(
        name="compensation_benchmark",
        function="compensation_benchmark",
        description="Executive compensation benchmarks for a specific year.",
        category="company",
        example_use_cases=[
            "Industry compensation comparison",
            "Pay benchmarking",
        ],
        returns="Compensation benchmark data.",
        example="compensation_benchmark(2024)",),
    "company_notes": FMPEndpoint(
        name="company_notes",
        function="company_notes",
        description="Company notes and additional information.",
        category="company",
        example_use_cases=[
            "Additional company context",
            "Notes and observations",
        ],
        returns="Company notes data.",
        example="company_notes('MSFT')",),
    # =========================================================================
    # M&A
    # =========================================================================
    "search_mergers_acquisitions": FMPEndpoint(
        name="search_mergers_acquisitions",
        function="search_mergers_acquisitions",
        description="Search for M&A deals by company name.",
        category="corporate_actions",
        example_use_cases=[
            "M&A activity research",
            "Deal history lookup",
            "Strategic transaction analysis",
        ],
        returns="M&A deal data.",
        example="search_mergers_acquisitions()",),
    "mergers_acquisitions_rss_feed": FMPEndpoint(
        name="mergers_acquisitions_rss_feed",
        function="mergers_acquisitions_rss_feed",
        description="RSS feed of latest M&A news and announcements.",
        category="news",
        example_use_cases=[
            "Real-time M&A monitoring",
            "Deal flow tracking",
        ],
        returns="Latest M&A news.",
        example="mergers_acquisitions_rss_feed()",),
    # =========================================================================
    # NEWS
    # =========================================================================
    "stock_news": FMPEndpoint(
        name="stock_news",
        function="stock_news",
        description="Stock-specific news articles from various sources.",
        category="news",
        example_use_cases=[
            "Company-specific news tracking",
            "Event-driven analysis",
            "Sentiment research",
        ],
        returns="News articles with title, publishedDate, site, url, text snippet.",
        example="stock_news()",),
    "general_news": FMPEndpoint(
        name="general_news",
        function="general_news",
        description="General financial and market news from various sources.",
        category="news",
        example_use_cases=[
            "Market news overview",
            "General financial coverage",
        ],
        returns="General news articles.",
        example="general_news()",),
    "fmp_articles": FMPEndpoint(
        name="fmp_articles",
        function="fmp_articles",
        description="Articles published by Financial Modeling Prep.",
        category="news",
        example_use_cases=[
            "FMP analysis and research",
            "Educational content",
        ],
        returns="FMP articles with title, date, content.",
        example="fmp_articles()",),
    "press_releases": FMPEndpoint(
        name="press_releases",
        function="press_releases",
        description="Company press releases with official announcements.",
        category="news",
        example_use_cases=[
            "Official company announcements",
            "Corporate communications tracking",
            "Event detection",
        ],
        returns="Press releases with title, date, text.",
        example="press_releases()",),
    "upgrades_downgrades_rss_feed": FMPEndpoint(
        name="upgrades_downgrades_rss_feed",
        function="upgrades_downgrades_rss_feed",
        description="RSS feed of latest analyst upgrades and downgrades.",
        category="news",
        example_use_cases=[
            "Real-time rating changes",
            "Analyst action monitoring",
        ],
        returns="Latest upgrades/downgrades.",
        example="upgrades_downgrades_rss_feed()",),
    # =========================================================================
    # CALENDAR
    # =========================================================================
    "earning_calendar": FMPEndpoint(
        name="earning_calendar",
        function="earning_calendar",
        description="Earnings announcement calendar showing upcoming and past earnings dates.",
        category="calendar",
        example_use_cases=[
            "Earnings season tracking",
            "Upcoming earnings dates",
            "Event planning",
        ],
        returns="Earnings calendar with date, symbol, eps, epsEstimated, revenue, revenueEstimated.",
        example="earning_calendar()",),
    "historical_earning_calendar": FMPEndpoint(
        name="historical_earning_calendar",
        function="historical_earning_calendar",
        description="Historical and upcoming earnings dates for a specific company.",
        category="calendar",
        example_use_cases=[
            "Company-specific earnings history",
            "Earnings pattern analysis",
        ],
        returns="Historical earnings calendar data.",
        example="historical_earning_calendar('GOOGL', limit=5)",),
    "dividend_calendar": FMPEndpoint(
        name="dividend_calendar",
        function="dividend_calendar",
        description="Dividend payment calendar showing upcoming dividend dates.",
        category="calendar",
        example_use_cases=[
            "Dividend income planning",
            "Ex-dividend date tracking",
        ],
        returns="Dividend calendar with date, symbol, dividend, recordDate, paymentDate.",
        example="dividend_calendar()",
        notes="Maximum 3-month date range.",
    ),
    "ipo_calendar": FMPEndpoint(
        name="ipo_calendar",
        function="ipo_calendar",
        description="IPO calendar showing upcoming and recent initial public offerings.",
        category="calendar",
        example_use_cases=[
            "IPO tracking",
            "New listing research",
        ],
        returns="IPO calendar with date, symbol, exchange, name, ipoPrice, priceRange.",
        example="ipo_calendar()",),
    "stock_split_calendar": FMPEndpoint(
        name="stock_split_calendar",
        function="stock_split_calendar",
        description="Stock split calendar showing upcoming splits.",
        category="calendar",
        example_use_cases=[
            "Split event tracking",
            "Corporate action monitoring",
        ],
        returns="Stock split calendar with date, symbol, numerator, denominator.",
        example="stock_split_calendar()",),
    "economic_calendar": FMPEndpoint(
        name="economic_calendar",
        function="economic_calendar",
        description="Economic events calendar with GDP, CPI, employment data releases.",
        category="calendar",
        example_use_cases=[
            "Macro event tracking",
            "Economic data releases",
            "Market-moving event planning",
        ],
        returns="Economic calendar with date, event, country, actual, previous, estimate, impact.",
        example="economic_calendar()",),
    # =========================================================================
    # QUOTES & MARKET DATA
    # =========================================================================
    "quote": FMPEndpoint(
        name="quote",
        function="quote",
        description="Real-time full quote with bid/ask, volume, price, and daily statistics.",
        category="market",
        example_use_cases=[
            "Real-time price lookup",
            "Current market data",
            "Trading decisions",
        ],
        returns="Full quote with price, change, changesPercentage, dayLow, dayHigh, volume, avgVolume, etc.",
        example="quote('AMZN')",),
    "quote_short": FMPEndpoint(
        name="quote_short",
        function="quote_short",
        description="Simplified real-time quote with just price, change, and volume.",
        category="market",
        example_use_cases=[
            "Quick price check",
            "Simple market snapshot",
        ],
        returns="Short quote with symbol, price, volume.",
        example="quote_short('META')",),
    "historical_price_full": FMPEndpoint(
        name="historical_price_full",
        function="historical_price_full",
        description="Daily historical OHLCV price data for up to 5 years.",
        category="market",
        example_use_cases=[
            "Historical price analysis",
            "Trend analysis",
            "Backtesting",
            "Chart data",
        ],
        returns="Historical prices with date, open, high, low, close, volume, change, changePercent.",
        example="historical_price_full('NVDA')",),
    "historical_chart": FMPEndpoint(
        name="historical_chart",
        function="historical_chart",
        description="Intraday and daily historical price data with various timeframes.",
        category="market",
        example_use_cases=[
            "Intraday analysis",
            "Short-term trading",
            "Technical analysis",
        ],
        returns="Historical chart data with date, open, high, low, close, volume.",
        example="historical_chart('TSLA', '1day', from_date='2024-01-01', to_date='2024-03-31')",),
    "multiple_company_prices": FMPEndpoint(
        name="multiple_company_prices",
        function="multiple_company_prices",
        description="Real-time prices for multiple companies in a single request.",
        category="market",
        example_use_cases=[
            "Portfolio monitoring",
            "Batch price lookup",
            "Watchlist updates",
        ],
        returns="Prices for multiple symbols.",
        example="multiple_company_prices('JPM')",),
    # =========================================================================
    # MARKET MOVERS
    # =========================================================================
    "actives": FMPEndpoint(
        name="actives",
        function="actives",
        description="Most actively traded stocks by volume.",
        category="market",
        example_use_cases=[
            "Market activity monitoring",
            "High volume stock discovery",
            "Liquidity analysis",
        ],
        returns="Active stocks with symbol, name, change, price, changesPercentage, volume.",
        example="actives()",),
    "gainers": FMPEndpoint(
        name="gainers",
        function="gainers",
        description="Stocks with the biggest gains today.",
        category="market",
        example_use_cases=[
            "Daily winners tracking",
            "Momentum stock discovery",
        ],
        returns="Top gaining stocks with symbol, name, change, price, changesPercentage.",
        example="gainers()",),
    "losers": FMPEndpoint(
        name="losers",
        function="losers",
        description="Stocks with the biggest losses today.",
        category="market",
        example_use_cases=[
            "Daily losers tracking",
            "Sell-off monitoring",
            "Potential recovery plays",
        ],
        returns="Top losing stocks with symbol, name, change, price, changesPercentage.",
        example="losers()",),
    "sectors_performance": FMPEndpoint(
        name="sectors_performance",
        function="sectors_performance",
        description="Current performance by sector.",
        category="market",
        example_use_cases=[
            "Sector rotation analysis",
            "Market breadth assessment",
        ],
        returns="Sector performance with sector name and changesPercentage.",
        example="sectors_performance()",),
    "historical_sectors_performance": FMPEndpoint(
        name="historical_sectors_performance",
        function="historical_sectors_performance",
        description="Historical sector performance over time.",
        category="market",
        example_use_cases=[
            "Sector trend analysis",
            "Historical rotation patterns",
        ],
        returns="Historical sector performance data.",
        example="historical_sectors_performance(from_date='2024-01-01', to_date='2024-03-31')",),
    "market_hours": FMPEndpoint(
        name="market_hours",
        function="market_hours",
        description="Market hours information for exchanges.",
        category="market",
        example_use_cases=[
            "Trading schedule lookup",
            "Market timing",
        ],
        returns="Market hours data.",
        example="market_hours()",),
    "is_market_open": FMPEndpoint(
        name="is_market_open",
        function="is_market_open",
        description="Check if a market/exchange is currently open.",
        category="market",
        example_use_cases=[
            "Market status check",
            "Trading availability",
        ],
        returns="Market open/closed status.",
        example="is_market_open()",),
    # =========================================================================
    # INDEXES
    # =========================================================================
    "indexes": FMPEndpoint(
        name="indexes",
        function="indexes",
        description="Major market indexes (S&P 500, Dow Jones, NASDAQ, etc.).",
        category="indexes",
        example_use_cases=[
            "Market benchmark tracking",
            "Index performance comparison",
        ],
        returns="Index data with symbol, name, price, change, changesPercentage.",
        example="indexes()",
    ),
    "sp500_constituent": FMPEndpoint(
        name="sp500_constituent",
        function="sp500_constituent",
        description="Current S&P 500 constituents list.",
        category="indexes",
        example_use_cases=[
            "S&P 500 stock list",
            "Index composition analysis",
        ],
        returns="S&P 500 constituents with symbol, name, sector, subSector.",
        example="sp500_constituent()",),
    "historical_sp500_constituent": FMPEndpoint(
        name="historical_sp500_constituent",
        function="historical_sp500_constituent",
        description="Historical S&P 500 additions and removals.",
        category="indexes",
        example_use_cases=[
            "Index changes tracking",
            "Historical composition",
        ],
        returns="Historical S&P 500 changes.",
        example="historical_sp500_constituent()",),
    "nasdaq_constituent": FMPEndpoint(
        name="nasdaq_constituent",
        function="nasdaq_constituent",
        description="Current NASDAQ 100 constituents list.",
        category="indexes",
        example_use_cases=[
            "NASDAQ 100 stock list",
            "Tech index composition",
        ],
        returns="NASDAQ constituents with symbol, name, sector.",
        example="nasdaq_constituent()",),
    "historical_nasdaq_constituent": FMPEndpoint(
        name="historical_nasdaq_constituent",
        function="historical_nasdaq_constituent",
        description="Historical NASDAQ additions and removals.",
        category="indexes",
        example_use_cases=[
            "NASDAQ changes tracking",
        ],
        returns="Historical NASDAQ changes.",
        example="historical_nasdaq_constituent()",),
    "dowjones_constituent": FMPEndpoint(
        name="dowjones_constituent",
        function="dowjones_constituent",
        description="Current Dow Jones Industrial Average constituents.",
        category="indexes",
        example_use_cases=[
            "DJIA stock list",
            "Blue chip analysis",
        ],
        returns="Dow Jones constituents.",
        example="dowjones_constituent()",),
    "historical_dowjones_constituent": FMPEndpoint(
        name="historical_dowjones_constituent",
        function="historical_dowjones_constituent",
        description="Historical Dow Jones additions and removals.",
        category="indexes",
        example_use_cases=[
            "DJIA changes tracking",
        ],
        returns="Historical Dow Jones changes.",
        example="historical_dowjones_constituent()",),
    # =========================================================================
    # INSTITUTIONAL & OWNERSHIP
    # =========================================================================
    "institutional_holders": FMPEndpoint(
        name="institutional_holders",
        function="institutional_holders",
        description="Major institutional investors holding a stock.",
        category="ownership",
        example_use_cases=[
            "Institutional ownership analysis",
            "Smart money tracking",
            "Ownership concentration",
        ],
        returns="Institutional holders with holder name, shares, dateReported, change, changePercentage.",
        example="institutional_holders('V')",),
    "mutual_fund_holders": FMPEndpoint(
        name="mutual_fund_holders",
        function="mutual_fund_holders",
        description="Mutual funds holding a stock.",
        category="ownership",
        example_use_cases=[
            "Mutual fund ownership tracking",
            "Fund flow analysis",
        ],
        returns="Mutual fund holders data.",
        example="mutual_fund_holders('JNJ')",),
    "etf_holders": FMPEndpoint(
        name="etf_holders",
        function="etf_holders",
        description="ETFs holding a specific stock.",
        category="ownership",
        example_use_cases=[
            "ETF exposure analysis",
            "Passive ownership tracking",
        ],
        returns="ETF holders data.",
        example="etf_holders('UNH')",),
    "form_13f": FMPEndpoint(
        name="form_13f",
        function="form_13f",
        description="Form 13F filings showing institutional holdings over $100M AUM.",
        category="ownership",
        example_use_cases=[
            "Institutional portfolio analysis",
            "Hedge fund tracking",
        ],
        returns="13F holdings with cusip, symbol, shares, value.",
        example="form_13f('0000320193')",),
    # =========================================================================
    # ETF DATA
    # =========================================================================
    "etf_sector_weightings": FMPEndpoint(
        name="etf_sector_weightings",
        function="etf_sector_weightings",
        description="Sector weightings for an ETF.",
        category="etf",
        example_use_cases=[
            "ETF sector exposure analysis",
            "Portfolio diversification assessment",
        ],
        returns="Sector weightings with sector and weightPercentage.",
        example="etf_sector_weightings('SPY')",),
    "etf_country_weightings": FMPEndpoint(
        name="etf_country_weightings",
        function="etf_country_weightings",
        description="Country/geographic weightings for an ETF.",
        category="etf",
        example_use_cases=[
            "Geographic exposure analysis",
            "International diversification",
        ],
        returns="Country weightings data.",
        example="etf_country_weightings('VEU')",),
    # =========================================================================
    # INSIDER TRADING
    # =========================================================================
    "insider_trading": FMPEndpoint(
        name="insider_trading",
        function="insider_trading",
        description="Insider trading transactions (Form 4 filings).",
        category="ownership",
        example_use_cases=[
            "Insider sentiment analysis",
            "Executive trading patterns",
            "Insider buying/selling signals",
        ],
        returns="Insider trades with reportingName, transactionType, securitiesTransacted, price.",
        notes="Provide only ONE of: symbol, reporting_cik, or company_cik.",
        example="insider_trading(symbol='AAPL', limit=20)",
    ),
    "insider_trading_rss_feed": FMPEndpoint(
        name="insider_trading_rss_feed",
        function="insider_trading_rss_feed",
        description="Real-time RSS feed of insider trading activity.",
        category="ownership",
        example_use_cases=[
            "Real-time insider activity monitoring",
            "Breaking insider trades",
        ],
        returns="Latest insider trades.",
        example="insider_trading_rss_feed()",),
    # =========================================================================
    # SENATE TRADING
    # =========================================================================
    "senate_trading_rss": FMPEndpoint(
        name="senate_trading_rss",
        function="senate_trading_rss",
        description="RSS feed of Senate member stock trades.",
        category="ownership",
        example_use_cases=[
            "Congressional trading tracking",
            "Political insider trading",
        ],
        returns="Senate trading data.",
        example="senate_trading_rss()",),
    "senate_trading_symbol": FMPEndpoint(
        name="senate_trading_symbol",
        function="senate_trading_symbol",
        description="Senate trades filtered by stock symbol.",
        category="ownership",
        example_use_cases=[
            "Congressional trades in specific stocks",
        ],
        returns="Senate trades for the symbol.",
        example="senate_trading_symbol('MSFT')",),
    "senate_disclosure_rss": FMPEndpoint(
        name="senate_disclosure_rss",
        function="senate_disclosure_rss",
        description="RSS feed of Senate financial disclosures.",
        category="ownership",
        example_use_cases=[
            "Senate disclosure monitoring",
        ],
        returns="Senate disclosure data.",
        example="senate_disclosure_rss()",),
    "senate_disclosure_symbol": FMPEndpoint(
        name="senate_disclosure_symbol",
        function="senate_disclosure_symbol",
        description="Senate disclosures filtered by stock symbol.",
        category="ownership",
        example_use_cases=[
            "Senate holdings in specific stocks",
        ],
        returns="Senate disclosures for the symbol.",
        example="senate_disclosure_symbol('GOOGL')",),
    # =========================================================================
    # DIVIDENDS & SPLITS
    # =========================================================================
    "historical_stock_dividend": FMPEndpoint(
        name="historical_stock_dividend",
        function="historical_stock_dividend",
        description="Historical dividend payments for a company.",
        category="dividends",
        example_use_cases=[
            "Dividend history analysis",
            "Dividend growth tracking",
            "Income investing research",
        ],
        returns="Historical dividends with date, label, adjDividend, dividend.",
        example="historical_stock_dividend('AMZN')",),
    "historical_stock_split": FMPEndpoint(
        name="historical_stock_split",
        function="historical_stock_split",
        description="Historical stock splits for a company.",
        category="corporate_actions",
        example_use_cases=[
            "Split history analysis",
            "Price adjustment research",
        ],
        returns="Historical splits with date, label, numerator, denominator.",
        example="historical_stock_split('META')",),
    # =========================================================================
    # SHARES FLOAT
    # =========================================================================
    "shares_float": FMPEndpoint(
        name="shares_float",
        function="shares_float",
        description="Shares float - publicly traded shares available for trading.",
        category="market",
        example_use_cases=[
            "Float analysis",
            "Short squeeze potential",
            "Liquidity assessment",
        ],
        returns="Shares float with symbol, date, freeFloat, floatShares, outstandingShares.",
        example="shares_float('NVDA')",),
    "historical_share_float": FMPEndpoint(
        name="historical_share_float",
        function="historical_share_float",
        description="Historical shares float data over time.",
        category="market",
        example_use_cases=[
            "Float changes over time",
            "Dilution tracking",
        ],
        returns="Historical float data.",
        example="historical_share_float('TSLA')",),
    # =========================================================================
    # SOCIAL SENTIMENT
    # =========================================================================
    "historical_social_sentiment": FMPEndpoint(
        name="historical_social_sentiment",
        function="historical_social_sentiment",
        description="Historical social media sentiment for a stock.",
        category="sentiment",
        example_use_cases=[
            "Social sentiment trends",
            "Retail investor sentiment",
        ],
        returns="Social sentiment data with date and sentiment metrics.",
        example="historical_social_sentiment('JPM')",),
    "trending_social_sentiment": FMPEndpoint(
        name="trending_social_sentiment",
        function="trending_social_sentiment",
        description="Currently trending stocks by social sentiment.",
        category="sentiment",
        example_use_cases=[
            "Trending stock discovery",
            "Social momentum tracking",
        ],
        returns="Trending stocks by sentiment.",
        example="trending_social_sentiment()",),
    "social_sentiment_changes": FMPEndpoint(
        name="social_sentiment_changes",
        function="social_sentiment_changes",
        description="Changes in social sentiment over time.",
        category="sentiment",
        example_use_cases=[
            "Sentiment shift detection",
            "Momentum changes",
        ],
        returns="Sentiment change data.",
        example="social_sentiment_changes()",),
    # =========================================================================
    # TECHNICAL INDICATORS
    # =========================================================================
    "technical_indicators": FMPEndpoint(
        name="technical_indicators",
        function="technical_indicators",
        description="Technical indicators (SMA, EMA, WMA, DEMA, TEMA, RSI, ADX, Williams %R, Standard Deviation).",
        category="technical",
        example_use_cases=[
            "Technical analysis",
            "Trading signals",
            "Trend identification",
        ],
        returns="Technical indicator values with date and indicator value.",
        example="technical_indicators('AAPL', period=14, statistics_type='rsi')",
    ),
    # =========================================================================
    # ECONOMICS
    # =========================================================================
    "treasury_rates": FMPEndpoint(
        name="treasury_rates",
        function="treasury_rates",
        description="US Treasury rates across all maturities.",
        category="economics",
        example_use_cases=[
            "Interest rate analysis",
            "Yield curve research",
            "Risk-free rate lookup",
        ],
        returns="Treasury rates with date and rates for various maturities.",
        example="treasury_rates()",),
    "economic_indicators": FMPEndpoint(
        name="economic_indicators",
        function="economic_indicators",
        description="Economic indicators (GDP, CPI, unemployment, etc.).",
        category="economics",
        example_use_cases=[
            "Macro economic analysis",
            "GDP tracking",
            "Inflation monitoring",
        ],
        returns="Economic indicator values with date and value.",
        example="economic_indicators('GDP')",
    ),
    "market_risk_premium": FMPEndpoint(
        name="market_risk_premium",
        function="market_risk_premium",
        description="Market risk premium by country for CAPM calculations.",
        category="economics",
        example_use_cases=[
            "CAPM calculations",
            "Cost of equity estimation",
        ],
        returns="Market risk premium data.",
        example="market_risk_premium()",),
    # =========================================================================
    # FOREX
    # =========================================================================
    "forex": FMPEndpoint(
        name="forex",
        function="forex",
        description="Real-time forex prices for all currency pairs.",
        category="forex",
        example_use_cases=[
            "Currency rate lookup",
            "FX market overview",
        ],
        returns="Forex prices with ticker, bid, ask, changes.",
        example="forex()",),
    "forex_list": FMPEndpoint(
        name="forex_list",
        function="forex_list",
        description="Full quote list for all forex currency pairs.",
        category="forex",
        example_use_cases=[
            "Complete FX market data",
        ],
        returns="Full forex quotes.",
        example="forex_list()",),
    "forex_quote": FMPEndpoint(
        name="forex_quote",
        function="forex_quote",
        description="Full quote for a specific forex pair.",
        category="forex",
        example_use_cases=[
            "Specific currency pair quote",
        ],
        returns="Forex quote data.",
        example="forex_quote('EURUSD')",),
    "forex_historical": FMPEndpoint(
        name="forex_historical",
        function="forex_historical",
        description="Historical forex data for a currency pair.",
        category="forex",
        example_use_cases=[
            "Historical FX analysis",
            "Currency trend research",
        ],
        returns="Historical forex prices.",
        example="forex_historical('EURUSD', from_date='2024-01-01', to_date='2024-03-31')",),
    # =========================================================================
    # CRYPTO
    # =========================================================================
    "cryptocurrency_quote": FMPEndpoint(
        name="cryptocurrency_quote",
        function="cryptocurrency_quote",
        description="Real-time cryptocurrency quote.",
        category="crypto",
        example_use_cases=[
            "Crypto price lookup",
            "Bitcoin/Ethereum quotes",
        ],
        returns="Cryptocurrency quote data.",
        example="cryptocurrency_quote('BTCUSD')",),
    "cryptocurrencies_list": FMPEndpoint(
        name="cryptocurrencies_list",
        function="cryptocurrencies_list",
        description="Full quotes for all cryptocurrencies.",
        category="crypto",
        example_use_cases=[
            "Full crypto market overview",
        ],
        returns="All cryptocurrency quotes.",
        example="cryptocurrencies_list()",),
    # =========================================================================
    # COMMODITIES
    # =========================================================================
    "commodity_price": FMPEndpoint(
        name="commodity_price",
        function="commodity_price",
        description="Historical commodity price data.",
        category="commodities",
        example_use_cases=[
            "Commodity price analysis",
            "Gold/oil/silver prices",
        ],
        returns="Commodity price data.",
        example="commodity_price('ZGUSD', from_date='2024-01-01', to_date='2024-03-31')",),
    "commodities_list": FMPEndpoint(
        name="commodities_list",
        function="commodities_list",
        description="Full quotes for all commodities.",
        category="commodities",
        example_use_cases=[
            "Commodities market overview",
        ],
        returns="All commodity quotes.",
        example="commodities_list()",),
    # =========================================================================
    # STOCK SCREENER
    # =========================================================================
    "stock_screener": FMPEndpoint(
        name="stock_screener",
        function="stock_screener",
        description="Screen stocks based on financial criteria (market cap, beta, dividend, etc.).",
        category="screener",
        example_use_cases=[
            "Investment screening",
            "Stock discovery by criteria",
            "Sector-specific searches",
        ],
        returns="Screened stocks with symbol, companyName, marketCap, sector, etc.",
        example="stock_screener(market_cap_more_than=1e9, sector='Technology', limit=10)",
    ),
    # =========================================================================
    # SEARCH
    # =========================================================================
    "search": FMPEndpoint(
        name="search",
        function="search",
        description="Search for stocks, ETFs, and financial instruments by name or ticker.",
        category="search",
        example_use_cases=[
            "Find stock by name",
            "Ticker lookup",
        ],
        returns="Search results with symbol, name, currency, stockExchange.",
        example="search()",),
    "search_ticker": FMPEndpoint(
        name="search_ticker",
        function="search_ticker",
        description="Search specifically for ticker symbols.",
        category="search",
        example_use_cases=[
            "Ticker symbol lookup",
        ],
        returns="Ticker search results.",
        example="search_ticker()",),
    # =========================================================================
    # REFERENCE DATA
    # =========================================================================
    "symbols_list": FMPEndpoint(
        name="symbols_list",
        function="symbols_list",
        description="Full list of all available stock symbols.",
        category="reference",
        example_use_cases=[
            "Complete stock universe",
        ],
        returns="All stock symbols.",
        example="symbols_list()",),
    "etf_list": FMPEndpoint(
        name="etf_list",
        function="etf_list",
        description="Full list of all available ETFs.",
        category="reference",
        example_use_cases=[
            "ETF universe",
        ],
        returns="All ETF symbols.",
        example="etf_list()",),
    "available_traded_list": FMPEndpoint(
        name="available_traded_list",
        function="available_traded_list",
        description="List of all tradable symbols.",
        category="reference",
        example_use_cases=[
            "Tradable securities list",
        ],
        returns="All tradable symbols.",
        example="available_traded_list()",),
    "available_forex": FMPEndpoint(
        name="available_forex",
        function="available_forex",
        description="List of available forex currency pairs.",
        category="reference",
        example_use_cases=[
            "FX pair availability",
        ],
        returns="Available forex pairs.",
        example="available_forex()",),
    "available_cryptocurrencies": FMPEndpoint(
        name="available_cryptocurrencies",
        function="available_cryptocurrencies",
        description="List of available cryptocurrencies.",
        category="reference",
        example_use_cases=[
            "Crypto availability",
        ],
        returns="Available cryptocurrencies.",
        example="available_cryptocurrencies()",),
    "available_commodities": FMPEndpoint(
        name="available_commodities",
        function="available_commodities",
        description="List of available commodities.",
        category="reference",
        example_use_cases=[
            "Commodity availability",
        ],
        returns="Available commodities.",
        example="available_commodities()",),
    "available_etfs": FMPEndpoint(
        name="available_etfs",
        function="available_etfs",
        description="List of available ETFs.",
        category="reference",
        example_use_cases=[
            "ETF availability",
        ],
        returns="Available ETFs.",
        example="available_etfs()",),
    "available_indexes": FMPEndpoint(
        name="available_indexes",
        function="available_indexes",
        description="List of available market indexes.",
        category="reference",
        example_use_cases=[
            "Index availability",
        ],
        returns="Available indexes.",
        example="available_indexes()",),
    "available_sectors": FMPEndpoint(
        name="available_sectors",
        function="available_sectors",
        description="List of available market sectors.",
        category="reference",
        example_use_cases=[
            "Sector list for screening",
        ],
        returns="Available sectors.",
        example="available_sectors()",),
    "available_industries": FMPEndpoint(
        name="available_industries",
        function="available_industries",
        description="List of available industries.",
        category="reference",
        example_use_cases=[
            "Industry list for screening",
        ],
        returns="Available industries.",
        example="available_industries()",),
    "available_exchanges": FMPEndpoint(
        name="available_exchanges",
        function="available_exchanges",
        description="List of available stock exchanges.",
        category="reference",
        example_use_cases=[
            "Exchange list",
        ],
        returns="Available exchanges.",
        example="available_exchanges()",),
    "all_countries": FMPEndpoint(
        name="all_countries",
        function="all_countries",
        description="List of all countries with market data.",
        category="reference",
        example_use_cases=[
            "Country availability",
        ],
        returns="All countries.",
        example="all_countries()",),
    "delisted_companies": FMPEndpoint(
        name="delisted_companies",
        function="delisted_companies",
        description="List of delisted companies.",
        category="reference",
        example_use_cases=[
            "Historical delisting tracking",
        ],
        returns="Delisted companies.",
        example="delisted_companies()",),
    "financial_statement_symbol_lists": FMPEndpoint(
        name="financial_statement_symbol_lists",
        function="financial_statement_symbol_lists",
        description="Symbols with available financial statements.",
        category="reference",
        example_use_cases=[
            "Find companies with financials",
        ],
        returns="Symbols with financial statements.",
        example="financial_statement_symbol_lists()",),
    # =========================================================================
    # CIK MAPPING
    # =========================================================================
    "cik": FMPEndpoint(
        name="cik",
        function="cik",
        description="Get company name by CIK.",
        category="reference",
        example_use_cases=[
            "CIK to company lookup",
        ],
        returns="Company name for CIK.",
        example="cik('0000320193')",),
    "cik_list": FMPEndpoint(
        name="cik_list",
        function="cik_list",
        description="Full list of CIK numbers.",
        category="reference",
        example_use_cases=[
            "CIK database",
        ],
        returns="CIK list.",
        example="cik_list()",),
    "cik_search": FMPEndpoint(
        name="cik_search",
        function="cik_search",
        description="Search for CIK by company name.",
        category="reference",
        example_use_cases=[
            "Find CIK by name",
        ],
        returns="CIK search results.",
        example="cik_search()",),
    "cusip": FMPEndpoint(
        name="cusip",
        function="cusip",
        description="CUSIP mapper for CIK.",
        category="reference",
        example_use_cases=[
            "CUSIP lookup",
        ],
        returns="CUSIP data.",
        example="cusip('0000320193')",),
    "mapper_cik_name": FMPEndpoint(
        name="mapper_cik_name",
        function="mapper_cik_name",
        description="Map CIK to insider names.",
        category="reference",
        example_use_cases=[
            "Find CIK for insider",
        ],
        returns="CIK mapping.",
        example="mapper_cik_name()",),
    "mapper_cik_company": FMPEndpoint(
        name="mapper_cik_company",
        function="mapper_cik_company",
        description="Map ticker to company CIK.",
        category="reference",
        example_use_cases=[
            "Find CIK for ticker",
        ],
        returns="Company CIK.",
        example="mapper_cik_company()",),
    # =========================================================================
    # ALTERNATIVE DATA
    # =========================================================================
    "commitment_of_traders_report_list": FMPEndpoint(
        name="commitment_of_traders_report_list",
        function="commitment_of_traders_report_list",
        description="List of available COT report symbols.",
        category="alternative",
        example_use_cases=[
            "COT report availability",
        ],
        returns="COT symbols.",
        example="commitment_of_traders_report_list()",),
    "commitment_of_traders_report": FMPEndpoint(
        name="commitment_of_traders_report",
        function="commitment_of_traders_report",
        description="CFTC Commitment of Traders report data.",
        category="alternative",
        example_use_cases=[
            "Futures positioning analysis",
            "Speculator vs hedger activity",
        ],
        returns="COT report data.",
        example="commitment_of_traders_report('MSFT')",),
    "commitment_of_traders_report_analysis": FMPEndpoint(
        name="commitment_of_traders_report_analysis",
        function="commitment_of_traders_report_analysis",
        description="Analysis of COT report data.",
        category="alternative",
        example_use_cases=[
            "COT trend analysis",
        ],
        returns="COT analysis data.",
        example="commitment_of_traders_report_analysis('GOOGL', from_date='2024-01-01', to_date='2024-03-31')",),
    "fail_to_deliver": FMPEndpoint(
        name="fail_to_deliver",
        function="fail_to_deliver",
        description="Fail-to-deliver data showing settlement failures.",
        category="alternative",
        example_use_cases=[
            "Short selling analysis",
            "Settlement issues tracking",
        ],
        returns="FTD data.",
        example="fail_to_deliver('AMZN')",),
    "sector_pe_ratio": FMPEndpoint(
        name="sector_pe_ratio",
        function="sector_pe_ratio",
        description="Sector-level P/E ratios.",
        category="valuation",
        example_use_cases=[
            "Sector valuation comparison",
        ],
        returns="Sector PE ratios.",
        example="sector_pe_ratio('2024-01-01')",),
    "industry_pe_ratio": FMPEndpoint(
        name="industry_pe_ratio",
        function="industry_pe_ratio",
        description="Industry-level P/E ratios.",
        category="valuation",
        example_use_cases=[
            "Industry valuation comparison",
        ],
        returns="Industry PE ratios.",
        example="industry_pe_ratio('2024-01-01')",),
    "batch_eod_prices": FMPEndpoint(
        name="batch_eod_prices",
        function="batch_eod_prices",
        description="End of day prices for all stocks on a specific date.",
        category="market",
        example_use_cases=[
            "Historical EOD snapshot",
            "Bulk price data",
        ],
        returns="All EOD prices for the date.",
        example="batch_eod_prices('2024-01-01')",),
    "sec_rss_feeds": FMPEndpoint(
        name="sec_rss_feeds",
        function="sec_rss_feeds",
        description="SEC RSS feed of latest filings.",
        category="sec",
        example_use_cases=[
            "Latest SEC filings",
            "Real-time filing monitoring",
        ],
        returns="Latest SEC filings.",
        example="sec_rss_feeds()",),
    "exchange_realtime": FMPEndpoint(
        name="exchange_realtime",
        function="exchange_realtime",
        description="Real-time quotes for all stocks on an exchange.",
        category="market",
        example_use_cases=[
            "Exchange-wide real-time data",
        ],
        returns="Real-time quotes for exchange.",
        example="exchange_realtime('NYSE')",),
    # =========================================================================
    # CROWDFUNDING
    # =========================================================================
    "crowdfunding_rss_feed": FMPEndpoint(
        name="crowdfunding_rss_feed",
        function="crowdfunding_rss_feed",
        description="RSS feed of crowdfunding campaigns.",
        category="alternative",
        example_use_cases=[
            "Crowdfunding monitoring",
        ],
        returns="Crowdfunding campaigns.",
        example="crowdfunding_rss_feed()",),
    "crowdfunding_search": FMPEndpoint(
        name="crowdfunding_search",
        function="crowdfunding_search",
        description="Search crowdfunding campaigns by name.",
        category="alternative",
        example_use_cases=[
            "Find specific crowdfunding campaigns",
        ],
        returns="Matching crowdfunding campaigns.",
        example="crowdfunding_search()",),
    "crowdfunding_by_cik": FMPEndpoint(
        name="crowdfunding_by_cik",
        function="crowdfunding_by_cik",
        description="Crowdfunding campaigns by company CIK.",
        category="alternative",
        example_use_cases=[
            "Company-specific crowdfunding",
        ],
        returns="Crowdfunding campaigns for CIK.",
        example="crowdfunding_by_cik('0000320193')",),
    # Additional reference data
    "available_mutual_funds": FMPEndpoint(
        name="available_mutual_funds",
        function="available_mutual_funds",
        description="List of available mutual funds.",
        category="reference",
        example_use_cases=["Mutual fund availability"],
        returns="Available mutual funds.",
        example="available_mutual_funds()",),
    "available_tsx": FMPEndpoint(
        name="available_tsx",
        function="available_tsx",
        description="List of available TSX symbols.",
        category="reference",
        example_use_cases=["TSX availability"],
        returns="Available TSX symbols.",
        example="available_tsx()",),
    "available_euronext": FMPEndpoint(
        name="available_euronext",
        function="available_euronext",
        description="List of available Euronext stocks.",
        category="reference",
        example_use_cases=["Euronext availability"],
        returns="Available Euronext stocks.",
        example="available_euronext()",),
    "mutual_fund_list": FMPEndpoint(
        name="mutual_fund_list",
        function="mutual_fund_list",
        description="Full quotes for all mutual funds.",
        category="market",
        example_use_cases=["Mutual fund quotes"],
        returns="All mutual fund quotes.",
        example="mutual_fund_list()",),
    "tsx_list": FMPEndpoint(
        name="tsx_list",
        function="tsx_list",
        description="TSX stocks data.",
        category="market",
        example_use_cases=["TSX market data"],
        returns="TSX stocks data.",
        example="tsx_list()",),
    # =========================================================================
    # NEW STABLE API ENDPOINTS
    # =========================================================================
    "income_statement_ttm": FMPEndpoint(
        name="income_statement_ttm",
        function="income_statement_ttm",
        description="Trailing twelve months (TTM) income statement data. Aggregates the most recent 12 months of data regardless of fiscal year.",
        category="financials",
        example_use_cases=[
            "Current profitability analysis without waiting for quarterly reports",
            "Rolling 12-month revenue trend analysis",
            "Most recent financial performance snapshot",
        ],
        returns="TTM income statement with revenue, expenses, netIncome, etc.",
        example="income_statement_ttm('NVDA')",
    ),
    "balance_sheet_statement_ttm": FMPEndpoint(
        name="balance_sheet_statement_ttm",
        function="balance_sheet_statement_ttm",
        description="Most recent balance sheet snapshot showing current financial position.",
        category="financials",
        example_use_cases=[
            "Current asset and liability analysis",
            "Latest equity position assessment",
            "Real-time financial health check",
        ],
        returns="Current balance sheet with totalAssets, totalLiabilities, totalEquity, etc.",
        example="balance_sheet_statement_ttm('NVDA')",),
    "cash_flow_statement_ttm": FMPEndpoint(
        name="cash_flow_statement_ttm",
        function="cash_flow_statement_ttm",
        description="Trailing twelve months (TTM) cash flow statement. Shows rolling 12-month cash generation and usage.",
        category="financials",
        example_use_cases=[
            "Current free cash flow analysis",
            "Rolling cash generation trends",
            "Capital expenditure assessment",
        ],
        returns="TTM cash flow statement with operatingCashFlow, investingCashFlow, financingCashFlow, etc.",
        example="cash_flow_statement_ttm('NVDA')",
    ),
    "latest_financial_statements": FMPEndpoint(
        name="latest_financial_statements",
        function="latest_financial_statements",
        description="Paginated list of the most recently filed financial statements across all companies. Useful for monitoring new filings.",
        category="financials",
        example_use_cases=[
            "Monitor new SEC filings across the market",
            "Track recently updated financials",
            "Find companies with fresh financial data",
        ],
        returns="List of recently filed financial statements with company info and filing dates.",
        example="latest_financial_statements()",),
    "earning_call_transcript_latest": FMPEndpoint(
        name="earning_call_transcript_latest",
        function="earning_call_transcript_latest",
        description="Most recent earnings call transcript for a company. Quick access without specifying year/quarter.",
        category="earnings",
        example_use_cases=[
            "Quick access to latest management commentary",
            "Recent earnings call analysis",
            "Current quarter executive discussions",
        ],
        returns="Latest earnings call transcript with content and metadata.",
        example="earning_call_transcript_latest('JPM')",
        notes="Transcripts can be very long (10k+ words). Consider token limits when processing.",
    ),
    "ratings_snapshot": FMPEndpoint(
        name="ratings_snapshot",
        function="ratings_snapshot",
        description="Snapshot of analyst ratings showing buy/hold/sell recommendations distribution.",
        category="analysts",
        example_use_cases=[
            "Quick analyst sentiment overview",
            "Buy/sell recommendation counts",
            "Market consensus assessment",
        ],
        returns="Rating distribution with strong buy, buy, hold, sell, strong sell counts.",
        example="ratings_snapshot('V')",),
    "grades_consensus": FMPEndpoint(
        name="grades_consensus",
        function="grades_consensus",
        description="Consensus grade from analyst ratings aggregated into a single recommendation.",
        category="analysts",
        example_use_cases=[
            "Overall analyst consensus rating",
            "Aggregated market opinion",
            "Quick recommendation lookup",
        ],
        returns="Consensus grade with overall recommendation and scores.",
        example="grades_consensus('JNJ')",),
    "aftermarket_trade": FMPEndpoint(
        name="aftermarket_trade",
        function="aftermarket_trade",
        description="After-hours trading data including price, volume, and timestamp. Shows extended hours activity.",
        category="market",
        example_use_cases=[
            "Monitor after-hours price movements",
            "Track extended hours volume",
            "Assess overnight market reactions",
        ],
        returns="After-hours trade data with price, volume, timestamp.",
        example="aftermarket_trade('UNH')",),
    "aftermarket_quote": FMPEndpoint(
        name="aftermarket_quote",
        function="aftermarket_quote",
        description="After-hours quote data including bid/ask prices. Shows extended hours pricing.",
        category="market",
        example_use_cases=[
            "After-hours bid/ask spread analysis",
            "Extended hours market sentiment",
            "Pre-market pricing assessment",
        ],
        returns="After-hours quote with bid, ask, and related pricing data.",
        example="aftermarket_quote('HD')",),
    "industry_performance_snapshot": FMPEndpoint(
        name="industry_performance_snapshot",
        function="industry_performance_snapshot",
        description="Current performance metrics for all market industries. Shows which industries are outperforming or underperforming.",
        category="market",
        example_use_cases=[
            "Industry sector comparison",
            "Identify outperforming sectors",
            "Market rotation analysis",
        ],
        returns="Performance data for each industry with change percentages.",
        example="industry_performance_snapshot()",),
    "holidays_by_exchange": FMPEndpoint(
        name="holidays_by_exchange",
        function="holidays_by_exchange",
        description="Market holidays for a specific exchange. Shows when markets are closed.",
        category="market",
        example_use_cases=[
            "Trading calendar planning",
            "Market closure schedule",
            "Holiday schedule lookup",
        ],
        returns="List of holiday dates with names for the exchange.",
        example="holidays_by_exchange('NYSE')",),
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
    """
    Get all endpoints in a specific category.

    Retrieves all FMP endpoint definitions that belong to the specified category,
    useful for filtering endpoints by functional area.

    :param category: Category name (e.g., 'financials', 'sec', 'news', 'market').
    :return: List of FMPEndpoint objects matching the category.
    :example: get_endpoints_by_category('financials')
    """
    return [ep for ep in FMP_REGISTRY.values() if ep.category == category]


def get_all_categories() -> List[str]:
    """
    Get all available endpoint categories.

    Returns the list of category names used to organize FMP endpoints.
    Categories include: financials, earnings, sec, company, metrics, etc.

    :return: List of category name strings.
    :example: get_all_categories()
    """
    return list(CATEGORIES.keys())


def _format_parameters_from_function(func_name: str) -> str:
    """
    Extract and format parameters from an fmpsdk function signature.

    GEN-93: Runtime parameter extraction for LLM context.
    This ensures parameter info stays in sync with actual function signatures.

    :param func_name: Name of the fmpsdk function.
    :return: Formatted parameter string, or empty string if function not found.
    """
    import inspect
    try:
        import fmpsdk
        func = getattr(fmpsdk, func_name, None)
        if func is None or not callable(func):
            return ""

        sig = inspect.signature(func)
        parts = []

        for param_name, param in sig.parameters.items():
            # Skip internal params not useful for LLM
            if param_name in ('download', 'filename'):
                continue

            if param.default == inspect.Parameter.empty:
                # Required parameter
                parts.append(f"{param_name} (required)")
            else:
                # Optional with default
                default = param.default
                if default is None:
                    parts.append(param_name)
                else:
                    parts.append(f"{param_name}={default}")

        return ", ".join(parts) if parts else ""
    except Exception:
        return ""


def get_registry_for_llm(
    categories: Optional[List[str]] = None,
    include_parameters: bool = True,
    include_use_cases: bool = True,
) -> str:
    """
    Format registry as context for LLM schema generation.

    Groups endpoints by category with descriptions, parameters, and use cases.
    Designed to be token-efficient while providing comprehensive information
    for LLM-powered data source selection.

    :param categories: Optional list of categories to include. If None, includes all.
    :param include_parameters: Whether to include parameter details. Default True.
    :param include_use_cases: Whether to include example use cases. Default True.
    :return: Markdown-formatted string suitable for LLM context.
    :example: get_registry_for_llm(categories=['financials', 'earnings'])
    :example: get_registry_for_llm(include_parameters=False)
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

            # GEN-93: Show both example AND parameters for completeness
            if include_parameters:
                if ep.example:
                    lines.append(f"**Example:** `{ep.example}`")
                # Always include parameters from function signature
                params = _format_parameters_from_function(ep.function)
                if params:
                    lines.append(f"**Parameters:** {params}")

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
    """
    Get a compact version of the registry for token-limited contexts.

    Returns a condensed view of all endpoints with truncated descriptions,
    ideal for contexts with limited token budgets while still providing
    endpoint discovery capabilities.

    :return: Compact markdown-formatted string with abbreviated endpoint info.
    :example: get_compact_registry_for_llm()
    """
    lines = ["# FMP DATA SOURCES (Compact)", ""]

    for cat, desc in CATEGORIES.items():
        endpoints = get_endpoints_by_category(cat)
        if not endpoints:
            continue

        lines.append(f"## {cat.upper()}: {desc}")
        for ep in endpoints:
            # GEN-93: Include both example AND parameters for completeness
            params = _format_parameters_from_function(ep.function)
            entry = f"- **{ep.name}**: {ep.description[:60]}..."
            if ep.example:
                entry += f" Ex: `{ep.example}`"
            if params:
                entry += f" Params: {params}"
            lines.append(entry)
        lines.append("")

    return "\n".join(lines)


def search_endpoints(query: str) -> List[FMPEndpoint]:
    """
    Search endpoints by keyword.

    Performs case-insensitive search across endpoint names, descriptions,
    categories, and use cases. Useful for finding relevant endpoints
    based on natural language queries.

    :param query: Search query string (e.g., 'income', 'earnings call', 'insider').
    :return: List of FMPEndpoint objects matching the search query.
    :example: search_endpoints('income statement')
    :example: search_endpoints('analyst')
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
