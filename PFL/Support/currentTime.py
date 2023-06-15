from datetime import datetime


def currentTime(format_str=None):
    """
The currentTime function returns the current time in a specified format.

Args:
    format_str: Format the date and time in a specific way

Returns:
    The current time as a string

Doc Author:
    Willem van der Schans
    """
    if format_str is not None:
        return datetime.now().strftime(format_str)
    else:
        return datetime.now()
