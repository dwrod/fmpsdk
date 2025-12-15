import typing
import os
from .settings import DEFAULT_LIMIT
from .url_methods import __return_json_v3, __return_json_v4, __return_json_stable
from datetime import date
from .data_compression import format_output

API_KEY = os.getenv('FMP_API_KEY')

def actives(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve a list of the most actively traded stocks on a given day.

    Provides information on stocks with the highest trading volume,
    indicating high market interest or significant news events. This data
    can be used to identify liquid stocks and potential trading opportunities.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with data on most active stocks.
    :example: actives()

    Each entry in the returned data contains details such as:
    - symbol: The stock's ticker symbol
    - name: The company name
    - change: Price change
    - price: Current stock price
    - changesPercentage: Percentage change in price
    - volume: Trading volume
    """
    path = f"actives"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def gainers(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve a list of stocks that have gained the most value on a given day.

    Provides insights into stocks with positive momentum, helping identify
    potential investment opportunities. Useful for traders looking for
    stocks with upward trends or significant price movements.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with data on biggest gainers.
    :example: gainers()
    """
    path = f"gainers"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def losers(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve a list of stocks that have lost the most value on a given day.

    Provides insights into stocks with negative momentum, helping identify
    underperforming stocks and potential trading opportunities. This data
    can be used to assess market sentiment and identify stocks that may
    continue to depreciate.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with data on biggest losers.
    :example: losers()
    """
    path = f"losers"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def market_hours(output: str = 'markdown') -> typing.Union[typing.Dict, str]:
    """
    Retrieve information about market hours for various exchanges.

    Provides data on opening and closing times for different stock markets,
    helping traders plan their activities around market schedules.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: Dict or formatted string with market hours data.
    :example: market_hours()
    """
    path = f"market-hours"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    
    if result is not None:
        return format_output([result], output)
    return result

def sectors_performance(
    limit: int = DEFAULT_LIMIT,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve performance data for various market sectors.

    Provides insights into sector-specific performance, helping investors
    identify trends and make informed decisions about sector allocation.

    :param limit: Number of records to retrieve. Default is DEFAULT_LIMIT.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with sector performance data.
    :example: sectors_performance(limit=5)
    """
    path = f"sectors-performance"
    query_vars = {"apikey": API_KEY, "limit": limit}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def fail_to_deliver(symbol: str, page: int = 0, output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /fail_to_deliver API for fail to deliver data.

    :param symbol: Company ticker symbol.
    :param page: Page number for pagination (default is 0).
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string containing fail to deliver data.
    :example: fail_to_deliver('AAPL', page=1)
    """
    path = "fail_to_deliver"
    query_vars = {
        "apikey": API_KEY,
        "symbol": symbol,
        "page": page
    }
    result = __return_json_v4(path=path, query_vars=query_vars)
    return format_output(result, output)

def sector_pe_ratio(date: date, exchange: str = "NYSE", 
                    output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /sector_price_earning_ratio API.

    :param date: The date for which to retrieve the sector PE ratios in 'yyyy-mm-dd' format.
    :param exchange: The stock exchange (default is NYSE).
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string containing sector PE ratios.
    :example: sector_pe_ratio('2023-01-01', exchange='NASDAQ')
    """
    path = f"sector_price_earning_ratio"
    query_vars = {
        "date": date,
        "exchange": exchange,
        "apikey": API_KEY
    }
    result = __return_json_v4(path=path, query_vars=query_vars)
    return format_output(result, output)

def industry_pe_ratio(date: str, exchange: str = "NYSE", 
                      output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve industry-specific price-to-earnings (PE) ratios.

    Provides PE ratios for various industries in the stock market, helping to
    identify potentially overvalued or undervalued sectors. This data is useful
    for comparing valuations across different industries and making informed
    investment decisions.

    :param date: Date for which to retrieve industry PE ratios (format: 'YYYY-MM-DD').
    :param exchange: Stock exchange (default is NYSE).
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string containing industry PE ratios.
    :example: industry_pe_ratio('2024-08-01', exchange='NYSE')

    Data can be used to:
    - Compare PE ratios across industries
    - Identify potential investment opportunities
    - Assess relative valuations within the market
    """
    path = "industry_price_earning_ratio"
    query_vars = {
        "date": date, 
        "exchange": exchange,
        "apikey": API_KEY
    }
    result = __return_json_v4(path=path, query_vars=query_vars)
    return format_output(result, output)

def batch_eod_prices(date: str, 
                     output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Get batch request that contains all end of day prices for a specific date.

    :param date: The date in format YYYY-MM-DD
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string containing EOD prices for multiple stocks
    """
    path = "batch-request-end-of-day-prices"
    query_vars = {"apikey": API_KEY, "date": date}
    result = __return_json_v4(path=path, query_vars=query_vars)
    return format_output(result, output)

def multiple_company_prices(
    symbols: typing.Union[str, typing.List[str]],
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve real-time price data for multiple companies in a single request.

    Provides key information such as current price, change, percent change,
    day low/high, year low/high, market cap, volume, and more for each symbol.
    Useful for tracking multiple stocks efficiently.

    :param symbols: Single stock symbol as string or list of stock symbols
                    (e.g., 'AAPL' or ['AAPL', 'MSFT'])
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with price information for the requested symbols
    :example: multiple_company_prices('AAPL,MSFT')
              multiple_company_prices(['AAPL', 'MSFT'])
    """
    symbols_str = ','.join(symbols) if isinstance(symbols, list) else symbols
    path = f"quote/{symbols_str}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def historical_sectors_performance(from_date: str,
                                   to_date: str,
                                   output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve historical performance data for stock market sectors.

    Provides insights into sector trends over time, helping investors identify
    patterns and make informed decisions. Useful for comparing sector
    performance and spotting potential investment opportunities.

    :param from_date: Start date in format YYYY-MM-DD.
    :param to_date: End date in format YYYY-MM-DD.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with historical sector performance data,
             including date and performance for each sector.
    :example: historical_sectors_performance('2024-01-01', '2024-03-01')
    """
    path = "historical-sectors-performance"
    query_vars = {
        "apikey": API_KEY,
        "from": from_date,
        "to": to_date
    }
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)


def industry_performance_snapshot(
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve a snapshot of performance for all market industries.

    Provides current performance metrics for each industry sector,
    including change percentages and other key indicators. Useful for
    identifying outperforming or underperforming industries.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with industry performance data.
    :example: industry_performance_snapshot()
    """
    path = "industry-performance-snapshot"
    query_vars = {"apikey": API_KEY}
    result = __return_json_stable(path=path, query_vars=query_vars)
    return format_output(result, output)


def holidays_by_exchange(
    exchange: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve market holidays for a specific exchange.

    Provides a list of dates when the exchange is closed for holidays,
    useful for planning trading activities and understanding market schedules.

    :param exchange: Exchange name (e.g., 'NASDAQ', 'NYSE').
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with holiday dates and names.
    :example: holidays_by_exchange('NASDAQ')
    """
    path = "holidays-by-exchange"
    query_vars = {"apikey": API_KEY, "exchange": exchange}
    result = __return_json_stable(path=path, query_vars=query_vars)
    return format_output(result, output)