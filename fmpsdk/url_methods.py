import logging
import typing
import os

import requests

from .settings import (
    INDUSTRY_VALUES,
    PERIOD_VALUES,
    SECTOR_VALUES,
    SERIES_TYPE_VALUES,
    STATISTICS_TYPE_VALUES,
    TECHNICAL_INDICATORS_TIME_DELTA_VALUES,
    TIME_DELTA_VALUES,
    BASE_URL_v3,
    BASE_URL_v4,
    BASE_URL_stable,
)

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30

# Disable excessive DEBUG messages.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class FMPAPIError(Exception):
    """Custom exception for FMP API errors with structured information."""

    def __init__(self, message: str, status_code: int = None, url: str = None):
        self.message = message
        self.status_code = status_code
        self.url = url
        super().__init__(self.message)

    def __str__(self):
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.url:
            parts.append(f"URL: {self.url}")
        return " | ".join(parts)


def _check_api_key() -> bool:
    """
    Verify that FMP_API_KEY environment variable is set.

    :return: True if API key is set, False otherwise.
    :raises FMPAPIError: If API key is missing.
    """
    api_key = os.getenv('FMP_API_KEY')
    if not api_key:
        logging.error("FMP_API_KEY environment variable is not set")
        return False
    return True


def _handle_response(response: requests.Response, url: str) -> typing.Optional[typing.Union[typing.List, typing.Dict]]:
    """
    Handle HTTP response with proper status code checking and error handling.

    :param response: requests.Response object
    :param url: URL that was requested (for error messages)
    :return: Parsed JSON data or None on error
    :raises FMPAPIError: For API-specific errors that should be surfaced
    """
    # Check for HTTP errors
    if response.status_code == 401:
        logging.error(f"API authentication failed (401). Check your FMP_API_KEY. URL: {url}")
        return None
    elif response.status_code == 403:
        logging.error(f"API access forbidden (403). Your plan may not include this endpoint. URL: {url}")
        return None
    elif response.status_code == 404:
        logging.warning(f"Resource not found (404). Symbol or endpoint may not exist. URL: {url}")
        return None
    elif response.status_code == 429:
        logging.error(f"Rate limit exceeded (429). Too many requests. URL: {url}")
        return None
    elif response.status_code >= 500:
        logging.error(f"FMP server error ({response.status_code}). Try again later. URL: {url}")
        return None
    elif response.status_code != 200:
        logging.error(f"Unexpected HTTP status ({response.status_code}). URL: {url}")
        return None

    # Handle empty responses
    if len(response.content) == 0:
        logging.warning("Response appears to have no data. Returning empty List.")
        return []

    # Parse JSON with error handling
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}. URL: {url}")
        return None

    # Check for FMP API error messages in response
    if isinstance(data, dict):
        if "Error Message" in data:
            logging.error(f"FMP API Error: {data['Error Message']}. URL: {url}")
            return None
        if len(data.keys()) == 0:
            logging.warning("Response appears to have no data. Returning empty List.")
            return []

    return data


def __return_json_v3(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """
    Query URL for JSON response for v3 of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response, empty list on no data, or None on error
    """
    if not _check_api_key():
        return None

    url = f"{BASE_URL_v3}{path}"
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        return _handle_response(response, url)

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed: DNS failure, refused connection or other connection issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(f"Unexpected error during request to {url}: {e}")

    return None


def __return_json_v4(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """
    Query URL for JSON response for v4 of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response, empty list on no data, or None on error
    """
    if not _check_api_key():
        return None

    url = f"{BASE_URL_v4}{path}"
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        return _handle_response(response, url)

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed: DNS failure, refused connection or other connection issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(f"Unexpected error during request to {url}: {e}")

    return None


def __return_json_stable(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """
    Query URL for JSON response for FMP stable API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response, empty list on no data, or None on error
    """
    if not _check_api_key():
        return None

    url = f"{BASE_URL_stable}{path}"
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        return _handle_response(response, url)

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed: DNS failure, refused connection or other connection issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(f"Unexpected error during request to {url}: {e}")

    return None


def __validate_period(value: str) -> str:
    """
    Check to see if passed string is in the list of possible time periods.

    :param value: Period name.
    :return: Passed value if valid.
    :raises ValueError: If value is not a valid period.
    """
    valid_values = PERIOD_VALUES
    if value in valid_values:
        return value
    else:
        error_msg = f"Invalid period value: '{value}'. Valid options: {valid_values}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def __validate_sector(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Sectors.

    :param value: Sector name.
    :return: Passed value if valid.
    :raises ValueError: If value is not a valid sector.
    """
    valid_values = SECTOR_VALUES
    if value in valid_values:
        return value
    else:
        error_msg = f"Invalid sector value: '{value}'. Valid options: {valid_values}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def __validate_industry(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Industries.

    :param value: Industry name.
    :return: Passed value if valid.
    :raises ValueError: If value is not a valid industry.
    """
    valid_values = INDUSTRY_VALUES
    if value in valid_values:
        return value
    else:
        error_msg = f"Invalid industry value: '{value}'. Valid options: {valid_values}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def __validate_time_delta(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Time Deltas.

    :param value: Time Delta name.
    :return: Passed value if valid.
    :raises ValueError: If value is not a valid time delta.
    """
    valid_values = TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        error_msg = f"Invalid time_delta value: '{value}'. Valid options: {valid_values}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def __validate_series_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Series Type.

    :param value: Series Type name.
    :return: Passed value if valid.
    :raises ValueError: If value is not a valid series type.
    """
    valid_values = SERIES_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        error_msg = f"Invalid series_type value: '{value}'. Valid options: {valid_values}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def __validate_statistics_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Statistics Type.

    :param value: Statistics Type name.
    :return: Passed value if valid.
    :raises ValueError: If value is not a valid statistics type.
    """
    valid_values = STATISTICS_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        error_msg = f"Invalid statistics_type value: '{value}'. Valid options: {valid_values}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def __validate_technical_indicators_time_delta(value: str) -> str:
    """
    Exactly like set_time_delta() method but for technical indicators.

    :param value: Indicators Time Delta name.
    :return: Passed value if valid.
    :raises ValueError: If value is not a valid technical indicators time delta.
    """
    valid_values = TECHNICAL_INDICATORS_TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        error_msg = f"Invalid time_delta value: '{value}'. Valid options: {valid_values}"
        logging.error(error_msg)
        raise ValueError(error_msg)
