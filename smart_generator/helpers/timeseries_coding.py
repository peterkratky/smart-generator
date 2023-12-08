from datetime import date, datetime

from ..templates.template_table import TimeseriesUnit


def encode_timestamp(
    timestamp: [datetime, date], frame: TimeseriesUnit, unit: TimeseriesUnit
):
    """
    Encodes a timestamp to a number within the specified frame and a time unit. This is
    used to encode timestamps to a generic number representing a certain point of time
    in the timeseries. It takes into consideration day of week, so this way we can
    encode weekend data regardless of the year. In the context of this library, this
    help to generate timeseries from templates in an arbitrary time frame.

    Args:
        timestamp (datetime): The timestamp to encode.
        frame (TimeseriesUnit): The frame of the timeseries.
        unit (TimeseriesUnit): The unit of the timeseries.

    Returns:
        tuple[int, int]: Tuple of the encoded timestamp and the period of the frame.

    Raises:
        NotImplementedError: If the conversion for timeseries unit is not implemented
            for the given time frame and unit.
    """
    result = None
    result_period = None
    if frame == TimeseriesUnit.YEAR:
        week_of_year = timestamp.isocalendar()[1] - 1 % 53
        if unit == TimeseriesUnit.WEEK:
            result = week_of_year
            result_period = 53
        elif unit == TimeseriesUnit.DAY:
            result = week_of_year * 7 + (timestamp.weekday())
            result_period = 53 * 7
        elif unit == TimeseriesUnit.HOUR:
            result = week_of_year * 7 * 24 + (timestamp.weekday() * 24)
            if type(timestamp) == datetime:
                result = result + timestamp.hour
            result_period = 53 * 7 * 24
        else:
            raise NotImplementedError(
                f"Not implemented for frame {frame} and unit {unit}"
            )

    elif frame == TimeseriesUnit.MONTH:
        coarsed_timestamp = timestamp.replace(day=1)
        week_of_month = (
            (timestamp.isocalendar()[1] - 1 % 53)
            - (coarsed_timestamp.isocalendar()[1] - 1 % 53)
        ) % 6
        if unit == TimeseriesUnit.WEEK:
            result = week_of_month
            result_period = 6
        elif unit == TimeseriesUnit.DAY:
            result = week_of_month * 7 + (timestamp.weekday())
            result_period = 6 * 7
        elif unit == TimeseriesUnit.HOUR:
            result = week_of_month * 7 * 24 + (timestamp.weekday() * 24)
            if type(timestamp) == datetime:
                result = result + timestamp.hour
            result_period = 6 * 7 * 24
        else:
            raise NotImplementedError(
                f"Not implemented for frame {frame} and unit {unit}"
            )

    elif frame == TimeseriesUnit.WEEK:
        day_of_week = timestamp.weekday()
        if unit == TimeseriesUnit.DAY:
            result = day_of_week
            result_period = 7
        elif unit == TimeseriesUnit.HOUR:
            result = day_of_week * 24
            if type(timestamp) == datetime:
                result = result + timestamp.hour
            result_period = 7 * 24
        else:
            raise NotImplementedError(
                f"Not implemented for frame {frame} and unit {unit}"
            )

    elif frame == TimeseriesUnit.DAY:
        if unit == TimeseriesUnit.HOUR:
            if type(timestamp) == datetime:
                result = timestamp.hour
            else:
                result = 0
            result_period = 24
        else:
            raise NotImplementedError(
                f"Not implemented for frame {frame} and unit {unit}"
            )

    else:
        raise NotImplementedError(f"Not implemented for frame {frame}")

    return result, result_period


def convert_step_to_millis(step: TimeseriesUnit):
    """
    Converts a timeseries unit to milliseconds.

    Args:
        step (TimeseriesUnit): The timeseries unit.

    Returns:
        int: The number of milliseconds.

    Raises:
        NotImplementedError: If the conversion for timeseries unit is not implemented.
    """
    if step == TimeseriesUnit.MILLISECOND:
        return 1
    elif step == TimeseriesUnit.SECOND:
        return 1000
    elif step == TimeseriesUnit.MINUTE:
        return 1000 * 60
    elif step == TimeseriesUnit.HOUR:
        return 1000 * 60 * 60
    elif step == TimeseriesUnit.DAY:
        return 1000 * 60 * 60 * 24
    elif step == TimeseriesUnit.WEEK:
        return 1000 * 60 * 60 * 24 * 7
    else:
        raise NotImplementedError(f"Not implemented for step {step}")
