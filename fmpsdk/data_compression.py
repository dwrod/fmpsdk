import typing
from decimal import Decimal, ROUND_HALF_UP

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