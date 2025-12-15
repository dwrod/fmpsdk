import logging
import typing
import os
import requests

from .settings import DEFAULT_LIMIT, SEC_RSS_FEEDS_FILENAME, BASE_URL_v3
from .url_methods import __return_json_v3, __return_json_v4
from .data_compression import format_output

API_KEY = os.getenv('FMP_API_KEY')

def institutional_holders(
    symbol: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve institutional holders for a specific company.

    Provides information on major institutional investors holding the company's stock.
    Useful for understanding institutional ownership and potential market influences.

    :param symbol: Company ticker symbol (e.g., 'AAPL').
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with institutional holder data.
    :example: institutional_holders('AAPL')
    """
    path = f"institutional-holder/{symbol}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def mutual_fund_holders(
    symbol: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve mutual fund holders for a specific company.

    Provides information on mutual funds holding the company's stock.
    Useful for understanding mutual fund ownership and investment trends.

    :param symbol: Company ticker symbol (e.g., 'AAPL').
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with mutual fund holder data.
    :example: mutual_fund_holders('AAPL')
    """
    path = f"mutual-fund-holder/{symbol}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def etf_holders(
    symbol: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve ETF holders for a specific company.

    Provides information on ETFs holding the company's stock.
    Useful for understanding ETF ownership and potential market impacts.

    :param symbol: Company ticker symbol (e.g., 'AAPL').
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with ETF holder data.
    :example: etf_holders('AAPL')
    """
    path = f"etf-holder/{symbol}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def etf_sector_weightings(
    symbol: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve sector weightings for a specific ETF.

    Provides a breakdown of the percentage of an ETF's assets invested in each sector.
    Useful for understanding ETF risk profiles, sector exposure, and portfolio diversification.

    :param symbol: ETF ticker symbol (e.g., 'SPY').
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with sector weighting data.
    :example: etf_sector_weightings('SPY')
    """
    path = f"etf-sector-weightings/{symbol}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def etf_country_weightings(
    symbol: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Retrieve country weightings for a specific ETF.

    Provides a breakdown of the percentage of an ETF's assets invested in each country.
    Useful for understanding geographic exposure, identifying country-specific
    investment opportunities, and diversifying portfolios.

    :param symbol: ETF ticker symbol (e.g., 'QDVE.DE').
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with country weighting data.
    :example: etf_country_weightings('QDVE.DE')
    """
    path = f"etf-country-weightings/{symbol}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def sec_rss_feeds(
    limit: int = DEFAULT_LIMIT,
    download: bool = False,
    filename: str = SEC_RSS_FEEDS_FILENAME,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Query FMP /rss_feed/ API.

    :param limit: Number of rows to return.
    :param download: True/False
    :param filename: Name of saved file.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with SEC RSS feed data, or None if downloading.
    """
    path = f"rss_feed"
    query_vars = {"apikey": API_KEY}
    if download:
        query_vars["datatype"] = "csv"  # Only CSV is supported.
        response = requests.get(f"{BASE_URL_v3}{path}", params=query_vars)
        with open(filename, "wb") as f:
            f.write(response.content)
        return None
    else:
        query_vars["limit"] = limit
        result = __return_json_v3(path=path, query_vars=query_vars)
        return format_output(result, output)

def cik_list(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /cik_list/ API.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with CIK data.
    """
    path = f"cik_list"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def cik_search(
    name: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /cik-search/ API.

    FORM 13F cik search by name
    :param name: Name
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with CIK search results.
    """
    path = f"cik-search/{name}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def cik(
    cik_id: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /cik/ API.

    FORM 13F get company name by cik
    :param cik_id: CIK value
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with company name data.
    """
    path = f"cik/{cik_id}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def form_13f(
    cik_id: str,
    date: str = None,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /form-thirteen/ API.

    FORM 13F statements provides position-level report of all institutional investment managers with more than $100m
    in assets under management.
    :param cik_id: CIK value
    :param date: 'YYYY-MM-DD'
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with FORM 13F data.
    """
    path = f"form-thirteen/{cik_id}"
    query_vars = {"apikey": API_KEY}
    if date:
        query_vars["date"] = date
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def cusip(
    cik_id: str,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /cusip/ API.

    Cusip mapper
    :param cik_id: CIK value
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with CUSIP data.
    """
    path = f"cusip/{cik_id}"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def institutional_symbol_ownership(
    symbol: str,
    limit: int,
    includeCurrentQuarter: bool = False,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /institutional-ownership/symbol-ownership API.

    :param symbol: Company ticker.
    :param limit: up to how many quarterly reports to return.
    :param includeCurrentQuarter: Whether to include any available data in the current quarter.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: List of dicts or formatted string with institutional symbol ownership data.
    """
    path = f"institutional-ownership/symbol-ownership"
    query_vars = {
        "symbol": symbol,
        "apikey": API_KEY,
        "includeCurrentQuarter": includeCurrentQuarter,
        "limit": limit,
    }
    result = __return_json_v4(path=path, query_vars=query_vars)
    return format_output(result, output)