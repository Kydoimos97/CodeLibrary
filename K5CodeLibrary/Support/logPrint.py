import inspect
import os
from datetime import datetime


# noinspection PyBroadException
def logPrint(return_string, log_type="l", include_time=True, seperator=False):
    """
The logPrint function is a simple function that prints out the input string with some additional information.
The additional information includes:
    - The time of the print (if specified)
    - The file and line number where it was called from (always included)
    - A log type, which can be one of three options: LOG, WARNING or ERROR. This will change the color of the output text to match its type.

Args:
    return_string: Print the string that is passed to it
    log_type: Specify the type of log message
    include_time: Include the time in the log string
    seperator: Print a seperator line in the console

Returns:
    A string, which is the log_string

Doc Author:
    Willem van der Schans
"""
    caller_file = inspect.stack()
    caller_file = caller_file[len(caller_file) - 1]
    caller_file = f"{str(os.path.basename(caller_file.filename))}:{caller_file.lineno}"
    log_type_str = str(log_type).upper()
    invalid_flag = False
    time_inp = include_time
    seperator_inp = seperator

    if seperator_inp:
        time_inp = False

    if log_type_str in ["LOG", "WARNING", "ERROR", "L", "W", "E", "NONE"]:
        if "LOG" in log_type_str or "L" in log_type_str:
            log_type_str = "LOG:    "
        elif "WARNING" in log_type_str or "W" in log_type_str:
            log_type_str = "WARNING:"
        elif "ERROR" in log_type_str or "E" in log_type_str:
            log_type_str = "ERROR:  "
        elif log_type_str == "NONE":
            log_type_str = ""
        else:
            invalid_flag = True
    else:
        invalid_flag = True

    if log_type_str == "":
        log_string = f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {caller_file} | {return_string}"
    elif time_inp:
        log_string = f"{log_type_str} {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {caller_file} | {return_string}"
    elif seperator_inp:
        log_string = f"\n{'-' * 10}{return_string}{'-' * 10}"
    else:
        log_string = f"{log_type_str} {caller_file} | {return_string}"

    if invalid_flag:
        print(log_string)
        warning_string = f"WARNING: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | logPrint.py:XX | Invalid input for log type"
        print(warning_string)
        return log_string, warning_string
    else:
        print(log_string)
        return log_string