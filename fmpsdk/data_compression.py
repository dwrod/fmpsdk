import typing
from decimal import Decimal, ROUND_HALF_UP
import csv
import io
import json
import re
from typing import List, Dict, Any, Tuple

def compress_json_to_tuples(
    result: typing.List[typing.Dict],
    condensed: bool = True,
    fields: typing.Optional[typing.Tuple[str, ...]] = None
) -> typing.Union[typing.List[typing.Dict], typing.Tuple[typing.Tuple[str, ...], ...]]:
    """
    Compress JSON data into machine-readable tuples of tuples.

    :param result: List of dictionaries containing JSON data
    :param condensed: If True, return tuple of tuples; else, list of dicts (default: True)
    :param fields: Optional tuple of field names to include in the output
    :return: Compressed data as tuple of tuples or original list of dicts
    """
    if result is not None and condensed:
        if result:
            if fields is None:
                # Get all unique keys from the result if fields are not specified
                fields = tuple(set(key for entry in result for key in entry.keys()))
            
            # Convert each entry to a tuple, preserving order of fields
            compact_result = tuple(
                tuple(str(entry.get(field, '')) for field in fields)
                for entry in result
            )
            
            return (fields,) + compact_result
        else:
            return ((),)  # Return an empty tuple of tuples if result is empty
    else:
        return result

def apply_precision(
    data: typing.Union[typing.List[typing.Dict], typing.Dict],
    precision: typing.Optional[int]
) -> typing.Union[typing.List[typing.Dict], typing.Dict]:
    """
    Apply precision rounding to numeric values in a dictionary or list of dictionaries.
    Maintains original precision if less than specified precision.

    :param data: Input data (dictionary or list of dictionaries)
    :param precision: Maximum number of decimal places to round to, or None for full precision
    :return: Data with numeric values rounded to specified precision or original precision
    """
    if precision is None:
        return data

    def round_value(value):
        if isinstance(value, (int, float)):
            # Convert to string to check original decimal places
            str_value = str(value)
            decimal_places = len(str_value.split('.')[-1]) if '.' in str_value else 0
            
            # Use the minimum of original decimal places and specified precision
            actual_precision = min(decimal_places, precision)
            
            if actual_precision > 0:
                return str(Decimal(str_value).quantize(Decimal(f'1.{"0" * actual_precision}'), 
                                                       rounding=ROUND_HALF_UP))
            else:
                return str(int(value))  # Return as integer if no decimal places
        return value

    if isinstance(data, list):
        return [apply_precision(item, precision) for item in data]
    elif isinstance(data, dict):
        return {key: round_value(value) for key, value in data.items()}
    else:
        return data

def compress_json_to_tsv(json_data: List[Dict[str, Any]], 
                         fields: Tuple[str, ...] = None) -> str:
    """
    Compress JSON data into TSV format for efficient LLM consumption.
    
    Args:
    json_data (List[Dict[str, Any]]): List of dictionaries containing the data.
    fields (Tuple[str, ...]): Tuple of field names to include in the output. If None, all fields are included.
    
    Returns:
    str: TSV formatted string of the compressed data.
    """
    if not json_data:
        return ""

    # Use specified fields if provided, otherwise use all keys from the first dictionary
    fieldnames = fields if fields else list(json_data[0].keys())

    # Create a StringIO object to write TSV data
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, 
                            delimiter='\t', extrasaction='ignore', 
                            lineterminator='\n')

    # Write the header
    writer.writeheader()

    # Write the rows
    for row in json_data:
        writer.writerow({field: row.get(field, '') for field in fieldnames})

    # Get the TSV string and remove any trailing newline
    tsv_string = output.getvalue().rstrip('\n')
    
    return tsv_string

def clean_html_content(soup):
    """
    Clean HTML content by removing scripts, styles, attributes, and unrecognized characters.

    :param soup: BeautifulSoup object containing HTML content.
    :return: Cleaned text content.
    """
    for script in soup(["script", "style"]):
        script.decompose()

    for tag in soup.recursiveChildGenerator():
        if hasattr(tag, 'attrs'):
            tag.attrs = {}

    text = soup.get_text()
    
    # Remove non-breaking spaces and other common unrecognized characters
    text = text.replace('\xa0', ' ')
    text = text.replace('\u200b', '')  # Zero-width space
    text = text.replace('\u2028', '\n')  # Line separator
    text = text.replace('\u2029', '\n\n')  # Paragraph separator

    # Replace multiple spaces with a single space
    text = ' '.join(text.split())

    # Remove any remaining non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char in ['\n', '\t'])

    # Clean up financial data formatting
    text = re.sub(r'(\$?\d+(?:,\d{3})*(?:\.\d+)?)\s*', r'\1 ', text)
    
    # Remove any leftover Unicode characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Clean up newlines and spaces
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

def _escape_markdown_cell(value: str) -> str:
    """
    Escape special characters in markdown table cell content.

    Handles pipe characters and newlines that would break table structure.

    :param value: Raw cell value.
    :return: Escaped value safe for markdown tables.
    """
    if not isinstance(value, str):
        value = str(value)
    # Escape pipe characters (would break table structure)
    value = value.replace('|', '\\|')
    # Replace newlines with space (would break table rows)
    value = value.replace('\n', ' ').replace('\r', '')
    return value


def compress_json_to_markdown(json_data: List[Dict[str, Any]],
                              fields: Tuple[str, ...] = None) -> str:
    """
    Compress JSON data into markdown-formatted tables for efficient LLM consumption.

    Properly escapes pipe characters and newlines in cell values to prevent
    malformed tables that could cause LLM parsing errors.

    Args:
    json_data (List[Dict[str, Any]]): List of dictionaries containing the data.
    fields (Tuple[str, ...]): Tuple of field names to include in the output. If None, all fields are included.

    Returns:
    str: Markdown formatted string of the compressed data.
    """
    if not json_data:
        return ""

    # Use specified fields if provided, otherwise use all keys from the first dictionary
    fieldnames = fields if fields else list(json_data[0].keys())

    # Escape field names for header (unlikely but defensive)
    escaped_fieldnames = [_escape_markdown_cell(f) for f in fieldnames]

    # Create the header row
    header = "| " + " | ".join(escaped_fieldnames) + " |"
    separator = "| " + " | ".join(["---" for _ in fieldnames]) + " |"

    # Create the data rows with escaped values
    rows = []
    for row in json_data:
        row_data = [_escape_markdown_cell(str(row.get(field, ''))) for field in fieldnames]
        rows.append("| " + " | ".join(row_data) + " |")

    # Combine all parts of the markdown table
    markdown_table = "\n".join([header, separator] + rows)

    return markdown_table

def format_output(data: List[Dict[str, Any]], output: str, 
                  fields: Tuple[str, ...] = None) -> typing.Union[typing.List[typing.Dict], str, None]:
    """
    Format the output data based on the specified format.

    Args:
    data (List[Dict[str, Any]]): List of dictionaries containing the data.
    output (str): Desired output format ('tsv', 'json', or 'markdown').
    fields (Tuple[str, ...]): Optional tuple of field names to include in the output.

    Returns:
    str: Formatted output string.
    """
    if output == 'tsv':
        return compress_json_to_tsv(data, fields)
    elif output == 'markdown':
        return compress_json_to_markdown(data, fields)
    elif output == 'json':
        return data
    else:
        raise ValueError(f"Unsupported output format: {output}. Supported formats are 'tsv', 'json', and 'markdown'.")