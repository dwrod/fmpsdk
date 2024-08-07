import typing
import os

from .general import __quotes
from .url_methods import __return_json_v3, __return_json_v4

API_KEY = os.getenv('FMP_API_KEY')

def available_efts():
    """
    Trying to avoid a breaking change.
    This method is misspelled so moving to a correct spelling method and deprecating this one.
    Use available_etfs() instead.
    :return:
    """
    print(
        "WARNING!  This is a deprecated method.  Use available_etfs() instead.  This will go away 20240101."
    )
    available_etfs()


def available_etfs() -> typing.Optional[typing.List[typing.Dict]]:
    """
    Query FMP /symbol/available-etfs/ API

    :return: A list of dictionaries.
    """
    path = f"symbol/available-etfs"
    query_vars = {"apikey": API_KEY}
    return __return_json_v3(path=path, query_vars=query_vars)


def etf_price_realtime() -> typing.Optional[typing.List[typing.Dict]]:
    """
    Query FMP /quotes/etf/ API

    All Real-time ETF Prices.

    :return: A list of dictionaries.
    """
    path = f"etf"
    return __quotes(apikey=API_KEY, value=path)


def etf_info(symbol: str) -> typing.Optional[typing.List[typing.Dict]]:
    """
    Query FMP /etf-info/ API

    All Real-time ETF Prices.

    :param symbol: ETF ticker.
    :return: A list of dictionaries.
    """
    path = f"etf-info"
    query_vars = {"symbol": symbol, "apikey": API_KEY}
    return __return_json_v4(path=path, query_vars=query_vars)