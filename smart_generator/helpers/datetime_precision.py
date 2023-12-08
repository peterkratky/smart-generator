from ..descriptor.enums import (DatePrecisionType, DatetimePrecisionType,
                                TimePrecisionType)


def datetime_precision_to_numpy_label(precision):
    """
    Converts a datetime precision to a numpy label.

    Args:
        precision (DatetimePrecisionType): The datetime precision.

    Returns:
        str: The numpy label.
    """
    if precision == DatetimePrecisionType.YEAR:
        return "Y"
    elif precision == DatetimePrecisionType.MONTH:
        return "M"
    elif precision == DatetimePrecisionType.WEEK:
        return "W"
    elif precision == DatetimePrecisionType.DAY:
        return "D"
    elif precision == DatetimePrecisionType.HOUR:
        return "h"
    elif precision == DatetimePrecisionType.MINUTE:
        return "m"
    elif precision == DatetimePrecisionType.SECOND:
        return "s"
    elif precision == DatetimePrecisionType.MILLISECOND:
        return "ms"


def date_precision_to_numpy_label(precision):
    """
    Converts a date precision to a numpy label.

    Args:
        precision (DatePrecisionType): The date precision.

    Returns:
        str: The numpy label.
    """
    if precision == DatePrecisionType.YEAR:
        return "Y"
    elif precision == DatePrecisionType.MONTH:
        return "M"
    elif precision == DatePrecisionType.WEEK:
        return "W"
    elif precision == DatePrecisionType.DAY:
        return "D"


def time_precision_to_numpy_label(precision):
    """
    Converts a time precision to a numpy label.

    Args:
        precision (TimePrecisionType): The time precision.

    Returns:
        str: The numpy label.
    """
    if precision == TimePrecisionType.HOUR:
        return "h"
    elif precision == TimePrecisionType.MINUTE:
        return "m"
    elif precision == TimePrecisionType.SECOND:
        return "s"
    elif precision == TimePrecisionType.MILLISECOND:
        return "ms"
