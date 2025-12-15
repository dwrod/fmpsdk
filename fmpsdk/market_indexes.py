import logging
import typing
import os
import requests

from .settings import (
    DOWJONES_CONSTITUENTS_FILENAME,
    NASDAQ_CONSTITUENTS_FILENAME,
    SP500_CONSTITUENTS_FILENAME,
    BASE_URL_v3,
)
from .url_methods import __return_json_v3
from .data_compression import format_output

API_KEY = os.getenv('FMP_API_KEY')

def indexes(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str]:
    """
    Query FMP /quotes/index API for major stock market indices.

    Retrieves a list of all major stock market indices, such as the S&P 500, 
    the Dow Jones Industrial Average, and the Nasdaq Composite Index and 
    returns their performance.
 
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: Index data in the specified format.
    :example: indexes(output='markdown')
    """
    path = "quotes/index"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    
    return format_output(result, output)

def sp500_constituent(
    download: bool = False,
    filename: str = SP500_CONSTITUENTS_FILENAME,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Query FMP /sp500_constituent/ API

    :param download: True/False
    :param filename: Name of saved file.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: SP500 constituent data in the specified format.
    """
    path = f"sp500_constituent"
    query_vars = {"apikey": API_KEY}
    if download:
        query_vars["datatype"] = "csv"  # Only CSV is supported.
        response = requests.get(f"{BASE_URL_v3}{path}", params=query_vars)
        with open(filename, "wb") as f:
            f.write(response.content)
        logging.info(f"Saving SP500 Constituents as {filename}.")
        return None
    else:
        result = __return_json_v3(path=path, query_vars=query_vars)
        return format_output(result, output)

def historical_sp500_constituent(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Query FMP /historical/sp500_constituent/ API.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: Historical SP500 constituent data in the specified format.
    """
    path = f"historical/sp500_constituent"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def nasdaq_constituent(
    download: bool = False,
    filename: str = NASDAQ_CONSTITUENTS_FILENAME,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Query FMP /nasdaq_constituent/ API

    :param download: True/False
    :param filename: Name of saved file.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: NASDAQ constituent data in the specified format.
    """
    path = f"nasdaq_constituent"
    query_vars = {"apikey": API_KEY}
    if download:
        query_vars["datatype"] = "csv"  # Only CSV is supported.
        response = requests.get(f"{BASE_URL_v3}{path}", params=query_vars)
        with open(filename, "wb") as f:
            f.write(response.content)
        logging.info(f"Saving NASDAQ Constituents as {filename}.")
        return None
    else:
        result = __return_json_v3(path=path, query_vars=query_vars)
        return format_output(result, output)

def historical_nasdaq_constituent(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Query FMP /historical/nasdaq_constituent/ API.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: Historical NASDAQ constituent data in the specified format.
    """
    path = f"historical/nasdaq_constituent"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)

def dowjones_constituent(
    download: bool = False,
    filename: str = DOWJONES_CONSTITUENTS_FILENAME,
    output: str = 'markdown'
) -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Query FMP /dowjones_constituent/ API

    :param download: True/False
    :param filename: Name of saved file.
    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: Dow Jones constituent data in the specified format.
    """
    path = f"dowjones_constituent"
    query_vars = {"apikey": API_KEY}
    if download:
        query_vars["datatype"] = "csv"  # Only CSV is supported.
        response = requests.get(f"{BASE_URL_v3}{path}", params=query_vars)
        with open(filename, "wb") as f:
            f.write(response.content)
        logging.info(f"Saving DOWJONES Constituents as {filename}.")
        return None
    else:
        result = __return_json_v3(path=path, query_vars=query_vars)
        return format_output(result, output)

def historical_dowjones_constituent(output: str = 'markdown') -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Query FMP /historical/dowjones_constituent/ API.

    :param output: Output format ('tsv', 'json', or 'markdown'). Defaults to 'markdown'.
    :return: Historical Dow Jones constituent data in the specified format.
    """
    path = f"historical/dowjones_constituent"
    query_vars = {"apikey": API_KEY}
    result = __return_json_v3(path=path, query_vars=query_vars)
    return format_output(result, output)